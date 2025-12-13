# pyFFEDITC

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/pgroenbaek/pyffeditc?style=flat&label=Latest%20Version)](https://github.com/pgroenbaek/pyffeditc/releases)
[![Python 3.6+](https://img.shields.io/badge/Python-3.6%2B-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License GNU GPL v3](https://img.shields.io/badge/License-%20%20GNU%20GPL%20v3%20-lightgrey?style=flat&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NDAgNTEyIj4KICA8IS0tIEZvbnQgQXdlc29tZSBGcmVlIDYuNy4yIGJ5IEBmb250YXdlc29tZSAtIGh0dHBzOi8vZm9udGF3ZXNvbWUuY29tIExpY2Vuc2UgLSBodHRwczovL2ZvbnRhd2Vzb21lLmNvbS9saWNlbnNlL2ZyZWUgQ29weXJpZ2h0IDIwMjUgRm9udGljb25zLCBJbmMuIC0tPgogIDxwYXRoIGZpbGw9IndoaXRlIiBkPSJNMzg0IDMybDEyOCAwYzE3LjcgMCAzMiAxNC4zIDMyIDMycy0xNC4zIDMyLTMyIDMyTDM5OC40IDk2Yy01LjIgMjUuOC0yMi45IDQ3LjEtNDYuNCA1Ny4zTDM1MiA0NDhsMTYwIDBjMTcuNyAwIDMyIDE0LjMgMzIgMzJzLTE0LjMgMzItMzIgMzJsLTE5MiAwLTE5MiAwYy0xNy43IDAtMzItMTQuMy0zMi0zMnMxNC4zLTMyIDMyLTMybDE2MCAwIDAtMjk0LjdjLTIzLjUtMTAuMy00MS4yLTMxLjYtNDYuNC01Ny4zTDEyOCA5NmMtMTcuNyAwLTMyLTE0LjMtMzItMzJzMTQuMy0zMiAzMi0zMmwxMjggMGMxNC42LTE5LjQgMzcuOC0zMiA2NC0zMnM0OS40IDEyLjYgNjQgMzJ6bTU1LjYgMjg4bDE0NC45IDBMNTEyIDE5NS44IDQzOS42IDMyMHpNNTEyIDQxNmMtNjIuOSAwLTExNS4yLTM0LTEyNi03OC45Yy0yLjYtMTEgMS0yMi4zIDYuNy0zMi4xbDk1LjItMTYzLjJjNS04LjYgMTQuMi0xMy44IDI0LjEtMTMuOHMxOS4xIDUuMyAyNC4xIDEzLjhsOTUuMiAxNjMuMmM1LjcgOS44IDkuMyAyMS4xIDYuNyAzMi4xQzYyNy4yIDM4MiA1NzQuOSA0MTYgNTEyIDQxNnpNMTI2LjggMTk1LjhMNTQuNCAzMjBsMTQ0LjkgMEwxMjYuOCAxOTUuOHpNLjkgMzM3LjFjLTIuNi0xMSAxLTIyLjMgNi43LTMyLjFsOTUuMi0xNjMuMmM1LTguNiAxNC4yLTEzLjggMjQuMS0xMy44czE5LjEgNS4zIDI0LjEgMTMuOGw5NS4yIDE2My4yYzUuNyA5LjggOS4zIDIxLjEgNi43IDMyLjFDMjQyIDM4MiAxODkuNyA0MTYgMTI2LjggNDE2UzExLjcgMzgyIC45IDMzNy4xeiIvPgo8L3N2Zz4=&logoColor=%23ffffff)](https://github.com/pgroenbaek/pyffeditc/blob/master/LICENSE)

This Python module wraps the `ffeditc_unicode.exe` utility. The module allows you to compress and decompress MSTS files such as shape and world files on Windows.

> [!IMPORTANT]
> This module requires `ffeditc_unicode.exe` from Microsoft Train Simulator (MSTS).
> It is **not included** with this Python module. You must provide the executable from your own MSTS installation.

See also:
- [pytkutils](https://github.com/pgroenbaek/pytkutils) - handles compression and decompression of MSTS files such as shape and world file through the `TK.MSTS.Tokens.dll` library by Okrasa Ghia.

## Prerequisites

This Python module requires Windows, and in addition you must supply the `ffeditc_unicode.exe` utility found in MSTS installations yourself.

## Installation

### Install from PyPI

```sh
pip install --upgrade pyffeditc
```

### Install from wheel

If you have downloaded a `.whl` file from the [Releases](https://github.com/pgroenbaek/pyffeditc/releases) page, install it with:

```sh
pip install path/to/pyffeditc-<version>‑py3‑none‑any.whl
```

Replace `<version>` with the actual version number in the filename.

### Install from source

```sh
git clone https://github.com/pgroenbaek/pyffeditc.git
pip install --upgrade ./pyffeditc
```

## Usage

### Check if a file on disk is compressed

To check whether a file on disk is compressed, you can use the `is_compressed` function. This function returns `True` if the file is compressed and `False` if it is not. If the file is empty or its state cannot be determined, the function will return `None`.

```python
import pyffeditc

compressed = pyffeditc.is_compressed("./path/to/example.s")

if compressed is True:
    print("Compressed")
elif compressed is False:
    print("Uncompressed")
else:
    print("Could not determine (possibly empty file)")
```

### Compress or decompress files

The compression and decompression functions in this module use the `ffeditc_unicode.exe` utility found in MSTS installations. This utility is not included with the Python module.

Alternatively, you can use [pytkutils](https://github.com/pgroenbaek/pytkutils) on both Windows, Linux and macOS. But note that only compression appears to work properly using the `TK.MSTS.Tokens.dll` library by Okrasa Ghia.

You can also compress/decompress manually using `ffeditc_unicode.exe` through the [Shape File Manager](https://www.trainsim.com/forums/filelib-search-fileid?fid=78928) or use the [FFEDIT\_Sub v1.2](https://www.trainsim.com/forums/filelib-search-fileid?fid=40291) utility by Ged Saunders.

```python
import pyffeditc

ffeditc_path = "./path/to/ffeditc_unicode.exe"

# Compress and decompress in-place.
pyffeditc.compress(ffeditc_path, "./path/to/example.s")
pyffeditc.decompress(ffeditc_path, "./path/to/example.s")

# Compress and decompress to an output file.
pyffeditc.compress(ffeditc_path, "./path/to/example.s", "./path/to/output.s")
pyffeditc.decompress(ffeditc_path, "./path/to/example.s", "./path/to/output.s")
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

## Contributing

Contributions of all kinds are welcome. These could be suggestions, issues, bug fixes, documentation improvements, or new features.

For more details see the [contribution guidelines](/CONTRIBUTING.md).

## License

This Python module was created by Peter Grønbæk Andersen and is licensed under [GNU GPL v3](https://github.com/pgroenbaek/pyffeditc/blob/master/LICENSE).
