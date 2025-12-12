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
import aws_cdk.interfaces.aws_autoscaling as _aws_cdk_interfaces_aws_autoscaling_ceddda9d


class AutoScalingGroupEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.events.AutoScalingGroupEvents",
):
    '''(experimental) EventBridge event patterns for AutoScalingGroup.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_autoscaling import events as autoscaling_events
        from aws_cdk.interfaces import aws_autoscaling as interfaces_autoscaling
        
        # auto_scaling_group_ref: interfaces_autoscaling.IAutoScalingGroupRef
        
        auto_scaling_group_events = autoscaling_events.AutoScalingGroupEvents.from_auto_scaling_group(auto_scaling_group_ref)
    '''

    @jsii.member(jsii_name="fromAutoScalingGroup")
    @builtins.classmethod
    def from_auto_scaling_group(
        cls,
        auto_scaling_group_ref: _aws_cdk_interfaces_aws_autoscaling_ceddda9d.IAutoScalingGroupRef,
    ) -> "AutoScalingGroupEvents":
        '''(experimental) Create AutoScalingGroupEvents from a AutoScalingGroup reference.

        :param auto_scaling_group_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__969e9a9ab78cc8e0d927bb6cc75bd3f471f7b0b3439b6bebcb043eab1ff95288)
            check_type(argname="argument auto_scaling_group_ref", value=auto_scaling_group_ref, expected_type=type_hints["auto_scaling_group_ref"])
        return typing.cast("AutoScalingGroupEvents", jsii.sinvoke(cls, "fromAutoScalingGroup", [auto_scaling_group_ref]))

    @jsii.member(jsii_name="eC2InstanceLaunchLifecycleActionPattern")
    def e_c2_instance_launch_lifecycle_action_pattern(
        self,
        *,
        auto_scaling_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        destination: typing.Optional[typing.Sequence[builtins.str]] = None,
        ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        lifecycle_action_token: typing.Optional[typing.Sequence[builtins.str]] = None,
        lifecycle_hook_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        lifecycle_transition: typing.Optional[typing.Sequence[builtins.str]] = None,
        notification_metadata: typing.Optional[typing.Sequence[builtins.str]] = None,
        origin: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for AutoScalingGroup EC2 Instance-launch Lifecycle Action.

        :param auto_scaling_group_name: (experimental) AutoScalingGroupName property. Specify an array of string values to match this event if the actual value of AutoScalingGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the AutoScalingGroup reference
        :param destination: (experimental) Destination property. Specify an array of string values to match this event if the actual value of Destination is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param ec2_instance_id: (experimental) EC2InstanceId property. Specify an array of string values to match this event if the actual value of EC2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param lifecycle_action_token: (experimental) LifecycleActionToken property. Specify an array of string values to match this event if the actual value of LifecycleActionToken is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param lifecycle_hook_name: (experimental) LifecycleHookName property. Specify an array of string values to match this event if the actual value of LifecycleHookName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param lifecycle_transition: (experimental) LifecycleTransition property. Specify an array of string values to match this event if the actual value of LifecycleTransition is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param notification_metadata: (experimental) NotificationMetadata property. Specify an array of string values to match this event if the actual value of NotificationMetadata is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param origin: (experimental) Origin property. Specify an array of string values to match this event if the actual value of Origin is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = AutoScalingGroupEvents.EC2InstanceLaunchLifecycleAction.EC2InstanceLaunchLifecycleActionProps(
            auto_scaling_group_name=auto_scaling_group_name,
            destination=destination,
            ec2_instance_id=ec2_instance_id,
            event_metadata=event_metadata,
            lifecycle_action_token=lifecycle_action_token,
            lifecycle_hook_name=lifecycle_hook_name,
            lifecycle_transition=lifecycle_transition,
            notification_metadata=notification_metadata,
            origin=origin,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "eC2InstanceLaunchLifecycleActionPattern", [options]))

    @jsii.member(jsii_name="eC2InstanceLaunchSuccessfulPattern")
    def e_c2_instance_launch_successful_pattern(
        self,
        *,
        activity_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        auto_scaling_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        cause: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[typing.Sequence[builtins.str]] = None,
        destination: typing.Optional[typing.Sequence[builtins.str]] = None,
        details: typing.Optional[typing.Union["AutoScalingGroupEvents.EC2InstanceLaunchSuccessful.Details", typing.Dict[builtins.str, typing.Any]]] = None,
        ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_time: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        origin: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_time: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for AutoScalingGroup EC2 Instance Launch Successful.

        :param activity_id: (experimental) ActivityId property. Specify an array of string values to match this event if the actual value of ActivityId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param auto_scaling_group_name: (experimental) AutoScalingGroupName property. Specify an array of string values to match this event if the actual value of AutoScalingGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the AutoScalingGroup reference
        :param cause: (experimental) Cause property. Specify an array of string values to match this event if the actual value of Cause is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param description: (experimental) Description property. Specify an array of string values to match this event if the actual value of Description is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param destination: (experimental) Destination property. Specify an array of string values to match this event if the actual value of Destination is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param details: (experimental) Details property. Specify an array of string values to match this event if the actual value of Details is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param ec2_instance_id: (experimental) EC2InstanceId property. Specify an array of string values to match this event if the actual value of EC2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param end_time: (experimental) EndTime property. Specify an array of string values to match this event if the actual value of EndTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param origin: (experimental) Origin property. Specify an array of string values to match this event if the actual value of Origin is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_id: (experimental) RequestId property. Specify an array of string values to match this event if the actual value of RequestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param start_time: (experimental) StartTime property. Specify an array of string values to match this event if the actual value of StartTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) StatusCode property. Specify an array of string values to match this event if the actual value of StatusCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_message: (experimental) StatusMessage property. Specify an array of string values to match this event if the actual value of StatusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = AutoScalingGroupEvents.EC2InstanceLaunchSuccessful.EC2InstanceLaunchSuccessfulProps(
            activity_id=activity_id,
            auto_scaling_group_name=auto_scaling_group_name,
            cause=cause,
            description=description,
            destination=destination,
            details=details,
            ec2_instance_id=ec2_instance_id,
            end_time=end_time,
            event_metadata=event_metadata,
            origin=origin,
            request_id=request_id,
            start_time=start_time,
            status_code=status_code,
            status_message=status_message,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "eC2InstanceLaunchSuccessfulPattern", [options]))

    @jsii.member(jsii_name="eC2InstanceLaunchUnsuccessfulPattern")
    def e_c2_instance_launch_unsuccessful_pattern(
        self,
        *,
        activity_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        auto_scaling_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        cause: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[typing.Sequence[builtins.str]] = None,
        destination: typing.Optional[typing.Sequence[builtins.str]] = None,
        details: typing.Optional[typing.Union["AutoScalingGroupEvents.EC2InstanceLaunchUnsuccessful.Details", typing.Dict[builtins.str, typing.Any]]] = None,
        ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_time: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        origin: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_time: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for AutoScalingGroup EC2 Instance Launch Unsuccessful.

        :param activity_id: (experimental) ActivityId property. Specify an array of string values to match this event if the actual value of ActivityId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param auto_scaling_group_name: (experimental) AutoScalingGroupName property. Specify an array of string values to match this event if the actual value of AutoScalingGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the AutoScalingGroup reference
        :param cause: (experimental) Cause property. Specify an array of string values to match this event if the actual value of Cause is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param description: (experimental) Description property. Specify an array of string values to match this event if the actual value of Description is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param destination: (experimental) Destination property. Specify an array of string values to match this event if the actual value of Destination is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param details: (experimental) Details property. Specify an array of string values to match this event if the actual value of Details is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param ec2_instance_id: (experimental) EC2InstanceId property. Specify an array of string values to match this event if the actual value of EC2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param end_time: (experimental) EndTime property. Specify an array of string values to match this event if the actual value of EndTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param origin: (experimental) Origin property. Specify an array of string values to match this event if the actual value of Origin is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_id: (experimental) RequestId property. Specify an array of string values to match this event if the actual value of RequestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param start_time: (experimental) StartTime property. Specify an array of string values to match this event if the actual value of StartTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) StatusCode property. Specify an array of string values to match this event if the actual value of StatusCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_message: (experimental) StatusMessage property. Specify an array of string values to match this event if the actual value of StatusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = AutoScalingGroupEvents.EC2InstanceLaunchUnsuccessful.EC2InstanceLaunchUnsuccessfulProps(
            activity_id=activity_id,
            auto_scaling_group_name=auto_scaling_group_name,
            cause=cause,
            description=description,
            destination=destination,
            details=details,
            ec2_instance_id=ec2_instance_id,
            end_time=end_time,
            event_metadata=event_metadata,
            origin=origin,
            request_id=request_id,
            start_time=start_time,
            status_code=status_code,
            status_message=status_message,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "eC2InstanceLaunchUnsuccessfulPattern", [options]))

    @jsii.member(jsii_name="eC2InstanceTerminateLifecycleActionPattern")
    def e_c2_instance_terminate_lifecycle_action_pattern(
        self,
        *,
        auto_scaling_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        destination: typing.Optional[typing.Sequence[builtins.str]] = None,
        ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        lifecycle_action_token: typing.Optional[typing.Sequence[builtins.str]] = None,
        lifecycle_hook_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        lifecycle_transition: typing.Optional[typing.Sequence[builtins.str]] = None,
        notification_metadata: typing.Optional[typing.Sequence[builtins.str]] = None,
        origin: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for AutoScalingGroup EC2 Instance-terminate Lifecycle Action.

        :param auto_scaling_group_name: (experimental) AutoScalingGroupName property. Specify an array of string values to match this event if the actual value of AutoScalingGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the AutoScalingGroup reference
        :param destination: (experimental) Destination property. Specify an array of string values to match this event if the actual value of Destination is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param ec2_instance_id: (experimental) EC2InstanceId property. Specify an array of string values to match this event if the actual value of EC2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param lifecycle_action_token: (experimental) LifecycleActionToken property. Specify an array of string values to match this event if the actual value of LifecycleActionToken is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param lifecycle_hook_name: (experimental) LifecycleHookName property. Specify an array of string values to match this event if the actual value of LifecycleHookName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param lifecycle_transition: (experimental) LifecycleTransition property. Specify an array of string values to match this event if the actual value of LifecycleTransition is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param notification_metadata: (experimental) NotificationMetadata property. Specify an array of string values to match this event if the actual value of NotificationMetadata is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param origin: (experimental) Origin property. Specify an array of string values to match this event if the actual value of Origin is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = AutoScalingGroupEvents.EC2InstanceTerminateLifecycleAction.EC2InstanceTerminateLifecycleActionProps(
            auto_scaling_group_name=auto_scaling_group_name,
            destination=destination,
            ec2_instance_id=ec2_instance_id,
            event_metadata=event_metadata,
            lifecycle_action_token=lifecycle_action_token,
            lifecycle_hook_name=lifecycle_hook_name,
            lifecycle_transition=lifecycle_transition,
            notification_metadata=notification_metadata,
            origin=origin,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "eC2InstanceTerminateLifecycleActionPattern", [options]))

    @jsii.member(jsii_name="eC2InstanceTerminateSuccessfulPattern")
    def e_c2_instance_terminate_successful_pattern(
        self,
        *,
        activity_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        auto_scaling_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        cause: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[typing.Sequence[builtins.str]] = None,
        destination: typing.Optional[typing.Sequence[builtins.str]] = None,
        details: typing.Optional[typing.Union["AutoScalingGroupEvents.EC2InstanceTerminateSuccessful.Details", typing.Dict[builtins.str, typing.Any]]] = None,
        ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_time: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        origin: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_time: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for AutoScalingGroup EC2 Instance Terminate Successful.

        :param activity_id: (experimental) ActivityId property. Specify an array of string values to match this event if the actual value of ActivityId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param auto_scaling_group_name: (experimental) AutoScalingGroupName property. Specify an array of string values to match this event if the actual value of AutoScalingGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the AutoScalingGroup reference
        :param cause: (experimental) Cause property. Specify an array of string values to match this event if the actual value of Cause is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param description: (experimental) Description property. Specify an array of string values to match this event if the actual value of Description is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param destination: (experimental) Destination property. Specify an array of string values to match this event if the actual value of Destination is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param details: (experimental) Details property. Specify an array of string values to match this event if the actual value of Details is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param ec2_instance_id: (experimental) EC2InstanceId property. Specify an array of string values to match this event if the actual value of EC2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param end_time: (experimental) EndTime property. Specify an array of string values to match this event if the actual value of EndTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param origin: (experimental) Origin property. Specify an array of string values to match this event if the actual value of Origin is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_id: (experimental) RequestId property. Specify an array of string values to match this event if the actual value of RequestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param start_time: (experimental) StartTime property. Specify an array of string values to match this event if the actual value of StartTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) StatusCode property. Specify an array of string values to match this event if the actual value of StatusCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_message: (experimental) StatusMessage property. Specify an array of string values to match this event if the actual value of StatusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = AutoScalingGroupEvents.EC2InstanceTerminateSuccessful.EC2InstanceTerminateSuccessfulProps(
            activity_id=activity_id,
            auto_scaling_group_name=auto_scaling_group_name,
            cause=cause,
            description=description,
            destination=destination,
            details=details,
            ec2_instance_id=ec2_instance_id,
            end_time=end_time,
            event_metadata=event_metadata,
            origin=origin,
            request_id=request_id,
            start_time=start_time,
            status_code=status_code,
            status_message=status_message,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "eC2InstanceTerminateSuccessfulPattern", [options]))

    @jsii.member(jsii_name="eC2InstanceTerminateUnsuccessfulPattern")
    def e_c2_instance_terminate_unsuccessful_pattern(
        self,
        *,
        activity_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        auto_scaling_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        cause: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[typing.Sequence[builtins.str]] = None,
        destination: typing.Optional[typing.Sequence[builtins.str]] = None,
        details: typing.Optional[typing.Union["AutoScalingGroupEvents.EC2InstanceTerminateUnsuccessful.Details", typing.Dict[builtins.str, typing.Any]]] = None,
        ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_time: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        origin: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_time: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for AutoScalingGroup EC2 Instance Terminate Unsuccessful.

        :param activity_id: (experimental) ActivityId property. Specify an array of string values to match this event if the actual value of ActivityId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param auto_scaling_group_name: (experimental) AutoScalingGroupName property. Specify an array of string values to match this event if the actual value of AutoScalingGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the AutoScalingGroup reference
        :param cause: (experimental) Cause property. Specify an array of string values to match this event if the actual value of Cause is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param description: (experimental) Description property. Specify an array of string values to match this event if the actual value of Description is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param destination: (experimental) Destination property. Specify an array of string values to match this event if the actual value of Destination is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param details: (experimental) Details property. Specify an array of string values to match this event if the actual value of Details is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param ec2_instance_id: (experimental) EC2InstanceId property. Specify an array of string values to match this event if the actual value of EC2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param end_time: (experimental) EndTime property. Specify an array of string values to match this event if the actual value of EndTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param origin: (experimental) Origin property. Specify an array of string values to match this event if the actual value of Origin is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_id: (experimental) RequestId property. Specify an array of string values to match this event if the actual value of RequestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param start_time: (experimental) StartTime property. Specify an array of string values to match this event if the actual value of StartTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_code: (experimental) StatusCode property. Specify an array of string values to match this event if the actual value of StatusCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param status_message: (experimental) StatusMessage property. Specify an array of string values to match this event if the actual value of StatusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = AutoScalingGroupEvents.EC2InstanceTerminateUnsuccessful.EC2InstanceTerminateUnsuccessfulProps(
            activity_id=activity_id,
            auto_scaling_group_name=auto_scaling_group_name,
            cause=cause,
            description=description,
            destination=destination,
            details=details,
            ec2_instance_id=ec2_instance_id,
            end_time=end_time,
            event_metadata=event_metadata,
            origin=origin,
            request_id=request_id,
            start_time=start_time,
            status_code=status_code,
            status_message=status_message,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "eC2InstanceTerminateUnsuccessfulPattern", [options]))

    class EC2InstanceLaunchLifecycleAction(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.events.AutoScalingGroupEvents.EC2InstanceLaunchLifecycleAction",
    ):
        '''(experimental) aws.autoscaling@EC2InstanceLaunchLifecycleAction event types for AutoScalingGroup.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_autoscaling import events as autoscaling_events
            
            e_c2_instance_launch_lifecycle_action = autoscaling_events.AutoScalingGroupEvents.EC2InstanceLaunchLifecycleAction()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.events.AutoScalingGroupEvents.EC2InstanceLaunchLifecycleAction.EC2InstanceLaunchLifecycleActionProps",
            jsii_struct_bases=[],
            name_mapping={
                "auto_scaling_group_name": "autoScalingGroupName",
                "destination": "destination",
                "ec2_instance_id": "ec2InstanceId",
                "event_metadata": "eventMetadata",
                "lifecycle_action_token": "lifecycleActionToken",
                "lifecycle_hook_name": "lifecycleHookName",
                "lifecycle_transition": "lifecycleTransition",
                "notification_metadata": "notificationMetadata",
                "origin": "origin",
            },
        )
        class EC2InstanceLaunchLifecycleActionProps:
            def __init__(
                self,
                *,
                auto_scaling_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                destination: typing.Optional[typing.Sequence[builtins.str]] = None,
                ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                lifecycle_action_token: typing.Optional[typing.Sequence[builtins.str]] = None,
                lifecycle_hook_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                lifecycle_transition: typing.Optional[typing.Sequence[builtins.str]] = None,
                notification_metadata: typing.Optional[typing.Sequence[builtins.str]] = None,
                origin: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for AutoScalingGroup aws.autoscaling@EC2InstanceLaunchLifecycleAction event.

                :param auto_scaling_group_name: (experimental) AutoScalingGroupName property. Specify an array of string values to match this event if the actual value of AutoScalingGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the AutoScalingGroup reference
                :param destination: (experimental) Destination property. Specify an array of string values to match this event if the actual value of Destination is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ec2_instance_id: (experimental) EC2InstanceId property. Specify an array of string values to match this event if the actual value of EC2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param lifecycle_action_token: (experimental) LifecycleActionToken property. Specify an array of string values to match this event if the actual value of LifecycleActionToken is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param lifecycle_hook_name: (experimental) LifecycleHookName property. Specify an array of string values to match this event if the actual value of LifecycleHookName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param lifecycle_transition: (experimental) LifecycleTransition property. Specify an array of string values to match this event if the actual value of LifecycleTransition is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param notification_metadata: (experimental) NotificationMetadata property. Specify an array of string values to match this event if the actual value of NotificationMetadata is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param origin: (experimental) Origin property. Specify an array of string values to match this event if the actual value of Origin is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_autoscaling import events as autoscaling_events
                    
                    e_c2_instance_launch_lifecycle_action_props = autoscaling_events.AutoScalingGroupEvents.EC2InstanceLaunchLifecycleAction.EC2InstanceLaunchLifecycleActionProps(
                        auto_scaling_group_name=["autoScalingGroupName"],
                        destination=["destination"],
                        ec2_instance_id=["ec2InstanceId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        lifecycle_action_token=["lifecycleActionToken"],
                        lifecycle_hook_name=["lifecycleHookName"],
                        lifecycle_transition=["lifecycleTransition"],
                        notification_metadata=["notificationMetadata"],
                        origin=["origin"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__602a08a9983785e5c470ccdf0da6fc9cdcf211e27bb9f7e1a752c446eae7c696)
                    check_type(argname="argument auto_scaling_group_name", value=auto_scaling_group_name, expected_type=type_hints["auto_scaling_group_name"])
                    check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                    check_type(argname="argument ec2_instance_id", value=ec2_instance_id, expected_type=type_hints["ec2_instance_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument lifecycle_action_token", value=lifecycle_action_token, expected_type=type_hints["lifecycle_action_token"])
                    check_type(argname="argument lifecycle_hook_name", value=lifecycle_hook_name, expected_type=type_hints["lifecycle_hook_name"])
                    check_type(argname="argument lifecycle_transition", value=lifecycle_transition, expected_type=type_hints["lifecycle_transition"])
                    check_type(argname="argument notification_metadata", value=notification_metadata, expected_type=type_hints["notification_metadata"])
                    check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if auto_scaling_group_name is not None:
                    self._values["auto_scaling_group_name"] = auto_scaling_group_name
                if destination is not None:
                    self._values["destination"] = destination
                if ec2_instance_id is not None:
                    self._values["ec2_instance_id"] = ec2_instance_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if lifecycle_action_token is not None:
                    self._values["lifecycle_action_token"] = lifecycle_action_token
                if lifecycle_hook_name is not None:
                    self._values["lifecycle_hook_name"] = lifecycle_hook_name
                if lifecycle_transition is not None:
                    self._values["lifecycle_transition"] = lifecycle_transition
                if notification_metadata is not None:
                    self._values["notification_metadata"] = notification_metadata
                if origin is not None:
                    self._values["origin"] = origin

            @builtins.property
            def auto_scaling_group_name(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) AutoScalingGroupName property.

                Specify an array of string values to match this event if the actual value of AutoScalingGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the AutoScalingGroup reference

                :stability: experimental
                '''
                result = self._values.get("auto_scaling_group_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def destination(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Destination property.

                Specify an array of string values to match this event if the actual value of Destination is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("destination")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def ec2_instance_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) EC2InstanceId property.

                Specify an array of string values to match this event if the actual value of EC2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

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
            def lifecycle_action_token(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) LifecycleActionToken property.

                Specify an array of string values to match this event if the actual value of LifecycleActionToken is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("lifecycle_action_token")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def lifecycle_hook_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) LifecycleHookName property.

                Specify an array of string values to match this event if the actual value of LifecycleHookName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("lifecycle_hook_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def lifecycle_transition(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) LifecycleTransition property.

                Specify an array of string values to match this event if the actual value of LifecycleTransition is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("lifecycle_transition")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def notification_metadata(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) NotificationMetadata property.

                Specify an array of string values to match this event if the actual value of NotificationMetadata is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("notification_metadata")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def origin(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Origin property.

                Specify an array of string values to match this event if the actual value of Origin is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("origin")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "EC2InstanceLaunchLifecycleActionProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class EC2InstanceLaunchSuccessful(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.events.AutoScalingGroupEvents.EC2InstanceLaunchSuccessful",
    ):
        '''(experimental) aws.autoscaling@EC2InstanceLaunchSuccessful event types for AutoScalingGroup.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_autoscaling import events as autoscaling_events
            
            e_c2_instance_launch_successful = autoscaling_events.AutoScalingGroupEvents.EC2InstanceLaunchSuccessful()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.events.AutoScalingGroupEvents.EC2InstanceLaunchSuccessful.Details",
            jsii_struct_bases=[],
            name_mapping={
                "availability_zone": "availabilityZone",
                "subnet_id": "subnetId",
            },
        )
        class Details:
            def __init__(
                self,
                *,
                availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
                subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Details.

                :param availability_zone: (experimental) Availability Zone property. Specify an array of string values to match this event if the actual value of Availability Zone is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param subnet_id: (experimental) Subnet ID property. Specify an array of string values to match this event if the actual value of Subnet ID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_autoscaling import events as autoscaling_events
                    
                    details = autoscaling_events.AutoScalingGroupEvents.EC2InstanceLaunchSuccessful.Details(
                        availability_zone=["availabilityZone"],
                        subnet_id=["subnetId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__41c045de150233a5afb5d5dce8c218dc22bcd1b80c1621af22a7b333715bb46b)
                    check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                    check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if availability_zone is not None:
                    self._values["availability_zone"] = availability_zone
                if subnet_id is not None:
                    self._values["subnet_id"] = subnet_id

            @builtins.property
            def availability_zone(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Availability Zone property.

                Specify an array of string values to match this event if the actual value of Availability Zone is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("availability_zone")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def subnet_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Subnet ID property.

                Specify an array of string values to match this event if the actual value of Subnet ID is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("subnet_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Details(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.events.AutoScalingGroupEvents.EC2InstanceLaunchSuccessful.EC2InstanceLaunchSuccessfulProps",
            jsii_struct_bases=[],
            name_mapping={
                "activity_id": "activityId",
                "auto_scaling_group_name": "autoScalingGroupName",
                "cause": "cause",
                "description": "description",
                "destination": "destination",
                "details": "details",
                "ec2_instance_id": "ec2InstanceId",
                "end_time": "endTime",
                "event_metadata": "eventMetadata",
                "origin": "origin",
                "request_id": "requestId",
                "start_time": "startTime",
                "status_code": "statusCode",
                "status_message": "statusMessage",
            },
        )
        class EC2InstanceLaunchSuccessfulProps:
            def __init__(
                self,
                *,
                activity_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                auto_scaling_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                cause: typing.Optional[typing.Sequence[builtins.str]] = None,
                description: typing.Optional[typing.Sequence[builtins.str]] = None,
                destination: typing.Optional[typing.Sequence[builtins.str]] = None,
                details: typing.Optional[typing.Union["AutoScalingGroupEvents.EC2InstanceLaunchSuccessful.Details", typing.Dict[builtins.str, typing.Any]]] = None,
                ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                origin: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                start_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for AutoScalingGroup aws.autoscaling@EC2InstanceLaunchSuccessful event.

                :param activity_id: (experimental) ActivityId property. Specify an array of string values to match this event if the actual value of ActivityId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param auto_scaling_group_name: (experimental) AutoScalingGroupName property. Specify an array of string values to match this event if the actual value of AutoScalingGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the AutoScalingGroup reference
                :param cause: (experimental) Cause property. Specify an array of string values to match this event if the actual value of Cause is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param description: (experimental) Description property. Specify an array of string values to match this event if the actual value of Description is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param destination: (experimental) Destination property. Specify an array of string values to match this event if the actual value of Destination is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param details: (experimental) Details property. Specify an array of string values to match this event if the actual value of Details is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ec2_instance_id: (experimental) EC2InstanceId property. Specify an array of string values to match this event if the actual value of EC2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param end_time: (experimental) EndTime property. Specify an array of string values to match this event if the actual value of EndTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param origin: (experimental) Origin property. Specify an array of string values to match this event if the actual value of Origin is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) RequestId property. Specify an array of string values to match this event if the actual value of RequestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_time: (experimental) StartTime property. Specify an array of string values to match this event if the actual value of StartTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) StatusCode property. Specify an array of string values to match this event if the actual value of StatusCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_message: (experimental) StatusMessage property. Specify an array of string values to match this event if the actual value of StatusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_autoscaling import events as autoscaling_events
                    
                    e_c2_instance_launch_successful_props = autoscaling_events.AutoScalingGroupEvents.EC2InstanceLaunchSuccessful.EC2InstanceLaunchSuccessfulProps(
                        activity_id=["activityId"],
                        auto_scaling_group_name=["autoScalingGroupName"],
                        cause=["cause"],
                        description=["description"],
                        destination=["destination"],
                        details=autoscaling_events.AutoScalingGroupEvents.EC2InstanceLaunchSuccessful.Details(
                            availability_zone=["availabilityZone"],
                            subnet_id=["subnetId"]
                        ),
                        ec2_instance_id=["ec2InstanceId"],
                        end_time=["endTime"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        origin=["origin"],
                        request_id=["requestId"],
                        start_time=["startTime"],
                        status_code=["statusCode"],
                        status_message=["statusMessage"]
                    )
                '''
                if isinstance(details, dict):
                    details = AutoScalingGroupEvents.EC2InstanceLaunchSuccessful.Details(**details)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__0d5378d9519db6ce8f908400eaa1633b078a2360a3f9c21a978e5ee4702df882)
                    check_type(argname="argument activity_id", value=activity_id, expected_type=type_hints["activity_id"])
                    check_type(argname="argument auto_scaling_group_name", value=auto_scaling_group_name, expected_type=type_hints["auto_scaling_group_name"])
                    check_type(argname="argument cause", value=cause, expected_type=type_hints["cause"])
                    check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                    check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                    check_type(argname="argument details", value=details, expected_type=type_hints["details"])
                    check_type(argname="argument ec2_instance_id", value=ec2_instance_id, expected_type=type_hints["ec2_instance_id"])
                    check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                    check_type(argname="argument status_message", value=status_message, expected_type=type_hints["status_message"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if activity_id is not None:
                    self._values["activity_id"] = activity_id
                if auto_scaling_group_name is not None:
                    self._values["auto_scaling_group_name"] = auto_scaling_group_name
                if cause is not None:
                    self._values["cause"] = cause
                if description is not None:
                    self._values["description"] = description
                if destination is not None:
                    self._values["destination"] = destination
                if details is not None:
                    self._values["details"] = details
                if ec2_instance_id is not None:
                    self._values["ec2_instance_id"] = ec2_instance_id
                if end_time is not None:
                    self._values["end_time"] = end_time
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if origin is not None:
                    self._values["origin"] = origin
                if request_id is not None:
                    self._values["request_id"] = request_id
                if start_time is not None:
                    self._values["start_time"] = start_time
                if status_code is not None:
                    self._values["status_code"] = status_code
                if status_message is not None:
                    self._values["status_message"] = status_message

            @builtins.property
            def activity_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ActivityId property.

                Specify an array of string values to match this event if the actual value of ActivityId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("activity_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def auto_scaling_group_name(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) AutoScalingGroupName property.

                Specify an array of string values to match this event if the actual value of AutoScalingGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the AutoScalingGroup reference

                :stability: experimental
                '''
                result = self._values.get("auto_scaling_group_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def cause(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Cause property.

                Specify an array of string values to match this event if the actual value of Cause is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("cause")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def description(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Description property.

                Specify an array of string values to match this event if the actual value of Description is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("description")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def destination(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Destination property.

                Specify an array of string values to match this event if the actual value of Destination is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("destination")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def details(
                self,
            ) -> typing.Optional["AutoScalingGroupEvents.EC2InstanceLaunchSuccessful.Details"]:
                '''(experimental) Details property.

                Specify an array of string values to match this event if the actual value of Details is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("details")
                return typing.cast(typing.Optional["AutoScalingGroupEvents.EC2InstanceLaunchSuccessful.Details"], result)

            @builtins.property
            def ec2_instance_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) EC2InstanceId property.

                Specify an array of string values to match this event if the actual value of EC2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ec2_instance_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) EndTime property.

                Specify an array of string values to match this event if the actual value of EndTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_time")
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
            def origin(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Origin property.

                Specify an array of string values to match this event if the actual value of Origin is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("origin")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) RequestId property.

                Specify an array of string values to match this event if the actual value of RequestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def start_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) StartTime property.

                Specify an array of string values to match this event if the actual value of StartTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) StatusCode property.

                Specify an array of string values to match this event if the actual value of StatusCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) StatusMessage property.

                Specify an array of string values to match this event if the actual value of StatusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "EC2InstanceLaunchSuccessfulProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class EC2InstanceLaunchUnsuccessful(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.events.AutoScalingGroupEvents.EC2InstanceLaunchUnsuccessful",
    ):
        '''(experimental) aws.autoscaling@EC2InstanceLaunchUnsuccessful event types for AutoScalingGroup.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_autoscaling import events as autoscaling_events
            
            e_c2_instance_launch_unsuccessful = autoscaling_events.AutoScalingGroupEvents.EC2InstanceLaunchUnsuccessful()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.events.AutoScalingGroupEvents.EC2InstanceLaunchUnsuccessful.Details",
            jsii_struct_bases=[],
            name_mapping={
                "availability_zone": "availabilityZone",
                "subnet_id": "subnetId",
            },
        )
        class Details:
            def __init__(
                self,
                *,
                availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
                subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Details.

                :param availability_zone: (experimental) Availability Zone property. Specify an array of string values to match this event if the actual value of Availability Zone is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param subnet_id: (experimental) Subnet ID property. Specify an array of string values to match this event if the actual value of Subnet ID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_autoscaling import events as autoscaling_events
                    
                    details = autoscaling_events.AutoScalingGroupEvents.EC2InstanceLaunchUnsuccessful.Details(
                        availability_zone=["availabilityZone"],
                        subnet_id=["subnetId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__e4fb046caa412f093a6c21bc03cfc3ef3fd2526e7bd8a8218265f3d01de52d92)
                    check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                    check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if availability_zone is not None:
                    self._values["availability_zone"] = availability_zone
                if subnet_id is not None:
                    self._values["subnet_id"] = subnet_id

            @builtins.property
            def availability_zone(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Availability Zone property.

                Specify an array of string values to match this event if the actual value of Availability Zone is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("availability_zone")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def subnet_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Subnet ID property.

                Specify an array of string values to match this event if the actual value of Subnet ID is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("subnet_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Details(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.events.AutoScalingGroupEvents.EC2InstanceLaunchUnsuccessful.EC2InstanceLaunchUnsuccessfulProps",
            jsii_struct_bases=[],
            name_mapping={
                "activity_id": "activityId",
                "auto_scaling_group_name": "autoScalingGroupName",
                "cause": "cause",
                "description": "description",
                "destination": "destination",
                "details": "details",
                "ec2_instance_id": "ec2InstanceId",
                "end_time": "endTime",
                "event_metadata": "eventMetadata",
                "origin": "origin",
                "request_id": "requestId",
                "start_time": "startTime",
                "status_code": "statusCode",
                "status_message": "statusMessage",
            },
        )
        class EC2InstanceLaunchUnsuccessfulProps:
            def __init__(
                self,
                *,
                activity_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                auto_scaling_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                cause: typing.Optional[typing.Sequence[builtins.str]] = None,
                description: typing.Optional[typing.Sequence[builtins.str]] = None,
                destination: typing.Optional[typing.Sequence[builtins.str]] = None,
                details: typing.Optional[typing.Union["AutoScalingGroupEvents.EC2InstanceLaunchUnsuccessful.Details", typing.Dict[builtins.str, typing.Any]]] = None,
                ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                origin: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                start_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for AutoScalingGroup aws.autoscaling@EC2InstanceLaunchUnsuccessful event.

                :param activity_id: (experimental) ActivityId property. Specify an array of string values to match this event if the actual value of ActivityId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param auto_scaling_group_name: (experimental) AutoScalingGroupName property. Specify an array of string values to match this event if the actual value of AutoScalingGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the AutoScalingGroup reference
                :param cause: (experimental) Cause property. Specify an array of string values to match this event if the actual value of Cause is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param description: (experimental) Description property. Specify an array of string values to match this event if the actual value of Description is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param destination: (experimental) Destination property. Specify an array of string values to match this event if the actual value of Destination is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param details: (experimental) Details property. Specify an array of string values to match this event if the actual value of Details is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ec2_instance_id: (experimental) EC2InstanceId property. Specify an array of string values to match this event if the actual value of EC2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param end_time: (experimental) EndTime property. Specify an array of string values to match this event if the actual value of EndTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param origin: (experimental) Origin property. Specify an array of string values to match this event if the actual value of Origin is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) RequestId property. Specify an array of string values to match this event if the actual value of RequestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_time: (experimental) StartTime property. Specify an array of string values to match this event if the actual value of StartTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) StatusCode property. Specify an array of string values to match this event if the actual value of StatusCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_message: (experimental) StatusMessage property. Specify an array of string values to match this event if the actual value of StatusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_autoscaling import events as autoscaling_events
                    
                    e_c2_instance_launch_unsuccessful_props = autoscaling_events.AutoScalingGroupEvents.EC2InstanceLaunchUnsuccessful.EC2InstanceLaunchUnsuccessfulProps(
                        activity_id=["activityId"],
                        auto_scaling_group_name=["autoScalingGroupName"],
                        cause=["cause"],
                        description=["description"],
                        destination=["destination"],
                        details=autoscaling_events.AutoScalingGroupEvents.EC2InstanceLaunchUnsuccessful.Details(
                            availability_zone=["availabilityZone"],
                            subnet_id=["subnetId"]
                        ),
                        ec2_instance_id=["ec2InstanceId"],
                        end_time=["endTime"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        origin=["origin"],
                        request_id=["requestId"],
                        start_time=["startTime"],
                        status_code=["statusCode"],
                        status_message=["statusMessage"]
                    )
                '''
                if isinstance(details, dict):
                    details = AutoScalingGroupEvents.EC2InstanceLaunchUnsuccessful.Details(**details)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__c964acf252951c78110207976d2f5321882843d2172708515433bc1509fa16de)
                    check_type(argname="argument activity_id", value=activity_id, expected_type=type_hints["activity_id"])
                    check_type(argname="argument auto_scaling_group_name", value=auto_scaling_group_name, expected_type=type_hints["auto_scaling_group_name"])
                    check_type(argname="argument cause", value=cause, expected_type=type_hints["cause"])
                    check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                    check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                    check_type(argname="argument details", value=details, expected_type=type_hints["details"])
                    check_type(argname="argument ec2_instance_id", value=ec2_instance_id, expected_type=type_hints["ec2_instance_id"])
                    check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                    check_type(argname="argument status_message", value=status_message, expected_type=type_hints["status_message"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if activity_id is not None:
                    self._values["activity_id"] = activity_id
                if auto_scaling_group_name is not None:
                    self._values["auto_scaling_group_name"] = auto_scaling_group_name
                if cause is not None:
                    self._values["cause"] = cause
                if description is not None:
                    self._values["description"] = description
                if destination is not None:
                    self._values["destination"] = destination
                if details is not None:
                    self._values["details"] = details
                if ec2_instance_id is not None:
                    self._values["ec2_instance_id"] = ec2_instance_id
                if end_time is not None:
                    self._values["end_time"] = end_time
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if origin is not None:
                    self._values["origin"] = origin
                if request_id is not None:
                    self._values["request_id"] = request_id
                if start_time is not None:
                    self._values["start_time"] = start_time
                if status_code is not None:
                    self._values["status_code"] = status_code
                if status_message is not None:
                    self._values["status_message"] = status_message

            @builtins.property
            def activity_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ActivityId property.

                Specify an array of string values to match this event if the actual value of ActivityId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("activity_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def auto_scaling_group_name(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) AutoScalingGroupName property.

                Specify an array of string values to match this event if the actual value of AutoScalingGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the AutoScalingGroup reference

                :stability: experimental
                '''
                result = self._values.get("auto_scaling_group_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def cause(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Cause property.

                Specify an array of string values to match this event if the actual value of Cause is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("cause")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def description(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Description property.

                Specify an array of string values to match this event if the actual value of Description is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("description")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def destination(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Destination property.

                Specify an array of string values to match this event if the actual value of Destination is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("destination")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def details(
                self,
            ) -> typing.Optional["AutoScalingGroupEvents.EC2InstanceLaunchUnsuccessful.Details"]:
                '''(experimental) Details property.

                Specify an array of string values to match this event if the actual value of Details is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("details")
                return typing.cast(typing.Optional["AutoScalingGroupEvents.EC2InstanceLaunchUnsuccessful.Details"], result)

            @builtins.property
            def ec2_instance_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) EC2InstanceId property.

                Specify an array of string values to match this event if the actual value of EC2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ec2_instance_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) EndTime property.

                Specify an array of string values to match this event if the actual value of EndTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_time")
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
            def origin(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Origin property.

                Specify an array of string values to match this event if the actual value of Origin is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("origin")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) RequestId property.

                Specify an array of string values to match this event if the actual value of RequestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def start_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) StartTime property.

                Specify an array of string values to match this event if the actual value of StartTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) StatusCode property.

                Specify an array of string values to match this event if the actual value of StatusCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) StatusMessage property.

                Specify an array of string values to match this event if the actual value of StatusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "EC2InstanceLaunchUnsuccessfulProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class EC2InstanceTerminateLifecycleAction(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.events.AutoScalingGroupEvents.EC2InstanceTerminateLifecycleAction",
    ):
        '''(experimental) aws.autoscaling@EC2InstanceTerminateLifecycleAction event types for AutoScalingGroup.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_autoscaling import events as autoscaling_events
            
            e_c2_instance_terminate_lifecycle_action = autoscaling_events.AutoScalingGroupEvents.EC2InstanceTerminateLifecycleAction()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.events.AutoScalingGroupEvents.EC2InstanceTerminateLifecycleAction.EC2InstanceTerminateLifecycleActionProps",
            jsii_struct_bases=[],
            name_mapping={
                "auto_scaling_group_name": "autoScalingGroupName",
                "destination": "destination",
                "ec2_instance_id": "ec2InstanceId",
                "event_metadata": "eventMetadata",
                "lifecycle_action_token": "lifecycleActionToken",
                "lifecycle_hook_name": "lifecycleHookName",
                "lifecycle_transition": "lifecycleTransition",
                "notification_metadata": "notificationMetadata",
                "origin": "origin",
            },
        )
        class EC2InstanceTerminateLifecycleActionProps:
            def __init__(
                self,
                *,
                auto_scaling_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                destination: typing.Optional[typing.Sequence[builtins.str]] = None,
                ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                lifecycle_action_token: typing.Optional[typing.Sequence[builtins.str]] = None,
                lifecycle_hook_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                lifecycle_transition: typing.Optional[typing.Sequence[builtins.str]] = None,
                notification_metadata: typing.Optional[typing.Sequence[builtins.str]] = None,
                origin: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for AutoScalingGroup aws.autoscaling@EC2InstanceTerminateLifecycleAction event.

                :param auto_scaling_group_name: (experimental) AutoScalingGroupName property. Specify an array of string values to match this event if the actual value of AutoScalingGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the AutoScalingGroup reference
                :param destination: (experimental) Destination property. Specify an array of string values to match this event if the actual value of Destination is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ec2_instance_id: (experimental) EC2InstanceId property. Specify an array of string values to match this event if the actual value of EC2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param lifecycle_action_token: (experimental) LifecycleActionToken property. Specify an array of string values to match this event if the actual value of LifecycleActionToken is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param lifecycle_hook_name: (experimental) LifecycleHookName property. Specify an array of string values to match this event if the actual value of LifecycleHookName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param lifecycle_transition: (experimental) LifecycleTransition property. Specify an array of string values to match this event if the actual value of LifecycleTransition is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param notification_metadata: (experimental) NotificationMetadata property. Specify an array of string values to match this event if the actual value of NotificationMetadata is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param origin: (experimental) Origin property. Specify an array of string values to match this event if the actual value of Origin is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_autoscaling import events as autoscaling_events
                    
                    e_c2_instance_terminate_lifecycle_action_props = autoscaling_events.AutoScalingGroupEvents.EC2InstanceTerminateLifecycleAction.EC2InstanceTerminateLifecycleActionProps(
                        auto_scaling_group_name=["autoScalingGroupName"],
                        destination=["destination"],
                        ec2_instance_id=["ec2InstanceId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        lifecycle_action_token=["lifecycleActionToken"],
                        lifecycle_hook_name=["lifecycleHookName"],
                        lifecycle_transition=["lifecycleTransition"],
                        notification_metadata=["notificationMetadata"],
                        origin=["origin"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__4f24ef7dde0876c731e29fd87f5fa46788d7557c3037cccfdbab64fe865d69b4)
                    check_type(argname="argument auto_scaling_group_name", value=auto_scaling_group_name, expected_type=type_hints["auto_scaling_group_name"])
                    check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                    check_type(argname="argument ec2_instance_id", value=ec2_instance_id, expected_type=type_hints["ec2_instance_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument lifecycle_action_token", value=lifecycle_action_token, expected_type=type_hints["lifecycle_action_token"])
                    check_type(argname="argument lifecycle_hook_name", value=lifecycle_hook_name, expected_type=type_hints["lifecycle_hook_name"])
                    check_type(argname="argument lifecycle_transition", value=lifecycle_transition, expected_type=type_hints["lifecycle_transition"])
                    check_type(argname="argument notification_metadata", value=notification_metadata, expected_type=type_hints["notification_metadata"])
                    check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if auto_scaling_group_name is not None:
                    self._values["auto_scaling_group_name"] = auto_scaling_group_name
                if destination is not None:
                    self._values["destination"] = destination
                if ec2_instance_id is not None:
                    self._values["ec2_instance_id"] = ec2_instance_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if lifecycle_action_token is not None:
                    self._values["lifecycle_action_token"] = lifecycle_action_token
                if lifecycle_hook_name is not None:
                    self._values["lifecycle_hook_name"] = lifecycle_hook_name
                if lifecycle_transition is not None:
                    self._values["lifecycle_transition"] = lifecycle_transition
                if notification_metadata is not None:
                    self._values["notification_metadata"] = notification_metadata
                if origin is not None:
                    self._values["origin"] = origin

            @builtins.property
            def auto_scaling_group_name(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) AutoScalingGroupName property.

                Specify an array of string values to match this event if the actual value of AutoScalingGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the AutoScalingGroup reference

                :stability: experimental
                '''
                result = self._values.get("auto_scaling_group_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def destination(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Destination property.

                Specify an array of string values to match this event if the actual value of Destination is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("destination")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def ec2_instance_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) EC2InstanceId property.

                Specify an array of string values to match this event if the actual value of EC2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

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
            def lifecycle_action_token(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) LifecycleActionToken property.

                Specify an array of string values to match this event if the actual value of LifecycleActionToken is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("lifecycle_action_token")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def lifecycle_hook_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) LifecycleHookName property.

                Specify an array of string values to match this event if the actual value of LifecycleHookName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("lifecycle_hook_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def lifecycle_transition(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) LifecycleTransition property.

                Specify an array of string values to match this event if the actual value of LifecycleTransition is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("lifecycle_transition")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def notification_metadata(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) NotificationMetadata property.

                Specify an array of string values to match this event if the actual value of NotificationMetadata is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("notification_metadata")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def origin(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Origin property.

                Specify an array of string values to match this event if the actual value of Origin is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("origin")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "EC2InstanceTerminateLifecycleActionProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class EC2InstanceTerminateSuccessful(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.events.AutoScalingGroupEvents.EC2InstanceTerminateSuccessful",
    ):
        '''(experimental) aws.autoscaling@EC2InstanceTerminateSuccessful event types for AutoScalingGroup.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_autoscaling import events as autoscaling_events
            
            e_c2_instance_terminate_successful = autoscaling_events.AutoScalingGroupEvents.EC2InstanceTerminateSuccessful()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.events.AutoScalingGroupEvents.EC2InstanceTerminateSuccessful.Details",
            jsii_struct_bases=[],
            name_mapping={
                "availability_zone": "availabilityZone",
                "subnet_id": "subnetId",
            },
        )
        class Details:
            def __init__(
                self,
                *,
                availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
                subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Details.

                :param availability_zone: (experimental) Availability Zone property. Specify an array of string values to match this event if the actual value of Availability Zone is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param subnet_id: (experimental) Subnet ID property. Specify an array of string values to match this event if the actual value of Subnet ID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_autoscaling import events as autoscaling_events
                    
                    details = autoscaling_events.AutoScalingGroupEvents.EC2InstanceTerminateSuccessful.Details(
                        availability_zone=["availabilityZone"],
                        subnet_id=["subnetId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__b507a6c7c24fc81f22befb66ffa7052854f324501faa672a111e156a0f70e690)
                    check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                    check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if availability_zone is not None:
                    self._values["availability_zone"] = availability_zone
                if subnet_id is not None:
                    self._values["subnet_id"] = subnet_id

            @builtins.property
            def availability_zone(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Availability Zone property.

                Specify an array of string values to match this event if the actual value of Availability Zone is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("availability_zone")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def subnet_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Subnet ID property.

                Specify an array of string values to match this event if the actual value of Subnet ID is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("subnet_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Details(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.events.AutoScalingGroupEvents.EC2InstanceTerminateSuccessful.EC2InstanceTerminateSuccessfulProps",
            jsii_struct_bases=[],
            name_mapping={
                "activity_id": "activityId",
                "auto_scaling_group_name": "autoScalingGroupName",
                "cause": "cause",
                "description": "description",
                "destination": "destination",
                "details": "details",
                "ec2_instance_id": "ec2InstanceId",
                "end_time": "endTime",
                "event_metadata": "eventMetadata",
                "origin": "origin",
                "request_id": "requestId",
                "start_time": "startTime",
                "status_code": "statusCode",
                "status_message": "statusMessage",
            },
        )
        class EC2InstanceTerminateSuccessfulProps:
            def __init__(
                self,
                *,
                activity_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                auto_scaling_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                cause: typing.Optional[typing.Sequence[builtins.str]] = None,
                description: typing.Optional[typing.Sequence[builtins.str]] = None,
                destination: typing.Optional[typing.Sequence[builtins.str]] = None,
                details: typing.Optional[typing.Union["AutoScalingGroupEvents.EC2InstanceTerminateSuccessful.Details", typing.Dict[builtins.str, typing.Any]]] = None,
                ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                origin: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                start_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for AutoScalingGroup aws.autoscaling@EC2InstanceTerminateSuccessful event.

                :param activity_id: (experimental) ActivityId property. Specify an array of string values to match this event if the actual value of ActivityId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param auto_scaling_group_name: (experimental) AutoScalingGroupName property. Specify an array of string values to match this event if the actual value of AutoScalingGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the AutoScalingGroup reference
                :param cause: (experimental) Cause property. Specify an array of string values to match this event if the actual value of Cause is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param description: (experimental) Description property. Specify an array of string values to match this event if the actual value of Description is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param destination: (experimental) Destination property. Specify an array of string values to match this event if the actual value of Destination is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param details: (experimental) Details property. Specify an array of string values to match this event if the actual value of Details is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ec2_instance_id: (experimental) EC2InstanceId property. Specify an array of string values to match this event if the actual value of EC2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param end_time: (experimental) EndTime property. Specify an array of string values to match this event if the actual value of EndTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param origin: (experimental) Origin property. Specify an array of string values to match this event if the actual value of Origin is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) RequestId property. Specify an array of string values to match this event if the actual value of RequestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_time: (experimental) StartTime property. Specify an array of string values to match this event if the actual value of StartTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) StatusCode property. Specify an array of string values to match this event if the actual value of StatusCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_message: (experimental) StatusMessage property. Specify an array of string values to match this event if the actual value of StatusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_autoscaling import events as autoscaling_events
                    
                    e_c2_instance_terminate_successful_props = autoscaling_events.AutoScalingGroupEvents.EC2InstanceTerminateSuccessful.EC2InstanceTerminateSuccessfulProps(
                        activity_id=["activityId"],
                        auto_scaling_group_name=["autoScalingGroupName"],
                        cause=["cause"],
                        description=["description"],
                        destination=["destination"],
                        details=autoscaling_events.AutoScalingGroupEvents.EC2InstanceTerminateSuccessful.Details(
                            availability_zone=["availabilityZone"],
                            subnet_id=["subnetId"]
                        ),
                        ec2_instance_id=["ec2InstanceId"],
                        end_time=["endTime"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        origin=["origin"],
                        request_id=["requestId"],
                        start_time=["startTime"],
                        status_code=["statusCode"],
                        status_message=["statusMessage"]
                    )
                '''
                if isinstance(details, dict):
                    details = AutoScalingGroupEvents.EC2InstanceTerminateSuccessful.Details(**details)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__849fa2b01c3e601d09e9b93649a027c7dc784cc1812310bf79f56a020b7edb08)
                    check_type(argname="argument activity_id", value=activity_id, expected_type=type_hints["activity_id"])
                    check_type(argname="argument auto_scaling_group_name", value=auto_scaling_group_name, expected_type=type_hints["auto_scaling_group_name"])
                    check_type(argname="argument cause", value=cause, expected_type=type_hints["cause"])
                    check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                    check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                    check_type(argname="argument details", value=details, expected_type=type_hints["details"])
                    check_type(argname="argument ec2_instance_id", value=ec2_instance_id, expected_type=type_hints["ec2_instance_id"])
                    check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                    check_type(argname="argument status_message", value=status_message, expected_type=type_hints["status_message"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if activity_id is not None:
                    self._values["activity_id"] = activity_id
                if auto_scaling_group_name is not None:
                    self._values["auto_scaling_group_name"] = auto_scaling_group_name
                if cause is not None:
                    self._values["cause"] = cause
                if description is not None:
                    self._values["description"] = description
                if destination is not None:
                    self._values["destination"] = destination
                if details is not None:
                    self._values["details"] = details
                if ec2_instance_id is not None:
                    self._values["ec2_instance_id"] = ec2_instance_id
                if end_time is not None:
                    self._values["end_time"] = end_time
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if origin is not None:
                    self._values["origin"] = origin
                if request_id is not None:
                    self._values["request_id"] = request_id
                if start_time is not None:
                    self._values["start_time"] = start_time
                if status_code is not None:
                    self._values["status_code"] = status_code
                if status_message is not None:
                    self._values["status_message"] = status_message

            @builtins.property
            def activity_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ActivityId property.

                Specify an array of string values to match this event if the actual value of ActivityId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("activity_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def auto_scaling_group_name(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) AutoScalingGroupName property.

                Specify an array of string values to match this event if the actual value of AutoScalingGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the AutoScalingGroup reference

                :stability: experimental
                '''
                result = self._values.get("auto_scaling_group_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def cause(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Cause property.

                Specify an array of string values to match this event if the actual value of Cause is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("cause")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def description(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Description property.

                Specify an array of string values to match this event if the actual value of Description is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("description")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def destination(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Destination property.

                Specify an array of string values to match this event if the actual value of Destination is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("destination")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def details(
                self,
            ) -> typing.Optional["AutoScalingGroupEvents.EC2InstanceTerminateSuccessful.Details"]:
                '''(experimental) Details property.

                Specify an array of string values to match this event if the actual value of Details is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("details")
                return typing.cast(typing.Optional["AutoScalingGroupEvents.EC2InstanceTerminateSuccessful.Details"], result)

            @builtins.property
            def ec2_instance_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) EC2InstanceId property.

                Specify an array of string values to match this event if the actual value of EC2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ec2_instance_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) EndTime property.

                Specify an array of string values to match this event if the actual value of EndTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_time")
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
            def origin(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Origin property.

                Specify an array of string values to match this event if the actual value of Origin is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("origin")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) RequestId property.

                Specify an array of string values to match this event if the actual value of RequestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def start_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) StartTime property.

                Specify an array of string values to match this event if the actual value of StartTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) StatusCode property.

                Specify an array of string values to match this event if the actual value of StatusCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) StatusMessage property.

                Specify an array of string values to match this event if the actual value of StatusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "EC2InstanceTerminateSuccessfulProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class EC2InstanceTerminateUnsuccessful(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.events.AutoScalingGroupEvents.EC2InstanceTerminateUnsuccessful",
    ):
        '''(experimental) aws.autoscaling@EC2InstanceTerminateUnsuccessful event types for AutoScalingGroup.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_autoscaling import events as autoscaling_events
            
            e_c2_instance_terminate_unsuccessful = autoscaling_events.AutoScalingGroupEvents.EC2InstanceTerminateUnsuccessful()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.events.AutoScalingGroupEvents.EC2InstanceTerminateUnsuccessful.Details",
            jsii_struct_bases=[],
            name_mapping={
                "availability_zone": "availabilityZone",
                "subnet_id": "subnetId",
            },
        )
        class Details:
            def __init__(
                self,
                *,
                availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
                subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Details.

                :param availability_zone: (experimental) Availability Zone property. Specify an array of string values to match this event if the actual value of Availability Zone is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param subnet_id: (experimental) Subnet ID property. Specify an array of string values to match this event if the actual value of Subnet ID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_autoscaling import events as autoscaling_events
                    
                    details = autoscaling_events.AutoScalingGroupEvents.EC2InstanceTerminateUnsuccessful.Details(
                        availability_zone=["availabilityZone"],
                        subnet_id=["subnetId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__26300445befdb882925f476d1f827328e02ed79a7c526e3b5447893b612db273)
                    check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                    check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if availability_zone is not None:
                    self._values["availability_zone"] = availability_zone
                if subnet_id is not None:
                    self._values["subnet_id"] = subnet_id

            @builtins.property
            def availability_zone(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Availability Zone property.

                Specify an array of string values to match this event if the actual value of Availability Zone is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("availability_zone")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def subnet_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Subnet ID property.

                Specify an array of string values to match this event if the actual value of Subnet ID is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("subnet_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Details(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.events.AutoScalingGroupEvents.EC2InstanceTerminateUnsuccessful.EC2InstanceTerminateUnsuccessfulProps",
            jsii_struct_bases=[],
            name_mapping={
                "activity_id": "activityId",
                "auto_scaling_group_name": "autoScalingGroupName",
                "cause": "cause",
                "description": "description",
                "destination": "destination",
                "details": "details",
                "ec2_instance_id": "ec2InstanceId",
                "end_time": "endTime",
                "event_metadata": "eventMetadata",
                "origin": "origin",
                "request_id": "requestId",
                "start_time": "startTime",
                "status_code": "statusCode",
                "status_message": "statusMessage",
            },
        )
        class EC2InstanceTerminateUnsuccessfulProps:
            def __init__(
                self,
                *,
                activity_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                auto_scaling_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                cause: typing.Optional[typing.Sequence[builtins.str]] = None,
                description: typing.Optional[typing.Sequence[builtins.str]] = None,
                destination: typing.Optional[typing.Sequence[builtins.str]] = None,
                details: typing.Optional[typing.Union["AutoScalingGroupEvents.EC2InstanceTerminateUnsuccessful.Details", typing.Dict[builtins.str, typing.Any]]] = None,
                ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                end_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                origin: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                start_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for AutoScalingGroup aws.autoscaling@EC2InstanceTerminateUnsuccessful event.

                :param activity_id: (experimental) ActivityId property. Specify an array of string values to match this event if the actual value of ActivityId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param auto_scaling_group_name: (experimental) AutoScalingGroupName property. Specify an array of string values to match this event if the actual value of AutoScalingGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the AutoScalingGroup reference
                :param cause: (experimental) Cause property. Specify an array of string values to match this event if the actual value of Cause is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param description: (experimental) Description property. Specify an array of string values to match this event if the actual value of Description is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param destination: (experimental) Destination property. Specify an array of string values to match this event if the actual value of Destination is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param details: (experimental) Details property. Specify an array of string values to match this event if the actual value of Details is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ec2_instance_id: (experimental) EC2InstanceId property. Specify an array of string values to match this event if the actual value of EC2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param end_time: (experimental) EndTime property. Specify an array of string values to match this event if the actual value of EndTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param origin: (experimental) Origin property. Specify an array of string values to match this event if the actual value of Origin is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) RequestId property. Specify an array of string values to match this event if the actual value of RequestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param start_time: (experimental) StartTime property. Specify an array of string values to match this event if the actual value of StartTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) StatusCode property. Specify an array of string values to match this event if the actual value of StatusCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_message: (experimental) StatusMessage property. Specify an array of string values to match this event if the actual value of StatusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_autoscaling import events as autoscaling_events
                    
                    e_c2_instance_terminate_unsuccessful_props = autoscaling_events.AutoScalingGroupEvents.EC2InstanceTerminateUnsuccessful.EC2InstanceTerminateUnsuccessfulProps(
                        activity_id=["activityId"],
                        auto_scaling_group_name=["autoScalingGroupName"],
                        cause=["cause"],
                        description=["description"],
                        destination=["destination"],
                        details=autoscaling_events.AutoScalingGroupEvents.EC2InstanceTerminateUnsuccessful.Details(
                            availability_zone=["availabilityZone"],
                            subnet_id=["subnetId"]
                        ),
                        ec2_instance_id=["ec2InstanceId"],
                        end_time=["endTime"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        origin=["origin"],
                        request_id=["requestId"],
                        start_time=["startTime"],
                        status_code=["statusCode"],
                        status_message=["statusMessage"]
                    )
                '''
                if isinstance(details, dict):
                    details = AutoScalingGroupEvents.EC2InstanceTerminateUnsuccessful.Details(**details)
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__df2d8bbe9b3a3d722a8414f632d636848122b8370e71796fd94f0acaff707ced)
                    check_type(argname="argument activity_id", value=activity_id, expected_type=type_hints["activity_id"])
                    check_type(argname="argument auto_scaling_group_name", value=auto_scaling_group_name, expected_type=type_hints["auto_scaling_group_name"])
                    check_type(argname="argument cause", value=cause, expected_type=type_hints["cause"])
                    check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                    check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                    check_type(argname="argument details", value=details, expected_type=type_hints["details"])
                    check_type(argname="argument ec2_instance_id", value=ec2_instance_id, expected_type=type_hints["ec2_instance_id"])
                    check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                    check_type(argname="argument status_message", value=status_message, expected_type=type_hints["status_message"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if activity_id is not None:
                    self._values["activity_id"] = activity_id
                if auto_scaling_group_name is not None:
                    self._values["auto_scaling_group_name"] = auto_scaling_group_name
                if cause is not None:
                    self._values["cause"] = cause
                if description is not None:
                    self._values["description"] = description
                if destination is not None:
                    self._values["destination"] = destination
                if details is not None:
                    self._values["details"] = details
                if ec2_instance_id is not None:
                    self._values["ec2_instance_id"] = ec2_instance_id
                if end_time is not None:
                    self._values["end_time"] = end_time
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if origin is not None:
                    self._values["origin"] = origin
                if request_id is not None:
                    self._values["request_id"] = request_id
                if start_time is not None:
                    self._values["start_time"] = start_time
                if status_code is not None:
                    self._values["status_code"] = status_code
                if status_message is not None:
                    self._values["status_message"] = status_message

            @builtins.property
            def activity_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ActivityId property.

                Specify an array of string values to match this event if the actual value of ActivityId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("activity_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def auto_scaling_group_name(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) AutoScalingGroupName property.

                Specify an array of string values to match this event if the actual value of AutoScalingGroupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the AutoScalingGroup reference

                :stability: experimental
                '''
                result = self._values.get("auto_scaling_group_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def cause(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Cause property.

                Specify an array of string values to match this event if the actual value of Cause is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("cause")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def description(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Description property.

                Specify an array of string values to match this event if the actual value of Description is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("description")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def destination(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Destination property.

                Specify an array of string values to match this event if the actual value of Destination is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("destination")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def details(
                self,
            ) -> typing.Optional["AutoScalingGroupEvents.EC2InstanceTerminateUnsuccessful.Details"]:
                '''(experimental) Details property.

                Specify an array of string values to match this event if the actual value of Details is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("details")
                return typing.cast(typing.Optional["AutoScalingGroupEvents.EC2InstanceTerminateUnsuccessful.Details"], result)

            @builtins.property
            def ec2_instance_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) EC2InstanceId property.

                Specify an array of string values to match this event if the actual value of EC2InstanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ec2_instance_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def end_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) EndTime property.

                Specify an array of string values to match this event if the actual value of EndTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("end_time")
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
            def origin(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Origin property.

                Specify an array of string values to match this event if the actual value of Origin is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("origin")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) RequestId property.

                Specify an array of string values to match this event if the actual value of RequestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def start_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) StartTime property.

                Specify an array of string values to match this event if the actual value of StartTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("start_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) StatusCode property.

                Specify an array of string values to match this event if the actual value of StatusCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) StatusMessage property.

                Specify an array of string values to match this event if the actual value of StatusMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "EC2InstanceTerminateUnsuccessfulProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "AutoScalingGroupEvents",
]

publication.publish()

def _typecheckingstub__969e9a9ab78cc8e0d927bb6cc75bd3f471f7b0b3439b6bebcb043eab1ff95288(
    auto_scaling_group_ref: _aws_cdk_interfaces_aws_autoscaling_ceddda9d.IAutoScalingGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602a08a9983785e5c470ccdf0da6fc9cdcf211e27bb9f7e1a752c446eae7c696(
    *,
    auto_scaling_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    destination: typing.Optional[typing.Sequence[builtins.str]] = None,
    ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    lifecycle_action_token: typing.Optional[typing.Sequence[builtins.str]] = None,
    lifecycle_hook_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    lifecycle_transition: typing.Optional[typing.Sequence[builtins.str]] = None,
    notification_metadata: typing.Optional[typing.Sequence[builtins.str]] = None,
    origin: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c045de150233a5afb5d5dce8c218dc22bcd1b80c1621af22a7b333715bb46b(
    *,
    availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d5378d9519db6ce8f908400eaa1633b078a2360a3f9c21a978e5ee4702df882(
    *,
    activity_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    auto_scaling_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    cause: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[typing.Sequence[builtins.str]] = None,
    destination: typing.Optional[typing.Sequence[builtins.str]] = None,
    details: typing.Optional[typing.Union[AutoScalingGroupEvents.EC2InstanceLaunchSuccessful.Details, typing.Dict[builtins.str, typing.Any]]] = None,
    ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    origin: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4fb046caa412f093a6c21bc03cfc3ef3fd2526e7bd8a8218265f3d01de52d92(
    *,
    availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c964acf252951c78110207976d2f5321882843d2172708515433bc1509fa16de(
    *,
    activity_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    auto_scaling_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    cause: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[typing.Sequence[builtins.str]] = None,
    destination: typing.Optional[typing.Sequence[builtins.str]] = None,
    details: typing.Optional[typing.Union[AutoScalingGroupEvents.EC2InstanceLaunchUnsuccessful.Details, typing.Dict[builtins.str, typing.Any]]] = None,
    ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    origin: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f24ef7dde0876c731e29fd87f5fa46788d7557c3037cccfdbab64fe865d69b4(
    *,
    auto_scaling_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    destination: typing.Optional[typing.Sequence[builtins.str]] = None,
    ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    lifecycle_action_token: typing.Optional[typing.Sequence[builtins.str]] = None,
    lifecycle_hook_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    lifecycle_transition: typing.Optional[typing.Sequence[builtins.str]] = None,
    notification_metadata: typing.Optional[typing.Sequence[builtins.str]] = None,
    origin: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b507a6c7c24fc81f22befb66ffa7052854f324501faa672a111e156a0f70e690(
    *,
    availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849fa2b01c3e601d09e9b93649a027c7dc784cc1812310bf79f56a020b7edb08(
    *,
    activity_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    auto_scaling_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    cause: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[typing.Sequence[builtins.str]] = None,
    destination: typing.Optional[typing.Sequence[builtins.str]] = None,
    details: typing.Optional[typing.Union[AutoScalingGroupEvents.EC2InstanceTerminateSuccessful.Details, typing.Dict[builtins.str, typing.Any]]] = None,
    ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    origin: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26300445befdb882925f476d1f827328e02ed79a7c526e3b5447893b612db273(
    *,
    availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df2d8bbe9b3a3d722a8414f632d636848122b8370e71796fd94f0acaff707ced(
    *,
    activity_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    auto_scaling_group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    cause: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[typing.Sequence[builtins.str]] = None,
    destination: typing.Optional[typing.Sequence[builtins.str]] = None,
    details: typing.Optional[typing.Union[AutoScalingGroupEvents.EC2InstanceTerminateUnsuccessful.Details, typing.Dict[builtins.str, typing.Any]]] = None,
    ec2_instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    origin: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_message: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
