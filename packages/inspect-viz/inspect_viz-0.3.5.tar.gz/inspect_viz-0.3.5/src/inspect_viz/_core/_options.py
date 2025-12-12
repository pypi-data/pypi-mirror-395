from contextlib import contextmanager
from types import SimpleNamespace
from typing import Iterator, Literal, TypedDict

from typing_extensions import Unpack


class OptionsArgs(TypedDict):
    output_format: Literal["auto", "js", "png"]


class Options(SimpleNamespace):
    """Inspect Viz global options."""

    output_format: Literal["auto", "js", "png"]
    """Output format for components.

    Defaults to "auto", which resolves to "js" (interactive plots and tables)
    in all contexts except Quarto PDF output (which uses "png"). Specify
    "png" to always write static PNG images instead (interactive features will
    be disabled in this case).
    """


options: Options = Options(output_format="auto")
"""Inspect Viz global options."""


@contextmanager
def options_context(**kwargs: Unpack[OptionsArgs]) -> Iterator[None]:
    """Context manager for temporarily overriding global options.

    Args:
        **kwargs: Options to override within the context.
    """
    global options
    options_backup = Options(**vars(options))
    try:
        for k, v in kwargs.items():
            setattr(options, k, v)
        yield
    finally:
        options = options_backup
