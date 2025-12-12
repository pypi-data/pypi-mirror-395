"""Type report, version 002"""

from typing import Literal

from pydantic import BaseModel, PositiveInt, field_validator

from gwproto.named_types.channel_readings import ChannelReadings
from gwproto.named_types.fsm_full_report import FsmFullReport
from gwproto.named_types.machine_states import MachineStates
from gwproto.property_format import (
    LeftRightDotStr,
    UTCMilliseconds,
    UTCSeconds,
    UUID4Str,
)


class Report(BaseModel):
    """ """

    FromGNodeAlias: LeftRightDotStr
    FromGNodeInstanceId: UUID4Str
    AboutGNodeAlias: LeftRightDotStr
    SlotStartUnixS: UTCSeconds
    SlotDurationS: PositiveInt
    ChannelReadingList: list[ChannelReadings]
    StateList: list[MachineStates]
    FsmReportList: list[FsmFullReport]
    MessageCreatedMs: UTCMilliseconds
    Id: UUID4Str
    TypeName: Literal["report"] = "report"
    Version: str = "002"

    @field_validator("ChannelReadingList")
    @classmethod
    def _check_channel_reading_list(
        cls, v: list[ChannelReadings]
    ) -> list[ChannelReadings]:
        return v
