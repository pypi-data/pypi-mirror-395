from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from common.command.base_command import BaseCommand

C = TypeVar("C", bound=BaseCommand)


class BaseCommandHandler(Generic[C], ABC):
    @abstractmethod
    async def handle_command(self, command: C) -> tuple[dict, int]:
        pass
