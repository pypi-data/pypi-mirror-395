class CpfFormatterTypeError(TypeError):
    """Base error for all type validation for incoming arguments."""


class CpfFormatterInputTypeError(CpfFormatterTypeError):
    """Raised when the CPF value provided to the formatting function does not match the expected type."""

    def __init__(self, input_value, expected_types: list[type]) -> None:
        self.input_value = input_value
        self.expected_types = expected_types

        expected_types_str = ", ".join([t.__name__ for t in expected_types])

        super().__init__(
            f"CPF input must be of type {expected_types_str}. Got {type(input_value).__name__}."
        )


class CpfFormatterOptionTypeError(CpfFormatterTypeError):
    """Raised when a formatter option does not match the expected type."""

    def __init__(
        self, option_name: str, option_value, expected_types: list[type]
    ) -> None:
        self.option_name = option_name
        self.option_value = option_value
        self.expected_types = expected_types

        expected_types_str = ", ".join([t.__name__ for t in expected_types])

        super().__init__(
            f"Option '{option_name}' must be of type {expected_types_str}. "
            f"Got {type(option_value).__name__}."
        )


class CpfFormatterError(Exception):
    """Base exception for all cpf-fmt related errors."""


class CpfFormatterHiddenRangeError(CpfFormatterError):
    """Raised when a range value (hidden_start or hidden_end) is out of bounds."""

    def __init__(
        self, option_name: str, value: int, min_val: int, max_val: int
    ) -> None:
        self.option_name = option_name
        self.value = value
        self.min_val = min_val
        self.max_val = max_val

        super().__init__(
            f'Option "{option_name}" must be an integer between {min_val} and {max_val}. '
            f"Got {value}."
        )


class CpfFormatterInputLengthError(CpfFormatterError):
    """Raised when the formatting method input does not contain the expected number of digits."""

    def __init__(
        self,
        actual_input: str,
        evaluated_input: str,
        expected_length: int,
    ) -> None:
        self.actual_input = actual_input
        self.evaluated_input = evaluated_input
        self.expected_length = expected_length

        if actual_input == evaluated_input:
            fmt_evaluated_input = f"{len(evaluated_input)}"
        else:
            fmt_evaluated_input = f'{len(evaluated_input)} in "{evaluated_input}"'

        super().__init__(
            f'CPF input "{actual_input}" does not contain '
            f"{expected_length} digits. Got {fmt_evaluated_input}."
        )
