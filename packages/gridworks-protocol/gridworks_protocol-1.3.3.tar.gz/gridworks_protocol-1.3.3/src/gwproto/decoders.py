# ruff: noqa: ANN401

import abc
import inspect
import re
import sys
from abc import abstractmethod
from collections.abc import Sequence

# Static analysis (mypy, pycharm) thinks 'types' here is gwproto.named_types.
from types import ModuleType  # noqa
from typing import (
    Any,
    Generic,
    Literal,
    Optional,
    TypeVar,
    Union,
    get_origin,
)

import pydantic
from pydantic import BaseModel, Field, ValidationError, create_model
from pydantic_core import ErrorDetails

from gwproto.message import Message
from gwproto.messages import AnyEvent
from gwproto.named_types import ComponentAttributeClassGt, ComponentGt
from gwproto.topic import MQTTTopic

MessageDiscriminator = TypeVar("MessageDiscriminator", bound=Message[Any])

TYPE_NAME_FIELD: str = "TypeName"


class MQTTCodec(abc.ABC):
    ENCODING = "utf-8"
    message_model: type[Message[Any]]

    def __init__(self, message_model: type[Message[Any]]) -> None:
        self.message_model = message_model

    def encode(self, content: bytes | BaseModel) -> bytes:  # noqa
        if isinstance(content, bytes):
            encoded = content
        else:
            encoded = content.model_dump_json().encode()
        return encoded

    @classmethod
    def get_unrecognized_payload_error(
        cls, e: ValidationError
    ) -> Optional[ErrorDetails]:
        for error in e.errors():
            if error.get("type", "") == "union_tag_invalid" and error.get("loc") == (
                "Payload",
            ):
                ctx = error.get("ctx", {})
                if ctx.get("discriminator") == "'TypeName'":
                    return error
        return None

    def handle_unrecognized_payload(  # noqa
        self, payload: bytes, e: ValidationError, details: ErrorDetails
    ) -> Message[Any]:
        if details.get("ctx", {}).get("tag", "").startswith("gridworks.event"):
            try:
                return Message[AnyEvent].model_validate_json(payload)
            except ValidationError as e2:
                raise e2 from e
        raise e

    def decode(self, topic: str, payload: bytes) -> Message[Any]:
        self.validate_topic(topic)
        try:
            message = self.message_model.model_validate_json(payload)
        except pydantic.ValidationError as e:
            # ValidationError can result because we receive a TypeName we don't
            # recognize, either because the sender is newer or older than our
            # code. In some cases we can still meaningfully interpret the
            # message, for example if we can recognize that it is an event
            # message, as is done here.
            if error_details := self.get_unrecognized_payload_error(e):
                return self.handle_unrecognized_payload(payload, e, error_details)
            raise
        return message

    def validate_topic(self, topic: str) -> None:
        decoded_topic = MQTTTopic.decode(topic)
        if decoded_topic.envelope_type != self.message_model.type_name():
            raise ValueError(
                f"Type {decoded_topic.envelope_type} not recognized. "
                f"Available decoders: {self.message_model.type_name()}"
            )
        self.validate_source_and_destination(decoded_topic.src, decoded_topic.dst)

    @abstractmethod
    def validate_source_and_destination(self, src: str, dst: str) -> None: ...

    @classmethod
    def _try_message_as_event(
        cls, payload: bytes, original_exception: ValidationError
    ) -> Message[Any]:
        for error in original_exception.errors():
            if error.get("type", "") == "union_tag_invalid":
                ctx = error.get("ctx", {})
                if ctx.get("discriminator", "") == "'TypeName'" and ctx.get(
                    "tag", ""
                ).startswith("gridworks.event"):
                    try:
                        return Message[AnyEvent].model_validate_json(payload)
                    except Exception as e2:  # noqa: BLE001
                        raise e2 from original_exception
        raise original_exception


def get_model_type_name(cls: Any) -> str:
    """Return cls.TypeName, if cls inherits from BaseModel, has a TypeName field,
    and that field is a Literal, else returns an empty string.
    """
    if (
        issubclass(cls, BaseModel)
        and TYPE_NAME_FIELD in cls.model_fields
        and get_origin(cls.model_fields[TYPE_NAME_FIELD].annotation) == Literal
    ):
        return str(cls.model_fields[TYPE_NAME_FIELD].default)
    return ""


def get_candidate_modules(
    module_names: str | Sequence[str],
    modules: Optional[Sequence[Any]] = None,
) -> Sequence[ModuleType]:
    if isinstance(module_names, str):
        module_names = [module_names] if module_names else []
    if unimported := [
        module_name for module_name in module_names if module_name not in sys.modules
    ]:
        raise ValueError(f"ERROR. modules {unimported} have not been imported.")
    if modules is None:
        modules = []
    return [sys.modules[module_name] for module_name in module_names] + list(modules)


EXCLUDED_TYPE_NAMES: set[str] = {Message.type_name()}


def get_candidate_payload_classes(
    module: ModuleType,
) -> Sequence[tuple[str, type[BaseModel]]]:
    """From a given module, return list of (TypeName, class) tuples for each
    object in the module that:
        * Is a class
        * Is or inherits from BaseModel
        * Has a TypeName which is a Literal with a value.
        * TypeName is not in EXCLUDED_TYPE_NAMES, which can happen if the class
          is a refinement of Message (e.g. PingMessage).
    """
    return [
        (str(module_class.model_fields[TYPE_NAME_FIELD].default), module_class)
        for _, module_class in inspect.getmembers(module, inspect.isclass)
        if (
            issubclass(module_class, BaseModel)
            and TYPE_NAME_FIELD in module_class.model_fields
            and get_origin(module_class.model_fields[TYPE_NAME_FIELD].annotation)
            == Literal
            and len(str(module_class.model_fields[TYPE_NAME_FIELD].default)) > 0
            and str(module_class.model_fields[TYPE_NAME_FIELD].default)
            not in EXCLUDED_TYPE_NAMES
        )
    ]


def include_candidate_class(
    type_name: str,
    candidate_class: type[BaseModel],
    accumulated_types: dict[str, type[BaseModel]],
    type_name_regex: Optional[re.Pattern[str]],
) -> bool:
    if (
        type_name not in EXCLUDED_TYPE_NAMES
        and type_name in accumulated_types
        and accumulated_types[type_name] is not candidate_class
    ):
        raise ValueError(
            f"ERROR {TYPE_NAME_FIELD} ({type_name}) "
            f"for {candidate_class} already seen for "
            f"class {accumulated_types[type_name]}"
        )
    return not (type_name_regex is not None and not type_name_regex.match(type_name))


def pydantic_named_types(
    module_names: str | Sequence[str],
    modules: Optional[Sequence[Any]] = None,
    type_name_regex: Optional[re.Pattern[str]] = None,
) -> list[Any]:
    """Find Pyantic BaseModels with Literal 'TypeName' fields."""
    named_types = []
    accumulated_types: dict[str, Any] = {}
    for module in get_candidate_modules(module_names, modules):
        for type_name, candidate_class in get_candidate_payload_classes(module):
            if (
                type_name in accumulated_types
                and accumulated_types[type_name] is not candidate_class
            ):
                raise ValueError(
                    f"ERROR {TYPE_NAME_FIELD} ({type_name}) "
                    f"for {candidate_class} already seen for "
                    f"class {accumulated_types[type_name]}"
                )
            if type_name_regex is None or type_name_regex.match(type_name):
                accumulated_types[type_name] = candidate_class
                named_types.append(candidate_class)
    return named_types


def create_message_model(
    model_name: str,
    module_names: str | Sequence[str] = "",
    modules: Optional[Sequence[Any]] = None,
    explicit_types: Optional[Sequence[Any]] = None,
    type_name_regex: Optional[re.Pattern[str]] = None,
) -> type[Message[Any]]:
    used_types = pydantic_named_types(
        module_names=module_names,
        modules=modules,
        type_name_regex=type_name_regex,
    )
    if explicit_types is not None:
        used_types.extend(explicit_types)
    return create_model(
        model_name,
        __base__=Message,
        Payload=(
            Union[tuple(used_types)],
            Field(..., discriminator=TYPE_NAME_FIELD),
        ),
    )


WrappedT = TypeVar("WrappedT")


class UnionWrapper(BaseModel, Generic[WrappedT]):
    """A utility class suitable for decoding a from union of types. In order
    to treat input as a union of types, Pydantic requires that our union be in
    named field, which by convention we call "Wrapped".
    """

    Wrapped: WrappedT

    @classmethod
    def create(
        cls,
        model_name: str,
        *,
        module_names: str | Sequence[str] = "",
        modules: Optional[Sequence[Any]] = None,
        explicit_types: Optional[Sequence[Any]] = None,
        type_name_regex: Optional[re.Pattern[str]] = None,
    ) -> type["UnionWrapper[WrappedT]"]:
        """Create pydantic model that is a union of all appropriate types found via
        module_names, modules and explicit_types"""
        used_types = pydantic_named_types(
            module_names=module_names,
            modules=modules,
            type_name_regex=type_name_regex,
        )
        if explicit_types is not None:
            used_types.extend(explicit_types)
        if len(used_types) == 1:
            payload_field_type = (
                used_types[0],
                Field(...),
            )
        else:
            payload_field_type = (
                Union[tuple(used_types)],
                Field(..., discriminator=TYPE_NAME_FIELD),
            )
        # Pydantic requires us to put our discriminated union in a named field.
        # We use the name 'Wrapped'.
        return create_model(
            model_name, __base__=UnionWrapper, Wrapped=payload_field_type
        )


class UnionDecoder:
    """A Utility base class for decoding from a union of types."""

    loader: type[UnionWrapper[Any]]

    def __init__(
        self,
        model_name: str,
        *,
        module_names: str | Sequence[str] = "",
        modules: Optional[Sequence[Any]] = None,
        explicit_types: Optional[Sequence[Any]] = None,
        type_name_regex: Optional[re.Pattern[str]] = None,
    ) -> None:
        self.loader = UnionWrapper.create(
            model_name=model_name,
            module_names=module_names,
            modules=modules,
            explicit_types=explicit_types,
            type_name_regex=type_name_regex,
        )


class CacDecoder(UnionDecoder):
    TYPE_NAME_REGEX = re.compile(r".*\.cac\.gt")
    loader: type[UnionWrapper[Any]]

    def __init__(
        self,
        model_name: str,
        type_name_regex: Optional[re.Pattern[str]] = TYPE_NAME_REGEX,
        **kwargs: Any,
    ) -> None:
        super().__init__(model_name, type_name_regex=type_name_regex, **kwargs)

    def decode(
        self, cac_dict: dict[str, Any], *, allow_missing: bool = True
    ) -> ComponentAttributeClassGt:
        decoded: ComponentAttributeClassGt
        try:
            decoded = self.loader.model_validate({"Wrapped": cac_dict}).Wrapped
            if not isinstance(decoded, ComponentAttributeClassGt):
                raise TypeError(
                    f"ERROR. CacDecoder decoded type {type(decoded)}, "
                    "not ComponentAttributeClassGt"
                )
        except ValidationError as e:
            if allow_missing and any(
                error.get("type") == "union_tag_invalid" for error in e.errors()
            ):
                decoded = ComponentAttributeClassGt(**cac_dict)
            else:
                raise
        return decoded


class ComponentDecoder(UnionDecoder):
    TYPE_NAME_REGEX = re.compile(r".*\.?component\.gt")

    def __init__(
        self,
        model_name: str,
        type_name_regex: Optional[re.Pattern[str]] = TYPE_NAME_REGEX,
        **kwargs: Any,
    ) -> None:
        super().__init__(model_name, type_name_regex=type_name_regex, **kwargs)

    def decode(
        self, component_dict: dict[str, Any], *, allow_missing: bool = True
    ) -> ComponentGt:
        decoded: ComponentGt
        try:
            # Pydantic requires that our union of types (components here) be in
            # a named field, which by convention we call "Wrapped".
            decoded = self.loader.model_validate({"Wrapped": component_dict}).Wrapped
            if not isinstance(decoded, ComponentGt):
                raise TypeError(
                    f"ERROR. ComponentDecoder decoded type {type(decoded)}, "
                    "not ComponentGt"
                )
        except ValidationError as e:
            if allow_missing and any(
                error.get("type") == "union_tag_invalid" for error in e.errors()
            ):
                decoded = ComponentGt(**component_dict)
            else:
                raise
        return decoded
