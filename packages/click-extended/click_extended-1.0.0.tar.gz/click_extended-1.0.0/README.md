![Banner](./assets/click-extended-banner.png)

# Click Extended

![top language](https://img.shields.io/github/languages/top/marcusfrdk/click-extended)
![code size](https://img.shields.io/github/languages/code-size/marcusfrdk/click-extended)
![last commit](https://img.shields.io/github/last-commit/marcusfrdk/click-extended)
![tests](https://github.com/marcusfrdk/click-extended/actions/workflows/tests.yml/badge.svg)
![release](https://github.com/marcusfrdk/click-extended/actions/workflows/release.yml/badge.svg)
![issues](https://img.shields.io/github/issues/marcusfrdk/click-extended)
![contributors](https://img.shields.io/github/contributors/marcusfrdk/click-extended)
![pypi](https://img.shields.io/pypi/v/click-extended)
![license](https://img.shields.io/github/license/marcusfrdk/click-extended)
![downloads](https://static.pepy.tech/badge/click-extended)
![monthly downloads](https://static.pepy.tech/badge/click-extended/month)

An extension of the [Click](https://github.com/pallets/click) library with additional features like aliasing, asynchronous support, an extended decorator API and more.

## Features

- **Decorator API**: Extend the functionality your command line by adding custom data sources, data processing pipelines, and more.
- **Aliasing**: Use aliases for groups and commands to reduce boilerplate and code repetition.
- **Tags**: Use tags to group several data sources together to apply batch processing.
- **Async Support**: Native support for declaring functions and methods asynchronous.
- **Environment Variables**: Built-in support for loading and using environment variables as a data source.
- **Full Type Support**: Built with type-hinting from the ground up, meaning everything is fully typed.
- **Improved Errors**: Improved error output like tips, debugging, and more.
- **Short Flag Concatenation**: Automatically support concatenating short hand flags where `-r -f` is the same as `-rf`.

## Installation

```bash
pip install click-extended
```

## Requirements

- **Python**: 3.10 or higher

## Quick Start

### Basic Command

```python
from click_extended import command, argument, option

@command(aliases="ping")
@argument("value")
@option("--count", "-c", default=1)
def my_function(value: str, count: int):
    """This is the help message for my_function."""
    if _ in range(count):
        print(value)

if __name__ == "__main__":
    my_function()
```

```bash
$ python cli.py "Hello world"
Hello world
```

```bash
$ python cli.py "Hello world" --count 3
Hello world
Hello world
Hello world
```

### Basic Command Line Interface

```python
from click_extended import group, argument, option

@group()
def my_group():
    """This is the help message for my_group."""
    print("Running initialization code...")

@my_group.command(aliases=["ping", "repeat"])
@argument("value")
@option("--count", "-c", default=1)
def my_function(value: str, count: int):
    """This is the help message for my_function."""
    if _ in range(count):
        print(value)

if __name__ == "__main__":
    my_group()
```

```bash
$ python cli.py my_function "Hello world"
Running initialization code...
Hello world
```

```bash
$ python cli.py my_function "Hello world" --count 3
Running initialization code...
Hello world
Hello world
Hello world
```

### Using Environment Variables

```python
from click_extended import group, command, env

@group()
def my_group():
    """This is the help message for my_group."""

@my_group.command()
@env("API_KEY")
def my_function_1(api_key: str | None):
    """This is the help message for my_function."""
    print(f"The API key is: {api_key}")

@my_group.command()
@env("API_KEY", required=True)
def my_function_2(api_key: str):
    """This is the help message for my_function."""
    print(f"The API key is: {api_key}")

if __name__ == "__main__":
    my_group()
```

```bash
$ python cli.py my_function_1
The API key is: None
```

```bash
$ API_KEY=api-key python cli.py my_function_1
The API key is: api-key
```

```bash
$ python cli.py my_function_2
ProcessError (my_function_2): Required environment variable 'API_KEY' is not set.
```

```bash
$ API_KEY=api-key python cli.py my_function_2
The API key is: api-key
```

### Load CSV Data

```python
import pandas as pd
from click_extended import command, argument
from click_extended.decorators import to_path, load_csv

@command()
@argument("file", param="data")
@to_path(extensions=["csv"], exists=True)
@load_csv()
def my_command(data: dict[str, Any], *args: Any, **kwargs: Any) -> None:
    df = pd.DataFrame(data)
    print(df.head())
```

_Note: `pandas` is not installed in this library and must be installed manually due to size._

### Pre-Built Children

This library includes a vast number of pre-built children, everything from checking values to transforming values.

```python
from click_extended import command, argument, option
from click_extended.decorators import to_snake_case, strip, is_email, minimum, dependencies

@command()
@dependencies("username", "email", "password")
@argument("username")
@to_snake_case()
@strip()
@option("email")
@is_email()
@option("password")
@minimum(8)
def create_account(username: str, email: str, password: str) -> None:
    print("Username:", username)
    print("Email:", email)
    print("Password:", password)
```

### Custom Nodes

If the library does not include a decorator you need, you can easily create your own. Read more about creating your own [children](./docs/core/CHILD_NODE.md), [validators](./docs/core/VALIDATION_NODE.md), [child validators](./docs/core/CHILD_VALIDATION_NODE.md) or [parents](./docs/core/PARENT_NODE.md).

```python
from typing import Any

from click_extended import group, argument, option
from click_extended.classes import ChildNode
from click_extended.types import Context, Decorator

class MyCustomChild(ChildNode):
    def handle_string(
        self,
        value: str,
        context: Context,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        if value == "invalid":
            raise ValueError("The value 'invalid' is not valid")

        return value.upper()

def my_custom_child() -> Decorator:
    """Checks if the value is invalid and converts it to uppercase."""
    return MyCustomChild.as_decorator()


@group()
def my_group():
    """This is the help message for my_group."""
    print("Running initialization code...")

@my_group.command(aliases=["ping", "repeat"])
@argument("value")
@my_custom_child()
def my_function(value: str):
    """This is the help message for my_function."""
    print(f"The value '{value}' should be uppercase.")

if __name__ == "__main__":
    my_group()
```

```bash
$ python cli.py my_function valid
The value 'VALID' should be uppercase.
```

```bash
$ python cli.py my_function invalid
ValueError (my_function): "The value 'invalid' is not valid"
```

## Documentation

The full documentation is [available here](./docs/README.md) and goes through the full library, from explaining design choices, how to use the library, and much more.

## Contributing

Contributors are more than welcome to work on this project. Read the [contribution documentation](./CONTRIBUTING.md) to learn more.

## License

This project is licensed under the MIT License, see the [license file](./LICENSE) for details.

## Acknowledgements

This project is built on top of the [Click](https://github.com/pallets/click) library.
