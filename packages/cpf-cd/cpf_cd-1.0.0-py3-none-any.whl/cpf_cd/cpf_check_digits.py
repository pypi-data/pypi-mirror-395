import re

from .exceptions import (
    CpfCheckDigitsCalculationError,
    CpfCheckDigitsInputLengthError,
    CpfCheckDigitsInputNotValidError,
    CpfCheckDigitsInputTypeError,
)

CPF_MIN_LENGTH = 9
CPF_MAX_LENGTH = 11


class CpfCheckDigits:
    """Class to calculate CPF check digits."""

    __slots__ = ("_cpf_digits", "_first_digit", "_second_digit")

    def __init__(self, cpf_input: str | list[str] | list[int]) -> None:
        original_input = cpf_input

        if not isinstance(cpf_input, (str, list)):
            raise CpfCheckDigitsInputTypeError(original_input)

        if isinstance(cpf_input, str):
            cpf_input = self._handle_string_input(cpf_input)
        else:
            cpf_input = self._handle_list_input(cpf_input, original_input)

        self._validate_length(cpf_input, original_input)
        self._validate_non_repeated_digits(cpf_input, original_input)

        self._cpf_digits = cpf_input[:CPF_MIN_LENGTH]
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

    def _handle_string_input(self, cpf_string: str) -> list[int]:
        """When CPF is provided as a string, it is sanitized, validated and converted to a list of integers."""
        digits_only_string = re.sub(r"[^0-9]", "", cpf_string)

        return [int(digit_string) for digit_string in digits_only_string]

    def _handle_list_input(
        self,
        cpf_list: list[str] | list[int],
        original_input: list,
    ) -> list[int]:
        """When CPF is provided as a list of strings or integers, it is sanitized, validated and converted to a list of integers for further processing."""
        if all(isinstance(digit, str) for digit in cpf_list):
            return self._handle_string_list_input(cpf_list)

        if all(isinstance(digit, int) for digit in cpf_list):
            return self._flatten_digits(cpf_list)

        raise CpfCheckDigitsInputTypeError(original_input)

    def _handle_string_list_input(self, cpf_string_list: list[str]) -> list[int]:
        """When CPF is provided as a list of strings, it is sanitized, validated and converted to a list of integers for further processing."""
        final_cpf_int_list = []

        for list_item in cpf_string_list:
            cpf_int_list = self._handle_string_input(list_item)
            final_cpf_int_list.extend(cpf_int_list)

        return final_cpf_int_list

    def _flatten_digits(self, int_list: list[int]) -> list[int]:
        """Breaks down multiple digits within the array into individual ones. Negative numbers are converted to their absolute value."""
        final_cpf_int_list = []

        for number in int_list:
            abs_number = abs(number)
            final_cpf_int_list.extend(
                [int(digit_string) for digit_string in str(abs_number)]
            )

        return final_cpf_int_list

    def _validate_length(
        self,
        cpf_int_list: list[int],
        original_input: str | list[str] | list[int],
    ) -> None:
        """Validates the length of the CPF digits."""
        digits_count = len(cpf_int_list)

        if digits_count < CPF_MIN_LENGTH or digits_count > CPF_MAX_LENGTH:
            raise CpfCheckDigitsInputLengthError(
                original_input,
                "".join(str(digit) for digit in cpf_int_list),
                CPF_MIN_LENGTH,
                CPF_MAX_LENGTH,
            )

    def _validate_non_repeated_digits(
        self,
        cpf_int_list: list[int],
        original_input: str | list[str] | list[int],
    ) -> None:
        """Validates that the CPF digits are not all the same."""
        eligible_cpf_int_list = cpf_int_list[:CPF_MIN_LENGTH]
        digits_set = set(eligible_cpf_int_list)

        if len(digits_set) == 1:
            raise CpfCheckDigitsInputNotValidError(
                original_input,
                "Repeated digits are not considered valid.",
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
