# GridWorks Protocol

[![PyPI](https://img.shields.io/pypi/v/gridworks-protocol.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/gridworks-protocol.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/gridworks-protocol)][python version]
[![License](https://img.shields.io/pypi/l/gridworks-protocol)][license]

[![Read the documentation at https://gridworks-protocol.readthedocs.io/](https://img.shields.io/readthedocs/gridworks-protocol/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/thegridelectric/gridworks-protocol/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/thegridelectric/gridworks-protocol/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/gridworks-protocol/
[status]: https://pypi.org/project/gridworks-protocol/
[python version]: https://pypi.org/project/gridworks-protocol
[read the docs]: https://gridworks-protocol.readthedocs.io/
[tests]: https://github.com/thegridelectric/gridworks-protocol/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/thegridelectric/gridworks-protocol
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

GridWorks Protocol (gwproto) is a [Application Shared Language](https://gridwork-type-registry.readthedocs.io/en/latest/asls.html)
used by [SCADA](https://gridworks.readthedocs.io/en/latest/scada.html)/[AtomicTNode](https://gridworks.readthedocs.io/en/latest/atomic-t-node.html) actor pairs to communicate
with each other as they work together to manage the Service Level Agreement for
[transactive devices](https://gridworks.readthedocs.io/en/latest/transactive-device.html) dedicated to residential thermal storage heating.

## Installation

You can install _Gridworks Protocol_ via [pip] from [PyPI]:

```console
$ pip install gridworks-protocol
```

## Usage

When gridworks-protocol has been included as a package:

```
from gwproto.types import SpaceheatNodeGt
```

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Gridworks Protocol_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/thegridelectric/gridworks-protocol/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/thegridelectric/gridworks-protocol/blob/main/LICENSE
[contributor guide]: https://github.com/thegridelectric/gridworks-protocol/blob/main/CONTRIBUTING.md
