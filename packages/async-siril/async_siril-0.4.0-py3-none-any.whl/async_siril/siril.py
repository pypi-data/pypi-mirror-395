import asyncio
import asyncio.subprocess
import structlog.stdlib
import os
import platform
import subprocess
import typing as t

from .command import BaseCommand, setcpu, set as siril_set, capabilities
from .command_types import SirilSetting
from .event import AsyncSirilEventConsumer, AsyncSirilCommandProducer
from .resources import SirilResource
from pathlib import Path


logger = structlog.stdlib.get_logger("async_siril")


class SirilError(Exception):
    """Base class for Siril errors and exceptions"""

    def __init__(self, cmd: str, message: str):
        self.command = cmd
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"SirilError from command: `{self.command}` error: `{self.message}`"


class SirilCli(object):
    """
    Main class for interacting with Siril using the async context manager pattern

    async with SirilCli() as siril:
        await siril.command("stack")
    """

    def __init__(
        self,
        siril_exe: str = "siril-cli",
        directory: t.Optional[Path] = None,
        resources: SirilResource = SirilResource.default_limits(),
    ):
        self._siril_exe = self._find_siril_cli(siril_exe)
        logger.info("Found Siril CLI executable: %s", self._siril_exe)

        self._cwd = directory
        self._resources = resources

        self._process: t.Optional[asyncio.subprocess.Process] = None
        self._consumer = AsyncSirilEventConsumer()
        self._producer = AsyncSirilCommandProducer()
        self._log_tasks = []

        # Get the version of the executable
        output = subprocess.Popen([self._siril_exe, "--version"], stdout=subprocess.PIPE)
        response, _ = output.communicate()
        self.version = response.decode().rstrip()
        logger.info("Found %s version: %s", self._siril_exe, self.version)

    async def _start(self):
        logger.debug("Initializing Siril CLI with Async Consumer & Producer")
        self._consumer.start()
        logger.debug("Siril CLI outpipe: %s", self._consumer.pipe_path)
        self._producer.start()
        logger.debug("Siril CLI inpipe: %s", self._producer.pipe_path)

        params = ["--pipe", "--inpipe", self._producer.pipe_path, "--outpipe", self._consumer.pipe_path]
        if self._cwd is not None:
            params.insert(0, "-d")
            params.insert(1, str(self._cwd))

        logger.info("Starting Siril CLI with params: %s", params)
        self._process = await asyncio.create_subprocess_exec(
            self._siril_exe,
            *params,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        logger.info("Siril CLI process started")

        # Start logging tasks in background
        self._log_tasks = [
            asyncio.create_task(self._log_stream(self._process.stdout, "stdout")),
            asyncio.create_task(self._log_stream(self._process.stderr, "stderr")),
        ]

        # Start reading and become ready when the CLI says so
        await self._consumer.siril_ready
        logger.info("Siril CLI is now ready for startup commands")

        # Call this command as the first thing we do for all sessions
        from .command import requires

        # Still needed as the first command to be called
        await self.command(requires("0.99.10"))
        if self._resources.cpu_limit is not None:
            await self.command(setcpu(self._resources.cpu_limit))
        if self._resources.memory_limit is not None:
            await self.set(SirilSetting.MEM_MODE, "1")
            await self.set(SirilSetting.MEM_AMOUNT, self._resources.memory_limit)

        await self.set(SirilSetting.MEM_RATIO, str(self._resources.memory_percent))
        await self.command(capabilities())
        logger.info("AsyncSiril is ready for additional commands")

    async def _stop(self):
        logger.info("Stopping AsyncSiril process")
        try:
            # Kill process first to break pipe connections and unblock I/O
            if self._process and self._process.returncode is None:
                self._process.kill()
                await self._process.wait()
                logger.info("Siril CLI Process killed")

            # Now stop consumer and producer - they should exit naturally since pipes are broken
            await self._consumer.stop()
            await self._producer.stop()

            # Cancel and wait for log tasks
            for task in self._log_tasks:
                if not task.done():
                    task.cancel()

            try:
                await asyncio.wait_for(asyncio.gather(*self._log_tasks, return_exceptions=True), timeout=1.0)
            except asyncio.TimeoutError:
                logger.warning("Log tasks did not cancel in time")
            logger.info("AsyncSiril Cleanup completed")
        except Exception as e:
            logger.error("error during close: %s" % e)

    async def _log_stream(self, stream, stream_name):
        """Read lines from a subprocess stream and log them via structlog."""
        try:
            while True:
                line = await stream.readline()
                if not line:
                    break
                decoded = line.decode().rstrip()
                logger.info("siril_output", stream=stream_name, message=decoded)
        except asyncio.CancelledError:
            logger.debug(f"Log stream {stream_name} cancelled")
            raise

    async def command(self, cmd: t.Union[str, t.List[str], BaseCommand, t.List[BaseCommand]]):
        """Will run a command on the Siril pipe and throw `SirilError`'s as it sees them."""

        def is_list_of_types(lst, _type):
            if lst and isinstance(lst, list):
                return all(isinstance(elem, _type) for elem in lst)
            else:
                return False

        if isinstance(cmd, str) or isinstance(cmd, BaseCommand):
            await self._run_command(str(cmd))
        elif is_list_of_types(cmd, str) or is_list_of_types(cmd, BaseCommand):
            for c in cmd:
                await self._run_command(str(c))
        else:
            logger.error("incorrect command type")

    async def failable_command(self, cmd: t.Union[str, BaseCommand]) -> bool:
        """Will run a command on the Siril pipe and return a bool result if successful (catching any errors)"""
        try:
            await self.command(cmd)
            return True
        except SirilError as siril_error:
            logger.warn(f"Error caught by failable_command: {str(siril_error)}")
            return False

    async def _run_command(self, _command: str):
        # Use the special command to close the wrapper
        if _command == "exit":
            await self.stop()
            return

        logger.info(f"running command: '{_command}'")

        # Write the command first
        await self._producer.send(_command)

        # Read it the events off the listening queue
        while True:
            result = await self._consumer.queue.get()
            self._consumer.queue.task_done()

            if result.errored:
                logger.info("result errored")
                raise SirilError(_command, result.message)

            if result.completed:
                logger.info("result completed")
                break

            if result.siril_ready:
                logger.info("siril ready")
                break
        logger.info("Command completed")

    async def set(self, key: SirilSetting, value: str | bool):
        """Set a Siril setting using the `set` command"""
        await self.command(siril_set(key=key, value=str(value).lower()))

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        from .command import exit

        await self.command(exit())

    async def start(self):
        """Manually start the Siril process and pipes"""
        await self._start()
        logger.info("SirilCli started")

    async def stop(self):
        """Manually stop the Siril process and pipes"""
        await self._stop()
        logger.info("SirilCli stopped")

    def _find_siril_cli(self, siril_exe: str = "siril-cli") -> str:
        """Find the path to the Siril CLI executable"""
        if os.path.exists(siril_exe):
            return siril_exe

        # Try to find Siril dynamically
        system = platform.system()
        possible_paths = []
        if system == "Windows":
            possible_paths.append("C:/msys64/mingw64/bin/siril-cli.exe")  # msys2 path when building locally
            possible_paths.append("C:/Program Files/SiriL/bin/siril-cli.exe")
        elif system == "Darwin":
            possible_paths.append("/Applications/Siril.app/Contents/MacOS/siril-cli")
            possible_paths.append("/Applications/Siril.app/Contents/MacOS/Siril")
        elif system == "Linux":
            possible_paths.append("/usr/local/bin/siril-cli")
            possible_paths.append("/usr/bin/siril-cli")

        for path in possible_paths:
            if os.path.exists(path):
                return path

        raise FileNotFoundError("Siril CLI executable not found")
