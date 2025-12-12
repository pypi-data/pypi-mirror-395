from pathlib import Path
import pytest
from configlite.config import BaseConfig


class ConfigTest(BaseConfig):
    foo: str = "foo"


def test_no_args() -> None:
    """Tests that an error is raised when no paths are provided."""

    with pytest.raises(ValueError):
        ConfigTest()


def test_both_args() -> None:
    """Tests that providing both path and paths prioritises path."""

    config = ConfigTest(path="config1.yaml", paths=["config2.yaml", "config3.yaml"])
    assert config._paths == ["config1.yaml"]
    assert config.path == Path("config1.yaml")
    assert config.filename == "config1.yaml"


def test_path_as_list() -> None:
    """Tests that providing path as a list works."""

    config = ConfigTest(path=["config1.yaml", "config2.yaml"])
    assert config._paths == ["config1.yaml", "config2.yaml"]
    assert config.path == Path("config2.yaml")
    assert config.filename == "config2.yaml"


def test_paths_as_empty_list() -> None:
    """Tests that providing paths as an empty list raises an error."""

    with pytest.raises(ValueError):
        ConfigTest(paths=[])


def test_paths_as_paths() -> None:
    """Tests that providing paths as a valid list works."""

    with pytest.raises(ValueError):
        ConfigTest(paths="config.yaml")


def test_empty_paths():
    """Tests that providing empty paths raises an error."""
    with pytest.raises(ValueError):
        ConfigTest(paths=[])
