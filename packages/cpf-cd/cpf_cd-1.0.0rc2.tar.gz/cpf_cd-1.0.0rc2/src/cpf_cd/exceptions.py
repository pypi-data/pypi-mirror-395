class CpfCheckDigitsError(Exception):
    """Base exception for all cpf-cd related errors."""


class CpfCheckDigitsInputTypeError(CpfCheckDigitsError):
    """Raised when the class input does not match the expected type."""

    def __init__(self, actual_input) -> None:
        self.actual_input = actual_input

        super().__init__(
            f"CPF input must be of type str, list[str] or list[int]. Got {type(actual_input).__name__}."
        )


class CpfCheckDigitsInputLengthError(CpfCheckDigitsError):
    """Raised when the class input does not contain the expected number of digits."""

    def __init__(
        self,
        actual_input: str | list[str] | list[int],
        evaluated_input: str,
        min_expected_length: int,
        max_expected_length: int,
    ) -> None:
        self.actual_input = actual_input
        self.evaluated_input = evaluated_input
        self.min_expected_length = min_expected_length
        self.max_expected_length = max_expected_length

        if isinstance(actual_input, str):
            fmt_actual_input = f'"{actual_input}"'
        else:
            fmt_actual_input = f"{actual_input}"

        if actual_input == evaluated_input:
            fmt_evaluated_input = f"{len(evaluated_input)}"
        else:
            fmt_evaluated_input = f'{len(evaluated_input)} in "{evaluated_input}"'

        super().__init__(
            f"CPF input {fmt_actual_input} does not contain "
            f"{min_expected_length} to {max_expected_length} digits. "
            f"Got {fmt_evaluated_input}."
        )


class CpfCheckDigitsInputNotValidError(CpfCheckDigitsError):
    """Raised when the class input is not valid (e.g., repeated digits)."""

    def __init__(self, actual_input: str | list[str] | list[int], reason: str) -> None:
        self.actual_input = actual_input
        self.reason = reason

        if isinstance(actual_input, str):
            fmt_actual_input = f'"{actual_input}"'
        else:
            fmt_actual_input = f"{actual_input}"

        super().__init__(f"CPF input {fmt_actual_input} is invalid. {reason}")


class CpfCheckDigitsCalculationError(CpfCheckDigitsError):
    """Raised when the calculation of the CPF check digits fails."""

    def __init__(self, actual_input: list[int]) -> None:
        self.actual_input = actual_input

        super().__init__(
            f"Failed to calculate CPF check digits for the sequence: {actual_input}."
        )
