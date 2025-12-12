from enum import auto

from gw.enums import GwStrEnum


class AlertPriority(GwStrEnum):
    """
    The GridWorks in-house enum for prioritizing alerts in a context where distributed equipment
    maintenance affects people's comfort and well-being.
    Values:
      - P1Critical: Critical alerts represent situations where immediate action is required
        to prevent significant impact or harm. These alerts should be addressed immediately,
        as they have the potential to cause significant disruption or endangerment to people's
        comfort and well-being.
      - P2High: High-priority alerts represent situations that require urgent attention
        to prevent significant impact or harm. While not as critical as P1 alerts, P2 alerts
        still require prompt action to address the issue and prevent further escalation.
      - P3Medium: Medium-priority alerts represent situations that require attention to
        prevent potential impact or harm. These alerts should be addressed in a timely manner
        to prevent any negative impact on people's comfort and well-being.
      - P4Low: Low-priority alerts represent situations that require attention but are
        not urgent. While not as critical as P1, P2, or P3 alerts, P4 alerts should still be
        addressed in a reasonable timeframe to prevent any negative impact on people's comfort
        and well-being.
      - P5Info: Informational alerts provide general information and do not require immediate
        action. These alerts may include notifications, status updates, or routine maintenance
        reminders.

    For more information:
      - [ASLs](https://gridworks-type-registry.readthedocs.io/en/latest/)
      - [Global Authority](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#alertpriority)
    """

    P1Critical = auto()
    P2High = auto()
    P3Medium = auto()
    P4Low = auto()
    P5Info = auto()

    @classmethod
    def default(cls) -> "AlertPriority":
        return cls.P3Medium

    @classmethod
    def values(cls) -> list[str]:
        return [elt.value for elt in cls]

    @classmethod
    def enum_name(cls) -> str:
        return "alert.priority"

    @classmethod
    def enum_version(cls) -> str:
        return "000"
