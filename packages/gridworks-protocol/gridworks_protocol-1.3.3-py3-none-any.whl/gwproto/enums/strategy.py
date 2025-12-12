from enum import auto

from gw.enums import GwStrEnum


class Strategy(GwStrEnum):
    """

    Values:
      - Ha2Oil: HomeAlone2 - Also a home alone strategy for House0. If the heat pump is
        not coming on, then switch to oil boiler. TODO: DESIGN, WRITE UP
      - Ha1: HomeAlone1 - the first home alone strategy for House0. TODO: WRITE UP

    For more information:
      - [ASLs](https://gridworks-type-registry.readthedocs.io/en/latest/)
      - [Global Authority](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#spaceheatstrategy)
    """

    Ha2Oil = auto()
    Ha1 = auto()

    @classmethod
    def default(cls) -> "Strategy":
        return cls.Ha1

    @classmethod
    def values(cls) -> list[str]:
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        return "spaceheat.strategy"

    @classmethod
    def enum_version(cls) -> str:
        return "000"
