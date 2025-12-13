# ruff: noqa: F401, I001

from . import api, context, models, types, warnings
from ._load_udf import load, load_async
from ._options import env as _env
from ._options import options
from ._public_api import ingest, ingest_nongeospatial
from ._run import run, run_async
from ._secrets import secrets
from ._submit import submit
from ._udf import udf
from ._utils import utils
from ._version import __version__

# TODO: fused.{download, get_chunk_from_table, get_chunks_metadata} are deprecated here
from .core import cache, download, file_path, get_chunk_from_table, get_chunks_metadata
from .ipython.fused_magics import autoload_extension as _autoload_extension
from .ipython.fused_magics import load_ipython_extension

# import last to avoid circular imports
from . import _h3 as h3
from . import _fasttortoise
from ._fasttortoise import find_dataset, register_dataset

__all__ = [
    "api",
    "cache",
    "download",
    "context",
    "_fasttortoise",
    "file_path",
    "find_dataset",
    "get_chunk_from_table",
    "get_chunks_metadata",
    "h3",
    "get_header",
    "get_headers",
    "ingest",
    # "ingest_nongeospatial",
    "load",
    "load_async",
    # "models",
    "register_dataset",
    "run",
    "run_async",
    # "secrets",
    "submit",
    # "types",
    "udf",
    "utils",
    # "warnings",
    # "options",
    # "_env",
    "load_ipython_extension",
    "__version__",
]

_autoload_extension()
