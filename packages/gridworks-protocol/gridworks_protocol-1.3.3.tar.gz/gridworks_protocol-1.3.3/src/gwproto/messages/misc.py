# ruff: noqa: ANN401

import uuid
from typing import Any, Literal

from pydantic import BaseModel, Field

from gwproto.message import Message


class Ack(BaseModel):
    AckMessageID: str
    TypeName: Literal["gridworks.ack"] = "gridworks.ack"


class Ping(BaseModel):
    MessageId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    TypeName: Literal["gridworks.ping"] = "gridworks.ping"


class PingMessage(Message[Ping]):
    def __init__(self, *, AckRequired: bool = True, **kwargs: Any) -> None:  # noqa: N803
        if "Payload" not in kwargs:
            kwargs["Payload"] = Ping()
        super().__init__(AckRequired=AckRequired, **kwargs)
