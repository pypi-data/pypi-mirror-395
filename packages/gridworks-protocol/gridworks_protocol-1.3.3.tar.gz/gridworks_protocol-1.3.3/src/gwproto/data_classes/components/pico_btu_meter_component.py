"""PicoBtuMeterComponent definition"""

from gwproto.data_classes.components.component import Component
from gwproto.named_types import ComponentAttributeClassGt, PicoBtuMeterComponentGt


class PicoBtuMeterComponent(
    Component[PicoBtuMeterComponentGt, ComponentAttributeClassGt]
): ...
