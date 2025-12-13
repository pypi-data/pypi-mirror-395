from .generation_models import *  # noqa: F403
from .v2_output_schema import *  # noqa: F403
from .utils import reform_for_multiindex_df  # noqa: F403
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("generation-models")
except PackageNotFoundError:
    __version__ = "generation"
