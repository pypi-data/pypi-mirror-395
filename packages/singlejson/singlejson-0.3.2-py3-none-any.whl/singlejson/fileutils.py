"""Utils for handling IO and JSON operations."""
from __future__ import annotations

import json
import os
import logging
from dataclasses import dataclass
from json import dump, load
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, TypeAlias, Union, Optional

JSONSerializable: TypeAlias = (
        dict[str, "JSONSerializable"]
        | list["JSONSerializable"]
        | str
        | int
        | float
        | bool
        | None
)

PathOrSimilar = Union[str, os.PathLike[str]]


logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class JsonSerializationSettings:
    indent: int = 4
    sort_keys: bool = True
    ensure_ascii: bool = False


def abs_filename(file: PathOrSimilar) -> Path:
    """
    Return the absolute path of a file as pathlib.Path

    :param file: File to get the absolute path of
    :return: Absolute Path of file
    """
    return Path(file).expanduser().resolve()


def prepare(file: PathOrSimilar, default: str) -> None:
    """
    Prepare a file (check if it exists and create it if not)

    :param file: File to open
    :param default: default text to save if file is nonexistent
    """
    p = abs_filename(file)
    if not p.exists():
        dirpath = p.parent
        if str(dirpath):  # avoid trying to create ''
            dirpath.mkdir(parents=True, exist_ok=True)
        with p.open("w", encoding="utf-8") as writeable:
            writeable.write(default)


class FileAccessError(Exception):
    """Raised when the file cannot be accessed due to permissions or IO errors."""


class JSONFile:
    """
    A .json file on the disk.
    """

    __path: Path  # Full absolute path
    json: Any
    __default_data: Any
    __encoding: str
    __auto_save: bool

    def __init__(
            self,
            path: PathOrSimilar,
            default_data: Any = None,
            *,
            encoding: str = "utf-8",
            settings: Optional[JsonSerializationSettings] = None,
            auto_save: bool = True,
            **kwargs: Any,
    ) -> None:
        """
        Create a new json file instance and load data from disk

        :param path: path to file (str or PathLike)
        :param default_data: default data to save if file is empty / nonexistent
        :param encoding: file encoding
        :param settings: JsonSerializationSettings object
        :param auto_save: if True, context manager will save on exit
        """
        self.__path = abs_filename(path)
        self.__encoding = encoding
        self.settings = settings or DEFAULT_SERIALIZATION_SETTINGS
        self.__auto_save = auto_save
        # Backward-compat: support legacy keyword "default"
        if default_data is None and "default" in kwargs:
            default_data = kwargs["default"]
        if default_data is None:
            default_data = {}
        self.__default_data = default_data
        self.reload()

    def path(self) -> Path:
        """
        Return the absolute path of the file

        :return:
        """
        return self.__path

    def reload(self) -> None:
        """
        Reload from disk, recovering to default on invalid JSON.
        Raises FileAccessError on permission issues.
        """
        try:
            prepare(self.__path, default=json.dumps(self.__default_data, indent=4, sort_keys=True))
        except (PermissionError, OSError) as e:
            raise FileAccessError(f"Cannot prepare file '{self.__path}': {e}") from e

        try:
            with self.__path.open("r", encoding=self.__encoding) as file:
                self.json = load(file)
        except json.JSONDecodeError as e:
            # Recover to default data (do not raise)
            self.json = json.loads(json.dumps(self.__default_data))  # deep copy via json
            logger.log(logging.WARN, f"Cannot read json from file '{self.__path}'. Using default!\nDecoding error: {e}")
        except (PermissionError, OSError) as e:
            raise FileAccessError(f"Cannot read file '{self.__path}': {e}") from e

    def save(self, settings: JsonSerializationSettings | None = None) -> None:
        """
        Save the data to the disk

        :param settings: JsonSerializationSettings object
        """
        settings = settings or self.settings
        try:
            prepare(self.__path,
                    default=json.dumps(self.__default_data, indent=settings.indent, sort_keys=settings.sort_keys))
            with self.__path.open("w", encoding=self.__encoding) as file:
                dump(
                    self.json,
                    file,
                    indent=settings.indent,
                    sort_keys=settings.sort_keys,
                    ensure_ascii=settings.ensure_ascii,
                )
        except (PermissionError, OSError) as e:
            raise FileAccessError(f"Cannot write file '{self.__path}': {e}") from e

    def save_atomic(self, tmp_suffix: str = ".tmp") -> None:
        """
        Save atomically by writing to a temp file and replacing the target.
        Specify serialization settings with JSONFile.settings.

        :param tmp_suffix: suffix to add to target file
        :return:
        """
        settings = self.settings
        tmp_dir = self.__path.parent
        try:
            tmp_dir.mkdir(parents=True, exist_ok=True)
            with NamedTemporaryFile("w", encoding=self.__encoding, dir=tmp_dir, delete=False, suffix=tmp_suffix) as tf:
                json.dump(
                    self.json,
                    tf,
                    indent=settings.indent,
                    sort_keys=settings.sort_keys,
                    ensure_ascii=settings.ensure_ascii,
                )
                temp_name = tf.name
            os.replace(temp_name, self.__path)
        except (PermissionError, OSError) as e:
            # Best effort cleanup
            try:
                if "temp_name" in locals() and os.path.exists(temp_name):
                    os.remove(temp_name)
            except Exception:
                # Ignore cleanup errors to avoid masking the original exception
                pass
            raise FileAccessError(f"Cannot atomically write file '{self.__path}': {e}") from e

    # Context manager support
    def __enter__(self) -> JSONFile:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc_type is None and self.__auto_save:
            self.save()


# Default settings instance used by JSONFile.save() when not provided
DEFAULT_SERIALIZATION_SETTINGS = JsonSerializationSettings()
