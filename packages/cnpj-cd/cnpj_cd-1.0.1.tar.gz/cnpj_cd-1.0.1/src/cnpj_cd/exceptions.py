class CnpjCheckDigitsError(Exception):
    """Base exception for all cnpj-cd related errors."""


class CnpjTypeError(CnpjCheckDigitsError):
    """Raised when a CNPJ digits is not a string or a list of strings or integers."""

    def __init__(self, cnpj) -> None:
        self.cnpj = cnpj

        super().__init__(
            f"CNPJ input must be of type str, list[str] or list[int]. Got {type(cnpj).__name__}."
        )


class CnpjInvalidLengthError(CnpjCheckDigitsError):
    """Raised when a CNPJ string does not contain the expected number of digits."""

    def __init__(
        self,
        cnpj: str | list[str] | list[int],
        min_expected_length: int,
        max_expected_length: int,
        actual_length: int,
    ) -> None:
        self.cnpj = cnpj
        self.min_expected_length = min_expected_length
        self.max_expected_length = max_expected_length
        self.actual_length = actual_length

        super().__init__(
            f'Parameter "{cnpj}" does not contain {min_expected_length} to {max_expected_length} digits. '
            f"Got {actual_length}."
        )


class CnpjCheckDigitsCalculationError(CnpjCheckDigitsError):
    """Raised when the calculation of the CNPJ check digits fails."""

    def __init__(self, cnpj_digits: list[int]) -> None:
        self.cnpj_digits = cnpj_digits

        super().__init__(
            f"Failed to calculate the CNPJ check digits for the sequence: {cnpj_digits}."
        )
