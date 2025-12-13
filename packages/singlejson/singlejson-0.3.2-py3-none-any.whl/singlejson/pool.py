"""The main files handling the file pool."""
from __future__ import annotations

from threading import Lock
from typing import Any, Dict, Optional

from .fileutils import JSONFile, abs_filename, PathOrSimilar, JSONSerializable
from pathlib import Path


_pool_lock: Lock = Lock()
_file_pool: Dict[Path, JSONFile] = {}


def load(path: PathOrSimilar, default_data: JSONSerializable = None, **kwargs: Any) -> JSONFile:
    """
    Open a JSONFile (synchronously) with pooling per absolute path.
    Backward-compat: accepts legacy "default" keyword.
    """
    p = abs_filename(path)
    key = p
    with _pool_lock:
        if key not in _file_pool:
            jf = JSONFile(p, default_data=default_data, **kwargs)
            _file_pool[key] = jf
        return _file_pool[key]


def sync() -> None:
    """
    Sync all pooled files to the filesystem.
    If you wish to adjust settings, change the default or change the JsonFile.settings property.
    """
    with _pool_lock:
        for file in list(_file_pool.values()):
            file.save()


def reset() -> None:
    """
    Clear the file pool WITHOUT saving.
    """
    with _pool_lock:
        _file_pool.clear()


def close(path: Optional[PathOrSimilar] = None, *, save: bool = True) -> None:
    """
    Close one file (by path) or all files, optionally saving first.
    If you wish to adjust settings, change the default or change the JsonFile.settings property.

    :param path: The path of the file to close.
    :param save: Whether to save the file or not.
    """
    with _pool_lock:
        if path is None:
            # Close all
            if save:
                for file in list(_file_pool.values()):
                    file.save()
            _file_pool.clear()
        else:
            p = abs_filename(path)
            jf = _file_pool.pop(p, None)
            if jf and save:
                jf.save()
