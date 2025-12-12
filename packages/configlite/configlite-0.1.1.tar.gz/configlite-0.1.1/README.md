# ConfigLite

A lightweight self-healing config handler.

## Quickstart

Subclass from the base `BaseConfig` object and add your variables and defaults.

You can then set import this from wherever is needed and access properties.


## Installation

`git clone` this repository, then use `pip install .` to install it in your current environment.


## Usage

### Creating a Config
Create a subclass of the base `BaseConfig` object, adding your parameters and their defaults.

For example:

```python
from configlite import BaseConfig


class MyConfig(BaseConfig):
    value: int = 10
    name: str = "test"
    pi: float = 3.14
```

### Access
To use your created config, there are two methods:

- "globally", where a single instance created.
- "locally", initialising the class where needed.

#### Global

To create a global config, set up the config as a parameter in the toplevel `__init__.py`:
```python
CONFIG = MyConfig("./path/to/config.yaml")
```

Then in the rest of your code you may import this object:

```python
from my_package import CONFIG

value = CONFIG.value
```

This is most useful if your code requires a single config file for everything.

#### Local
Or a local config, where you create an instance of your subclass wherever it is needed:

```python
from my_package import MyConfig

config = MyConfig("./path/to/config.yaml")

value = config.value
```

This can be useful if you are juggling multiple different config files dynamically.

## Paths

The `BaseConfig` object can take either a single path, or a list of paths.

If a list is passed, the config will search each one in order, using the last one in the list if none are found.

### Path Lists

Lets say you create a config this way:

```python
class Config(BaseConfig):
    ...

CONFIG = Config(
    paths=[
        "config.yaml",
        "~/.config/app/config.yaml",
    ]
)
```

In this case, `Config` will take these steps:

1) Search for `config.yaml` in the current working directory.
2) If not found, search for `~/.config/app/config.yaml`.
3) If still no file exists, create a default config at `~/.config/app/config.yaml`

If we get to step 3, but then create a new config at `./config.yaml`, this will take priority over the one found at `~/.config/app/config.yaml`.

## Example

See `usage.py` for an example.
