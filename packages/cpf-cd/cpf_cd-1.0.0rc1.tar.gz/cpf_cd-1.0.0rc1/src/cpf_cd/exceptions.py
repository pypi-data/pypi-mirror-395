class CpfCheckDigitsError(Exception):
    """Base exception for all cpf-cd related errors."""


class CpfTypeError(CpfCheckDigitsError):
    """Raised when a CPF digits is not a string or a list of strings or integers."""

    def __init__(self, cpf) -> None:
        self.cpf = cpf

        super().__init__(
            f"CPF input must be of type str, list[str] or list[int]. Got {type(cpf).__name__}."
        )


class CpfInvalidLengthError(CpfCheckDigitsError):
    """Raised when a CPF string does not contain the expected number of digits."""

    def __init__(
        self,
        cpf: str | list[str] | list[int],
        min_expected_length: int,
        max_expected_length: int,
        actual_length: int,
    ) -> None:
        self.cpf = cpf
        self.min_expected_length = min_expected_length
        self.max_expected_length = max_expected_length
        self.actual_length = actual_length

        super().__init__(
            f'Parameter "{cpf}" does not contain {min_expected_length} to {max_expected_length} digits. '
            f"Got {actual_length}."
        )


class CpfCheckDigitsCalculationError(CpfCheckDigitsError):
    """Raised when the calculation of the CPF check digits fails."""

    def __init__(self, cpf_digits: list[int]) -> None:
        self.cpf_digits = cpf_digits

        super().__init__(
            f"Failed to calculate the CPF check digits for the sequence: {cpf_digits}."
        )
