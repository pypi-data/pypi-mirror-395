"""DfrComponent definition"""

from gwproto.data_classes.components.component import Component
from gwproto.named_types import ComponentAttributeClassGt, DfrComponentGt


class DfrComponent(Component[DfrComponentGt, ComponentAttributeClassGt]): ...
