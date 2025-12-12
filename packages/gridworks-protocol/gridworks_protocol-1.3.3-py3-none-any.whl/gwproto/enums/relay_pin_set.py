"""Old School enum (uses integers)"""

from enum import Enum


class RelayPinSet(Enum):
    """
    This refers to an ACTION taken by a driver (as opposed to a relay energization pin STATE
    read by the same driver). It is an old-school enum, where DeEnergized encodes 0 and Energized
    encodes 1.
    """

    DeEnergized = 0
    Energized = 1

    @classmethod
    def values(cls) -> list[int]:
        """
        Returns enum choices
        """
        return [elt.value for elt in cls]

    @classmethod
    def default(cls) -> "RelayPinSet":
        return cls.DeEnergized

    @classmethod
    def enum_name(cls) -> str:
        return "relay.pin.set"
