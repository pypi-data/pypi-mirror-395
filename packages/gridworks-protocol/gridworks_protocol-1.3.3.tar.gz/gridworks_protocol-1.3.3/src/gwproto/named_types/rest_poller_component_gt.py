"""Code for actors that use a simple rest interaction, converting the response to one or more
REST commands into a message posted to main processing thread.

"""

from typing import Literal

from gwproto.named_types import ComponentGt
from gwproto.named_types.rest_poller_gt import RESTPollerSettings


class RESTPollerComponentGt(ComponentGt):
    Rest: RESTPollerSettings
    TypeName: Literal["rest.poller.component.gt"] = "rest.poller.component.gt"
