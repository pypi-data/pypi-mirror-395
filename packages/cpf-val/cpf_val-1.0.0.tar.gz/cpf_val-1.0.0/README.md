![cpf-val for Python](https://br-utils.vercel.app/img/cover_cpf-val.jpg)

[![PyPI Version](https://img.shields.io/pypi/v/cpf-val)](https://pypi.org/project/cpf-val)
[![PyPI Downloads](https://img.shields.io/pypi/dm/cpf-val)](https://pypi.org/project/cpf-val)
[![Python Version](https://img.shields.io/pypi/pyversions/cpf-val)](https://www.python.org/)
[![Test Status](https://img.shields.io/github/actions/workflow/status/LacusSolutions/br-utils-py/ci.yml?label=ci/cd)](https://github.com/LacusSolutions/br-utils-py/actions)
[![Last Update Date](https://img.shields.io/github/last-commit/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py)
[![Project License](https://img.shields.io/github/license/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE)

Utility function/class to validate CPF (Brazilian personal ID).

CPF validation follows the official rules established by Receita Federal:
- The CPF must contain exactly 11 digits.
- All digits cannot be identical (e.g., `111.111.111-11` is considered invalid).
- The last two digits (10th and 11th) are check digits, calculated from the preceding nine digits.

## Python Support

| ![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) | ![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) | ![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | ![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white) | ![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white) |
|--- | --- | --- | --- | --- |
| Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ |

## Installation

```bash
$ pip install cpf-val
```

## Import

```python
# Using class-based resource
from cpf_val import CpfValidator

# Or using function-based one
from cpf_val import cpf_val
```

## Usage

### Object-Oriented Usage

```python
validator = CpfValidator()
cpf = '11144477735'

print('Valid' if validator.is_valid(cpf) else 'Invalid')  # returns 'Valid'

cpf = '111.444.777-35'
print('Valid' if validator.is_valid(cpf) else 'Invalid')  # returns 'Valid'

cpf = '11144477736'
print('Valid' if validator.is_valid(cpf) else 'Invalid')  # returns 'Invalid'
```

### Functional programming

The helper function `cpf_val()` is just a functional abstraction. Internally it creates an instance of `CpfValidator` and calls the `is_valid()` method right away.

```python
cpf = '11144477735'

print('Valid' if cpf_val(cpf) else 'Invalid')      # returns 'Valid'

print('Valid' if cpf_val('111.444.777-35') else 'Invalid')  # returns 'Valid'

print('Valid' if cpf_val('11144477736') else 'Invalid')      # returns 'Invalid'
```

### Validation Examples

```python
# Valid CPF numbers
cpf_val('11144477735')      # returns True
cpf_val('111.444.777-35')   # returns True
cpf_val('12345678909')      # returns True

# Invalid CPF numbers
cpf_val('11144477736')      # returns False
cpf_val('12345678901')      # returns False
cpf_val('00000000000')      # returns False
cpf_val('11111111111')      # returns False
cpf_val('123')              # returns False (too short)
cpf_val('')                 # returns False (empty)
```

## Features

- ✅ **Format Agnostic**: Accepts CPF with or without formatting (dots, dashes)
- ✅ **Strict Validation**: Validates both check digits according to Brazilian CPF algorithm
- ✅ **Type Safety**: Built with Python 3.10+ type hints
- ✅ **Lightweight**: Minimal dependencies, only requires `cpf-cd` for check digit calculation
- ✅ **Dual API**: Both object-oriented and functional programming styles supported

## API Reference

### CpfValidator Class

#### `is_valid(cpf_string: str) -> bool`

Validates a CPF string and returns `True` if valid, `False` otherwise.

**Parameters:**
- `cpf_string` (str): The CPF to validate (with or without formatting)

**Returns:**
- `bool`: `True` if the CPF is valid, `False` otherwise

### cpf_val() Function

#### `cpf_val(cpf_string: str) -> bool`

Functional wrapper around `CpfValidator.is_valid()`.

**Parameters:**
- `cpf_string` (str): The CPF to validate (with or without formatting)

**Returns:**
- `bool`: `True` if the CPF is valid, `False` otherwise

## Validation Algorithm

The package validates CPF using the official Brazilian algorithm:

1. **Length Check**: Ensures the CPF has exactly 11 digits
2. **Repeated Digits Check**: Rejects CPFs with all digits being the same (e.g., 11111111111, 00000000000)
3. **First Check Digit**: Calculates and validates the 10th digit
4. **Second Check Digit**: Calculates and validates the 11th digit
5. **Format Tolerance**: Automatically strips non-numeric characters before validation

## Error Handling

The validator is designed to be forgiving with input format but strict with validation:

- Invalid formats (too short, too long) return `False`
- Invalid check digits return `False`
- Empty strings return `False`
- Non-numeric strings (after stripping formatting) return `False`
- CPFs with all digits the same return `False`

## Dependencies

- **Python**: >= 3.10
- **cpf-cd**: for check digit calculation

## Contribution & Support

We welcome contributions! Please see our [Contributing Guidelines](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md) for details. But if you find this project helpful, please consider:

- ⭐ Starring the repository
- 🤝 Contributing to the codebase
- 💡 [Suggesting new features](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reporting bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE) file for details.

## Changelog

See [CHANGELOG](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cpf-val/CHANGELOG.md) for a list of changes and version history.

---

Made with ❤️ by [Lacus Solutions](https://github.com/LacusSolutions)
