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
import aws_cdk.interfaces.aws_medialive as _aws_cdk_interfaces_aws_medialive_ceddda9d


class ChannelEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_medialive.events.ChannelEvents",
):
    '''(experimental) EventBridge event patterns for Channel.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_medialive import events as medialive_events
        from aws_cdk.interfaces import aws_medialive as interfaces_medialive
        
        # channel_ref: interfaces_medialive.IChannelRef
        
        channel_events = medialive_events.ChannelEvents.from_channel(channel_ref)
    '''

    @jsii.member(jsii_name="fromChannel")
    @builtins.classmethod
    def from_channel(
        cls,
        channel_ref: _aws_cdk_interfaces_aws_medialive_ceddda9d.IChannelRef,
    ) -> "ChannelEvents":
        '''(experimental) Create ChannelEvents from a Channel reference.

        :param channel_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__781c517defde0e17fe01331d76449619e67189af644908068453d406ea74b7a3)
            check_type(argname="argument channel_ref", value=channel_ref, expected_type=type_hints["channel_ref"])
        return typing.cast("ChannelEvents", jsii.sinvoke(cls, "fromChannel", [channel_ref]))

    @jsii.member(jsii_name="mediaLiveChannelInputChangePattern")
    def media_live_channel_input_change_pattern(
        self,
        *,
        active_input_attachment_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        active_input_switch_action_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        channel_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        message: typing.Optional[typing.Sequence[builtins.str]] = None,
        pipeline: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Channel MediaLive Channel Input Change.

        :param active_input_attachment_name: (experimental) active_input_attachment_name property. Specify an array of string values to match this event if the actual value of active_input_attachment_name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param active_input_switch_action_name: (experimental) active_input_switch_action_name property. Specify an array of string values to match this event if the actual value of active_input_switch_action_name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param channel_arn: (experimental) channel_arn property. Specify an array of string values to match this event if the actual value of channel_arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Channel reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param message: (experimental) message property. Specify an array of string values to match this event if the actual value of message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param pipeline: (experimental) pipeline property. Specify an array of string values to match this event if the actual value of pipeline is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = ChannelEvents.MediaLiveChannelInputChange.MediaLiveChannelInputChangeProps(
            active_input_attachment_name=active_input_attachment_name,
            active_input_switch_action_name=active_input_switch_action_name,
            channel_arn=channel_arn,
            event_metadata=event_metadata,
            message=message,
            pipeline=pipeline,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "mediaLiveChannelInputChangePattern", [options]))

    class MediaLiveChannelInputChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_medialive.events.ChannelEvents.MediaLiveChannelInputChange",
    ):
        '''(experimental) aws.medialive@MediaLiveChannelInputChange event types for Channel.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_medialive import events as medialive_events
            
            media_live_channel_input_change = medialive_events.ChannelEvents.MediaLiveChannelInputChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_medialive.events.ChannelEvents.MediaLiveChannelInputChange.MediaLiveChannelInputChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "active_input_attachment_name": "activeInputAttachmentName",
                "active_input_switch_action_name": "activeInputSwitchActionName",
                "channel_arn": "channelArn",
                "event_metadata": "eventMetadata",
                "message": "message",
                "pipeline": "pipeline",
            },
        )
        class MediaLiveChannelInputChangeProps:
            def __init__(
                self,
                *,
                active_input_attachment_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                active_input_switch_action_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                channel_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                message: typing.Optional[typing.Sequence[builtins.str]] = None,
                pipeline: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Channel aws.medialive@MediaLiveChannelInputChange event.

                :param active_input_attachment_name: (experimental) active_input_attachment_name property. Specify an array of string values to match this event if the actual value of active_input_attachment_name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param active_input_switch_action_name: (experimental) active_input_switch_action_name property. Specify an array of string values to match this event if the actual value of active_input_switch_action_name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param channel_arn: (experimental) channel_arn property. Specify an array of string values to match this event if the actual value of channel_arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Channel reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param message: (experimental) message property. Specify an array of string values to match this event if the actual value of message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param pipeline: (experimental) pipeline property. Specify an array of string values to match this event if the actual value of pipeline is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_medialive import events as medialive_events
                    
                    media_live_channel_input_change_props = medialive_events.ChannelEvents.MediaLiveChannelInputChange.MediaLiveChannelInputChangeProps(
                        active_input_attachment_name=["activeInputAttachmentName"],
                        active_input_switch_action_name=["activeInputSwitchActionName"],
                        channel_arn=["channelArn"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        message=["message"],
                        pipeline=["pipeline"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__87d55463ff3f32088679bc4b900f0db97e3fbe4c6417fd9f1d3b8d871e91b987)
                    check_type(argname="argument active_input_attachment_name", value=active_input_attachment_name, expected_type=type_hints["active_input_attachment_name"])
                    check_type(argname="argument active_input_switch_action_name", value=active_input_switch_action_name, expected_type=type_hints["active_input_switch_action_name"])
                    check_type(argname="argument channel_arn", value=channel_arn, expected_type=type_hints["channel_arn"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument message", value=message, expected_type=type_hints["message"])
                    check_type(argname="argument pipeline", value=pipeline, expected_type=type_hints["pipeline"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if active_input_attachment_name is not None:
                    self._values["active_input_attachment_name"] = active_input_attachment_name
                if active_input_switch_action_name is not None:
                    self._values["active_input_switch_action_name"] = active_input_switch_action_name
                if channel_arn is not None:
                    self._values["channel_arn"] = channel_arn
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if message is not None:
                    self._values["message"] = message
                if pipeline is not None:
                    self._values["pipeline"] = pipeline

            @builtins.property
            def active_input_attachment_name(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) active_input_attachment_name property.

                Specify an array of string values to match this event if the actual value of active_input_attachment_name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("active_input_attachment_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def active_input_switch_action_name(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) active_input_switch_action_name property.

                Specify an array of string values to match this event if the actual value of active_input_switch_action_name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("active_input_switch_action_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def channel_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) channel_arn property.

                Specify an array of string values to match this event if the actual value of channel_arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Channel reference

                :stability: experimental
                '''
                result = self._values.get("channel_arn")
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
            def message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) message property.

                Specify an array of string values to match this event if the actual value of message is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def pipeline(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) pipeline property.

                Specify an array of string values to match this event if the actual value of pipeline is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("pipeline")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "MediaLiveChannelInputChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "ChannelEvents",
]

publication.publish()

def _typecheckingstub__781c517defde0e17fe01331d76449619e67189af644908068453d406ea74b7a3(
    channel_ref: _aws_cdk_interfaces_aws_medialive_ceddda9d.IChannelRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d55463ff3f32088679bc4b900f0db97e3fbe4c6417fd9f1d3b8d871e91b987(
    *,
    active_input_attachment_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    active_input_switch_action_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    channel_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    message: typing.Optional[typing.Sequence[builtins.str]] = None,
    pipeline: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
