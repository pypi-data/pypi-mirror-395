import re

from .exceptions import (
    CpfCheckDigitsCalculationError,
    CpfInvalidLengthError,
    CpfTypeError,
)

CPF_MIN_LENGTH = 9
CPF_MAX_LENGTH = 11


class CpfCheckDigits:
    """Class to calculate CPF check digits."""

    __slots__ = ("_cpf_digits", "_first_digit", "_second_digit")

    def __init__(self, cpf_digits: str | list[str] | list[int]) -> None:
        original_input = cpf_digits

        if not isinstance(cpf_digits, (str, list)):
            raise CpfTypeError(original_input)

        if isinstance(cpf_digits, str):
            cpf_digits = self._handle_string_input(cpf_digits, original_input)
        elif isinstance(cpf_digits, list):
            cpf_digits = self._handle_list_input(cpf_digits, original_input)

        self._validate_length(cpf_digits, original_input)
        self._cpf_digits = cpf_digits[:CPF_MIN_LENGTH]
        self._first_digit: int | None = None
        self._second_digit: int | None = None

    @property
    def first_digit(self) -> int:
        """Calculates and returns the first check digit.As it's immutable, it caches the calculation result."""
        if self._first_digit is None:
            base_digits_sequence = self._cpf_digits.copy()
            self._first_digit = self._calculate(base_digits_sequence)

        return self._first_digit

    @property
    def second_digit(self) -> int:
        """Calculates and returns the second check digit.As it's immutable, it caches the calculation result. And, as it depends on the first check digit, it's also calculated."""
        if self._second_digit is None:
            base_digits_sequence = [*self._cpf_digits, self.first_digit]
            self._second_digit = self._calculate(base_digits_sequence)

        return self._second_digit

    def to_list(self) -> list[int]:
        """Returns the complete CPF as a list of 11 integers (9 base digits + 2 check digits)."""
        return [*self._cpf_digits, self.first_digit, self.second_digit]

    def to_string(self) -> str:
        """Returns the complete CPF as a string of 11 digits (9 base digits + 2 check digits)."""
        return "".join(str(digit) for digit in self.to_list())

    def _handle_string_input(self, cpf_digits: str, original_input: str) -> list[int]:
        """When CPF is provided as a string, it's validated and converted to a list of integers."""
        numeric_str = re.sub(r"[^0-9]", "", cpf_digits)

        if not numeric_str:
            raise CpfInvalidLengthError(
                original_input, CPF_MIN_LENGTH, CPF_MAX_LENGTH, 0
            )

        return [int(d) for d in numeric_str]

    def _handle_list_input(
        self, cpf_digits: list[str] | list[int], original_input: list
    ) -> list[int]:
        """When CPF is provided as a list of strings or integers, it's validated and converted to a list of integers for further processing."""
        if all(isinstance(digit, str) for digit in cpf_digits):
            return self._handle_string_list(cpf_digits, original_input)

        if all(isinstance(digit, int) for digit in cpf_digits):
            return self._flatten_digits(cpf_digits)

        raise CpfTypeError(original_input)

    def _handle_string_list(
        self, cpf_digits: list[str], original_input: list
    ) -> list[int]:
        """When CPF is provided as a list of strings, it's validated and converted to a list of integers for further processing."""
        total_length = sum(len(digit_str) for digit_str in cpf_digits if digit_str)

        if total_length < CPF_MIN_LENGTH or total_length > CPF_MAX_LENGTH:
            raise CpfInvalidLengthError(
                original_input, CPF_MIN_LENGTH, CPF_MAX_LENGTH, total_length
            )

        flat_digits = []

        for digit_str in cpf_digits:
            if not digit_str:
                continue

            try:
                digit_int = int(digit_str)
                flat_digits.extend(self._flatten_digits([digit_int]))
            except ValueError as e:
                raise CpfTypeError(original_input) from e

        return flat_digits

    def _flatten_digits(self, digits: list[int]) -> list[int]:
        """Breaks down multiple digits within the array into individual digits. Negative numbers are converted to their absolute value."""
        flat_digits = []

        for digit in digits:
            abs_digit = abs(digit)
            flat_digits.extend([int(d) for d in str(abs_digit)])

        return flat_digits

    def _validate_length(
        self, cpf_digits: list[int], original_input: str | list
    ) -> None:
        """Validates the length of the CPF digits."""
        length = len(cpf_digits)

        if length < CPF_MIN_LENGTH or length > CPF_MAX_LENGTH:
            raise CpfInvalidLengthError(
                original_input, CPF_MIN_LENGTH, CPF_MAX_LENGTH, length
            )

    def _calculate(self, cpf_sequence: list[int]) -> int:
        """Calculates the CPF check digits using the official Brazilian algorithm. For the first check digit, it uses the digits 1 through 9 of the CPF base. For the second one, it uses the digits 1 through 10 (with the first check digit)."""
        min_length = CPF_MIN_LENGTH
        max_length = CPF_MAX_LENGTH - 1
        sequence_length = len(cpf_sequence)

        if sequence_length < min_length or sequence_length > max_length:
            raise CpfCheckDigitsCalculationError(cpf_sequence)

        factor = sequence_length + 1
        sum_result = 0

        for num in cpf_sequence:
            sum_result += num * factor
            factor -= 1

        remainder = 11 - (sum_result % 11)

        return 0 if remainder > 9 else remainder
