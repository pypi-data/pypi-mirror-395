import os
from pathlib import Path

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
