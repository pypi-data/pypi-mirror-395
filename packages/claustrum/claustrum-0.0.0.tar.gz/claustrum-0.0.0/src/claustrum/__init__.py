from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("claustrum")
except PackageNotFoundError:
    __version__ = "0.0.0"