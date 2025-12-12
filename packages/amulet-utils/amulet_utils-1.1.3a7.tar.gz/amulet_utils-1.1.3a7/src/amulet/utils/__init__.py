import logging as _logging

from . import _version

__version__ = _version.get_versions()["version"]

# init a default logger
_logging.basicConfig(level=_logging.INFO, format="%(levelname)s - %(message)s")


def _init() -> None:
    import os
    import sys
    import ctypes
    import platformdirs

    if sys.platform == "win32":
        lib_path = os.path.join(os.path.dirname(__file__), "amulet_utils.dll")
    elif sys.platform == "darwin":
        lib_path = os.path.join(os.path.dirname(__file__), "libamulet_utils.dylib")
    elif sys.platform == "linux":
        lib_path = os.path.join(os.path.dirname(__file__), "libamulet_utils.so")
    else:
        raise RuntimeError(f"Unsupported platform {sys.platform}")

    # Load the shared library
    ctypes.cdll.LoadLibrary(lib_path)

    from ._amulet_utils import init

    init(sys.modules[__name__])

    from .temp import set_temp_dir

    cache_dir = os.environ.get("CACHE_DIR")
    if cache_dir is None:
        cache_dir = platformdirs.user_cache_dir("AmuletTeam", "AmuletTeam")
    os.makedirs(cache_dir, exist_ok=True)
    set_temp_dir(cache_dir)


_init()
