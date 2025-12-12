from __future__ import annotations

import structlog.stdlib
import asyncio
import cappa
from dataclasses import dataclass

from async_siril import SirilCli
from async_siril.command import get
from async_siril.command_types import SirilSetting
from rich.prompt import Confirm

log = structlog.stdlib.get_logger()


@dataclass
class TestSiril:
    async def __call__(self) -> None:
        log.info("Testing Siril Interface")

        async with SirilCli() as siril:
            await siril.set(SirilSetting.FORCE_16BIT, False)
            await siril.command(get(list_all=True))
            Confirm.ask("Continue")

        log.info("Siril Interface completed")


def main() -> None:  # pragma: no cover
    try:
        asyncio.run(cappa.invoke_async(TestSiril))
    except Exception as e:
        log.exception("Unhandled exception")
        raise cappa.Exit("There was an error while executing", code=-1) from e


if __name__ == "__main__":
    main()
