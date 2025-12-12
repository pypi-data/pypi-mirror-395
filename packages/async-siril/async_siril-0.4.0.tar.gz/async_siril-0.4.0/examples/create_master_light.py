from __future__ import annotations

import structlog.stdlib
import asyncio
import cappa
import pathlib
import tempfile
import typing as t
from dataclasses import dataclass

from async_siril import SirilCli, BestRejection
from async_siril.command import (
    setext,
    set32bits,
    cd,
    convert,
    stack,
    register,
    seqsubsky,
    seqapplyreg,
    mirrorx,
    load,
    save,
)
from async_siril.command import fits_extension, stack_norm

log = structlog.stdlib.get_logger()


@dataclass
class CreateMasterLight:
    pp_folder: t.Annotated[pathlib.Path, cappa.Arg(help="Path to the raw folder of calibrated Light frames")]
    output: t.Annotated[pathlib.Path, cappa.Arg(help="Path to the output folder")]
    ext: t.Annotated[
        fits_extension, cappa.Arg(short=True, default=fits_extension.FITS_EXT_FIT, help="Extension of the Light frames")
    ]

    background_extraction: t.Annotated[bool, cappa.Arg(short=True, default=False, help="Enable background extraction")]
    name: t.Annotated[str, cappa.Arg(short=True, default="LIGHT_2025-06-30", help="Name of the master light")]

    async def __call__(self) -> None:
        log.info("Starting create master light")
        log.info(f"input: {self.pp_folder}")
        log.info(f"output: {self.output}")
        log.info(f"extension: {self.ext}")
        log.info(f"name: {self.name}")

        # Check if output folder exists else make it
        if not self.output.exists():
            self.output.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory(dir=self.pp_folder) as tempdir:  # type: ignore
            temp = pathlib.Path(tempdir)
            log.info(f"temp dir: {temp}")

            # Find the best rejection method
            rejection = BestRejection.find(list(self.pp_folder.glob(f"*.{self.ext.value}")))

            async with SirilCli(directory=self.pp_folder) as siril:
                # Caution: these settings are saved between Siril sessions
                await siril.command(setext(self.ext))
                await siril.command(set32bits())

                # Manage the next prefix
                prefix = "light_"

                await siril.command(convert(prefix, output_dir=f"./{temp.name}"))
                await siril.command(cd(f"{temp.name}"))

                if self.background_extraction:
                    # Background extraction
                    await siril.command(seqsubsky(prefix))
                    prefix = f"bkg_{prefix}"

                # Register all the images
                await siril.command(register(prefix, two_pass=True))

                # and generate their transformed version
                await siril.command(seqapplyreg(prefix))
                prefix = f"r_{prefix}"

                # Stack the background extracted images
                await siril.command(
                    stack(
                        prefix,
                        norm=stack_norm.NORM_ADD_SCALE,
                        filter_included=True,
                        output_norm=True,
                        rgb_equalization=True,
                        rejection=rejection.method,
                        lower_rej=rejection.low_threshold,
                        higher_rej=rejection.high_threshold,
                        out="siril_result",
                    )
                )

                await siril.command(load("siril_result"))
                await siril.command(mirrorx())
                await siril.command(save(f"{self.output}/{self.name}_linear_stack"))

        log.info(f"Master light created and saved to: {self.output}")


def main() -> None:  # pragma: no cover
    try:
        asyncio.run(cappa.invoke_async(CreateMasterLight))
    except Exception as e:
        log.exception("Unhandled exception")
        raise cappa.Exit("There was an error while executing", code=-1) from e


if __name__ == "__main__":
    main()
