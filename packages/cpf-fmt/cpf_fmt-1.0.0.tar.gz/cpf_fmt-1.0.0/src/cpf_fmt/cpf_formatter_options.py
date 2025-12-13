from collections.abc import Callable
from dataclasses import dataclass, replace

from .exceptions import CpfFormatterHiddenRangeError

CPF_LENGTH = 11
MIN_HIDDEN_RANGE = 0
MAX_HIDDEN_RANGE = CPF_LENGTH - 1

DEFAULT_HIDDEN = False
DEFAULT_HIDDEN_KEY = "*"
DEFAULT_HIDDEN_START = 3
DEFAULT_HIDDEN_END = 10
DEFAULT_DOT_KEY = "."
DEFAULT_DASH_KEY = "-"
DEFAULT_ESCAPE = False


def DEFAULT_ON_FAIL(value: str, _error: Exception | None = None) -> str:
    """Default callback for invalid CPF input."""
    return value


@dataclass(slots=True, frozen=False)
class CpfFormatterOptions:
    """Class to manage and store the options for the CPF formatter."""

    hidden: bool | None = None
    hidden_key: str | None = None
    hidden_start: int | None = None
    hidden_end: int | None = None
    dot_key: str | None = None
    dash_key: str | None = None
    escape: bool | None = None
    on_fail: Callable | None = None

    def __post_init__(self) -> None:
        if self.hidden is None:
            object.__setattr__(self, "hidden", DEFAULT_HIDDEN)
        if self.hidden_key is None:
            object.__setattr__(self, "hidden_key", DEFAULT_HIDDEN_KEY)
        if self.hidden_start is None:
            object.__setattr__(self, "hidden_start", DEFAULT_HIDDEN_START)
        if self.hidden_end is None:
            object.__setattr__(self, "hidden_end", DEFAULT_HIDDEN_END)
        if self.dot_key is None:
            object.__setattr__(self, "dot_key", DEFAULT_DOT_KEY)
        if self.dash_key is None:
            object.__setattr__(self, "dash_key", DEFAULT_DASH_KEY)
        if self.escape is None:
            object.__setattr__(self, "escape", DEFAULT_ESCAPE)
        if self.on_fail is None:
            object.__setattr__(self, "on_fail", DEFAULT_ON_FAIL)

        self.set_hidden_range(self.hidden_start, self.hidden_end)

        if not callable(self.on_fail):
            raise TypeError(
                f'"on_fail" argument must be a callable, {type(self.on_fail).__name__} given'
            )

    def merge(
        self,
        hidden: bool | None = None,
        hidden_key: str | None = None,
        hidden_start: int | None = None,
        hidden_end: int | None = None,
        dot_key: str | None = None,
        dash_key: str | None = None,
        escape: bool | None = None,
        on_fail: Callable | None = None,
    ) -> "CpfFormatterOptions":
        """Creates a new CpfFormatterOptions instance with the given options merged with the current instance."""
        kwargs = {}

        if hidden is not None:
            kwargs["hidden"] = hidden
        if hidden_key is not None:
            kwargs["hidden_key"] = hidden_key
        if hidden_start is not None:
            kwargs["hidden_start"] = hidden_start
        if hidden_end is not None:
            kwargs["hidden_end"] = hidden_end
        if dot_key is not None:
            kwargs["dot_key"] = dot_key
        if dash_key is not None:
            kwargs["dash_key"] = dash_key
        if escape is not None:
            kwargs["escape"] = escape
        if on_fail is not None:
            kwargs["on_fail"] = on_fail

        new_start = kwargs.get("hidden_start", self.hidden_start)
        new_end = kwargs.get("hidden_end", self.hidden_end)

        new_options = replace(self, **kwargs)
        new_options.set_hidden_range(new_start, new_end)

        return new_options

    def set_hidden_range(self, start: int, end: int) -> None:
        """Sets the range of hidden digits for the CPF formatter."""
        if start < MIN_HIDDEN_RANGE or start > MAX_HIDDEN_RANGE:
            raise CpfFormatterHiddenRangeError(
                "hidden_start", start, MIN_HIDDEN_RANGE, MAX_HIDDEN_RANGE
            )

        if end < MIN_HIDDEN_RANGE or end > MAX_HIDDEN_RANGE:
            raise CpfFormatterHiddenRangeError(
                "hidden_end", end, MIN_HIDDEN_RANGE, MAX_HIDDEN_RANGE
            )

        if start > end:
            start, end = end, start

        object.__setattr__(self, "hidden_start", start)
        object.__setattr__(self, "hidden_end", end)

    def __setattr__(self, name: str, value: object):
        if name == "hidden_start":
            if value is not None:
                object.__setattr__(self, name, value)

                if hasattr(self, "hidden_end") and self.hidden_end is not None:
                    self.set_hidden_range(self.hidden_start, self.hidden_end)
                    return
        elif name == "hidden_end":
            if value is not None:
                object.__setattr__(self, name, value)

                if hasattr(self, "hidden_start") and self.hidden_start is not None:
                    self.set_hidden_range(self.hidden_start, self.hidden_end)
                    return
        elif name == "on_fail":
            if value is None:
                if hasattr(self, "on_fail") and self.on_fail is not None:
                    raise TypeError(
                        '"on_fail" argument must be a callable, NoneType given'
                    )
            elif not callable(value):
                raise TypeError(
                    f'"on_fail" argument must be a callable, {type(value).__name__} given'
                )

        object.__setattr__(self, name, value)
