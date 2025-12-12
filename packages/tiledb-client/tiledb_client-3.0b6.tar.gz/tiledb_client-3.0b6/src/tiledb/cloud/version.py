from tiledb.client.version import __commit_id__
from tiledb.client.version import commit_id

# We set version to 0.0.1 as that is the pypi dummy package
# This lets clients know that tiledb.cloud module is a shim
# and they are in a carrara environment
__version__ = "0.0.1"
__version_tuple__ = (0, 0, 1)
version = __version__
version_tuple = __version_tuple__

__all__ = [
    "__version__",
    "__version_tuple__",
    "version",
    "version_tuple",
    "__commit_id__",
    "commit_id",
]
