from abc import ABC
from pydantic import BaseModel, ConfigDict


class BaseCommand(BaseModel, ABC):
    model_config = ConfigDict(frozen=True)
