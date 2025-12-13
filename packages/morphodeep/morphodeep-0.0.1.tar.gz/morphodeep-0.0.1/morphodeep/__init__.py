try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"


from .model_core import MorphoModel
from .config import Config


