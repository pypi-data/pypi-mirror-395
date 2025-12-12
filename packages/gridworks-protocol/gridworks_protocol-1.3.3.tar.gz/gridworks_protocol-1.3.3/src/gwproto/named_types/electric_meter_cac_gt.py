"""Type electric.meter.cac.gt, version 010"""

from typing import Literal, Optional

from gwproto.enums import TelemetryName
from gwproto.named_types import ComponentAttributeClassGt


class ElectricMeterCacGt(ComponentAttributeClassGt):
    TelemetryNameList: list[TelemetryName]
    DefaultBaud: Optional[int] = None
    TypeName: Literal["electric.meter.cac.gt"] = "electric.meter.cac.gt"
    Version: str = "001"
