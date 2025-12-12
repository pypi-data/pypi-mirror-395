"""tinycolors package public surface."""

from importlib import import_module
from importlib.metadata import version, PackageNotFoundError

# Package version: prefer installed package metadata, fallback to local _version
try:
    __version__ = version("tinycolors")
except PackageNotFoundError:
    try:
        # If you have a local _version.py with __version__ defined
        from ._version import __version__  # type: ignore
    except Exception:
        __version__ = "0.6.0"

# Attempt to import and re-export public names from likely submodules.
__all__ = ["__version__"]

_known_submodules = ("core", "color", "utils", "converters", "names", "cli")

for _sub in _known_submodules:
    try:
        _mod = import_module(f".{_sub}", __package__)
    except Exception:
        continue
    for _name in dir(_mod):
        if _name.startswith("_"):
            continue
        # Do not overwrite existing globals
        if _name in globals():
            continue
        globals()[_name] = getattr(_mod, _name)
        __all__.append(_name)

# Provide attribute access helpers (PEP 562)
def __getattr__(name: str):
    if name in globals():
        return globals()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

def __dir__():
    return sorted(__all__)

__author__ = "Razka Rizaldi"