"""PicoFlowModuleComponent definition"""

from gwproto.data_classes.components.component import Component
from gwproto.named_types import ComponentAttributeClassGt, PicoFlowModuleComponentGt


class PicoFlowModuleComponent(
    Component[PicoFlowModuleComponentGt, ComponentAttributeClassGt]
): ...
