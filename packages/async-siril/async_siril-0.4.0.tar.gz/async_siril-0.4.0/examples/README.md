# Examples

Development dependencies:
- pydash
- astropy
- cappa

Usage:

## Create master bias

Basic bias creation by stacking all Bias frames in the raw folder.

```bash
uv run create_master_bias.py -e fit -n BIAS_2025-06-30 /path/to/raw/folder
# master ends up in /path/to/raw/BIAS_2025-06-30_stacked.fit
```

# Create master dark

Basic dark creation by stacking all Dark frames in the raw folder.

```bash
uv run create_master_dark.py -e fit -n DARK_2025-06-30 /path/to/raw/folder
# master ends up in /path/to/raw/DARK_2025-06-30_stacked.fit
```

## Create master flat

Basic flat creation by calibration all frames with the bias fram and stacking all the calibrated flats.

```bash
uv run create_master_flat.py -e fit -n FLAT_2025-06-30 -b /path/to/master/bias /path/to/raw/folder
# master ends up in /path/to/raw/FLAT_2025-06-30_stacked.fit
```

## Calibrate light

Calibrate all light frames with the bias, dark, and flat frames, outputing the calibrated light frames to the specified output folder.

```bash
uv run calibrate_light.py -e fit -n LIGHT_2025-06-30 -d /path/to/master/dark -f /path/to/master/flat /path/to/raw/folder /path/to/output/folder
# calibrated light frames end up in /path/to/output/folder
```

## Create master light

Basic light creation by stacking all calibrated light frames in the calibrated folder. Optional, background extraction can be enabled.

```bash
uv run create_master_light.py -e fit -n LIGHT_2025-06-30 /path/to/pp/folder /path/to/output/folder
# master ends up in /path/to/output/LIGHT_2025-06-30_linear_stack.fit
```
