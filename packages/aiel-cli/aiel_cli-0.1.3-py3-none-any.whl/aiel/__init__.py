from importlib.metadata import version as _pkg_version, PackageNotFoundError

__all__ = ["__version__"]

try:
    __version__ = _pkg_version("aiel-cli")
except PackageNotFoundError:
    __version__ = "0+unknown"