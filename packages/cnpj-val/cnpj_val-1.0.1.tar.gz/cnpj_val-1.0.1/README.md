![cnpj-val for Python](https://br-utils.vercel.app/img/cover_cnpj-val.jpg)

[![PyPI Version](https://img.shields.io/pypi/v/cnpj-val)](https://pypi.org/project/cnpj-val)
[![PyPI Downloads](https://img.shields.io/pypi/dm/cnpj-val)](https://pypi.org/project/cnpj-val)
[![Python Version](https://img.shields.io/pypi/pyversions/cnpj-val)](https://www.python.org/)
[![Test Status](https://img.shields.io/github/actions/workflow/status/LacusSolutions/br-utils-py/ci.yml?label=ci/cd)](https://github.com/LacusSolutions/br-utils-py/actions)
[![Last Update Date](https://img.shields.io/github/last-commit/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py)
[![Project License](https://img.shields.io/github/license/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE)

Utility function/class to validate CNPJ (Brazilian employer ID).

## Python Support

| ![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) | ![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) | ![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | ![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white) | ![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white) |
|--- | --- | --- | --- | --- |
| Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ |

## Installation

```bash
$ pip install cnpj-val
```

## Import

```python
# Using class-based resource
from cnpj_val import CnpjValidator

# Or using function-based one
from cnpj_val import cnpj_val
```

## Usage

### Object-Oriented Usage

```python
validator = CnpjValidator()
cnpj = '98765432000198'

print('Valid' if validator.is_valid(cnpj) else 'Invalid')  # returns 'Valid'

cnpj = '98.765.432/0001-98'
print('Valid' if validator.is_valid(cnpj) else 'Invalid')  # returns 'Valid'

cnpj = '98765432000199'
print('Valid' if validator.is_valid(cnpj) else 'Invalid')  # returns 'Invalid'
```

### Functional programming

The helper function `cnpj_val()` is just a functional abstraction. Internally it creates an instance of `CnpjValidator` and calls the `is_valid()` method right away.

```python
cnpj = '98765432000198'

print('Valid' if cnpj_val(cnpj) else 'Invalid')      # returns 'Valid'

print('Valid' if cnpj_val('98.765.432/0001-98') else 'Invalid')  # returns 'Valid'

print('Valid' if cnpj_val('98765432000199') else 'Invalid')      # returns 'Invalid'
```

### Validation Examples

```python
# Valid CNPJ numbers
cnpj_val('98765432000198')      # returns True
cnpj_val('98.765.432/0001-98')  # returns True
cnpj_val('03603568000195')      # returns True

# Invalid CNPJ numbers
cnpj_val('98765432000199')      # returns False
cnpj_val('12345678901234')      # returns False
cnpj_val('00000000000000')      # returns False
cnpj_val('11111111111111')      # returns False
cnpj_val('123')                 # returns False (too short)
cnpj_val('')                    # returns False (empty)
```

## Features

- ✅ **Format Agnostic**: Accepts CNPJ with or without formatting (dots, slashes, dashes)
- ✅ **Strict Validation**: Validates both check digits according to Brazilian CNPJ algorithm
- ✅ **Type Safety**: Built with Python 3.10+ type hints
- ✅ **Lightweight**: Minimal dependencies, only requires `cnpj-gen` for check digit calculation
- ✅ **Dual API**: Both object-oriented and functional programming styles supported

## API Reference

### CnpjValidator Class

#### `is_valid(cnpj_string: str) -> bool`

Validates a CNPJ string and returns `True` if valid, `False` otherwise.

**Parameters:**
- `cnpj_string` (str): The CNPJ to validate (with or without formatting)

**Returns:**
- `bool`: `True` if the CNPJ is valid, `False` otherwise

### cnpj_val() Function

#### `cnpj_val(cnpj_string: str) -> bool`

Functional wrapper around `CnpjValidator.is_valid()`.

**Parameters:**
- `cnpj_string` (str): The CNPJ to validate (with or without formatting)

**Returns:**
- `bool`: `True` if the CNPJ is valid, `False` otherwise

## Validation Algorithm

The package validates CNPJ using the official Brazilian algorithm:

1. **Length Check**: Ensures the CNPJ has exactly 14 digits
2. **First Check Digit**: Calculates and validates the 13th digit
3. **Second Check Digit**: Calculates and validates the 14th digit
4. **Format Tolerance**: Automatically strips non-numeric characters before validation

## Error Handling

The validator is designed to be forgiving with input format but strict with validation:

- Invalid formats (too short, too long) return `False`
- Invalid check digits return `False`
- Empty strings return `False`
- Non-numeric strings (after stripping formatting) return `False`

## Dependencies

- **Python**: >= 3.10
- **cnpj-gen**: >= 1.0.0 (for check digit calculation)

## Contribution & Support

We welcome contributions! Please see our [Contributing Guidelines](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md) for details. But if you find this project helpful, please consider:

- ⭐ Starring the repository
- 🤝 Contributing to the codebase
- 💡 [Suggesting new features](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reporting bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE) file for details.

## Changelog

See [CHANGELOG](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cnpj-val/CHANGELOG.md) for a list of changes and version history.

---

Made with ❤️ by [Lacus Solutions](https://github.com/LacusSolutions)
