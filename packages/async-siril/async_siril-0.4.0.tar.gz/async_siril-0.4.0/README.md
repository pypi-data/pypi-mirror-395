[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![image](https://img.shields.io/pypi/v/async-siril.svg)](https://pypi.python.org/pypi/async-siril)
[![image](https://img.shields.io/pypi/l/async-siril.svg)](https://pypi.python.org/pypi/async-siril)
[![image](https://img.shields.io/pypi/pyversions/async-siril.svg)](https://pypi.python.org/pypi/async-siril)
[![Actions status](https://github.com/KyleLeNeau/async-siril/actions/workflows/ci.yml/badge.svg)](https://github.com/KyleLeNeau/async-siril/actions)
![Static Badge](https://img.shields.io/badge/coverage-93%25-brightgreen)

# async-siril

Async Siril is an asyncio based python wrapper around [Siril 1.4.0](https://www.siril.org/) used for processing astronomy data for astrophotography and science. The library provides a pythonic interface to the Siril command line interface and all of it's commands. Scripts, processes, and workflows can be built with modern async python.

## Features

* async/await based using [asyncio](https://docs.python.org/3/library/asyncio.html)
* code generated Siril commands from [free-astro/siril-doc](https://gitlab.com/free-astro/siril-doc/)
* logging with [structlog](https://www.structlog.org/)
* example CLI commands built for calibration, registration & stacking workflows [examples](./examples)
* some helpers for common logic (see `async_siril.helpers`)
* minimal dependencies (`asyncio`, `structlog`, `psutil`)
* Linux, Mac, & Windows support
* Docker support (see [Dockerfile.siril](./Dockerfile.siril))
* 93% test coverage 

## Requirements

* Siril installed on your system (https://www.siril.org/)
* Python 3.12 or higher
* [uv](https://docs.astral.sh/uv/) or [pip](https://pip.pypa.io/en/stable/)

## Installation

```bash
uv add async-siril
# OR
pip install async-siril
```

## Usage

Here is a simple example of how to create a master bias using the library:

```python
import asyncio
import pathlib

from async_siril import SirilCli
from async_siril.command import setext, set32bits, convert, stack
from async_siril.command_types import fits_extension

async def main():
    current_dir = pathlib.Path(__file__).parent
    async with SirilCli(directory=current_dir) as siril:
        await siril.command(setext(fits_extension.FITS_EXT_FIT))
        await siril.command(set32bits())

        await siril.command(convert("bias"))
        await siril.command(stack("bias", out="bias_master"))

if __name__ == "__main__":
    asyncio.run(main())
```

For advanced use cases you can run the Siril commands directly as strings.

```python
from async_siril import SirilCli

async def main():
    async with SirilCli() as siril:
        await siril.command("setext fits")
        await siril.command("set32bits")
        await siril.command("convert bias")
        await siril.command("stack bias bias_master")

if __name__ == "__main__":
    asyncio.run(main())
```

By default, any command that fails will throw an exception and shut things down. If you want to catch these types of errors and try again or handle a different way you can use the `failable_command` method.

```python
from async_siril import SirilCli

async def main():
    async with SirilCli() as siril:
        await siril.command("setext fits")
        await siril.command("set32bits")
        await siril.command("convert bias")
        result = await siril.failable_command("stack bias bias_master")
        if not result:
            print("Stack failed, make a change and try again")

if __name__ == "__main__":
    asyncio.run(main())
```

## Docker (example only)

You can use the example [Dockerfile.siril](./Dockerfile.siril) to build a docker image with Siril installed. This is useful for running the examples or for running Siril commands in a container.

```bash
docker build -f Dockerfile.siril -t async-siril:latest .
```

Once built you can test the interface with this (runs `uv run ./examples/test_siril.py`):

```bash
docker run --rm -it --name siril-test async-siril:latest
```

## Roadmap

Please see [ROADMAP.md](./ROADMAP.md) for more details.

## Contributing

PRs are welcome & appreciated! See the [contributing guide](./CONTRIBUTING.md) to get started.

## FAQ

#### Why not use [pysiril](https://gitlab.com/free-astro/pysiril)?

[pysiril](https://gitlab.com/free-astro/pysiril) is a great library for interacting with Siril. However, it is not asyncio based and does not provide a pythonic interface to the Siril command line interface.

#### Siril just added python scripting, how is this different?

The new python scripting added to Siril is a great improvement for in-app scripts. However, sometimes you just need a simple interface for headless operations of Siril.

## Acknowledgements

Siril is a fantastic piece of software and I am grateful to the [free-astro](https://gitlab.com/free-astro) team for their hard work. Special thanks to [Vincent](https://gitlab.com/Vincent-FA) for answering questions and providing support.

## License

async-siril is licensed under:

- BSD-3-Clause license ([LICENSE](LICENSE) or <https://opensource.org/licenses/BSD-3-Clause>)

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in async-siril by you, as defined in the BSD-3-Clause license, shall be dually licensed as above, without any additional terms or conditions.