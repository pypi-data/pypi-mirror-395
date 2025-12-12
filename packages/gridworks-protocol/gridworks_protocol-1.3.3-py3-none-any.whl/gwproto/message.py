# ruff: noqa: ANN401

from collections.abc import Mapping
from typing import (
    Any,
    Callable,
    Generic,
    Literal,
    Optional,
    TypeAlias,
    TypeVar,
    Union,
)

from pydantic import BaseModel

from gwproto.topic import MQTTTopic

EnumType = TypeVar("EnumType")


def as_enum(
    value: Any, enum_type: Callable[[Any], EnumType], default: Optional[EnumType] = None
) -> Optional[EnumType]:
    try:
        return enum_type(value)
    except ValueError:
        return default


class Header(BaseModel):
    Src: str
    Dst: str = ""
    MessageType: str
    MessageId: str = ""
    AckRequired: bool = False
    TypeName: Literal["gridworks.header"] = "gridworks.header"
    Version: str = "001"


# MyPy needs this because the class variable of Message is 'Header'.
# An alternative might be use snake case and set up pydantic to
# correct generate the aliases as expected.
HeaderT: TypeAlias = Header

PayloadT = TypeVar("PayloadT")

PAYLOAD_TYPE_FIELDS = ["TypeName", "type_alias", "TypeName", "type_name"]


def ensure_arg(arg_name: str, default_value: Any, kwargs_dict: dict[str, Any]) -> None:
    if arg_name not in kwargs_dict:
        payload = kwargs_dict.get("Payload")
        if payload is None or not hasattr(payload, arg_name):
            kwargs_dict[arg_name] = default_value


class Message(BaseModel, Generic[PayloadT]):
    Header: Header
    Payload: PayloadT
    TypeName: Literal["gw"] = "gw"

    def __init__(self, header: Optional[HeaderT] = None, **kwargs: Any) -> None:
        if header is None:
            header = self._header_from_kwargs(kwargs)
        super().__init__(Header=header, **kwargs)

    def message_type(self) -> str:
        return self.Header.MessageType

    def src(self) -> str:
        return self.Header.Src

    def dst(self) -> str:
        return self.Header.Dst

    @classmethod
    def type_name(cls) -> str:
        return str(Message.model_fields["TypeName"].default)

    def mqtt_topic(self) -> str:
        return MQTTTopic.encode(
            envelope_type=self.type_name(),
            src=self.src(),
            dst=self.dst(),
            message_type=self.message_type(),
        )

    @classmethod
    def _header_from_kwargs(cls, kwargs: dict[str, Any]) -> HeaderT:
        header_kwargs = {}
        if "Payload" in kwargs:
            payload = kwargs["Payload"]
            for header_field, payload_fields in [
                ("Src", ["Src"]),
                ("Dst", ["Dst"]),
                ("MessageId", ["MessageId"]),
                ("MessageType", PAYLOAD_TYPE_FIELDS),
                ("AckRequired", ["AckRequired"]),
            ]:
                val = kwargs.get(header_field)
                if val is None:
                    for payload_field in payload_fields:
                        if hasattr(payload, payload_field):
                            val = getattr(payload, payload_field)
                        elif isinstance(payload, Mapping) and payload_field in payload:
                            val = payload[payload_field]
                if val is not None:
                    header_kwargs[header_field] = val
        header: Optional[Union[Header, dict[str, Any]]] = kwargs.pop("Header", None)
        if isinstance(header, Header):
            header = header.model_copy(update=header_kwargs, deep=True)
        else:
            if header is not None:
                header_kwargs = dict(header, **header_kwargs)
            header = Header(**header_kwargs)
        return header


GRIDWORKS_ENVELOPE_TYPE = Message.type_name()
