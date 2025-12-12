"""Type dfr.component.gt, version 000"""

from collections.abc import Sequence
from typing import Literal

from pydantic import PositiveInt

from gwproto.named_types import ComponentGt
from gwproto.named_types.dfr_config import DfrConfig


class DfrComponentGt(ComponentGt):
    ConfigList: Sequence[DfrConfig]
    I2cAddressList: list[PositiveInt]
    TypeName: Literal["dfr.component.gt"] = "dfr.component.gt"
    Version: str = "000"
