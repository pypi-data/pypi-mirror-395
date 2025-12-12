from __future__ import annotations

import os
import pathlib

__all__: list[str] = ["get_temp_dir", "set_temp_dir"]

def get_temp_dir() -> pathlib.Path:
    """
    Get the directory in which temporary directories will be created.
    This is configurable by setting the "CACHE_DIR" environment variable.
    Thread safe.
    """

def set_temp_dir(path: os.PathLike | str | bytes) -> None:
    """
    Set the temporary directory path.
    It must be a path to an existing directory.
    Anything using the previous path will continue using that path.
    """
