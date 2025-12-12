from configlite.config import BaseConfig


class ConfigA(BaseConfig):
    param1: str = "value1"


class ConfigB(BaseConfig):
    """Simulate updating the config to include a new parameter."""
    param1: str = "value1"
    param2: str = "value2"


def test_update_config():
    cfg = ConfigA("config.yaml")

    assert cfg.param1 == "value1"

    assert cfg.path.exists()

    # Simulate updating the config class to add a new parameter"
    cfg = ConfigB("config.yaml")
    assert cfg.param1 == "value1"
    assert cfg.param2 == "value2"