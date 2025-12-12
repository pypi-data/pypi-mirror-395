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
from async_siril.command import fits_extension

log = structlog.stdlib.get_logger()


@dataclass
class CreateMasterDark:
    raw_folder: t.Annotated[pathlib.Path, cappa.Arg(help="Path to the raw folder of Dark frames")]
    ext: t.Annotated[
        fits_extension, cappa.Arg(short=True, default=fits_extension.FITS_EXT_FIT, help="Extension of the Dark frames")
    ]
    name: t.Annotated[str, cappa.Arg(short=True, default="DARK_2025-06-30", help="Name of the master dark")]

    dslr: t.Annotated[bool, cappa.Arg(short=True, default=False, help="Use DSLR mode (dark optimization)")]
    bias: t.Annotated[t.Optional[pathlib.Path], cappa.Arg(short=True, help="Path to the master bias")] = None

    async def __call__(self) -> None:
        log.info("Starting create master dark")
        log.info(f"input: {self.raw_folder}")
        log.info(f"extension: {self.ext}")
        log.info(f"name: {self.name}")
        log.info(f"dslr: {self.dslr}")
        log.info(f"bias: {self.bias}")

        if self.dslr and self.bias is None:
            log.error("Bias must be specified when using DSLR mode")
            raise cappa.Exit()

        with tempfile.TemporaryDirectory(dir=self.raw_folder) as tempdir:  # type: ignore
            temp = pathlib.Path(tempdir)
            log.info(f"temp dir: {temp}")

            async with SirilCli(directory=self.raw_folder) as siril:
                # Caution: these settings are saved between Siril sessions
                await siril.command(setext(self.ext))
                await siril.command(set32bits())

                await siril.command(convert(self.name, output_dir=f"./{temp.name}"))
                await siril.command(cd(f"{temp.name}"))

                out = f"../../{self.name}_stacked"
                if self.dslr and self.bias is not None:
                    # This is really geared towards the DSLR users
                    # produces: calibrated-master-dark
                    # Dark Optimization: used to identify the thermal noise in non-temp controlled cameras (dslr)
                    await siril.command(calibrate(self.name, bias=f"{str(self.bias.relative_to(temp))}"))
                    await siril.command(stack(f"pp_{self.name}", out=out))
                else:
                    await siril.command(stack(self.name, out=out))

        log.info("Master dark created")


def main() -> None:  # pragma: no cover
    try:
        asyncio.run(cappa.invoke_async(CreateMasterDark))
    except Exception as e:
        log.exception("Unhandled exception")
        raise cappa.Exit("There was an error while executing", code=-1) from e


if __name__ == "__main__":
    main()
