"""Type dfr.config, version 000"""

from typing import Literal

from pydantic import PositiveInt, StrictInt

from gwproto.named_types import ChannelConfig


class DfrConfig(ChannelConfig):
    OutputIdx: PositiveInt
    InitialVoltsTimes100: StrictInt
    TypeName: Literal["dfr.config"] = "dfr.config"
    Version: str = "000"
