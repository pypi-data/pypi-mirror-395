import asyncio
import structlog.stdlib
import typing as t
import os
import re
import sys
from enum import Enum

logger = structlog.stdlib.get_logger("async_siril")


class SirilEvent:
    """
    Represents an event from the Siril CLI
    """

    LOG = "log"
    PROGRESS = "progress"
    STATUS = "status"

    def __init__(self, raw_string: str):
        self.status = None
        self.message = None
        self.progress = 0
        self._raw_string = raw_string

        if raw_string.startswith("status:"):
            self.value = SirilEvent.STATUS
            self._parse_status_output()
        elif raw_string.startswith("progress:"):
            self.value = SirilEvent.PROGRESS
            self._parse_progress_output()
        elif raw_string.startswith("log:"):
            self.value = SirilEvent.LOG
            self._parse_log_output()
        elif raw_string == "ready":
            self.value = SirilEvent.STATUS
            self._parse_ready_output()
        else:
            self.value = SirilEvent.LOG
            self.message = raw_string

    def __str__(self):
        return self._raw_string

    def _parse_status_output(self):
        matches = re.search(r"status\:\s(\S*)\s(.*)", self._raw_string)
        self.status = matches.group(1) if matches and matches.group(1) else None
        self.message = matches.group(2) if matches and matches.group(2) else None

    def _parse_log_output(self):
        matches = re.search(r"log\:\s(.*)", self._raw_string)
        self.message = matches.group(1) if matches and matches.group(1) else None

    def _parse_progress_output(self):
        matches = re.search(r"progress\:\s(\d*)", self._raw_string)
        self.progress = int(matches.group(1)) if matches and matches.group(1) else None

    def _parse_ready_output(self):
        self.status = self._raw_string

    @property
    def completed(self) -> bool:
        return self.status == "success" or self.status == "error" or self.status == "exit"

    @property
    def errored(self) -> bool:
        return self.status == "error"

    @property
    def siril_ready(self) -> bool:
        return self.status == "ready"


class AsyncSirilEventConsumer:
    """
    Represents the async reader of events from the Siril CLI
    """

    def __init__(self):
        self._loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue()
        self.fifo_closed = self._loop.create_future()
        self.siril_ready = self._loop.create_future()
        self._running = False
        self._pipe = PipeClient(mode=PipeMode.READ)

    @property
    def pipe_path(self):
        """Returns the path to the pipe"""
        return self._pipe.path

    def start(self):
        """Return a task that runs the consumer loop in the background."""
        self._running = True
        self._task = asyncio.create_task(self._run(), name=type(self).__name__)
        return self._task

    async def stop(self):
        """Gracefully stop the background reader."""
        if self._running:
            logger.info("Stopping consumer fifo pipe")
            self._running = False

        if self._task:
            logger.info("Cancelling consumer task")
            self._task.cancel()
            try:
                await asyncio.wait_for(self._task, timeout=1.0)
            except asyncio.TimeoutError:
                logger.warning("Consumer task did not cancel in time")
            except asyncio.CancelledError:
                pass
            except Exception as e:
                logger.warning(f"Error stopping consumer task: {e}")

        if self._pipe:
            self._pipe.close()
        logger.info("Consumer stopped")

    async def _run(self):
        """Main consumer loop that waits for writers and reads FIFO."""
        if not self._running:
            return

        try:
            logger.debug(f"consumer path: {self._pipe.path}")
            logger.debug(f"consumer readable: {True}")
            logger.debug(f"consumer writable: {False}")

            # Wait for the client to connect and create a stream (blocking)
            await self._pipe.connect()

            logger.info("Consumer fifo pipe opened")

            async for event in self._aiter_events():
                if event.siril_ready:
                    logger.info("Consumer received ready event")
                    self.siril_ready.set_result(None)
                else:
                    self.queue.put_nowait(event)

            logger.info("EOF from the consumer")
        except Exception as e:
            logger.info(f"Error in consumer task: {e}")
            await asyncio.sleep(1)

    async def _aiter_events(self) -> t.AsyncGenerator[SirilEvent, None]:
        """Asynchronously yield events from a blocking file object."""
        try:
            while self._running:
                line = await self._pipe.read_line()
                if line == "":
                    logger.info("Consumer fifo pipe closed")
                    if not self.fifo_closed.done():
                        self.fifo_closed.set_result(None)
                    break

                yield SirilEvent(line.rstrip())
        except asyncio.CancelledError:
            logger.debug("Consumer event iteration cancelled")
            raise


class AsyncSirilCommandProducer:
    """
    Represents the async writer of commands to the Siril CLI
    """

    def __init__(self):
        self._loop = asyncio.get_event_loop()
        self._queue = asyncio.Queue()
        self._task = None
        self._running = False
        self.fifo_closed = self._loop.create_future()
        self._pipe = PipeClient(mode=PipeMode.WRITE)

    @property
    def pipe_path(self):
        """Returns the path to the pipe"""
        return self._pipe.path

    def start(self):
        """Starts the background writer task."""
        self._running = True
        self._task = asyncio.create_task(self._run(), name=type(self).__name__)
        return self._task

    async def stop(self):
        """Gracefully stop the background writer."""
        if self._running:
            logger.info("Stopping producer fifo pipe")
            self._running = False
            if not self.fifo_closed.done():
                self.fifo_closed.set_result(None)

        if self._task:
            logger.info("Cancelling producer task")
            self._task.cancel()
            try:
                await asyncio.wait_for(self._task, timeout=1.0)
            except asyncio.TimeoutError:
                logger.warning("Producer task did not cancel in time")
            except asyncio.CancelledError:
                pass
            except Exception as e:
                logger.warning(f"Error stopping producer task: {e}")

        if self._pipe:
            self._pipe.close()
        logger.info("Producer stopped")

    async def send(self, command: str):
        """Send a message to be written to the FIFO."""
        await self._queue.put(command)

    async def _run(self):
        """Main producer loop that waits for messages and writes them to the FIFO."""
        if not self._running:
            return

        try:
            logger.debug(f"producer path: {self._pipe.path}")
            logger.debug(f"producer readable: {False}")
            logger.debug(f"producer writable: {True}")

            # Wait for the client to connect and create a stream (blocking)
            await self._pipe.connect()

            logger.info("Producer fifo pipe opened")

            while self._running:
                try:
                    message = await self._queue.get()
                    await self._pipe.write_line(message)
                except asyncio.CancelledError:
                    break
        finally:
            if self._pipe:
                self._pipe.close()

        logger.info("The producer was nicely stopped.")


class PipeMode(Enum):
    READ = "read"
    WRITE = "write"

    @property
    def default_path(self):
        if sys.platform == "win32":
            # Have to use the standard names only on windows
            custom_read_pipe_name = r"\\.\pipe\siril_command.out"
            custom_write_pipe_name = r"\\.\pipe\siril_command.in"
        else:
            # Custom pipes for Siril CLI supported on unix/linux only
            custom_read_pipe_name = "/tmp/siril_command.out"
            custom_write_pipe_name = "/tmp/siril_command.in"

        if self == PipeMode.READ:
            return custom_read_pipe_name
        elif self == PipeMode.WRITE:
            return custom_write_pipe_name


class PipeClient:
    """
    Represents a pipe client for reading or writing to a text based fifo pipe
    """

    def __init__(self, mode: PipeMode, encoding: str = "utf-8"):
        self.path = mode.default_path
        self.mode = mode
        self.encoding = encoding
        self._file = None
        self._loop = asyncio.get_event_loop()

    async def connect(self):
        """Connect to the pipe and wait for open (cross platform)"""
        if self._is_windows:
            await self._connect_windows()
        else:
            await self._connect_unix()

    async def _connect_unix(self):
        while not os.path.exists(self.path):
            await asyncio.sleep(0.1)
        self._file = await asyncio.to_thread(open, self.path, self._open_mode, encoding=self.encoding)

    async def _connect_windows(self):
        while True:
            try:
                # 'b' mode required for named pipes on Windows, no buffering
                self._file = await asyncio.to_thread(open, self.path, self._open_mode, buffering=0)
                break
            except FileNotFoundError:
                await asyncio.sleep(0.1)

    def close(self):
        """Close the pipe and cleanup file"""
        if self._file:
            self._file.close()
            self._file = None

        # Remove the named pipe file if it exists (Unix only)
        if not self._is_windows and os.path.exists(self.path):
            try:
                os.unlink(self.path)
                logger.debug(f"Removed pipe file: {self.path}")
            except OSError as e:
                logger.warning(f"Could not remove pipe file {self.path}: {e}")

    async def write_line(self, message: str):
        """Write a line to the pipe"""
        if self.mode != PipeMode.WRITE:
            raise RuntimeError("Pipe not in write mode")
        if not self._file:
            raise RuntimeError("Pipe not connected")

        encoded = (message + "\n").encode(self.encoding) if self._is_binary else message + "\n"
        await self._loop.run_in_executor(None, self._file.write, encoded)
        await self._loop.run_in_executor(None, self._file.flush)

    async def read_line(self) -> str:
        """Read a line from the pipe"""
        if self.mode != PipeMode.READ:
            raise RuntimeError("Pipe not in read mode")
        if not self._file:
            raise RuntimeError("Pipe not connected")

        line = await self._loop.run_in_executor(None, self._file.readline)
        if isinstance(line, bytes):
            return line.decode(self.encoding)
        return line

    @property
    def _is_windows(self):
        return sys.platform == "win32"

    @property
    def _is_binary(self):
        return self._is_windows

    @property
    def _open_mode(self):
        if self.mode == PipeMode.READ:
            return "rb" if self._is_windows else "r"
        elif self.mode == PipeMode.WRITE:
            return "wb" if self._is_windows else "w"
