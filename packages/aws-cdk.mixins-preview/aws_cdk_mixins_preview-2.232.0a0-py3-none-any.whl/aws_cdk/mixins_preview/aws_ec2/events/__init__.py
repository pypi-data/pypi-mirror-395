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
import aws_cdk.interfaces.aws_ec2 as _aws_cdk_interfaces_aws_ec2_ceddda9d


class InstanceEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents",
):
    '''(experimental) EventBridge event patterns for Instance.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
        from aws_cdk.interfaces import aws_ec2 as interfaces_ec2
        
        # instance_ref: interfaces_ec2.IInstanceRef
        
        instance_events = ec2_events.InstanceEvents.from_instance(instance_ref)
    '''

    @jsii.member(jsii_name="fromInstance")
    @builtins.classmethod
    def from_instance(
        cls,
        instance_ref: _aws_cdk_interfaces_aws_ec2_ceddda9d.IInstanceRef,
    ) -> "InstanceEvents":
        '''(experimental) Create InstanceEvents from a Instance reference.

        :param instance_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5352af6d26a80d213c38949b3d48fe4eb34e4981293dfa424dc3a3055df2e5d)
            check_type(argname="argument instance_ref", value=instance_ref, expected_type=type_hints["instance_ref"])
        return typing.cast("InstanceEvents", jsii.sinvoke(cls, "fromInstance", [instance_ref]))

    @jsii.member(jsii_name="awsAPICallViaCloudTrailPattern")
    def aws_api_call_via_cloud_trail_pattern(
        self,
        *,
        aws_region: typing.Optional[typing.Sequence[builtins.str]] = None,
        error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
        error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_source: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_time: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_version: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_parameters: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.RequestParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        response_elements: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.ResponseElements", typing.Dict[builtins.str, typing.Any]]] = None,
        source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_identity: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.UserIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Instance AWS API Call via CloudTrail.

        :param aws_region: (experimental) awsRegion property. Specify an array of string values to match this event if the actual value of awsRegion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param error_code: (experimental) errorCode property. Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param error_message: (experimental) errorMessage property. Specify an array of string values to match this event if the actual value of errorMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_id: (experimental) eventID property. Specify an array of string values to match this event if the actual value of eventID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param event_name: (experimental) eventName property. Specify an array of string values to match this event if the actual value of eventName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_source: (experimental) eventSource property. Specify an array of string values to match this event if the actual value of eventSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_time: (experimental) eventTime property. Specify an array of string values to match this event if the actual value of eventTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_type: (experimental) eventType property. Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_version: (experimental) eventVersion property. Specify an array of string values to match this event if the actual value of eventVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_id: (experimental) requestID property. Specify an array of string values to match this event if the actual value of requestID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_parameters: (experimental) requestParameters property. Specify an array of string values to match this event if the actual value of requestParameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param response_elements: (experimental) responseElements property. Specify an array of string values to match this event if the actual value of responseElements is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_ip_address: (experimental) sourceIPAddress property. Specify an array of string values to match this event if the actual value of sourceIPAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param user_agent: (experimental) userAgent property. Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param user_identity: (experimental) userIdentity property. Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = InstanceEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps(
            aws_region=aws_region,
            error_code=error_code,
            error_message=error_message,
            event_id=event_id,
            event_metadata=event_metadata,
            event_name=event_name,
            event_source=event_source,
            event_time=event_time,
            event_type=event_type,
            event_version=event_version,
            request_id=request_id,
            request_parameters=request_parameters,
            response_elements=response_elements,
            source_ip_address=source_ip_address,
            user_agent=user_agent,
            user_identity=user_identity,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "awsAPICallViaCloudTrailPattern", [options]))

    @jsii.member(jsii_name="eC2InstanceStateChangeNotificationPattern")
    def e_c2_instance_state_change_notification_pattern(
        self,
        *,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        state: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Instance EC2 Instance State-change Notification.

        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param instance_id: (experimental) instance-id property. Specify an array of string values to match this event if the actual value of instance-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Instance reference
        :param state: (experimental) state property. Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = InstanceEvents.EC2InstanceStateChangeNotification.EC2InstanceStateChangeNotificationProps(
            event_metadata=event_metadata, instance_id=instance_id, state=state
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "eC2InstanceStateChangeNotificationPattern", [options]))

    @jsii.member(jsii_name="eC2SpotInstanceInterruptionWarningPattern")
    def e_c2_spot_instance_interruption_warning_pattern(
        self,
        *,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        instance_action: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Instance EC2 Spot Instance Interruption Warning.

        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param instance_action: (experimental) instance-action property. Specify an array of string values to match this event if the actual value of instance-action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param instance_id: (experimental) instance-id property. Specify an array of string values to match this event if the actual value of instance-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Instance reference

        :stability: experimental
        '''
        options = InstanceEvents.EC2SpotInstanceInterruptionWarning.EC2SpotInstanceInterruptionWarningProps(
            event_metadata=event_metadata,
            instance_action=instance_action,
            instance_id=instance_id,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "eC2SpotInstanceInterruptionWarningPattern", [options]))

    class AWSAPICallViaCloudTrail(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail",
    ):
        '''(experimental) aws.ec2@AWSAPICallViaCloudTrail event types for Instance.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
            
            a_wSAPICall_via_cloud_trail = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps",
            jsii_struct_bases=[],
            name_mapping={
                "aws_region": "awsRegion",
                "error_code": "errorCode",
                "error_message": "errorMessage",
                "event_id": "eventId",
                "event_metadata": "eventMetadata",
                "event_name": "eventName",
                "event_source": "eventSource",
                "event_time": "eventTime",
                "event_type": "eventType",
                "event_version": "eventVersion",
                "request_id": "requestId",
                "request_parameters": "requestParameters",
                "response_elements": "responseElements",
                "source_ip_address": "sourceIpAddress",
                "user_agent": "userAgent",
                "user_identity": "userIdentity",
            },
        )
        class AWSAPICallViaCloudTrailProps:
            def __init__(
                self,
                *,
                aws_region: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_source: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_parameters: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.RequestParameters", typing.Dict[builtins.str, typing.Any]]] = None,
                response_elements: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.ResponseElements", typing.Dict[builtins.str, typing.Any]]] = None,
                source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_identity: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.UserIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Props type for Instance aws.ec2@AWSAPICallViaCloudTrail event.

                :param aws_region: (experimental) awsRegion property. Specify an array of string values to match this event if the actual value of awsRegion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_code: (experimental) errorCode property. Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_message: (experimental) errorMessage property. Specify an array of string values to match this event if the actual value of errorMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_id: (experimental) eventID property. Specify an array of string values to match this event if the actual value of eventID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param event_name: (experimental) eventName property. Specify an array of string values to match this event if the actual value of eventName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_source: (experimental) eventSource property. Specify an array of string values to match this event if the actual value of eventSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_time: (experimental) eventTime property. Specify an array of string values to match this event if the actual value of eventTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_type: (experimental) eventType property. Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_version: (experimental) eventVersion property. Specify an array of string values to match this event if the actual value of eventVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) requestID property. Specify an array of string values to match this event if the actual value of requestID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_parameters: (experimental) requestParameters property. Specify an array of string values to match this event if the actual value of requestParameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param response_elements: (experimental) responseElements property. Specify an array of string values to match this event if the actual value of responseElements is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_ip_address: (experimental) sourceIPAddress property. Specify an array of string values to match this event if the actual value of sourceIPAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_agent: (experimental) userAgent property. Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_identity: (experimental) userIdentity property. Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    # overrides: Any
                    
                    a_wSAPICall_via_cloud_trail_props = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps(
                        aws_region=["awsRegion"],
                        error_code=["errorCode"],
                        error_message=["errorMessage"],
                        event_id=["eventId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        event_name=["eventName"],
                        event_source=["eventSource"],
                        event_time=["eventTime"],
                        event_type=["eventType"],
                        event_version=["eventVersion"],
                        request_id=["requestId"],
                        request_parameters=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.RequestParameters(
                            availability_zone=["availabilityZone"],
                            block_device_mapping=["blockDeviceMapping"],
                            client_token=["clientToken"],
                            create_fleet_request=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.CreateFleetRequest(
                                client_token=["clientToken"],
                                existing_instances=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.ExistingInstances(
                                    availability_zone=["availabilityZone"],
                                    count=["count"],
                                    instance_type=["instanceType"],
                                    market_option=["marketOption"],
                                    operating_system=["operatingSystem"],
                                    tag=["tag"]
                                ),
                                launch_template_configs=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateConfigs(
                                    launch_template_specification=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateSpecification(
                                        launch_template_id=["launchTemplateId"],
                                        version=["version"]
                                    ),
                                    overrides=[overrides],
                                    tag=["tag"]
                                ),
                                on_demand_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.OnDemandOptions(
                                    allocation_strategy=["allocationStrategy"],
                                    instance_pool_constraint_filter_disabled=["instancePoolConstraintFilterDisabled"],
                                    max_instance_count=["maxInstanceCount"],
                                    max_target_capacity=["maxTargetCapacity"]
                                ),
                                spot_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions(
                                    allocation_strategy=["allocationStrategy"],
                                    instance_pool_constraint_filter_disabled=["instancePoolConstraintFilterDisabled"],
                                    instance_pools_to_use_count=["instancePoolsToUseCount"],
                                    max_instance_count=["maxInstanceCount"],
                                    max_target_capacity=["maxTargetCapacity"]
                                ),
                                tag_specification=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecification(
                                    resource_type=["resourceType"],
                                    tag=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Tag(
                                        key=["key"],
                                        tag=["tag"],
                                        value=["value"]
                                    )
                                ),
                                target_capacity_specification=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TargetCapacitySpecification(
                                    default_target_capacity_type=["defaultTargetCapacityType"],
                                    on_demand_target_capacity=["onDemandTargetCapacity"],
                                    spot_target_capacity=["spotTargetCapacity"],
                                    total_target_capacity=["totalTargetCapacity"]
                                ),
                                type=["type"]
                            ),
                            create_launch_template_request=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.CreateLaunchTemplateRequest(
                                launch_template_data=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateData(
                                    image_id=["imageId"],
                                    instance_market_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceMarketOptions1(
                                        market_type=["marketType"],
                                        spot_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions2(
                                            max_price=["maxPrice"],
                                            spot_instance_type=["spotInstanceType"]
                                        )
                                    ),
                                    instance_type=["instanceType"],
                                    network_interface=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterface1(
                                        device_index=["deviceIndex"],
                                        security_group_id=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SecurityGroupId(
                                            content=["content"],
                                            tag=["tag"]
                                        ),
                                        subnet_id=["subnetId"],
                                        tag=["tag"]
                                    ),
                                    user_data=["userData"]
                                ),
                                launch_template_name=["launchTemplateName"]
                            ),
                            delete_launch_template_request=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateRequest(
                                launch_template_name=["launchTemplateName"]
                            ),
                            description=["description"],
                            disable_api_termination=["disableApiTermination"],
                            group_description=["groupDescription"],
                            group_id=["groupId"],
                            group_name=["groupName"],
                            group_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet1(
                                items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet1Item(
                                    group_id=["groupId"]
                                )]
                            ),
                            instance_market_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceMarketOptions(
                                market_type=["marketType"],
                                spot_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions1(
                                    max_price=["maxPrice"],
                                    spot_instance_type=["spotInstanceType"]
                                )
                            ),
                            instances_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet1(
                                items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet1Item(
                                    image_id=["imageId"],
                                    instance_id=["instanceId"],
                                    max_count=["maxCount"],
                                    min_count=["minCount"]
                                )]
                            ),
                            instance_type=["instanceType"],
                            ipv6_address_count=["ipv6AddressCount"],
                            launch_template=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate(
                                launch_template_id=["launchTemplateId"],
                                version=["version"]
                            ),
                            monitoring=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Monitoring(
                                enabled=["enabled"]
                            ),
                            network_interface_id=["networkInterfaceId"],
                            network_interface_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet(
                                items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSetItem(
                                    device_index=["deviceIndex"],
                                    subnet_id=["subnetId"]
                                )]
                            ),
                            private_ip_addresses_set=["privateIpAddressesSet"],
                            subnet_id=["subnetId"],
                            tag_specification_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSet(
                                items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItem(
                                    resource_type=["resourceType"],
                                    tags=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItemItem(
                                        key=["key"],
                                        value=["value"]
                                    )]
                                )]
                            ),
                            user_data=["userData"],
                            vpc_id=["vpcId"]
                        ),
                        response_elements=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.ResponseElements(
                            create_fleet_response=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.CreateFleetResponse(
                                error_set=["errorSet"],
                                fleet_id=["fleetId"],
                                fleet_instance_set=["fleetInstanceSet"],
                                request_id=["requestId"],
                                xmlns=["xmlns"]
                            ),
                            create_launch_template_response=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateResponse(
                                launch_template=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate1(
                                    created_by=["createdBy"],
                                    create_time=["createTime"],
                                    default_version_number=["defaultVersionNumber"],
                                    latest_version_number=["latestVersionNumber"],
                                    launch_template_id=["launchTemplateId"],
                                    launch_template_name=["launchTemplateName"]
                                ),
                                request_id=["requestId"],
                                xmlns=["xmlns"]
                            ),
                            delete_launch_template_response=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateResponse(
                                launch_template=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate1(
                                    created_by=["createdBy"],
                                    create_time=["createTime"],
                                    default_version_number=["defaultVersionNumber"],
                                    latest_version_number=["latestVersionNumber"],
                                    launch_template_id=["launchTemplateId"],
                                    launch_template_name=["launchTemplateName"]
                                ),
                                request_id=["requestId"],
                                xmlns=["xmlns"]
                            ),
                            group_id=["groupId"],
                            group_set=["groupSet"],
                            instances_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet(
                                items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstancesSetItem(
                                    ami_launch_index=["amiLaunchIndex"],
                                    architecture=["architecture"],
                                    block_device_mapping=["blockDeviceMapping"],
                                    capacity_reservation_specification=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.CapacityReservationSpecification(
                                        capacity_reservation_preference=["capacityReservationPreference"]
                                    ),
                                    client_token=["clientToken"],
                                    cpu_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.CpuOptions(
                                        core_count=["coreCount"],
                                        threads_per_core=["threadsPerCore"]
                                    ),
                                    current_state=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceState(
                                        code=["code"],
                                        name=["name"]
                                    ),
                                    ebs_optimized=["ebsOptimized"],
                                    enclave_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.EnclaveOptions(
                                        enabled=["enabled"]
                                    ),
                                    group_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2(
                                        items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item(
                                            group_id=["groupId"],
                                            group_name=["groupName"]
                                        )]
                                    ),
                                    hypervisor=["hypervisor"],
                                    image_id=["imageId"],
                                    instance_id=["instanceId"],
                                    instance_lifecycle=["instanceLifecycle"],
                                    instance_state=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceState(
                                        code=["code"],
                                        name=["name"]
                                    ),
                                    instance_type=["instanceType"],
                                    launch_time=["launchTime"],
                                    monitoring=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Monitoring1(
                                        state=["state"]
                                    ),
                                    network_interface_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1(
                                        items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1Item(
                                            attachment=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Attachment(
                                                attachment_id=["attachmentId"],
                                                attach_time=["attachTime"],
                                                delete_on_termination=["deleteOnTermination"],
                                                device_index=["deviceIndex"],
                                                status=["status"]
                                            ),
                                            group_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet3(
                                                items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item(
                                                    group_id=["groupId"],
                                                    group_name=["groupName"]
                                                )]
                                            ),
                                            interface_type=["interfaceType"],
                                            ipv6_addresses_set=["ipv6AddressesSet"],
                                            mac_address=["macAddress"],
                                            network_interface_id=["networkInterfaceId"],
                                            owner_id=["ownerId"],
                                            private_ip_address=["privateIpAddress"],
                                            private_ip_addresses_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet2(
                                                item=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item(
                                                    primary=["primary"],
                                                    private_ip_address=["privateIpAddress"]
                                                )]
                                            ),
                                            source_dest_check=["sourceDestCheck"],
                                            status=["status"],
                                            subnet_id=["subnetId"],
                                            tag_set=["tagSet"],
                                            vpc_id=["vpcId"]
                                        )]
                                    ),
                                    placement=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Placement(
                                        availability_zone=["availabilityZone"],
                                        tenancy=["tenancy"]
                                    ),
                                    previous_state=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceState(
                                        code=["code"],
                                        name=["name"]
                                    ),
                                    private_ip_address=["privateIpAddress"],
                                    product_codes=["productCodes"],
                                    root_device_name=["rootDeviceName"],
                                    root_device_type=["rootDeviceType"],
                                    source_dest_check=["sourceDestCheck"],
                                    spot_instance_request_id=["spotInstanceRequestId"],
                                    state_reason=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.StateReason(
                                        code=["code"],
                                        message=["message"]
                                    ),
                                    subnet_id=["subnetId"],
                                    tag_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSet(
                                        items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItemItem(
                                            key=["key"],
                                            value=["value"]
                                        )]
                                    ),
                                    virtualization_type=["virtualizationType"],
                                    vpc_id=["vpcId"]
                                )]
                            ),
                            network_interface=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterface(
                                availability_zone=["availabilityZone"],
                                description=["description"],
                                group_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2(
                                    items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item(
                                        group_id=["groupId"],
                                        group_name=["groupName"]
                                    )]
                                ),
                                interface_type=["interfaceType"],
                                ipv6_addresses_set=["ipv6AddressesSet"],
                                mac_address=["macAddress"],
                                network_interface_id=["networkInterfaceId"],
                                owner_id=["ownerId"],
                                private_ip_address=["privateIpAddress"],
                                private_ip_addresses_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1(
                                    item=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item(
                                        primary=["primary"],
                                        private_ip_address=["privateIpAddress"]
                                    )]
                                ),
                                requester_id=["requesterId"],
                                requester_managed=["requesterManaged"],
                                source_dest_check=["sourceDestCheck"],
                                status=["status"],
                                subnet_id=["subnetId"],
                                tag_set=["tagSet"],
                                vpc_id=["vpcId"]
                            ),
                            owner_id=["ownerId"],
                            requester_id=["requesterId"],
                            request_id=["requestId"],
                            reservation_id=["reservationId"],
                            return=["return"]
                        ),
                        source_ip_address=["sourceIpAddress"],
                        user_agent=["userAgent"],
                        user_identity=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.UserIdentity(
                            access_key_id=["accessKeyId"],
                            account_id=["accountId"],
                            arn=["arn"],
                            invoked_by=["invokedBy"],
                            principal_id=["principalId"],
                            session_context=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SessionContext(
                                attributes=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Attributes(
                                    creation_date=["creationDate"],
                                    mfa_authenticated=["mfaAuthenticated"]
                                ),
                                session_issuer=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                                    account_id=["accountId"],
                                    arn=["arn"],
                                    principal_id=["principalId"],
                                    type=["type"],
                                    user_name=["userName"]
                                ),
                                web_id_federation_data=["webIdFederationData"]
                            ),
                            type=["type"]
                        )
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(request_parameters, dict):
                    request_parameters = InstanceEvents.AWSAPICallViaCloudTrail.RequestParameters(**request_parameters)
                if isinstance(response_elements, dict):
                    response_elements = InstanceEvents.AWSAPICallViaCloudTrail.ResponseElements(**response_elements)
                if isinstance(user_identity, dict):
                    user_identity = InstanceEvents.AWSAPICallViaCloudTrail.UserIdentity(**user_identity)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__4af87d466137a8d2827d9ff6aec47b98251e0abb255638219bd66d2c82d440e1)
                    check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                    check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
                    check_type(argname="argument error_message", value=error_message, expected_type=type_hints["error_message"])
                    check_type(argname="argument event_id", value=event_id, expected_type=type_hints["event_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument event_name", value=event_name, expected_type=type_hints["event_name"])
                    check_type(argname="argument event_source", value=event_source, expected_type=type_hints["event_source"])
                    check_type(argname="argument event_time", value=event_time, expected_type=type_hints["event_time"])
                    check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
                    check_type(argname="argument event_version", value=event_version, expected_type=type_hints["event_version"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument request_parameters", value=request_parameters, expected_type=type_hints["request_parameters"])
                    check_type(argname="argument response_elements", value=response_elements, expected_type=type_hints["response_elements"])
                    check_type(argname="argument source_ip_address", value=source_ip_address, expected_type=type_hints["source_ip_address"])
                    check_type(argname="argument user_agent", value=user_agent, expected_type=type_hints["user_agent"])
                    check_type(argname="argument user_identity", value=user_identity, expected_type=type_hints["user_identity"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if aws_region is not None:
                    self._values["aws_region"] = aws_region
                if error_code is not None:
                    self._values["error_code"] = error_code
                if error_message is not None:
                    self._values["error_message"] = error_message
                if event_id is not None:
                    self._values["event_id"] = event_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if event_name is not None:
                    self._values["event_name"] = event_name
                if event_source is not None:
                    self._values["event_source"] = event_source
                if event_time is not None:
                    self._values["event_time"] = event_time
                if event_type is not None:
                    self._values["event_type"] = event_type
                if event_version is not None:
                    self._values["event_version"] = event_version
                if request_id is not None:
                    self._values["request_id"] = request_id
                if request_parameters is not None:
                    self._values["request_parameters"] = request_parameters
                if response_elements is not None:
                    self._values["response_elements"] = response_elements
                if source_ip_address is not None:
                    self._values["source_ip_address"] = source_ip_address
                if user_agent is not None:
                    self._values["user_agent"] = user_agent
                if user_identity is not None:
                    self._values["user_identity"] = user_identity

            @builtins.property
            def aws_region(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) awsRegion property.

                Specify an array of string values to match this event if the actual value of awsRegion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("aws_region")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def error_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) errorCode property.

                Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def error_message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) errorMessage property.

                Specify an array of string values to match this event if the actual value of errorMessage is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventID property.

                Specify an array of string values to match this event if the actual value of eventID is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_id")
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
            def event_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventName property.

                Specify an array of string values to match this event if the actual value of eventName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_source(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventSource property.

                Specify an array of string values to match this event if the actual value of eventSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_source")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventTime property.

                Specify an array of string values to match this event if the actual value of eventTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

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
            def event_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventVersion property.

                Specify an array of string values to match this event if the actual value of eventVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requestID property.

                Specify an array of string values to match this event if the actual value of requestID is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_parameters(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.RequestParameters"]:
                '''(experimental) requestParameters property.

                Specify an array of string values to match this event if the actual value of requestParameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_parameters")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.RequestParameters"], result)

            @builtins.property
            def response_elements(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.ResponseElements"]:
                '''(experimental) responseElements property.

                Specify an array of string values to match this event if the actual value of responseElements is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("response_elements")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.ResponseElements"], result)

            @builtins.property
            def source_ip_address(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sourceIPAddress property.

                Specify an array of string values to match this event if the actual value of sourceIPAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_ip_address")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def user_agent(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) userAgent property.

                Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_agent")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def user_identity(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.UserIdentity"]:
                '''(experimental) userIdentity property.

                Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_identity")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.UserIdentity"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AWSAPICallViaCloudTrailProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.Attachment",
            jsii_struct_bases=[],
            name_mapping={
                "attachment_id": "attachmentId",
                "attach_time": "attachTime",
                "delete_on_termination": "deleteOnTermination",
                "device_index": "deviceIndex",
                "status": "status",
            },
        )
        class Attachment:
            def __init__(
                self,
                *,
                attachment_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                attach_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                delete_on_termination: typing.Optional[typing.Sequence[builtins.str]] = None,
                device_index: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Attachment.

                :param attachment_id: (experimental) attachmentId property. Specify an array of string values to match this event if the actual value of attachmentId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param attach_time: (experimental) attachTime property. Specify an array of string values to match this event if the actual value of attachTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param delete_on_termination: (experimental) deleteOnTermination property. Specify an array of string values to match this event if the actual value of deleteOnTermination is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param device_index: (experimental) deviceIndex property. Specify an array of string values to match this event if the actual value of deviceIndex is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    attachment = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Attachment(
                        attachment_id=["attachmentId"],
                        attach_time=["attachTime"],
                        delete_on_termination=["deleteOnTermination"],
                        device_index=["deviceIndex"],
                        status=["status"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__374852cd79152bb3e2b21bd41510c83630fa3f8254a8934c5921cf1e5ec1d3b6)
                    check_type(argname="argument attachment_id", value=attachment_id, expected_type=type_hints["attachment_id"])
                    check_type(argname="argument attach_time", value=attach_time, expected_type=type_hints["attach_time"])
                    check_type(argname="argument delete_on_termination", value=delete_on_termination, expected_type=type_hints["delete_on_termination"])
                    check_type(argname="argument device_index", value=device_index, expected_type=type_hints["device_index"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if attachment_id is not None:
                    self._values["attachment_id"] = attachment_id
                if attach_time is not None:
                    self._values["attach_time"] = attach_time
                if delete_on_termination is not None:
                    self._values["delete_on_termination"] = delete_on_termination
                if device_index is not None:
                    self._values["device_index"] = device_index
                if status is not None:
                    self._values["status"] = status

            @builtins.property
            def attachment_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) attachmentId property.

                Specify an array of string values to match this event if the actual value of attachmentId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("attachment_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def attach_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) attachTime property.

                Specify an array of string values to match this event if the actual value of attachTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("attach_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def delete_on_termination(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) deleteOnTermination property.

                Specify an array of string values to match this event if the actual value of deleteOnTermination is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("delete_on_termination")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def device_index(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) deviceIndex property.

                Specify an array of string values to match this event if the actual value of deviceIndex is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("device_index")
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
                return "Attachment(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.Attributes",
            jsii_struct_bases=[],
            name_mapping={
                "creation_date": "creationDate",
                "mfa_authenticated": "mfaAuthenticated",
            },
        )
        class Attributes:
            def __init__(
                self,
                *,
                creation_date: typing.Optional[typing.Sequence[builtins.str]] = None,
                mfa_authenticated: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Attributes.

                :param creation_date: (experimental) creationDate property. Specify an array of string values to match this event if the actual value of creationDate is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mfa_authenticated: (experimental) mfaAuthenticated property. Specify an array of string values to match this event if the actual value of mfaAuthenticated is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    attributes = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Attributes(
                        creation_date=["creationDate"],
                        mfa_authenticated=["mfaAuthenticated"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__95aa3ccbce662e29b86925d318c10b8f5bc86123d62359de95adf412db7b4778)
                    check_type(argname="argument creation_date", value=creation_date, expected_type=type_hints["creation_date"])
                    check_type(argname="argument mfa_authenticated", value=mfa_authenticated, expected_type=type_hints["mfa_authenticated"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if creation_date is not None:
                    self._values["creation_date"] = creation_date
                if mfa_authenticated is not None:
                    self._values["mfa_authenticated"] = mfa_authenticated

            @builtins.property
            def creation_date(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) creationDate property.

                Specify an array of string values to match this event if the actual value of creationDate is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("creation_date")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mfa_authenticated(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mfaAuthenticated property.

                Specify an array of string values to match this event if the actual value of mfaAuthenticated is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mfa_authenticated")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Attributes(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.CapacityReservationSpecification",
            jsii_struct_bases=[],
            name_mapping={
                "capacity_reservation_preference": "capacityReservationPreference",
            },
        )
        class CapacityReservationSpecification:
            def __init__(
                self,
                *,
                capacity_reservation_preference: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for CapacityReservationSpecification.

                :param capacity_reservation_preference: (experimental) capacityReservationPreference property. Specify an array of string values to match this event if the actual value of capacityReservationPreference is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    capacity_reservation_specification = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.CapacityReservationSpecification(
                        capacity_reservation_preference=["capacityReservationPreference"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__748cf5f120b22b2689c0ebb0de0a16e4fee50d092544de275910e48d13e02eff)
                    check_type(argname="argument capacity_reservation_preference", value=capacity_reservation_preference, expected_type=type_hints["capacity_reservation_preference"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if capacity_reservation_preference is not None:
                    self._values["capacity_reservation_preference"] = capacity_reservation_preference

            @builtins.property
            def capacity_reservation_preference(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) capacityReservationPreference property.

                Specify an array of string values to match this event if the actual value of capacityReservationPreference is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("capacity_reservation_preference")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "CapacityReservationSpecification(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.CpuOptions",
            jsii_struct_bases=[],
            name_mapping={
                "core_count": "coreCount",
                "threads_per_core": "threadsPerCore",
            },
        )
        class CpuOptions:
            def __init__(
                self,
                *,
                core_count: typing.Optional[typing.Sequence[builtins.str]] = None,
                threads_per_core: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for CpuOptions.

                :param core_count: (experimental) coreCount property. Specify an array of string values to match this event if the actual value of coreCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param threads_per_core: (experimental) threadsPerCore property. Specify an array of string values to match this event if the actual value of threadsPerCore is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    cpu_options = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.CpuOptions(
                        core_count=["coreCount"],
                        threads_per_core=["threadsPerCore"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__161cc862e0be22e176f67d09de0f72b4ca72a6811654a376528d0818a16ce2b0)
                    check_type(argname="argument core_count", value=core_count, expected_type=type_hints["core_count"])
                    check_type(argname="argument threads_per_core", value=threads_per_core, expected_type=type_hints["threads_per_core"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if core_count is not None:
                    self._values["core_count"] = core_count
                if threads_per_core is not None:
                    self._values["threads_per_core"] = threads_per_core

            @builtins.property
            def core_count(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) coreCount property.

                Specify an array of string values to match this event if the actual value of coreCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("core_count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def threads_per_core(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) threadsPerCore property.

                Specify an array of string values to match this event if the actual value of threadsPerCore is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("threads_per_core")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "CpuOptions(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.CreateFleetRequest",
            jsii_struct_bases=[],
            name_mapping={
                "client_token": "clientToken",
                "existing_instances": "existingInstances",
                "launch_template_configs": "launchTemplateConfigs",
                "on_demand_options": "onDemandOptions",
                "spot_options": "spotOptions",
                "tag_specification": "tagSpecification",
                "target_capacity_specification": "targetCapacitySpecification",
                "type": "type",
            },
        )
        class CreateFleetRequest:
            def __init__(
                self,
                *,
                client_token: typing.Optional[typing.Sequence[builtins.str]] = None,
                existing_instances: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.ExistingInstances", typing.Dict[builtins.str, typing.Any]]] = None,
                launch_template_configs: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateConfigs", typing.Dict[builtins.str, typing.Any]]] = None,
                on_demand_options: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.OnDemandOptions", typing.Dict[builtins.str, typing.Any]]] = None,
                spot_options: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions", typing.Dict[builtins.str, typing.Any]]] = None,
                tag_specification: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.TagSpecification", typing.Dict[builtins.str, typing.Any]]] = None,
                target_capacity_specification: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.TargetCapacitySpecification", typing.Dict[builtins.str, typing.Any]]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for CreateFleetRequest.

                :param client_token: (experimental) ClientToken property. Specify an array of string values to match this event if the actual value of ClientToken is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param existing_instances: (experimental) ExistingInstances property. Specify an array of string values to match this event if the actual value of ExistingInstances is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param launch_template_configs: (experimental) LaunchTemplateConfigs property. Specify an array of string values to match this event if the actual value of LaunchTemplateConfigs is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param on_demand_options: (experimental) OnDemandOptions property. Specify an array of string values to match this event if the actual value of OnDemandOptions is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param spot_options: (experimental) SpotOptions property. Specify an array of string values to match this event if the actual value of SpotOptions is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tag_specification: (experimental) TagSpecification property. Specify an array of string values to match this event if the actual value of TagSpecification is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param target_capacity_specification: (experimental) TargetCapacitySpecification property. Specify an array of string values to match this event if the actual value of TargetCapacitySpecification is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) Type property. Specify an array of string values to match this event if the actual value of Type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    # overrides: Any
                    
                    create_fleet_request = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.CreateFleetRequest(
                        client_token=["clientToken"],
                        existing_instances=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.ExistingInstances(
                            availability_zone=["availabilityZone"],
                            count=["count"],
                            instance_type=["instanceType"],
                            market_option=["marketOption"],
                            operating_system=["operatingSystem"],
                            tag=["tag"]
                        ),
                        launch_template_configs=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateConfigs(
                            launch_template_specification=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateSpecification(
                                launch_template_id=["launchTemplateId"],
                                version=["version"]
                            ),
                            overrides=[overrides],
                            tag=["tag"]
                        ),
                        on_demand_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.OnDemandOptions(
                            allocation_strategy=["allocationStrategy"],
                            instance_pool_constraint_filter_disabled=["instancePoolConstraintFilterDisabled"],
                            max_instance_count=["maxInstanceCount"],
                            max_target_capacity=["maxTargetCapacity"]
                        ),
                        spot_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions(
                            allocation_strategy=["allocationStrategy"],
                            instance_pool_constraint_filter_disabled=["instancePoolConstraintFilterDisabled"],
                            instance_pools_to_use_count=["instancePoolsToUseCount"],
                            max_instance_count=["maxInstanceCount"],
                            max_target_capacity=["maxTargetCapacity"]
                        ),
                        tag_specification=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecification(
                            resource_type=["resourceType"],
                            tag=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Tag(
                                key=["key"],
                                tag=["tag"],
                                value=["value"]
                            )
                        ),
                        target_capacity_specification=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TargetCapacitySpecification(
                            default_target_capacity_type=["defaultTargetCapacityType"],
                            on_demand_target_capacity=["onDemandTargetCapacity"],
                            spot_target_capacity=["spotTargetCapacity"],
                            total_target_capacity=["totalTargetCapacity"]
                        ),
                        type=["type"]
                    )
                '''
                if isinstance(existing_instances, dict):
                    existing_instances = InstanceEvents.AWSAPICallViaCloudTrail.ExistingInstances(**existing_instances)
                if isinstance(launch_template_configs, dict):
                    launch_template_configs = InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateConfigs(**launch_template_configs)
                if isinstance(on_demand_options, dict):
                    on_demand_options = InstanceEvents.AWSAPICallViaCloudTrail.OnDemandOptions(**on_demand_options)
                if isinstance(spot_options, dict):
                    spot_options = InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions(**spot_options)
                if isinstance(tag_specification, dict):
                    tag_specification = InstanceEvents.AWSAPICallViaCloudTrail.TagSpecification(**tag_specification)
                if isinstance(target_capacity_specification, dict):
                    target_capacity_specification = InstanceEvents.AWSAPICallViaCloudTrail.TargetCapacitySpecification(**target_capacity_specification)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__030bd01279c90beb3a428ed91eb67b234fea18c57471c0c1dcffac1207b172f2)
                    check_type(argname="argument client_token", value=client_token, expected_type=type_hints["client_token"])
                    check_type(argname="argument existing_instances", value=existing_instances, expected_type=type_hints["existing_instances"])
                    check_type(argname="argument launch_template_configs", value=launch_template_configs, expected_type=type_hints["launch_template_configs"])
                    check_type(argname="argument on_demand_options", value=on_demand_options, expected_type=type_hints["on_demand_options"])
                    check_type(argname="argument spot_options", value=spot_options, expected_type=type_hints["spot_options"])
                    check_type(argname="argument tag_specification", value=tag_specification, expected_type=type_hints["tag_specification"])
                    check_type(argname="argument target_capacity_specification", value=target_capacity_specification, expected_type=type_hints["target_capacity_specification"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if client_token is not None:
                    self._values["client_token"] = client_token
                if existing_instances is not None:
                    self._values["existing_instances"] = existing_instances
                if launch_template_configs is not None:
                    self._values["launch_template_configs"] = launch_template_configs
                if on_demand_options is not None:
                    self._values["on_demand_options"] = on_demand_options
                if spot_options is not None:
                    self._values["spot_options"] = spot_options
                if tag_specification is not None:
                    self._values["tag_specification"] = tag_specification
                if target_capacity_specification is not None:
                    self._values["target_capacity_specification"] = target_capacity_specification
                if type is not None:
                    self._values["type"] = type

            @builtins.property
            def client_token(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ClientToken property.

                Specify an array of string values to match this event if the actual value of ClientToken is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("client_token")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def existing_instances(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.ExistingInstances"]:
                '''(experimental) ExistingInstances property.

                Specify an array of string values to match this event if the actual value of ExistingInstances is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("existing_instances")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.ExistingInstances"], result)

            @builtins.property
            def launch_template_configs(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateConfigs"]:
                '''(experimental) LaunchTemplateConfigs property.

                Specify an array of string values to match this event if the actual value of LaunchTemplateConfigs is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("launch_template_configs")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateConfigs"], result)

            @builtins.property
            def on_demand_options(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.OnDemandOptions"]:
                '''(experimental) OnDemandOptions property.

                Specify an array of string values to match this event if the actual value of OnDemandOptions is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("on_demand_options")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.OnDemandOptions"], result)

            @builtins.property
            def spot_options(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions"]:
                '''(experimental) SpotOptions property.

                Specify an array of string values to match this event if the actual value of SpotOptions is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("spot_options")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions"], result)

            @builtins.property
            def tag_specification(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.TagSpecification"]:
                '''(experimental) TagSpecification property.

                Specify an array of string values to match this event if the actual value of TagSpecification is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tag_specification")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.TagSpecification"], result)

            @builtins.property
            def target_capacity_specification(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.TargetCapacitySpecification"]:
                '''(experimental) TargetCapacitySpecification property.

                Specify an array of string values to match this event if the actual value of TargetCapacitySpecification is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("target_capacity_specification")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.TargetCapacitySpecification"], result)

            @builtins.property
            def type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Type property.

                Specify an array of string values to match this event if the actual value of Type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

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
                return "CreateFleetRequest(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.CreateFleetResponse",
            jsii_struct_bases=[],
            name_mapping={
                "error_set": "errorSet",
                "fleet_id": "fleetId",
                "fleet_instance_set": "fleetInstanceSet",
                "request_id": "requestId",
                "xmlns": "xmlns",
            },
        )
        class CreateFleetResponse:
            def __init__(
                self,
                *,
                error_set: typing.Optional[typing.Sequence[builtins.str]] = None,
                fleet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                fleet_instance_set: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                xmlns: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for CreateFleetResponse.

                :param error_set: (experimental) errorSet property. Specify an array of string values to match this event if the actual value of errorSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param fleet_id: (experimental) fleetId property. Specify an array of string values to match this event if the actual value of fleetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param fleet_instance_set: (experimental) fleetInstanceSet property. Specify an array of string values to match this event if the actual value of fleetInstanceSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) requestId property. Specify an array of string values to match this event if the actual value of requestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param xmlns: (experimental) xmlns property. Specify an array of string values to match this event if the actual value of xmlns is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    create_fleet_response = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.CreateFleetResponse(
                        error_set=["errorSet"],
                        fleet_id=["fleetId"],
                        fleet_instance_set=["fleetInstanceSet"],
                        request_id=["requestId"],
                        xmlns=["xmlns"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__ada89cb7e7ef99166fdc7d51dac073f7d20ffe6ce0c819d403f15540c9aa5192)
                    check_type(argname="argument error_set", value=error_set, expected_type=type_hints["error_set"])
                    check_type(argname="argument fleet_id", value=fleet_id, expected_type=type_hints["fleet_id"])
                    check_type(argname="argument fleet_instance_set", value=fleet_instance_set, expected_type=type_hints["fleet_instance_set"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument xmlns", value=xmlns, expected_type=type_hints["xmlns"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if error_set is not None:
                    self._values["error_set"] = error_set
                if fleet_id is not None:
                    self._values["fleet_id"] = fleet_id
                if fleet_instance_set is not None:
                    self._values["fleet_instance_set"] = fleet_instance_set
                if request_id is not None:
                    self._values["request_id"] = request_id
                if xmlns is not None:
                    self._values["xmlns"] = xmlns

            @builtins.property
            def error_set(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) errorSet property.

                Specify an array of string values to match this event if the actual value of errorSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_set")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def fleet_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) fleetId property.

                Specify an array of string values to match this event if the actual value of fleetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("fleet_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def fleet_instance_set(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) fleetInstanceSet property.

                Specify an array of string values to match this event if the actual value of fleetInstanceSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("fleet_instance_set")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requestId property.

                Specify an array of string values to match this event if the actual value of requestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def xmlns(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) xmlns property.

                Specify an array of string values to match this event if the actual value of xmlns is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("xmlns")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "CreateFleetResponse(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.CreateLaunchTemplateRequest",
            jsii_struct_bases=[],
            name_mapping={
                "launch_template_data": "launchTemplateData",
                "launch_template_name": "launchTemplateName",
            },
        )
        class CreateLaunchTemplateRequest:
            def __init__(
                self,
                *,
                launch_template_data: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateData", typing.Dict[builtins.str, typing.Any]]] = None,
                launch_template_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for CreateLaunchTemplateRequest.

                :param launch_template_data: (experimental) LaunchTemplateData property. Specify an array of string values to match this event if the actual value of LaunchTemplateData is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param launch_template_name: (experimental) LaunchTemplateName property. Specify an array of string values to match this event if the actual value of LaunchTemplateName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    create_launch_template_request = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.CreateLaunchTemplateRequest(
                        launch_template_data=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateData(
                            image_id=["imageId"],
                            instance_market_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceMarketOptions1(
                                market_type=["marketType"],
                                spot_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions2(
                                    max_price=["maxPrice"],
                                    spot_instance_type=["spotInstanceType"]
                                )
                            ),
                            instance_type=["instanceType"],
                            network_interface=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterface1(
                                device_index=["deviceIndex"],
                                security_group_id=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SecurityGroupId(
                                    content=["content"],
                                    tag=["tag"]
                                ),
                                subnet_id=["subnetId"],
                                tag=["tag"]
                            ),
                            user_data=["userData"]
                        ),
                        launch_template_name=["launchTemplateName"]
                    )
                '''
                if isinstance(launch_template_data, dict):
                    launch_template_data = InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateData(**launch_template_data)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__f1c8e9e767b64411b510a673bebcbe1e4f971693a40e6e4a3ede667de41f9628)
                    check_type(argname="argument launch_template_data", value=launch_template_data, expected_type=type_hints["launch_template_data"])
                    check_type(argname="argument launch_template_name", value=launch_template_name, expected_type=type_hints["launch_template_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if launch_template_data is not None:
                    self._values["launch_template_data"] = launch_template_data
                if launch_template_name is not None:
                    self._values["launch_template_name"] = launch_template_name

            @builtins.property
            def launch_template_data(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateData"]:
                '''(experimental) LaunchTemplateData property.

                Specify an array of string values to match this event if the actual value of LaunchTemplateData is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("launch_template_data")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateData"], result)

            @builtins.property
            def launch_template_name(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) LaunchTemplateName property.

                Specify an array of string values to match this event if the actual value of LaunchTemplateName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("launch_template_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "CreateLaunchTemplateRequest(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateRequest",
            jsii_struct_bases=[],
            name_mapping={"launch_template_name": "launchTemplateName"},
        )
        class DeleteLaunchTemplateRequest:
            def __init__(
                self,
                *,
                launch_template_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for DeleteLaunchTemplateRequest.

                :param launch_template_name: (experimental) LaunchTemplateName property. Specify an array of string values to match this event if the actual value of LaunchTemplateName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    delete_launch_template_request = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateRequest(
                        launch_template_name=["launchTemplateName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__08250557ba6a2587a3fa94b1e2b14be7f21c3b5660c90403a43a469ff246df52)
                    check_type(argname="argument launch_template_name", value=launch_template_name, expected_type=type_hints["launch_template_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if launch_template_name is not None:
                    self._values["launch_template_name"] = launch_template_name

            @builtins.property
            def launch_template_name(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) LaunchTemplateName property.

                Specify an array of string values to match this event if the actual value of LaunchTemplateName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("launch_template_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "DeleteLaunchTemplateRequest(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateResponse",
            jsii_struct_bases=[],
            name_mapping={
                "launch_template": "launchTemplate",
                "request_id": "requestId",
                "xmlns": "xmlns",
            },
        )
        class DeleteLaunchTemplateResponse:
            def __init__(
                self,
                *,
                launch_template: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate1", typing.Dict[builtins.str, typing.Any]]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                xmlns: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for DeleteLaunchTemplateResponse.

                :param launch_template: (experimental) launchTemplate property. Specify an array of string values to match this event if the actual value of launchTemplate is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) requestId property. Specify an array of string values to match this event if the actual value of requestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param xmlns: (experimental) xmlns property. Specify an array of string values to match this event if the actual value of xmlns is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    delete_launch_template_response = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateResponse(
                        launch_template=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate1(
                            created_by=["createdBy"],
                            create_time=["createTime"],
                            default_version_number=["defaultVersionNumber"],
                            latest_version_number=["latestVersionNumber"],
                            launch_template_id=["launchTemplateId"],
                            launch_template_name=["launchTemplateName"]
                        ),
                        request_id=["requestId"],
                        xmlns=["xmlns"]
                    )
                '''
                if isinstance(launch_template, dict):
                    launch_template = InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate1(**launch_template)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__779e13250be5511f578ccc8669dfa3457a35153979a963336894df80c375a8ba)
                    check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument xmlns", value=xmlns, expected_type=type_hints["xmlns"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if launch_template is not None:
                    self._values["launch_template"] = launch_template
                if request_id is not None:
                    self._values["request_id"] = request_id
                if xmlns is not None:
                    self._values["xmlns"] = xmlns

            @builtins.property
            def launch_template(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate1"]:
                '''(experimental) launchTemplate property.

                Specify an array of string values to match this event if the actual value of launchTemplate is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("launch_template")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate1"], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requestId property.

                Specify an array of string values to match this event if the actual value of requestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def xmlns(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) xmlns property.

                Specify an array of string values to match this event if the actual value of xmlns is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("xmlns")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "DeleteLaunchTemplateResponse(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.EnclaveOptions",
            jsii_struct_bases=[],
            name_mapping={"enabled": "enabled"},
        )
        class EnclaveOptions:
            def __init__(
                self,
                *,
                enabled: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for EnclaveOptions.

                :param enabled: (experimental) enabled property. Specify an array of string values to match this event if the actual value of enabled is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    enclave_options = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.EnclaveOptions(
                        enabled=["enabled"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__8e9cc9dae10ec8e474e7434903ca02941e1ab10e1911599c3638a0aa8ef72db8)
                    check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if enabled is not None:
                    self._values["enabled"] = enabled

            @builtins.property
            def enabled(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) enabled property.

                Specify an array of string values to match this event if the actual value of enabled is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("enabled")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "EnclaveOptions(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.ExistingInstances",
            jsii_struct_bases=[],
            name_mapping={
                "availability_zone": "availabilityZone",
                "count": "count",
                "instance_type": "instanceType",
                "market_option": "marketOption",
                "operating_system": "operatingSystem",
                "tag": "tag",
            },
        )
        class ExistingInstances:
            def __init__(
                self,
                *,
                availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
                count: typing.Optional[typing.Sequence[builtins.str]] = None,
                instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                market_option: typing.Optional[typing.Sequence[builtins.str]] = None,
                operating_system: typing.Optional[typing.Sequence[builtins.str]] = None,
                tag: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ExistingInstances.

                :param availability_zone: (experimental) AvailabilityZone property. Specify an array of string values to match this event if the actual value of AvailabilityZone is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param count: (experimental) Count property. Specify an array of string values to match this event if the actual value of Count is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_type: (experimental) InstanceType property. Specify an array of string values to match this event if the actual value of InstanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param market_option: (experimental) MarketOption property. Specify an array of string values to match this event if the actual value of MarketOption is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param operating_system: (experimental) OperatingSystem property. Specify an array of string values to match this event if the actual value of OperatingSystem is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tag: (experimental) tag property. Specify an array of string values to match this event if the actual value of tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    existing_instances = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.ExistingInstances(
                        availability_zone=["availabilityZone"],
                        count=["count"],
                        instance_type=["instanceType"],
                        market_option=["marketOption"],
                        operating_system=["operatingSystem"],
                        tag=["tag"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__35919d85ab88b879ff221bc792c6117926a59a36971f14f0b35e3798ebf44ac1)
                    check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                    check_type(argname="argument count", value=count, expected_type=type_hints["count"])
                    check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                    check_type(argname="argument market_option", value=market_option, expected_type=type_hints["market_option"])
                    check_type(argname="argument operating_system", value=operating_system, expected_type=type_hints["operating_system"])
                    check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if availability_zone is not None:
                    self._values["availability_zone"] = availability_zone
                if count is not None:
                    self._values["count"] = count
                if instance_type is not None:
                    self._values["instance_type"] = instance_type
                if market_option is not None:
                    self._values["market_option"] = market_option
                if operating_system is not None:
                    self._values["operating_system"] = operating_system
                if tag is not None:
                    self._values["tag"] = tag

            @builtins.property
            def availability_zone(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) AvailabilityZone property.

                Specify an array of string values to match this event if the actual value of AvailabilityZone is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("availability_zone")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def count(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Count property.

                Specify an array of string values to match this event if the actual value of Count is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def instance_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) InstanceType property.

                Specify an array of string values to match this event if the actual value of InstanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def market_option(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) MarketOption property.

                Specify an array of string values to match this event if the actual value of MarketOption is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("market_option")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def operating_system(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) OperatingSystem property.

                Specify an array of string values to match this event if the actual value of OperatingSystem is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("operating_system")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def tag(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) tag property.

                Specify an array of string values to match this event if the actual value of tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tag")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ExistingInstances(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet1",
            jsii_struct_bases=[],
            name_mapping={"items": "items"},
        )
        class GroupSet1:
            def __init__(
                self,
                *,
                items: typing.Optional[typing.Sequence[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet1Item", typing.Dict[builtins.str, typing.Any]]]] = None,
            ) -> None:
                '''(experimental) Type definition for GroupSet_1.

                :param items: (experimental) items property. Specify an array of string values to match this event if the actual value of items is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    group_set1 = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet1(
                        items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet1Item(
                            group_id=["groupId"]
                        )]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__1a3b7356f390410d4eaa38f16f303b0c971e4b7c81149a89a73898996acf265b)
                    check_type(argname="argument items", value=items, expected_type=type_hints["items"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if items is not None:
                    self._values["items"] = items

            @builtins.property
            def items(
                self,
            ) -> typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet1Item"]]:
                '''(experimental) items property.

                Specify an array of string values to match this event if the actual value of items is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("items")
                return typing.cast(typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet1Item"]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "GroupSet1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet1Item",
            jsii_struct_bases=[],
            name_mapping={"group_id": "groupId"},
        )
        class GroupSet1Item:
            def __init__(
                self,
                *,
                group_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for GroupSet_1Item.

                :param group_id: (experimental) groupId property. Specify an array of string values to match this event if the actual value of groupId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    group_set1_item = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet1Item(
                        group_id=["groupId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__cddda1126bc7b85ccfba6aebf3e054cbba3cdb5dcafa26b84075e9ba79945db5)
                    check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if group_id is not None:
                    self._values["group_id"] = group_id

            @builtins.property
            def group_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) groupId property.

                Specify an array of string values to match this event if the actual value of groupId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("group_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "GroupSet1Item(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2",
            jsii_struct_bases=[],
            name_mapping={"items": "items"},
        )
        class GroupSet2:
            def __init__(
                self,
                *,
                items: typing.Optional[typing.Sequence[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item", typing.Dict[builtins.str, typing.Any]]]] = None,
            ) -> None:
                '''(experimental) Type definition for GroupSet_2.

                :param items: (experimental) items property. Specify an array of string values to match this event if the actual value of items is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    group_set2 = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2(
                        items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item(
                            group_id=["groupId"],
                            group_name=["groupName"]
                        )]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__d762c5bfb573d4b7f5631beff7e6f2969ca63bee5a4a1d2092e135f67bfd5e47)
                    check_type(argname="argument items", value=items, expected_type=type_hints["items"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if items is not None:
                    self._values["items"] = items

            @builtins.property
            def items(
                self,
            ) -> typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item"]]:
                '''(experimental) items property.

                Specify an array of string values to match this event if the actual value of items is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("items")
                return typing.cast(typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item"]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "GroupSet2(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item",
            jsii_struct_bases=[],
            name_mapping={"group_id": "groupId", "group_name": "groupName"},
        )
        class GroupSet2Item:
            def __init__(
                self,
                *,
                group_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for GroupSet_2Item.

                :param group_id: (experimental) groupId property. Specify an array of string values to match this event if the actual value of groupId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param group_name: (experimental) groupName property. Specify an array of string values to match this event if the actual value of groupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    group_set2_item = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item(
                        group_id=["groupId"],
                        group_name=["groupName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__a838237263ddbfbc5d2146d11d3730e1fd756b278f6eda0003de1ed8635c30a0)
                    check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
                    check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if group_id is not None:
                    self._values["group_id"] = group_id
                if group_name is not None:
                    self._values["group_name"] = group_name

            @builtins.property
            def group_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) groupId property.

                Specify an array of string values to match this event if the actual value of groupId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("group_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def group_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) groupName property.

                Specify an array of string values to match this event if the actual value of groupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("group_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "GroupSet2Item(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet3",
            jsii_struct_bases=[],
            name_mapping={"items": "items"},
        )
        class GroupSet3:
            def __init__(
                self,
                *,
                items: typing.Optional[typing.Sequence[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item", typing.Dict[builtins.str, typing.Any]]]] = None,
            ) -> None:
                '''(experimental) Type definition for GroupSet_3.

                :param items: (experimental) items property. Specify an array of string values to match this event if the actual value of items is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    group_set3 = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet3(
                        items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item(
                            group_id=["groupId"],
                            group_name=["groupName"]
                        )]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__85c8f144ec0bdd769e9d662d98c595711fb128c42675ea2607ee0727d2560fb2)
                    check_type(argname="argument items", value=items, expected_type=type_hints["items"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if items is not None:
                    self._values["items"] = items

            @builtins.property
            def items(
                self,
            ) -> typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item"]]:
                '''(experimental) items property.

                Specify an array of string values to match this event if the actual value of items is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("items")
                return typing.cast(typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item"]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "GroupSet3(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceMarketOptions",
            jsii_struct_bases=[],
            name_mapping={"market_type": "marketType", "spot_options": "spotOptions"},
        )
        class InstanceMarketOptions:
            def __init__(
                self,
                *,
                market_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                spot_options: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions1", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for InstanceMarketOptions.

                :param market_type: (experimental) marketType property. Specify an array of string values to match this event if the actual value of marketType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param spot_options: (experimental) spotOptions property. Specify an array of string values to match this event if the actual value of spotOptions is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    instance_market_options = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceMarketOptions(
                        market_type=["marketType"],
                        spot_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions1(
                            max_price=["maxPrice"],
                            spot_instance_type=["spotInstanceType"]
                        )
                    )
                '''
                if isinstance(spot_options, dict):
                    spot_options = InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions1(**spot_options)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__5702b0e43e6cc4373bb45a5fba68c14c28bbffd2f827a70e4c35fb408462d98a)
                    check_type(argname="argument market_type", value=market_type, expected_type=type_hints["market_type"])
                    check_type(argname="argument spot_options", value=spot_options, expected_type=type_hints["spot_options"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if market_type is not None:
                    self._values["market_type"] = market_type
                if spot_options is not None:
                    self._values["spot_options"] = spot_options

            @builtins.property
            def market_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) marketType property.

                Specify an array of string values to match this event if the actual value of marketType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("market_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def spot_options(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions1"]:
                '''(experimental) spotOptions property.

                Specify an array of string values to match this event if the actual value of spotOptions is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("spot_options")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions1"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "InstanceMarketOptions(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceMarketOptions1",
            jsii_struct_bases=[],
            name_mapping={"market_type": "marketType", "spot_options": "spotOptions"},
        )
        class InstanceMarketOptions1:
            def __init__(
                self,
                *,
                market_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                spot_options: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions2", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for InstanceMarketOptions_1.

                :param market_type: (experimental) MarketType property. Specify an array of string values to match this event if the actual value of MarketType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param spot_options: (experimental) SpotOptions property. Specify an array of string values to match this event if the actual value of SpotOptions is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    instance_market_options1 = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceMarketOptions1(
                        market_type=["marketType"],
                        spot_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions2(
                            max_price=["maxPrice"],
                            spot_instance_type=["spotInstanceType"]
                        )
                    )
                '''
                if isinstance(spot_options, dict):
                    spot_options = InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions2(**spot_options)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__1c800b08c1a9a67ee7a77ac0489c5128b6bfdd52cfec82874d50a1a89d4ee620)
                    check_type(argname="argument market_type", value=market_type, expected_type=type_hints["market_type"])
                    check_type(argname="argument spot_options", value=spot_options, expected_type=type_hints["spot_options"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if market_type is not None:
                    self._values["market_type"] = market_type
                if spot_options is not None:
                    self._values["spot_options"] = spot_options

            @builtins.property
            def market_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) MarketType property.

                Specify an array of string values to match this event if the actual value of MarketType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("market_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def spot_options(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions2"]:
                '''(experimental) SpotOptions property.

                Specify an array of string values to match this event if the actual value of SpotOptions is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("spot_options")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions2"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "InstanceMarketOptions1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceState",
            jsii_struct_bases=[],
            name_mapping={"code": "code", "name": "name"},
        )
        class InstanceState:
            def __init__(
                self,
                *,
                code: typing.Optional[typing.Sequence[builtins.str]] = None,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for InstanceState.

                :param code: (experimental) code property. Specify an array of string values to match this event if the actual value of code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    instance_state = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceState(
                        code=["code"],
                        name=["name"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__ae6d0470565d233c804fe1145c175fedd14e0a45f9fce1ce5cf6b65183ce0a2d)
                    check_type(argname="argument code", value=code, expected_type=type_hints["code"])
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if code is not None:
                    self._values["code"] = code
                if name is not None:
                    self._values["name"] = name

            @builtins.property
            def code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) code property.

                Specify an array of string values to match this event if the actual value of code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "InstanceState(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet",
            jsii_struct_bases=[],
            name_mapping={"items": "items"},
        )
        class InstancesSet:
            def __init__(
                self,
                *,
                items: typing.Optional[typing.Sequence[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.InstancesSetItem", typing.Dict[builtins.str, typing.Any]]]] = None,
            ) -> None:
                '''(experimental) Type definition for InstancesSet.

                :param items: (experimental) items property. Specify an array of string values to match this event if the actual value of items is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    instances_set = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet(
                        items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstancesSetItem(
                            ami_launch_index=["amiLaunchIndex"],
                            architecture=["architecture"],
                            block_device_mapping=["blockDeviceMapping"],
                            capacity_reservation_specification=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.CapacityReservationSpecification(
                                capacity_reservation_preference=["capacityReservationPreference"]
                            ),
                            client_token=["clientToken"],
                            cpu_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.CpuOptions(
                                core_count=["coreCount"],
                                threads_per_core=["threadsPerCore"]
                            ),
                            current_state=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceState(
                                code=["code"],
                                name=["name"]
                            ),
                            ebs_optimized=["ebsOptimized"],
                            enclave_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.EnclaveOptions(
                                enabled=["enabled"]
                            ),
                            group_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2(
                                items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item(
                                    group_id=["groupId"],
                                    group_name=["groupName"]
                                )]
                            ),
                            hypervisor=["hypervisor"],
                            image_id=["imageId"],
                            instance_id=["instanceId"],
                            instance_lifecycle=["instanceLifecycle"],
                            instance_state=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceState(
                                code=["code"],
                                name=["name"]
                            ),
                            instance_type=["instanceType"],
                            launch_time=["launchTime"],
                            monitoring=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Monitoring1(
                                state=["state"]
                            ),
                            network_interface_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1(
                                items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1Item(
                                    attachment=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Attachment(
                                        attachment_id=["attachmentId"],
                                        attach_time=["attachTime"],
                                        delete_on_termination=["deleteOnTermination"],
                                        device_index=["deviceIndex"],
                                        status=["status"]
                                    ),
                                    group_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet3(
                                        items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item(
                                            group_id=["groupId"],
                                            group_name=["groupName"]
                                        )]
                                    ),
                                    interface_type=["interfaceType"],
                                    ipv6_addresses_set=["ipv6AddressesSet"],
                                    mac_address=["macAddress"],
                                    network_interface_id=["networkInterfaceId"],
                                    owner_id=["ownerId"],
                                    private_ip_address=["privateIpAddress"],
                                    private_ip_addresses_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet2(
                                        item=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item(
                                            primary=["primary"],
                                            private_ip_address=["privateIpAddress"]
                                        )]
                                    ),
                                    source_dest_check=["sourceDestCheck"],
                                    status=["status"],
                                    subnet_id=["subnetId"],
                                    tag_set=["tagSet"],
                                    vpc_id=["vpcId"]
                                )]
                            ),
                            placement=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Placement(
                                availability_zone=["availabilityZone"],
                                tenancy=["tenancy"]
                            ),
                            previous_state=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceState(
                                code=["code"],
                                name=["name"]
                            ),
                            private_ip_address=["privateIpAddress"],
                            product_codes=["productCodes"],
                            root_device_name=["rootDeviceName"],
                            root_device_type=["rootDeviceType"],
                            source_dest_check=["sourceDestCheck"],
                            spot_instance_request_id=["spotInstanceRequestId"],
                            state_reason=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.StateReason(
                                code=["code"],
                                message=["message"]
                            ),
                            subnet_id=["subnetId"],
                            tag_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSet(
                                items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItemItem(
                                    key=["key"],
                                    value=["value"]
                                )]
                            ),
                            virtualization_type=["virtualizationType"],
                            vpc_id=["vpcId"]
                        )]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__2f6c6129972df9dc8ac56a18bb37d5585d6796b520f03a5d64620d12011a06f9)
                    check_type(argname="argument items", value=items, expected_type=type_hints["items"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if items is not None:
                    self._values["items"] = items

            @builtins.property
            def items(
                self,
            ) -> typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.InstancesSetItem"]]:
                '''(experimental) items property.

                Specify an array of string values to match this event if the actual value of items is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("items")
                return typing.cast(typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.InstancesSetItem"]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "InstancesSet(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet1",
            jsii_struct_bases=[],
            name_mapping={"items": "items"},
        )
        class InstancesSet1:
            def __init__(
                self,
                *,
                items: typing.Optional[typing.Sequence[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet1Item", typing.Dict[builtins.str, typing.Any]]]] = None,
            ) -> None:
                '''(experimental) Type definition for InstancesSet_1.

                :param items: (experimental) items property. Specify an array of string values to match this event if the actual value of items is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    instances_set1 = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet1(
                        items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet1Item(
                            image_id=["imageId"],
                            instance_id=["instanceId"],
                            max_count=["maxCount"],
                            min_count=["minCount"]
                        )]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__2a810ec72970081dd109d62c211ca7eab09d61a759d93ba9c6aa6dbeb44be525)
                    check_type(argname="argument items", value=items, expected_type=type_hints["items"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if items is not None:
                    self._values["items"] = items

            @builtins.property
            def items(
                self,
            ) -> typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet1Item"]]:
                '''(experimental) items property.

                Specify an array of string values to match this event if the actual value of items is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("items")
                return typing.cast(typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet1Item"]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "InstancesSet1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet1Item",
            jsii_struct_bases=[],
            name_mapping={
                "image_id": "imageId",
                "instance_id": "instanceId",
                "max_count": "maxCount",
                "min_count": "minCount",
            },
        )
        class InstancesSet1Item:
            def __init__(
                self,
                *,
                image_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                max_count: typing.Optional[typing.Sequence[builtins.str]] = None,
                min_count: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for InstancesSet_1Item.

                :param image_id: (experimental) imageId property. Specify an array of string values to match this event if the actual value of imageId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_id: (experimental) instanceId property. Specify an array of string values to match this event if the actual value of instanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param max_count: (experimental) maxCount property. Specify an array of string values to match this event if the actual value of maxCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param min_count: (experimental) minCount property. Specify an array of string values to match this event if the actual value of minCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    instances_set1_item = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet1Item(
                        image_id=["imageId"],
                        instance_id=["instanceId"],
                        max_count=["maxCount"],
                        min_count=["minCount"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__78f9f1cf045d80b4b5e90f6d37685c83df33cfc9f8520c134cd6233069b3ccef)
                    check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
                    check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
                    check_type(argname="argument max_count", value=max_count, expected_type=type_hints["max_count"])
                    check_type(argname="argument min_count", value=min_count, expected_type=type_hints["min_count"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if image_id is not None:
                    self._values["image_id"] = image_id
                if instance_id is not None:
                    self._values["instance_id"] = instance_id
                if max_count is not None:
                    self._values["max_count"] = max_count
                if min_count is not None:
                    self._values["min_count"] = min_count

            @builtins.property
            def image_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageId property.

                Specify an array of string values to match this event if the actual value of imageId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def instance_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instanceId property.

                Specify an array of string values to match this event if the actual value of instanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def max_count(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) maxCount property.

                Specify an array of string values to match this event if the actual value of maxCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("max_count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def min_count(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) minCount property.

                Specify an array of string values to match this event if the actual value of minCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("min_count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "InstancesSet1Item(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.InstancesSetItem",
            jsii_struct_bases=[],
            name_mapping={
                "ami_launch_index": "amiLaunchIndex",
                "architecture": "architecture",
                "block_device_mapping": "blockDeviceMapping",
                "capacity_reservation_specification": "capacityReservationSpecification",
                "client_token": "clientToken",
                "cpu_options": "cpuOptions",
                "current_state": "currentState",
                "ebs_optimized": "ebsOptimized",
                "enclave_options": "enclaveOptions",
                "group_set": "groupSet",
                "hypervisor": "hypervisor",
                "image_id": "imageId",
                "instance_id": "instanceId",
                "instance_lifecycle": "instanceLifecycle",
                "instance_state": "instanceState",
                "instance_type": "instanceType",
                "launch_time": "launchTime",
                "monitoring": "monitoring",
                "network_interface_set": "networkInterfaceSet",
                "placement": "placement",
                "previous_state": "previousState",
                "private_ip_address": "privateIpAddress",
                "product_codes": "productCodes",
                "root_device_name": "rootDeviceName",
                "root_device_type": "rootDeviceType",
                "source_dest_check": "sourceDestCheck",
                "spot_instance_request_id": "spotInstanceRequestId",
                "state_reason": "stateReason",
                "subnet_id": "subnetId",
                "tag_set": "tagSet",
                "virtualization_type": "virtualizationType",
                "vpc_id": "vpcId",
            },
        )
        class InstancesSetItem:
            def __init__(
                self,
                *,
                ami_launch_index: typing.Optional[typing.Sequence[builtins.str]] = None,
                architecture: typing.Optional[typing.Sequence[builtins.str]] = None,
                block_device_mapping: typing.Optional[typing.Sequence[builtins.str]] = None,
                capacity_reservation_specification: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.CapacityReservationSpecification", typing.Dict[builtins.str, typing.Any]]] = None,
                client_token: typing.Optional[typing.Sequence[builtins.str]] = None,
                cpu_options: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.CpuOptions", typing.Dict[builtins.str, typing.Any]]] = None,
                current_state: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.InstanceState", typing.Dict[builtins.str, typing.Any]]] = None,
                ebs_optimized: typing.Optional[typing.Sequence[builtins.str]] = None,
                enclave_options: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.EnclaveOptions", typing.Dict[builtins.str, typing.Any]]] = None,
                group_set: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2", typing.Dict[builtins.str, typing.Any]]] = None,
                hypervisor: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                instance_lifecycle: typing.Optional[typing.Sequence[builtins.str]] = None,
                instance_state: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.InstanceState", typing.Dict[builtins.str, typing.Any]]] = None,
                instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                launch_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                monitoring: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.Monitoring1", typing.Dict[builtins.str, typing.Any]]] = None,
                network_interface_set: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1", typing.Dict[builtins.str, typing.Any]]] = None,
                placement: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.Placement", typing.Dict[builtins.str, typing.Any]]] = None,
                previous_state: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.InstanceState", typing.Dict[builtins.str, typing.Any]]] = None,
                private_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                product_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
                root_device_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                root_device_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_dest_check: typing.Optional[typing.Sequence[builtins.str]] = None,
                spot_instance_request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                state_reason: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.StateReason", typing.Dict[builtins.str, typing.Any]]] = None,
                subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                tag_set: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.TagSet", typing.Dict[builtins.str, typing.Any]]] = None,
                virtualization_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                vpc_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for InstancesSetItem.

                :param ami_launch_index: (experimental) amiLaunchIndex property. Specify an array of string values to match this event if the actual value of amiLaunchIndex is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param architecture: (experimental) architecture property. Specify an array of string values to match this event if the actual value of architecture is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param block_device_mapping: (experimental) blockDeviceMapping property. Specify an array of string values to match this event if the actual value of blockDeviceMapping is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param capacity_reservation_specification: (experimental) capacityReservationSpecification property. Specify an array of string values to match this event if the actual value of capacityReservationSpecification is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param client_token: (experimental) clientToken property. Specify an array of string values to match this event if the actual value of clientToken is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param cpu_options: (experimental) cpuOptions property. Specify an array of string values to match this event if the actual value of cpuOptions is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param current_state: (experimental) currentState property. Specify an array of string values to match this event if the actual value of currentState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ebs_optimized: (experimental) ebsOptimized property. Specify an array of string values to match this event if the actual value of ebsOptimized is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param enclave_options: (experimental) enclaveOptions property. Specify an array of string values to match this event if the actual value of enclaveOptions is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param group_set: (experimental) groupSet property. Specify an array of string values to match this event if the actual value of groupSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param hypervisor: (experimental) hypervisor property. Specify an array of string values to match this event if the actual value of hypervisor is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_id: (experimental) imageId property. Specify an array of string values to match this event if the actual value of imageId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_id: (experimental) instanceId property. Specify an array of string values to match this event if the actual value of instanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Instance reference
                :param instance_lifecycle: (experimental) instanceLifecycle property. Specify an array of string values to match this event if the actual value of instanceLifecycle is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_state: (experimental) instanceState property. Specify an array of string values to match this event if the actual value of instanceState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_type: (experimental) instanceType property. Specify an array of string values to match this event if the actual value of instanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param launch_time: (experimental) launchTime property. Specify an array of string values to match this event if the actual value of launchTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param monitoring: (experimental) monitoring property. Specify an array of string values to match this event if the actual value of monitoring is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param network_interface_set: (experimental) networkInterfaceSet property. Specify an array of string values to match this event if the actual value of networkInterfaceSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param placement: (experimental) placement property. Specify an array of string values to match this event if the actual value of placement is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param previous_state: (experimental) previousState property. Specify an array of string values to match this event if the actual value of previousState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param private_ip_address: (experimental) privateIpAddress property. Specify an array of string values to match this event if the actual value of privateIpAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param product_codes: (experimental) productCodes property. Specify an array of string values to match this event if the actual value of productCodes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param root_device_name: (experimental) rootDeviceName property. Specify an array of string values to match this event if the actual value of rootDeviceName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param root_device_type: (experimental) rootDeviceType property. Specify an array of string values to match this event if the actual value of rootDeviceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_dest_check: (experimental) sourceDestCheck property. Specify an array of string values to match this event if the actual value of sourceDestCheck is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param spot_instance_request_id: (experimental) spotInstanceRequestId property. Specify an array of string values to match this event if the actual value of spotInstanceRequestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param state_reason: (experimental) stateReason property. Specify an array of string values to match this event if the actual value of stateReason is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param subnet_id: (experimental) subnetId property. Specify an array of string values to match this event if the actual value of subnetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tag_set: (experimental) tagSet property. Specify an array of string values to match this event if the actual value of tagSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param virtualization_type: (experimental) virtualizationType property. Specify an array of string values to match this event if the actual value of virtualizationType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param vpc_id: (experimental) vpcId property. Specify an array of string values to match this event if the actual value of vpcId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    instances_set_item = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstancesSetItem(
                        ami_launch_index=["amiLaunchIndex"],
                        architecture=["architecture"],
                        block_device_mapping=["blockDeviceMapping"],
                        capacity_reservation_specification=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.CapacityReservationSpecification(
                            capacity_reservation_preference=["capacityReservationPreference"]
                        ),
                        client_token=["clientToken"],
                        cpu_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.CpuOptions(
                            core_count=["coreCount"],
                            threads_per_core=["threadsPerCore"]
                        ),
                        current_state=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceState(
                            code=["code"],
                            name=["name"]
                        ),
                        ebs_optimized=["ebsOptimized"],
                        enclave_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.EnclaveOptions(
                            enabled=["enabled"]
                        ),
                        group_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2(
                            items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item(
                                group_id=["groupId"],
                                group_name=["groupName"]
                            )]
                        ),
                        hypervisor=["hypervisor"],
                        image_id=["imageId"],
                        instance_id=["instanceId"],
                        instance_lifecycle=["instanceLifecycle"],
                        instance_state=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceState(
                            code=["code"],
                            name=["name"]
                        ),
                        instance_type=["instanceType"],
                        launch_time=["launchTime"],
                        monitoring=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Monitoring1(
                            state=["state"]
                        ),
                        network_interface_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1(
                            items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1Item(
                                attachment=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Attachment(
                                    attachment_id=["attachmentId"],
                                    attach_time=["attachTime"],
                                    delete_on_termination=["deleteOnTermination"],
                                    device_index=["deviceIndex"],
                                    status=["status"]
                                ),
                                group_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet3(
                                    items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item(
                                        group_id=["groupId"],
                                        group_name=["groupName"]
                                    )]
                                ),
                                interface_type=["interfaceType"],
                                ipv6_addresses_set=["ipv6AddressesSet"],
                                mac_address=["macAddress"],
                                network_interface_id=["networkInterfaceId"],
                                owner_id=["ownerId"],
                                private_ip_address=["privateIpAddress"],
                                private_ip_addresses_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet2(
                                    item=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item(
                                        primary=["primary"],
                                        private_ip_address=["privateIpAddress"]
                                    )]
                                ),
                                source_dest_check=["sourceDestCheck"],
                                status=["status"],
                                subnet_id=["subnetId"],
                                tag_set=["tagSet"],
                                vpc_id=["vpcId"]
                            )]
                        ),
                        placement=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Placement(
                            availability_zone=["availabilityZone"],
                            tenancy=["tenancy"]
                        ),
                        previous_state=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceState(
                            code=["code"],
                            name=["name"]
                        ),
                        private_ip_address=["privateIpAddress"],
                        product_codes=["productCodes"],
                        root_device_name=["rootDeviceName"],
                        root_device_type=["rootDeviceType"],
                        source_dest_check=["sourceDestCheck"],
                        spot_instance_request_id=["spotInstanceRequestId"],
                        state_reason=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.StateReason(
                            code=["code"],
                            message=["message"]
                        ),
                        subnet_id=["subnetId"],
                        tag_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSet(
                            items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItemItem(
                                key=["key"],
                                value=["value"]
                            )]
                        ),
                        virtualization_type=["virtualizationType"],
                        vpc_id=["vpcId"]
                    )
                '''
                if isinstance(capacity_reservation_specification, dict):
                    capacity_reservation_specification = InstanceEvents.AWSAPICallViaCloudTrail.CapacityReservationSpecification(**capacity_reservation_specification)
                if isinstance(cpu_options, dict):
                    cpu_options = InstanceEvents.AWSAPICallViaCloudTrail.CpuOptions(**cpu_options)
                if isinstance(current_state, dict):
                    current_state = InstanceEvents.AWSAPICallViaCloudTrail.InstanceState(**current_state)
                if isinstance(enclave_options, dict):
                    enclave_options = InstanceEvents.AWSAPICallViaCloudTrail.EnclaveOptions(**enclave_options)
                if isinstance(group_set, dict):
                    group_set = InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2(**group_set)
                if isinstance(instance_state, dict):
                    instance_state = InstanceEvents.AWSAPICallViaCloudTrail.InstanceState(**instance_state)
                if isinstance(monitoring, dict):
                    monitoring = InstanceEvents.AWSAPICallViaCloudTrail.Monitoring1(**monitoring)
                if isinstance(network_interface_set, dict):
                    network_interface_set = InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1(**network_interface_set)
                if isinstance(placement, dict):
                    placement = InstanceEvents.AWSAPICallViaCloudTrail.Placement(**placement)
                if isinstance(previous_state, dict):
                    previous_state = InstanceEvents.AWSAPICallViaCloudTrail.InstanceState(**previous_state)
                if isinstance(state_reason, dict):
                    state_reason = InstanceEvents.AWSAPICallViaCloudTrail.StateReason(**state_reason)
                if isinstance(tag_set, dict):
                    tag_set = InstanceEvents.AWSAPICallViaCloudTrail.TagSet(**tag_set)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__6b89073e73793af38f3e7003c25f44cf4b74eebecd8f187afeac59fe3ebc277b)
                    check_type(argname="argument ami_launch_index", value=ami_launch_index, expected_type=type_hints["ami_launch_index"])
                    check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
                    check_type(argname="argument block_device_mapping", value=block_device_mapping, expected_type=type_hints["block_device_mapping"])
                    check_type(argname="argument capacity_reservation_specification", value=capacity_reservation_specification, expected_type=type_hints["capacity_reservation_specification"])
                    check_type(argname="argument client_token", value=client_token, expected_type=type_hints["client_token"])
                    check_type(argname="argument cpu_options", value=cpu_options, expected_type=type_hints["cpu_options"])
                    check_type(argname="argument current_state", value=current_state, expected_type=type_hints["current_state"])
                    check_type(argname="argument ebs_optimized", value=ebs_optimized, expected_type=type_hints["ebs_optimized"])
                    check_type(argname="argument enclave_options", value=enclave_options, expected_type=type_hints["enclave_options"])
                    check_type(argname="argument group_set", value=group_set, expected_type=type_hints["group_set"])
                    check_type(argname="argument hypervisor", value=hypervisor, expected_type=type_hints["hypervisor"])
                    check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
                    check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
                    check_type(argname="argument instance_lifecycle", value=instance_lifecycle, expected_type=type_hints["instance_lifecycle"])
                    check_type(argname="argument instance_state", value=instance_state, expected_type=type_hints["instance_state"])
                    check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                    check_type(argname="argument launch_time", value=launch_time, expected_type=type_hints["launch_time"])
                    check_type(argname="argument monitoring", value=monitoring, expected_type=type_hints["monitoring"])
                    check_type(argname="argument network_interface_set", value=network_interface_set, expected_type=type_hints["network_interface_set"])
                    check_type(argname="argument placement", value=placement, expected_type=type_hints["placement"])
                    check_type(argname="argument previous_state", value=previous_state, expected_type=type_hints["previous_state"])
                    check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
                    check_type(argname="argument product_codes", value=product_codes, expected_type=type_hints["product_codes"])
                    check_type(argname="argument root_device_name", value=root_device_name, expected_type=type_hints["root_device_name"])
                    check_type(argname="argument root_device_type", value=root_device_type, expected_type=type_hints["root_device_type"])
                    check_type(argname="argument source_dest_check", value=source_dest_check, expected_type=type_hints["source_dest_check"])
                    check_type(argname="argument spot_instance_request_id", value=spot_instance_request_id, expected_type=type_hints["spot_instance_request_id"])
                    check_type(argname="argument state_reason", value=state_reason, expected_type=type_hints["state_reason"])
                    check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
                    check_type(argname="argument tag_set", value=tag_set, expected_type=type_hints["tag_set"])
                    check_type(argname="argument virtualization_type", value=virtualization_type, expected_type=type_hints["virtualization_type"])
                    check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if ami_launch_index is not None:
                    self._values["ami_launch_index"] = ami_launch_index
                if architecture is not None:
                    self._values["architecture"] = architecture
                if block_device_mapping is not None:
                    self._values["block_device_mapping"] = block_device_mapping
                if capacity_reservation_specification is not None:
                    self._values["capacity_reservation_specification"] = capacity_reservation_specification
                if client_token is not None:
                    self._values["client_token"] = client_token
                if cpu_options is not None:
                    self._values["cpu_options"] = cpu_options
                if current_state is not None:
                    self._values["current_state"] = current_state
                if ebs_optimized is not None:
                    self._values["ebs_optimized"] = ebs_optimized
                if enclave_options is not None:
                    self._values["enclave_options"] = enclave_options
                if group_set is not None:
                    self._values["group_set"] = group_set
                if hypervisor is not None:
                    self._values["hypervisor"] = hypervisor
                if image_id is not None:
                    self._values["image_id"] = image_id
                if instance_id is not None:
                    self._values["instance_id"] = instance_id
                if instance_lifecycle is not None:
                    self._values["instance_lifecycle"] = instance_lifecycle
                if instance_state is not None:
                    self._values["instance_state"] = instance_state
                if instance_type is not None:
                    self._values["instance_type"] = instance_type
                if launch_time is not None:
                    self._values["launch_time"] = launch_time
                if monitoring is not None:
                    self._values["monitoring"] = monitoring
                if network_interface_set is not None:
                    self._values["network_interface_set"] = network_interface_set
                if placement is not None:
                    self._values["placement"] = placement
                if previous_state is not None:
                    self._values["previous_state"] = previous_state
                if private_ip_address is not None:
                    self._values["private_ip_address"] = private_ip_address
                if product_codes is not None:
                    self._values["product_codes"] = product_codes
                if root_device_name is not None:
                    self._values["root_device_name"] = root_device_name
                if root_device_type is not None:
                    self._values["root_device_type"] = root_device_type
                if source_dest_check is not None:
                    self._values["source_dest_check"] = source_dest_check
                if spot_instance_request_id is not None:
                    self._values["spot_instance_request_id"] = spot_instance_request_id
                if state_reason is not None:
                    self._values["state_reason"] = state_reason
                if subnet_id is not None:
                    self._values["subnet_id"] = subnet_id
                if tag_set is not None:
                    self._values["tag_set"] = tag_set
                if virtualization_type is not None:
                    self._values["virtualization_type"] = virtualization_type
                if vpc_id is not None:
                    self._values["vpc_id"] = vpc_id

            @builtins.property
            def ami_launch_index(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) amiLaunchIndex property.

                Specify an array of string values to match this event if the actual value of amiLaunchIndex is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ami_launch_index")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def architecture(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) architecture property.

                Specify an array of string values to match this event if the actual value of architecture is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("architecture")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def block_device_mapping(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) blockDeviceMapping property.

                Specify an array of string values to match this event if the actual value of blockDeviceMapping is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("block_device_mapping")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def capacity_reservation_specification(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.CapacityReservationSpecification"]:
                '''(experimental) capacityReservationSpecification property.

                Specify an array of string values to match this event if the actual value of capacityReservationSpecification is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("capacity_reservation_specification")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.CapacityReservationSpecification"], result)

            @builtins.property
            def client_token(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) clientToken property.

                Specify an array of string values to match this event if the actual value of clientToken is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("client_token")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def cpu_options(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.CpuOptions"]:
                '''(experimental) cpuOptions property.

                Specify an array of string values to match this event if the actual value of cpuOptions is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("cpu_options")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.CpuOptions"], result)

            @builtins.property
            def current_state(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.InstanceState"]:
                '''(experimental) currentState property.

                Specify an array of string values to match this event if the actual value of currentState is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("current_state")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.InstanceState"], result)

            @builtins.property
            def ebs_optimized(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ebsOptimized property.

                Specify an array of string values to match this event if the actual value of ebsOptimized is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ebs_optimized")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def enclave_options(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.EnclaveOptions"]:
                '''(experimental) enclaveOptions property.

                Specify an array of string values to match this event if the actual value of enclaveOptions is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("enclave_options")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.EnclaveOptions"], result)

            @builtins.property
            def group_set(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2"]:
                '''(experimental) groupSet property.

                Specify an array of string values to match this event if the actual value of groupSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("group_set")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2"], result)

            @builtins.property
            def hypervisor(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) hypervisor property.

                Specify an array of string values to match this event if the actual value of hypervisor is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("hypervisor")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageId property.

                Specify an array of string values to match this event if the actual value of imageId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def instance_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instanceId property.

                Specify an array of string values to match this event if the actual value of instanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Instance reference

                :stability: experimental
                '''
                result = self._values.get("instance_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def instance_lifecycle(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instanceLifecycle property.

                Specify an array of string values to match this event if the actual value of instanceLifecycle is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_lifecycle")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def instance_state(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.InstanceState"]:
                '''(experimental) instanceState property.

                Specify an array of string values to match this event if the actual value of instanceState is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_state")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.InstanceState"], result)

            @builtins.property
            def instance_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instanceType property.

                Specify an array of string values to match this event if the actual value of instanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def launch_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) launchTime property.

                Specify an array of string values to match this event if the actual value of launchTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("launch_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def monitoring(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.Monitoring1"]:
                '''(experimental) monitoring property.

                Specify an array of string values to match this event if the actual value of monitoring is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("monitoring")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.Monitoring1"], result)

            @builtins.property
            def network_interface_set(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1"]:
                '''(experimental) networkInterfaceSet property.

                Specify an array of string values to match this event if the actual value of networkInterfaceSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("network_interface_set")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1"], result)

            @builtins.property
            def placement(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.Placement"]:
                '''(experimental) placement property.

                Specify an array of string values to match this event if the actual value of placement is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("placement")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.Placement"], result)

            @builtins.property
            def previous_state(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.InstanceState"]:
                '''(experimental) previousState property.

                Specify an array of string values to match this event if the actual value of previousState is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("previous_state")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.InstanceState"], result)

            @builtins.property
            def private_ip_address(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) privateIpAddress property.

                Specify an array of string values to match this event if the actual value of privateIpAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("private_ip_address")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def product_codes(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) productCodes property.

                Specify an array of string values to match this event if the actual value of productCodes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("product_codes")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def root_device_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) rootDeviceName property.

                Specify an array of string values to match this event if the actual value of rootDeviceName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("root_device_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def root_device_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) rootDeviceType property.

                Specify an array of string values to match this event if the actual value of rootDeviceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("root_device_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def source_dest_check(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sourceDestCheck property.

                Specify an array of string values to match this event if the actual value of sourceDestCheck is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_dest_check")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def spot_instance_request_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) spotInstanceRequestId property.

                Specify an array of string values to match this event if the actual value of spotInstanceRequestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("spot_instance_request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def state_reason(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.StateReason"]:
                '''(experimental) stateReason property.

                Specify an array of string values to match this event if the actual value of stateReason is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("state_reason")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.StateReason"], result)

            @builtins.property
            def subnet_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) subnetId property.

                Specify an array of string values to match this event if the actual value of subnetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("subnet_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def tag_set(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.TagSet"]:
                '''(experimental) tagSet property.

                Specify an array of string values to match this event if the actual value of tagSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tag_set")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.TagSet"], result)

            @builtins.property
            def virtualization_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) virtualizationType property.

                Specify an array of string values to match this event if the actual value of virtualizationType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("virtualization_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def vpc_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) vpcId property.

                Specify an array of string values to match this event if the actual value of vpcId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("vpc_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "InstancesSetItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate",
            jsii_struct_bases=[],
            name_mapping={
                "launch_template_id": "launchTemplateId",
                "version": "version",
            },
        )
        class LaunchTemplate:
            def __init__(
                self,
                *,
                launch_template_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for LaunchTemplate.

                :param launch_template_id: (experimental) launchTemplateId property. Specify an array of string values to match this event if the actual value of launchTemplateId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    launch_template = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate(
                        launch_template_id=["launchTemplateId"],
                        version=["version"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__86ab16eec5d4aed85cdbabefebe222f14bbd24a7c2c65ee8a17da46ee1c2f52d)
                    check_type(argname="argument launch_template_id", value=launch_template_id, expected_type=type_hints["launch_template_id"])
                    check_type(argname="argument version", value=version, expected_type=type_hints["version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if launch_template_id is not None:
                    self._values["launch_template_id"] = launch_template_id
                if version is not None:
                    self._values["version"] = version

            @builtins.property
            def launch_template_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) launchTemplateId property.

                Specify an array of string values to match this event if the actual value of launchTemplateId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("launch_template_id")
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
                return "LaunchTemplate(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate1",
            jsii_struct_bases=[],
            name_mapping={
                "created_by": "createdBy",
                "create_time": "createTime",
                "default_version_number": "defaultVersionNumber",
                "latest_version_number": "latestVersionNumber",
                "launch_template_id": "launchTemplateId",
                "launch_template_name": "launchTemplateName",
            },
        )
        class LaunchTemplate1:
            def __init__(
                self,
                *,
                created_by: typing.Optional[typing.Sequence[builtins.str]] = None,
                create_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                default_version_number: typing.Optional[typing.Sequence[builtins.str]] = None,
                latest_version_number: typing.Optional[typing.Sequence[builtins.str]] = None,
                launch_template_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                launch_template_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for LaunchTemplate_1.

                :param created_by: (experimental) createdBy property. Specify an array of string values to match this event if the actual value of createdBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param create_time: (experimental) createTime property. Specify an array of string values to match this event if the actual value of createTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param default_version_number: (experimental) defaultVersionNumber property. Specify an array of string values to match this event if the actual value of defaultVersionNumber is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param latest_version_number: (experimental) latestVersionNumber property. Specify an array of string values to match this event if the actual value of latestVersionNumber is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param launch_template_id: (experimental) launchTemplateId property. Specify an array of string values to match this event if the actual value of launchTemplateId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param launch_template_name: (experimental) launchTemplateName property. Specify an array of string values to match this event if the actual value of launchTemplateName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    launch_template1 = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate1(
                        created_by=["createdBy"],
                        create_time=["createTime"],
                        default_version_number=["defaultVersionNumber"],
                        latest_version_number=["latestVersionNumber"],
                        launch_template_id=["launchTemplateId"],
                        launch_template_name=["launchTemplateName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__a6d3a5b77c875b32e411ec34d1b46d0d009e9c485fd2cdbbdc32c3088a19dfc8)
                    check_type(argname="argument created_by", value=created_by, expected_type=type_hints["created_by"])
                    check_type(argname="argument create_time", value=create_time, expected_type=type_hints["create_time"])
                    check_type(argname="argument default_version_number", value=default_version_number, expected_type=type_hints["default_version_number"])
                    check_type(argname="argument latest_version_number", value=latest_version_number, expected_type=type_hints["latest_version_number"])
                    check_type(argname="argument launch_template_id", value=launch_template_id, expected_type=type_hints["launch_template_id"])
                    check_type(argname="argument launch_template_name", value=launch_template_name, expected_type=type_hints["launch_template_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if created_by is not None:
                    self._values["created_by"] = created_by
                if create_time is not None:
                    self._values["create_time"] = create_time
                if default_version_number is not None:
                    self._values["default_version_number"] = default_version_number
                if latest_version_number is not None:
                    self._values["latest_version_number"] = latest_version_number
                if launch_template_id is not None:
                    self._values["launch_template_id"] = launch_template_id
                if launch_template_name is not None:
                    self._values["launch_template_name"] = launch_template_name

            @builtins.property
            def created_by(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) createdBy property.

                Specify an array of string values to match this event if the actual value of createdBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("created_by")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def create_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) createTime property.

                Specify an array of string values to match this event if the actual value of createTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("create_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def default_version_number(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) defaultVersionNumber property.

                Specify an array of string values to match this event if the actual value of defaultVersionNumber is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("default_version_number")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def latest_version_number(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) latestVersionNumber property.

                Specify an array of string values to match this event if the actual value of latestVersionNumber is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("latest_version_number")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def launch_template_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) launchTemplateId property.

                Specify an array of string values to match this event if the actual value of launchTemplateId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("launch_template_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def launch_template_name(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) launchTemplateName property.

                Specify an array of string values to match this event if the actual value of launchTemplateName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("launch_template_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "LaunchTemplate1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateConfigs",
            jsii_struct_bases=[],
            name_mapping={
                "launch_template_specification": "launchTemplateSpecification",
                "overrides": "overrides",
                "tag": "tag",
            },
        )
        class LaunchTemplateConfigs:
            def __init__(
                self,
                *,
                launch_template_specification: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateSpecification", typing.Dict[builtins.str, typing.Any]]] = None,
                overrides: typing.Optional[typing.Sequence[typing.Any]] = None,
                tag: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for LaunchTemplateConfigs.

                :param launch_template_specification: (experimental) LaunchTemplateSpecification property. Specify an array of string values to match this event if the actual value of LaunchTemplateSpecification is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param overrides: (experimental) Overrides property. Specify an array of string values to match this event if the actual value of Overrides is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tag: (experimental) tag property. Specify an array of string values to match this event if the actual value of tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    # overrides: Any
                    
                    launch_template_configs = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateConfigs(
                        launch_template_specification=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateSpecification(
                            launch_template_id=["launchTemplateId"],
                            version=["version"]
                        ),
                        overrides=[overrides],
                        tag=["tag"]
                    )
                '''
                if isinstance(launch_template_specification, dict):
                    launch_template_specification = InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateSpecification(**launch_template_specification)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__f7fd4b54f27fa211d7355c7d77c6d259ec15ec460b2af4c5a58e2c4cf30023c3)
                    check_type(argname="argument launch_template_specification", value=launch_template_specification, expected_type=type_hints["launch_template_specification"])
                    check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
                    check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if launch_template_specification is not None:
                    self._values["launch_template_specification"] = launch_template_specification
                if overrides is not None:
                    self._values["overrides"] = overrides
                if tag is not None:
                    self._values["tag"] = tag

            @builtins.property
            def launch_template_specification(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateSpecification"]:
                '''(experimental) LaunchTemplateSpecification property.

                Specify an array of string values to match this event if the actual value of LaunchTemplateSpecification is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("launch_template_specification")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateSpecification"], result)

            @builtins.property
            def overrides(self) -> typing.Optional[typing.List[typing.Any]]:
                '''(experimental) Overrides property.

                Specify an array of string values to match this event if the actual value of Overrides is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("overrides")
                return typing.cast(typing.Optional[typing.List[typing.Any]], result)

            @builtins.property
            def tag(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) tag property.

                Specify an array of string values to match this event if the actual value of tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tag")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "LaunchTemplateConfigs(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateData",
            jsii_struct_bases=[],
            name_mapping={
                "image_id": "imageId",
                "instance_market_options": "instanceMarketOptions",
                "instance_type": "instanceType",
                "network_interface": "networkInterface",
                "user_data": "userData",
            },
        )
        class LaunchTemplateData:
            def __init__(
                self,
                *,
                image_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                instance_market_options: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.InstanceMarketOptions1", typing.Dict[builtins.str, typing.Any]]] = None,
                instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                network_interface: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterface1", typing.Dict[builtins.str, typing.Any]]] = None,
                user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for LaunchTemplateData.

                :param image_id: (experimental) ImageId property. Specify an array of string values to match this event if the actual value of ImageId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_market_options: (experimental) InstanceMarketOptions property. Specify an array of string values to match this event if the actual value of InstanceMarketOptions is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_type: (experimental) InstanceType property. Specify an array of string values to match this event if the actual value of InstanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param network_interface: (experimental) NetworkInterface property. Specify an array of string values to match this event if the actual value of NetworkInterface is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_data: (experimental) UserData property. Specify an array of string values to match this event if the actual value of UserData is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    launch_template_data = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateData(
                        image_id=["imageId"],
                        instance_market_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceMarketOptions1(
                            market_type=["marketType"],
                            spot_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions2(
                                max_price=["maxPrice"],
                                spot_instance_type=["spotInstanceType"]
                            )
                        ),
                        instance_type=["instanceType"],
                        network_interface=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterface1(
                            device_index=["deviceIndex"],
                            security_group_id=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SecurityGroupId(
                                content=["content"],
                                tag=["tag"]
                            ),
                            subnet_id=["subnetId"],
                            tag=["tag"]
                        ),
                        user_data=["userData"]
                    )
                '''
                if isinstance(instance_market_options, dict):
                    instance_market_options = InstanceEvents.AWSAPICallViaCloudTrail.InstanceMarketOptions1(**instance_market_options)
                if isinstance(network_interface, dict):
                    network_interface = InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterface1(**network_interface)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__95204bf01d0fd6dd98f65b9baf42ccfbbd41027f6343c2a6b358d2034d06fe4d)
                    check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
                    check_type(argname="argument instance_market_options", value=instance_market_options, expected_type=type_hints["instance_market_options"])
                    check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                    check_type(argname="argument network_interface", value=network_interface, expected_type=type_hints["network_interface"])
                    check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if image_id is not None:
                    self._values["image_id"] = image_id
                if instance_market_options is not None:
                    self._values["instance_market_options"] = instance_market_options
                if instance_type is not None:
                    self._values["instance_type"] = instance_type
                if network_interface is not None:
                    self._values["network_interface"] = network_interface
                if user_data is not None:
                    self._values["user_data"] = user_data

            @builtins.property
            def image_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ImageId property.

                Specify an array of string values to match this event if the actual value of ImageId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def instance_market_options(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.InstanceMarketOptions1"]:
                '''(experimental) InstanceMarketOptions property.

                Specify an array of string values to match this event if the actual value of InstanceMarketOptions is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_market_options")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.InstanceMarketOptions1"], result)

            @builtins.property
            def instance_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) InstanceType property.

                Specify an array of string values to match this event if the actual value of InstanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def network_interface(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterface1"]:
                '''(experimental) NetworkInterface property.

                Specify an array of string values to match this event if the actual value of NetworkInterface is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("network_interface")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterface1"], result)

            @builtins.property
            def user_data(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) UserData property.

                Specify an array of string values to match this event if the actual value of UserData is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_data")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "LaunchTemplateData(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateSpecification",
            jsii_struct_bases=[],
            name_mapping={
                "launch_template_id": "launchTemplateId",
                "version": "version",
            },
        )
        class LaunchTemplateSpecification:
            def __init__(
                self,
                *,
                launch_template_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for LaunchTemplateSpecification.

                :param launch_template_id: (experimental) LaunchTemplateId property. Specify an array of string values to match this event if the actual value of LaunchTemplateId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version: (experimental) Version property. Specify an array of string values to match this event if the actual value of Version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    launch_template_specification = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateSpecification(
                        launch_template_id=["launchTemplateId"],
                        version=["version"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__761e170e2e3e6f52ed74840d8fbd3e248a575d3c28a6f686e07dd14c7ba6bab2)
                    check_type(argname="argument launch_template_id", value=launch_template_id, expected_type=type_hints["launch_template_id"])
                    check_type(argname="argument version", value=version, expected_type=type_hints["version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if launch_template_id is not None:
                    self._values["launch_template_id"] = launch_template_id
                if version is not None:
                    self._values["version"] = version

            @builtins.property
            def launch_template_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) LaunchTemplateId property.

                Specify an array of string values to match this event if the actual value of LaunchTemplateId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("launch_template_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Version property.

                Specify an array of string values to match this event if the actual value of Version is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

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
                return "LaunchTemplateSpecification(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.Monitoring",
            jsii_struct_bases=[],
            name_mapping={"enabled": "enabled"},
        )
        class Monitoring:
            def __init__(
                self,
                *,
                enabled: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Monitoring.

                :param enabled: (experimental) enabled property. Specify an array of string values to match this event if the actual value of enabled is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    monitoring = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Monitoring(
                        enabled=["enabled"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__70c38dd40fbdbe925c31f9da42637549d2b30b4e7736b201d240b327a1395097)
                    check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if enabled is not None:
                    self._values["enabled"] = enabled

            @builtins.property
            def enabled(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) enabled property.

                Specify an array of string values to match this event if the actual value of enabled is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("enabled")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Monitoring(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.Monitoring1",
            jsii_struct_bases=[],
            name_mapping={"state": "state"},
        )
        class Monitoring1:
            def __init__(
                self,
                *,
                state: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Monitoring_1.

                :param state: (experimental) state property. Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    monitoring1 = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Monitoring1(
                        state=["state"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__867e3e98deddfda165d9013ad31ff5bf2297930dd2746be49e24487d22ba2100)
                    check_type(argname="argument state", value=state, expected_type=type_hints["state"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if state is not None:
                    self._values["state"] = state

            @builtins.property
            def state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) state property.

                Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("state")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Monitoring1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterface",
            jsii_struct_bases=[],
            name_mapping={
                "availability_zone": "availabilityZone",
                "description": "description",
                "group_set": "groupSet",
                "interface_type": "interfaceType",
                "ipv6_addresses_set": "ipv6AddressesSet",
                "mac_address": "macAddress",
                "network_interface_id": "networkInterfaceId",
                "owner_id": "ownerId",
                "private_ip_address": "privateIpAddress",
                "private_ip_addresses_set": "privateIpAddressesSet",
                "requester_id": "requesterId",
                "requester_managed": "requesterManaged",
                "source_dest_check": "sourceDestCheck",
                "status": "status",
                "subnet_id": "subnetId",
                "tag_set": "tagSet",
                "vpc_id": "vpcId",
            },
        )
        class NetworkInterface:
            def __init__(
                self,
                *,
                availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
                description: typing.Optional[typing.Sequence[builtins.str]] = None,
                group_set: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2", typing.Dict[builtins.str, typing.Any]]] = None,
                interface_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                ipv6_addresses_set: typing.Optional[typing.Sequence[builtins.str]] = None,
                mac_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                network_interface_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                owner_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                private_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                private_ip_addresses_set: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1", typing.Dict[builtins.str, typing.Any]]] = None,
                requester_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                requester_managed: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_dest_check: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
                subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                tag_set: typing.Optional[typing.Sequence[builtins.str]] = None,
                vpc_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for NetworkInterface.

                :param availability_zone: (experimental) availabilityZone property. Specify an array of string values to match this event if the actual value of availabilityZone is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param description: (experimental) description property. Specify an array of string values to match this event if the actual value of description is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param group_set: (experimental) groupSet property. Specify an array of string values to match this event if the actual value of groupSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param interface_type: (experimental) interfaceType property. Specify an array of string values to match this event if the actual value of interfaceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ipv6_addresses_set: (experimental) ipv6AddressesSet property. Specify an array of string values to match this event if the actual value of ipv6AddressesSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mac_address: (experimental) macAddress property. Specify an array of string values to match this event if the actual value of macAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param network_interface_id: (experimental) networkInterfaceId property. Specify an array of string values to match this event if the actual value of networkInterfaceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param owner_id: (experimental) ownerId property. Specify an array of string values to match this event if the actual value of ownerId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param private_ip_address: (experimental) privateIpAddress property. Specify an array of string values to match this event if the actual value of privateIpAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param private_ip_addresses_set: (experimental) privateIpAddressesSet property. Specify an array of string values to match this event if the actual value of privateIpAddressesSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param requester_id: (experimental) requesterId property. Specify an array of string values to match this event if the actual value of requesterId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param requester_managed: (experimental) requesterManaged property. Specify an array of string values to match this event if the actual value of requesterManaged is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_dest_check: (experimental) sourceDestCheck property. Specify an array of string values to match this event if the actual value of sourceDestCheck is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param subnet_id: (experimental) subnetId property. Specify an array of string values to match this event if the actual value of subnetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tag_set: (experimental) tagSet property. Specify an array of string values to match this event if the actual value of tagSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param vpc_id: (experimental) vpcId property. Specify an array of string values to match this event if the actual value of vpcId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    network_interface = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterface(
                        availability_zone=["availabilityZone"],
                        description=["description"],
                        group_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2(
                            items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item(
                                group_id=["groupId"],
                                group_name=["groupName"]
                            )]
                        ),
                        interface_type=["interfaceType"],
                        ipv6_addresses_set=["ipv6AddressesSet"],
                        mac_address=["macAddress"],
                        network_interface_id=["networkInterfaceId"],
                        owner_id=["ownerId"],
                        private_ip_address=["privateIpAddress"],
                        private_ip_addresses_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1(
                            item=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item(
                                primary=["primary"],
                                private_ip_address=["privateIpAddress"]
                            )]
                        ),
                        requester_id=["requesterId"],
                        requester_managed=["requesterManaged"],
                        source_dest_check=["sourceDestCheck"],
                        status=["status"],
                        subnet_id=["subnetId"],
                        tag_set=["tagSet"],
                        vpc_id=["vpcId"]
                    )
                '''
                if isinstance(group_set, dict):
                    group_set = InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2(**group_set)
                if isinstance(private_ip_addresses_set, dict):
                    private_ip_addresses_set = InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1(**private_ip_addresses_set)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__73f5bff2427627cecc1fffb6c74e02b56cacbde9023679bd6bc8373ed29b8e9c)
                    check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                    check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                    check_type(argname="argument group_set", value=group_set, expected_type=type_hints["group_set"])
                    check_type(argname="argument interface_type", value=interface_type, expected_type=type_hints["interface_type"])
                    check_type(argname="argument ipv6_addresses_set", value=ipv6_addresses_set, expected_type=type_hints["ipv6_addresses_set"])
                    check_type(argname="argument mac_address", value=mac_address, expected_type=type_hints["mac_address"])
                    check_type(argname="argument network_interface_id", value=network_interface_id, expected_type=type_hints["network_interface_id"])
                    check_type(argname="argument owner_id", value=owner_id, expected_type=type_hints["owner_id"])
                    check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
                    check_type(argname="argument private_ip_addresses_set", value=private_ip_addresses_set, expected_type=type_hints["private_ip_addresses_set"])
                    check_type(argname="argument requester_id", value=requester_id, expected_type=type_hints["requester_id"])
                    check_type(argname="argument requester_managed", value=requester_managed, expected_type=type_hints["requester_managed"])
                    check_type(argname="argument source_dest_check", value=source_dest_check, expected_type=type_hints["source_dest_check"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                    check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
                    check_type(argname="argument tag_set", value=tag_set, expected_type=type_hints["tag_set"])
                    check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if availability_zone is not None:
                    self._values["availability_zone"] = availability_zone
                if description is not None:
                    self._values["description"] = description
                if group_set is not None:
                    self._values["group_set"] = group_set
                if interface_type is not None:
                    self._values["interface_type"] = interface_type
                if ipv6_addresses_set is not None:
                    self._values["ipv6_addresses_set"] = ipv6_addresses_set
                if mac_address is not None:
                    self._values["mac_address"] = mac_address
                if network_interface_id is not None:
                    self._values["network_interface_id"] = network_interface_id
                if owner_id is not None:
                    self._values["owner_id"] = owner_id
                if private_ip_address is not None:
                    self._values["private_ip_address"] = private_ip_address
                if private_ip_addresses_set is not None:
                    self._values["private_ip_addresses_set"] = private_ip_addresses_set
                if requester_id is not None:
                    self._values["requester_id"] = requester_id
                if requester_managed is not None:
                    self._values["requester_managed"] = requester_managed
                if source_dest_check is not None:
                    self._values["source_dest_check"] = source_dest_check
                if status is not None:
                    self._values["status"] = status
                if subnet_id is not None:
                    self._values["subnet_id"] = subnet_id
                if tag_set is not None:
                    self._values["tag_set"] = tag_set
                if vpc_id is not None:
                    self._values["vpc_id"] = vpc_id

            @builtins.property
            def availability_zone(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) availabilityZone property.

                Specify an array of string values to match this event if the actual value of availabilityZone is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("availability_zone")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def description(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) description property.

                Specify an array of string values to match this event if the actual value of description is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("description")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def group_set(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2"]:
                '''(experimental) groupSet property.

                Specify an array of string values to match this event if the actual value of groupSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("group_set")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2"], result)

            @builtins.property
            def interface_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) interfaceType property.

                Specify an array of string values to match this event if the actual value of interfaceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("interface_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def ipv6_addresses_set(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ipv6AddressesSet property.

                Specify an array of string values to match this event if the actual value of ipv6AddressesSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ipv6_addresses_set")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mac_address(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) macAddress property.

                Specify an array of string values to match this event if the actual value of macAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mac_address")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def network_interface_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) networkInterfaceId property.

                Specify an array of string values to match this event if the actual value of networkInterfaceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("network_interface_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def owner_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ownerId property.

                Specify an array of string values to match this event if the actual value of ownerId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("owner_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def private_ip_address(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) privateIpAddress property.

                Specify an array of string values to match this event if the actual value of privateIpAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("private_ip_address")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def private_ip_addresses_set(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1"]:
                '''(experimental) privateIpAddressesSet property.

                Specify an array of string values to match this event if the actual value of privateIpAddressesSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("private_ip_addresses_set")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1"], result)

            @builtins.property
            def requester_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requesterId property.

                Specify an array of string values to match this event if the actual value of requesterId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("requester_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def requester_managed(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requesterManaged property.

                Specify an array of string values to match this event if the actual value of requesterManaged is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("requester_managed")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def source_dest_check(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sourceDestCheck property.

                Specify an array of string values to match this event if the actual value of sourceDestCheck is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_dest_check")
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
            def subnet_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) subnetId property.

                Specify an array of string values to match this event if the actual value of subnetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("subnet_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def tag_set(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) tagSet property.

                Specify an array of string values to match this event if the actual value of tagSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tag_set")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def vpc_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) vpcId property.

                Specify an array of string values to match this event if the actual value of vpcId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("vpc_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "NetworkInterface(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterface1",
            jsii_struct_bases=[],
            name_mapping={
                "device_index": "deviceIndex",
                "security_group_id": "securityGroupId",
                "subnet_id": "subnetId",
                "tag": "tag",
            },
        )
        class NetworkInterface1:
            def __init__(
                self,
                *,
                device_index: typing.Optional[typing.Sequence[builtins.str]] = None,
                security_group_id: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.SecurityGroupId", typing.Dict[builtins.str, typing.Any]]] = None,
                subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                tag: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for NetworkInterface_1.

                :param device_index: (experimental) DeviceIndex property. Specify an array of string values to match this event if the actual value of DeviceIndex is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param security_group_id: (experimental) SecurityGroupId property. Specify an array of string values to match this event if the actual value of SecurityGroupId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param subnet_id: (experimental) SubnetId property. Specify an array of string values to match this event if the actual value of SubnetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tag: (experimental) tag property. Specify an array of string values to match this event if the actual value of tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    network_interface1 = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterface1(
                        device_index=["deviceIndex"],
                        security_group_id=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SecurityGroupId(
                            content=["content"],
                            tag=["tag"]
                        ),
                        subnet_id=["subnetId"],
                        tag=["tag"]
                    )
                '''
                if isinstance(security_group_id, dict):
                    security_group_id = InstanceEvents.AWSAPICallViaCloudTrail.SecurityGroupId(**security_group_id)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__a5bc3519a30abfc7d2b326761c249257189f84410a1ac0334def48fa96cb2e86)
                    check_type(argname="argument device_index", value=device_index, expected_type=type_hints["device_index"])
                    check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
                    check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
                    check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if device_index is not None:
                    self._values["device_index"] = device_index
                if security_group_id is not None:
                    self._values["security_group_id"] = security_group_id
                if subnet_id is not None:
                    self._values["subnet_id"] = subnet_id
                if tag is not None:
                    self._values["tag"] = tag

            @builtins.property
            def device_index(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) DeviceIndex property.

                Specify an array of string values to match this event if the actual value of DeviceIndex is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("device_index")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def security_group_id(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.SecurityGroupId"]:
                '''(experimental) SecurityGroupId property.

                Specify an array of string values to match this event if the actual value of SecurityGroupId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("security_group_id")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.SecurityGroupId"], result)

            @builtins.property
            def subnet_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) SubnetId property.

                Specify an array of string values to match this event if the actual value of SubnetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("subnet_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def tag(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) tag property.

                Specify an array of string values to match this event if the actual value of tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tag")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "NetworkInterface1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet",
            jsii_struct_bases=[],
            name_mapping={"items": "items"},
        )
        class NetworkInterfaceSet:
            def __init__(
                self,
                *,
                items: typing.Optional[typing.Sequence[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSetItem", typing.Dict[builtins.str, typing.Any]]]] = None,
            ) -> None:
                '''(experimental) Type definition for NetworkInterfaceSet.

                :param items: (experimental) items property. Specify an array of string values to match this event if the actual value of items is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    network_interface_set = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet(
                        items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSetItem(
                            device_index=["deviceIndex"],
                            subnet_id=["subnetId"]
                        )]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__7f6b68f13a4eaad72a1fa8fcd5527e67c8658651a171ef1cd2d646c0a6ff693e)
                    check_type(argname="argument items", value=items, expected_type=type_hints["items"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if items is not None:
                    self._values["items"] = items

            @builtins.property
            def items(
                self,
            ) -> typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSetItem"]]:
                '''(experimental) items property.

                Specify an array of string values to match this event if the actual value of items is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("items")
                return typing.cast(typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSetItem"]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "NetworkInterfaceSet(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1",
            jsii_struct_bases=[],
            name_mapping={"items": "items"},
        )
        class NetworkInterfaceSet1:
            def __init__(
                self,
                *,
                items: typing.Optional[typing.Sequence[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1Item", typing.Dict[builtins.str, typing.Any]]]] = None,
            ) -> None:
                '''(experimental) Type definition for NetworkInterfaceSet_1.

                :param items: (experimental) items property. Specify an array of string values to match this event if the actual value of items is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    network_interface_set1 = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1(
                        items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1Item(
                            attachment=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Attachment(
                                attachment_id=["attachmentId"],
                                attach_time=["attachTime"],
                                delete_on_termination=["deleteOnTermination"],
                                device_index=["deviceIndex"],
                                status=["status"]
                            ),
                            group_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet3(
                                items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item(
                                    group_id=["groupId"],
                                    group_name=["groupName"]
                                )]
                            ),
                            interface_type=["interfaceType"],
                            ipv6_addresses_set=["ipv6AddressesSet"],
                            mac_address=["macAddress"],
                            network_interface_id=["networkInterfaceId"],
                            owner_id=["ownerId"],
                            private_ip_address=["privateIpAddress"],
                            private_ip_addresses_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet2(
                                item=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item(
                                    primary=["primary"],
                                    private_ip_address=["privateIpAddress"]
                                )]
                            ),
                            source_dest_check=["sourceDestCheck"],
                            status=["status"],
                            subnet_id=["subnetId"],
                            tag_set=["tagSet"],
                            vpc_id=["vpcId"]
                        )]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3b5673f2e1e9b64da1a945761fff4ce66a83c1c6fd40e1e65705e38993351723)
                    check_type(argname="argument items", value=items, expected_type=type_hints["items"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if items is not None:
                    self._values["items"] = items

            @builtins.property
            def items(
                self,
            ) -> typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1Item"]]:
                '''(experimental) items property.

                Specify an array of string values to match this event if the actual value of items is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("items")
                return typing.cast(typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1Item"]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "NetworkInterfaceSet1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1Item",
            jsii_struct_bases=[],
            name_mapping={
                "attachment": "attachment",
                "group_set": "groupSet",
                "interface_type": "interfaceType",
                "ipv6_addresses_set": "ipv6AddressesSet",
                "mac_address": "macAddress",
                "network_interface_id": "networkInterfaceId",
                "owner_id": "ownerId",
                "private_ip_address": "privateIpAddress",
                "private_ip_addresses_set": "privateIpAddressesSet",
                "source_dest_check": "sourceDestCheck",
                "status": "status",
                "subnet_id": "subnetId",
                "tag_set": "tagSet",
                "vpc_id": "vpcId",
            },
        )
        class NetworkInterfaceSet1Item:
            def __init__(
                self,
                *,
                attachment: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.Attachment", typing.Dict[builtins.str, typing.Any]]] = None,
                group_set: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet3", typing.Dict[builtins.str, typing.Any]]] = None,
                interface_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                ipv6_addresses_set: typing.Optional[typing.Sequence[builtins.str]] = None,
                mac_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                network_interface_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                owner_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                private_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                private_ip_addresses_set: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet2", typing.Dict[builtins.str, typing.Any]]] = None,
                source_dest_check: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
                subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                tag_set: typing.Optional[typing.Sequence[builtins.str]] = None,
                vpc_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for NetworkInterfaceSet_1Item.

                :param attachment: (experimental) attachment property. Specify an array of string values to match this event if the actual value of attachment is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param group_set: (experimental) groupSet property. Specify an array of string values to match this event if the actual value of groupSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param interface_type: (experimental) interfaceType property. Specify an array of string values to match this event if the actual value of interfaceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ipv6_addresses_set: (experimental) ipv6AddressesSet property. Specify an array of string values to match this event if the actual value of ipv6AddressesSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mac_address: (experimental) macAddress property. Specify an array of string values to match this event if the actual value of macAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param network_interface_id: (experimental) networkInterfaceId property. Specify an array of string values to match this event if the actual value of networkInterfaceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param owner_id: (experimental) ownerId property. Specify an array of string values to match this event if the actual value of ownerId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param private_ip_address: (experimental) privateIpAddress property. Specify an array of string values to match this event if the actual value of privateIpAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param private_ip_addresses_set: (experimental) privateIpAddressesSet property. Specify an array of string values to match this event if the actual value of privateIpAddressesSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_dest_check: (experimental) sourceDestCheck property. Specify an array of string values to match this event if the actual value of sourceDestCheck is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param subnet_id: (experimental) subnetId property. Specify an array of string values to match this event if the actual value of subnetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tag_set: (experimental) tagSet property. Specify an array of string values to match this event if the actual value of tagSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param vpc_id: (experimental) vpcId property. Specify an array of string values to match this event if the actual value of vpcId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    network_interface_set1_item = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1Item(
                        attachment=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Attachment(
                            attachment_id=["attachmentId"],
                            attach_time=["attachTime"],
                            delete_on_termination=["deleteOnTermination"],
                            device_index=["deviceIndex"],
                            status=["status"]
                        ),
                        group_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet3(
                            items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item(
                                group_id=["groupId"],
                                group_name=["groupName"]
                            )]
                        ),
                        interface_type=["interfaceType"],
                        ipv6_addresses_set=["ipv6AddressesSet"],
                        mac_address=["macAddress"],
                        network_interface_id=["networkInterfaceId"],
                        owner_id=["ownerId"],
                        private_ip_address=["privateIpAddress"],
                        private_ip_addresses_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet2(
                            item=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item(
                                primary=["primary"],
                                private_ip_address=["privateIpAddress"]
                            )]
                        ),
                        source_dest_check=["sourceDestCheck"],
                        status=["status"],
                        subnet_id=["subnetId"],
                        tag_set=["tagSet"],
                        vpc_id=["vpcId"]
                    )
                '''
                if isinstance(attachment, dict):
                    attachment = InstanceEvents.AWSAPICallViaCloudTrail.Attachment(**attachment)
                if isinstance(group_set, dict):
                    group_set = InstanceEvents.AWSAPICallViaCloudTrail.GroupSet3(**group_set)
                if isinstance(private_ip_addresses_set, dict):
                    private_ip_addresses_set = InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet2(**private_ip_addresses_set)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__90986c59311afaab923444c2c7e871ac04f83be816045ffdf210b543f58d8ecb)
                    check_type(argname="argument attachment", value=attachment, expected_type=type_hints["attachment"])
                    check_type(argname="argument group_set", value=group_set, expected_type=type_hints["group_set"])
                    check_type(argname="argument interface_type", value=interface_type, expected_type=type_hints["interface_type"])
                    check_type(argname="argument ipv6_addresses_set", value=ipv6_addresses_set, expected_type=type_hints["ipv6_addresses_set"])
                    check_type(argname="argument mac_address", value=mac_address, expected_type=type_hints["mac_address"])
                    check_type(argname="argument network_interface_id", value=network_interface_id, expected_type=type_hints["network_interface_id"])
                    check_type(argname="argument owner_id", value=owner_id, expected_type=type_hints["owner_id"])
                    check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
                    check_type(argname="argument private_ip_addresses_set", value=private_ip_addresses_set, expected_type=type_hints["private_ip_addresses_set"])
                    check_type(argname="argument source_dest_check", value=source_dest_check, expected_type=type_hints["source_dest_check"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                    check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
                    check_type(argname="argument tag_set", value=tag_set, expected_type=type_hints["tag_set"])
                    check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if attachment is not None:
                    self._values["attachment"] = attachment
                if group_set is not None:
                    self._values["group_set"] = group_set
                if interface_type is not None:
                    self._values["interface_type"] = interface_type
                if ipv6_addresses_set is not None:
                    self._values["ipv6_addresses_set"] = ipv6_addresses_set
                if mac_address is not None:
                    self._values["mac_address"] = mac_address
                if network_interface_id is not None:
                    self._values["network_interface_id"] = network_interface_id
                if owner_id is not None:
                    self._values["owner_id"] = owner_id
                if private_ip_address is not None:
                    self._values["private_ip_address"] = private_ip_address
                if private_ip_addresses_set is not None:
                    self._values["private_ip_addresses_set"] = private_ip_addresses_set
                if source_dest_check is not None:
                    self._values["source_dest_check"] = source_dest_check
                if status is not None:
                    self._values["status"] = status
                if subnet_id is not None:
                    self._values["subnet_id"] = subnet_id
                if tag_set is not None:
                    self._values["tag_set"] = tag_set
                if vpc_id is not None:
                    self._values["vpc_id"] = vpc_id

            @builtins.property
            def attachment(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.Attachment"]:
                '''(experimental) attachment property.

                Specify an array of string values to match this event if the actual value of attachment is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("attachment")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.Attachment"], result)

            @builtins.property
            def group_set(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet3"]:
                '''(experimental) groupSet property.

                Specify an array of string values to match this event if the actual value of groupSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("group_set")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet3"], result)

            @builtins.property
            def interface_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) interfaceType property.

                Specify an array of string values to match this event if the actual value of interfaceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("interface_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def ipv6_addresses_set(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ipv6AddressesSet property.

                Specify an array of string values to match this event if the actual value of ipv6AddressesSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ipv6_addresses_set")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mac_address(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) macAddress property.

                Specify an array of string values to match this event if the actual value of macAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mac_address")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def network_interface_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) networkInterfaceId property.

                Specify an array of string values to match this event if the actual value of networkInterfaceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("network_interface_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def owner_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ownerId property.

                Specify an array of string values to match this event if the actual value of ownerId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("owner_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def private_ip_address(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) privateIpAddress property.

                Specify an array of string values to match this event if the actual value of privateIpAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("private_ip_address")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def private_ip_addresses_set(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet2"]:
                '''(experimental) privateIpAddressesSet property.

                Specify an array of string values to match this event if the actual value of privateIpAddressesSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("private_ip_addresses_set")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet2"], result)

            @builtins.property
            def source_dest_check(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sourceDestCheck property.

                Specify an array of string values to match this event if the actual value of sourceDestCheck is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_dest_check")
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
            def subnet_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) subnetId property.

                Specify an array of string values to match this event if the actual value of subnetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("subnet_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def tag_set(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) tagSet property.

                Specify an array of string values to match this event if the actual value of tagSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tag_set")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def vpc_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) vpcId property.

                Specify an array of string values to match this event if the actual value of vpcId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("vpc_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "NetworkInterfaceSet1Item(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSetItem",
            jsii_struct_bases=[],
            name_mapping={"device_index": "deviceIndex", "subnet_id": "subnetId"},
        )
        class NetworkInterfaceSetItem:
            def __init__(
                self,
                *,
                device_index: typing.Optional[typing.Sequence[builtins.str]] = None,
                subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for NetworkInterfaceSetItem.

                :param device_index: (experimental) deviceIndex property. Specify an array of string values to match this event if the actual value of deviceIndex is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param subnet_id: (experimental) subnetId property. Specify an array of string values to match this event if the actual value of subnetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    network_interface_set_item = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSetItem(
                        device_index=["deviceIndex"],
                        subnet_id=["subnetId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__be943c83da95e53c00f3837025f0129f93e9a196e8ec104a58ad1cfad0de0ed9)
                    check_type(argname="argument device_index", value=device_index, expected_type=type_hints["device_index"])
                    check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if device_index is not None:
                    self._values["device_index"] = device_index
                if subnet_id is not None:
                    self._values["subnet_id"] = subnet_id

            @builtins.property
            def device_index(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) deviceIndex property.

                Specify an array of string values to match this event if the actual value of deviceIndex is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("device_index")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def subnet_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) subnetId property.

                Specify an array of string values to match this event if the actual value of subnetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

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
                return "NetworkInterfaceSetItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.OnDemandOptions",
            jsii_struct_bases=[],
            name_mapping={
                "allocation_strategy": "allocationStrategy",
                "instance_pool_constraint_filter_disabled": "instancePoolConstraintFilterDisabled",
                "max_instance_count": "maxInstanceCount",
                "max_target_capacity": "maxTargetCapacity",
            },
        )
        class OnDemandOptions:
            def __init__(
                self,
                *,
                allocation_strategy: typing.Optional[typing.Sequence[builtins.str]] = None,
                instance_pool_constraint_filter_disabled: typing.Optional[typing.Sequence[builtins.str]] = None,
                max_instance_count: typing.Optional[typing.Sequence[builtins.str]] = None,
                max_target_capacity: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for OnDemandOptions.

                :param allocation_strategy: (experimental) AllocationStrategy property. Specify an array of string values to match this event if the actual value of AllocationStrategy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_pool_constraint_filter_disabled: (experimental) InstancePoolConstraintFilterDisabled property. Specify an array of string values to match this event if the actual value of InstancePoolConstraintFilterDisabled is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param max_instance_count: (experimental) MaxInstanceCount property. Specify an array of string values to match this event if the actual value of MaxInstanceCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param max_target_capacity: (experimental) MaxTargetCapacity property. Specify an array of string values to match this event if the actual value of MaxTargetCapacity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    on_demand_options = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.OnDemandOptions(
                        allocation_strategy=["allocationStrategy"],
                        instance_pool_constraint_filter_disabled=["instancePoolConstraintFilterDisabled"],
                        max_instance_count=["maxInstanceCount"],
                        max_target_capacity=["maxTargetCapacity"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3f6bfc4e3eedab1b03bedeacbb77ef623860f20a4e3bd9360117411b4ccbc688)
                    check_type(argname="argument allocation_strategy", value=allocation_strategy, expected_type=type_hints["allocation_strategy"])
                    check_type(argname="argument instance_pool_constraint_filter_disabled", value=instance_pool_constraint_filter_disabled, expected_type=type_hints["instance_pool_constraint_filter_disabled"])
                    check_type(argname="argument max_instance_count", value=max_instance_count, expected_type=type_hints["max_instance_count"])
                    check_type(argname="argument max_target_capacity", value=max_target_capacity, expected_type=type_hints["max_target_capacity"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if allocation_strategy is not None:
                    self._values["allocation_strategy"] = allocation_strategy
                if instance_pool_constraint_filter_disabled is not None:
                    self._values["instance_pool_constraint_filter_disabled"] = instance_pool_constraint_filter_disabled
                if max_instance_count is not None:
                    self._values["max_instance_count"] = max_instance_count
                if max_target_capacity is not None:
                    self._values["max_target_capacity"] = max_target_capacity

            @builtins.property
            def allocation_strategy(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) AllocationStrategy property.

                Specify an array of string values to match this event if the actual value of AllocationStrategy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("allocation_strategy")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def instance_pool_constraint_filter_disabled(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) InstancePoolConstraintFilterDisabled property.

                Specify an array of string values to match this event if the actual value of InstancePoolConstraintFilterDisabled is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_pool_constraint_filter_disabled")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def max_instance_count(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) MaxInstanceCount property.

                Specify an array of string values to match this event if the actual value of MaxInstanceCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("max_instance_count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def max_target_capacity(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) MaxTargetCapacity property.

                Specify an array of string values to match this event if the actual value of MaxTargetCapacity is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("max_target_capacity")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "OnDemandOptions(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.Placement",
            jsii_struct_bases=[],
            name_mapping={
                "availability_zone": "availabilityZone",
                "tenancy": "tenancy",
            },
        )
        class Placement:
            def __init__(
                self,
                *,
                availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
                tenancy: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Placement.

                :param availability_zone: (experimental) availabilityZone property. Specify an array of string values to match this event if the actual value of availabilityZone is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tenancy: (experimental) tenancy property. Specify an array of string values to match this event if the actual value of tenancy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    placement = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Placement(
                        availability_zone=["availabilityZone"],
                        tenancy=["tenancy"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__c8da6835d42c7ba911091f3f64a5667781519c248a0d0fd4673c97f478be3a27)
                    check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                    check_type(argname="argument tenancy", value=tenancy, expected_type=type_hints["tenancy"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if availability_zone is not None:
                    self._values["availability_zone"] = availability_zone
                if tenancy is not None:
                    self._values["tenancy"] = tenancy

            @builtins.property
            def availability_zone(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) availabilityZone property.

                Specify an array of string values to match this event if the actual value of availabilityZone is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("availability_zone")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def tenancy(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) tenancy property.

                Specify an array of string values to match this event if the actual value of tenancy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tenancy")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Placement(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1",
            jsii_struct_bases=[],
            name_mapping={"item": "item"},
        )
        class PrivateIpAddressesSet1:
            def __init__(
                self,
                *,
                item: typing.Optional[typing.Sequence[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item", typing.Dict[builtins.str, typing.Any]]]] = None,
            ) -> None:
                '''(experimental) Type definition for PrivateIpAddressesSet_1.

                :param item: (experimental) item property. Specify an array of string values to match this event if the actual value of item is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    private_ip_addresses_set1 = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1(
                        item=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item(
                            primary=["primary"],
                            private_ip_address=["privateIpAddress"]
                        )]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__fe652185c5fa050c66679c2fff9179c1b6f36148fa300c266fd8ab1f7299e259)
                    check_type(argname="argument item", value=item, expected_type=type_hints["item"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if item is not None:
                    self._values["item"] = item

            @builtins.property
            def item(
                self,
            ) -> typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item"]]:
                '''(experimental) item property.

                Specify an array of string values to match this event if the actual value of item is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("item")
                return typing.cast(typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item"]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "PrivateIpAddressesSet1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item",
            jsii_struct_bases=[],
            name_mapping={
                "primary": "primary",
                "private_ip_address": "privateIpAddress",
            },
        )
        class PrivateIpAddressesSet1Item:
            def __init__(
                self,
                *,
                primary: typing.Optional[typing.Sequence[builtins.str]] = None,
                private_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for PrivateIpAddressesSet_1Item.

                :param primary: (experimental) primary property. Specify an array of string values to match this event if the actual value of primary is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param private_ip_address: (experimental) privateIpAddress property. Specify an array of string values to match this event if the actual value of privateIpAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    private_ip_addresses_set1_item = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item(
                        primary=["primary"],
                        private_ip_address=["privateIpAddress"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__2830bf227e7b699c0a215abf0edb9ab50cff49df4cc51e61b1cd48632e2f4d32)
                    check_type(argname="argument primary", value=primary, expected_type=type_hints["primary"])
                    check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if primary is not None:
                    self._values["primary"] = primary
                if private_ip_address is not None:
                    self._values["private_ip_address"] = private_ip_address

            @builtins.property
            def primary(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) primary property.

                Specify an array of string values to match this event if the actual value of primary is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("primary")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def private_ip_address(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) privateIpAddress property.

                Specify an array of string values to match this event if the actual value of privateIpAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("private_ip_address")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "PrivateIpAddressesSet1Item(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet2",
            jsii_struct_bases=[],
            name_mapping={"item": "item"},
        )
        class PrivateIpAddressesSet2:
            def __init__(
                self,
                *,
                item: typing.Optional[typing.Sequence[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item", typing.Dict[builtins.str, typing.Any]]]] = None,
            ) -> None:
                '''(experimental) Type definition for PrivateIpAddressesSet_2.

                :param item: (experimental) item property. Specify an array of string values to match this event if the actual value of item is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    private_ip_addresses_set2 = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet2(
                        item=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item(
                            primary=["primary"],
                            private_ip_address=["privateIpAddress"]
                        )]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__1ba43b91eb28e2714bedc3b3388c7eb5fa069cc499568b5bcd713a867fb4003b)
                    check_type(argname="argument item", value=item, expected_type=type_hints["item"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if item is not None:
                    self._values["item"] = item

            @builtins.property
            def item(
                self,
            ) -> typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item"]]:
                '''(experimental) item property.

                Specify an array of string values to match this event if the actual value of item is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("item")
                return typing.cast(typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item"]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "PrivateIpAddressesSet2(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.RequestParameters",
            jsii_struct_bases=[],
            name_mapping={
                "availability_zone": "availabilityZone",
                "block_device_mapping": "blockDeviceMapping",
                "client_token": "clientToken",
                "create_fleet_request": "createFleetRequest",
                "create_launch_template_request": "createLaunchTemplateRequest",
                "delete_launch_template_request": "deleteLaunchTemplateRequest",
                "description": "description",
                "disable_api_termination": "disableApiTermination",
                "group_description": "groupDescription",
                "group_id": "groupId",
                "group_name": "groupName",
                "group_set": "groupSet",
                "instance_market_options": "instanceMarketOptions",
                "instances_set": "instancesSet",
                "instance_type": "instanceType",
                "ipv6_address_count": "ipv6AddressCount",
                "launch_template": "launchTemplate",
                "monitoring": "monitoring",
                "network_interface_id": "networkInterfaceId",
                "network_interface_set": "networkInterfaceSet",
                "private_ip_addresses_set": "privateIpAddressesSet",
                "subnet_id": "subnetId",
                "tag_specification_set": "tagSpecificationSet",
                "user_data": "userData",
                "vpc_id": "vpcId",
            },
        )
        class RequestParameters:
            def __init__(
                self,
                *,
                availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
                block_device_mapping: typing.Optional[typing.Sequence[builtins.str]] = None,
                client_token: typing.Optional[typing.Sequence[builtins.str]] = None,
                create_fleet_request: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.CreateFleetRequest", typing.Dict[builtins.str, typing.Any]]] = None,
                create_launch_template_request: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.CreateLaunchTemplateRequest", typing.Dict[builtins.str, typing.Any]]] = None,
                delete_launch_template_request: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateRequest", typing.Dict[builtins.str, typing.Any]]] = None,
                description: typing.Optional[typing.Sequence[builtins.str]] = None,
                disable_api_termination: typing.Optional[typing.Sequence[builtins.str]] = None,
                group_description: typing.Optional[typing.Sequence[builtins.str]] = None,
                group_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                group_set: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet1", typing.Dict[builtins.str, typing.Any]]] = None,
                instance_market_options: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.InstanceMarketOptions", typing.Dict[builtins.str, typing.Any]]] = None,
                instances_set: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet1", typing.Dict[builtins.str, typing.Any]]] = None,
                instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                ipv6_address_count: typing.Optional[typing.Sequence[builtins.str]] = None,
                launch_template: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
                monitoring: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.Monitoring", typing.Dict[builtins.str, typing.Any]]] = None,
                network_interface_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                network_interface_set: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet", typing.Dict[builtins.str, typing.Any]]] = None,
                private_ip_addresses_set: typing.Optional[typing.Sequence[builtins.str]] = None,
                subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                tag_specification_set: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSet", typing.Dict[builtins.str, typing.Any]]] = None,
                user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
                vpc_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for RequestParameters.

                :param availability_zone: (experimental) availabilityZone property. Specify an array of string values to match this event if the actual value of availabilityZone is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param block_device_mapping: (experimental) blockDeviceMapping property. Specify an array of string values to match this event if the actual value of blockDeviceMapping is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param client_token: (experimental) clientToken property. Specify an array of string values to match this event if the actual value of clientToken is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param create_fleet_request: (experimental) CreateFleetRequest property. Specify an array of string values to match this event if the actual value of CreateFleetRequest is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param create_launch_template_request: (experimental) CreateLaunchTemplateRequest property. Specify an array of string values to match this event if the actual value of CreateLaunchTemplateRequest is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param delete_launch_template_request: (experimental) DeleteLaunchTemplateRequest property. Specify an array of string values to match this event if the actual value of DeleteLaunchTemplateRequest is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param description: (experimental) description property. Specify an array of string values to match this event if the actual value of description is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param disable_api_termination: (experimental) disableApiTermination property. Specify an array of string values to match this event if the actual value of disableApiTermination is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param group_description: (experimental) groupDescription property. Specify an array of string values to match this event if the actual value of groupDescription is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param group_id: (experimental) groupId property. Specify an array of string values to match this event if the actual value of groupId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param group_name: (experimental) groupName property. Specify an array of string values to match this event if the actual value of groupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param group_set: (experimental) groupSet property. Specify an array of string values to match this event if the actual value of groupSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_market_options: (experimental) instanceMarketOptions property. Specify an array of string values to match this event if the actual value of instanceMarketOptions is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instances_set: (experimental) instancesSet property. Specify an array of string values to match this event if the actual value of instancesSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_type: (experimental) instanceType property. Specify an array of string values to match this event if the actual value of instanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ipv6_address_count: (experimental) ipv6AddressCount property. Specify an array of string values to match this event if the actual value of ipv6AddressCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param launch_template: (experimental) launchTemplate property. Specify an array of string values to match this event if the actual value of launchTemplate is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param monitoring: (experimental) monitoring property. Specify an array of string values to match this event if the actual value of monitoring is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param network_interface_id: (experimental) networkInterfaceId property. Specify an array of string values to match this event if the actual value of networkInterfaceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param network_interface_set: (experimental) networkInterfaceSet property. Specify an array of string values to match this event if the actual value of networkInterfaceSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param private_ip_addresses_set: (experimental) privateIpAddressesSet property. Specify an array of string values to match this event if the actual value of privateIpAddressesSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param subnet_id: (experimental) subnetId property. Specify an array of string values to match this event if the actual value of subnetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tag_specification_set: (experimental) tagSpecificationSet property. Specify an array of string values to match this event if the actual value of tagSpecificationSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_data: (experimental) userData property. Specify an array of string values to match this event if the actual value of userData is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param vpc_id: (experimental) vpcId property. Specify an array of string values to match this event if the actual value of vpcId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    # overrides: Any
                    
                    request_parameters = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.RequestParameters(
                        availability_zone=["availabilityZone"],
                        block_device_mapping=["blockDeviceMapping"],
                        client_token=["clientToken"],
                        create_fleet_request=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.CreateFleetRequest(
                            client_token=["clientToken"],
                            existing_instances=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.ExistingInstances(
                                availability_zone=["availabilityZone"],
                                count=["count"],
                                instance_type=["instanceType"],
                                market_option=["marketOption"],
                                operating_system=["operatingSystem"],
                                tag=["tag"]
                            ),
                            launch_template_configs=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateConfigs(
                                launch_template_specification=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateSpecification(
                                    launch_template_id=["launchTemplateId"],
                                    version=["version"]
                                ),
                                overrides=[overrides],
                                tag=["tag"]
                            ),
                            on_demand_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.OnDemandOptions(
                                allocation_strategy=["allocationStrategy"],
                                instance_pool_constraint_filter_disabled=["instancePoolConstraintFilterDisabled"],
                                max_instance_count=["maxInstanceCount"],
                                max_target_capacity=["maxTargetCapacity"]
                            ),
                            spot_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions(
                                allocation_strategy=["allocationStrategy"],
                                instance_pool_constraint_filter_disabled=["instancePoolConstraintFilterDisabled"],
                                instance_pools_to_use_count=["instancePoolsToUseCount"],
                                max_instance_count=["maxInstanceCount"],
                                max_target_capacity=["maxTargetCapacity"]
                            ),
                            tag_specification=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecification(
                                resource_type=["resourceType"],
                                tag=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Tag(
                                    key=["key"],
                                    tag=["tag"],
                                    value=["value"]
                                )
                            ),
                            target_capacity_specification=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TargetCapacitySpecification(
                                default_target_capacity_type=["defaultTargetCapacityType"],
                                on_demand_target_capacity=["onDemandTargetCapacity"],
                                spot_target_capacity=["spotTargetCapacity"],
                                total_target_capacity=["totalTargetCapacity"]
                            ),
                            type=["type"]
                        ),
                        create_launch_template_request=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.CreateLaunchTemplateRequest(
                            launch_template_data=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateData(
                                image_id=["imageId"],
                                instance_market_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceMarketOptions1(
                                    market_type=["marketType"],
                                    spot_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions2(
                                        max_price=["maxPrice"],
                                        spot_instance_type=["spotInstanceType"]
                                    )
                                ),
                                instance_type=["instanceType"],
                                network_interface=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterface1(
                                    device_index=["deviceIndex"],
                                    security_group_id=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SecurityGroupId(
                                        content=["content"],
                                        tag=["tag"]
                                    ),
                                    subnet_id=["subnetId"],
                                    tag=["tag"]
                                ),
                                user_data=["userData"]
                            ),
                            launch_template_name=["launchTemplateName"]
                        ),
                        delete_launch_template_request=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateRequest(
                            launch_template_name=["launchTemplateName"]
                        ),
                        description=["description"],
                        disable_api_termination=["disableApiTermination"],
                        group_description=["groupDescription"],
                        group_id=["groupId"],
                        group_name=["groupName"],
                        group_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet1(
                            items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet1Item(
                                group_id=["groupId"]
                            )]
                        ),
                        instance_market_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceMarketOptions(
                            market_type=["marketType"],
                            spot_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions1(
                                max_price=["maxPrice"],
                                spot_instance_type=["spotInstanceType"]
                            )
                        ),
                        instances_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet1(
                            items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet1Item(
                                image_id=["imageId"],
                                instance_id=["instanceId"],
                                max_count=["maxCount"],
                                min_count=["minCount"]
                            )]
                        ),
                        instance_type=["instanceType"],
                        ipv6_address_count=["ipv6AddressCount"],
                        launch_template=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate(
                            launch_template_id=["launchTemplateId"],
                            version=["version"]
                        ),
                        monitoring=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Monitoring(
                            enabled=["enabled"]
                        ),
                        network_interface_id=["networkInterfaceId"],
                        network_interface_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet(
                            items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSetItem(
                                device_index=["deviceIndex"],
                                subnet_id=["subnetId"]
                            )]
                        ),
                        private_ip_addresses_set=["privateIpAddressesSet"],
                        subnet_id=["subnetId"],
                        tag_specification_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSet(
                            items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItem(
                                resource_type=["resourceType"],
                                tags=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItemItem(
                                    key=["key"],
                                    value=["value"]
                                )]
                            )]
                        ),
                        user_data=["userData"],
                        vpc_id=["vpcId"]
                    )
                '''
                if isinstance(create_fleet_request, dict):
                    create_fleet_request = InstanceEvents.AWSAPICallViaCloudTrail.CreateFleetRequest(**create_fleet_request)
                if isinstance(create_launch_template_request, dict):
                    create_launch_template_request = InstanceEvents.AWSAPICallViaCloudTrail.CreateLaunchTemplateRequest(**create_launch_template_request)
                if isinstance(delete_launch_template_request, dict):
                    delete_launch_template_request = InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateRequest(**delete_launch_template_request)
                if isinstance(group_set, dict):
                    group_set = InstanceEvents.AWSAPICallViaCloudTrail.GroupSet1(**group_set)
                if isinstance(instance_market_options, dict):
                    instance_market_options = InstanceEvents.AWSAPICallViaCloudTrail.InstanceMarketOptions(**instance_market_options)
                if isinstance(instances_set, dict):
                    instances_set = InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet1(**instances_set)
                if isinstance(launch_template, dict):
                    launch_template = InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate(**launch_template)
                if isinstance(monitoring, dict):
                    monitoring = InstanceEvents.AWSAPICallViaCloudTrail.Monitoring(**monitoring)
                if isinstance(network_interface_set, dict):
                    network_interface_set = InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet(**network_interface_set)
                if isinstance(tag_specification_set, dict):
                    tag_specification_set = InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSet(**tag_specification_set)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__aa62146d02ad16f183a3a35e862a77e6f5aa36b0f5afb91c405ed576d6719484)
                    check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                    check_type(argname="argument block_device_mapping", value=block_device_mapping, expected_type=type_hints["block_device_mapping"])
                    check_type(argname="argument client_token", value=client_token, expected_type=type_hints["client_token"])
                    check_type(argname="argument create_fleet_request", value=create_fleet_request, expected_type=type_hints["create_fleet_request"])
                    check_type(argname="argument create_launch_template_request", value=create_launch_template_request, expected_type=type_hints["create_launch_template_request"])
                    check_type(argname="argument delete_launch_template_request", value=delete_launch_template_request, expected_type=type_hints["delete_launch_template_request"])
                    check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                    check_type(argname="argument disable_api_termination", value=disable_api_termination, expected_type=type_hints["disable_api_termination"])
                    check_type(argname="argument group_description", value=group_description, expected_type=type_hints["group_description"])
                    check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
                    check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
                    check_type(argname="argument group_set", value=group_set, expected_type=type_hints["group_set"])
                    check_type(argname="argument instance_market_options", value=instance_market_options, expected_type=type_hints["instance_market_options"])
                    check_type(argname="argument instances_set", value=instances_set, expected_type=type_hints["instances_set"])
                    check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                    check_type(argname="argument ipv6_address_count", value=ipv6_address_count, expected_type=type_hints["ipv6_address_count"])
                    check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
                    check_type(argname="argument monitoring", value=monitoring, expected_type=type_hints["monitoring"])
                    check_type(argname="argument network_interface_id", value=network_interface_id, expected_type=type_hints["network_interface_id"])
                    check_type(argname="argument network_interface_set", value=network_interface_set, expected_type=type_hints["network_interface_set"])
                    check_type(argname="argument private_ip_addresses_set", value=private_ip_addresses_set, expected_type=type_hints["private_ip_addresses_set"])
                    check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
                    check_type(argname="argument tag_specification_set", value=tag_specification_set, expected_type=type_hints["tag_specification_set"])
                    check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
                    check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if availability_zone is not None:
                    self._values["availability_zone"] = availability_zone
                if block_device_mapping is not None:
                    self._values["block_device_mapping"] = block_device_mapping
                if client_token is not None:
                    self._values["client_token"] = client_token
                if create_fleet_request is not None:
                    self._values["create_fleet_request"] = create_fleet_request
                if create_launch_template_request is not None:
                    self._values["create_launch_template_request"] = create_launch_template_request
                if delete_launch_template_request is not None:
                    self._values["delete_launch_template_request"] = delete_launch_template_request
                if description is not None:
                    self._values["description"] = description
                if disable_api_termination is not None:
                    self._values["disable_api_termination"] = disable_api_termination
                if group_description is not None:
                    self._values["group_description"] = group_description
                if group_id is not None:
                    self._values["group_id"] = group_id
                if group_name is not None:
                    self._values["group_name"] = group_name
                if group_set is not None:
                    self._values["group_set"] = group_set
                if instance_market_options is not None:
                    self._values["instance_market_options"] = instance_market_options
                if instances_set is not None:
                    self._values["instances_set"] = instances_set
                if instance_type is not None:
                    self._values["instance_type"] = instance_type
                if ipv6_address_count is not None:
                    self._values["ipv6_address_count"] = ipv6_address_count
                if launch_template is not None:
                    self._values["launch_template"] = launch_template
                if monitoring is not None:
                    self._values["monitoring"] = monitoring
                if network_interface_id is not None:
                    self._values["network_interface_id"] = network_interface_id
                if network_interface_set is not None:
                    self._values["network_interface_set"] = network_interface_set
                if private_ip_addresses_set is not None:
                    self._values["private_ip_addresses_set"] = private_ip_addresses_set
                if subnet_id is not None:
                    self._values["subnet_id"] = subnet_id
                if tag_specification_set is not None:
                    self._values["tag_specification_set"] = tag_specification_set
                if user_data is not None:
                    self._values["user_data"] = user_data
                if vpc_id is not None:
                    self._values["vpc_id"] = vpc_id

            @builtins.property
            def availability_zone(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) availabilityZone property.

                Specify an array of string values to match this event if the actual value of availabilityZone is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("availability_zone")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def block_device_mapping(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) blockDeviceMapping property.

                Specify an array of string values to match this event if the actual value of blockDeviceMapping is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("block_device_mapping")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def client_token(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) clientToken property.

                Specify an array of string values to match this event if the actual value of clientToken is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("client_token")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def create_fleet_request(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.CreateFleetRequest"]:
                '''(experimental) CreateFleetRequest property.

                Specify an array of string values to match this event if the actual value of CreateFleetRequest is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("create_fleet_request")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.CreateFleetRequest"], result)

            @builtins.property
            def create_launch_template_request(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.CreateLaunchTemplateRequest"]:
                '''(experimental) CreateLaunchTemplateRequest property.

                Specify an array of string values to match this event if the actual value of CreateLaunchTemplateRequest is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("create_launch_template_request")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.CreateLaunchTemplateRequest"], result)

            @builtins.property
            def delete_launch_template_request(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateRequest"]:
                '''(experimental) DeleteLaunchTemplateRequest property.

                Specify an array of string values to match this event if the actual value of DeleteLaunchTemplateRequest is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("delete_launch_template_request")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateRequest"], result)

            @builtins.property
            def description(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) description property.

                Specify an array of string values to match this event if the actual value of description is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("description")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def disable_api_termination(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) disableApiTermination property.

                Specify an array of string values to match this event if the actual value of disableApiTermination is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("disable_api_termination")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def group_description(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) groupDescription property.

                Specify an array of string values to match this event if the actual value of groupDescription is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("group_description")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def group_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) groupId property.

                Specify an array of string values to match this event if the actual value of groupId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("group_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def group_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) groupName property.

                Specify an array of string values to match this event if the actual value of groupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("group_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def group_set(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet1"]:
                '''(experimental) groupSet property.

                Specify an array of string values to match this event if the actual value of groupSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("group_set")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.GroupSet1"], result)

            @builtins.property
            def instance_market_options(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.InstanceMarketOptions"]:
                '''(experimental) instanceMarketOptions property.

                Specify an array of string values to match this event if the actual value of instanceMarketOptions is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_market_options")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.InstanceMarketOptions"], result)

            @builtins.property
            def instances_set(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet1"]:
                '''(experimental) instancesSet property.

                Specify an array of string values to match this event if the actual value of instancesSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instances_set")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet1"], result)

            @builtins.property
            def instance_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instanceType property.

                Specify an array of string values to match this event if the actual value of instanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def ipv6_address_count(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ipv6AddressCount property.

                Specify an array of string values to match this event if the actual value of ipv6AddressCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ipv6_address_count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def launch_template(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate"]:
                '''(experimental) launchTemplate property.

                Specify an array of string values to match this event if the actual value of launchTemplate is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("launch_template")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate"], result)

            @builtins.property
            def monitoring(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.Monitoring"]:
                '''(experimental) monitoring property.

                Specify an array of string values to match this event if the actual value of monitoring is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("monitoring")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.Monitoring"], result)

            @builtins.property
            def network_interface_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) networkInterfaceId property.

                Specify an array of string values to match this event if the actual value of networkInterfaceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("network_interface_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def network_interface_set(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet"]:
                '''(experimental) networkInterfaceSet property.

                Specify an array of string values to match this event if the actual value of networkInterfaceSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("network_interface_set")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet"], result)

            @builtins.property
            def private_ip_addresses_set(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) privateIpAddressesSet property.

                Specify an array of string values to match this event if the actual value of privateIpAddressesSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("private_ip_addresses_set")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def subnet_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) subnetId property.

                Specify an array of string values to match this event if the actual value of subnetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("subnet_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def tag_specification_set(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSet"]:
                '''(experimental) tagSpecificationSet property.

                Specify an array of string values to match this event if the actual value of tagSpecificationSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tag_specification_set")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSet"], result)

            @builtins.property
            def user_data(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) userData property.

                Specify an array of string values to match this event if the actual value of userData is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_data")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def vpc_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) vpcId property.

                Specify an array of string values to match this event if the actual value of vpcId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("vpc_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "RequestParameters(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.ResponseElements",
            jsii_struct_bases=[],
            name_mapping={
                "create_fleet_response": "createFleetResponse",
                "create_launch_template_response": "createLaunchTemplateResponse",
                "delete_launch_template_response": "deleteLaunchTemplateResponse",
                "group_id": "groupId",
                "group_set": "groupSet",
                "instances_set": "instancesSet",
                "network_interface": "networkInterface",
                "owner_id": "ownerId",
                "requester_id": "requesterId",
                "request_id": "requestId",
                "reservation_id": "reservationId",
                "return_": "return",
            },
        )
        class ResponseElements:
            def __init__(
                self,
                *,
                create_fleet_response: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.CreateFleetResponse", typing.Dict[builtins.str, typing.Any]]] = None,
                create_launch_template_response: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateResponse", typing.Dict[builtins.str, typing.Any]]] = None,
                delete_launch_template_response: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateResponse", typing.Dict[builtins.str, typing.Any]]] = None,
                group_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                group_set: typing.Optional[typing.Sequence[builtins.str]] = None,
                instances_set: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet", typing.Dict[builtins.str, typing.Any]]] = None,
                network_interface: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterface", typing.Dict[builtins.str, typing.Any]]] = None,
                owner_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                requester_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                reservation_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                return_: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ResponseElements.

                :param create_fleet_response: (experimental) CreateFleetResponse property. Specify an array of string values to match this event if the actual value of CreateFleetResponse is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param create_launch_template_response: (experimental) CreateLaunchTemplateResponse property. Specify an array of string values to match this event if the actual value of CreateLaunchTemplateResponse is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param delete_launch_template_response: (experimental) DeleteLaunchTemplateResponse property. Specify an array of string values to match this event if the actual value of DeleteLaunchTemplateResponse is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param group_id: (experimental) groupId property. Specify an array of string values to match this event if the actual value of groupId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param group_set: (experimental) groupSet property. Specify an array of string values to match this event if the actual value of groupSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instances_set: (experimental) instancesSet property. Specify an array of string values to match this event if the actual value of instancesSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param network_interface: (experimental) networkInterface property. Specify an array of string values to match this event if the actual value of networkInterface is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param owner_id: (experimental) ownerId property. Specify an array of string values to match this event if the actual value of ownerId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param requester_id: (experimental) requesterId property. Specify an array of string values to match this event if the actual value of requesterId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) requestId property. Specify an array of string values to match this event if the actual value of requestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param reservation_id: (experimental) reservationId property. Specify an array of string values to match this event if the actual value of reservationId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param return_: (experimental) _return property. Specify an array of string values to match this event if the actual value of _return is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    response_elements = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.ResponseElements(
                        create_fleet_response=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.CreateFleetResponse(
                            error_set=["errorSet"],
                            fleet_id=["fleetId"],
                            fleet_instance_set=["fleetInstanceSet"],
                            request_id=["requestId"],
                            xmlns=["xmlns"]
                        ),
                        create_launch_template_response=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateResponse(
                            launch_template=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate1(
                                created_by=["createdBy"],
                                create_time=["createTime"],
                                default_version_number=["defaultVersionNumber"],
                                latest_version_number=["latestVersionNumber"],
                                launch_template_id=["launchTemplateId"],
                                launch_template_name=["launchTemplateName"]
                            ),
                            request_id=["requestId"],
                            xmlns=["xmlns"]
                        ),
                        delete_launch_template_response=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateResponse(
                            launch_template=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate1(
                                created_by=["createdBy"],
                                create_time=["createTime"],
                                default_version_number=["defaultVersionNumber"],
                                latest_version_number=["latestVersionNumber"],
                                launch_template_id=["launchTemplateId"],
                                launch_template_name=["launchTemplateName"]
                            ),
                            request_id=["requestId"],
                            xmlns=["xmlns"]
                        ),
                        group_id=["groupId"],
                        group_set=["groupSet"],
                        instances_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet(
                            items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstancesSetItem(
                                ami_launch_index=["amiLaunchIndex"],
                                architecture=["architecture"],
                                block_device_mapping=["blockDeviceMapping"],
                                capacity_reservation_specification=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.CapacityReservationSpecification(
                                    capacity_reservation_preference=["capacityReservationPreference"]
                                ),
                                client_token=["clientToken"],
                                cpu_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.CpuOptions(
                                    core_count=["coreCount"],
                                    threads_per_core=["threadsPerCore"]
                                ),
                                current_state=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceState(
                                    code=["code"],
                                    name=["name"]
                                ),
                                ebs_optimized=["ebsOptimized"],
                                enclave_options=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.EnclaveOptions(
                                    enabled=["enabled"]
                                ),
                                group_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2(
                                    items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item(
                                        group_id=["groupId"],
                                        group_name=["groupName"]
                                    )]
                                ),
                                hypervisor=["hypervisor"],
                                image_id=["imageId"],
                                instance_id=["instanceId"],
                                instance_lifecycle=["instanceLifecycle"],
                                instance_state=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceState(
                                    code=["code"],
                                    name=["name"]
                                ),
                                instance_type=["instanceType"],
                                launch_time=["launchTime"],
                                monitoring=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Monitoring1(
                                    state=["state"]
                                ),
                                network_interface_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1(
                                    items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1Item(
                                        attachment=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Attachment(
                                            attachment_id=["attachmentId"],
                                            attach_time=["attachTime"],
                                            delete_on_termination=["deleteOnTermination"],
                                            device_index=["deviceIndex"],
                                            status=["status"]
                                        ),
                                        group_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet3(
                                            items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item(
                                                group_id=["groupId"],
                                                group_name=["groupName"]
                                            )]
                                        ),
                                        interface_type=["interfaceType"],
                                        ipv6_addresses_set=["ipv6AddressesSet"],
                                        mac_address=["macAddress"],
                                        network_interface_id=["networkInterfaceId"],
                                        owner_id=["ownerId"],
                                        private_ip_address=["privateIpAddress"],
                                        private_ip_addresses_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet2(
                                            item=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item(
                                                primary=["primary"],
                                                private_ip_address=["privateIpAddress"]
                                            )]
                                        ),
                                        source_dest_check=["sourceDestCheck"],
                                        status=["status"],
                                        subnet_id=["subnetId"],
                                        tag_set=["tagSet"],
                                        vpc_id=["vpcId"]
                                    )]
                                ),
                                placement=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Placement(
                                    availability_zone=["availabilityZone"],
                                    tenancy=["tenancy"]
                                ),
                                previous_state=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.InstanceState(
                                    code=["code"],
                                    name=["name"]
                                ),
                                private_ip_address=["privateIpAddress"],
                                product_codes=["productCodes"],
                                root_device_name=["rootDeviceName"],
                                root_device_type=["rootDeviceType"],
                                source_dest_check=["sourceDestCheck"],
                                spot_instance_request_id=["spotInstanceRequestId"],
                                state_reason=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.StateReason(
                                    code=["code"],
                                    message=["message"]
                                ),
                                subnet_id=["subnetId"],
                                tag_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSet(
                                    items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItemItem(
                                        key=["key"],
                                        value=["value"]
                                    )]
                                ),
                                virtualization_type=["virtualizationType"],
                                vpc_id=["vpcId"]
                            )]
                        ),
                        network_interface=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterface(
                            availability_zone=["availabilityZone"],
                            description=["description"],
                            group_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2(
                                items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item(
                                    group_id=["groupId"],
                                    group_name=["groupName"]
                                )]
                            ),
                            interface_type=["interfaceType"],
                            ipv6_addresses_set=["ipv6AddressesSet"],
                            mac_address=["macAddress"],
                            network_interface_id=["networkInterfaceId"],
                            owner_id=["ownerId"],
                            private_ip_address=["privateIpAddress"],
                            private_ip_addresses_set=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1(
                                item=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item(
                                    primary=["primary"],
                                    private_ip_address=["privateIpAddress"]
                                )]
                            ),
                            requester_id=["requesterId"],
                            requester_managed=["requesterManaged"],
                            source_dest_check=["sourceDestCheck"],
                            status=["status"],
                            subnet_id=["subnetId"],
                            tag_set=["tagSet"],
                            vpc_id=["vpcId"]
                        ),
                        owner_id=["ownerId"],
                        requester_id=["requesterId"],
                        request_id=["requestId"],
                        reservation_id=["reservationId"],
                        return=["return"]
                    )
                '''
                if isinstance(create_fleet_response, dict):
                    create_fleet_response = InstanceEvents.AWSAPICallViaCloudTrail.CreateFleetResponse(**create_fleet_response)
                if isinstance(create_launch_template_response, dict):
                    create_launch_template_response = InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateResponse(**create_launch_template_response)
                if isinstance(delete_launch_template_response, dict):
                    delete_launch_template_response = InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateResponse(**delete_launch_template_response)
                if isinstance(instances_set, dict):
                    instances_set = InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet(**instances_set)
                if isinstance(network_interface, dict):
                    network_interface = InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterface(**network_interface)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__c66ae8ce4979d3800e7bdb0e2b37ecd5e70dfffcf65ddbad398f9210ec11aee7)
                    check_type(argname="argument create_fleet_response", value=create_fleet_response, expected_type=type_hints["create_fleet_response"])
                    check_type(argname="argument create_launch_template_response", value=create_launch_template_response, expected_type=type_hints["create_launch_template_response"])
                    check_type(argname="argument delete_launch_template_response", value=delete_launch_template_response, expected_type=type_hints["delete_launch_template_response"])
                    check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
                    check_type(argname="argument group_set", value=group_set, expected_type=type_hints["group_set"])
                    check_type(argname="argument instances_set", value=instances_set, expected_type=type_hints["instances_set"])
                    check_type(argname="argument network_interface", value=network_interface, expected_type=type_hints["network_interface"])
                    check_type(argname="argument owner_id", value=owner_id, expected_type=type_hints["owner_id"])
                    check_type(argname="argument requester_id", value=requester_id, expected_type=type_hints["requester_id"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument reservation_id", value=reservation_id, expected_type=type_hints["reservation_id"])
                    check_type(argname="argument return_", value=return_, expected_type=type_hints["return_"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if create_fleet_response is not None:
                    self._values["create_fleet_response"] = create_fleet_response
                if create_launch_template_response is not None:
                    self._values["create_launch_template_response"] = create_launch_template_response
                if delete_launch_template_response is not None:
                    self._values["delete_launch_template_response"] = delete_launch_template_response
                if group_id is not None:
                    self._values["group_id"] = group_id
                if group_set is not None:
                    self._values["group_set"] = group_set
                if instances_set is not None:
                    self._values["instances_set"] = instances_set
                if network_interface is not None:
                    self._values["network_interface"] = network_interface
                if owner_id is not None:
                    self._values["owner_id"] = owner_id
                if requester_id is not None:
                    self._values["requester_id"] = requester_id
                if request_id is not None:
                    self._values["request_id"] = request_id
                if reservation_id is not None:
                    self._values["reservation_id"] = reservation_id
                if return_ is not None:
                    self._values["return_"] = return_

            @builtins.property
            def create_fleet_response(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.CreateFleetResponse"]:
                '''(experimental) CreateFleetResponse property.

                Specify an array of string values to match this event if the actual value of CreateFleetResponse is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("create_fleet_response")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.CreateFleetResponse"], result)

            @builtins.property
            def create_launch_template_response(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateResponse"]:
                '''(experimental) CreateLaunchTemplateResponse property.

                Specify an array of string values to match this event if the actual value of CreateLaunchTemplateResponse is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("create_launch_template_response")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateResponse"], result)

            @builtins.property
            def delete_launch_template_response(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateResponse"]:
                '''(experimental) DeleteLaunchTemplateResponse property.

                Specify an array of string values to match this event if the actual value of DeleteLaunchTemplateResponse is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("delete_launch_template_response")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateResponse"], result)

            @builtins.property
            def group_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) groupId property.

                Specify an array of string values to match this event if the actual value of groupId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("group_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def group_set(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) groupSet property.

                Specify an array of string values to match this event if the actual value of groupSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("group_set")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def instances_set(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet"]:
                '''(experimental) instancesSet property.

                Specify an array of string values to match this event if the actual value of instancesSet is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instances_set")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet"], result)

            @builtins.property
            def network_interface(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterface"]:
                '''(experimental) networkInterface property.

                Specify an array of string values to match this event if the actual value of networkInterface is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("network_interface")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterface"], result)

            @builtins.property
            def owner_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ownerId property.

                Specify an array of string values to match this event if the actual value of ownerId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("owner_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def requester_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requesterId property.

                Specify an array of string values to match this event if the actual value of requesterId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("requester_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requestId property.

                Specify an array of string values to match this event if the actual value of requestId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def reservation_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) reservationId property.

                Specify an array of string values to match this event if the actual value of reservationId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("reservation_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def return_(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) _return property.

                Specify an array of string values to match this event if the actual value of _return is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("return_")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ResponseElements(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.SecurityGroupId",
            jsii_struct_bases=[],
            name_mapping={"content": "content", "tag": "tag"},
        )
        class SecurityGroupId:
            def __init__(
                self,
                *,
                content: typing.Optional[typing.Sequence[builtins.str]] = None,
                tag: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for SecurityGroupId.

                :param content: (experimental) content property. Specify an array of string values to match this event if the actual value of content is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tag: (experimental) tag property. Specify an array of string values to match this event if the actual value of tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    security_group_id = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SecurityGroupId(
                        content=["content"],
                        tag=["tag"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__dd5cfda337adf0aa924c95dd1f4a9ee281130579188bfee537c629e4f34682fe)
                    check_type(argname="argument content", value=content, expected_type=type_hints["content"])
                    check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if content is not None:
                    self._values["content"] = content
                if tag is not None:
                    self._values["tag"] = tag

            @builtins.property
            def content(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) content property.

                Specify an array of string values to match this event if the actual value of content is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("content")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def tag(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) tag property.

                Specify an array of string values to match this event if the actual value of tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tag")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SecurityGroupId(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.SessionContext",
            jsii_struct_bases=[],
            name_mapping={
                "attributes": "attributes",
                "session_issuer": "sessionIssuer",
                "web_id_federation_data": "webIdFederationData",
            },
        )
        class SessionContext:
            def __init__(
                self,
                *,
                attributes: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
                session_issuer: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.SessionIssuer", typing.Dict[builtins.str, typing.Any]]] = None,
                web_id_federation_data: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for SessionContext.

                :param attributes: (experimental) attributes property. Specify an array of string values to match this event if the actual value of attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param session_issuer: (experimental) sessionIssuer property. Specify an array of string values to match this event if the actual value of sessionIssuer is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param web_id_federation_data: (experimental) webIdFederationData property. Specify an array of string values to match this event if the actual value of webIdFederationData is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    session_context = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SessionContext(
                        attributes=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Attributes(
                            creation_date=["creationDate"],
                            mfa_authenticated=["mfaAuthenticated"]
                        ),
                        session_issuer=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                            account_id=["accountId"],
                            arn=["arn"],
                            principal_id=["principalId"],
                            type=["type"],
                            user_name=["userName"]
                        ),
                        web_id_federation_data=["webIdFederationData"]
                    )
                '''
                if isinstance(attributes, dict):
                    attributes = InstanceEvents.AWSAPICallViaCloudTrail.Attributes(**attributes)
                if isinstance(session_issuer, dict):
                    session_issuer = InstanceEvents.AWSAPICallViaCloudTrail.SessionIssuer(**session_issuer)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__4fd2ddd96270e5843c28583668a38713eff08100c035e85cf07cfa26d3b67b23)
                    check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                    check_type(argname="argument session_issuer", value=session_issuer, expected_type=type_hints["session_issuer"])
                    check_type(argname="argument web_id_federation_data", value=web_id_federation_data, expected_type=type_hints["web_id_federation_data"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if attributes is not None:
                    self._values["attributes"] = attributes
                if session_issuer is not None:
                    self._values["session_issuer"] = session_issuer
                if web_id_federation_data is not None:
                    self._values["web_id_federation_data"] = web_id_federation_data

            @builtins.property
            def attributes(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.Attributes"]:
                '''(experimental) attributes property.

                Specify an array of string values to match this event if the actual value of attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("attributes")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.Attributes"], result)

            @builtins.property
            def session_issuer(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.SessionIssuer"]:
                '''(experimental) sessionIssuer property.

                Specify an array of string values to match this event if the actual value of sessionIssuer is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_issuer")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.SessionIssuer"], result)

            @builtins.property
            def web_id_federation_data(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) webIdFederationData property.

                Specify an array of string values to match this event if the actual value of webIdFederationData is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("web_id_federation_data")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SessionContext(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.SessionIssuer",
            jsii_struct_bases=[],
            name_mapping={
                "account_id": "accountId",
                "arn": "arn",
                "principal_id": "principalId",
                "type": "type",
                "user_name": "userName",
            },
        )
        class SessionIssuer:
            def __init__(
                self,
                *,
                account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for SessionIssuer.

                :param account_id: (experimental) accountId property. Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param principal_id: (experimental) principalId property. Specify an array of string values to match this event if the actual value of principalId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_name: (experimental) userName property. Specify an array of string values to match this event if the actual value of userName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    session_issuer = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                        account_id=["accountId"],
                        arn=["arn"],
                        principal_id=["principalId"],
                        type=["type"],
                        user_name=["userName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__655dadb2c749c4cd1d5ca0a6bd9aed4fddf445c2b20de37cb59205982975e5cb)
                    check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                    check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                    check_type(argname="argument principal_id", value=principal_id, expected_type=type_hints["principal_id"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                    check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if account_id is not None:
                    self._values["account_id"] = account_id
                if arn is not None:
                    self._values["arn"] = arn
                if principal_id is not None:
                    self._values["principal_id"] = principal_id
                if type is not None:
                    self._values["type"] = type
                if user_name is not None:
                    self._values["user_name"] = user_name

            @builtins.property
            def account_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) accountId property.

                Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("account_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) arn property.

                Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def principal_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) principalId property.

                Specify an array of string values to match this event if the actual value of principalId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("principal_id")
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

            @builtins.property
            def user_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) userName property.

                Specify an array of string values to match this event if the actual value of userName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SessionIssuer(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions",
            jsii_struct_bases=[],
            name_mapping={
                "allocation_strategy": "allocationStrategy",
                "instance_pool_constraint_filter_disabled": "instancePoolConstraintFilterDisabled",
                "instance_pools_to_use_count": "instancePoolsToUseCount",
                "max_instance_count": "maxInstanceCount",
                "max_target_capacity": "maxTargetCapacity",
            },
        )
        class SpotOptions:
            def __init__(
                self,
                *,
                allocation_strategy: typing.Optional[typing.Sequence[builtins.str]] = None,
                instance_pool_constraint_filter_disabled: typing.Optional[typing.Sequence[builtins.str]] = None,
                instance_pools_to_use_count: typing.Optional[typing.Sequence[builtins.str]] = None,
                max_instance_count: typing.Optional[typing.Sequence[builtins.str]] = None,
                max_target_capacity: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for SpotOptions.

                :param allocation_strategy: (experimental) AllocationStrategy property. Specify an array of string values to match this event if the actual value of AllocationStrategy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_pool_constraint_filter_disabled: (experimental) InstancePoolConstraintFilterDisabled property. Specify an array of string values to match this event if the actual value of InstancePoolConstraintFilterDisabled is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_pools_to_use_count: (experimental) InstancePoolsToUseCount property. Specify an array of string values to match this event if the actual value of InstancePoolsToUseCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param max_instance_count: (experimental) MaxInstanceCount property. Specify an array of string values to match this event if the actual value of MaxInstanceCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param max_target_capacity: (experimental) MaxTargetCapacity property. Specify an array of string values to match this event if the actual value of MaxTargetCapacity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    spot_options = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions(
                        allocation_strategy=["allocationStrategy"],
                        instance_pool_constraint_filter_disabled=["instancePoolConstraintFilterDisabled"],
                        instance_pools_to_use_count=["instancePoolsToUseCount"],
                        max_instance_count=["maxInstanceCount"],
                        max_target_capacity=["maxTargetCapacity"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__19aba2042fd043e9fd9acc51ec17c4a32daa1fe3bb69b811198f67d192c61f4a)
                    check_type(argname="argument allocation_strategy", value=allocation_strategy, expected_type=type_hints["allocation_strategy"])
                    check_type(argname="argument instance_pool_constraint_filter_disabled", value=instance_pool_constraint_filter_disabled, expected_type=type_hints["instance_pool_constraint_filter_disabled"])
                    check_type(argname="argument instance_pools_to_use_count", value=instance_pools_to_use_count, expected_type=type_hints["instance_pools_to_use_count"])
                    check_type(argname="argument max_instance_count", value=max_instance_count, expected_type=type_hints["max_instance_count"])
                    check_type(argname="argument max_target_capacity", value=max_target_capacity, expected_type=type_hints["max_target_capacity"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if allocation_strategy is not None:
                    self._values["allocation_strategy"] = allocation_strategy
                if instance_pool_constraint_filter_disabled is not None:
                    self._values["instance_pool_constraint_filter_disabled"] = instance_pool_constraint_filter_disabled
                if instance_pools_to_use_count is not None:
                    self._values["instance_pools_to_use_count"] = instance_pools_to_use_count
                if max_instance_count is not None:
                    self._values["max_instance_count"] = max_instance_count
                if max_target_capacity is not None:
                    self._values["max_target_capacity"] = max_target_capacity

            @builtins.property
            def allocation_strategy(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) AllocationStrategy property.

                Specify an array of string values to match this event if the actual value of AllocationStrategy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("allocation_strategy")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def instance_pool_constraint_filter_disabled(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) InstancePoolConstraintFilterDisabled property.

                Specify an array of string values to match this event if the actual value of InstancePoolConstraintFilterDisabled is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_pool_constraint_filter_disabled")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def instance_pools_to_use_count(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) InstancePoolsToUseCount property.

                Specify an array of string values to match this event if the actual value of InstancePoolsToUseCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_pools_to_use_count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def max_instance_count(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) MaxInstanceCount property.

                Specify an array of string values to match this event if the actual value of MaxInstanceCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("max_instance_count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def max_target_capacity(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) MaxTargetCapacity property.

                Specify an array of string values to match this event if the actual value of MaxTargetCapacity is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("max_target_capacity")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SpotOptions(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions1",
            jsii_struct_bases=[],
            name_mapping={
                "max_price": "maxPrice",
                "spot_instance_type": "spotInstanceType",
            },
        )
        class SpotOptions1:
            def __init__(
                self,
                *,
                max_price: typing.Optional[typing.Sequence[builtins.str]] = None,
                spot_instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for SpotOptions_1.

                :param max_price: (experimental) maxPrice property. Specify an array of string values to match this event if the actual value of maxPrice is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param spot_instance_type: (experimental) spotInstanceType property. Specify an array of string values to match this event if the actual value of spotInstanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    spot_options1 = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions1(
                        max_price=["maxPrice"],
                        spot_instance_type=["spotInstanceType"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__cfef8dfbd68deb517d1020f4ba6e223f6ac494b5f8d2ca9ba347341e43a726a9)
                    check_type(argname="argument max_price", value=max_price, expected_type=type_hints["max_price"])
                    check_type(argname="argument spot_instance_type", value=spot_instance_type, expected_type=type_hints["spot_instance_type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if max_price is not None:
                    self._values["max_price"] = max_price
                if spot_instance_type is not None:
                    self._values["spot_instance_type"] = spot_instance_type

            @builtins.property
            def max_price(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) maxPrice property.

                Specify an array of string values to match this event if the actual value of maxPrice is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("max_price")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def spot_instance_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) spotInstanceType property.

                Specify an array of string values to match this event if the actual value of spotInstanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("spot_instance_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SpotOptions1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions2",
            jsii_struct_bases=[],
            name_mapping={
                "max_price": "maxPrice",
                "spot_instance_type": "spotInstanceType",
            },
        )
        class SpotOptions2:
            def __init__(
                self,
                *,
                max_price: typing.Optional[typing.Sequence[builtins.str]] = None,
                spot_instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for SpotOptions_2.

                :param max_price: (experimental) MaxPrice property. Specify an array of string values to match this event if the actual value of MaxPrice is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param spot_instance_type: (experimental) SpotInstanceType property. Specify an array of string values to match this event if the actual value of SpotInstanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    spot_options2 = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions2(
                        max_price=["maxPrice"],
                        spot_instance_type=["spotInstanceType"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__258ae572e4116a4aa0b58c100229f695b1bbfc22ef7b7cc658afd47801b8ed7d)
                    check_type(argname="argument max_price", value=max_price, expected_type=type_hints["max_price"])
                    check_type(argname="argument spot_instance_type", value=spot_instance_type, expected_type=type_hints["spot_instance_type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if max_price is not None:
                    self._values["max_price"] = max_price
                if spot_instance_type is not None:
                    self._values["spot_instance_type"] = spot_instance_type

            @builtins.property
            def max_price(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) MaxPrice property.

                Specify an array of string values to match this event if the actual value of MaxPrice is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("max_price")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def spot_instance_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) SpotInstanceType property.

                Specify an array of string values to match this event if the actual value of SpotInstanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("spot_instance_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SpotOptions2(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.StateReason",
            jsii_struct_bases=[],
            name_mapping={"code": "code", "message": "message"},
        )
        class StateReason:
            def __init__(
                self,
                *,
                code: typing.Optional[typing.Sequence[builtins.str]] = None,
                message: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for StateReason.

                :param code: (experimental) code property. Specify an array of string values to match this event if the actual value of code is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param message: (experimental) message property. Specify an array of string values to match this event if the actual value of message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    state_reason = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.StateReason(
                        code=["code"],
                        message=["message"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__96c28e031ba0ca1f8615d974cb4b3ed265094cf43551dfe3594eac0727421122)
                    check_type(argname="argument code", value=code, expected_type=type_hints["code"])
                    check_type(argname="argument message", value=message, expected_type=type_hints["message"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if code is not None:
                    self._values["code"] = code
                if message is not None:
                    self._values["message"] = message

            @builtins.property
            def code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) code property.

                Specify an array of string values to match this event if the actual value of code is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("code")
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

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "StateReason(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.Tag",
            jsii_struct_bases=[],
            name_mapping={"key": "key", "tag": "tag", "value": "value"},
        )
        class Tag:
            def __init__(
                self,
                *,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
                tag: typing.Optional[typing.Sequence[builtins.str]] = None,
                value: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Tag.

                :param key: (experimental) Key property. Specify an array of string values to match this event if the actual value of Key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tag: (experimental) tag property. Specify an array of string values to match this event if the actual value of tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param value: (experimental) Value property. Specify an array of string values to match this event if the actual value of Value is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    tag = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Tag(
                        key=["key"],
                        tag=["tag"],
                        value=["value"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__61a95545e6f211fe6c6a45e811b8bc0c14ef7967c330a80a938aed1ef4561e3d)
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                    check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
                    check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if key is not None:
                    self._values["key"] = key
                if tag is not None:
                    self._values["tag"] = tag
                if value is not None:
                    self._values["value"] = value

            @builtins.property
            def key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Key property.

                Specify an array of string values to match this event if the actual value of Key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def tag(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) tag property.

                Specify an array of string values to match this event if the actual value of tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tag")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def value(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) Value property.

                Specify an array of string values to match this event if the actual value of Value is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("value")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Tag(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.TagSet",
            jsii_struct_bases=[],
            name_mapping={"items": "items"},
        )
        class TagSet:
            def __init__(
                self,
                *,
                items: typing.Optional[typing.Sequence[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItemItem", typing.Dict[builtins.str, typing.Any]]]] = None,
            ) -> None:
                '''(experimental) Type definition for TagSet.

                :param items: (experimental) items property. Specify an array of string values to match this event if the actual value of items is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    tag_set = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSet(
                        items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItemItem(
                            key=["key"],
                            value=["value"]
                        )]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__cafa1b710f357aab97385164446159a65740379924ff120ffffcf986bcc1c1a9)
                    check_type(argname="argument items", value=items, expected_type=type_hints["items"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if items is not None:
                    self._values["items"] = items

            @builtins.property
            def items(
                self,
            ) -> typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItemItem"]]:
                '''(experimental) items property.

                Specify an array of string values to match this event if the actual value of items is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("items")
                return typing.cast(typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItemItem"]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "TagSet(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecification",
            jsii_struct_bases=[],
            name_mapping={"resource_type": "resourceType", "tag": "tag"},
        )
        class TagSpecification:
            def __init__(
                self,
                *,
                resource_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                tag: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.Tag", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for TagSpecification.

                :param resource_type: (experimental) ResourceType property. Specify an array of string values to match this event if the actual value of ResourceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tag: (experimental) Tag property. Specify an array of string values to match this event if the actual value of Tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    tag_specification = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecification(
                        resource_type=["resourceType"],
                        tag=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Tag(
                            key=["key"],
                            tag=["tag"],
                            value=["value"]
                        )
                    )
                '''
                if isinstance(tag, dict):
                    tag = InstanceEvents.AWSAPICallViaCloudTrail.Tag(**tag)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__f893531394408b53539961fda00095891bad6b7bbb0d2e798d465babd95a7adb)
                    check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
                    check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if resource_type is not None:
                    self._values["resource_type"] = resource_type
                if tag is not None:
                    self._values["tag"] = tag

            @builtins.property
            def resource_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ResourceType property.

                Specify an array of string values to match this event if the actual value of ResourceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("resource_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def tag(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.Tag"]:
                '''(experimental) Tag property.

                Specify an array of string values to match this event if the actual value of Tag is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tag")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.Tag"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "TagSpecification(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSet",
            jsii_struct_bases=[],
            name_mapping={"items": "items"},
        )
        class TagSpecificationSet:
            def __init__(
                self,
                *,
                items: typing.Optional[typing.Sequence[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItem", typing.Dict[builtins.str, typing.Any]]]] = None,
            ) -> None:
                '''(experimental) Type definition for TagSpecificationSet.

                :param items: (experimental) items property. Specify an array of string values to match this event if the actual value of items is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    tag_specification_set = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSet(
                        items=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItem(
                            resource_type=["resourceType"],
                            tags=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItemItem(
                                key=["key"],
                                value=["value"]
                            )]
                        )]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__1d166e9b79f868aab164b926dc452378fc2ef1fd52e8732789106f686584175a)
                    check_type(argname="argument items", value=items, expected_type=type_hints["items"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if items is not None:
                    self._values["items"] = items

            @builtins.property
            def items(
                self,
            ) -> typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItem"]]:
                '''(experimental) items property.

                Specify an array of string values to match this event if the actual value of items is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("items")
                return typing.cast(typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItem"]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "TagSpecificationSet(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItem",
            jsii_struct_bases=[],
            name_mapping={"resource_type": "resourceType", "tags": "tags"},
        )
        class TagSpecificationSetItem:
            def __init__(
                self,
                *,
                resource_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                tags: typing.Optional[typing.Sequence[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItemItem", typing.Dict[builtins.str, typing.Any]]]] = None,
            ) -> None:
                '''(experimental) Type definition for TagSpecificationSetItem.

                :param resource_type: (experimental) resourceType property. Specify an array of string values to match this event if the actual value of resourceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tags: (experimental) tags property. Specify an array of string values to match this event if the actual value of tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    tag_specification_set_item = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItem(
                        resource_type=["resourceType"],
                        tags=[ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItemItem(
                            key=["key"],
                            value=["value"]
                        )]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__1d433978d6894c83f33fe79f66769badebbdbdb59c93c42de3e1f9b45efeef8d)
                    check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
                    check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if resource_type is not None:
                    self._values["resource_type"] = resource_type
                if tags is not None:
                    self._values["tags"] = tags

            @builtins.property
            def resource_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) resourceType property.

                Specify an array of string values to match this event if the actual value of resourceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("resource_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def tags(
                self,
            ) -> typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItemItem"]]:
                '''(experimental) tags property.

                Specify an array of string values to match this event if the actual value of tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tags")
                return typing.cast(typing.Optional[typing.List["InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItemItem"]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "TagSpecificationSetItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItemItem",
            jsii_struct_bases=[],
            name_mapping={"key": "key", "value": "value"},
        )
        class TagSpecificationSetItemItem:
            def __init__(
                self,
                *,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
                value: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for TagSpecificationSetItemItem.

                :param key: (experimental) key property. Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param value: (experimental) value property. Specify an array of string values to match this event if the actual value of value is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    tag_specification_set_item_item = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItemItem(
                        key=["key"],
                        value=["value"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__104142981c85b4b653a0a228b91aef7274e4f6fbeed65ccb677e3aba1d1ee7fe)
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                    check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if key is not None:
                    self._values["key"] = key
                if value is not None:
                    self._values["value"] = value

            @builtins.property
            def key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) key property.

                Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def value(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) value property.

                Specify an array of string values to match this event if the actual value of value is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("value")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "TagSpecificationSetItemItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.TargetCapacitySpecification",
            jsii_struct_bases=[],
            name_mapping={
                "default_target_capacity_type": "defaultTargetCapacityType",
                "on_demand_target_capacity": "onDemandTargetCapacity",
                "spot_target_capacity": "spotTargetCapacity",
                "total_target_capacity": "totalTargetCapacity",
            },
        )
        class TargetCapacitySpecification:
            def __init__(
                self,
                *,
                default_target_capacity_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                on_demand_target_capacity: typing.Optional[typing.Sequence[builtins.str]] = None,
                spot_target_capacity: typing.Optional[typing.Sequence[builtins.str]] = None,
                total_target_capacity: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for TargetCapacitySpecification.

                :param default_target_capacity_type: (experimental) DefaultTargetCapacityType property. Specify an array of string values to match this event if the actual value of DefaultTargetCapacityType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param on_demand_target_capacity: (experimental) OnDemandTargetCapacity property. Specify an array of string values to match this event if the actual value of OnDemandTargetCapacity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param spot_target_capacity: (experimental) SpotTargetCapacity property. Specify an array of string values to match this event if the actual value of SpotTargetCapacity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param total_target_capacity: (experimental) TotalTargetCapacity property. Specify an array of string values to match this event if the actual value of TotalTargetCapacity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    target_capacity_specification = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.TargetCapacitySpecification(
                        default_target_capacity_type=["defaultTargetCapacityType"],
                        on_demand_target_capacity=["onDemandTargetCapacity"],
                        spot_target_capacity=["spotTargetCapacity"],
                        total_target_capacity=["totalTargetCapacity"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__51a58eb341a6679cfe38b48c66345e40a469536b3c4b26f366952b619fd38feb)
                    check_type(argname="argument default_target_capacity_type", value=default_target_capacity_type, expected_type=type_hints["default_target_capacity_type"])
                    check_type(argname="argument on_demand_target_capacity", value=on_demand_target_capacity, expected_type=type_hints["on_demand_target_capacity"])
                    check_type(argname="argument spot_target_capacity", value=spot_target_capacity, expected_type=type_hints["spot_target_capacity"])
                    check_type(argname="argument total_target_capacity", value=total_target_capacity, expected_type=type_hints["total_target_capacity"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if default_target_capacity_type is not None:
                    self._values["default_target_capacity_type"] = default_target_capacity_type
                if on_demand_target_capacity is not None:
                    self._values["on_demand_target_capacity"] = on_demand_target_capacity
                if spot_target_capacity is not None:
                    self._values["spot_target_capacity"] = spot_target_capacity
                if total_target_capacity is not None:
                    self._values["total_target_capacity"] = total_target_capacity

            @builtins.property
            def default_target_capacity_type(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) DefaultTargetCapacityType property.

                Specify an array of string values to match this event if the actual value of DefaultTargetCapacityType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("default_target_capacity_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def on_demand_target_capacity(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) OnDemandTargetCapacity property.

                Specify an array of string values to match this event if the actual value of OnDemandTargetCapacity is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("on_demand_target_capacity")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def spot_target_capacity(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) SpotTargetCapacity property.

                Specify an array of string values to match this event if the actual value of SpotTargetCapacity is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("spot_target_capacity")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def total_target_capacity(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) TotalTargetCapacity property.

                Specify an array of string values to match this event if the actual value of TotalTargetCapacity is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("total_target_capacity")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "TargetCapacitySpecification(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.AWSAPICallViaCloudTrail.UserIdentity",
            jsii_struct_bases=[],
            name_mapping={
                "access_key_id": "accessKeyId",
                "account_id": "accountId",
                "arn": "arn",
                "invoked_by": "invokedBy",
                "principal_id": "principalId",
                "session_context": "sessionContext",
                "type": "type",
            },
        )
        class UserIdentity:
            def __init__(
                self,
                *,
                access_key_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                invoked_by: typing.Optional[typing.Sequence[builtins.str]] = None,
                principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                session_context: typing.Optional[typing.Union["InstanceEvents.AWSAPICallViaCloudTrail.SessionContext", typing.Dict[builtins.str, typing.Any]]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for UserIdentity.

                :param access_key_id: (experimental) accessKeyId property. Specify an array of string values to match this event if the actual value of accessKeyId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param account_id: (experimental) accountId property. Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param invoked_by: (experimental) invokedBy property. Specify an array of string values to match this event if the actual value of invokedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param principal_id: (experimental) principalId property. Specify an array of string values to match this event if the actual value of principalId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param session_context: (experimental) sessionContext property. Specify an array of string values to match this event if the actual value of sessionContext is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    user_identity = ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.UserIdentity(
                        access_key_id=["accessKeyId"],
                        account_id=["accountId"],
                        arn=["arn"],
                        invoked_by=["invokedBy"],
                        principal_id=["principalId"],
                        session_context=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SessionContext(
                            attributes=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.Attributes(
                                creation_date=["creationDate"],
                                mfa_authenticated=["mfaAuthenticated"]
                            ),
                            session_issuer=ec2_events.InstanceEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                                account_id=["accountId"],
                                arn=["arn"],
                                principal_id=["principalId"],
                                type=["type"],
                                user_name=["userName"]
                            ),
                            web_id_federation_data=["webIdFederationData"]
                        ),
                        type=["type"]
                    )
                '''
                if isinstance(session_context, dict):
                    session_context = InstanceEvents.AWSAPICallViaCloudTrail.SessionContext(**session_context)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__1698d7b57ae1b252c6193eb25037e747b1638cdfe66365d70e1f4ff8c148ef84)
                    check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
                    check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                    check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                    check_type(argname="argument invoked_by", value=invoked_by, expected_type=type_hints["invoked_by"])
                    check_type(argname="argument principal_id", value=principal_id, expected_type=type_hints["principal_id"])
                    check_type(argname="argument session_context", value=session_context, expected_type=type_hints["session_context"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if access_key_id is not None:
                    self._values["access_key_id"] = access_key_id
                if account_id is not None:
                    self._values["account_id"] = account_id
                if arn is not None:
                    self._values["arn"] = arn
                if invoked_by is not None:
                    self._values["invoked_by"] = invoked_by
                if principal_id is not None:
                    self._values["principal_id"] = principal_id
                if session_context is not None:
                    self._values["session_context"] = session_context
                if type is not None:
                    self._values["type"] = type

            @builtins.property
            def access_key_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) accessKeyId property.

                Specify an array of string values to match this event if the actual value of accessKeyId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("access_key_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def account_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) accountId property.

                Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("account_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) arn property.

                Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def invoked_by(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) invokedBy property.

                Specify an array of string values to match this event if the actual value of invokedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("invoked_by")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def principal_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) principalId property.

                Specify an array of string values to match this event if the actual value of principalId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("principal_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def session_context(
                self,
            ) -> typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.SessionContext"]:
                '''(experimental) sessionContext property.

                Specify an array of string values to match this event if the actual value of sessionContext is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_context")
                return typing.cast(typing.Optional["InstanceEvents.AWSAPICallViaCloudTrail.SessionContext"], result)

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
                return "UserIdentity(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class EC2InstanceStateChangeNotification(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.EC2InstanceStateChangeNotification",
    ):
        '''(experimental) aws.ec2@EC2InstanceStateChangeNotification event types for Instance.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
            
            e_c2_instance_state_change_notification = ec2_events.InstanceEvents.EC2InstanceStateChangeNotification()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.EC2InstanceStateChangeNotification.EC2InstanceStateChangeNotificationProps",
            jsii_struct_bases=[],
            name_mapping={
                "event_metadata": "eventMetadata",
                "instance_id": "instanceId",
                "state": "state",
            },
        )
        class EC2InstanceStateChangeNotificationProps:
            def __init__(
                self,
                *,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                state: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Instance aws.ec2@EC2InstanceStateChangeNotification event.

                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param instance_id: (experimental) instance-id property. Specify an array of string values to match this event if the actual value of instance-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Instance reference
                :param state: (experimental) state property. Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    e_c2_instance_state_change_notification_props = ec2_events.InstanceEvents.EC2InstanceStateChangeNotification.EC2InstanceStateChangeNotificationProps(
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        instance_id=["instanceId"],
                        state=["state"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__c6ed3ede7b118424045ec343333c887e9f34a9ae961d8a458a6e5b808da808c9)
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
                    check_type(argname="argument state", value=state, expected_type=type_hints["state"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if instance_id is not None:
                    self._values["instance_id"] = instance_id
                if state is not None:
                    self._values["state"] = state

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
            def state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) state property.

                Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("state")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "EC2InstanceStateChangeNotificationProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class EC2SpotInstanceInterruptionWarning(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.EC2SpotInstanceInterruptionWarning",
    ):
        '''(experimental) aws.ec2@EC2SpotInstanceInterruptionWarning event types for Instance.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
            
            e_c2_spot_instance_interruption_warning = ec2_events.InstanceEvents.EC2SpotInstanceInterruptionWarning()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_ec2.events.InstanceEvents.EC2SpotInstanceInterruptionWarning.EC2SpotInstanceInterruptionWarningProps",
            jsii_struct_bases=[],
            name_mapping={
                "event_metadata": "eventMetadata",
                "instance_action": "instanceAction",
                "instance_id": "instanceId",
            },
        )
        class EC2SpotInstanceInterruptionWarningProps:
            def __init__(
                self,
                *,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                instance_action: typing.Optional[typing.Sequence[builtins.str]] = None,
                instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Instance aws.ec2@EC2SpotInstanceInterruptionWarning event.

                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param instance_action: (experimental) instance-action property. Specify an array of string values to match this event if the actual value of instance-action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_id: (experimental) instance-id property. Specify an array of string values to match this event if the actual value of instance-id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Instance reference

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_ec2 import events as ec2_events
                    
                    e_c2_spot_instance_interruption_warning_props = ec2_events.InstanceEvents.EC2SpotInstanceInterruptionWarning.EC2SpotInstanceInterruptionWarningProps(
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        instance_action=["instanceAction"],
                        instance_id=["instanceId"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__1aeb96463e6caca904445b09f670d4d7f66ef18178abc8954601b6e7e638bcb7)
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument instance_action", value=instance_action, expected_type=type_hints["instance_action"])
                    check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if instance_action is not None:
                    self._values["instance_action"] = instance_action
                if instance_id is not None:
                    self._values["instance_id"] = instance_id

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
            def instance_action(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instance-action property.

                Specify an array of string values to match this event if the actual value of instance-action is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_action")
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

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "EC2SpotInstanceInterruptionWarningProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "InstanceEvents",
]

publication.publish()

def _typecheckingstub__a5352af6d26a80d213c38949b3d48fe4eb34e4981293dfa424dc3a3055df2e5d(
    instance_ref: _aws_cdk_interfaces_aws_ec2_ceddda9d.IInstanceRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af87d466137a8d2827d9ff6aec47b98251e0abb255638219bd66d2c82d440e1(
    *,
    aws_region: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_message: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_source: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_parameters: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.RequestParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    response_elements: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.ResponseElements, typing.Dict[builtins.str, typing.Any]]] = None,
    source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_identity: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.UserIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374852cd79152bb3e2b21bd41510c83630fa3f8254a8934c5921cf1e5ec1d3b6(
    *,
    attachment_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    attach_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    delete_on_termination: typing.Optional[typing.Sequence[builtins.str]] = None,
    device_index: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95aa3ccbce662e29b86925d318c10b8f5bc86123d62359de95adf412db7b4778(
    *,
    creation_date: typing.Optional[typing.Sequence[builtins.str]] = None,
    mfa_authenticated: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__748cf5f120b22b2689c0ebb0de0a16e4fee50d092544de275910e48d13e02eff(
    *,
    capacity_reservation_preference: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__161cc862e0be22e176f67d09de0f72b4ca72a6811654a376528d0818a16ce2b0(
    *,
    core_count: typing.Optional[typing.Sequence[builtins.str]] = None,
    threads_per_core: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030bd01279c90beb3a428ed91eb67b234fea18c57471c0c1dcffac1207b172f2(
    *,
    client_token: typing.Optional[typing.Sequence[builtins.str]] = None,
    existing_instances: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.ExistingInstances, typing.Dict[builtins.str, typing.Any]]] = None,
    launch_template_configs: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateConfigs, typing.Dict[builtins.str, typing.Any]]] = None,
    on_demand_options: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.OnDemandOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    spot_options: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_specification: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.TagSpecification, typing.Dict[builtins.str, typing.Any]]] = None,
    target_capacity_specification: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.TargetCapacitySpecification, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada89cb7e7ef99166fdc7d51dac073f7d20ffe6ce0c819d403f15540c9aa5192(
    *,
    error_set: typing.Optional[typing.Sequence[builtins.str]] = None,
    fleet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    fleet_instance_set: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    xmlns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1c8e9e767b64411b510a673bebcbe1e4f971693a40e6e4a3ede667de41f9628(
    *,
    launch_template_data: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateData, typing.Dict[builtins.str, typing.Any]]] = None,
    launch_template_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08250557ba6a2587a3fa94b1e2b14be7f21c3b5660c90403a43a469ff246df52(
    *,
    launch_template_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__779e13250be5511f578ccc8669dfa3457a35153979a963336894df80c375a8ba(
    *,
    launch_template: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate1, typing.Dict[builtins.str, typing.Any]]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    xmlns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9cc9dae10ec8e474e7434903ca02941e1ab10e1911599c3638a0aa8ef72db8(
    *,
    enabled: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35919d85ab88b879ff221bc792c6117926a59a36971f14f0b35e3798ebf44ac1(
    *,
    availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
    count: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    market_option: typing.Optional[typing.Sequence[builtins.str]] = None,
    operating_system: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3b7356f390410d4eaa38f16f303b0c971e4b7c81149a89a73898996acf265b(
    *,
    items: typing.Optional[typing.Sequence[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.GroupSet1Item, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cddda1126bc7b85ccfba6aebf3e054cbba3cdb5dcafa26b84075e9ba79945db5(
    *,
    group_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d762c5bfb573d4b7f5631beff7e6f2969ca63bee5a4a1d2092e135f67bfd5e47(
    *,
    items: typing.Optional[typing.Sequence[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a838237263ddbfbc5d2146d11d3730e1fd756b278f6eda0003de1ed8635c30a0(
    *,
    group_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85c8f144ec0bdd769e9d662d98c595711fb128c42675ea2607ee0727d2560fb2(
    *,
    items: typing.Optional[typing.Sequence[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2Item, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5702b0e43e6cc4373bb45a5fba68c14c28bbffd2f827a70e4c35fb408462d98a(
    *,
    market_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    spot_options: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions1, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c800b08c1a9a67ee7a77ac0489c5128b6bfdd52cfec82874d50a1a89d4ee620(
    *,
    market_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    spot_options: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.SpotOptions2, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae6d0470565d233c804fe1145c175fedd14e0a45f9fce1ce5cf6b65183ce0a2d(
    *,
    code: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f6c6129972df9dc8ac56a18bb37d5585d6796b520f03a5d64620d12011a06f9(
    *,
    items: typing.Optional[typing.Sequence[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.InstancesSetItem, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a810ec72970081dd109d62c211ca7eab09d61a759d93ba9c6aa6dbeb44be525(
    *,
    items: typing.Optional[typing.Sequence[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet1Item, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f9f1cf045d80b4b5e90f6d37685c83df33cfc9f8520c134cd6233069b3ccef(
    *,
    image_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_count: typing.Optional[typing.Sequence[builtins.str]] = None,
    min_count: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b89073e73793af38f3e7003c25f44cf4b74eebecd8f187afeac59fe3ebc277b(
    *,
    ami_launch_index: typing.Optional[typing.Sequence[builtins.str]] = None,
    architecture: typing.Optional[typing.Sequence[builtins.str]] = None,
    block_device_mapping: typing.Optional[typing.Sequence[builtins.str]] = None,
    capacity_reservation_specification: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.CapacityReservationSpecification, typing.Dict[builtins.str, typing.Any]]] = None,
    client_token: typing.Optional[typing.Sequence[builtins.str]] = None,
    cpu_options: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.CpuOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    current_state: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.InstanceState, typing.Dict[builtins.str, typing.Any]]] = None,
    ebs_optimized: typing.Optional[typing.Sequence[builtins.str]] = None,
    enclave_options: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.EnclaveOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    group_set: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2, typing.Dict[builtins.str, typing.Any]]] = None,
    hypervisor: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_lifecycle: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_state: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.InstanceState, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    launch_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    monitoring: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.Monitoring1, typing.Dict[builtins.str, typing.Any]]] = None,
    network_interface_set: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1, typing.Dict[builtins.str, typing.Any]]] = None,
    placement: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.Placement, typing.Dict[builtins.str, typing.Any]]] = None,
    previous_state: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.InstanceState, typing.Dict[builtins.str, typing.Any]]] = None,
    private_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    product_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    root_device_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    root_device_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_dest_check: typing.Optional[typing.Sequence[builtins.str]] = None,
    spot_instance_request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    state_reason: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.StateReason, typing.Dict[builtins.str, typing.Any]]] = None,
    subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_set: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.TagSet, typing.Dict[builtins.str, typing.Any]]] = None,
    virtualization_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ab16eec5d4aed85cdbabefebe222f14bbd24a7c2c65ee8a17da46ee1c2f52d(
    *,
    launch_template_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6d3a5b77c875b32e411ec34d1b46d0d009e9c485fd2cdbbdc32c3088a19dfc8(
    *,
    created_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    create_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_version_number: typing.Optional[typing.Sequence[builtins.str]] = None,
    latest_version_number: typing.Optional[typing.Sequence[builtins.str]] = None,
    launch_template_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    launch_template_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7fd4b54f27fa211d7355c7d77c6d259ec15ec460b2af4c5a58e2c4cf30023c3(
    *,
    launch_template_specification: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplateSpecification, typing.Dict[builtins.str, typing.Any]]] = None,
    overrides: typing.Optional[typing.Sequence[typing.Any]] = None,
    tag: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95204bf01d0fd6dd98f65b9baf42ccfbbd41027f6343c2a6b358d2034d06fe4d(
    *,
    image_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_market_options: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.InstanceMarketOptions1, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_interface: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterface1, typing.Dict[builtins.str, typing.Any]]] = None,
    user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761e170e2e3e6f52ed74840d8fbd3e248a575d3c28a6f686e07dd14c7ba6bab2(
    *,
    launch_template_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70c38dd40fbdbe925c31f9da42637549d2b30b4e7736b201d240b327a1395097(
    *,
    enabled: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__867e3e98deddfda165d9013ad31ff5bf2297930dd2746be49e24487d22ba2100(
    *,
    state: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f5bff2427627cecc1fffb6c74e02b56cacbde9023679bd6bc8373ed29b8e9c(
    *,
    availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[typing.Sequence[builtins.str]] = None,
    group_set: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.GroupSet2, typing.Dict[builtins.str, typing.Any]]] = None,
    interface_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    ipv6_addresses_set: typing.Optional[typing.Sequence[builtins.str]] = None,
    mac_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_interface_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    owner_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    private_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    private_ip_addresses_set: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1, typing.Dict[builtins.str, typing.Any]]] = None,
    requester_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    requester_managed: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_dest_check: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_set: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5bc3519a30abfc7d2b326761c249257189f84410a1ac0334def48fa96cb2e86(
    *,
    device_index: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_group_id: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.SecurityGroupId, typing.Dict[builtins.str, typing.Any]]] = None,
    subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f6b68f13a4eaad72a1fa8fcd5527e67c8658651a171ef1cd2d646c0a6ff693e(
    *,
    items: typing.Optional[typing.Sequence[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSetItem, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b5673f2e1e9b64da1a945761fff4ce66a83c1c6fd40e1e65705e38993351723(
    *,
    items: typing.Optional[typing.Sequence[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet1Item, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90986c59311afaab923444c2c7e871ac04f83be816045ffdf210b543f58d8ecb(
    *,
    attachment: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.Attachment, typing.Dict[builtins.str, typing.Any]]] = None,
    group_set: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.GroupSet3, typing.Dict[builtins.str, typing.Any]]] = None,
    interface_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    ipv6_addresses_set: typing.Optional[typing.Sequence[builtins.str]] = None,
    mac_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_interface_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    owner_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    private_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    private_ip_addresses_set: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet2, typing.Dict[builtins.str, typing.Any]]] = None,
    source_dest_check: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_set: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be943c83da95e53c00f3837025f0129f93e9a196e8ec104a58ad1cfad0de0ed9(
    *,
    device_index: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f6bfc4e3eedab1b03bedeacbb77ef623860f20a4e3bd9360117411b4ccbc688(
    *,
    allocation_strategy: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_pool_constraint_filter_disabled: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_instance_count: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_target_capacity: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8da6835d42c7ba911091f3f64a5667781519c248a0d0fd4673c97f478be3a27(
    *,
    availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
    tenancy: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe652185c5fa050c66679c2fff9179c1b6f36148fa300c266fd8ab1f7299e259(
    *,
    item: typing.Optional[typing.Sequence[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2830bf227e7b699c0a215abf0edb9ab50cff49df4cc51e61b1cd48632e2f4d32(
    *,
    primary: typing.Optional[typing.Sequence[builtins.str]] = None,
    private_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba43b91eb28e2714bedc3b3388c7eb5fa069cc499568b5bcd713a867fb4003b(
    *,
    item: typing.Optional[typing.Sequence[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.PrivateIpAddressesSet1Item, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa62146d02ad16f183a3a35e862a77e6f5aa36b0f5afb91c405ed576d6719484(
    *,
    availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
    block_device_mapping: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_token: typing.Optional[typing.Sequence[builtins.str]] = None,
    create_fleet_request: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.CreateFleetRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    create_launch_template_request: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.CreateLaunchTemplateRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    delete_launch_template_request: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[typing.Sequence[builtins.str]] = None,
    disable_api_termination: typing.Optional[typing.Sequence[builtins.str]] = None,
    group_description: typing.Optional[typing.Sequence[builtins.str]] = None,
    group_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    group_set: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.GroupSet1, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_market_options: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.InstanceMarketOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    instances_set: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet1, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    ipv6_address_count: typing.Optional[typing.Sequence[builtins.str]] = None,
    launch_template: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.LaunchTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    monitoring: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.Monitoring, typing.Dict[builtins.str, typing.Any]]] = None,
    network_interface_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_interface_set: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterfaceSet, typing.Dict[builtins.str, typing.Any]]] = None,
    private_ip_addresses_set: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_specification_set: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSet, typing.Dict[builtins.str, typing.Any]]] = None,
    user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66ae8ce4979d3800e7bdb0e2b37ecd5e70dfffcf65ddbad398f9210ec11aee7(
    *,
    create_fleet_response: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.CreateFleetResponse, typing.Dict[builtins.str, typing.Any]]] = None,
    create_launch_template_response: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateResponse, typing.Dict[builtins.str, typing.Any]]] = None,
    delete_launch_template_response: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.DeleteLaunchTemplateResponse, typing.Dict[builtins.str, typing.Any]]] = None,
    group_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    group_set: typing.Optional[typing.Sequence[builtins.str]] = None,
    instances_set: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.InstancesSet, typing.Dict[builtins.str, typing.Any]]] = None,
    network_interface: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.NetworkInterface, typing.Dict[builtins.str, typing.Any]]] = None,
    owner_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    requester_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    reservation_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    return_: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd5cfda337adf0aa924c95dd1f4a9ee281130579188bfee537c629e4f34682fe(
    *,
    content: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd2ddd96270e5843c28583668a38713eff08100c035e85cf07cfa26d3b67b23(
    *,
    attributes: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.Attributes, typing.Dict[builtins.str, typing.Any]]] = None,
    session_issuer: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.SessionIssuer, typing.Dict[builtins.str, typing.Any]]] = None,
    web_id_federation_data: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__655dadb2c749c4cd1d5ca0a6bd9aed4fddf445c2b20de37cb59205982975e5cb(
    *,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19aba2042fd043e9fd9acc51ec17c4a32daa1fe3bb69b811198f67d192c61f4a(
    *,
    allocation_strategy: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_pool_constraint_filter_disabled: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_pools_to_use_count: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_instance_count: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_target_capacity: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfef8dfbd68deb517d1020f4ba6e223f6ac494b5f8d2ca9ba347341e43a726a9(
    *,
    max_price: typing.Optional[typing.Sequence[builtins.str]] = None,
    spot_instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__258ae572e4116a4aa0b58c100229f695b1bbfc22ef7b7cc658afd47801b8ed7d(
    *,
    max_price: typing.Optional[typing.Sequence[builtins.str]] = None,
    spot_instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c28e031ba0ca1f8615d974cb4b3ed265094cf43551dfe3594eac0727421122(
    *,
    code: typing.Optional[typing.Sequence[builtins.str]] = None,
    message: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a95545e6f211fe6c6a45e811b8bc0c14ef7967c330a80a938aed1ef4561e3d(
    *,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag: typing.Optional[typing.Sequence[builtins.str]] = None,
    value: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cafa1b710f357aab97385164446159a65740379924ff120ffffcf986bcc1c1a9(
    *,
    items: typing.Optional[typing.Sequence[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItemItem, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f893531394408b53539961fda00095891bad6b7bbb0d2e798d465babd95a7adb(
    *,
    resource_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.Tag, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d166e9b79f868aab164b926dc452378fc2ef1fd52e8732789106f686584175a(
    *,
    items: typing.Optional[typing.Sequence[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItem, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d433978d6894c83f33fe79f66769badebbdbdb59c93c42de3e1f9b45efeef8d(
    *,
    resource_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.TagSpecificationSetItemItem, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__104142981c85b4b653a0a228b91aef7274e4f6fbeed65ccb677e3aba1d1ee7fe(
    *,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
    value: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51a58eb341a6679cfe38b48c66345e40a469536b3c4b26f366952b619fd38feb(
    *,
    default_target_capacity_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    on_demand_target_capacity: typing.Optional[typing.Sequence[builtins.str]] = None,
    spot_target_capacity: typing.Optional[typing.Sequence[builtins.str]] = None,
    total_target_capacity: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1698d7b57ae1b252c6193eb25037e747b1638cdfe66365d70e1f4ff8c148ef84(
    *,
    access_key_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    invoked_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_context: typing.Optional[typing.Union[InstanceEvents.AWSAPICallViaCloudTrail.SessionContext, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ed3ede7b118424045ec343333c887e9f34a9ae961d8a458a6e5b808da808c9(
    *,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    state: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aeb96463e6caca904445b09f670d4d7f66ef18178abc8954601b6e7e638bcb7(
    *,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_action: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
