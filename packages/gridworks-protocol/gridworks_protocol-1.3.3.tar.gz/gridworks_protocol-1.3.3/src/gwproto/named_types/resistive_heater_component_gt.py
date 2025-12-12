"""Type resistive.heater.component.gt, version 000"""

from typing import Literal, Optional

from gwproto.named_types import ComponentGt


class ResistiveHeaterComponentGt(ComponentGt):
    TestedMaxHotMilliOhms: Optional[int] = None
    TestedMaxColdMilliOhms: Optional[int] = None
    TypeName: Literal["resistive.heater.component.gt"] = "resistive.heater.component.gt"
