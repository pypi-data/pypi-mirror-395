"""Type resistive.heater.cac.gt, version 000"""

from typing import Literal

from gwproto.named_types import ComponentAttributeClassGt


class ResistiveHeaterCacGt(ComponentAttributeClassGt):
    NameplateMaxPowerW: int
    RatedVoltageV: int
    TypeName: Literal["resistive.heater.cac.gt"] = "resistive.heater.cac.gt"
