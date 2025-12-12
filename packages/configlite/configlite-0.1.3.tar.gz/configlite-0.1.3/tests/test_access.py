from configlite.config import BaseConfig


class ConfigTest(BaseConfig):
    foo: str = "foo"


def test_attribute_access():
    cfg = ConfigTest("test_config.yaml")

    assert cfg.foo == "foo"


def test_subscript_access():
    cfg = ConfigTest("test_config.yaml")

    assert cfg["foo"] == "foo"
