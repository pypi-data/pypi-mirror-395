from enum import auto

from gw.enums import GwStrEnum


class FsmName(GwStrEnum):
    """
    The name of a specific Spaceheat finite state machine. That name is used as a literal enum
    for a set of staets.
    Values:
      - Unknown
      - StoreFlowDirection
      - RelayState: Finite State Machine for a normally open or normally closed relay
        whose states (Closed, Open) are enumerated by RelayClosedOrOpen.
      - RelayPinState: Finite State Machine for a relay pin with states enumerated by
        RelayEnergizationState (Energized and DeEnergized).

    For more information:
      - [ASLs](https://gridworks-type-registry.readthedocs.io/en/latest/)
      - [Global Authority](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#shfsmname)
      - [More Info](https://gridworks-protocol.readthedocs.io/en/latest/house-0.html)
    """

    Unknown = auto()
    StoreFlowDirection = auto()
    RelayState = auto()
    RelayPinState = auto()

    @classmethod
    def default(cls) -> "FsmName":
        return cls.StoreFlowDirection

    @classmethod
    def values(cls) -> list[str]:
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        return "sh.fsm.name"

    @classmethod
    def enum_version(cls) -> str:
        return "000"
