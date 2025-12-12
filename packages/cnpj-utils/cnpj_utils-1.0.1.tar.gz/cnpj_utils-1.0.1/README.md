![cnpj-utils for Python](https://br-utils.vercel.app/img/cover_cnpj-utils.jpg)

[![PyPI Version](https://img.shields.io/pypi/v/cnpj-utils)](https://pypi.org/project/cnpj-utils)
[![PyPI Downloads](https://img.shields.io/pypi/dm/cnpj-utils)](https://pypi.org/project/cnpj-utils)
[![Python Version](https://img.shields.io/pypi/pyversions/cnpj-utils)](https://www.python.org/)
[![Test Status](https://img.shields.io/github/actions/workflow/status/LacusSolutions/br-utils-py/ci.yml?label=ci/cd)](https://github.com/LacusSolutions/br-utils-py/actions)
[![Last Update Date](https://img.shields.io/github/last-commit/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py)
[![Project License](https://img.shields.io/github/license/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE)

Toolkit to deal with CNPJ data (Brazilian employer ID): validation, formatting and generation of valid IDs.

## Python Support

| ![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) | ![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) | ![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | ![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white) | ![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white) |
|--- | --- | --- | --- | --- |
| Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ |

## Installation

```bash
$ pip install cnpj-utils
```

## Import

```python
# Using class-based resource
from cnpj_utils import CnpjUtils

# Or using function-based approach
from cnpj_utils import cnpj_fmt, cnpj_gen, cnpj_val

# Or using the default instance
from cnpj_utils import cnpj_utils
```

## Usage

### Object-Oriented Usage

The `CnpjUtils` class provides a unified interface for all CNPJ operations:

```python
cnpj_utils = CnpjUtils()
cnpj = '03603568000195'

# Format CNPJ
print(cnpj_utils.format(cnpj))       # returns '03.603.568/0001-95'

# Validate CNPJ
print(cnpj_utils.is_valid(cnpj))      # returns True

# Generate CNPJ
print(cnpj_utils.generate())          # returns '65453043000178'
```

#### With Configuration Options

You can configure the formatter and generator options in the constructor:

```python
from cnpj_fmt import CnpjFormatterOptions
from cnpj_gen import CnpjGeneratorOptions

cnpj_utils = CnpjUtils(
    formatter=CnpjFormatterOptions(
        hidden=True,
        hidden_key='#',
        hidden_start=5,
        hidden_end=13
    ),
    generator=CnpjGeneratorOptions(format=True)
)

cnpj = '03603568000195'
print(cnpj_utils.format(cnpj))       # returns '03.603.###/####-##'
print(cnpj_utils.generate())          # returns '73.008.535/0005-06'
```

The options can be provided to the constructor or the respective methods. If passed to the constructor, the options will be attached to the `CnpjUtils` instance. When passed to the methods, it only applies the options to that specific call.

```python
cnpj_utils = CnpjUtils(
    formatter=CnpjFormatterOptions(hidden=True)
)

cnpj = '03603568000195'
print(cnpj_utils.format(cnpj))                  # '03.603.***/****-**'
print(cnpj_utils.format(cnpj, hidden=False))    # '03.603.568/0001-95' (overrides instance options)
print(cnpj_utils.format(cnpj))                  # '03.603.***/****-**' (uses instance options again)
```

### Functional Programming

The package also provides standalone functions for each operation:

```python
cnpj = '03603568000195'

# Format CNPJ
print(cnpj_fmt(cnpj))                 # returns '03.603.568/0001-95'

# Validate CNPJ
print(cnpj_val(cnpj))                 # returns True

# Generate CNPJ
print(cnpj_gen())                     # returns '65453043000178'
```

Or use the default instance:

```python
from cnpj_utils import cnpj_utils

cnpj = '03603568000195'
print(cnpj_utils.format(cnpj))        # returns '03.603.568/0001-95'
print(cnpj_utils.is_valid(cnpj))      # returns True
print(cnpj_utils.generate())          # returns '65453043000178'
```

## API Reference

### Formatting (`cnpj_fmt` / `CnpjUtils.format`)

Formats a CNPJ string with customizable delimiters and masking options.

```python
cnpj_utils.format(
    cnpj_string: str,
    hidden: bool | None = None,
    hidden_key: str | None = None,
    hidden_start: int | None = None,
    hidden_end: int | None = None,
    dot_key: str | None = None,
    slash_key: str | None = None,
    dash_key: str | None = None,
    escape: bool | None = None,
    on_fail: Callable | None = None,
) -> str
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `hidden` | `bool \| None` | `False` | Whether to hide digits with a mask |
| `hidden_key` | `str \| None` | `'*'` | Character to replace hidden digits |
| `hidden_start` | `int \| None` | `5` | Starting index for hidden range (0-13) |
| `hidden_end` | `int \| None` | `13` | Ending index for hidden range (0-13) |
| `dot_key` | `str \| None` | `'.'` | String to replace dot characters |
| `slash_key` | `str \| None` | `'/'` | String to replace slash character |
| `dash_key` | `str \| None` | `'-'` | String to replace dash character |
| `escape` | `bool \| None` | `False` | Whether to HTML escape the result |
| `on_fail` | `Callable \| None` | `lambda value, error=None: value` | Fallback function for invalid input |

**Examples:**

```python
cnpj = '03603568000195'

# Basic formatting
print(cnpj_fmt(cnpj))                 # '03.603.568/0001-95'

# With hidden digits
print(cnpj_fmt(cnpj, hidden=True))    # '03.603.***/****-**'

# Custom delimiters
print(cnpj_fmt(cnpj, dot_key='', slash_key='|', dash_key='_'))  # '03603568|0001_95'

# Custom hidden range
print(cnpj_fmt(cnpj, hidden=True, hidden_start=2, hidden_end=8, hidden_key='#'))  # '03###.###/0001-95'
```

### Generation (`cnpj_gen` / `CnpjUtils.generate`)

Generates valid CNPJ numbers with optional formatting and prefix completion.

```python
cnpj_utils.generate(
    format: bool | None = None,
    prefix: str | None = None,
) -> str
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `format` | `bool \| None` | `False` | Whether to format the output |
| `prefix` | `str \| None` | `''` | Prefix to complete with valid digits (1-12 digits) |

**Examples:**

```python
# Generate random CNPJ
print(cnpj_gen())                     # '65453043000178'

# Generate formatted CNPJ
print(cnpj_gen(format=True))          # '73.008.535/0005-06'

# Complete a prefix
print(cnpj_gen(prefix='45623767'))    # '45623767000296'

# Complete and format
print(cnpj_gen(prefix='456237670002', format=True))  # '45.623.767/0002-96'
```

### Validation (`cnpj_val` / `CnpjUtils.is_valid`)

Validates CNPJ numbers using the official algorithm.

```python
cnpj_utils.is_valid(cnpj_string: str) -> bool
```

**Examples:**

```python
# Valid CNPJ
print(cnpj_val('98765432000198'))      # True
print(cnpj_val('98.765.432/0001-98'))  # True

# Invalid CNPJ
print(cnpj_val('98765432000199'))      # False
```

## Advanced Usage

### Accessing Individual Components

You can access the individual formatter, generator, and validator instances:

```python
cnpj_utils = CnpjUtils()

# Access individual components
formatter = cnpj_utils.formatter
generator = cnpj_utils.generator
validator = cnpj_utils.validator

# Use them directly
formatter.format('03603568000195', hidden=True)
generator.generate(format=True)
validator.is_valid('03603568000195')
```

### Custom Error Handling

```python
cnpj = '123'  # Invalid length

# Custom fallback
def custom_fail(value, error=None):
    return f"Invalid CNPJ: {value}"

print(cnpj_fmt(cnpj, on_fail=custom_fail))  # 'Invalid CNPJ: 123'

# Return original value (default behavior)
print(cnpj_fmt(cnpj))  # '123'
```

## Dependencies

This package is built on top of the following specialized packages:

- [`cnpj-fmt`](https://pypi.org/project/cnpj-fmt) - CNPJ formatting
- [`cnpj-gen`](https://pypi.org/project/cnpj-gen) - CNPJ generation
- [`cnpj-val`](https://pypi.org/project/cnpj-val) - CNPJ validation

## Contribution & Support

We welcome contributions! Please see our [Contributing Guidelines](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md) for details. But if you find this project helpful, please consider:

- ⭐ Starring the repository
- 🤝 Contributing to the codebase
- 💡 [Suggesting new features](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reporting bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE) file for details.

## Changelog

See [CHANGELOG](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cnpj-utils/CHANGELOG.md) for a list of changes and version history.

---

Made with ❤️ by [Lacus Solutions](https://github.com/LacusSolutions)
