"""
GridWorks Enums used in gwproto, the Application Shared Language (ASL) used by SCADA
devices and AtomicTNodes to communicate with each other. These enums play a specific structural
role as semantic "glue" within ASLs.

Key attributes:
  - Enum values are translated into "GridWorks Type Enum Symbols" (GtEnumSymbols) when embedded
  in a serialized type sent as a message from one Application and/or Actor to another.
  - Each Enum has a unique name in the type registry (like spaceheat.telemetry.name), along
  with a version (like 001).
  - That name are interpretted locally in the SDK and do not necessarily carry the larger
  context of the unique type registry name (for example gwproto uses TelemetryName, since
  the `spaceheat` context goes without saying).
  - Each Value/Symbol pair also has a version. Value/Symbol pairs cannot be changed or removed.
  The only adjustments that can be made to an enum are adding more Value/Symbols. This is to
  support forwards- and backwards- compatability in GridWorks Types that use these enums.

If Enums are "glue", then GridWorks Types are the building blocks of SALs. Every SAL is comprised
of a set of shared GridWorks Types.

Application Shared Languages are an evolution of the concept of Application Programming Interfaces.
In a nutshell, an API can be viewed as a rather restricted version of an SAL, where only one application
has anything complex/interesting to say and, in general, the developers/owners of that application
have sole responsibility for managing the versioning and changing of that API. Note also that SALs
do not make any a priori assumption about the relationship (i.e. the default client/server for an API)
or the message delivery mechanism (i.e. via default GET/POST to RESTful URLs). For more information
on these ideas:
  - [GridWorks Enums](https://gridwork-type-registry.readthedocs.io/en/latest/types.html)
  - [GridWorks Types](https://gridwork-type-registry.readthedocs.io/en/latest/types.html)
  - [ASLs](https://gridwork-type-registry.readthedocs.io/en/latest/asls.html)
"""

from gwproto.enums.actor_class import ActorClass
from gwproto.enums.admin_event import AdminEvent
from gwproto.enums.admin_state import AdminState
from gwproto.enums.alert_priority import AlertPriority
from gwproto.enums.aquastat_control import AquastatControl
from gwproto.enums.change_aquastat_control import ChangeAquastatControl
from gwproto.enums.change_heat_pump_control import ChangeHeatPumpControl
from gwproto.enums.change_heatcall_source import ChangeHeatcallSource
from gwproto.enums.change_primary_pump_control import ChangePrimaryPumpControl
from gwproto.enums.change_relay_pin import ChangeRelayPin
from gwproto.enums.change_relay_state import ChangeRelayState
from gwproto.enums.change_store_flow_relay import ChangeStoreFlowRelay
from gwproto.enums.change_valve_state import ChangeValveState
from gwproto.enums.fsm_action_type import FsmActionType
from gwproto.enums.fsm_name import FsmName
from gwproto.enums.fsm_report_type import FsmReportType
from gwproto.enums.gpm_from_hz_method import GpmFromHzMethod
from gwproto.enums.heat_pump_control import HeatPumpControl
from gwproto.enums.heatcall_source import HeatcallSource
from gwproto.enums.hz_calc_method import HzCalcMethod
from gwproto.enums.kind_of_param import KindOfParam
from gwproto.enums.make_model import MakeModel
from gwproto.enums.primary_pump_control import PrimaryPumpControl
from gwproto.enums.relay_closed_or_open import RelayClosedOrOpen
from gwproto.enums.relay_energization_state import RelayEnergizationState
from gwproto.enums.relay_pin_set import RelayPinSet
from gwproto.enums.relay_wiring_config import RelayWiringConfig
from gwproto.enums.store_flow_relay import StoreFlowRelay
from gwproto.enums.strategy import Strategy
from gwproto.enums.telemetry_name import TelemetryName
from gwproto.enums.temp_calc_method import TempCalcMethod
from gwproto.enums.thermistor_data_method import ThermistorDataMethod
from gwproto.enums.unit import Unit

__all__ = [
    "ActorClass",  # [sh.actor.class.005](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#shactorclass)
    "AdminEvent",  # [admin.event.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#adminevent)
    "AdminState",  # [admin.state.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#adminstate)
    "AlertPriority",  # [alert.priority.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#alertpriority)
    "AquastatControl",  # [aquastat.control.state.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#aquastatcontrolstate)
    "ChangeAquastatControl",  # [change.aquastat.control.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#changeaquastatcontrol)
    "ChangeHeatPumpControl",  # [change.heat.pump.control.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#changeheatpumpcontrol)
    "ChangeHeatcallSource",  # [change.heatcall.source.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#changeheatcallsource)
    "ChangePrimaryPumpControl",  # [change.primary.pump.control.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#changeprimarypumpcontrol)
    "ChangeRelayPin",  # [change.relay.pin.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#changerelaypin)
    "ChangeRelayState",  # [change.relay.state.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#changerelaystate)
    "ChangeStoreFlowRelay",  # [change.store.flow.relay.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#changestoreflowrelay)
    "ChangeValveState",  # [change.valve.state.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#changevalvestate)
    "FsmActionType",  # [sh.fsm.action.type.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#shfsmactiontype)
    "FsmName",  # [sh.fsm.name.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#shfsmname)
    "FsmReportType",  # [fsm.report.type.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#fsmreporttype)
    "GpmFromHzMethod",  # [gpm.from.hz.method.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#gpmfromhzmethod)
    "HeatPumpControl",  # [heat.pump.control.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#heatpumpcontrol)
    "HeatcallSource",  # [heatcall.source.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#heatcallsource)
    "HzCalcMethod",  # [hz.calc.method.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#hzcalcmethod)
    "KindOfParam",  # [spaceheat.kind.of.param.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#spaceheatkindofparam)
    "MakeModel",  # [spaceheat.make.model.004](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#spaceheatmakemodel)
    "PrimaryPumpControl",  # [primary.pump.control.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#primarypumpcontrol)
    "RelayClosedOrOpen",  # [relay.closed.or.open.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#relayclosedoropen)
    "RelayEnergizationState",  # [relay.energization.state.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#relayenergizationstate)
    "RelayPinSet",  # [relay.pin.set.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#relaypinset)
    "RelayWiringConfig",  # [relay.wiring.config.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#relaywiringconfig)
    "StoreFlowRelay",  # [store.flow.relay.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#storeflowrelay)
    "Strategy",  # [spaceheat.strategy.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#spaceheatstrategy)
    "TelemetryName",  # [spaceheat.telemetry.name.004](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#spaceheattelemetryname)
    "TempCalcMethod",  # [temp.calc.method.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#tempcalcmethod)
    "ThermistorDataMethod",  # [thermistor.data.method.000](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#thermistordatamethod)
    "Unit",  # [spaceheat.unit.001](https://gridworks-type-registry.readthedocs.io/en/latest/enums.html#spaceheatunit)
]
