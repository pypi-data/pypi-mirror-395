"""JAXGB"""

from importlib.metadata import PackageNotFoundError, metadata, version

try:
    __version__ = version(__name__)
    __license__ = metadata(__name__)["license"]
except PackageNotFoundError:
    __version__ = "0.0.0"  # Fallback for development mode
    __license__ = "Undefined"

__copyright__ = "2023, CEA and CNRS"
