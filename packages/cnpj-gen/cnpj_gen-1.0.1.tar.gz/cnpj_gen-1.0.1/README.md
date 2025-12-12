![cnpj-gen for Python](https://br-utils.vercel.app/img/cover_cnpj-gen.jpg)

[![PyPI Version](https://img.shields.io/pypi/v/cnpj-gen)](https://pypi.org/project/cnpj-gen)
[![PyPI Downloads](https://img.shields.io/pypi/dm/cnpj-gen)](https://pypi.org/project/cnpj-gen)
[![Python Version](https://img.shields.io/pypi/pyversions/cnpj-gen)](https://www.python.org/)
[![Test Status](https://img.shields.io/github/actions/workflow/status/LacusSolutions/br-utils-py/ci.yml?label=ci/cd)](https://github.com/LacusSolutions/br-utils-py/actions)
[![Last Update Date](https://img.shields.io/github/last-commit/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py)
[![Project License](https://img.shields.io/github/license/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE)

Utility function/class to generate valid CNPJ (Brazilian employer ID).

## Python Support

| ![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) | ![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) | ![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | ![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white) | ![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white) |
|--- | --- | --- | --- | --- |
| Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ |

## Installation

```bash
$ pip install cnpj-gen
```

## Import

```python
# Using class-based resource
from cnpj_gen import CnpjGenerator

# Or using function-based one
from cnpj_gen import cnpj_gen
```

## Usage

### Object-Oriented Usage

```python
generator = CnpjGenerator()
cnpj = generator.generate()  # returns '65453043000178'

# With options
cnpj = generator.generate(
    format=True
)  # returns '65.453.043/0001-78'

cnpj = generator.generate(
    prefix='45623767'
)  # returns '45623767000296'

cnpj = generator.generate(
    prefix='456237670002',
    format=True
)  # returns '45.623.767/0002-96'
```

The options can be provided to the constructor or the `generate()` method. If passed to the constructor, the options will be attached to the `CnpjGenerator` instance. When passed to the `generate()` method, it only applies the options to that specific call.

```python
generator = CnpjGenerator(format=True)

cnpj1 = generator.generate()  # '65.453.043/0001-78' (uses instance options)
cnpj2 = generator.generate(format=False)  # '65453043000178' (overrides instance options)
cnpj3 = generator.generate()  # '12.345.678/0001-95' (uses instance options again)
```

### Functional programming

The helper function `cnpj_gen()` is just a functional abstraction. Internally it creates an instance of `CnpjGenerator` and calls the `generate()` method right away.

```python
cnpj = cnpj_gen()  # returns '65453043000178'

cnpj = cnpj_gen(format=True)  # returns '65.453.043/0001-78'

cnpj = cnpj_gen(prefix='45623767')  # returns '45623767000296'

cnpj = cnpj_gen(prefix='456237670002', format=True)  # returns '45.623.767/0002-96'
```

### Generator Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `format` | `bool \| None` | `False` | Whether to format the output with dots, slash, and dash |
| `prefix` | `str \| None` | `''` | If you have CNPJ initials and want to complete it with valid digits. The string provided must contain between 0 and 12 digits. The branch ID (characters 8 to 11) cannot be "0000". |

## Contribution & Support

We welcome contributions! Please see our [Contributing Guidelines](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md) for details. But if you find this project helpful, please consider:

- ⭐ Starring the repository
- 🤝 Contributing to the codebase
- 💡 [Suggesting new features](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reporting bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE) file for details.

## Changelog

See [CHANGELOG](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cnpj-gen/CHANGELOG.md) for a list of changes and version history.

---

Made with ❤️ by [Lacus Solutions](https://github.com/LacusSolutions)
