import re
import pathlib
import typing as t

from dataclasses import dataclass


@dataclass
class ConversionEntry:
    """
    Represents a single entry in a conversion file
    """

    original_file: pathlib.Path
    converted_file: pathlib.Path


@dataclass
class ConversionFile:
    """
    Represents a conversion file from siril as a result of the `convert` command or other sequence operations
    """

    entries: t.List[ConversionEntry]
    file: pathlib.Path

    def __init__(self, file: pathlib.Path):
        self.file = file
        self.entries = []
        self.read()

    def read(self):
        """
        Reads the conversion file and populates the entries list
        """
        if not self.file.exists():
            return None

        regex = r"'(.*?)'.*?'(.*?)'"
        with open(self.file) as txt_file:
            raw = txt_file.read()
            matches = re.finditer(regex, raw, re.MULTILINE)
            for _match_num, match in enumerate(matches, start=1):
                orig_file = pathlib.Path(match.group(1))
                conv_file = pathlib.Path(match.group(2))

                self.entries.append(ConversionEntry(orig_file, conv_file))
