from importlib.metadata import version

from ._core import goodbye, hello

__version__ = version(__package__ or __name__)  # Python 3.9+ only
__all__ = ["goodbye", "hello", "__version__"]
