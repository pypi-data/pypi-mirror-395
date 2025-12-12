from .._internal import is_package_installed

if not is_package_installed("httpx"):
    raise ImportError("Install `httpx` extra to use httpx features")

from .auth.header import HeaderAuth

__all__ = ["HeaderAuth"]
