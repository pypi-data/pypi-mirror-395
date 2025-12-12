import os
from pathlib import Path
from typing import Any
import yaml


class BaseConfig:
    """Lightweight Self-Healing config object."""

    def __init__(
        self, path: Path | str | None = None, paths: list[Path | str] | None = None
    ) -> None:
        """Initialize the config object.

        Args:
            path:
                The path to the config file. If the file does not exist, it will be created.
            paths:
                A list of paths to search for the config file.
                If it is not found in any, the last one in the list is used for creation.
        """
        # Prioritise direct assignment
        if path is not None:
            # cover the case of BaseConfig(path=["a", "b"])
            if isinstance(path, (list, tuple)):
                self._paths = path
            else:
                self._paths = [path]
        elif paths is not None:
            if not isinstance(paths, (list, tuple)) or len(paths) == 0:
                raise ValueError(
                    f"`paths` (type {type(paths)}) must be a valid list of paths"
                )
            self._paths = paths
        else:
            raise ValueError("Either `path` or `paths` must be provided.")

        self._attributes = {}
        for k, v in self.__class__.__dict__.items():
            if k in BaseConfig.__dict__:
                continue
            if not k.startswith("_"):
                self._attributes[k] = v
                setattr(self, k, DeferredValue(k))

    def __getattribute__(self, name: str) -> Any:
        """Proxy attribute access. If the item is deferred, return the get instead."""
        item = object.__getattribute__(self, name)
        if isinstance(item, DeferredValue):
            return self.read()[item.value]
        else:
            return item

    @property
    def filename(self) -> str:
        """Filename, excluding path."""
        return self._path.name

    @property
    def path(self) -> Path:
        """Path to the config file."""
        return self._find_path()

    @property
    def abspath(self) -> Path:
        """Absolute path to the config file."""
        return self.path.resolve()

    def _find_path(self) -> Path:
        """Dynamically find the path"""
        path_obj = None
        for path in self._paths:
            path_obj = Path(os.path.expandvars(str(path))).expanduser()
            if path_obj.exists():
                return path_obj
        if path_obj is None:
            raise FileNotFoundError(f"Path list is malformed: {self._paths}")
        return path_obj

    def _read(self) -> dict[str, Any]:
        """Read the config file and return its contents."""
        with self.path.open("r") as f:
            return yaml.safe_load(f)

    def read(self) -> dict[str, Any]:
        """Read the config file and return its contents.

        If it does not exist, creates the file and fills it with default vaulues.
        """
        if not self.path.exists():
            self.write()
        return self._read()

    def write(self) -> None:
        """Write to the config, ignoring any existing values."""
        defaults = self._attributes.copy()
        if self.path.exists():
            defaults.update(self._read())
        with self.path.open("w+") as f:
            yaml.dump(defaults, f)

    @property
    def attributes(self) -> list[str]:
        """List of attributes that are defined in this config."""
        return [attr for attr in self._attributes.keys()]


class DeferredValue:
    """Stub class for deferring value access."""

    __slots__ = ["_parent", "_value"]

    def __init__(self, value: str) -> None:
        """Create the stub.

        Args:
            value: The name of the variable to access.
        """
        if not isinstance(value, str):
            raise TypeError("Value target must be a string")

        self._value = value

    @property
    def value(self) -> str:
        return self._value
