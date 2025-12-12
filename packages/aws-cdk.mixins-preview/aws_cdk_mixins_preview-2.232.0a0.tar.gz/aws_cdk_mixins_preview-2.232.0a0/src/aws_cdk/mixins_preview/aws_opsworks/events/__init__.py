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
import aws_cdk.interfaces.aws_opsworks as _aws_cdk_interfaces_aws_opsworks_ceddda9d


class InstanceEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_opsworks.events.InstanceEvents",
):
    '''(experimental) EventBridge event patterns for Instance.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_opsworks import events as opsworks_events
        from aws_cdk.interfaces import aws_opsworks as interfaces_opsworks
        
        # instance_ref: interfaces_opsworks.IInstanceRef
        
        instance_events = opsworks_events.InstanceEvents.from_instance(instance_ref)
    '''

    @jsii.member(jsii_name="fromInstance")
    @builtins.classmethod
    def from_instance(
        cls,
        instance_ref: _aws_cdk_interfaces_aws_opsworks_ceddda9d.IInstanceRef,
    ) -> "InstanceEvents":
        '''(experimental) Create InstanceEvents from a Instance reference.

        :param instance_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e54533e82baad1aafebf63f8f0b50a1aca163f44cd87c6c1d88d8329d46b06b)
            check_type(argname="argument instance_ref", value=instance_ref, expected_type=type_hints["instance_ref"])
        return typing.cast("InstanceEvents", jsii.sinvoke(cls, "fromInstance", [instance_ref]))

    @jsii.member(jsii_name="opsWorksAlertPattern")
    def ops_works_alert_pattern(
        self,
        *,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        message: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        type: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Instance OpsWorks Alert.

        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param instance_id: (experimental) instance-id property. Specify an array of string values to match this event if the actual value of instance-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Instance reference
        :param message: (experimental) message property. Specify an array of string values to match this event if the actual value of message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param stack_id: (experimental) stack-id property. Specify an array of string values to match this event if the actual value of stack-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = InstanceEvents.OpsWorksAlert.OpsWorksAlertProps(
            event_metadata=event_metadata,
            instance_id=instance_id,
            message=message,
            stack_id=stack_id,
            type=type,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "opsWorksAlertPattern", [options]))

    @jsii.member(jsii_name="opsWorksCommandStateChangePattern")
    def ops_works_command_state_change_pattern(
        self,
        *,
        command_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[typing.Sequence[builtins.str]] = None,
        type: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Instance OpsWorks Command State Change.

        :param command_id: (experimental) command-id property. Specify an array of string values to match this event if the actual value of command-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param instance_id: (experimental) instance-id property. Specify an array of string values to match this event if the actual value of instance-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Instance reference
        :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = InstanceEvents.OpsWorksCommandStateChange.OpsWorksCommandStateChangeProps(
            command_id=command_id,
            event_metadata=event_metadata,
            instance_id=instance_id,
            status=status,
            type=type,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "opsWorksCommandStateChangePattern", [options]))

    @jsii.member(jsii_name="opsWorksInstanceStateChangePattern")
    def ops_works_instance_state_change_pattern(
        self,
        *,
        ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        hostname: typing.Optional[typing.Sequence[builtins.str]] = None,
        initiated_by: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        layer_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Instance OpsWorks Instance State Change.

        :param ec2_instance_id: (experimental) ec2-instance-id property. Specify an array of string values to match this event if the actual value of ec2-instance-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param hostname: (experimental) hostname property. Specify an array of string values to match this event if the actual value of hostname is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param initiated_by: (experimental) initiated_by property. Specify an array of string values to match this event if the actual value of initiated_by is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param instance_id: (experimental) instance-id property. Specify an array of string values to match this event if the actual value of instance-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Instance reference
        :param layer_ids: (experimental) layer-ids property. Specify an array of string values to match this event if the actual value of layer-ids is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param stack_id: (experimental) stack-id property. Specify an array of string values to match this event if the actual value of stack-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = InstanceEvents.OpsWorksInstanceStateChange.OpsWorksInstanceStateChangeProps(
            ec2_instance_id=ec2_instance_id,
            event_metadata=event_metadata,
            hostname=hostname,
            initiated_by=initiated_by,
            instance_id=instance_id,
            layer_ids=layer_ids,
            stack_id=stack_id,
            status=status,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "opsWorksInstanceStateChangePattern", [options]))

    class OpsWorksAlert(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.events.InstanceEvents.OpsWorksAlert",
    ):
        '''(experimental) aws.opsworks@OpsWorksAlert event types for Instance.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opsworks import events as opsworks_events
            
            ops_works_alert = opsworks_events.InstanceEvents.OpsWorksAlert()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_opsworks.events.InstanceEvents.OpsWorksAlert.OpsWorksAlertProps",
            jsii_struct_bases=[],
            name_mapping={
                "event_metadata": "eventMetadata",
                "instance_id": "instanceId",
                "message": "message",
                "stack_id": "stackId",
                "type": "type",
            },
        )
        class OpsWorksAlertProps:
            def __init__(
                self,
                *,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                message: typing.Optional[typing.Sequence[builtins.str]] = None,
                stack_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Instance aws.opsworks@OpsWorksAlert event.

                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param instance_id: (experimental) instance-id property. Specify an array of string values to match this event if the actual value of instance-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Instance reference
                :param message: (experimental) message property. Specify an array of string values to match this event if the actual value of message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param stack_id: (experimental) stack-id property. Specify an array of string values to match this event if the actual value of stack-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_opsworks import events as opsworks_events
                    
                    ops_works_alert_props = opsworks_events.InstanceEvents.OpsWorksAlert.OpsWorksAlertProps(
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        instance_id=["instanceId"],
                        message=["message"],
                        stack_id=["stackId"],
                        type=["type"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__bd2afc869d716ebac2e140f13022f5577135837fb273b61614a860d42fc283b1)
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
                    check_type(argname="argument message", value=message, expected_type=type_hints["message"])
                    check_type(argname="argument stack_id", value=stack_id, expected_type=type_hints["stack_id"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if instance_id is not None:
                    self._values["instance_id"] = instance_id
                if message is not None:
                    self._values["message"] = message
                if stack_id is not None:
                    self._values["stack_id"] = stack_id
                if type is not None:
                    self._values["type"] = type

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
            def instance_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instance-id property.

                Specify an array of string values to match this event if the actual value of instance-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Instance reference

                :stability: experimental
                '''
                result = self._values.get("instance_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) message property.

                Specify an array of string values to match this event if the actual value of message is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def stack_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) stack-id property.

                Specify an array of string values to match this event if the actual value of stack-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("stack_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) type property.

                Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "OpsWorksAlertProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class OpsWorksCommandStateChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.events.InstanceEvents.OpsWorksCommandStateChange",
    ):
        '''(experimental) aws.opsworks@OpsWorksCommandStateChange event types for Instance.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opsworks import events as opsworks_events
            
            ops_works_command_state_change = opsworks_events.InstanceEvents.OpsWorksCommandStateChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_opsworks.events.InstanceEvents.OpsWorksCommandStateChange.OpsWorksCommandStateChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "command_id": "commandId",
                "event_metadata": "eventMetadata",
                "instance_id": "instanceId",
                "status": "status",
                "type": "type",
            },
        )
        class OpsWorksCommandStateChangeProps:
            def __init__(
                self,
                *,
                command_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Instance aws.opsworks@OpsWorksCommandStateChange event.

                :param command_id: (experimental) command-id property. Specify an array of string values to match this event if the actual value of command-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param instance_id: (experimental) instance-id property. Specify an array of string values to match this event if the actual value of instance-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Instance reference
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_opsworks import events as opsworks_events
                    
                    ops_works_command_state_change_props = opsworks_events.InstanceEvents.OpsWorksCommandStateChange.OpsWorksCommandStateChangeProps(
                        command_id=["commandId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        instance_id=["instanceId"],
                        status=["status"],
                        type=["type"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__f7cabb7a8a2401e444dfbfe696a250ef85fbc7cbe7a5c8455541541fd9027be7)
                    check_type(argname="argument command_id", value=command_id, expected_type=type_hints["command_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if command_id is not None:
                    self._values["command_id"] = command_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if instance_id is not None:
                    self._values["instance_id"] = instance_id
                if status is not None:
                    self._values["status"] = status
                if type is not None:
                    self._values["type"] = type

            @builtins.property
            def command_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) command-id property.

                Specify an array of string values to match this event if the actual value of command-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("command_id")
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
            def instance_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instance-id property.

                Specify an array of string values to match this event if the actual value of instance-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Instance reference

                :stability: experimental
                '''
                result = self._values.get("instance_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status property.

                Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) type property.

                Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "OpsWorksCommandStateChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class OpsWorksInstanceStateChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.events.InstanceEvents.OpsWorksInstanceStateChange",
    ):
        '''(experimental) aws.opsworks@OpsWorksInstanceStateChange event types for Instance.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opsworks import events as opsworks_events
            
            ops_works_instance_state_change = opsworks_events.InstanceEvents.OpsWorksInstanceStateChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_opsworks.events.InstanceEvents.OpsWorksInstanceStateChange.OpsWorksInstanceStateChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "ec2_instance_id": "ec2InstanceId",
                "event_metadata": "eventMetadata",
                "hostname": "hostname",
                "initiated_by": "initiatedBy",
                "instance_id": "instanceId",
                "layer_ids": "layerIds",
                "stack_id": "stackId",
                "status": "status",
            },
        )
        class OpsWorksInstanceStateChangeProps:
            def __init__(
                self,
                *,
                ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                hostname: typing.Optional[typing.Sequence[builtins.str]] = None,
                initiated_by: typing.Optional[typing.Sequence[builtins.str]] = None,
                instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                layer_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
                stack_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Instance aws.opsworks@OpsWorksInstanceStateChange event.

                :param ec2_instance_id: (experimental) ec2-instance-id property. Specify an array of string values to match this event if the actual value of ec2-instance-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param hostname: (experimental) hostname property. Specify an array of string values to match this event if the actual value of hostname is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param initiated_by: (experimental) initiated_by property. Specify an array of string values to match this event if the actual value of initiated_by is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_id: (experimental) instance-id property. Specify an array of string values to match this event if the actual value of instance-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Instance reference
                :param layer_ids: (experimental) layer-ids property. Specify an array of string values to match this event if the actual value of layer-ids is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param stack_id: (experimental) stack-id property. Specify an array of string values to match this event if the actual value of stack-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_opsworks import events as opsworks_events
                    
                    ops_works_instance_state_change_props = opsworks_events.InstanceEvents.OpsWorksInstanceStateChange.OpsWorksInstanceStateChangeProps(
                        ec2_instance_id=["ec2InstanceId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        hostname=["hostname"],
                        initiated_by=["initiatedBy"],
                        instance_id=["instanceId"],
                        layer_ids=["layerIds"],
                        stack_id=["stackId"],
                        status=["status"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__64ec5934ce5c3826b10fa29b9a82f8e38cdefb74c14a2eae8bbdff0571088191)
                    check_type(argname="argument ec2_instance_id", value=ec2_instance_id, expected_type=type_hints["ec2_instance_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
                    check_type(argname="argument initiated_by", value=initiated_by, expected_type=type_hints["initiated_by"])
                    check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
                    check_type(argname="argument layer_ids", value=layer_ids, expected_type=type_hints["layer_ids"])
                    check_type(argname="argument stack_id", value=stack_id, expected_type=type_hints["stack_id"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if ec2_instance_id is not None:
                    self._values["ec2_instance_id"] = ec2_instance_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if hostname is not None:
                    self._values["hostname"] = hostname
                if initiated_by is not None:
                    self._values["initiated_by"] = initiated_by
                if instance_id is not None:
                    self._values["instance_id"] = instance_id
                if layer_ids is not None:
                    self._values["layer_ids"] = layer_ids
                if stack_id is not None:
                    self._values["stack_id"] = stack_id
                if status is not None:
                    self._values["status"] = status

            @builtins.property
            def ec2_instance_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ec2-instance-id property.

                Specify an array of string values to match this event if the actual value of ec2-instance-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ec2_instance_id")
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
            def hostname(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) hostname property.

                Specify an array of string values to match this event if the actual value of hostname is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("hostname")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def initiated_by(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) initiated_by property.

                Specify an array of string values to match this event if the actual value of initiated_by is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("initiated_by")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def instance_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instance-id property.

                Specify an array of string values to match this event if the actual value of instance-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Instance reference

                :stability: experimental
                '''
                result = self._values.get("instance_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def layer_ids(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) layer-ids property.

                Specify an array of string values to match this event if the actual value of layer-ids is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("layer_ids")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def stack_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) stack-id property.

                Specify an array of string values to match this event if the actual value of stack-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("stack_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status property.

                Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "OpsWorksInstanceStateChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


class StackEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_opsworks.events.StackEvents",
):
    '''(experimental) EventBridge event patterns for Stack.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_opsworks import events as opsworks_events
        from aws_cdk.interfaces import aws_opsworks as interfaces_opsworks
        
        # stack_ref: interfaces_opsworks.IStackRef
        
        stack_events = opsworks_events.StackEvents.from_stack(stack_ref)
    '''

    @jsii.member(jsii_name="fromStack")
    @builtins.classmethod
    def from_stack(
        cls,
        stack_ref: _aws_cdk_interfaces_aws_opsworks_ceddda9d.IStackRef,
    ) -> "StackEvents":
        '''(experimental) Create StackEvents from a Stack reference.

        :param stack_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3d41ee0d5dedba82521340aa4d10a6b78b5070cc2fe162d7962df07a2e115e)
            check_type(argname="argument stack_ref", value=stack_ref, expected_type=type_hints["stack_ref"])
        return typing.cast("StackEvents", jsii.sinvoke(cls, "fromStack", [stack_ref]))

    @jsii.member(jsii_name="opsWorksDeploymentStateChangePattern")
    def ops_works_deployment_state_change_pattern(
        self,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        duration: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        instance_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Stack OpsWorks Deployment State Change.

        :param command: (experimental) command property. Specify an array of string values to match this event if the actual value of command is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param deployment_id: (experimental) deployment-id property. Specify an array of string values to match this event if the actual value of deployment-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param duration: (experimental) duration property. Specify an array of string values to match this event if the actual value of duration is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param instance_ids: (experimental) instance-ids property. Specify an array of string values to match this event if the actual value of instance-ids is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param stack_id: (experimental) stack-id property. Specify an array of string values to match this event if the actual value of stack-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Stack reference
        :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = StackEvents.OpsWorksDeploymentStateChange.OpsWorksDeploymentStateChangeProps(
            command=command,
            deployment_id=deployment_id,
            duration=duration,
            event_metadata=event_metadata,
            instance_ids=instance_ids,
            stack_id=stack_id,
            status=status,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "opsWorksDeploymentStateChangePattern", [options]))

    class OpsWorksDeploymentStateChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.events.StackEvents.OpsWorksDeploymentStateChange",
    ):
        '''(experimental) aws.opsworks@OpsWorksDeploymentStateChange event types for Stack.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opsworks import events as opsworks_events
            
            ops_works_deployment_state_change = opsworks_events.StackEvents.OpsWorksDeploymentStateChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_opsworks.events.StackEvents.OpsWorksDeploymentStateChange.OpsWorksDeploymentStateChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "command": "command",
                "deployment_id": "deploymentId",
                "duration": "duration",
                "event_metadata": "eventMetadata",
                "instance_ids": "instanceIds",
                "stack_id": "stackId",
                "status": "status",
            },
        )
        class OpsWorksDeploymentStateChangeProps:
            def __init__(
                self,
                *,
                command: typing.Optional[typing.Sequence[builtins.str]] = None,
                deployment_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                duration: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                instance_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
                stack_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Stack aws.opsworks@OpsWorksDeploymentStateChange event.

                :param command: (experimental) command property. Specify an array of string values to match this event if the actual value of command is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param deployment_id: (experimental) deployment-id property. Specify an array of string values to match this event if the actual value of deployment-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param duration: (experimental) duration property. Specify an array of string values to match this event if the actual value of duration is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param instance_ids: (experimental) instance-ids property. Specify an array of string values to match this event if the actual value of instance-ids is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param stack_id: (experimental) stack-id property. Specify an array of string values to match this event if the actual value of stack-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Stack reference
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_opsworks import events as opsworks_events
                    
                    ops_works_deployment_state_change_props = opsworks_events.StackEvents.OpsWorksDeploymentStateChange.OpsWorksDeploymentStateChangeProps(
                        command=["command"],
                        deployment_id=["deploymentId"],
                        duration=["duration"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        instance_ids=["instanceIds"],
                        stack_id=["stackId"],
                        status=["status"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__f7b707cd538ae89650d66782dd1e0a4fff411d7af6fd1ac9b567f3ac56c4f274)
                    check_type(argname="argument command", value=command, expected_type=type_hints["command"])
                    check_type(argname="argument deployment_id", value=deployment_id, expected_type=type_hints["deployment_id"])
                    check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument instance_ids", value=instance_ids, expected_type=type_hints["instance_ids"])
                    check_type(argname="argument stack_id", value=stack_id, expected_type=type_hints["stack_id"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if command is not None:
                    self._values["command"] = command
                if deployment_id is not None:
                    self._values["deployment_id"] = deployment_id
                if duration is not None:
                    self._values["duration"] = duration
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if instance_ids is not None:
                    self._values["instance_ids"] = instance_ids
                if stack_id is not None:
                    self._values["stack_id"] = stack_id
                if status is not None:
                    self._values["status"] = status

            @builtins.property
            def command(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) command property.

                Specify an array of string values to match this event if the actual value of command is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("command")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def deployment_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) deployment-id property.

                Specify an array of string values to match this event if the actual value of deployment-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("deployment_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def duration(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) duration property.

                Specify an array of string values to match this event if the actual value of duration is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("duration")
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
            def instance_ids(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instance-ids property.

                Specify an array of string values to match this event if the actual value of instance-ids is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_ids")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def stack_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) stack-id property.

                Specify an array of string values to match this event if the actual value of stack-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Stack reference

                :stability: experimental
                '''
                result = self._values.get("stack_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status property.

                Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "OpsWorksDeploymentStateChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "InstanceEvents",
    "StackEvents",
]

publication.publish()

def _typecheckingstub__6e54533e82baad1aafebf63f8f0b50a1aca163f44cd87c6c1d88d8329d46b06b(
    instance_ref: _aws_cdk_interfaces_aws_opsworks_ceddda9d.IInstanceRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2afc869d716ebac2e140f13022f5577135837fb273b61614a860d42fc283b1(
    *,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    message: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7cabb7a8a2401e444dfbfe696a250ef85fbc7cbe7a5c8455541541fd9027be7(
    *,
    command_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ec5934ce5c3826b10fa29b9a82f8e38cdefb74c14a2eae8bbdff0571088191(
    *,
    ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    hostname: typing.Optional[typing.Sequence[builtins.str]] = None,
    initiated_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    layer_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3d41ee0d5dedba82521340aa4d10a6b78b5070cc2fe162d7962df07a2e115e(
    stack_ref: _aws_cdk_interfaces_aws_opsworks_ceddda9d.IStackRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7b707cd538ae89650d66782dd1e0a4fff411d7af6fd1ac9b567f3ac56c4f274(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    deployment_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    duration: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
