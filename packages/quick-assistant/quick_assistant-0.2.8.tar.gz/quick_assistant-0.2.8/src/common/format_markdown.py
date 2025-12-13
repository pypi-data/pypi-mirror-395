from typing import List
from rich.markdown import Markdown
from rich.padding import Padding

from common.console import get_console


class Format:
    @staticmethod
    def markdown(response: str, spacing: List[int] = [1, 0, 0, 0]) -> None:
        console = get_console()
        markdown = Markdown(response, justify="full")
        padded_content = Padding(markdown, (spacing[0], spacing[1], spacing[2], spacing[3]))
        console.print(padded_content)
