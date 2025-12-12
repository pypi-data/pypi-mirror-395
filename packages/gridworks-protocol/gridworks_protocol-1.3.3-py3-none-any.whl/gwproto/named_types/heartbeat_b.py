"""Type heartbeat.b, version 001"""

from typing import Literal

from pydantic import BaseModel, Field

from gwproto.property_format import HexChar, LeftRightDotStr, UTCMilliseconds, UUID4Str


class HeartbeatB(BaseModel):
    FromGNodeAlias: LeftRightDotStr
    FromGNodeInstanceId: UUID4Str
    MyHex: HexChar = Field(
        title="Hex character getting sent",
        default="0",
    )
    YourLastHex: HexChar = Field(
        title="Last hex character received from heartbeat partner.",
    )
    LastReceivedTimeUnixMs: UTCMilliseconds = Field(
        title="Time YourLastHex was received on my clock",
    )
    SendTimeUnixMs: UTCMilliseconds = Field(
        title="Time this message is made and sent on my clock",
    )
    StartingOver: bool = Field(
        title="True if the heartbeat initiator wants to start the volley over",
        description=(
            "(typically the AtomicTNode in an AtomicTNode / SCADA pair) wants to start the heartbeating "
            "volley over. The result is that its partner will not expect the initiator to know "
            "its last Hex."
        ),
    )
    TypeName: Literal["heartbeat.b"] = "heartbeat.b"
    Version: str = "001"

    def __hash__(self) -> int:
        return hash((type(self), *self.__dict__.values()))
