from gwproto.data_classes.components.component import Component
from gwproto.named_types.component_attribute_class_gt import ComponentAttributeClassGt
from gwproto.named_types.fibaro_smart_implant_component_gt import (
    FibaroSmartImplantComponentGt,
)


class FibaroSmartImplantComponent(
    Component[FibaroSmartImplantComponentGt, ComponentAttributeClassGt]
): ...
