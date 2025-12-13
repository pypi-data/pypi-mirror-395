![cpf-fmt for Python](https://br-utils.vercel.app/img/cover_cpf-fmt.jpg)

[![PyPI Version](https://img.shields.io/pypi/v/cpf-fmt)](https://pypi.org/project/cpf-fmt)
[![PyPI Downloads](https://img.shields.io/pypi/dm/cpf-fmt)](https://pypi.org/project/cpf-fmt)
[![Python Version](https://img.shields.io/pypi/pyversions/cpf-fmt)](https://www.python.org/)
[![Test Status](https://img.shields.io/github/actions/workflow/status/LacusSolutions/br-utils-py/ci.yml?label=ci/cd)](https://github.com/LacusSolutions/br-utils-py/actions)
[![Last Update Date](https://img.shields.io/github/last-commit/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py)
[![Project License](https://img.shields.io/github/license/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE)

Utility function/class to format CPF (Brazilian ID document).

## Python Support

| ![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) | ![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) | ![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | ![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white) | ![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white) |
|--- | --- | --- | --- | --- |
| Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ |

## Installation

```bash
$ pip install cpf-fmt
```

## Import

```python
# Using class-based resource
from cpf_fmt import CpfFormatter

# Or using function-based one
from cpf_fmt import cpf_fmt
```

## Usage

### Object-Oriented Usage

```python
formatter = CpfFormatter()
cpf = '47844241055'

print(formatter.format(cpf))       # returns '478.442.410-55'

# With options
print(formatter.format(
    cpf,
    hidden=True,
    hidden_key='#',
    hidden_start=3,
    hidden_end=10
))  # returns '478.###.###-##'
```

The options can be provided to the constructor or the `format()` method. If passed to the constructor, the options will be attached to the `CpfFormatter` instance. When passed to the `format()` method, it only applies the options to that specific call.

```python
cpf = '12345678910'
formatter = CpfFormatter(hidden=True)

print(formatter.format(cpf))                  # '123.***.***-**'
print(formatter.format(cpf, hidden=False))    # '123.456.789-10' merges the options to the instance's
print(formatter.format(cpf))                  # '123.***.***-**' uses only the instance options
```

### Functional programming

The helper function `cpf_fmt()` is just a functional abstraction. Internally it creates an instance of `CpfFormatter` and calls the `format()` method right away.

```python
cpf = '47844241055'

print(cpf_fmt(cpf))       # returns '478.442.410-55'

print(cpf_fmt(cpf, hidden=True))     # returns '478.***.***-**'

print(cpf_fmt(cpf, dot_key='', dash_key='_'))     # returns '478442410_55'
```

### Formatting Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `escape` | `bool \| None` | `False` | Whether to HTML escape the result |
| `hidden` | `bool \| None` | `False` | Whether to hide digits with a mask |
| `hidden_key` | `str \| None` | `'*'` | Character to replace hidden digits |
| `hidden_start` | `int \| None` | `3` | Starting index for hidden range (0-10) |
| `hidden_end` | `int \| None` | `10` | Ending index for hidden range (0-10) |
| `dot_key` | `str \| None` | `'.'` | String to replace dot characters |
| `dash_key` | `str \| None` | `'-'` | String to replace dash character |
| `on_fail` | `Callable \| None` | `lambda value, error=None: value` | Fallback function for invalid input |

## Contribution & Support

We welcome contributions! Please see our [Contributing Guidelines](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md) for details. But if you find this project helpful, please consider:

- ⭐ Starring the repository
- 🤝 Contributing to the codebase
- 💡 [Suggesting new features](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reporting bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE) file for details.

## Changelog

See [CHANGELOG](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cpf-fmt/CHANGELOG.md) for a list of changes and version history.

---

Made with ❤️ by [Lacus Solutions](https://github.com/LacusSolutions)
