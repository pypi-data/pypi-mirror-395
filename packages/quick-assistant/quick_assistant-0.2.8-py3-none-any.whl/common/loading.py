from contextlib import contextmanager
from typing import Generator

from common.console import get_console


@contextmanager
def spinner(message: str, spinner_style: str = "dots") -> Generator[None, None, None]:
    console = get_console()
    with console.status(message, spinner=spinner_style):
        yield
