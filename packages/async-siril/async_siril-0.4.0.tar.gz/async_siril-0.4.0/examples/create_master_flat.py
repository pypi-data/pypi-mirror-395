from __future__ import annotations

import structlog.stdlib
import asyncio
import cappa
import pathlib
import tempfile
import typing as t
from dataclasses import dataclass

from async_siril import SirilCli
from async_siril.command import setext, set32bits, cd, convert, stack, calibrate
from async_siril.command import fits_extension, stack_norm

log = structlog.stdlib.get_logger()


@dataclass
class CreateMasterFlat:
    raw_folder: t.Annotated[pathlib.Path, cappa.Arg(help="Path to the raw folder of Flat frames")]
    ext: t.Annotated[
        fits_extension, cappa.Arg(short=True, default=fits_extension.FITS_EXT_FIT, help="Extension of the Flat frames")
    ]
    name: t.Annotated[str, cappa.Arg(short=True, default="FLAT_2025-06-30", help="Name of the master flat")]

    bias: t.Annotated[pathlib.Path, cappa.Arg(short=True, help="Path to the master bias")]

    async def __call__(self) -> None:
        log.info("Starting create master flat")
        log.info(f"input: {self.raw_folder}")
        log.info(f"extension: {self.ext}")
        log.info(f"name: {self.name}")
        log.info(f"bias: {self.bias}")

        with tempfile.TemporaryDirectory(dir=self.raw_folder) as tempdir:  # type: ignore
            temp = pathlib.Path(tempdir)
            log.info(f"temp dir: {temp}")

            async with SirilCli(directory=self.raw_folder) as siril:
                # Caution: these settings are saved between Siril sessions
                await siril.command(setext(self.ext))
                await siril.command(set32bits())

                await siril.command(convert(self.name, output_dir=f"./{temp.name}"))
                await siril.command(cd(f"{temp.name}"))

                # Calibrate the flat frames using the master bias
                await siril.command(calibrate(self.name, bias=f"{str(self.bias)}"))

                # Stack the calibrated flat frames into a master flat
                await siril.command(
                    stack(f"pp_{self.name}", norm=stack_norm.NORM_MUL, out=f"../../{self.name}_stacked")
                )

        log.info("Master flat created")


def main() -> None:  # pragma: no cover
    try:
        asyncio.run(cappa.invoke_async(CreateMasterFlat))
    except Exception as e:
        log.exception("Unhandled exception")
        raise cappa.Exit("There was an error while executing", code=-1) from e


if __name__ == "__main__":
    main()
