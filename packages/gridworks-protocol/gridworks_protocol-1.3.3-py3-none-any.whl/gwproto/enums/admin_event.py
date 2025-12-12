from enum import auto

from gw.enums import GwStrEnum


class AdminEvent(GwStrEnum):
    """

    Values:
      - WakeUp
      - GoDormant

    For more information:
      - [ASLs](https://gridworks-type-registry.readthedocs.io/en/latest/)
      - [Global Authority](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#adminevent)
    """

    WakeUp = auto()
    GoDormant = auto()

    @classmethod
    def default(cls) -> "AdminEvent":
        return cls.WakeUp

    @classmethod
    def values(cls) -> list[str]:
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        return "admin.event"

    @classmethod
    def enum_version(cls) -> str:
        return "000"
