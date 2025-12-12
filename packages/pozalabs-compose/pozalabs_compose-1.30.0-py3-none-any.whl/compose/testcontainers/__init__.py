from .._internal import is_package_installed

if not is_package_installed("testcontainers"):
    raise ImportError("Install `testcontainers` to use testing fixtures")

from .mongodb import MongoDbContainer

__all__ = ["MongoDbContainer"]
