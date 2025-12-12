from importlib.metadata import PackageNotFoundError, version as _v

try:
    __version__ = _v("aiel-sdk")
except PackageNotFoundError:
    __version__ = "0+unknown"
