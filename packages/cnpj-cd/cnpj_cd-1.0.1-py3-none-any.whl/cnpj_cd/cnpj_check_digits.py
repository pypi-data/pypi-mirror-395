import re

from .exceptions import (
    CnpjCheckDigitsCalculationError,
    CnpjInvalidLengthError,
    CnpjTypeError,
)

CNPJ_MIN_LENGTH = 12
CNPJ_MAX_LENGTH = 14


class CnpjCheckDigits:
    """Class to calculate CNPJ check digits."""

    __slots__ = ("_cnpj_digits", "_first_digit", "_second_digit")

    def __init__(self, cnpj_digits: str | list[str] | list[int]) -> None:
        original_input = cnpj_digits

        if not isinstance(cnpj_digits, (str, list)):
            raise CnpjTypeError(original_input)

        if isinstance(cnpj_digits, str):
            cnpj_digits = self._handle_string_input(cnpj_digits, original_input)
        elif isinstance(cnpj_digits, list):
            cnpj_digits = self._handle_list_input(cnpj_digits, original_input)

        self._validate_length(cnpj_digits, original_input)
        self._cnpj_digits = cnpj_digits[:CNPJ_MIN_LENGTH]
        self._first_digit: int | None = None
        self._second_digit: int | None = None

    @property
    def first_digit(self) -> int:
        """Calculates and returns the first check digit.As it's immutable, it caches the calculation result."""
        if self._first_digit is None:
            base_digits_sequence = self._cnpj_digits.copy()
            self._first_digit = self._calculate(base_digits_sequence)

        return self._first_digit

    @property
    def second_digit(self) -> int:
        """Calculates and returns the second check digit.As it's immutable, it caches the calculation result. And, as it depends on the first check digit, it's also calculated."""
        if self._second_digit is None:
            base_digits_sequence = [*self._cnpj_digits, self.first_digit]
            self._second_digit = self._calculate(base_digits_sequence)

        return self._second_digit

    def to_list(self) -> list[int]:
        """Returns the complete CNPJ as a list of 14 integers (12 base digits + 2 check digits)."""
        return [*self._cnpj_digits, self.first_digit, self.second_digit]

    def to_string(self) -> str:
        """Returns the complete CNPJ as a string of 14 digits (12 base digits + 2 check digits)."""
        return "".join(str(digit) for digit in self.to_list())

    def _handle_string_input(self, cnpj_digits: str, original_input: str) -> list[int]:
        """When CNPJ is provided as a string, it's validated and converted to a list of integers."""
        numeric_str = re.sub(r"[^0-9]", "", cnpj_digits)

        if not numeric_str:
            raise CnpjInvalidLengthError(
                original_input, CNPJ_MIN_LENGTH, CNPJ_MAX_LENGTH, 0
            )

        return [int(d) for d in numeric_str]

    def _handle_list_input(
        self, cnpj_digits: list[str] | list[int], original_input: list
    ) -> list[int]:
        """When CNPJ is provided as a list of strings or integers, it's validated and converted to a list of integers for further processing."""
        if all(isinstance(digit, str) for digit in cnpj_digits):
            return self._handle_string_list(cnpj_digits, original_input)

        if all(isinstance(digit, int) for digit in cnpj_digits):
            return self._flatten_digits(cnpj_digits)

        raise CnpjTypeError(original_input)

    def _handle_string_list(
        self, cnpj_digits: list[str], original_input: list
    ) -> list[int]:
        """When CNPJ is provided as a list of strings, it's validated and converted to a list of integers for further processing."""
        total_length = sum(len(digit_str) for digit_str in cnpj_digits if digit_str)

        if total_length < CNPJ_MIN_LENGTH or total_length > CNPJ_MAX_LENGTH:
            raise CnpjInvalidLengthError(
                original_input, CNPJ_MIN_LENGTH, CNPJ_MAX_LENGTH, total_length
            )

        flat_digits = []

        for digit_str in cnpj_digits:
            if not digit_str:
                continue

            try:
                digit_int = int(digit_str)
                flat_digits.extend(self._flatten_digits([digit_int]))
            except ValueError as e:
                raise CnpjTypeError(original_input) from e

        return flat_digits

    def _flatten_digits(self, digits: list[int]) -> list[int]:
        """Breaks down multiple digits within the array into individual digits. Negative numbers are converted to their absolute value."""
        flat_digits = []

        for digit in digits:
            abs_digit = abs(digit)
            flat_digits.extend([int(d) for d in str(abs_digit)])

        return flat_digits

    def _validate_length(
        self, cnpj_digits: list[int], original_input: str | list
    ) -> None:
        """Validates the length of the CNPJ digits."""
        length = len(cnpj_digits)

        if length < CNPJ_MIN_LENGTH or length > CNPJ_MAX_LENGTH:
            raise CnpjInvalidLengthError(
                original_input, CNPJ_MIN_LENGTH, CNPJ_MAX_LENGTH, length
            )

    def _calculate(self, cnpj_sequence: list[int]) -> int:
        """Calculates the CNPJ check digits using the official Brazilian algorithm. For the first check digit, it uses the digits 1 through 12 of the CNPJ base. For the second one, it uses the digits 1 through 13 (with the first check digit)."""
        min_length = CNPJ_MIN_LENGTH
        max_length = CNPJ_MAX_LENGTH - 1
        sequence_length = len(cnpj_sequence)

        if sequence_length < min_length or sequence_length > max_length:
            raise CnpjCheckDigitsCalculationError(cnpj_sequence)

        factor = 2
        sum_result = 0

        for num in reversed(cnpj_sequence):
            sum_result += num * factor
            factor = 2 if factor == 9 else factor + 1

        remainder = sum_result % 11

        return 0 if remainder < 2 else 11 - remainder
