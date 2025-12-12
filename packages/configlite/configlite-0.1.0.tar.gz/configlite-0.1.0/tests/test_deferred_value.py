import pytest
from configlite.config import DeferredValue


@pytest.mark.parametrize("value", [10, True, None])
def test_invalid_value(value) -> None:
    with pytest.raises(TypeError):
        DeferredValue(value)
