"""Type alert, version 000"""

from typing import Literal, Optional

from pydantic import BaseModel

from gwproto.property_format import (
    LeftRightDotStr,
    SpaceheatName,
    UTCSeconds,
)


class Alert(BaseModel):
    FromGNodeAlias: LeftRightDotStr
    AboutNode: Optional[SpaceheatName] = None
    UnixS: UTCSeconds
    Summary: str
    OpsGenieAlias: Optional[str] = None
    TypeName: Literal["alert"] = "alert"
    Version: str = "000"
