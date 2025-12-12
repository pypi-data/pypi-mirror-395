from gwproto.data_classes.components.component import Component
from gwproto.named_types.component_attribute_class_gt import ComponentAttributeClassGt
from gwproto.named_types.web_server_component_gt import WebServerComponentGt
from gwproto.named_types.web_server_gt import WebServerGt


class WebServerComponent(Component[WebServerComponentGt, ComponentAttributeClassGt]):
    @property
    def web_server_gt(self) -> WebServerGt:
        return self.gt.WebServer
