# pyTKUtils

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/pgroenbaek/pytkutils?style=flat&label=Latest%20Version)](https://github.com/pgroenbaek/pytkutils/releases)
[![Python 3.7 - 3.13](https://img.shields.io/badge/Python-3.7%20%E2%80%93%203.13-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License GNU GPL v3](https://img.shields.io/badge/License-%20%20GNU%20GPL%20v3%20-lightgrey?style=flat&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NDAgNTEyIj4KICA8IS0tIEZvbnQgQXdlc29tZSBGcmVlIDYuNy4yIGJ5IEBmb250YXdlc29tZSAtIGh0dHBzOi8vZm9udGF3ZXNvbWUuY29tIExpY2Vuc2UgLSBodHRwczovL2ZvbnRhd2Vzb21lLmNvbS9saWNlbnNlL2ZyZWUgQ29weXJpZ2h0IDIwMjUgRm9udGljb25zLCBJbmMuIC0tPgogIDxwYXRoIGZpbGw9IndoaXRlIiBkPSJNMzg0IDMybDEyOCAwYzE3LjcgMCAzMiAxNC4zIDMyIDMycy0xNC4zIDMyLTMyIDMyTDM5OC40IDk2Yy01LjIgMjUuOC0yMi45IDQ3LjEtNDYuNCA1Ny4zTDM1MiA0NDhsMTYwIDBjMTcuNyAwIDMyIDE0LjMgMzIgMzJzLTE0LjMgMzItMzIgMzJsLTE5MiAwLTE5MiAwYy0xNy43IDAtMzItMTQuMy0zMi0zMnMxNC4zLTMyIDMyLTMybDE2MCAwIDAtMjk0LjdjLTIzLjUtMTAuMy00MS4yLTMxLjYtNDYuNC01Ny4zTDEyOCA5NmMtMTcuNyAwLTMyLTE0LjMtMzItMzJzMTQuMy0zMiAzMi0zMmwxMjggMGMxNC42LTE5LjQgMzcuOC0zMiA2NC0zMnM0OS40IDEyLjYgNjQgMzJ6bTU1LjYgMjg4bDE0NC45IDBMNTEyIDE5NS44IDQzOS42IDMyMHpNNTEyIDQxNmMtNjIuOSAwLTExNS4yLTM0LTEyNi03OC45Yy0yLjYtMTEgMS0yMi4zIDYuNy0zMi4xbDk1LjItMTYzLjJjNS04LjYgMTQuMi0xMy44IDI0LjEtMTMuOHMxOS4xIDUuMyAyNC4xIDEzLjhsOTUuMiAxNjMuMmM1LjcgOS44IDkuMyAyMS4xIDYuNyAzMi4xQzYyNy4yIDM4MiA1NzQuOSA0MTYgNTEyIDQxNnpNMTI2LjggMTk1LjhMNTQuNCAzMjBsMTQ0LjkgMEwxMjYuOCAxOTUuOHpNLjkgMzM3LjFjLTIuNi0xMSAxLTIyLjMgNi43LTMyLjFsOTUuMi0xNjMuMmM1LTguNiAxNC4yLTEzLjggMjQuMS0xMy44czE5LjEgNS4zIDI0LjEgMTMuOGw5NS4yIDE2My4yYzUuNyA5LjggOS4zIDIxLjEgNi43IDMyLjFDMjQyIDM4MiAxODkuNyA0MTYgMTI2LjggNDE2UzExLjcgMzgyIC45IDMzNy4xeiIvPgo8L3N2Zz4=&logoColor=%23ffffff)](https://github.com/pgroenbaek/pytkutils/blob/master/LICENSE)

This Python module wraps the `TK.MSTS.Tokens.dll` library by Okrasa Ghia. The module allows you to compress and decompress MSTS files such as shape and world files.

> [!IMPORTANT]
> This module requires `TK.MSTS.Tokens.dll` from the [TK\_Utils package](https://the-train.de/downloads/entry/9385-tk-utils-updated/).
> It is **not included** with this Python module. You must download the DLL yourself.

> [!NOTE]
> Only compression appears to work properly.
> The DLL fails internally for decompression regardless of operating system.

See also:
- [pyffeditc](https://github.com/pgroenbaek/pyffeditc) - handles compression and decompression of MSTS files such as shape and world files through the `ffeditc_unicode.exe` utility.

## Prerequisites

A Common Language Runtime (CLR) is required if you wish to compress and decompress files through this module. You can use the Mono runtime on Linux and macOS, or the .NET Framework on Windows.

The `TK.MSTS.Tokens.dll` library is not bundled with this Python module. It is available as part of the **TK\_Utils** package from [the-train.de](https://the-train.de/downloads/entry/9385-tk-utils-updated/).


See the [Usage section](#usage) for more details on how to compress and decompress shape and world files using the module.

Steps to install a CLR on your operating system:

#### Linux

```bash
sudo apt update
sudo apt install mono-complete
```

#### macOS

```bash
brew install mono
```

#### Windows

Download and install the [.NET Framework 4.0 or later](https://dotnet.microsoft.com/en-us/download/dotnet-framework) from Microsoft.

The .NET Framework is typically already installed on most Windows systems.


## Installation

### Install from PyPI

```sh
pip install --upgrade pytkutils
```

### Install from wheel

If you have downloaded a `.whl` file from the [Releases](https://github.com/pgroenbaek/pytkutils/releases) page, install it with:

```sh
pip install path/to/pytkutils-<version>‑py3‑none‑any.whl
```

Replace `<version>` with the actual version number in the filename.

### Install from source

```sh
git clone https://github.com/pgroenbaek/pytkutils.git
pip install --upgrade ./pytkutils
```

## Usage

### Check if a file on disk is compressed

To check whether a file on disk is compressed, you can use the `is_compressed` function. This function returns `True` if the file is compressed and `False` if it is not. If the file is empty or its state cannot be determined, the function will return `None`.

```python
import pytkutils

compressed = pytkutils.is_compressed("./path/to/example.s")

if compressed is True:
    print("Compressed")
elif compressed is False:
    print("Uncompressed")
else:
    print("Could not determine (possibly empty file)")
```

### Compress or decompress files

The compression and decompression functions in this module use the `TK.MSTS.Tokens.dll` library by Okrasa Ghia. This library is not included with the Python module. You will also need a CLR installed to load this file.

See the [Prerequisites section](#prerequisites) for instructions on how to obtain the `TK.MSTS.Tokens.dll` library and set up a CLR on your machine.

Alternatively, you can use the [pyffeditc](https://github.com/pgroenbaek/pyffeditc) module on Windows.

You can also compress/decompress manually using `ffeditc_unicode.exe` through the [Shape File Manager](https://www.trainsim.com/forums/filelib-search-fileid?fid=78928) or use the [FFEDIT\_Sub v1.2](https://www.trainsim.com/forums/filelib-search-fileid?fid=40291) utility by Ged Saunders.

```python
import pytkutils

dll_path = "./path/to/TK.MSTS.Tokens.dll"

# Compress and decompress in-place.
pytkutils.compress(dll_path, "./path/to/example.s")
pytkutils.decompress(dll_path, "./path/to/example.s")

# Compress and decompress to an output file.
pytkutils.compress(dll_path, "./path/to/example.s", "./path/to/output.s")
pytkutils.decompress(dll_path, "./path/to/example.s", "./path/to/output.s")
```


## Running Tests

You can run tests manually or use `tox` to test across multiple Python versions.

### Run Tests Manually
First, install the required dependencies:

```sh
pip install pytest pytest-dependency
```

Then, run tests with:

```sh
pytest
```


### Run Tests with `tox`

First, install the required dependencies:

```sh
pip install tox pytest pytest-dependency
```

Then, run tests with:

```sh
tox
```

This will execute tests for all Python versions specified in `tox.ini`.

## Known Issues

Only compression appears to work through `TK.MSTS.Tokens.dll`. The DLL fails internally for decompression.

As an alternative, on Windows, you can use the [pyffeditc](https://github.com/pgroenbaek/pyffeditc) module that uses `ffeditc_unicode.exe` and works for both compression and decompression.

## Contributing

Contributions of all kinds are welcome. These could be suggestions, issues, bug fixes, documentation improvements, or new features.

For more details see the [contribution guidelines](/CONTRIBUTING.md).

## License

This Python module was created by Peter Grønbæk Andersen and is licensed under [GNU GPL v3](https://github.com/pgroenbaek/pytkutils/blob/master/LICENSE).

> [!NOTE]
> The `TK.MSTS.Tokens.dll` library itself comes with a different license by Okrasa Ghia.
> That license can be found in the TK\_Utils package from [the-train.de](https://the-train.de/downloads/entry/9385-tk-utils-updated/).
