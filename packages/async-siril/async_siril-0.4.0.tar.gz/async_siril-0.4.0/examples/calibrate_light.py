from __future__ import annotations

import structlog.stdlib
import asyncio
import cappa
import pathlib
import tempfile
import typing as t
from dataclasses import dataclass

from async_siril import SirilCli, ConversionFile
from async_siril.command import setext, set32bits, cd, convert, calibrate
from async_siril.command import fits_extension


log = structlog.stdlib.get_logger()


@dataclass
class CalibrateLight:
    raw_folder: t.Annotated[pathlib.Path, cappa.Arg(help="Path to the raw folder of Light frames")]
    output: t.Annotated[pathlib.Path, cappa.Arg(help="Path to the output folder")]
    ext: t.Annotated[
        fits_extension, cappa.Arg(short=True, default=fits_extension.FITS_EXT_FIT, help="Extension of the Light frames")
    ]

    dark: t.Annotated[t.Optional[pathlib.Path], cappa.Arg(short=True, help="Path to the master dark")]
    flat: t.Annotated[t.Optional[pathlib.Path], cappa.Arg(short=True, help="Path to the master flat")]
    bias: t.Annotated[t.Optional[pathlib.Path], cappa.Arg(short=True, help="Path to the master bias")]

    async def __call__(self) -> None:
        log.info("Starting calibrate light")
        log.info(f"input: {self.raw_folder}")
        log.info(f"extension: {self.ext}")
        log.info(f"dark: {self.dark}")
        log.info(f"flat: {self.flat}")
        log.info(f"bias: {self.bias}")

        if self.dark is None and self.flat is None and self.bias is None:
            log.error("Dark, flat, or bias not specified")
            raise cappa.Exit()

        # Check if all raw frames are OSC
        all_color = await self._all_color_raw_frames()
        log.info(f"Raw images are OSC: {all_color}")

        # Check if output folder exists else make it
        if not self.output.exists():
            self.output.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory(dir=self.raw_folder) as tempdir:  # type: ignore
            temp = pathlib.Path(tempdir)
            log.info(f"temp dir: {temp}")

            async with SirilCli(directory=self.raw_folder) as siril:
                # Caution: these settings are saved between Siril sessions
                await siril.command(setext(self.ext))
                await siril.command(set32bits())

                await siril.command(convert("light_", output_dir=f"./{temp.name}"))
                await siril.command(cd(f"{temp.name}"))

                await siril.command(
                    calibrate(
                        "light_",
                        bias=f"{str(self.bias)}" if self.bias is not None else None,
                        dark=f"{str(self.dark)}" if self.dark is not None else None,
                        flat=f"{str(self.flat)}" if self.flat is not None else None,
                        cfa=all_color,
                        debayer=all_color,
                        equalize_cfa=all_color,
                    )
                )

                conversion = ConversionFile(temp / "light_conversion.txt")
                log.info(f"conversion: {conversion.entries}")
                await self._move_converted_files(conversion, prefix="pp_")

        log.info("Light calibrated and saved to: {self.output}")

    async def _all_color_raw_frames(self) -> bool:
        from astropy.io import fits  # type: ignore
        from astropy.io.fits import PrimaryHDU  # type: ignore

        def is_color(file: pathlib.Path) -> bool:
            with fits.open(file, ignore_missing_simple=True) as hdu_list:
                primary_hdu = next(h for h in hdu_list if isinstance(h, PrimaryHDU))
                return "BAYERPAT" in primary_hdu.header and primary_hdu.header["BAYERPAT"] != ""

        raw_files = list(self.raw_folder.glob(f"*.{self.ext.value}"))
        result = all(is_color(raw_file) for raw_file in raw_files)
        return result

    async def _move_converted_files(self, conversion: ConversionFile, prefix: str) -> None:
        log.info(f"Moving converted files to {self.output}")
        for entry in conversion.entries:
            converted_file = conversion.file.parent.joinpath(f"{prefix}{entry.converted_file.name}")
            converted_file.rename(self.output / f"{prefix}{entry.original_file.name}")


def main() -> None:  # pragma: no cover
    try:
        asyncio.run(cappa.invoke_async(CalibrateLight))
    except Exception as e:
        log.exception("Unhandled exception")
        raise cappa.Exit("There was an error while executing", code=-1) from e


if __name__ == "__main__":
    main()
