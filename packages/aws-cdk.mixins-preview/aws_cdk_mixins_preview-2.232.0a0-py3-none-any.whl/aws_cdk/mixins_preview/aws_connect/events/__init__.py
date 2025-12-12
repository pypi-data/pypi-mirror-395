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
import aws_cdk.interfaces.aws_connect as _aws_cdk_interfaces_aws_connect_ceddda9d


class InstanceEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.events.InstanceEvents",
):
    '''(experimental) EventBridge event patterns for Instance.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_connect import events as connect_events
        from aws_cdk.interfaces import aws_connect as interfaces_connect
        
        # instance_ref: interfaces_connect.IInstanceRef
        
        instance_events = connect_events.InstanceEvents.from_instance(instance_ref)
    '''

    @jsii.member(jsii_name="fromInstance")
    @builtins.classmethod
    def from_instance(
        cls,
        instance_ref: _aws_cdk_interfaces_aws_connect_ceddda9d.IInstanceRef,
    ) -> "InstanceEvents":
        '''(experimental) Create InstanceEvents from a Instance reference.

        :param instance_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a6f14fffbee0d4e1c88aa93635443b38c0f2f5a5f2bf5182efcea94b8c9b90f)
            check_type(argname="argument instance_ref", value=instance_ref, expected_type=type_hints["instance_ref"])
        return typing.cast("InstanceEvents", jsii.sinvoke(cls, "fromInstance", [instance_ref]))

    @jsii.member(jsii_name="codeConnectContactPattern")
    def code_connect_contact_pattern(
        self,
        *,
        agent_info: typing.Optional[typing.Union["InstanceEvents.CodeConnectContact.AgentInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        channel: typing.Optional[typing.Sequence[builtins.str]] = None,
        contact_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        initial_contact_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        initiation_method: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        previous_contact_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        queue_info: typing.Optional[typing.Union["InstanceEvents.CodeConnectContact.QueueInfo", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Instance Amazon Connect Contact Event.

        :param agent_info: (experimental) agentInfo property. Specify an array of string values to match this event if the actual value of agentInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param channel: (experimental) channel property. Specify an array of string values to match this event if the actual value of channel is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param contact_id: (experimental) contactId property. Specify an array of string values to match this event if the actual value of contactId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param event_type: (experimental) eventType property. Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param initial_contact_id: (experimental) initialContactId property. Specify an array of string values to match this event if the actual value of initialContactId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param initiation_method: (experimental) initiationMethod property. Specify an array of string values to match this event if the actual value of initiationMethod is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param instance_arn: (experimental) instanceArn property. Specify an array of string values to match this event if the actual value of instanceArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Instance reference
        :param previous_contact_id: (experimental) previousContactId property. Specify an array of string values to match this event if the actual value of previousContactId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param queue_info: (experimental) queueInfo property. Specify an array of string values to match this event if the actual value of queueInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = InstanceEvents.CodeConnectContact.CodeConnectContactProps(
            agent_info=agent_info,
            channel=channel,
            contact_id=contact_id,
            event_metadata=event_metadata,
            event_type=event_type,
            initial_contact_id=initial_contact_id,
            initiation_method=initiation_method,
            instance_arn=instance_arn,
            previous_contact_id=previous_contact_id,
            queue_info=queue_info,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "codeConnectContactPattern", [options]))

    @jsii.member(jsii_name="contactLensPostCallRulesMatchedPattern")
    def contact_lens_post_call_rules_matched_pattern(
        self,
        *,
        action_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        agent_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        contact_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        instance_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        queue_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        rule_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Instance Contact Lens Post Call Rules Matched.

        :param action_name: (experimental) actionName property. Specify an array of string values to match this event if the actual value of actionName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param agent_arn: (experimental) agentArn property. Specify an array of string values to match this event if the actual value of agentArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param contact_arn: (experimental) contactArn property. Specify an array of string values to match this event if the actual value of contactArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param instance_arn: (experimental) instanceArn property. Specify an array of string values to match this event if the actual value of instanceArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Instance reference
        :param queue_arn: (experimental) queueArn property. Specify an array of string values to match this event if the actual value of queueArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param rule_name: (experimental) ruleName property. Specify an array of string values to match this event if the actual value of ruleName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = InstanceEvents.ContactLensPostCallRulesMatched.ContactLensPostCallRulesMatchedProps(
            action_name=action_name,
            agent_arn=agent_arn,
            contact_arn=contact_arn,
            event_metadata=event_metadata,
            instance_arn=instance_arn,
            queue_arn=queue_arn,
            rule_name=rule_name,
            version=version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "contactLensPostCallRulesMatchedPattern", [options]))

    @jsii.member(jsii_name="contactLensRealtimeRulesMatchedPattern")
    def contact_lens_realtime_rules_matched_pattern(
        self,
        *,
        action_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        agent_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        contact_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        instance_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        queue_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        rule_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Instance Contact Lens Realtime Rules Matched.

        :param action_name: (experimental) actionName property. Specify an array of string values to match this event if the actual value of actionName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param agent_arn: (experimental) agentArn property. Specify an array of string values to match this event if the actual value of agentArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param contact_arn: (experimental) contactArn property. Specify an array of string values to match this event if the actual value of contactArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param instance_arn: (experimental) instanceArn property. Specify an array of string values to match this event if the actual value of instanceArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Instance reference
        :param queue_arn: (experimental) queueArn property. Specify an array of string values to match this event if the actual value of queueArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param rule_name: (experimental) ruleName property. Specify an array of string values to match this event if the actual value of ruleName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = InstanceEvents.ContactLensRealtimeRulesMatched.ContactLensRealtimeRulesMatchedProps(
            action_name=action_name,
            agent_arn=agent_arn,
            contact_arn=contact_arn,
            event_metadata=event_metadata,
            instance_arn=instance_arn,
            queue_arn=queue_arn,
            rule_name=rule_name,
            version=version,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "contactLensRealtimeRulesMatchedPattern", [options]))

    class CodeConnectContact(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_connect.events.InstanceEvents.CodeConnectContact",
    ):
        '''(experimental) aws.connect@CodeConnectContact event types for Instance.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import events as connect_events
            
            code_connect_contact = connect_events.InstanceEvents.CodeConnectContact()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_connect.events.InstanceEvents.CodeConnectContact.AgentInfo",
            jsii_struct_bases=[],
            name_mapping={"agent_arn": "agentArn"},
        )
        class AgentInfo:
            def __init__(
                self,
                *,
                agent_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AgentInfo.

                :param agent_arn: (experimental) agentArn property. Specify an array of string values to match this event if the actual value of agentArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_connect import events as connect_events
                    
                    agent_info = connect_events.InstanceEvents.CodeConnectContact.AgentInfo(
                        agent_arn=["agentArn"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__f731106873862d9751464422ef58a769fb937e25c6e9d0bde43523a280171513)
                    check_type(argname="argument agent_arn", value=agent_arn, expected_type=type_hints["agent_arn"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if agent_arn is not None:
                    self._values["agent_arn"] = agent_arn

            @builtins.property
            def agent_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) agentArn property.

                Specify an array of string values to match this event if the actual value of agentArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("agent_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AgentInfo(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_connect.events.InstanceEvents.CodeConnectContact.CodeConnectContactProps",
            jsii_struct_bases=[],
            name_mapping={
                "agent_info": "agentInfo",
                "channel": "channel",
                "contact_id": "contactId",
                "event_metadata": "eventMetadata",
                "event_type": "eventType",
                "initial_contact_id": "initialContactId",
                "initiation_method": "initiationMethod",
                "instance_arn": "instanceArn",
                "previous_contact_id": "previousContactId",
                "queue_info": "queueInfo",
            },
        )
        class CodeConnectContactProps:
            def __init__(
                self,
                *,
                agent_info: typing.Optional[typing.Union["InstanceEvents.CodeConnectContact.AgentInfo", typing.Dict[builtins.str, typing.Any]]] = None,
                channel: typing.Optional[typing.Sequence[builtins.str]] = None,
                contact_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                initial_contact_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                initiation_method: typing.Optional[typing.Sequence[builtins.str]] = None,
                instance_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                previous_contact_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                queue_info: typing.Optional[typing.Union["InstanceEvents.CodeConnectContact.QueueInfo", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Props type for Instance aws.connect@CodeConnectContact event.

                :param agent_info: (experimental) agentInfo property. Specify an array of string values to match this event if the actual value of agentInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param channel: (experimental) channel property. Specify an array of string values to match this event if the actual value of channel is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param contact_id: (experimental) contactId property. Specify an array of string values to match this event if the actual value of contactId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param event_type: (experimental) eventType property. Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param initial_contact_id: (experimental) initialContactId property. Specify an array of string values to match this event if the actual value of initialContactId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param initiation_method: (experimental) initiationMethod property. Specify an array of string values to match this event if the actual value of initiationMethod is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_arn: (experimental) instanceArn property. Specify an array of string values to match this event if the actual value of instanceArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Instance reference
                :param previous_contact_id: (experimental) previousContactId property. Specify an array of string values to match this event if the actual value of previousContactId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param queue_info: (experimental) queueInfo property. Specify an array of string values to match this event if the actual value of queueInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_connect import events as connect_events
                    
                    code_connect_contact_props = connect_events.InstanceEvents.CodeConnectContact.CodeConnectContactProps(
                        agent_info=connect_events.InstanceEvents.CodeConnectContact.AgentInfo(
                            agent_arn=["agentArn"]
                        ),
                        channel=["channel"],
                        contact_id=["contactId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        event_type=["eventType"],
                        initial_contact_id=["initialContactId"],
                        initiation_method=["initiationMethod"],
                        instance_arn=["instanceArn"],
                        previous_contact_id=["previousContactId"],
                        queue_info=connect_events.InstanceEvents.CodeConnectContact.QueueInfo(
                            queue_arn=["queueArn"],
                            queue_type=["queueType"]
                        )
                    )
                '''
                if isinstance(agent_info, dict):
                    agent_info = InstanceEvents.CodeConnectContact.AgentInfo(**agent_info)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(queue_info, dict):
                    queue_info = InstanceEvents.CodeConnectContact.QueueInfo(**queue_info)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__e981ce2a66816cbcf1a77bc5b5f79a81db192b297a9172ba782eec324ae26b5e)
                    check_type(argname="argument agent_info", value=agent_info, expected_type=type_hints["agent_info"])
                    check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
                    check_type(argname="argument contact_id", value=contact_id, expected_type=type_hints["contact_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
                    check_type(argname="argument initial_contact_id", value=initial_contact_id, expected_type=type_hints["initial_contact_id"])
                    check_type(argname="argument initiation_method", value=initiation_method, expected_type=type_hints["initiation_method"])
                    check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
                    check_type(argname="argument previous_contact_id", value=previous_contact_id, expected_type=type_hints["previous_contact_id"])
                    check_type(argname="argument queue_info", value=queue_info, expected_type=type_hints["queue_info"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if agent_info is not None:
                    self._values["agent_info"] = agent_info
                if channel is not None:
                    self._values["channel"] = channel
                if contact_id is not None:
                    self._values["contact_id"] = contact_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if event_type is not None:
                    self._values["event_type"] = event_type
                if initial_contact_id is not None:
                    self._values["initial_contact_id"] = initial_contact_id
                if initiation_method is not None:
                    self._values["initiation_method"] = initiation_method
                if instance_arn is not None:
                    self._values["instance_arn"] = instance_arn
                if previous_contact_id is not None:
                    self._values["previous_contact_id"] = previous_contact_id
                if queue_info is not None:
                    self._values["queue_info"] = queue_info

            @builtins.property
            def agent_info(
                self,
            ) -> typing.Optional["InstanceEvents.CodeConnectContact.AgentInfo"]:
                '''(experimental) agentInfo property.

                Specify an array of string values to match this event if the actual value of agentInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("agent_info")
                return typing.cast(typing.Optional["InstanceEvents.CodeConnectContact.AgentInfo"], result)

            @builtins.property
            def channel(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) channel property.

                Specify an array of string values to match this event if the actual value of channel is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("channel")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def contact_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) contactId property.

                Specify an array of string values to match this event if the actual value of contactId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("contact_id")
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
            def event_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventType property.

                Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def initial_contact_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) initialContactId property.

                Specify an array of string values to match this event if the actual value of initialContactId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("initial_contact_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def initiation_method(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) initiationMethod property.

                Specify an array of string values to match this event if the actual value of initiationMethod is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("initiation_method")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def instance_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instanceArn property.

                Specify an array of string values to match this event if the actual value of instanceArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Instance reference

                :stability: experimental
                '''
                result = self._values.get("instance_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def previous_contact_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) previousContactId property.

                Specify an array of string values to match this event if the actual value of previousContactId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("previous_contact_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def queue_info(
                self,
            ) -> typing.Optional["InstanceEvents.CodeConnectContact.QueueInfo"]:
                '''(experimental) queueInfo property.

                Specify an array of string values to match this event if the actual value of queueInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("queue_info")
                return typing.cast(typing.Optional["InstanceEvents.CodeConnectContact.QueueInfo"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "CodeConnectContactProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_connect.events.InstanceEvents.CodeConnectContact.QueueInfo",
            jsii_struct_bases=[],
            name_mapping={"queue_arn": "queueArn", "queue_type": "queueType"},
        )
        class QueueInfo:
            def __init__(
                self,
                *,
                queue_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                queue_type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for QueueInfo.

                :param queue_arn: (experimental) queueArn property. Specify an array of string values to match this event if the actual value of queueArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param queue_type: (experimental) queueType property. Specify an array of string values to match this event if the actual value of queueType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_connect import events as connect_events
                    
                    queue_info = connect_events.InstanceEvents.CodeConnectContact.QueueInfo(
                        queue_arn=["queueArn"],
                        queue_type=["queueType"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__da6c59a7d3c5b2faba4a29f204e37c18fbd929707447e0105e90b1b07bc5d21e)
                    check_type(argname="argument queue_arn", value=queue_arn, expected_type=type_hints["queue_arn"])
                    check_type(argname="argument queue_type", value=queue_type, expected_type=type_hints["queue_type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if queue_arn is not None:
                    self._values["queue_arn"] = queue_arn
                if queue_type is not None:
                    self._values["queue_type"] = queue_type

            @builtins.property
            def queue_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) queueArn property.

                Specify an array of string values to match this event if the actual value of queueArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("queue_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def queue_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) queueType property.

                Specify an array of string values to match this event if the actual value of queueType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("queue_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "QueueInfo(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ContactLensPostCallRulesMatched(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_connect.events.InstanceEvents.ContactLensPostCallRulesMatched",
    ):
        '''(experimental) aws.connect@ContactLensPostCallRulesMatched event types for Instance.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import events as connect_events
            
            contact_lens_post_call_rules_matched = connect_events.InstanceEvents.ContactLensPostCallRulesMatched()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_connect.events.InstanceEvents.ContactLensPostCallRulesMatched.ContactLensPostCallRulesMatchedProps",
            jsii_struct_bases=[],
            name_mapping={
                "action_name": "actionName",
                "agent_arn": "agentArn",
                "contact_arn": "contactArn",
                "event_metadata": "eventMetadata",
                "instance_arn": "instanceArn",
                "queue_arn": "queueArn",
                "rule_name": "ruleName",
                "version": "version",
            },
        )
        class ContactLensPostCallRulesMatchedProps:
            def __init__(
                self,
                *,
                action_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                agent_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                contact_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                instance_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                queue_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                rule_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Instance aws.connect@ContactLensPostCallRulesMatched event.

                :param action_name: (experimental) actionName property. Specify an array of string values to match this event if the actual value of actionName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param agent_arn: (experimental) agentArn property. Specify an array of string values to match this event if the actual value of agentArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param contact_arn: (experimental) contactArn property. Specify an array of string values to match this event if the actual value of contactArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param instance_arn: (experimental) instanceArn property. Specify an array of string values to match this event if the actual value of instanceArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Instance reference
                :param queue_arn: (experimental) queueArn property. Specify an array of string values to match this event if the actual value of queueArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param rule_name: (experimental) ruleName property. Specify an array of string values to match this event if the actual value of ruleName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_connect import events as connect_events
                    
                    contact_lens_post_call_rules_matched_props = connect_events.InstanceEvents.ContactLensPostCallRulesMatched.ContactLensPostCallRulesMatchedProps(
                        action_name=["actionName"],
                        agent_arn=["agentArn"],
                        contact_arn=["contactArn"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        instance_arn=["instanceArn"],
                        queue_arn=["queueArn"],
                        rule_name=["ruleName"],
                        version=["version"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__eb2b9af285f595269beb64fdc889185e70b5486ffa7831ccc84421a016809b03)
                    check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
                    check_type(argname="argument agent_arn", value=agent_arn, expected_type=type_hints["agent_arn"])
                    check_type(argname="argument contact_arn", value=contact_arn, expected_type=type_hints["contact_arn"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
                    check_type(argname="argument queue_arn", value=queue_arn, expected_type=type_hints["queue_arn"])
                    check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
                    check_type(argname="argument version", value=version, expected_type=type_hints["version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if action_name is not None:
                    self._values["action_name"] = action_name
                if agent_arn is not None:
                    self._values["agent_arn"] = agent_arn
                if contact_arn is not None:
                    self._values["contact_arn"] = contact_arn
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if instance_arn is not None:
                    self._values["instance_arn"] = instance_arn
                if queue_arn is not None:
                    self._values["queue_arn"] = queue_arn
                if rule_name is not None:
                    self._values["rule_name"] = rule_name
                if version is not None:
                    self._values["version"] = version

            @builtins.property
            def action_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) actionName property.

                Specify an array of string values to match this event if the actual value of actionName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("action_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def agent_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) agentArn property.

                Specify an array of string values to match this event if the actual value of agentArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("agent_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def contact_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) contactArn property.

                Specify an array of string values to match this event if the actual value of contactArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("contact_arn")
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
            def instance_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instanceArn property.

                Specify an array of string values to match this event if the actual value of instanceArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Instance reference

                :stability: experimental
                '''
                result = self._values.get("instance_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def queue_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) queueArn property.

                Specify an array of string values to match this event if the actual value of queueArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("queue_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def rule_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ruleName property.

                Specify an array of string values to match this event if the actual value of ruleName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("rule_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) version property.

                Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ContactLensPostCallRulesMatchedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class ContactLensRealtimeRulesMatched(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_connect.events.InstanceEvents.ContactLensRealtimeRulesMatched",
    ):
        '''(experimental) aws.connect@ContactLensRealtimeRulesMatched event types for Instance.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import events as connect_events
            
            contact_lens_realtime_rules_matched = connect_events.InstanceEvents.ContactLensRealtimeRulesMatched()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_connect.events.InstanceEvents.ContactLensRealtimeRulesMatched.ContactLensRealtimeRulesMatchedProps",
            jsii_struct_bases=[],
            name_mapping={
                "action_name": "actionName",
                "agent_arn": "agentArn",
                "contact_arn": "contactArn",
                "event_metadata": "eventMetadata",
                "instance_arn": "instanceArn",
                "queue_arn": "queueArn",
                "rule_name": "ruleName",
                "version": "version",
            },
        )
        class ContactLensRealtimeRulesMatchedProps:
            def __init__(
                self,
                *,
                action_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                agent_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                contact_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                instance_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                queue_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                rule_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Instance aws.connect@ContactLensRealtimeRulesMatched event.

                :param action_name: (experimental) actionName property. Specify an array of string values to match this event if the actual value of actionName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param agent_arn: (experimental) agentArn property. Specify an array of string values to match this event if the actual value of agentArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param contact_arn: (experimental) contactArn property. Specify an array of string values to match this event if the actual value of contactArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param instance_arn: (experimental) instanceArn property. Specify an array of string values to match this event if the actual value of instanceArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Instance reference
                :param queue_arn: (experimental) queueArn property. Specify an array of string values to match this event if the actual value of queueArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param rule_name: (experimental) ruleName property. Specify an array of string values to match this event if the actual value of ruleName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_connect import events as connect_events
                    
                    contact_lens_realtime_rules_matched_props = connect_events.InstanceEvents.ContactLensRealtimeRulesMatched.ContactLensRealtimeRulesMatchedProps(
                        action_name=["actionName"],
                        agent_arn=["agentArn"],
                        contact_arn=["contactArn"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        instance_arn=["instanceArn"],
                        queue_arn=["queueArn"],
                        rule_name=["ruleName"],
                        version=["version"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__5a38cd8e1e7e9584456ba3acb291da892de2ee7fdd6f54def6d60b037b0b9fb1)
                    check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
                    check_type(argname="argument agent_arn", value=agent_arn, expected_type=type_hints["agent_arn"])
                    check_type(argname="argument contact_arn", value=contact_arn, expected_type=type_hints["contact_arn"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
                    check_type(argname="argument queue_arn", value=queue_arn, expected_type=type_hints["queue_arn"])
                    check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
                    check_type(argname="argument version", value=version, expected_type=type_hints["version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if action_name is not None:
                    self._values["action_name"] = action_name
                if agent_arn is not None:
                    self._values["agent_arn"] = agent_arn
                if contact_arn is not None:
                    self._values["contact_arn"] = contact_arn
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if instance_arn is not None:
                    self._values["instance_arn"] = instance_arn
                if queue_arn is not None:
                    self._values["queue_arn"] = queue_arn
                if rule_name is not None:
                    self._values["rule_name"] = rule_name
                if version is not None:
                    self._values["version"] = version

            @builtins.property
            def action_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) actionName property.

                Specify an array of string values to match this event if the actual value of actionName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("action_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def agent_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) agentArn property.

                Specify an array of string values to match this event if the actual value of agentArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("agent_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def contact_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) contactArn property.

                Specify an array of string values to match this event if the actual value of contactArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("contact_arn")
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
            def instance_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instanceArn property.

                Specify an array of string values to match this event if the actual value of instanceArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Instance reference

                :stability: experimental
                '''
                result = self._values.get("instance_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def queue_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) queueArn property.

                Specify an array of string values to match this event if the actual value of queueArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("queue_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def rule_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ruleName property.

                Specify an array of string values to match this event if the actual value of ruleName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("rule_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) version property.

                Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ContactLensRealtimeRulesMatchedProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "InstanceEvents",
]

publication.publish()

def _typecheckingstub__6a6f14fffbee0d4e1c88aa93635443b38c0f2f5a5f2bf5182efcea94b8c9b90f(
    instance_ref: _aws_cdk_interfaces_aws_connect_ceddda9d.IInstanceRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f731106873862d9751464422ef58a769fb937e25c6e9d0bde43523a280171513(
    *,
    agent_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e981ce2a66816cbcf1a77bc5b5f79a81db192b297a9172ba782eec324ae26b5e(
    *,
    agent_info: typing.Optional[typing.Union[InstanceEvents.CodeConnectContact.AgentInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    channel: typing.Optional[typing.Sequence[builtins.str]] = None,
    contact_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    initial_contact_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    initiation_method: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    previous_contact_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    queue_info: typing.Optional[typing.Union[InstanceEvents.CodeConnectContact.QueueInfo, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da6c59a7d3c5b2faba4a29f204e37c18fbd929707447e0105e90b1b07bc5d21e(
    *,
    queue_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    queue_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2b9af285f595269beb64fdc889185e70b5486ffa7831ccc84421a016809b03(
    *,
    action_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    agent_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    contact_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    queue_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    rule_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a38cd8e1e7e9584456ba3acb291da892de2ee7fdd6f54def6d60b037b0b9fb1(
    *,
    action_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    agent_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    contact_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    queue_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    rule_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
