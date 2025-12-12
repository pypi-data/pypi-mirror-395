from __future__ import annotations

from enum import Enum
from dataclasses import dataclass


class SirilSetting(Enum):
    """Represents some of the common Siril settings, use `get -a` to discover more."""

    EXTENSION = "core.extension"
    FORCE_16BIT = "core.force_16bit"
    MEM_MODE = "core.mem_mode"
    MEM_AMOUNT = "core.mem_amount"
    MEM_RATIO = "core.mem_ratio"


@dataclass
class Rect:
    x: int
    y: int
    width: int
    height: int

    def __str__(self):
        return f"{self.x} {self.y} {self.width} {self.height}"


@dataclass
class SigmaRange:
    low: float
    high: float

    def __str__(self):
        return f"{self.low} {self.high}"


class clipmode(Enum):
    CLIPMODE_CLIP = "clip"
    CLIPMODE_RESCALE = "rescale"
    CLIPMODE_RGB_BLEND = "rgbblend"
    CLIPMODE_GLOBAL_RESCALE = "globalrescale"


class fits_extension(Enum):
    FITS_EXT_FIT = "fit"
    FITS_EXT_FITS = "fits"
    FITS_EXT_FTS = "fts"


class registration_transformation(Enum):
    REG_TRANSF_SHIFT = "shift"
    REG_TRANSF_SIMILARITY = "similarity"
    REG_TRANSF_AFFINE = "affine"
    REG_TRANSF_HOMOGRAPHY = "homography"


class pixel_interpolation(Enum):
    INTERP_NONE = "none"
    INTERP_NEAREST = "nearest"
    INTERP_CUBIC = "cubic"
    INTERP_LANCZOS4 = "lanczos4"
    INTERP_LINEAR = "linear"
    INTERP_AREA = "area"


class sequence_framing(Enum):
    FRAME_CURRENT = "current"
    FRAME_MIN = "min"
    FRAME_MAX = "max"
    FRAME_COG = "cog"


class sequence_filter_type(Enum):
    FILTER_NONE = ""
    FILTER_FWHM = "filter-fwhm"
    FILTER_WFWHM = "filter-wfwhm"
    FILTER_ROUNDNESS = "filter-round"
    FILTER_QUALITY = "filter-quality"
    FILTER_INCLUSION = "filter-incl"
    FILTER_BACKGROUND = "filter-bkg"
    FILTER_STAR_COUNT = "filter-nbstars"


class compression_type(Enum):
    COMPRESSION_RICE = "rice"
    COMPRESSION_GZIP1 = "gzip1"
    COMPRESSION_GZIP2 = "gzip2"


class stack_type(Enum):
    STACK_SUM = "sum"
    STACK_REJ = "rej"
    STACK_MED = "med"
    STACK_MIN = "min"
    STACK_MAX = "max"


class stack_norm(Enum):
    NO_NORM = "-nonorm"
    NORM_ADD = "-norm=add"
    NORM_ADD_SCALE = "-norm=addscale"
    NORM_MUL = "-norm=mul"
    NORM_MUL_SCALE = "-norm=mulscale"


class stack_rejection(Enum):
    REJECTION_NONE = "n"
    REJECTION_PERCENTILE = "p"
    REJECTION_SIGMA = "s"
    REJECTION_MEDIAN = "m"
    REJECTION_WINSORIZED = "w"
    REJECTION_LINEAR_FIT = "l"
    REJECTION_GESDT = "g"
    REJECTION_MAD = "a"


class stack_weighting(Enum):
    NO_WEIGHT = ""
    WEIGHT_FROM_NOISE = "-weight_from_noise"
    WEIGHT_FROM_WFWHM = "-weight_from_wfwhm"
    WEIGHT_FROM_NBSTARS = "-weight_from_nbstars"
    WEIGHT_FROM_NBSTACK = "-weight_from_nbstack"


class stack_rejmaps(Enum):
    NO_REJECTION_MAPS = ""
    TWO_REJECTION_MAPS = "-rejmaps"
    MERGED_REJECTION_MAPS = "-rejmap"


class magnitude_option(Enum):
    DEFAULT_MAGNITUDE = 1
    MAGNITUDE_OFFSET = 2
    ABSOLUTE_MAGNITUDE = 3


class star_catalog(Enum):
    TYCHO2 = "tycho2"
    NOMAD = "nomad"
    GAIA = "gaia"
    PPMXL = "ppmxl"
    BRIGHTSTARS = "brightstars"
    APASS = "apass"


class rmgreen_protection(Enum):
    AVERAGE_NEUTRAL = 0
    MAXIMUM_NEUTRAL = 1
    MAXIMUM_MASK = 2
    ADDITIVE_MASK = 3


class saturation_hue_range(Enum):
    PINK_ORANGE = 0
    ORANGE_YELLOW = 1
    YELLOW_CYAN = 2
    CYAN = 3
    CYAN_MAGENTA = 4
    MAGENTA_PINK = 5
    ALL = 6


class catalog_option(Enum):
    APASS = "apass"
    LOCAL_GAIA = "localgaia"
    GAIA = "gaia"


class online_catalog(Enum):
    TYCHO2 = "tycho2"
    NOMAD = "nomad"
    GAIA = "gaia"
    LOCAL_GAIA = "localgaia"
    PPMXL = "ppmxl"
    BSC = "bsc"
    APASS = "apass"
    GCVS = "gcvsc"
    VSX = "vsx"
    SIMBAD = "simbad"
    AAVSO_VSP = "aavso_chart"
    EXOPLANET_ARCHIVE = "exo"
    PGC = "pgc"
    SOLSYS = "solsys"


class extract_resample(Enum):
    HA = "ha"
    OIII = "oiii"


class ght_weighting(Enum):
    HUMAN = "human"
    EVEN = "even"
    INDEPENDENT = "independent"
    SATURATION = "sat"


class Channel(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2


class channel_label(Enum):
    RED = "R"
    GREEN = "G"
    BLUE = "B"
    RED_GREEN = "RG"
    RED_BLUE = "RB"
    GREEN_BLUE = "GB"
    ALL = "RGB"


class limit_option(Enum):
    CLIP = "clip"
    POS_RESCALE = "posrescale"
    RESCALE = "rescale"


class wavelet_type(Enum):
    LINEAR = 1
    BSPLINE = 2


class star_range(Enum):
    NARROW = "narrow"
    WIDE = "wide"


class find_star_catalog(Enum):
    NOMAD = "nomad"
    APASS = "apass"


class drizzle_kernel(Enum):
    POINT = "point"
    TURBO = "turbo"
    SQUARE = "square"
    GAUSSIAN = "gaussian"
    LANCZOS2 = "lanczos2"
    LANCZOS3 = "lanczos3"


class split_option(Enum):
    HSL = "hsl"
    HSV = "hsv"
    CIELAB = "lab"


class spcc_list_type(Enum):
    OSCSENSOR = "oscsensor"
    MONOSENSOR = "monosensor"
    REDFILTER = "redfilter"
    GREENFILTER = "greenfilter"
    BLUEFILTER = "bluefilter"
    OSCFILTER = "oscfilter"
    OSCLPF = "osclpf"
    WHITEREF = "whiteref"


class stat_detail(Enum):
    BASIC = "basic"
    MAIN = "main"
    FULL = "full"


class psf_method(Enum):
    CLEAR = "clear"
    LOAD = "load"
    SAVE = "save"
    BLIND = "blind"
    STARS = "stars"
    MANUAL = "manual"


class manual_psf_method(Enum):
    GAUSSIAN = "gaussian"
    MOFFAT = "moffat"
    DISC = "disc"
    AIRY = "airy"
