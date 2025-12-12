from configlite.config import BaseConfig
import yaml

def test_ensure_empty() -> None:
    assert BaseConfig("test.yaml").attributes == []


def test_attributes() -> None:
    class TestConfig(BaseConfig):
        test = 10

    assert TestConfig("test.yaml").attributes == ["test"]


def test_update(simple_config) -> None:
    with open("test.yaml", "w+") as o:
        yaml.dump({"test": "bar"}, o)

    print(type(simple_config.test))

    assert simple_config.test == "bar"
