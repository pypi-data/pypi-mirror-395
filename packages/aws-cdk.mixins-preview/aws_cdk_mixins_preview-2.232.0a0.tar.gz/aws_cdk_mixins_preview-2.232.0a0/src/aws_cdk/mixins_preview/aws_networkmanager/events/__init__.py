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
import aws_cdk.interfaces.aws_networkmanager as _aws_cdk_interfaces_aws_networkmanager_ceddda9d


class CoreNetworkEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.events.CoreNetworkEvents",
):
    '''(experimental) EventBridge event patterns for CoreNetwork.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_networkmanager import events as networkmanager_events
        from aws_cdk.interfaces import aws_networkmanager as interfaces_networkmanager
        
        # core_network_ref: interfaces_networkmanager.ICoreNetworkRef
        
        core_network_events = networkmanager_events.CoreNetworkEvents.from_core_network(core_network_ref)
    '''

    @jsii.member(jsii_name="fromCoreNetwork")
    @builtins.classmethod
    def from_core_network(
        cls,
        core_network_ref: _aws_cdk_interfaces_aws_networkmanager_ceddda9d.ICoreNetworkRef,
    ) -> "CoreNetworkEvents":
        '''(experimental) Create CoreNetworkEvents from a CoreNetwork reference.

        :param core_network_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05bde8df55f6a491e54a2b9df26da7c107f163640d4e977dd90a2c2728eb4669)
            check_type(argname="argument core_network_ref", value=core_network_ref, expected_type=type_hints["core_network_ref"])
        return typing.cast("CoreNetworkEvents", jsii.sinvoke(cls, "fromCoreNetwork", [core_network_ref]))

    @jsii.member(jsii_name="networkManagerPolicyUpdatePattern")
    def network_manager_policy_update_pattern(
        self,
        *,
        change_description: typing.Optional[typing.Sequence[builtins.str]] = None,
        change_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        core_network_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        policy_version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for CoreNetwork Network Manager Policy Update.

        :param change_description: (experimental) changeDescription property. Specify an array of string values to match this event if the actual value of changeDescription is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param change_type: (experimental) changeType property. Specify an array of string values to match this event if the actual value of changeType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param core_network_arn: (experimental) coreNetworkArn property. Specify an array of string values to match this event if the actual value of coreNetworkArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the CoreNetwork reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param policy_version_id: (experimental) policyVersionId property. Specify an array of string values to match this event if the actual value of policyVersionId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = CoreNetworkEvents.NetworkManagerPolicyUpdate.NetworkManagerPolicyUpdateProps(
            change_description=change_description,
            change_type=change_type,
            core_network_arn=core_network_arn,
            event_metadata=event_metadata,
            policy_version_id=policy_version_id,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "networkManagerPolicyUpdatePattern", [options]))

    @jsii.member(jsii_name="networkManagerSegmentUpdatePattern")
    def network_manager_segment_update_pattern(
        self,
        *,
        attachment_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        change_description: typing.Optional[typing.Sequence[builtins.str]] = None,
        change_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        core_network_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        edge_location: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        network_function_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        new_network_function_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        new_segment_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        previous_network_function_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        previous_segment_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        segment_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for CoreNetwork Network Manager Segment Update.

        :param attachment_arn: (experimental) attachmentArn property. Specify an array of string values to match this event if the actual value of attachmentArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param change_description: (experimental) changeDescription property. Specify an array of string values to match this event if the actual value of changeDescription is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param change_type: (experimental) changeType property. Specify an array of string values to match this event if the actual value of changeType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param core_network_arn: (experimental) coreNetworkArn property. Specify an array of string values to match this event if the actual value of coreNetworkArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the CoreNetwork reference
        :param edge_location: (experimental) edgeLocation property. Specify an array of string values to match this event if the actual value of edgeLocation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param network_function_group_name: (experimental) networkFunctionGroupName property. Specify an array of string values to match this event if the actual value of networkFunctionGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param new_network_function_group_name: (experimental) newNetworkFunctionGroupName property. Specify an array of string values to match this event if the actual value of newNetworkFunctionGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param new_segment_name: (experimental) newSegmentName property. Specify an array of string values to match this event if the actual value of newSegmentName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param previous_network_function_group_name: (experimental) previousNetworkFunctionGroupName property. Specify an array of string values to match this event if the actual value of previousNetworkFunctionGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param previous_segment_name: (experimental) previousSegmentName property. Specify an array of string values to match this event if the actual value of previousSegmentName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param segment_name: (experimental) segmentName property. Specify an array of string values to match this event if the actual value of segmentName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = CoreNetworkEvents.NetworkManagerSegmentUpdate.NetworkManagerSegmentUpdateProps(
            attachment_arn=attachment_arn,
            change_description=change_description,
            change_type=change_type,
            core_network_arn=core_network_arn,
            edge_location=edge_location,
            event_metadata=event_metadata,
            network_function_group_name=network_function_group_name,
            new_network_function_group_name=new_network_function_group_name,
            new_segment_name=new_segment_name,
            previous_network_function_group_name=previous_network_function_group_name,
            previous_segment_name=previous_segment_name,
            segment_name=segment_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "networkManagerSegmentUpdatePattern", [options]))

    class NetworkManagerPolicyUpdate(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.events.CoreNetworkEvents.NetworkManagerPolicyUpdate",
    ):
        '''(experimental) aws.networkmanager@NetworkManagerPolicyUpdate event types for CoreNetwork.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkmanager import events as networkmanager_events
            
            network_manager_policy_update = networkmanager_events.CoreNetworkEvents.NetworkManagerPolicyUpdate()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.events.CoreNetworkEvents.NetworkManagerPolicyUpdate.NetworkManagerPolicyUpdateProps",
            jsii_struct_bases=[],
            name_mapping={
                "change_description": "changeDescription",
                "change_type": "changeType",
                "core_network_arn": "coreNetworkArn",
                "event_metadata": "eventMetadata",
                "policy_version_id": "policyVersionId",
            },
        )
        class NetworkManagerPolicyUpdateProps:
            def __init__(
                self,
                *,
                change_description: typing.Optional[typing.Sequence[builtins.str]] = None,
                change_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                core_network_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                policy_version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for CoreNetwork aws.networkmanager@NetworkManagerPolicyUpdate event.

                :param change_description: (experimental) changeDescription property. Specify an array of string values to match this event if the actual value of changeDescription is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param change_type: (experimental) changeType property. Specify an array of string values to match this event if the actual value of changeType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param core_network_arn: (experimental) coreNetworkArn property. Specify an array of string values to match this event if the actual value of coreNetworkArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the CoreNetwork reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param policy_version_id: (experimental) policyVersionId property. Specify an array of string values to match this event if the actual value of policyVersionId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_networkmanager import events as networkmanager_events
                    
                    network_manager_policy_update_props = networkmanager_events.CoreNetworkEvents.NetworkManagerPolicyUpdate.NetworkManagerPolicyUpdateProps(
                        change_description=["changeDescription"],
                        change_type=["changeType"],
                        core_network_arn=["coreNetworkArn"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        policy_version_id=["policyVersionId"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__1dcd2b299d17a232954fbe4d760cafe1ca0619e5c2105df9cd1f7b5730a0d08b)
                    check_type(argname="argument change_description", value=change_description, expected_type=type_hints["change_description"])
                    check_type(argname="argument change_type", value=change_type, expected_type=type_hints["change_type"])
                    check_type(argname="argument core_network_arn", value=core_network_arn, expected_type=type_hints["core_network_arn"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument policy_version_id", value=policy_version_id, expected_type=type_hints["policy_version_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if change_description is not None:
                    self._values["change_description"] = change_description
                if change_type is not None:
                    self._values["change_type"] = change_type
                if core_network_arn is not None:
                    self._values["core_network_arn"] = core_network_arn
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if policy_version_id is not None:
                    self._values["policy_version_id"] = policy_version_id

            @builtins.property
            def change_description(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) changeDescription property.

                Specify an array of string values to match this event if the actual value of changeDescription is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("change_description")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def change_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) changeType property.

                Specify an array of string values to match this event if the actual value of changeType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("change_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def core_network_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) coreNetworkArn property.

                Specify an array of string values to match this event if the actual value of coreNetworkArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the CoreNetwork reference

                :stability: experimental
                '''
                result = self._values.get("core_network_arn")
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
            def policy_version_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) policyVersionId property.

                Specify an array of string values to match this event if the actual value of policyVersionId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("policy_version_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "NetworkManagerPolicyUpdateProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class NetworkManagerSegmentUpdate(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.events.CoreNetworkEvents.NetworkManagerSegmentUpdate",
    ):
        '''(experimental) aws.networkmanager@NetworkManagerSegmentUpdate event types for CoreNetwork.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkmanager import events as networkmanager_events
            
            network_manager_segment_update = networkmanager_events.CoreNetworkEvents.NetworkManagerSegmentUpdate()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.events.CoreNetworkEvents.NetworkManagerSegmentUpdate.NetworkManagerSegmentUpdateProps",
            jsii_struct_bases=[],
            name_mapping={
                "attachment_arn": "attachmentArn",
                "change_description": "changeDescription",
                "change_type": "changeType",
                "core_network_arn": "coreNetworkArn",
                "edge_location": "edgeLocation",
                "event_metadata": "eventMetadata",
                "network_function_group_name": "networkFunctionGroupName",
                "new_network_function_group_name": "newNetworkFunctionGroupName",
                "new_segment_name": "newSegmentName",
                "previous_network_function_group_name": "previousNetworkFunctionGroupName",
                "previous_segment_name": "previousSegmentName",
                "segment_name": "segmentName",
            },
        )
        class NetworkManagerSegmentUpdateProps:
            def __init__(
                self,
                *,
                attachment_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                change_description: typing.Optional[typing.Sequence[builtins.str]] = None,
                change_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                core_network_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                edge_location: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                network_function_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                new_network_function_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                new_segment_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                previous_network_function_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                previous_segment_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                segment_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for CoreNetwork aws.networkmanager@NetworkManagerSegmentUpdate event.

                :param attachment_arn: (experimental) attachmentArn property. Specify an array of string values to match this event if the actual value of attachmentArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param change_description: (experimental) changeDescription property. Specify an array of string values to match this event if the actual value of changeDescription is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param change_type: (experimental) changeType property. Specify an array of string values to match this event if the actual value of changeType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param core_network_arn: (experimental) coreNetworkArn property. Specify an array of string values to match this event if the actual value of coreNetworkArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the CoreNetwork reference
                :param edge_location: (experimental) edgeLocation property. Specify an array of string values to match this event if the actual value of edgeLocation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param network_function_group_name: (experimental) networkFunctionGroupName property. Specify an array of string values to match this event if the actual value of networkFunctionGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param new_network_function_group_name: (experimental) newNetworkFunctionGroupName property. Specify an array of string values to match this event if the actual value of newNetworkFunctionGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param new_segment_name: (experimental) newSegmentName property. Specify an array of string values to match this event if the actual value of newSegmentName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param previous_network_function_group_name: (experimental) previousNetworkFunctionGroupName property. Specify an array of string values to match this event if the actual value of previousNetworkFunctionGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param previous_segment_name: (experimental) previousSegmentName property. Specify an array of string values to match this event if the actual value of previousSegmentName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param segment_name: (experimental) segmentName property. Specify an array of string values to match this event if the actual value of segmentName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_networkmanager import events as networkmanager_events
                    
                    network_manager_segment_update_props = networkmanager_events.CoreNetworkEvents.NetworkManagerSegmentUpdate.NetworkManagerSegmentUpdateProps(
                        attachment_arn=["attachmentArn"],
                        change_description=["changeDescription"],
                        change_type=["changeType"],
                        core_network_arn=["coreNetworkArn"],
                        edge_location=["edgeLocation"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        network_function_group_name=["networkFunctionGroupName"],
                        new_network_function_group_name=["newNetworkFunctionGroupName"],
                        new_segment_name=["newSegmentName"],
                        previous_network_function_group_name=["previousNetworkFunctionGroupName"],
                        previous_segment_name=["previousSegmentName"],
                        segment_name=["segmentName"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__febac10ff39bceb523149f98835177b5a3e7b37341b62c86fbff968bfd9283f1)
                    check_type(argname="argument attachment_arn", value=attachment_arn, expected_type=type_hints["attachment_arn"])
                    check_type(argname="argument change_description", value=change_description, expected_type=type_hints["change_description"])
                    check_type(argname="argument change_type", value=change_type, expected_type=type_hints["change_type"])
                    check_type(argname="argument core_network_arn", value=core_network_arn, expected_type=type_hints["core_network_arn"])
                    check_type(argname="argument edge_location", value=edge_location, expected_type=type_hints["edge_location"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument network_function_group_name", value=network_function_group_name, expected_type=type_hints["network_function_group_name"])
                    check_type(argname="argument new_network_function_group_name", value=new_network_function_group_name, expected_type=type_hints["new_network_function_group_name"])
                    check_type(argname="argument new_segment_name", value=new_segment_name, expected_type=type_hints["new_segment_name"])
                    check_type(argname="argument previous_network_function_group_name", value=previous_network_function_group_name, expected_type=type_hints["previous_network_function_group_name"])
                    check_type(argname="argument previous_segment_name", value=previous_segment_name, expected_type=type_hints["previous_segment_name"])
                    check_type(argname="argument segment_name", value=segment_name, expected_type=type_hints["segment_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if attachment_arn is not None:
                    self._values["attachment_arn"] = attachment_arn
                if change_description is not None:
                    self._values["change_description"] = change_description
                if change_type is not None:
                    self._values["change_type"] = change_type
                if core_network_arn is not None:
                    self._values["core_network_arn"] = core_network_arn
                if edge_location is not None:
                    self._values["edge_location"] = edge_location
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if network_function_group_name is not None:
                    self._values["network_function_group_name"] = network_function_group_name
                if new_network_function_group_name is not None:
                    self._values["new_network_function_group_name"] = new_network_function_group_name
                if new_segment_name is not None:
                    self._values["new_segment_name"] = new_segment_name
                if previous_network_function_group_name is not None:
                    self._values["previous_network_function_group_name"] = previous_network_function_group_name
                if previous_segment_name is not None:
                    self._values["previous_segment_name"] = previous_segment_name
                if segment_name is not None:
                    self._values["segment_name"] = segment_name

            @builtins.property
            def attachment_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) attachmentArn property.

                Specify an array of string values to match this event if the actual value of attachmentArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("attachment_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def change_description(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) changeDescription property.

                Specify an array of string values to match this event if the actual value of changeDescription is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("change_description")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def change_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) changeType property.

                Specify an array of string values to match this event if the actual value of changeType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("change_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def core_network_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) coreNetworkArn property.

                Specify an array of string values to match this event if the actual value of coreNetworkArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the CoreNetwork reference

                :stability: experimental
                '''
                result = self._values.get("core_network_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def edge_location(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) edgeLocation property.

                Specify an array of string values to match this event if the actual value of edgeLocation is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("edge_location")
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
            def network_function_group_name(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) networkFunctionGroupName property.

                Specify an array of string values to match this event if the actual value of networkFunctionGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("network_function_group_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def new_network_function_group_name(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) newNetworkFunctionGroupName property.

                Specify an array of string values to match this event if the actual value of newNetworkFunctionGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("new_network_function_group_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def new_segment_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) newSegmentName property.

                Specify an array of string values to match this event if the actual value of newSegmentName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("new_segment_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def previous_network_function_group_name(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) previousNetworkFunctionGroupName property.

                Specify an array of string values to match this event if the actual value of previousNetworkFunctionGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("previous_network_function_group_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def previous_segment_name(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) previousSegmentName property.

                Specify an array of string values to match this event if the actual value of previousSegmentName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("previous_segment_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def segment_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) segmentName property.

                Specify an array of string values to match this event if the actual value of segmentName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("segment_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "NetworkManagerSegmentUpdateProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "CoreNetworkEvents",
]

publication.publish()

def _typecheckingstub__05bde8df55f6a491e54a2b9df26da7c107f163640d4e977dd90a2c2728eb4669(
    core_network_ref: _aws_cdk_interfaces_aws_networkmanager_ceddda9d.ICoreNetworkRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dcd2b299d17a232954fbe4d760cafe1ca0619e5c2105df9cd1f7b5730a0d08b(
    *,
    change_description: typing.Optional[typing.Sequence[builtins.str]] = None,
    change_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    core_network_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    policy_version_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__febac10ff39bceb523149f98835177b5a3e7b37341b62c86fbff968bfd9283f1(
    *,
    attachment_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    change_description: typing.Optional[typing.Sequence[builtins.str]] = None,
    change_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    core_network_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    edge_location: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    network_function_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    new_network_function_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    new_segment_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    previous_network_function_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    previous_segment_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    segment_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
