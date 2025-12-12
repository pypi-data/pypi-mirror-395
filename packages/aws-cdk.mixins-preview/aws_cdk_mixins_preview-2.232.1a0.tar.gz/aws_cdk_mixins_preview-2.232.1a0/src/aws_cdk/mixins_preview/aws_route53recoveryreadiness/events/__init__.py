from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ..._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.interfaces.aws_route53recoveryreadiness as _aws_cdk_interfaces_aws_route53recoveryreadiness_ceddda9d


class CellEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.events.CellEvents",
):
    '''(experimental) EventBridge event patterns for Cell.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_route53recoveryreadiness import events as route53recoveryreadiness_events
        from aws_cdk.interfaces import aws_route53recoveryreadiness as interfaces_route53recoveryreadiness
        
        # cell_ref: interfaces_route53recoveryreadiness.ICellRef
        
        cell_events = route53recoveryreadiness_events.CellEvents.from_cell(cell_ref)
    '''

    @jsii.member(jsii_name="fromCell")
    @builtins.classmethod
    def from_cell(
        cls,
        cell_ref: _aws_cdk_interfaces_aws_route53recoveryreadiness_ceddda9d.ICellRef,
    ) -> "CellEvents":
        '''(experimental) Create CellEvents from a Cell reference.

        :param cell_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df57577472ae02773f619a396eaabfd625c5e9d1de1c07e28cd6aad8dc3f5250)
            check_type(argname="argument cell_ref", value=cell_ref, expected_type=type_hints["cell_ref"])
        return typing.cast("CellEvents", jsii.sinvoke(cls, "fromCell", [cell_ref]))

    @jsii.member(jsii_name="route53ApplicationRecoveryControllerCellReadinessStatusChangePattern")
    def route53_application_recovery_controller_cell_readiness_status_change_pattern(
        self,
        *,
        cell_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        new_state: typing.Optional[typing.Union["CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange.State", typing.Dict[builtins.str, typing.Any]]] = None,
        previous_state: typing.Optional[typing.Union["CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange.State", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Cell Route 53 Application Recovery Controller cell readiness status change.

        :param cell_name: (experimental) cell-name property. Specify an array of string values to match this event if the actual value of cell-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Cell reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param new_state: (experimental) new-state property. Specify an array of string values to match this event if the actual value of new-state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param previous_state: (experimental) previous-state property. Specify an array of string values to match this event if the actual value of previous-state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange.Route53ApplicationRecoveryControllerCellReadinessStatusChangeProps(
            cell_name=cell_name,
            event_metadata=event_metadata,
            new_state=new_state,
            previous_state=previous_state,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "route53ApplicationRecoveryControllerCellReadinessStatusChangePattern", [options]))

    class Route53ApplicationRecoveryControllerCellReadinessStatusChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.events.CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange",
    ):
        '''(experimental) aws.route53recoveryreadiness@Route53ApplicationRecoveryControllerCellReadinessStatusChange event types for Cell.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53recoveryreadiness import events as route53recoveryreadiness_events
            
            route53_application_recovery_controller_cell_readiness_status_change = route53recoveryreadiness_events.CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.events.CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange.Route53ApplicationRecoveryControllerCellReadinessStatusChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "cell_name": "cellName",
                "event_metadata": "eventMetadata",
                "new_state": "newState",
                "previous_state": "previousState",
            },
        )
        class Route53ApplicationRecoveryControllerCellReadinessStatusChangeProps:
            def __init__(
                self,
                *,
                cell_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                new_state: typing.Optional[typing.Union["CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange.State", typing.Dict[builtins.str, typing.Any]]] = None,
                previous_state: typing.Optional[typing.Union["CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange.State", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Props type for Cell aws.route53recoveryreadiness@Route53ApplicationRecoveryControllerCellReadinessStatusChange event.

                :param cell_name: (experimental) cell-name property. Specify an array of string values to match this event if the actual value of cell-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Cell reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param new_state: (experimental) new-state property. Specify an array of string values to match this event if the actual value of new-state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param previous_state: (experimental) previous-state property. Specify an array of string values to match this event if the actual value of previous-state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_route53recoveryreadiness import events as route53recoveryreadiness_events
                    
                    route53_application_recovery_controller_cell_readiness_status_change_props = route53recoveryreadiness_events.CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange.Route53ApplicationRecoveryControllerCellReadinessStatusChangeProps(
                        cell_name=["cellName"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        new_state=route53recoveryreadiness_events.CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange.State(
                            readiness_status=["readinessStatus"]
                        ),
                        previous_state=route53recoveryreadiness_events.CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange.State(
                            readiness_status=["readinessStatus"]
                        )
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(new_state, dict):
                    new_state = CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange.State(**new_state)
                if isinstance(previous_state, dict):
                    previous_state = CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange.State(**previous_state)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__89255c1708da7d4d8e7992ae964b123ec370258ee3d4d0387f57c98740ef3d22)
                    check_type(argname="argument cell_name", value=cell_name, expected_type=type_hints["cell_name"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument new_state", value=new_state, expected_type=type_hints["new_state"])
                    check_type(argname="argument previous_state", value=previous_state, expected_type=type_hints["previous_state"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if cell_name is not None:
                    self._values["cell_name"] = cell_name
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if new_state is not None:
                    self._values["new_state"] = new_state
                if previous_state is not None:
                    self._values["previous_state"] = previous_state

            @builtins.property
            def cell_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) cell-name property.

                Specify an array of string values to match this event if the actual value of cell-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Cell reference

                :stability: experimental
                '''
                result = self._values.get("cell_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_metadata(
                self,
            ) -> typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps]:
                '''(experimental) EventBridge event metadata.

                :default:

                -
                -

                :stability: experimental
                '''
                result = self._values.get("event_metadata")
                return typing.cast(typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps], result)

            @builtins.property
            def new_state(
                self,
            ) -> typing.Optional["CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange.State"]:
                '''(experimental) new-state property.

                Specify an array of string values to match this event if the actual value of new-state is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("new_state")
                return typing.cast(typing.Optional["CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange.State"], result)

            @builtins.property
            def previous_state(
                self,
            ) -> typing.Optional["CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange.State"]:
                '''(experimental) previous-state property.

                Specify an array of string values to match this event if the actual value of previous-state is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("previous_state")
                return typing.cast(typing.Optional["CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange.State"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Route53ApplicationRecoveryControllerCellReadinessStatusChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.events.CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange.State",
            jsii_struct_bases=[],
            name_mapping={"readiness_status": "readinessStatus"},
        )
        class State:
            def __init__(
                self,
                *,
                readiness_status: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for State.

                :param readiness_status: (experimental) readiness-status property. Specify an array of string values to match this event if the actual value of readiness-status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_route53recoveryreadiness import events as route53recoveryreadiness_events
                    
                    state = route53recoveryreadiness_events.CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange.State(
                        readiness_status=["readinessStatus"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__16d6b940d052031a087e88634e8f27899c498abf7708dc9d7994f0038bf43b61)
                    check_type(argname="argument readiness_status", value=readiness_status, expected_type=type_hints["readiness_status"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if readiness_status is not None:
                    self._values["readiness_status"] = readiness_status

            @builtins.property
            def readiness_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) readiness-status property.

                Specify an array of string values to match this event if the actual value of readiness-status is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("readiness_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "State(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


class ReadinessCheckEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.events.ReadinessCheckEvents",
):
    '''(experimental) EventBridge event patterns for ReadinessCheck.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_route53recoveryreadiness import events as route53recoveryreadiness_events
        from aws_cdk.interfaces import aws_route53recoveryreadiness as interfaces_route53recoveryreadiness
        
        # readiness_check_ref: interfaces_route53recoveryreadiness.IReadinessCheckRef
        
        readiness_check_events = route53recoveryreadiness_events.ReadinessCheckEvents.from_readiness_check(readiness_check_ref)
    '''

    @jsii.member(jsii_name="fromReadinessCheck")
    @builtins.classmethod
    def from_readiness_check(
        cls,
        readiness_check_ref: _aws_cdk_interfaces_aws_route53recoveryreadiness_ceddda9d.IReadinessCheckRef,
    ) -> "ReadinessCheckEvents":
        '''(experimental) Create ReadinessCheckEvents from a ReadinessCheck reference.

        :param readiness_check_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10a876190198d9de26334337cf7ac01c4406ac42c22902a968f4f28fdf1632c7)
            check_type(argname="argument readiness_check_ref", value=readiness_check_ref, expected_type=type_hints["readiness_check_ref"])
        return typing.cast("ReadinessCheckEvents", jsii.sinvoke(cls, "fromReadinessCheck", [readiness_check_ref]))

    @jsii.member(jsii_name="route53ApplicationRecoveryControllerReadinessCheckStatusChangePattern")
    def route53_application_recovery_controller_readiness_check_status_change_pattern(
        self,
        *,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        new_state: typing.Optional[typing.Union["ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange.State", typing.Dict[builtins.str, typing.Any]]] = None,
        previous_state: typing.Optional[typing.Union["ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange.State", typing.Dict[builtins.str, typing.Any]]] = None,
        readiness_check_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for ReadinessCheck Route 53 Application Recovery Controller readiness check status change.

        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param new_state: (experimental) new-state property. Specify an array of string values to match this event if the actual value of new-state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param previous_state: (experimental) previous-state property. Specify an array of string values to match this event if the actual value of previous-state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param readiness_check_name: (experimental) readiness-check-name property. Specify an array of string values to match this event if the actual value of readiness-check-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the ReadinessCheck reference

        :stability: experimental
        '''
        options = ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange.Route53ApplicationRecoveryControllerReadinessCheckStatusChangeProps(
            event_metadata=event_metadata,
            new_state=new_state,
            previous_state=previous_state,
            readiness_check_name=readiness_check_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "route53ApplicationRecoveryControllerReadinessCheckStatusChangePattern", [options]))

    class Route53ApplicationRecoveryControllerReadinessCheckStatusChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.events.ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange",
    ):
        '''(experimental) aws.route53recoveryreadiness@Route53ApplicationRecoveryControllerReadinessCheckStatusChange event types for ReadinessCheck.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53recoveryreadiness import events as route53recoveryreadiness_events
            
            route53_application_recovery_controller_readiness_check_status_change = route53recoveryreadiness_events.ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.events.ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange.Route53ApplicationRecoveryControllerReadinessCheckStatusChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "event_metadata": "eventMetadata",
                "new_state": "newState",
                "previous_state": "previousState",
                "readiness_check_name": "readinessCheckName",
            },
        )
        class Route53ApplicationRecoveryControllerReadinessCheckStatusChangeProps:
            def __init__(
                self,
                *,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                new_state: typing.Optional[typing.Union["ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange.State", typing.Dict[builtins.str, typing.Any]]] = None,
                previous_state: typing.Optional[typing.Union["ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange.State", typing.Dict[builtins.str, typing.Any]]] = None,
                readiness_check_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for ReadinessCheck aws.route53recoveryreadiness@Route53ApplicationRecoveryControllerReadinessCheckStatusChange event.

                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param new_state: (experimental) new-state property. Specify an array of string values to match this event if the actual value of new-state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param previous_state: (experimental) previous-state property. Specify an array of string values to match this event if the actual value of previous-state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param readiness_check_name: (experimental) readiness-check-name property. Specify an array of string values to match this event if the actual value of readiness-check-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the ReadinessCheck reference

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_route53recoveryreadiness import events as route53recoveryreadiness_events
                    
                    route53_application_recovery_controller_readiness_check_status_change_props = route53recoveryreadiness_events.ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange.Route53ApplicationRecoveryControllerReadinessCheckStatusChangeProps(
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        new_state=route53recoveryreadiness_events.ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange.State(
                            readiness_status=["readinessStatus"]
                        ),
                        previous_state=route53recoveryreadiness_events.ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange.State(
                            readiness_status=["readinessStatus"]
                        ),
                        readiness_check_name=["readinessCheckName"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(new_state, dict):
                    new_state = ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange.State(**new_state)
                if isinstance(previous_state, dict):
                    previous_state = ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange.State(**previous_state)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__a2eb8bead577a911decd291412ccd7b9daffcc431023fca131df41e36c8bb504)
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument new_state", value=new_state, expected_type=type_hints["new_state"])
                    check_type(argname="argument previous_state", value=previous_state, expected_type=type_hints["previous_state"])
                    check_type(argname="argument readiness_check_name", value=readiness_check_name, expected_type=type_hints["readiness_check_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if new_state is not None:
                    self._values["new_state"] = new_state
                if previous_state is not None:
                    self._values["previous_state"] = previous_state
                if readiness_check_name is not None:
                    self._values["readiness_check_name"] = readiness_check_name

            @builtins.property
            def event_metadata(
                self,
            ) -> typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps]:
                '''(experimental) EventBridge event metadata.

                :default:

                -
                -

                :stability: experimental
                '''
                result = self._values.get("event_metadata")
                return typing.cast(typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps], result)

            @builtins.property
            def new_state(
                self,
            ) -> typing.Optional["ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange.State"]:
                '''(experimental) new-state property.

                Specify an array of string values to match this event if the actual value of new-state is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("new_state")
                return typing.cast(typing.Optional["ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange.State"], result)

            @builtins.property
            def previous_state(
                self,
            ) -> typing.Optional["ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange.State"]:
                '''(experimental) previous-state property.

                Specify an array of string values to match this event if the actual value of previous-state is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("previous_state")
                return typing.cast(typing.Optional["ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange.State"], result)

            @builtins.property
            def readiness_check_name(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) readiness-check-name property.

                Specify an array of string values to match this event if the actual value of readiness-check-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the ReadinessCheck reference

                :stability: experimental
                '''
                result = self._values.get("readiness_check_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Route53ApplicationRecoveryControllerReadinessCheckStatusChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.events.ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange.State",
            jsii_struct_bases=[],
            name_mapping={"readiness_status": "readinessStatus"},
        )
        class State:
            def __init__(
                self,
                *,
                readiness_status: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for State.

                :param readiness_status: (experimental) readiness-status property. Specify an array of string values to match this event if the actual value of readiness-status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_route53recoveryreadiness import events as route53recoveryreadiness_events
                    
                    state = route53recoveryreadiness_events.ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange.State(
                        readiness_status=["readinessStatus"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__aac8d2d4a5cd91febec462ee851fdbd5c9aeed5bf25091dd78faf73cf57b0a5f)
                    check_type(argname="argument readiness_status", value=readiness_status, expected_type=type_hints["readiness_status"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if readiness_status is not None:
                    self._values["readiness_status"] = readiness_status

            @builtins.property
            def readiness_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) readiness-status property.

                Specify an array of string values to match this event if the actual value of readiness-status is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("readiness_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "State(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


class RecoveryGroupEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.events.RecoveryGroupEvents",
):
    '''(experimental) EventBridge event patterns for RecoveryGroup.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_route53recoveryreadiness import events as route53recoveryreadiness_events
        from aws_cdk.interfaces import aws_route53recoveryreadiness as interfaces_route53recoveryreadiness
        
        # recovery_group_ref: interfaces_route53recoveryreadiness.IRecoveryGroupRef
        
        recovery_group_events = route53recoveryreadiness_events.RecoveryGroupEvents.from_recovery_group(recovery_group_ref)
    '''

    @jsii.member(jsii_name="fromRecoveryGroup")
    @builtins.classmethod
    def from_recovery_group(
        cls,
        recovery_group_ref: _aws_cdk_interfaces_aws_route53recoveryreadiness_ceddda9d.IRecoveryGroupRef,
    ) -> "RecoveryGroupEvents":
        '''(experimental) Create RecoveryGroupEvents from a RecoveryGroup reference.

        :param recovery_group_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb774a8a207cc4aedb3b8b5a8389935c923ae79d25bbfbd067883dc61b773c43)
            check_type(argname="argument recovery_group_ref", value=recovery_group_ref, expected_type=type_hints["recovery_group_ref"])
        return typing.cast("RecoveryGroupEvents", jsii.sinvoke(cls, "fromRecoveryGroup", [recovery_group_ref]))

    @jsii.member(jsii_name="route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChangePattern")
    def route53_application_recovery_controller_recovery_group_readiness_status_change_pattern(
        self,
        *,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        new_state: typing.Optional[typing.Union["RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange.State", typing.Dict[builtins.str, typing.Any]]] = None,
        previous_state: typing.Optional[typing.Union["RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange.State", typing.Dict[builtins.str, typing.Any]]] = None,
        recovery_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for RecoveryGroup Route 53 Application Recovery Controller recovery group readiness status change.

        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param new_state: (experimental) new-state property. Specify an array of string values to match this event if the actual value of new-state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param previous_state: (experimental) previous-state property. Specify an array of string values to match this event if the actual value of previous-state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param recovery_group_name: (experimental) recovery-group-name property. Specify an array of string values to match this event if the actual value of recovery-group-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the RecoveryGroup reference

        :stability: experimental
        '''
        options = RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChangeProps(
            event_metadata=event_metadata,
            new_state=new_state,
            previous_state=previous_state,
            recovery_group_name=recovery_group_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChangePattern", [options]))

    class Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.events.RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange",
    ):
        '''(experimental) aws.route53recoveryreadiness@Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange event types for RecoveryGroup.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_route53recoveryreadiness import events as route53recoveryreadiness_events
            
            route53_application_recovery_controller_recovery_group_readiness_status_change = route53recoveryreadiness_events.RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.events.RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "event_metadata": "eventMetadata",
                "new_state": "newState",
                "previous_state": "previousState",
                "recovery_group_name": "recoveryGroupName",
            },
        )
        class Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChangeProps:
            def __init__(
                self,
                *,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                new_state: typing.Optional[typing.Union["RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange.State", typing.Dict[builtins.str, typing.Any]]] = None,
                previous_state: typing.Optional[typing.Union["RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange.State", typing.Dict[builtins.str, typing.Any]]] = None,
                recovery_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for RecoveryGroup aws.route53recoveryreadiness@Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange event.

                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param new_state: (experimental) new-state property. Specify an array of string values to match this event if the actual value of new-state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param previous_state: (experimental) previous-state property. Specify an array of string values to match this event if the actual value of previous-state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param recovery_group_name: (experimental) recovery-group-name property. Specify an array of string values to match this event if the actual value of recovery-group-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the RecoveryGroup reference

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_route53recoveryreadiness import events as route53recoveryreadiness_events
                    
                    route53_application_recovery_controller_recovery_group_readiness_status_change_props = route53recoveryreadiness_events.RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChangeProps(
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        new_state=route53recoveryreadiness_events.RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange.State(
                            readiness_status=["readinessStatus"]
                        ),
                        previous_state=route53recoveryreadiness_events.RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange.State(
                            readiness_status=["readinessStatus"]
                        ),
                        recovery_group_name=["recoveryGroupName"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(new_state, dict):
                    new_state = RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange.State(**new_state)
                if isinstance(previous_state, dict):
                    previous_state = RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange.State(**previous_state)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__4b04818524e3d3a94cbd8e1760497e11cf7fa00c533fa788b94c25c6124e4366)
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument new_state", value=new_state, expected_type=type_hints["new_state"])
                    check_type(argname="argument previous_state", value=previous_state, expected_type=type_hints["previous_state"])
                    check_type(argname="argument recovery_group_name", value=recovery_group_name, expected_type=type_hints["recovery_group_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if new_state is not None:
                    self._values["new_state"] = new_state
                if previous_state is not None:
                    self._values["previous_state"] = previous_state
                if recovery_group_name is not None:
                    self._values["recovery_group_name"] = recovery_group_name

            @builtins.property
            def event_metadata(
                self,
            ) -> typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps]:
                '''(experimental) EventBridge event metadata.

                :default:

                -
                -

                :stability: experimental
                '''
                result = self._values.get("event_metadata")
                return typing.cast(typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps], result)

            @builtins.property
            def new_state(
                self,
            ) -> typing.Optional["RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange.State"]:
                '''(experimental) new-state property.

                Specify an array of string values to match this event if the actual value of new-state is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("new_state")
                return typing.cast(typing.Optional["RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange.State"], result)

            @builtins.property
            def previous_state(
                self,
            ) -> typing.Optional["RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange.State"]:
                '''(experimental) previous-state property.

                Specify an array of string values to match this event if the actual value of previous-state is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("previous_state")
                return typing.cast(typing.Optional["RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange.State"], result)

            @builtins.property
            def recovery_group_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) recovery-group-name property.

                Specify an array of string values to match this event if the actual value of recovery-group-name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the RecoveryGroup reference

                :stability: experimental
                '''
                result = self._values.get("recovery_group_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_route53recoveryreadiness.events.RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange.State",
            jsii_struct_bases=[],
            name_mapping={"readiness_status": "readinessStatus"},
        )
        class State:
            def __init__(
                self,
                *,
                readiness_status: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for State.

                :param readiness_status: (experimental) readiness-status property. Specify an array of string values to match this event if the actual value of readiness-status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_route53recoveryreadiness import events as route53recoveryreadiness_events
                    
                    state = route53recoveryreadiness_events.RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange.State(
                        readiness_status=["readinessStatus"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__47d90d0fa6cfa7bdcb396b94c15eae83d661da5b250d88b1332825c1e99dc333)
                    check_type(argname="argument readiness_status", value=readiness_status, expected_type=type_hints["readiness_status"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if readiness_status is not None:
                    self._values["readiness_status"] = readiness_status

            @builtins.property
            def readiness_status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) readiness-status property.

                Specify an array of string values to match this event if the actual value of readiness-status is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("readiness_status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "State(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "CellEvents",
    "ReadinessCheckEvents",
    "RecoveryGroupEvents",
]

publication.publish()

def _typecheckingstub__df57577472ae02773f619a396eaabfd625c5e9d1de1c07e28cd6aad8dc3f5250(
    cell_ref: _aws_cdk_interfaces_aws_route53recoveryreadiness_ceddda9d.ICellRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89255c1708da7d4d8e7992ae964b123ec370258ee3d4d0387f57c98740ef3d22(
    *,
    cell_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    new_state: typing.Optional[typing.Union[CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange.State, typing.Dict[builtins.str, typing.Any]]] = None,
    previous_state: typing.Optional[typing.Union[CellEvents.Route53ApplicationRecoveryControllerCellReadinessStatusChange.State, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d6b940d052031a087e88634e8f27899c498abf7708dc9d7994f0038bf43b61(
    *,
    readiness_status: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a876190198d9de26334337cf7ac01c4406ac42c22902a968f4f28fdf1632c7(
    readiness_check_ref: _aws_cdk_interfaces_aws_route53recoveryreadiness_ceddda9d.IReadinessCheckRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2eb8bead577a911decd291412ccd7b9daffcc431023fca131df41e36c8bb504(
    *,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    new_state: typing.Optional[typing.Union[ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange.State, typing.Dict[builtins.str, typing.Any]]] = None,
    previous_state: typing.Optional[typing.Union[ReadinessCheckEvents.Route53ApplicationRecoveryControllerReadinessCheckStatusChange.State, typing.Dict[builtins.str, typing.Any]]] = None,
    readiness_check_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac8d2d4a5cd91febec462ee851fdbd5c9aeed5bf25091dd78faf73cf57b0a5f(
    *,
    readiness_status: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb774a8a207cc4aedb3b8b5a8389935c923ae79d25bbfbd067883dc61b773c43(
    recovery_group_ref: _aws_cdk_interfaces_aws_route53recoveryreadiness_ceddda9d.IRecoveryGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b04818524e3d3a94cbd8e1760497e11cf7fa00c533fa788b94c25c6124e4366(
    *,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    new_state: typing.Optional[typing.Union[RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange.State, typing.Dict[builtins.str, typing.Any]]] = None,
    previous_state: typing.Optional[typing.Union[RecoveryGroupEvents.Route53ApplicationRecoveryControllerRecoveryGroupReadinessStatusChange.State, typing.Dict[builtins.str, typing.Any]]] = None,
    recovery_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47d90d0fa6cfa7bdcb396b94c15eae83d661da5b250d88b1332825c1e99dc333(
    *,
    readiness_status: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
