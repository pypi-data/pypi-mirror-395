"""Type single.reading, version 000"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, StrictInt

from gwproto.property_format import (
    SpaceheatName,
    UTCMilliseconds,
)


class SingleReading(BaseModel):
    ChannelName: SpaceheatName
    Value: StrictInt
    ScadaReadTimeUnixMs: UTCMilliseconds
    TypeName: Literal["single.reading"] = "single.reading"
    Version: str = "000"

    model_config = ConfigDict(use_enum_values=True)
