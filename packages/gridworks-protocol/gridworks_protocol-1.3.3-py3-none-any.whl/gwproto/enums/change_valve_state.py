# Literal Enum:
#  - no additional values can be added over time.
#  - Sent as-is, not in hex symbol
from enum import auto

from gw.enums import GwStrEnum


class ChangeValveState(GwStrEnum):
    """
    Events used in the IsoValve finite state machine.
    """

    OpenValve = auto()
    CloseValve = auto()

    @classmethod
    def values(cls) -> list[str]:
        """
        Returns enum choices
        """
        return [elt.value for elt in cls]

    @classmethod
    def default(cls) -> "ChangeValveState":
        return cls.OpenValve

    @classmethod
    def enum_name(cls) -> str:
        return "change.valve.state"
