from pydantic import BaseModel, ConfigDict
from common.json import FromJSON, ToJSON


class BaseFrozen(BaseModel):
    model_config = ConfigDict(strict=True, frozen=True, arbitrary_types_allowed=False, extra="forbid")


class BaseMutable(BaseModel):
    model_config = ConfigDict(strict=True, frozen=False, arbitrary_types_allowed=False, extra="forbid")


class BaseMutableArbitrary(BaseModel):
    model_config = ConfigDict(strict=True, frozen=False, arbitrary_types_allowed=True, extra="forbid")


class BaseFrozenArbitrary(BaseModel):
    model_config = ConfigDict(strict=True, frozen=True, arbitrary_types_allowed=True, extra="forbid")


class BaseSerializable(BaseFrozen, FromJSON, ToJSON):
    pass
