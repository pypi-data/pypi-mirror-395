"""Type keyparam.change.log, version 000"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator

from gwproto.enums import KindOfParam
from gwproto.property_format import (
    LeftRightDotStr,
    check_is_log_style_date_with_millis,
)


class KeyparamChangeLog(BaseModel):
    """
    Key Param Change Record.

    The keyparam.change.record type is designed for straightforward logging of important parameter
    changes in the SCADA and AtomicTNode code for transactive space-heating systems. Check out
    the details in [gridworks-atn]( https://github.com/thegridelectric/gridworks-atn) and [gw-scada-spaceheat-python](https://github.com/thegridelectric/gw-scada-spaceheat-python).
    It's made for humans—developers and system maintainers—to easily create and reference records
    of significant changes. Keep it short and sweet. We suggest using a "Before" and "After"
    attribute pattern to include the changed value, focusing for example on specific components
    rather than the entire hardware layout.
    """

    AboutNodeAlias: LeftRightDotStr
    ChangeTimeUtc: str
    Author: str
    ParamName: str
    Description: str
    Kind: KindOfParam
    TypeName: Literal["keyparam.change.log"] = "keyparam.change.log"
    Version: str = "000"

    model_config = ConfigDict(extra="allow", use_enum_values=True)

    @field_validator("ChangeTimeUtc")
    @classmethod
    def _check_change_time_utc(cls, v: str) -> str:
        try:
            check_is_log_style_date_with_millis(v)
        except ValueError as e:
            raise ValueError(
                f"ChangeTimeUtc failed LogStyleDateWithMillis format validation: {e}",
            ) from e
        return v
