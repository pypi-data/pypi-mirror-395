from configlite.config import BaseConfig


class ConfigTest(BaseConfig):
    test_value: int = 42
    name: str = "Test_Name"

    @property
    def uppercase_name(self) -> str:
        return self.name.upper()


def test_extra_methods():
    config = ConfigTest(path="test.yaml")
    assert config.name == "Test_Name"
    assert config.uppercase_name == "TEST_NAME"
