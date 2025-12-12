![cnpj-cd for Python](https://br-utils.vercel.app/img/cover_cnpj-cd.jpg)

[![PyPI Version](https://img.shields.io/pypi/v/cnpj-cd)](https://pypi.org/project/cnpj-cd)
[![PyPI Downloads](https://img.shields.io/pypi/dm/cnpj-cd)](https://pypi.org/project/cnpj-cd)
[![Python Version](https://img.shields.io/pypi/pyversions/cnpj-cd)](https://www.python.org/)
[![Test Status](https://img.shields.io/github/actions/workflow/status/LacusSolutions/br-utils-py/ci.yml?label=ci/cd)](https://github.com/LacusSolutions/br-utils-py/actions)
[![Last Update Date](https://img.shields.io/github/last-commit/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py)
[![Project License](https://img.shields.io/github/license/LacusSolutions/br-utils-py)](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE)

Utility class to calculate check digits on CNPJ (Brazilian employer ID).

## Python Support

| ![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) | ![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white) | ![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | ![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white) | ![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white) |
|--- | --- | --- | --- | --- |
| Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ | Passing ✔ |

## Installation

```bash
$ pip install cnpj-cd
```

## Import

```python
from cnpj_cd import CnpjCheckDigits
```

## Usage

### Basic Usage

```python
# Calculate check digits from a 12-digit CNPJ base
check_digits = CnpjCheckDigits("914157320007")

print(check_digits.first_digit)    # returns 9
print(check_digits.second_digit)   # returns 3
print(check_digits.to_string())    # returns '91415732000793'
print(check_digits.to_list())      # returns [9, 1, 4, 1, 5, 7, 3, 2, 0, 0, 0, 7, 9, 3]
```

### Input Formats

The `CnpjCheckDigits` class accepts multiple input formats:

#### String Input

```python
# Plain string (non-numeric characters are automatically stripped)
check_digits = CnpjCheckDigits("914157320007")
check_digits = CnpjCheckDigits("91.415.732/0007")  # formatting is ignored
check_digits = CnpjCheckDigits("914157320007")      # 12 digits
check_digits = CnpjCheckDigits("91415732000793")    # 14 digits (only first 12 are used)
```

#### List of Strings

```python
# List of single-character strings
check_digits = CnpjCheckDigits(["9", "1", "4", "1", "5", "7", "3", "2", "0", "0", "0", "7"])

# List with multi-digit strings (automatically flattened)
check_digits = CnpjCheckDigits(["914157320007"])     # flattens to individual digits
check_digits = CnpjCheckDigits(["91", "415", "732", "0007"])  # also flattens
```

#### List of Integers

```python
# List of single-digit integers
check_digits = CnpjCheckDigits([9, 1, 4, 1, 5, 7, 3, 2, 0, 0, 0, 7])

# List with multi-digit integers (automatically flattened)
check_digits = CnpjCheckDigits([914157320007])       # flattens to individual digits
check_digits = CnpjCheckDigits([914, 157, 320, 7])  # also flattens
```

### Properties

#### `first_digit: int`

Returns the first check digit (13th digit of the CNPJ).

```python
check_digits = CnpjCheckDigits("914157320007")
print(check_digits.first_digit)  # returns 9
```

#### `second_digit: int`

Returns the second check digit (14th digit of the CNPJ).

```python
check_digits = CnpjCheckDigits("914157320007")
print(check_digits.second_digit)  # returns 3
```

### Methods

#### `to_list() -> list[int]`

Returns the complete CNPJ as a list of integers (12 base digits + 2 check digits).

```python
check_digits = CnpjCheckDigits("914157320007")
print(check_digits.to_list())  # returns [9, 1, 4, 1, 5, 7, 3, 2, 0, 0, 0, 7, 9, 3]
```

#### `to_string() -> str`

Returns the complete CNPJ as a string (12 base digits + 2 check digits).

```python
check_digits = CnpjCheckDigits("914157320007")
print(check_digits.to_string())  # returns '91415732000793'
```

### Examples

```python
from cnpj_cd import CnpjCheckDigits

# Calculate check digits for a CNPJ base
base = "914157320007"
check_digits = CnpjCheckDigits(base)

# Get individual check digits
first = check_digits.first_digit    # 9
second = check_digits.second_digit   # 3

# Get complete CNPJ
complete = check_digits.to_string()  # '91415732000793'

# Work with formatted input
formatted = CnpjCheckDigits("91.415.732/0007")
print(formatted.to_string())  # '91415732000793'

# Work with list input
list_input = CnpjCheckDigits([9, 1, 4, 1, 5, 7, 3, 2, 0, 0, 0, 7])
print(list_input.to_string())  # '91415732000793'
```

## Error Handling

The package raises specific exceptions for different error scenarios:

### `CnpjTypeError`

Raised when the input type is not supported (must be `str`, `list[str]`, or `list[int]`).

```python
from cnpj_cd import CnpjCheckDigits, CnpjTypeError

try:
    CnpjCheckDigits(12345678901234)  # int not allowed
except CnpjTypeError as e:
    print(e)  # CNPJ input must be of type str, list[str] or list[int]. Got "int".
```

### `CnpjInvalidLengthError`

Raised when the input does not contain 12 to 14 digits.

```python
from cnpj_cd import CnpjCheckDigits, CnpjInvalidLengthError

try:
    CnpjCheckDigits("12345678901")  # only 11 digits
except CnpjInvalidLengthError as e:
    print(e)  # Parameter "12345678901" does not contain 12 to 14 digits. Got 11.
```

### `CnpjCheckDigitsCalculationError`

Raised when the check digit calculation fails due to invalid sequence length.

```python
from cnpj_cd import CnpjCheckDigits, CnpjCheckDigitsCalculationError

# This is an internal error that should not occur in normal usage
# It happens when the sequence passed to _calculate() has invalid length
```

## Features

- ✅ **Multiple Input Formats**: Accepts strings, lists of strings, or lists of integers
- ✅ **Format Agnostic**: Automatically strips non-numeric characters from string input
- ✅ **Auto-Expansion**: Automatically expands multi-digit numbers in lists to individual digits
- ✅ **Lazy Evaluation**: Check digits are calculated only when accessed (via properties)
- ✅ **Type Safety**: Built with Python 3.10+ type hints
- ✅ **Zero Dependencies**: No external dependencies required
- ✅ **Comprehensive Error Handling**: Specific exceptions for different error scenarios

## API Reference

### CnpjCheckDigits Class

#### Constructor

```python
CnpjCheckDigits(cnpj_digits: str | list[str] | list[int]) -> CnpjCheckDigits
```

Creates a new `CnpjCheckDigits` instance from the provided CNPJ base digits.

**Parameters:**
- `cnpj_digits` (str | list[str] | list[int]): The CNPJ base digits (12-14 digits). Can be:
  - A string with 12-14 digits (formatting characters are ignored)
  - A list of strings (each string can be a single digit or multi-digit number)
  - A list of integers (each integer can be a single digit or multi-digit number)

**Raises:**
- `CnpjTypeError`: If the input type is not supported
- `CnpjInvalidLengthError`: If the input does not contain 12-14 digits

**Returns:**
- `CnpjCheckDigits`: A new instance ready to calculate check digits

#### Properties

##### `first_digit: int`

The first check digit (13th digit of the CNPJ). Calculated lazily on first access.

##### `second_digit: int`

The second check digit (14th digit of the CNPJ). Calculated lazily on first access.

#### Methods

##### `to_list() -> list[int]`

Returns the complete CNPJ as a list of 14 integers (12 base digits + 2 check digits).

##### `to_string() -> str`

Returns the complete CNPJ as a string of 14 digits (12 base digits + 2 check digits).

## Calculation Algorithm

The package calculates CNPJ check digits using the official Brazilian algorithm:

1. **First Check Digit (13th position)**:
   - Uses digits 1-12 of the CNPJ base
   - Applies weights: 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2 (from right to left)
   - Calculates: `sum(digit × weight) % 11`
   - Result: `0` if remainder < 2, otherwise `11 - remainder`

2. **Second Check Digit (14th position)**:
   - Uses digits 1-12 + first check digit
   - Applies weights: 6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2 (from right to left)
   - Calculates: `sum(digit × weight) % 11`
   - Result: `0` if remainder < 2, otherwise `11 - remainder`

## Dependencies

- **Python**: >= 3.10

No external dependencies required.

## Contribution & Support

We welcome contributions! Please see our [Contributing Guidelines](https://github.com/LacusSolutions/br-utils-py/blob/main/CONTRIBUTING.md) for details. But if you find this project helpful, please consider:

- ⭐ Starring the repository
- 🤝 Contributing to the codebase
- 💡 [Suggesting new features](https://github.com/LacusSolutions/br-utils-py/issues)
- 🐛 [Reporting bugs](https://github.com/LacusSolutions/br-utils-py/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/LacusSolutions/br-utils-py/blob/main/LICENSE) file for details.

## Changelog

See [CHANGELOG](https://github.com/LacusSolutions/br-utils-py/blob/main/packages/cnpj-cd/CHANGELOG.md) for a list of changes and version history.

---

Made with ❤️ by [Lacus Solutions](https://github.com/LacusSolutions)
