from trap import io, post_processing
from trap.io import open_db
from trap.log import logger

try:
    from trap._version import version as __version__
except ImportError:
    __version__ = "v0.1.0.dev"
