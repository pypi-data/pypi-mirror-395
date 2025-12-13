from collections.abc import Callable

from .cpf_formatter import CpfFormatter


def cpf_fmt(
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
    """Formats a CPF string according to the given options. Default options returns the traditional CPF format (`91.415.732/0007-93`)."""
    formatter = CpfFormatter(
        hidden,
        hidden_key,
        hidden_start,
        hidden_end,
        dot_key,
        dash_key,
        escape,
        on_fail,
    )

    return formatter.format(cpf_string)
