import html
from collections.abc import Callable

from .cpf_formatter_options import CPF_LENGTH, CpfFormatterOptions
from .exceptions import CpfFormatterInputLengthError


class CpfFormatter:
    """Class to format a CPF string according to the given options."""

    __slots__ = ("_options",)

    def __init__(
        self,
        hidden: bool | None = None,
        hidden_key: str | None = None,
        hidden_start: int | None = None,
        hidden_end: int | None = None,
        dot_key: str | None = None,
        dash_key: str | None = None,
        escape: bool | None = None,
        on_fail: Callable | None = None,
    ) -> None:
        self._options = CpfFormatterOptions(
            hidden,
            hidden_key,
            hidden_start,
            hidden_end,
            dot_key,
            dash_key,
            escape,
            on_fail,
        )

    def format(
        self,
        cpf_string: str,
        hidden: bool | None = None,
        hidden_key: str | None = None,
        hidden_start: int | None = None,
        hidden_end: int | None = None,
        dot_key: str | None = None,
        dash_key: str | None = None,
        escape: bool | None = None,
        on_fail: Callable | None = None,
    ) -> str:
        """Executes the CPF string formatting, overriding any given options with the ones set on the formatter instance."""
        actual_options = self._options.merge(
            hidden,
            hidden_key,
            hidden_start,
            hidden_end,
            dot_key,
            dash_key,
            escape,
            on_fail,
        )

        cpf_numbers_string = "".join(filter(str.isdigit, cpf_string))

        if len(cpf_numbers_string) != CPF_LENGTH:
            on_fail_callback = actual_options.on_fail

            try:
                error = CpfFormatterInputLengthError(
                    actual_input=cpf_string,
                    evaluated_input=cpf_numbers_string,
                    expected_length=CPF_LENGTH,
                )

                return on_fail_callback(cpf_string, error)
            except TypeError:
                return on_fail_callback(cpf_string)

        if actual_options.hidden:
            hidden_start = actual_options.hidden_start
            hidden_end = actual_options.hidden_end
            hidden_key = actual_options.hidden_key

            prefix = cpf_numbers_string[:hidden_start]
            hidden_part_length = hidden_end - hidden_start + 1
            masked = hidden_key * hidden_part_length
            suffix = cpf_numbers_string[hidden_end + 1 :]
            cpf_numbers_string = prefix + masked + suffix

        pretty_cpf = (
            cpf_numbers_string[0:3]
            + actual_options.dot_key
            + cpf_numbers_string[3:6]
            + actual_options.dot_key
            + cpf_numbers_string[6:9]
            + actual_options.dash_key
            + cpf_numbers_string[9:11]
        )

        if actual_options.escape:
            return html.escape(pretty_cpf, quote=True)

        return pretty_cpf

    @property
    def options(self) -> CpfFormatterOptions:
        """Direct access to the options manager for the CPF formatter."""
        return self._options
