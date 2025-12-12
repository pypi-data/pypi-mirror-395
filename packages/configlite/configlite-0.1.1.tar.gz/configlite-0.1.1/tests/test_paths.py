import os
from pathlib import Path

import pytest
import yaml
from configlite.config import BaseConfig

class ConfigTest(BaseConfig):
    foo: str = "foo"


def test_default_to_last():
    """Tests that the default path is the last one in the list."""

    workdir = Path(os.getcwd()) / "config_local.yaml"
    lastdir = workdir / ".config" / "config.yaml"

    config = ConfigTest(paths=[workdir, lastdir])

    assert config.path == lastdir

    # now test that creating a config in the higher priority directories works
    with open(workdir, "w+") as o:
        yaml.dump({"foo": "bar"}, o)

    assert config.path == workdir
    assert config.foo == "bar"


@pytest.mark.parametrize(
    "path",
    [
        "$HOME/config.yaml",
        "~/config.yaml",
    ]
)
def test_home_expansion(path: str) -> None:
    """Tests that paths are properly expanded."""

    config = ConfigTest(paths=[path])

    expected_path = Path(os.path.expanduser("~")) / "config.yaml"

    assert config.path == expected_path


def test_arbitrary_variable() -> None:
    """Tests that arbitrary environment variables are expanded."""

    os.environ["CONFIGLITE_TEST_PATH"] = "config_env.yaml"

    config = ConfigTest(paths=["$CONFIGLITE_TEST_PATH"])

    expected_path = Path(os.getcwd()) / "config_env.yaml"

    assert config.abspath == expected_path
