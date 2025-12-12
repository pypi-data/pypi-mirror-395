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
import constructs as _constructs_77d1e7e8
from ...core import IMixin as _IMixin_11e4b965, Mixin as _Mixin_a69446c0
from ...mixins import (
    CfnPropertyMixinOptions as _CfnPropertyMixinOptions_9cbff649,
    PropertyMergeStrategy as _PropertyMergeStrategy_49c157e8,
)


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_group_name": "autoScalingGroupName",
        "availability_zone_distribution": "availabilityZoneDistribution",
        "availability_zone_impairment_policy": "availabilityZoneImpairmentPolicy",
        "availability_zones": "availabilityZones",
        "capacity_rebalance": "capacityRebalance",
        "capacity_reservation_specification": "capacityReservationSpecification",
        "context": "context",
        "cooldown": "cooldown",
        "default_instance_warmup": "defaultInstanceWarmup",
        "desired_capacity": "desiredCapacity",
        "desired_capacity_type": "desiredCapacityType",
        "health_check_grace_period": "healthCheckGracePeriod",
        "health_check_type": "healthCheckType",
        "instance_id": "instanceId",
        "instance_maintenance_policy": "instanceMaintenancePolicy",
        "launch_configuration_name": "launchConfigurationName",
        "launch_template": "launchTemplate",
        "lifecycle_hook_specification_list": "lifecycleHookSpecificationList",
        "load_balancer_names": "loadBalancerNames",
        "max_instance_lifetime": "maxInstanceLifetime",
        "max_size": "maxSize",
        "metrics_collection": "metricsCollection",
        "min_size": "minSize",
        "mixed_instances_policy": "mixedInstancesPolicy",
        "new_instances_protected_from_scale_in": "newInstancesProtectedFromScaleIn",
        "notification_configuration": "notificationConfiguration",
        "notification_configurations": "notificationConfigurations",
        "placement_group": "placementGroup",
        "service_linked_role_arn": "serviceLinkedRoleArn",
        "skip_zonal_shift_validation": "skipZonalShiftValidation",
        "tags": "tags",
        "target_group_arns": "targetGroupArns",
        "termination_policies": "terminationPolicies",
        "traffic_sources": "trafficSources",
        "vpc_zone_identifier": "vpcZoneIdentifier",
    },
)
class CfnAutoScalingGroupMixinProps:
    def __init__(
        self,
        *,
        auto_scaling_group_name: typing.Optional[builtins.str] = None,
        availability_zone_distribution: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.AvailabilityZoneDistributionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        availability_zone_impairment_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.AvailabilityZoneImpairmentPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        capacity_rebalance: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        capacity_reservation_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.CapacityReservationSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        context: typing.Optional[builtins.str] = None,
        cooldown: typing.Optional[builtins.str] = None,
        default_instance_warmup: typing.Optional[jsii.Number] = None,
        desired_capacity: typing.Optional[builtins.str] = None,
        desired_capacity_type: typing.Optional[builtins.str] = None,
        health_check_grace_period: typing.Optional[jsii.Number] = None,
        health_check_type: typing.Optional[builtins.str] = None,
        instance_id: typing.Optional[builtins.str] = None,
        instance_maintenance_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.InstanceMaintenancePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        launch_configuration_name: typing.Optional[builtins.str] = None,
        launch_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        lifecycle_hook_specification_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.LifecycleHookSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        load_balancer_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_instance_lifetime: typing.Optional[jsii.Number] = None,
        max_size: typing.Optional[builtins.str] = None,
        metrics_collection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.MetricsCollectionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        min_size: typing.Optional[builtins.str] = None,
        mixed_instances_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.MixedInstancesPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        new_instances_protected_from_scale_in: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        notification_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.NotificationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        notification_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.NotificationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        placement_group: typing.Optional[builtins.str] = None,
        service_linked_role_arn: typing.Optional[builtins.str] = None,
        skip_zonal_shift_validation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnAutoScalingGroupPropsMixin.TagPropertyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        target_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        termination_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        traffic_sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.TrafficSourceIdentifierProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        vpc_zone_identifier: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnAutoScalingGroupPropsMixin.

        :param auto_scaling_group_name: The name of the Auto Scaling group. This name must be unique per Region per account. The name can contain any ASCII character 33 to 126 including most punctuation characters, digits, and upper and lowercased letters. .. epigraph:: You cannot use a colon (:) in the name.
        :param availability_zone_distribution: The instance capacity distribution across Availability Zones.
        :param availability_zone_impairment_policy: The Availability Zone impairment policy.
        :param availability_zones: A list of Availability Zones where instances in the Auto Scaling group can be created. Used for launching into the default VPC subnet in each Availability Zone when not using the ``VPCZoneIdentifier`` property, or for attaching a network interface when an existing network interface ID is specified in a launch template.
        :param capacity_rebalance: Indicates whether Capacity Rebalancing is enabled. Otherwise, Capacity Rebalancing is disabled. When you turn on Capacity Rebalancing, Amazon EC2 Auto Scaling attempts to launch a Spot Instance whenever Amazon EC2 notifies that a Spot Instance is at an elevated risk of interruption. After launching a new instance, it then terminates an old instance. For more information, see `Use Capacity Rebalancing to handle Amazon EC2 Spot Interruptions <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-capacity-rebalancing.html>`_ in the in the *Amazon EC2 Auto Scaling User Guide* .
        :param capacity_reservation_specification: The capacity reservation specification.
        :param context: Reserved.
        :param cooldown: *Only needed if you use simple scaling policies.*. The amount of time, in seconds, between one scaling activity ending and another one starting due to simple scaling policies. For more information, see `Scaling cooldowns for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-scaling-cooldowns.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . Default: ``300`` seconds
        :param default_instance_warmup: The amount of time, in seconds, until a new instance is considered to have finished initializing and resource consumption to become stable after it enters the ``InService`` state. During an instance refresh, Amazon EC2 Auto Scaling waits for the warm-up period after it replaces an instance before it moves on to replacing the next instance. Amazon EC2 Auto Scaling also waits for the warm-up period before aggregating the metrics for new instances with existing instances in the Amazon CloudWatch metrics that are used for scaling, resulting in more reliable usage data. For more information, see `Set the default instance warmup for an Auto Scaling group <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-default-instance-warmup.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . .. epigraph:: To manage various warm-up settings at the group level, we recommend that you set the default instance warmup, *even if it is set to 0 seconds* . To remove a value that you previously set, include the property but specify ``-1`` for the value. However, we strongly recommend keeping the default instance warmup enabled by specifying a value of ``0`` or other nominal value. Default: None
        :param desired_capacity: The desired capacity is the initial capacity of the Auto Scaling group at the time of its creation and the capacity it attempts to maintain. It can scale beyond this capacity if you configure automatic scaling. The number must be greater than or equal to the minimum size of the group and less than or equal to the maximum size of the group. If you do not specify a desired capacity when creating the stack, the default is the minimum size of the group. CloudFormation marks the Auto Scaling group as successful (by setting its status to CREATE_COMPLETE) when the desired capacity is reached. However, if a maximum Spot price is set in the launch template or launch configuration that you specified, then desired capacity is not used as a criteria for success. Whether your request is fulfilled depends on Spot Instance capacity and your maximum price.
        :param desired_capacity_type: The unit of measurement for the value specified for desired capacity. Amazon EC2 Auto Scaling supports ``DesiredCapacityType`` for attribute-based instance type selection only. For more information, see `Create a mixed instances group using attribute-based instance type selection <https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-mixed-instances-group-attribute-based-instance-type-selection.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . By default, Amazon EC2 Auto Scaling specifies ``units`` , which translates into number of instances. Valid values: ``units`` | ``vcpu`` | ``memory-mib``
        :param health_check_grace_period: The amount of time, in seconds, that Amazon EC2 Auto Scaling waits before checking the health status of an EC2 instance that has come into service and marking it unhealthy due to a failed health check. This is useful if your instances do not immediately pass their health checks after they enter the ``InService`` state. For more information, see `Set the health check grace period for an Auto Scaling group <https://docs.aws.amazon.com/autoscaling/ec2/userguide/health-check-grace-period.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . Default: ``0`` seconds
        :param health_check_type: A comma-separated value string of one or more health check types. The valid values are ``EC2`` , ``EBS`` , ``ELB`` , and ``VPC_LATTICE`` . ``EC2`` is the default health check and cannot be disabled. For more information, see `Health checks for instances in an Auto Scaling group <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-health-checks.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . Only specify ``EC2`` if you must clear a value that was previously set.
        :param instance_id: The ID of the instance used to base the launch configuration on. For more information, see `Create an Auto Scaling group using an EC2 instance <https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-asg-from-instance.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . If you specify ``LaunchTemplate`` , ``MixedInstancesPolicy`` , or ``LaunchConfigurationName`` , don't specify ``InstanceId`` .
        :param instance_maintenance_policy: An instance maintenance policy. For more information, see `Set instance maintenance policy <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-instance-maintenance-policy.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .
        :param launch_configuration_name: The name of the launch configuration to use to launch instances. Required only if you don't specify ``LaunchTemplate`` , ``MixedInstancesPolicy`` , or ``InstanceId`` .
        :param launch_template: Information used to specify the launch template and version to use to launch instances. You can alternatively associate a launch template to the Auto Scaling group by specifying a ``MixedInstancesPolicy`` . For more information about creating launch templates, see `Create a launch template for an Auto Scaling group <https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-launch-template.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . If you omit this property, you must specify ``MixedInstancesPolicy`` , ``LaunchConfigurationName`` , or ``InstanceId`` .
        :param lifecycle_hook_specification_list: One or more lifecycle hooks to add to the Auto Scaling group before instances are launched.
        :param load_balancer_names: A list of Classic Load Balancers associated with this Auto Scaling group. For Application Load Balancers, Network Load Balancers, and Gateway Load Balancers, specify the ``TargetGroupARNs`` property instead.
        :param max_instance_lifetime: The maximum amount of time, in seconds, that an instance can be in service. The default is null. If specified, the value must be either 0 or a number equal to or greater than 86,400 seconds (1 day). For more information, see `Replace Auto Scaling instances based on maximum instance lifetime <https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-max-instance-lifetime.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .
        :param max_size: The maximum size of the group. .. epigraph:: With a mixed instances policy that uses instance weighting, Amazon EC2 Auto Scaling may need to go above ``MaxSize`` to meet your capacity requirements. In this event, Amazon EC2 Auto Scaling will never go above ``MaxSize`` by more than your largest instance weight (weights that define how many units each instance contributes to the desired capacity of the group).
        :param metrics_collection: Enables the monitoring of group metrics of an Auto Scaling group. By default, these metrics are disabled.
        :param min_size: The minimum size of the group.
        :param mixed_instances_policy: An embedded object that specifies a mixed instances policy. The policy includes properties that not only define the distribution of On-Demand Instances and Spot Instances, the maximum price to pay for Spot Instances (optional), and how the Auto Scaling group allocates instance types to fulfill On-Demand and Spot capacities, but also the properties that specify the instance configuration information—the launch template and instance types. The policy can also include a weight for each instance type and different launch templates for individual instance types. For more information, see `Auto Scaling groups with multiple instance types and purchase options <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-mixed-instances-groups.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .
        :param new_instances_protected_from_scale_in: Indicates whether newly launched instances are protected from termination by Amazon EC2 Auto Scaling when scaling in. For more information about preventing instances from terminating on scale in, see `Use instance scale-in protection <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-instance-protection.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .
        :param notification_configuration: (deprecated) A structure that specifies an Amazon SNS notification configuration for the ``NotificationConfigurations`` property of the `AWS::AutoScaling::AutoScalingGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html>`_ resource. For an example template snippet, see `Configure Amazon EC2 Auto Scaling resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-ec2-auto-scaling.html>`_. For more information, see `Get Amazon SNS notifications when your Auto Scaling group scales <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ASGettingNotifications.html>`_ in the *Amazon EC2 Auto Scaling User Guide*.
        :param notification_configurations: Configures an Auto Scaling group to send notifications when specified events take place.
        :param placement_group: The name of the placement group into which to launch your instances. For more information, see `Placement groups <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html>`_ in the *Amazon EC2 User Guide* . .. epigraph:: A *cluster* placement group is a logical grouping of instances within a single Availability Zone. You cannot specify multiple Availability Zones and a cluster placement group.
        :param service_linked_role_arn: The Amazon Resource Name (ARN) of the service-linked role that the Auto Scaling group uses to call other AWS service on your behalf. By default, Amazon EC2 Auto Scaling uses a service-linked role named ``AWSServiceRoleForAutoScaling`` , which it creates if it does not exist. For more information, see `Service-linked roles <https://docs.aws.amazon.com/autoscaling/ec2/userguide/autoscaling-service-linked-role.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .
        :param skip_zonal_shift_validation: 
        :param tags: One or more tags. You can tag your Auto Scaling group and propagate the tags to the Amazon EC2 instances it launches. Tags are not propagated to Amazon EBS volumes. To add tags to Amazon EBS volumes, specify the tags in a launch template but use caution. If the launch template specifies an instance tag with a key that is also specified for the Auto Scaling group, Amazon EC2 Auto Scaling overrides the value of that instance tag with the value specified by the Auto Scaling group. For more information, see `Tag Auto Scaling groups and instances <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-tagging.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .
        :param target_group_arns: The Amazon Resource Names (ARN) of the Elastic Load Balancing target groups to associate with the Auto Scaling group. Instances are registered as targets with the target groups. The target groups receive incoming traffic and route requests to one or more registered targets. For more information, see `Use Elastic Load Balancing to distribute traffic across the instances in your Auto Scaling group <https://docs.aws.amazon.com/autoscaling/ec2/userguide/autoscaling-load-balancer.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .
        :param termination_policies: A policy or a list of policies that are used to select the instance to terminate. These policies are executed in the order that you list them. For more information, see `Configure termination policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-termination-policies.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . Valid values: ``Default`` | ``AllocationStrategy`` | ``ClosestToNextInstanceHour`` | ``NewestInstance`` | ``OldestInstance`` | ``OldestLaunchConfiguration`` | ``OldestLaunchTemplate`` | ``arn:aws:lambda:region:account-id:function:my-function:my-alias``
        :param traffic_sources: The traffic sources associated with this Auto Scaling group.
        :param vpc_zone_identifier: A list of subnet IDs for a virtual private cloud (VPC) where instances in the Auto Scaling group can be created. If this resource specifies public subnets and is also in a VPC that is defined in the same stack template, you must use the `DependsOn attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ to declare a dependency on the `VPC-gateway attachment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc-gateway-attachment.html>`_ . .. epigraph:: When you update ``VPCZoneIdentifier`` , this retains the same Auto Scaling group and replaces old instances with new ones, according to the specified subnets. You can optionally specify how CloudFormation handles these updates by using an `UpdatePolicy attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html>`_ . Required to launch instances into a nondefault VPC. If you specify ``VPCZoneIdentifier`` with ``AvailabilityZones`` , the subnets that you specify for this property must reside in those Availability Zones.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
            
            cfn_auto_scaling_group_mixin_props = autoscaling_mixins.CfnAutoScalingGroupMixinProps(
                auto_scaling_group_name="autoScalingGroupName",
                availability_zone_distribution=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.AvailabilityZoneDistributionProperty(
                    capacity_distribution_strategy="capacityDistributionStrategy"
                ),
                availability_zone_impairment_policy=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.AvailabilityZoneImpairmentPolicyProperty(
                    impaired_zone_health_check_behavior="impairedZoneHealthCheckBehavior",
                    zonal_shift_enabled=False
                ),
                availability_zones=["availabilityZones"],
                capacity_rebalance=False,
                capacity_reservation_specification=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.CapacityReservationSpecificationProperty(
                    capacity_reservation_preference="capacityReservationPreference",
                    capacity_reservation_target=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.CapacityReservationTargetProperty(
                        capacity_reservation_ids=["capacityReservationIds"],
                        capacity_reservation_resource_group_arns=["capacityReservationResourceGroupArns"]
                    )
                ),
                context="context",
                cooldown="cooldown",
                default_instance_warmup=123,
                desired_capacity="desiredCapacity",
                desired_capacity_type="desiredCapacityType",
                health_check_grace_period=123,
                health_check_type="healthCheckType",
                instance_id="instanceId",
                instance_maintenance_policy=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.InstanceMaintenancePolicyProperty(
                    max_healthy_percentage=123,
                    min_healthy_percentage=123
                ),
                launch_configuration_name="launchConfigurationName",
                launch_template=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty(
                    launch_template_id="launchTemplateId",
                    launch_template_name="launchTemplateName",
                    version="version"
                ),
                lifecycle_hook_specification_list=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LifecycleHookSpecificationProperty(
                    default_result="defaultResult",
                    heartbeat_timeout=123,
                    lifecycle_hook_name="lifecycleHookName",
                    lifecycle_transition="lifecycleTransition",
                    notification_metadata="notificationMetadata",
                    notification_target_arn="notificationTargetArn",
                    role_arn="roleArn"
                )],
                load_balancer_names=["loadBalancerNames"],
                max_instance_lifetime=123,
                max_size="maxSize",
                metrics_collection=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.MetricsCollectionProperty(
                    granularity="granularity",
                    metrics=["metrics"]
                )],
                min_size="minSize",
                mixed_instances_policy=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.MixedInstancesPolicyProperty(
                    instances_distribution=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.InstancesDistributionProperty(
                        on_demand_allocation_strategy="onDemandAllocationStrategy",
                        on_demand_base_capacity=123,
                        on_demand_percentage_above_base_capacity=123,
                        spot_allocation_strategy="spotAllocationStrategy",
                        spot_instance_pools=123,
                        spot_max_price="spotMaxPrice"
                    ),
                    launch_template=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateProperty(
                        launch_template_specification=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty(
                            launch_template_id="launchTemplateId",
                            launch_template_name="launchTemplateName",
                            version="version"
                        ),
                        overrides=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateOverridesProperty(
                            instance_requirements=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.InstanceRequirementsProperty(
                                accelerator_count=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.AcceleratorCountRequestProperty(
                                    max=123,
                                    min=123
                                ),
                                accelerator_manufacturers=["acceleratorManufacturers"],
                                accelerator_names=["acceleratorNames"],
                                accelerator_total_memory_mi_b=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.AcceleratorTotalMemoryMiBRequestProperty(
                                    max=123,
                                    min=123
                                ),
                                accelerator_types=["acceleratorTypes"],
                                allowed_instance_types=["allowedInstanceTypes"],
                                bare_metal="bareMetal",
                                baseline_ebs_bandwidth_mbps=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.BaselineEbsBandwidthMbpsRequestProperty(
                                    max=123,
                                    min=123
                                ),
                                baseline_performance_factors=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.BaselinePerformanceFactorsRequestProperty(
                                    cpu=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.CpuPerformanceFactorRequestProperty(
                                        references=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.PerformanceFactorReferenceRequestProperty(
                                            instance_family="instanceFamily"
                                        )]
                                    )
                                ),
                                burstable_performance="burstablePerformance",
                                cpu_manufacturers=["cpuManufacturers"],
                                excluded_instance_types=["excludedInstanceTypes"],
                                instance_generations=["instanceGenerations"],
                                local_storage="localStorage",
                                local_storage_types=["localStorageTypes"],
                                max_spot_price_as_percentage_of_optimal_on_demand_price=123,
                                memory_gi_bPer_vCpu=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.MemoryGiBPerVCpuRequestProperty(
                                    max=123,
                                    min=123
                                ),
                                memory_mi_b=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.MemoryMiBRequestProperty(
                                    max=123,
                                    min=123
                                ),
                                network_bandwidth_gbps=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.NetworkBandwidthGbpsRequestProperty(
                                    max=123,
                                    min=123
                                ),
                                network_interface_count=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.NetworkInterfaceCountRequestProperty(
                                    max=123,
                                    min=123
                                ),
                                on_demand_max_price_percentage_over_lowest_price=123,
                                require_hibernate_support=False,
                                spot_max_price_percentage_over_lowest_price=123,
                                total_local_storage_gb=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.TotalLocalStorageGBRequestProperty(
                                    max=123,
                                    min=123
                                ),
                                v_cpu_count=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.VCpuCountRequestProperty(
                                    max=123,
                                    min=123
                                )
                            ),
                            instance_type="instanceType",
                            launch_template_specification=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty(
                                launch_template_id="launchTemplateId",
                                launch_template_name="launchTemplateName",
                                version="version"
                            ),
                            weighted_capacity="weightedCapacity"
                        )]
                    )
                ),
                new_instances_protected_from_scale_in=False,
                notification_configuration=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.NotificationConfigurationProperty(
                    notification_types=["notificationTypes"],
                    topic_arn="topicArn"
                ),
                notification_configurations=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.NotificationConfigurationProperty(
                    notification_types=["notificationTypes"],
                    topic_arn="topicArn"
                )],
                placement_group="placementGroup",
                service_linked_role_arn="serviceLinkedRoleArn",
                skip_zonal_shift_validation=False,
                tags=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.TagPropertyProperty(
                    key="key",
                    propagate_at_launch=False,
                    value="value"
                )],
                target_group_arns=["targetGroupArns"],
                termination_policies=["terminationPolicies"],
                traffic_sources=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.TrafficSourceIdentifierProperty(
                    identifier="identifier",
                    type="type"
                )],
                vpc_zone_identifier=["vpcZoneIdentifier"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__263f37d5b93143ba12d509ca54fb68af5089157d7dd9cd494eea2e39db8b522c)
            check_type(argname="argument auto_scaling_group_name", value=auto_scaling_group_name, expected_type=type_hints["auto_scaling_group_name"])
            check_type(argname="argument availability_zone_distribution", value=availability_zone_distribution, expected_type=type_hints["availability_zone_distribution"])
            check_type(argname="argument availability_zone_impairment_policy", value=availability_zone_impairment_policy, expected_type=type_hints["availability_zone_impairment_policy"])
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument capacity_rebalance", value=capacity_rebalance, expected_type=type_hints["capacity_rebalance"])
            check_type(argname="argument capacity_reservation_specification", value=capacity_reservation_specification, expected_type=type_hints["capacity_reservation_specification"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument cooldown", value=cooldown, expected_type=type_hints["cooldown"])
            check_type(argname="argument default_instance_warmup", value=default_instance_warmup, expected_type=type_hints["default_instance_warmup"])
            check_type(argname="argument desired_capacity", value=desired_capacity, expected_type=type_hints["desired_capacity"])
            check_type(argname="argument desired_capacity_type", value=desired_capacity_type, expected_type=type_hints["desired_capacity_type"])
            check_type(argname="argument health_check_grace_period", value=health_check_grace_period, expected_type=type_hints["health_check_grace_period"])
            check_type(argname="argument health_check_type", value=health_check_type, expected_type=type_hints["health_check_type"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument instance_maintenance_policy", value=instance_maintenance_policy, expected_type=type_hints["instance_maintenance_policy"])
            check_type(argname="argument launch_configuration_name", value=launch_configuration_name, expected_type=type_hints["launch_configuration_name"])
            check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
            check_type(argname="argument lifecycle_hook_specification_list", value=lifecycle_hook_specification_list, expected_type=type_hints["lifecycle_hook_specification_list"])
            check_type(argname="argument load_balancer_names", value=load_balancer_names, expected_type=type_hints["load_balancer_names"])
            check_type(argname="argument max_instance_lifetime", value=max_instance_lifetime, expected_type=type_hints["max_instance_lifetime"])
            check_type(argname="argument max_size", value=max_size, expected_type=type_hints["max_size"])
            check_type(argname="argument metrics_collection", value=metrics_collection, expected_type=type_hints["metrics_collection"])
            check_type(argname="argument min_size", value=min_size, expected_type=type_hints["min_size"])
            check_type(argname="argument mixed_instances_policy", value=mixed_instances_policy, expected_type=type_hints["mixed_instances_policy"])
            check_type(argname="argument new_instances_protected_from_scale_in", value=new_instances_protected_from_scale_in, expected_type=type_hints["new_instances_protected_from_scale_in"])
            check_type(argname="argument notification_configuration", value=notification_configuration, expected_type=type_hints["notification_configuration"])
            check_type(argname="argument notification_configurations", value=notification_configurations, expected_type=type_hints["notification_configurations"])
            check_type(argname="argument placement_group", value=placement_group, expected_type=type_hints["placement_group"])
            check_type(argname="argument service_linked_role_arn", value=service_linked_role_arn, expected_type=type_hints["service_linked_role_arn"])
            check_type(argname="argument skip_zonal_shift_validation", value=skip_zonal_shift_validation, expected_type=type_hints["skip_zonal_shift_validation"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_group_arns", value=target_group_arns, expected_type=type_hints["target_group_arns"])
            check_type(argname="argument termination_policies", value=termination_policies, expected_type=type_hints["termination_policies"])
            check_type(argname="argument traffic_sources", value=traffic_sources, expected_type=type_hints["traffic_sources"])
            check_type(argname="argument vpc_zone_identifier", value=vpc_zone_identifier, expected_type=type_hints["vpc_zone_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_scaling_group_name is not None:
            self._values["auto_scaling_group_name"] = auto_scaling_group_name
        if availability_zone_distribution is not None:
            self._values["availability_zone_distribution"] = availability_zone_distribution
        if availability_zone_impairment_policy is not None:
            self._values["availability_zone_impairment_policy"] = availability_zone_impairment_policy
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if capacity_rebalance is not None:
            self._values["capacity_rebalance"] = capacity_rebalance
        if capacity_reservation_specification is not None:
            self._values["capacity_reservation_specification"] = capacity_reservation_specification
        if context is not None:
            self._values["context"] = context
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if default_instance_warmup is not None:
            self._values["default_instance_warmup"] = default_instance_warmup
        if desired_capacity is not None:
            self._values["desired_capacity"] = desired_capacity
        if desired_capacity_type is not None:
            self._values["desired_capacity_type"] = desired_capacity_type
        if health_check_grace_period is not None:
            self._values["health_check_grace_period"] = health_check_grace_period
        if health_check_type is not None:
            self._values["health_check_type"] = health_check_type
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if instance_maintenance_policy is not None:
            self._values["instance_maintenance_policy"] = instance_maintenance_policy
        if launch_configuration_name is not None:
            self._values["launch_configuration_name"] = launch_configuration_name
        if launch_template is not None:
            self._values["launch_template"] = launch_template
        if lifecycle_hook_specification_list is not None:
            self._values["lifecycle_hook_specification_list"] = lifecycle_hook_specification_list
        if load_balancer_names is not None:
            self._values["load_balancer_names"] = load_balancer_names
        if max_instance_lifetime is not None:
            self._values["max_instance_lifetime"] = max_instance_lifetime
        if max_size is not None:
            self._values["max_size"] = max_size
        if metrics_collection is not None:
            self._values["metrics_collection"] = metrics_collection
        if min_size is not None:
            self._values["min_size"] = min_size
        if mixed_instances_policy is not None:
            self._values["mixed_instances_policy"] = mixed_instances_policy
        if new_instances_protected_from_scale_in is not None:
            self._values["new_instances_protected_from_scale_in"] = new_instances_protected_from_scale_in
        if notification_configuration is not None:
            self._values["notification_configuration"] = notification_configuration
        if notification_configurations is not None:
            self._values["notification_configurations"] = notification_configurations
        if placement_group is not None:
            self._values["placement_group"] = placement_group
        if service_linked_role_arn is not None:
            self._values["service_linked_role_arn"] = service_linked_role_arn
        if skip_zonal_shift_validation is not None:
            self._values["skip_zonal_shift_validation"] = skip_zonal_shift_validation
        if tags is not None:
            self._values["tags"] = tags
        if target_group_arns is not None:
            self._values["target_group_arns"] = target_group_arns
        if termination_policies is not None:
            self._values["termination_policies"] = termination_policies
        if traffic_sources is not None:
            self._values["traffic_sources"] = traffic_sources
        if vpc_zone_identifier is not None:
            self._values["vpc_zone_identifier"] = vpc_zone_identifier

    @builtins.property
    def auto_scaling_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Auto Scaling group. This name must be unique per Region per account.

        The name can contain any ASCII character 33 to 126 including most punctuation characters, digits, and upper and lowercased letters.
        .. epigraph::

           You cannot use a colon (:) in the name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-autoscalinggroupname
        '''
        result = self._values.get("auto_scaling_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def availability_zone_distribution(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.AvailabilityZoneDistributionProperty"]]:
        '''The instance capacity distribution across Availability Zones.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-availabilityzonedistribution
        '''
        result = self._values.get("availability_zone_distribution")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.AvailabilityZoneDistributionProperty"]], result)

    @builtins.property
    def availability_zone_impairment_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.AvailabilityZoneImpairmentPolicyProperty"]]:
        '''The Availability Zone impairment policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-availabilityzoneimpairmentpolicy
        '''
        result = self._values.get("availability_zone_impairment_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.AvailabilityZoneImpairmentPolicyProperty"]], result)

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Availability Zones where instances in the Auto Scaling group can be created.

        Used for launching into the default VPC subnet in each Availability Zone when not using the ``VPCZoneIdentifier`` property, or for attaching a network interface when an existing network interface ID is specified in a launch template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-availabilityzones
        '''
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def capacity_rebalance(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether Capacity Rebalancing is enabled.

        Otherwise, Capacity Rebalancing is disabled. When you turn on Capacity Rebalancing, Amazon EC2 Auto Scaling attempts to launch a Spot Instance whenever Amazon EC2 notifies that a Spot Instance is at an elevated risk of interruption. After launching a new instance, it then terminates an old instance. For more information, see `Use Capacity Rebalancing to handle Amazon EC2 Spot Interruptions <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-capacity-rebalancing.html>`_ in the in the *Amazon EC2 Auto Scaling User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-capacityrebalance
        '''
        result = self._values.get("capacity_rebalance")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def capacity_reservation_specification(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.CapacityReservationSpecificationProperty"]]:
        '''The capacity reservation specification.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-capacityreservationspecification
        '''
        result = self._values.get("capacity_reservation_specification")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.CapacityReservationSpecificationProperty"]], result)

    @builtins.property
    def context(self) -> typing.Optional[builtins.str]:
        '''Reserved.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-context
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cooldown(self) -> typing.Optional[builtins.str]:
        '''*Only needed if you use simple scaling policies.*.

        The amount of time, in seconds, between one scaling activity ending and another one starting due to simple scaling policies. For more information, see `Scaling cooldowns for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-scaling-cooldowns.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        Default: ``300`` seconds

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-cooldown
        '''
        result = self._values.get("cooldown")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_instance_warmup(self) -> typing.Optional[jsii.Number]:
        '''The amount of time, in seconds, until a new instance is considered to have finished initializing and resource consumption to become stable after it enters the ``InService`` state.

        During an instance refresh, Amazon EC2 Auto Scaling waits for the warm-up period after it replaces an instance before it moves on to replacing the next instance. Amazon EC2 Auto Scaling also waits for the warm-up period before aggregating the metrics for new instances with existing instances in the Amazon CloudWatch metrics that are used for scaling, resulting in more reliable usage data. For more information, see `Set the default instance warmup for an Auto Scaling group <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-default-instance-warmup.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .
        .. epigraph::

           To manage various warm-up settings at the group level, we recommend that you set the default instance warmup, *even if it is set to 0 seconds* . To remove a value that you previously set, include the property but specify ``-1`` for the value. However, we strongly recommend keeping the default instance warmup enabled by specifying a value of ``0`` or other nominal value.

        Default: None

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-defaultinstancewarmup
        '''
        result = self._values.get("default_instance_warmup")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def desired_capacity(self) -> typing.Optional[builtins.str]:
        '''The desired capacity is the initial capacity of the Auto Scaling group at the time of its creation and the capacity it attempts to maintain.

        It can scale beyond this capacity if you configure automatic scaling.

        The number must be greater than or equal to the minimum size of the group and less than or equal to the maximum size of the group. If you do not specify a desired capacity when creating the stack, the default is the minimum size of the group.

        CloudFormation marks the Auto Scaling group as successful (by setting its status to CREATE_COMPLETE) when the desired capacity is reached. However, if a maximum Spot price is set in the launch template or launch configuration that you specified, then desired capacity is not used as a criteria for success. Whether your request is fulfilled depends on Spot Instance capacity and your maximum price.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-desiredcapacity
        '''
        result = self._values.get("desired_capacity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def desired_capacity_type(self) -> typing.Optional[builtins.str]:
        '''The unit of measurement for the value specified for desired capacity.

        Amazon EC2 Auto Scaling supports ``DesiredCapacityType`` for attribute-based instance type selection only. For more information, see `Create a mixed instances group using attribute-based instance type selection <https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-mixed-instances-group-attribute-based-instance-type-selection.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        By default, Amazon EC2 Auto Scaling specifies ``units`` , which translates into number of instances.

        Valid values: ``units`` | ``vcpu`` | ``memory-mib``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-desiredcapacitytype
        '''
        result = self._values.get("desired_capacity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[jsii.Number]:
        '''The amount of time, in seconds, that Amazon EC2 Auto Scaling waits before checking the health status of an EC2 instance that has come into service and marking it unhealthy due to a failed health check.

        This is useful if your instances do not immediately pass their health checks after they enter the ``InService`` state. For more information, see `Set the health check grace period for an Auto Scaling group <https://docs.aws.amazon.com/autoscaling/ec2/userguide/health-check-grace-period.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        Default: ``0`` seconds

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-healthcheckgraceperiod
        '''
        result = self._values.get("health_check_grace_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_type(self) -> typing.Optional[builtins.str]:
        '''A comma-separated value string of one or more health check types.

        The valid values are ``EC2`` , ``EBS`` , ``ELB`` , and ``VPC_LATTICE`` . ``EC2`` is the default health check and cannot be disabled. For more information, see `Health checks for instances in an Auto Scaling group <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-health-checks.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        Only specify ``EC2`` if you must clear a value that was previously set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-healthchecktype
        '''
        result = self._values.get("health_check_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the instance used to base the launch configuration on.

        For more information, see `Create an Auto Scaling group using an EC2 instance <https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-asg-from-instance.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        If you specify ``LaunchTemplate`` , ``MixedInstancesPolicy`` , or ``LaunchConfigurationName`` , don't specify ``InstanceId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-instanceid
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_maintenance_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.InstanceMaintenancePolicyProperty"]]:
        '''An instance maintenance policy.

        For more information, see `Set instance maintenance policy <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-instance-maintenance-policy.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-instancemaintenancepolicy
        '''
        result = self._values.get("instance_maintenance_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.InstanceMaintenancePolicyProperty"]], result)

    @builtins.property
    def launch_configuration_name(self) -> typing.Optional[builtins.str]:
        '''The name of the launch configuration to use to launch instances.

        Required only if you don't specify ``LaunchTemplate`` , ``MixedInstancesPolicy`` , or ``InstanceId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-launchconfigurationname
        '''
        result = self._values.get("launch_configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def launch_template(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty"]]:
        '''Information used to specify the launch template and version to use to launch instances.

        You can alternatively associate a launch template to the Auto Scaling group by specifying a ``MixedInstancesPolicy`` . For more information about creating launch templates, see `Create a launch template for an Auto Scaling group <https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-launch-template.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        If you omit this property, you must specify ``MixedInstancesPolicy`` , ``LaunchConfigurationName`` , or ``InstanceId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-launchtemplate
        '''
        result = self._values.get("launch_template")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty"]], result)

    @builtins.property
    def lifecycle_hook_specification_list(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.LifecycleHookSpecificationProperty"]]]]:
        '''One or more lifecycle hooks to add to the Auto Scaling group before instances are launched.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecificationlist
        '''
        result = self._values.get("lifecycle_hook_specification_list")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.LifecycleHookSpecificationProperty"]]]], result)

    @builtins.property
    def load_balancer_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Classic Load Balancers associated with this Auto Scaling group.

        For Application Load Balancers, Network Load Balancers, and Gateway Load Balancers, specify the ``TargetGroupARNs`` property instead.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-loadbalancernames
        '''
        result = self._values.get("load_balancer_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_instance_lifetime(self) -> typing.Optional[jsii.Number]:
        '''The maximum amount of time, in seconds, that an instance can be in service.

        The default is null. If specified, the value must be either 0 or a number equal to or greater than 86,400 seconds (1 day). For more information, see `Replace Auto Scaling instances based on maximum instance lifetime <https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-max-instance-lifetime.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-maxinstancelifetime
        '''
        result = self._values.get("max_instance_lifetime")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_size(self) -> typing.Optional[builtins.str]:
        '''The maximum size of the group.

        .. epigraph::

           With a mixed instances policy that uses instance weighting, Amazon EC2 Auto Scaling may need to go above ``MaxSize`` to meet your capacity requirements. In this event, Amazon EC2 Auto Scaling will never go above ``MaxSize`` by more than your largest instance weight (weights that define how many units each instance contributes to the desired capacity of the group).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-maxsize
        '''
        result = self._values.get("max_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metrics_collection(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.MetricsCollectionProperty"]]]]:
        '''Enables the monitoring of group metrics of an Auto Scaling group.

        By default, these metrics are disabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-metricscollection
        '''
        result = self._values.get("metrics_collection")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.MetricsCollectionProperty"]]]], result)

    @builtins.property
    def min_size(self) -> typing.Optional[builtins.str]:
        '''The minimum size of the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-minsize
        '''
        result = self._values.get("min_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mixed_instances_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.MixedInstancesPolicyProperty"]]:
        '''An embedded object that specifies a mixed instances policy.

        The policy includes properties that not only define the distribution of On-Demand Instances and Spot Instances, the maximum price to pay for Spot Instances (optional), and how the Auto Scaling group allocates instance types to fulfill On-Demand and Spot capacities, but also the properties that specify the instance configuration information—the launch template and instance types. The policy can also include a weight for each instance type and different launch templates for individual instance types.

        For more information, see `Auto Scaling groups with multiple instance types and purchase options <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-mixed-instances-groups.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-mixedinstancespolicy
        '''
        result = self._values.get("mixed_instances_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.MixedInstancesPolicyProperty"]], result)

    @builtins.property
    def new_instances_protected_from_scale_in(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether newly launched instances are protected from termination by Amazon EC2 Auto Scaling when scaling in.

        For more information about preventing instances from terminating on scale in, see `Use instance scale-in protection <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-instance-protection.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-newinstancesprotectedfromscalein
        '''
        result = self._values.get("new_instances_protected_from_scale_in")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def notification_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.NotificationConfigurationProperty"]]:
        '''(deprecated) A structure that specifies an Amazon SNS notification configuration for the ``NotificationConfigurations`` property of the `AWS::AutoScaling::AutoScalingGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html>`_ resource.  For an example template snippet, see `Configure Amazon EC2 Auto Scaling resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-ec2-auto-scaling.html>`_.  For more information, see `Get Amazon SNS notifications when your Auto Scaling group scales <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ASGettingNotifications.html>`_ in the *Amazon EC2 Auto Scaling User Guide*.

        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-notificationconfiguration
        :stability: deprecated
        '''
        result = self._values.get("notification_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.NotificationConfigurationProperty"]], result)

    @builtins.property
    def notification_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.NotificationConfigurationProperty"]]]]:
        '''Configures an Auto Scaling group to send notifications when specified events take place.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-notificationconfigurations
        '''
        result = self._values.get("notification_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.NotificationConfigurationProperty"]]]], result)

    @builtins.property
    def placement_group(self) -> typing.Optional[builtins.str]:
        '''The name of the placement group into which to launch your instances.

        For more information, see `Placement groups <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html>`_ in the *Amazon EC2 User Guide* .
        .. epigraph::

           A *cluster* placement group is a logical grouping of instances within a single Availability Zone. You cannot specify multiple Availability Zones and a cluster placement group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-placementgroup
        '''
        result = self._values.get("placement_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_linked_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the service-linked role that the Auto Scaling group uses to call other AWS service on your behalf.

        By default, Amazon EC2 Auto Scaling uses a service-linked role named ``AWSServiceRoleForAutoScaling`` , which it creates if it does not exist. For more information, see `Service-linked roles <https://docs.aws.amazon.com/autoscaling/ec2/userguide/autoscaling-service-linked-role.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-servicelinkedrolearn
        '''
        result = self._values.get("service_linked_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_zonal_shift_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-skipzonalshiftvalidation
        '''
        result = self._values.get("skip_zonal_shift_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnAutoScalingGroupPropsMixin.TagPropertyProperty"]]:
        '''One or more tags.

        You can tag your Auto Scaling group and propagate the tags to the Amazon EC2 instances it launches. Tags are not propagated to Amazon EBS volumes. To add tags to Amazon EBS volumes, specify the tags in a launch template but use caution. If the launch template specifies an instance tag with a key that is also specified for the Auto Scaling group, Amazon EC2 Auto Scaling overrides the value of that instance tag with the value specified by the Auto Scaling group. For more information, see `Tag Auto Scaling groups and instances <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-tagging.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnAutoScalingGroupPropsMixin.TagPropertyProperty"]], result)

    @builtins.property
    def target_group_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Names (ARN) of the Elastic Load Balancing target groups to associate with the Auto Scaling group.

        Instances are registered as targets with the target groups. The target groups receive incoming traffic and route requests to one or more registered targets. For more information, see `Use Elastic Load Balancing to distribute traffic across the instances in your Auto Scaling group <https://docs.aws.amazon.com/autoscaling/ec2/userguide/autoscaling-load-balancer.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-targetgrouparns
        '''
        result = self._values.get("target_group_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def termination_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A policy or a list of policies that are used to select the instance to terminate.

        These policies are executed in the order that you list them. For more information, see `Configure termination policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-termination-policies.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        Valid values: ``Default`` | ``AllocationStrategy`` | ``ClosestToNextInstanceHour`` | ``NewestInstance`` | ``OldestInstance`` | ``OldestLaunchConfiguration`` | ``OldestLaunchTemplate`` | ``arn:aws:lambda:region:account-id:function:my-function:my-alias``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-terminationpolicies
        '''
        result = self._values.get("termination_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def traffic_sources(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.TrafficSourceIdentifierProperty"]]]]:
        '''The traffic sources associated with this Auto Scaling group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-trafficsources
        '''
        result = self._values.get("traffic_sources")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.TrafficSourceIdentifierProperty"]]]], result)

    @builtins.property
    def vpc_zone_identifier(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of subnet IDs for a virtual private cloud (VPC) where instances in the Auto Scaling group can be created.

        If this resource specifies public subnets and is also in a VPC that is defined in the same stack template, you must use the `DependsOn attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ to declare a dependency on the `VPC-gateway attachment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc-gateway-attachment.html>`_ .
        .. epigraph::

           When you update ``VPCZoneIdentifier`` , this retains the same Auto Scaling group and replaces old instances with new ones, according to the specified subnets. You can optionally specify how CloudFormation handles these updates by using an `UpdatePolicy attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html>`_ .

        Required to launch instances into a nondefault VPC. If you specify ``VPCZoneIdentifier`` with ``AvailabilityZones`` , the subnets that you specify for this property must reside in those Availability Zones.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#cfn-autoscaling-autoscalinggroup-vpczoneidentifier
        '''
        result = self._values.get("vpc_zone_identifier")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAutoScalingGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAutoScalingGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin",
):
    '''The ``AWS::AutoScaling::AutoScalingGroup`` resource defines an Amazon EC2 Auto Scaling group, which is a collection of Amazon EC2 instances that are treated as a logical grouping for the purposes of automatic scaling and management.

    For more information about Amazon EC2 Auto Scaling, see the `Amazon EC2 Auto Scaling User Guide <https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html>`_ .
    .. epigraph::

       Amazon EC2 Auto Scaling configures instances launched as part of an Auto Scaling group using either a `launch template <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-launchtemplate.html>`_ or a launch configuration. We strongly recommend that you do not use launch configurations. For more information, see `Launch configurations <https://docs.aws.amazon.com/autoscaling/ec2/userguide/launch-configurations.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

       For help migrating from launch configurations to launch templates, see `Migrate AWS CloudFormation stacks from launch configurations to launch templates <https://docs.aws.amazon.com/autoscaling/ec2/userguide/migrate-launch-configurations-with-cloudformation.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html
    :cloudformationResource: AWS::AutoScaling::AutoScalingGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
        
        cfn_auto_scaling_group_props_mixin = autoscaling_mixins.CfnAutoScalingGroupPropsMixin(autoscaling_mixins.CfnAutoScalingGroupMixinProps(
            auto_scaling_group_name="autoScalingGroupName",
            availability_zone_distribution=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.AvailabilityZoneDistributionProperty(
                capacity_distribution_strategy="capacityDistributionStrategy"
            ),
            availability_zone_impairment_policy=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.AvailabilityZoneImpairmentPolicyProperty(
                impaired_zone_health_check_behavior="impairedZoneHealthCheckBehavior",
                zonal_shift_enabled=False
            ),
            availability_zones=["availabilityZones"],
            capacity_rebalance=False,
            capacity_reservation_specification=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.CapacityReservationSpecificationProperty(
                capacity_reservation_preference="capacityReservationPreference",
                capacity_reservation_target=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.CapacityReservationTargetProperty(
                    capacity_reservation_ids=["capacityReservationIds"],
                    capacity_reservation_resource_group_arns=["capacityReservationResourceGroupArns"]
                )
            ),
            context="context",
            cooldown="cooldown",
            default_instance_warmup=123,
            desired_capacity="desiredCapacity",
            desired_capacity_type="desiredCapacityType",
            health_check_grace_period=123,
            health_check_type="healthCheckType",
            instance_id="instanceId",
            instance_maintenance_policy=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.InstanceMaintenancePolicyProperty(
                max_healthy_percentage=123,
                min_healthy_percentage=123
            ),
            launch_configuration_name="launchConfigurationName",
            launch_template=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty(
                launch_template_id="launchTemplateId",
                launch_template_name="launchTemplateName",
                version="version"
            ),
            lifecycle_hook_specification_list=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LifecycleHookSpecificationProperty(
                default_result="defaultResult",
                heartbeat_timeout=123,
                lifecycle_hook_name="lifecycleHookName",
                lifecycle_transition="lifecycleTransition",
                notification_metadata="notificationMetadata",
                notification_target_arn="notificationTargetArn",
                role_arn="roleArn"
            )],
            load_balancer_names=["loadBalancerNames"],
            max_instance_lifetime=123,
            max_size="maxSize",
            metrics_collection=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.MetricsCollectionProperty(
                granularity="granularity",
                metrics=["metrics"]
            )],
            min_size="minSize",
            mixed_instances_policy=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.MixedInstancesPolicyProperty(
                instances_distribution=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.InstancesDistributionProperty(
                    on_demand_allocation_strategy="onDemandAllocationStrategy",
                    on_demand_base_capacity=123,
                    on_demand_percentage_above_base_capacity=123,
                    spot_allocation_strategy="spotAllocationStrategy",
                    spot_instance_pools=123,
                    spot_max_price="spotMaxPrice"
                ),
                launch_template=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateProperty(
                    launch_template_specification=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty(
                        launch_template_id="launchTemplateId",
                        launch_template_name="launchTemplateName",
                        version="version"
                    ),
                    overrides=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateOverridesProperty(
                        instance_requirements=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.InstanceRequirementsProperty(
                            accelerator_count=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.AcceleratorCountRequestProperty(
                                max=123,
                                min=123
                            ),
                            accelerator_manufacturers=["acceleratorManufacturers"],
                            accelerator_names=["acceleratorNames"],
                            accelerator_total_memory_mi_b=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.AcceleratorTotalMemoryMiBRequestProperty(
                                max=123,
                                min=123
                            ),
                            accelerator_types=["acceleratorTypes"],
                            allowed_instance_types=["allowedInstanceTypes"],
                            bare_metal="bareMetal",
                            baseline_ebs_bandwidth_mbps=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.BaselineEbsBandwidthMbpsRequestProperty(
                                max=123,
                                min=123
                            ),
                            baseline_performance_factors=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.BaselinePerformanceFactorsRequestProperty(
                                cpu=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.CpuPerformanceFactorRequestProperty(
                                    references=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.PerformanceFactorReferenceRequestProperty(
                                        instance_family="instanceFamily"
                                    )]
                                )
                            ),
                            burstable_performance="burstablePerformance",
                            cpu_manufacturers=["cpuManufacturers"],
                            excluded_instance_types=["excludedInstanceTypes"],
                            instance_generations=["instanceGenerations"],
                            local_storage="localStorage",
                            local_storage_types=["localStorageTypes"],
                            max_spot_price_as_percentage_of_optimal_on_demand_price=123,
                            memory_gi_bPer_vCpu=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.MemoryGiBPerVCpuRequestProperty(
                                max=123,
                                min=123
                            ),
                            memory_mi_b=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.MemoryMiBRequestProperty(
                                max=123,
                                min=123
                            ),
                            network_bandwidth_gbps=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.NetworkBandwidthGbpsRequestProperty(
                                max=123,
                                min=123
                            ),
                            network_interface_count=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.NetworkInterfaceCountRequestProperty(
                                max=123,
                                min=123
                            ),
                            on_demand_max_price_percentage_over_lowest_price=123,
                            require_hibernate_support=False,
                            spot_max_price_percentage_over_lowest_price=123,
                            total_local_storage_gb=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.TotalLocalStorageGBRequestProperty(
                                max=123,
                                min=123
                            ),
                            v_cpu_count=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.VCpuCountRequestProperty(
                                max=123,
                                min=123
                            )
                        ),
                        instance_type="instanceType",
                        launch_template_specification=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty(
                            launch_template_id="launchTemplateId",
                            launch_template_name="launchTemplateName",
                            version="version"
                        ),
                        weighted_capacity="weightedCapacity"
                    )]
                )
            ),
            new_instances_protected_from_scale_in=False,
            notification_configuration=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.NotificationConfigurationProperty(
                notification_types=["notificationTypes"],
                topic_arn="topicArn"
            ),
            notification_configurations=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.NotificationConfigurationProperty(
                notification_types=["notificationTypes"],
                topic_arn="topicArn"
            )],
            placement_group="placementGroup",
            service_linked_role_arn="serviceLinkedRoleArn",
            skip_zonal_shift_validation=False,
            tags=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.TagPropertyProperty(
                key="key",
                propagate_at_launch=False,
                value="value"
            )],
            target_group_arns=["targetGroupArns"],
            termination_policies=["terminationPolicies"],
            traffic_sources=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.TrafficSourceIdentifierProperty(
                identifier="identifier",
                type="type"
            )],
            vpc_zone_identifier=["vpcZoneIdentifier"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAutoScalingGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AutoScaling::AutoScalingGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__112ae175d73915392830869d82f09263102006c659d735c41ef5d7c0fbc7b135)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        options = _CfnPropertyMixinOptions_9cbff649(strategy=strategy)

        jsii.create(self.__class__, self, [props, options])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply the mixin properties to the construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f163fe4a672c71d5938e040e13052303459f5bd3fd5bc334834efcd0ea4a2fe8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d9440e844b7d7fefdd405d2533777a4d84411cb6c17495393f7519db2170f7b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAutoScalingGroupMixinProps:
        return typing.cast(CfnAutoScalingGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.AcceleratorCountRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"max": "max", "min": "min"},
    )
    class AcceleratorCountRequestProperty:
        def __init__(
            self,
            *,
            max: typing.Optional[jsii.Number] = None,
            min: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``AcceleratorCountRequest`` is a property of the ``InstanceRequirements`` property of the `AWS::AutoScaling::AutoScalingGroup LaunchTemplateOverrides <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplateoverrides.html>`_ property type that describes the minimum and maximum number of accelerators for an instance type.

            :param max: The maximum value.
            :param min: The minimum value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-acceleratorcountrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                accelerator_count_request_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.AcceleratorCountRequestProperty(
                    max=123,
                    min=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__54ebde666f10b627fbe322c9fb13ff136d93d3be4d7f807c388f74f82ab008b3)
                check_type(argname="argument max", value=max, expected_type=type_hints["max"])
                check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max is not None:
                self._values["max"] = max
            if min is not None:
                self._values["min"] = min

        @builtins.property
        def max(self) -> typing.Optional[jsii.Number]:
            '''The maximum value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-acceleratorcountrequest.html#cfn-autoscaling-autoscalinggroup-acceleratorcountrequest-max
            '''
            result = self._values.get("max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min(self) -> typing.Optional[jsii.Number]:
            '''The minimum value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-acceleratorcountrequest.html#cfn-autoscaling-autoscalinggroup-acceleratorcountrequest-min
            '''
            result = self._values.get("min")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AcceleratorCountRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.AcceleratorTotalMemoryMiBRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"max": "max", "min": "min"},
    )
    class AcceleratorTotalMemoryMiBRequestProperty:
        def __init__(
            self,
            *,
            max: typing.Optional[jsii.Number] = None,
            min: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``AcceleratorTotalMemoryMiBRequest`` is a property of the ``InstanceRequirements`` property of the `AWS::AutoScaling::AutoScalingGroup LaunchTemplateOverrides <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplateoverrides.html>`_ property type that describes the minimum and maximum total memory size for the accelerators for an instance type, in MiB.

            :param max: The memory maximum in MiB.
            :param min: The memory minimum in MiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-acceleratortotalmemorymibrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                accelerator_total_memory_mi_bRequest_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.AcceleratorTotalMemoryMiBRequestProperty(
                    max=123,
                    min=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f1de934747c7d6e959c704e34fd5e2de8e1c05d0f7dfdbc8e22c5c6481f9db37)
                check_type(argname="argument max", value=max, expected_type=type_hints["max"])
                check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max is not None:
                self._values["max"] = max
            if min is not None:
                self._values["min"] = min

        @builtins.property
        def max(self) -> typing.Optional[jsii.Number]:
            '''The memory maximum in MiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-acceleratortotalmemorymibrequest.html#cfn-autoscaling-autoscalinggroup-acceleratortotalmemorymibrequest-max
            '''
            result = self._values.get("max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min(self) -> typing.Optional[jsii.Number]:
            '''The memory minimum in MiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-acceleratortotalmemorymibrequest.html#cfn-autoscaling-autoscalinggroup-acceleratortotalmemorymibrequest-min
            '''
            result = self._values.get("min")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AcceleratorTotalMemoryMiBRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.AvailabilityZoneDistributionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capacity_distribution_strategy": "capacityDistributionStrategy",
        },
    )
    class AvailabilityZoneDistributionProperty:
        def __init__(
            self,
            *,
            capacity_distribution_strategy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``AvailabilityZoneDistribution`` is a property of the `AWS::AutoScaling::AutoScalingGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html>`_ resource.

            :param capacity_distribution_strategy: If launches fail in an Availability Zone, the following strategies are available. The default is ``balanced-best-effort`` . - ``balanced-only`` - If launches fail in an Availability Zone, Auto Scaling will continue to attempt to launch in the unhealthy zone to preserve a balanced distribution. - ``balanced-best-effort`` - If launches fail in an Availability Zone, Auto Scaling will attempt to launch in another healthy Availability Zone instead.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-availabilityzonedistribution.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                availability_zone_distribution_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.AvailabilityZoneDistributionProperty(
                    capacity_distribution_strategy="capacityDistributionStrategy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__561e51301a99db50db25aa514ed54308c62de8aa0a44d6446b703a0465c6c4d0)
                check_type(argname="argument capacity_distribution_strategy", value=capacity_distribution_strategy, expected_type=type_hints["capacity_distribution_strategy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capacity_distribution_strategy is not None:
                self._values["capacity_distribution_strategy"] = capacity_distribution_strategy

        @builtins.property
        def capacity_distribution_strategy(self) -> typing.Optional[builtins.str]:
            '''If launches fail in an Availability Zone, the following strategies are available. The default is ``balanced-best-effort`` .

            - ``balanced-only`` - If launches fail in an Availability Zone, Auto Scaling will continue to attempt to launch in the unhealthy zone to preserve a balanced distribution.
            - ``balanced-best-effort`` - If launches fail in an Availability Zone, Auto Scaling will attempt to launch in another healthy Availability Zone instead.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-availabilityzonedistribution.html#cfn-autoscaling-autoscalinggroup-availabilityzonedistribution-capacitydistributionstrategy
            '''
            result = self._values.get("capacity_distribution_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AvailabilityZoneDistributionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.AvailabilityZoneImpairmentPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "impaired_zone_health_check_behavior": "impairedZoneHealthCheckBehavior",
            "zonal_shift_enabled": "zonalShiftEnabled",
        },
    )
    class AvailabilityZoneImpairmentPolicyProperty:
        def __init__(
            self,
            *,
            impaired_zone_health_check_behavior: typing.Optional[builtins.str] = None,
            zonal_shift_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Describes an Availability Zone impairment policy.

            :param impaired_zone_health_check_behavior: Specifies the health check behavior for the impaired Availability Zone in an active zonal shift. If you select ``Replace unhealthy`` , instances that appear unhealthy will be replaced in all Availability Zones. If you select ``Ignore unhealthy`` , instances will not be replaced in the Availability Zone with the active zonal shift. For more information, see `Auto Scaling group zonal shift <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-zonal-shift.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .
            :param zonal_shift_enabled: If ``true`` , enable zonal shift for your Auto Scaling group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-availabilityzoneimpairmentpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                availability_zone_impairment_policy_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.AvailabilityZoneImpairmentPolicyProperty(
                    impaired_zone_health_check_behavior="impairedZoneHealthCheckBehavior",
                    zonal_shift_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3e388abc303ec0216355bae8268a80a4d0bd1d9d9a42c9641199ea2bde0db517)
                check_type(argname="argument impaired_zone_health_check_behavior", value=impaired_zone_health_check_behavior, expected_type=type_hints["impaired_zone_health_check_behavior"])
                check_type(argname="argument zonal_shift_enabled", value=zonal_shift_enabled, expected_type=type_hints["zonal_shift_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if impaired_zone_health_check_behavior is not None:
                self._values["impaired_zone_health_check_behavior"] = impaired_zone_health_check_behavior
            if zonal_shift_enabled is not None:
                self._values["zonal_shift_enabled"] = zonal_shift_enabled

        @builtins.property
        def impaired_zone_health_check_behavior(self) -> typing.Optional[builtins.str]:
            '''Specifies the health check behavior for the impaired Availability Zone in an active zonal shift.

            If you select ``Replace unhealthy`` , instances that appear unhealthy will be replaced in all Availability Zones. If you select ``Ignore unhealthy`` , instances will not be replaced in the Availability Zone with the active zonal shift. For more information, see `Auto Scaling group zonal shift <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-zonal-shift.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-availabilityzoneimpairmentpolicy.html#cfn-autoscaling-autoscalinggroup-availabilityzoneimpairmentpolicy-impairedzonehealthcheckbehavior
            '''
            result = self._values.get("impaired_zone_health_check_behavior")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def zonal_shift_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If ``true`` , enable zonal shift for your Auto Scaling group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-availabilityzoneimpairmentpolicy.html#cfn-autoscaling-autoscalinggroup-availabilityzoneimpairmentpolicy-zonalshiftenabled
            '''
            result = self._values.get("zonal_shift_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AvailabilityZoneImpairmentPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.BaselineEbsBandwidthMbpsRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"max": "max", "min": "min"},
    )
    class BaselineEbsBandwidthMbpsRequestProperty:
        def __init__(
            self,
            *,
            max: typing.Optional[jsii.Number] = None,
            min: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``BaselineEbsBandwidthMbpsRequest`` is a property of the ``InstanceRequirements`` property of the `AWS::AutoScaling::AutoScalingGroup LaunchTemplateOverrides <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplateoverrides.html>`_ property type that describes the minimum and maximum baseline bandwidth performance for an instance type, in Mbps.

            :param max: The maximum value in Mbps.
            :param min: The minimum value in Mbps.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-baselineebsbandwidthmbpsrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                baseline_ebs_bandwidth_mbps_request_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.BaselineEbsBandwidthMbpsRequestProperty(
                    max=123,
                    min=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a7a5dad1a6260ae7be680b9b919f7ff3ebd1598458bd6e379de89801a65125e3)
                check_type(argname="argument max", value=max, expected_type=type_hints["max"])
                check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max is not None:
                self._values["max"] = max
            if min is not None:
                self._values["min"] = min

        @builtins.property
        def max(self) -> typing.Optional[jsii.Number]:
            '''The maximum value in Mbps.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-baselineebsbandwidthmbpsrequest.html#cfn-autoscaling-autoscalinggroup-baselineebsbandwidthmbpsrequest-max
            '''
            result = self._values.get("max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min(self) -> typing.Optional[jsii.Number]:
            '''The minimum value in Mbps.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-baselineebsbandwidthmbpsrequest.html#cfn-autoscaling-autoscalinggroup-baselineebsbandwidthmbpsrequest-min
            '''
            result = self._values.get("min")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BaselineEbsBandwidthMbpsRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.BaselinePerformanceFactorsRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"cpu": "cpu"},
    )
    class BaselinePerformanceFactorsRequestProperty:
        def __init__(
            self,
            *,
            cpu: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.CpuPerformanceFactorRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The baseline performance to consider, using an instance family as a baseline reference.

            The instance family establishes the lowest acceptable level of performance. Auto Scaling uses this baseline to guide instance type selection, but there is no guarantee that the selected instance types will always exceed the baseline for every application.

            Currently, this parameter only supports CPU performance as a baseline performance factor. For example, specifying ``c6i`` uses the CPU performance of the ``c6i`` family as the baseline reference.

            :param cpu: The CPU performance to consider, using an instance family as the baseline reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-baselineperformancefactorsrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                baseline_performance_factors_request_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.BaselinePerformanceFactorsRequestProperty(
                    cpu=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.CpuPerformanceFactorRequestProperty(
                        references=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.PerformanceFactorReferenceRequestProperty(
                            instance_family="instanceFamily"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__11466c41d569c969205ad479f837d22fb0ece6ce4d7d06ff9062c76f58332477)
                check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cpu is not None:
                self._values["cpu"] = cpu

        @builtins.property
        def cpu(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.CpuPerformanceFactorRequestProperty"]]:
            '''The CPU performance to consider, using an instance family as the baseline reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-baselineperformancefactorsrequest.html#cfn-autoscaling-autoscalinggroup-baselineperformancefactorsrequest-cpu
            '''
            result = self._values.get("cpu")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.CpuPerformanceFactorRequestProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BaselinePerformanceFactorsRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.CapacityReservationSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capacity_reservation_preference": "capacityReservationPreference",
            "capacity_reservation_target": "capacityReservationTarget",
        },
    )
    class CapacityReservationSpecificationProperty:
        def __init__(
            self,
            *,
            capacity_reservation_preference: typing.Optional[builtins.str] = None,
            capacity_reservation_target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.CapacityReservationTargetProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the Capacity Reservation preference and targeting options.

            If you specify ``open`` or ``none`` for ``CapacityReservationPreference`` , do not specify a ``CapacityReservationTarget`` .

            :param capacity_reservation_preference: The capacity reservation preference. The following options are available:. - ``capacity-reservations-only`` - Auto Scaling will only launch instances into a Capacity Reservation or Capacity Reservation resource group. If capacity isn't available, instances will fail to launch. - ``capacity-reservations-first`` - Auto Scaling will try to launch instances into a Capacity Reservation or Capacity Reservation resource group first. If capacity isn't available, instances will run in On-Demand capacity. - ``none`` - Auto Scaling will not launch instances into a Capacity Reservation. Instances will run in On-Demand capacity. - ``default`` - Auto Scaling uses the Capacity Reservation preference from your launch template or an open Capacity Reservation.
            :param capacity_reservation_target: Describes a target Capacity Reservation or Capacity Reservation resource group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-capacityreservationspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                capacity_reservation_specification_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.CapacityReservationSpecificationProperty(
                    capacity_reservation_preference="capacityReservationPreference",
                    capacity_reservation_target=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.CapacityReservationTargetProperty(
                        capacity_reservation_ids=["capacityReservationIds"],
                        capacity_reservation_resource_group_arns=["capacityReservationResourceGroupArns"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b3f9584945e2608153728d61494b08ca3b13fedacfaf2fdd40268315dfe34794)
                check_type(argname="argument capacity_reservation_preference", value=capacity_reservation_preference, expected_type=type_hints["capacity_reservation_preference"])
                check_type(argname="argument capacity_reservation_target", value=capacity_reservation_target, expected_type=type_hints["capacity_reservation_target"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capacity_reservation_preference is not None:
                self._values["capacity_reservation_preference"] = capacity_reservation_preference
            if capacity_reservation_target is not None:
                self._values["capacity_reservation_target"] = capacity_reservation_target

        @builtins.property
        def capacity_reservation_preference(self) -> typing.Optional[builtins.str]:
            '''The capacity reservation preference. The following options are available:.

            - ``capacity-reservations-only`` - Auto Scaling will only launch instances into a Capacity Reservation or Capacity Reservation resource group. If capacity isn't available, instances will fail to launch.
            - ``capacity-reservations-first`` - Auto Scaling will try to launch instances into a Capacity Reservation or Capacity Reservation resource group first. If capacity isn't available, instances will run in On-Demand capacity.
            - ``none`` - Auto Scaling will not launch instances into a Capacity Reservation. Instances will run in On-Demand capacity.
            - ``default`` - Auto Scaling uses the Capacity Reservation preference from your launch template or an open Capacity Reservation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-capacityreservationspecification.html#cfn-autoscaling-autoscalinggroup-capacityreservationspecification-capacityreservationpreference
            '''
            result = self._values.get("capacity_reservation_preference")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def capacity_reservation_target(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.CapacityReservationTargetProperty"]]:
            '''Describes a target Capacity Reservation or Capacity Reservation resource group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-capacityreservationspecification.html#cfn-autoscaling-autoscalinggroup-capacityreservationspecification-capacityreservationtarget
            '''
            result = self._values.get("capacity_reservation_target")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.CapacityReservationTargetProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityReservationSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.CapacityReservationTargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capacity_reservation_ids": "capacityReservationIds",
            "capacity_reservation_resource_group_arns": "capacityReservationResourceGroupArns",
        },
    )
    class CapacityReservationTargetProperty:
        def __init__(
            self,
            *,
            capacity_reservation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            capacity_reservation_resource_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The target for the Capacity Reservation.

            Specify Capacity Reservations IDs or Capacity Reservation resource group ARNs.

            :param capacity_reservation_ids: The Capacity Reservation IDs to launch instances into.
            :param capacity_reservation_resource_group_arns: The resource group ARNs of the Capacity Reservation to launch instances into.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-capacityreservationtarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                capacity_reservation_target_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.CapacityReservationTargetProperty(
                    capacity_reservation_ids=["capacityReservationIds"],
                    capacity_reservation_resource_group_arns=["capacityReservationResourceGroupArns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6ed7a417ad40a1eefcc9feed5a11525334481f52a8c295ef6f1b7ceffd88aa56)
                check_type(argname="argument capacity_reservation_ids", value=capacity_reservation_ids, expected_type=type_hints["capacity_reservation_ids"])
                check_type(argname="argument capacity_reservation_resource_group_arns", value=capacity_reservation_resource_group_arns, expected_type=type_hints["capacity_reservation_resource_group_arns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capacity_reservation_ids is not None:
                self._values["capacity_reservation_ids"] = capacity_reservation_ids
            if capacity_reservation_resource_group_arns is not None:
                self._values["capacity_reservation_resource_group_arns"] = capacity_reservation_resource_group_arns

        @builtins.property
        def capacity_reservation_ids(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The Capacity Reservation IDs to launch instances into.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-capacityreservationtarget.html#cfn-autoscaling-autoscalinggroup-capacityreservationtarget-capacityreservationids
            '''
            result = self._values.get("capacity_reservation_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def capacity_reservation_resource_group_arns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The resource group ARNs of the Capacity Reservation to launch instances into.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-capacityreservationtarget.html#cfn-autoscaling-autoscalinggroup-capacityreservationtarget-capacityreservationresourcegrouparns
            '''
            result = self._values.get("capacity_reservation_resource_group_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityReservationTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.CpuPerformanceFactorRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"references": "references"},
    )
    class CpuPerformanceFactorRequestProperty:
        def __init__(
            self,
            *,
            references: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.PerformanceFactorReferenceRequestProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The CPU performance to consider, using an instance family as the baseline reference.

            :param references: Specify an instance family to use as the baseline reference for CPU performance. All instance types that match your specified attributes will be compared against the CPU performance of the referenced instance family, regardless of CPU manufacturer or architecture differences. .. epigraph:: Currently only one instance family can be specified in the list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-cpuperformancefactorrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                cpu_performance_factor_request_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.CpuPerformanceFactorRequestProperty(
                    references=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.PerformanceFactorReferenceRequestProperty(
                        instance_family="instanceFamily"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__53621c12a7067d137b4a17dcfa7c0c846a3544d472b367aafcfc0abf7a600cda)
                check_type(argname="argument references", value=references, expected_type=type_hints["references"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if references is not None:
                self._values["references"] = references

        @builtins.property
        def references(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.PerformanceFactorReferenceRequestProperty"]]]]:
            '''Specify an instance family to use as the baseline reference for CPU performance.

            All instance types that match your specified attributes will be compared against the CPU performance of the referenced instance family, regardless of CPU manufacturer or architecture differences.
            .. epigraph::

               Currently only one instance family can be specified in the list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-cpuperformancefactorrequest.html#cfn-autoscaling-autoscalinggroup-cpuperformancefactorrequest-references
            '''
            result = self._values.get("references")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.PerformanceFactorReferenceRequestProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CpuPerformanceFactorRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.InstanceMaintenancePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_healthy_percentage": "maxHealthyPercentage",
            "min_healthy_percentage": "minHealthyPercentage",
        },
    )
    class InstanceMaintenancePolicyProperty:
        def __init__(
            self,
            *,
            max_healthy_percentage: typing.Optional[jsii.Number] = None,
            min_healthy_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``InstanceMaintenancePolicy`` is a property of the `AWS::AutoScaling::AutoScalingGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html>`_ resource.

            For more information, see `Instance maintenance policies <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-instance-maintenance-policy.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

            :param max_healthy_percentage: Specifies the upper threshold as a percentage of the desired capacity of the Auto Scaling group. It represents the maximum percentage of the group that can be in service and healthy, or pending, to support your workload when replacing instances. Value range is 100 to 200. To clear a previously set value, specify a value of ``-1`` . Both ``MinHealthyPercentage`` and ``MaxHealthyPercentage`` must be specified, and the difference between them cannot be greater than 100. A large range increases the number of instances that can be replaced at the same time.
            :param min_healthy_percentage: Specifies the lower threshold as a percentage of the desired capacity of the Auto Scaling group. It represents the minimum percentage of the group to keep in service, healthy, and ready to use to support your workload when replacing instances. Value range is 0 to 100. To clear a previously set value, specify a value of ``-1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancemaintenancepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                instance_maintenance_policy_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.InstanceMaintenancePolicyProperty(
                    max_healthy_percentage=123,
                    min_healthy_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__005b347b6d1c8d4f505704ea90dad06ed58709850ff978bf05a6b3ceea64439e)
                check_type(argname="argument max_healthy_percentage", value=max_healthy_percentage, expected_type=type_hints["max_healthy_percentage"])
                check_type(argname="argument min_healthy_percentage", value=min_healthy_percentage, expected_type=type_hints["min_healthy_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_healthy_percentage is not None:
                self._values["max_healthy_percentage"] = max_healthy_percentage
            if min_healthy_percentage is not None:
                self._values["min_healthy_percentage"] = min_healthy_percentage

        @builtins.property
        def max_healthy_percentage(self) -> typing.Optional[jsii.Number]:
            '''Specifies the upper threshold as a percentage of the desired capacity of the Auto Scaling group.

            It represents the maximum percentage of the group that can be in service and healthy, or pending, to support your workload when replacing instances. Value range is 100 to 200. To clear a previously set value, specify a value of ``-1`` .

            Both ``MinHealthyPercentage`` and ``MaxHealthyPercentage`` must be specified, and the difference between them cannot be greater than 100. A large range increases the number of instances that can be replaced at the same time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancemaintenancepolicy.html#cfn-autoscaling-autoscalinggroup-instancemaintenancepolicy-maxhealthypercentage
            '''
            result = self._values.get("max_healthy_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_healthy_percentage(self) -> typing.Optional[jsii.Number]:
            '''Specifies the lower threshold as a percentage of the desired capacity of the Auto Scaling group.

            It represents the minimum percentage of the group to keep in service, healthy, and ready to use to support your workload when replacing instances. Value range is 0 to 100. To clear a previously set value, specify a value of ``-1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancemaintenancepolicy.html#cfn-autoscaling-autoscalinggroup-instancemaintenancepolicy-minhealthypercentage
            '''
            result = self._values.get("min_healthy_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceMaintenancePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.InstanceRequirementsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "accelerator_count": "acceleratorCount",
            "accelerator_manufacturers": "acceleratorManufacturers",
            "accelerator_names": "acceleratorNames",
            "accelerator_total_memory_mib": "acceleratorTotalMemoryMiB",
            "accelerator_types": "acceleratorTypes",
            "allowed_instance_types": "allowedInstanceTypes",
            "bare_metal": "bareMetal",
            "baseline_ebs_bandwidth_mbps": "baselineEbsBandwidthMbps",
            "baseline_performance_factors": "baselinePerformanceFactors",
            "burstable_performance": "burstablePerformance",
            "cpu_manufacturers": "cpuManufacturers",
            "excluded_instance_types": "excludedInstanceTypes",
            "instance_generations": "instanceGenerations",
            "local_storage": "localStorage",
            "local_storage_types": "localStorageTypes",
            "max_spot_price_as_percentage_of_optimal_on_demand_price": "maxSpotPriceAsPercentageOfOptimalOnDemandPrice",
            "memory_gib_per_v_cpu": "memoryGiBPerVCpu",
            "memory_mib": "memoryMiB",
            "network_bandwidth_gbps": "networkBandwidthGbps",
            "network_interface_count": "networkInterfaceCount",
            "on_demand_max_price_percentage_over_lowest_price": "onDemandMaxPricePercentageOverLowestPrice",
            "require_hibernate_support": "requireHibernateSupport",
            "spot_max_price_percentage_over_lowest_price": "spotMaxPricePercentageOverLowestPrice",
            "total_local_storage_gb": "totalLocalStorageGb",
            "v_cpu_count": "vCpuCount",
        },
    )
    class InstanceRequirementsProperty:
        def __init__(
            self,
            *,
            accelerator_count: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.AcceleratorCountRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            accelerator_manufacturers: typing.Optional[typing.Sequence[builtins.str]] = None,
            accelerator_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            accelerator_total_memory_mib: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.AcceleratorTotalMemoryMiBRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            accelerator_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            allowed_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            bare_metal: typing.Optional[builtins.str] = None,
            baseline_ebs_bandwidth_mbps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.BaselineEbsBandwidthMbpsRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            baseline_performance_factors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.BaselinePerformanceFactorsRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            burstable_performance: typing.Optional[builtins.str] = None,
            cpu_manufacturers: typing.Optional[typing.Sequence[builtins.str]] = None,
            excluded_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            instance_generations: typing.Optional[typing.Sequence[builtins.str]] = None,
            local_storage: typing.Optional[builtins.str] = None,
            local_storage_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            max_spot_price_as_percentage_of_optimal_on_demand_price: typing.Optional[jsii.Number] = None,
            memory_gib_per_v_cpu: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.MemoryGiBPerVCpuRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            memory_mib: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.MemoryMiBRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            network_bandwidth_gbps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.NetworkBandwidthGbpsRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            network_interface_count: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.NetworkInterfaceCountRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            on_demand_max_price_percentage_over_lowest_price: typing.Optional[jsii.Number] = None,
            require_hibernate_support: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            spot_max_price_percentage_over_lowest_price: typing.Optional[jsii.Number] = None,
            total_local_storage_gb: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.TotalLocalStorageGBRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            v_cpu_count: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.VCpuCountRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The attributes for the instance types for a mixed instances policy.

            Amazon EC2 Auto Scaling uses your specified requirements to identify instance types. Then, it uses your On-Demand and Spot allocation strategies to launch instances from these instance types.

            When you specify multiple attributes, you get instance types that satisfy all of the specified attributes. If you specify multiple values for an attribute, you get instance types that satisfy any of the specified values.

            To limit the list of instance types from which Amazon EC2 Auto Scaling can identify matching instance types, you can use one of the following parameters, but not both in the same request:

            - ``AllowedInstanceTypes`` - The instance types to include in the list. All other instance types are ignored, even if they match your specified attributes.
            - ``ExcludedInstanceTypes`` - The instance types to exclude from the list, even if they match your specified attributes.

            .. epigraph::

               You must specify ``VCpuCount`` and ``MemoryMiB`` . All other attributes are optional. Any unspecified optional attribute is set to its default.

            For an example template, see `Configure Amazon EC2 Auto Scaling resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-ec2-auto-scaling.html>`_ .

            For more information, see `Creating an Auto Scaling group using attribute-based instance type selection <https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-asg-instance-type-requirements.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . For help determining which instance types match your attributes before you apply them to your Auto Scaling group, see `Preview instance types with specified attributes <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-fleet-attribute-based-instance-type-selection.html#ec2fleet-get-instance-types-from-instance-requirements>`_ in the *Amazon EC2 User Guide for Linux Instances* .

            ``InstanceRequirements`` is a property of the ``LaunchTemplateOverrides`` property of the `AWS::AutoScaling::AutoScalingGroup LaunchTemplate <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplate.html>`_ property type.

            :param accelerator_count: The minimum and maximum number of accelerators (GPUs, FPGAs, or AWS Inferentia chips) for an instance type. To exclude accelerator-enabled instance types, set ``Max`` to ``0`` . Default: No minimum or maximum limits
            :param accelerator_manufacturers: Indicates whether instance types must have accelerators by specific manufacturers. - For instance types with NVIDIA devices, specify ``nvidia`` . - For instance types with AMD devices, specify ``amd`` . - For instance types with AWS devices, specify ``amazon-web-services`` . - For instance types with Xilinx devices, specify ``xilinx`` . Default: Any manufacturer
            :param accelerator_names: Lists the accelerators that must be on an instance type. - For instance types with NVIDIA A100 GPUs, specify ``a100`` . - For instance types with NVIDIA V100 GPUs, specify ``v100`` . - For instance types with NVIDIA K80 GPUs, specify ``k80`` . - For instance types with NVIDIA T4 GPUs, specify ``t4`` . - For instance types with NVIDIA M60 GPUs, specify ``m60`` . - For instance types with AMD Radeon Pro V520 GPUs, specify ``radeon-pro-v520`` . - For instance types with Xilinx VU9P FPGAs, specify ``vu9p`` . Default: Any accelerator
            :param accelerator_total_memory_mib: The minimum and maximum total memory size for the accelerators on an instance type, in MiB. Default: No minimum or maximum limits
            :param accelerator_types: Lists the accelerator types that must be on an instance type. - For instance types with GPU accelerators, specify ``gpu`` . - For instance types with FPGA accelerators, specify ``fpga`` . - For instance types with inference accelerators, specify ``inference`` . Default: Any accelerator type
            :param allowed_instance_types: The instance types to apply your specified attributes against. All other instance types are ignored, even if they match your specified attributes. You can use strings with one or more wild cards, represented by an asterisk ( ``*`` ), to allow an instance type, size, or generation. The following are examples: ``m5.8xlarge`` , ``c5*.*`` , ``m5a.*`` , ``r*`` , ``*3*`` . For example, if you specify ``c5*`` , Amazon EC2 Auto Scaling will allow the entire C5 instance family, which includes all C5a and C5n instance types. If you specify ``m5a.*`` , Amazon EC2 Auto Scaling will allow all the M5a instance types, but not the M5n instance types. .. epigraph:: If you specify ``AllowedInstanceTypes`` , you can't specify ``ExcludedInstanceTypes`` . Default: All instance types
            :param bare_metal: Indicates whether bare metal instance types are included, excluded, or required. Default: ``excluded``
            :param baseline_ebs_bandwidth_mbps: The minimum and maximum baseline bandwidth performance for an instance type, in Mbps. For more information, see `Amazon EBS–optimized instances <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-optimized.html>`_ in the *Amazon EC2 User Guide* . Default: No minimum or maximum limits
            :param baseline_performance_factors: The baseline performance factors for the instance requirements.
            :param burstable_performance: Indicates whether burstable performance instance types are included, excluded, or required. For more information, see `Burstable performance instances <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances.html>`_ in the *Amazon EC2 User Guide* . Default: ``excluded``
            :param cpu_manufacturers: Lists which specific CPU manufacturers to include. - For instance types with Intel CPUs, specify ``intel`` . - For instance types with AMD CPUs, specify ``amd`` . - For instance types with AWS CPUs, specify ``amazon-web-services`` . - For instance types with Apple CPUs, specify ``apple`` . .. epigraph:: Don't confuse the CPU hardware manufacturer with the CPU hardware architecture. Instances will be launched with a compatible CPU architecture based on the Amazon Machine Image (AMI) that you specify in your launch template. Default: Any manufacturer
            :param excluded_instance_types: The instance types to exclude. You can use strings with one or more wild cards, represented by an asterisk ( ``*`` ), to exclude an instance family, type, size, or generation. The following are examples: ``m5.8xlarge`` , ``c5*.*`` , ``m5a.*`` , ``r*`` , ``*3*`` . For example, if you specify ``c5*`` , you are excluding the entire C5 instance family, which includes all C5a and C5n instance types. If you specify ``m5a.*`` , Amazon EC2 Auto Scaling will exclude all the M5a instance types, but not the M5n instance types. .. epigraph:: If you specify ``ExcludedInstanceTypes`` , you can't specify ``AllowedInstanceTypes`` . Default: No excluded instance types
            :param instance_generations: Indicates whether current or previous generation instance types are included. - For current generation instance types, specify ``current`` . The current generation includes EC2 instance types currently recommended for use. This typically includes the latest two to three generations in each instance family. For more information, see `Instance types <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html>`_ in the *Amazon EC2 User Guide* . - For previous generation instance types, specify ``previous`` . Default: Any current or previous generation
            :param local_storage: Indicates whether instance types with instance store volumes are included, excluded, or required. For more information, see `Amazon EC2 instance store <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html>`_ in the *Amazon EC2 User Guide* . Default: ``included``
            :param local_storage_types: Indicates the type of local storage that is required. - For instance types with hard disk drive (HDD) storage, specify ``hdd`` . - For instance types with solid state drive (SSD) storage, specify ``ssd`` . Default: Any local storage type
            :param max_spot_price_as_percentage_of_optimal_on_demand_price: [Price protection] The price protection threshold for Spot Instances, as a percentage of an identified On-Demand price. The identified On-Demand price is the price of the lowest priced current generation C, M, or R instance type with your specified attributes. If no current generation C, M, or R instance type matches your attributes, then the identified price is from either the lowest priced current generation instance types or, failing that, the lowest priced previous generation instance types that match your attributes. When Amazon EC2 Auto Scaling selects instance types with your attributes, we will exclude instance types whose price exceeds your specified threshold. The parameter accepts an integer, which Amazon EC2 Auto Scaling interprets as a percentage. If you set ``DesiredCapacityType`` to ``vcpu`` or ``memory-mib`` , the price protection threshold is based on the per-vCPU or per-memory price instead of the per instance price. .. epigraph:: Only one of ``SpotMaxPricePercentageOverLowestPrice`` or ``MaxSpotPriceAsPercentageOfOptimalOnDemandPrice`` can be specified. If you don't specify either, Amazon EC2 Auto Scaling will automatically apply optimal price protection to consistently select from a wide range of instance types. To indicate no price protection threshold for Spot Instances, meaning you want to consider all instance types that match your attributes, include one of these parameters and specify a high value, such as ``999999`` .
            :param memory_gib_per_v_cpu: The minimum and maximum amount of memory per vCPU for an instance type, in GiB. Default: No minimum or maximum limits
            :param memory_mib: The minimum and maximum instance memory size for an instance type, in MiB.
            :param network_bandwidth_gbps: The minimum and maximum amount of network bandwidth, in gigabits per second (Gbps). Default: No minimum or maximum limits
            :param network_interface_count: The minimum and maximum number of network interfaces for an instance type. Default: No minimum or maximum limits
            :param on_demand_max_price_percentage_over_lowest_price: [Price protection] The price protection threshold for On-Demand Instances, as a percentage higher than an identified On-Demand price. The identified On-Demand price is the price of the lowest priced current generation C, M, or R instance type with your specified attributes. If no current generation C, M, or R instance type matches your attributes, then the identified price is from either the lowest priced current generation instance types or, failing that, the lowest priced previous generation instance types that match your attributes. When Amazon EC2 Auto Scaling selects instance types with your attributes, we will exclude instance types whose price exceeds your specified threshold. The parameter accepts an integer, which Amazon EC2 Auto Scaling interprets as a percentage. To turn off price protection, specify a high value, such as ``999999`` . If you set ``DesiredCapacityType`` to ``vcpu`` or ``memory-mib`` , the price protection threshold is applied based on the per-vCPU or per-memory price instead of the per instance price. Default: ``20``
            :param require_hibernate_support: Indicates whether instance types must provide On-Demand Instance hibernation support. Default: ``false``
            :param spot_max_price_percentage_over_lowest_price: [Price protection] The price protection threshold for Spot Instances, as a percentage higher than an identified Spot price. The identified Spot price is the price of the lowest priced current generation C, M, or R instance type with your specified attributes. If no current generation C, M, or R instance type matches your attributes, then the identified price is from either the lowest priced current generation instance types or, failing that, the lowest priced previous generation instance types that match your attributes. When Amazon EC2 Auto Scaling selects instance types with your attributes, we will exclude instance types whose price exceeds your specified threshold. The parameter accepts an integer, which Amazon EC2 Auto Scaling interprets as a percentage. If you set ``DesiredCapacityType`` to ``vcpu`` or ``memory-mib`` , the price protection threshold is based on the per-vCPU or per-memory price instead of the per instance price. .. epigraph:: Only one of ``SpotMaxPricePercentageOverLowestPrice`` or ``MaxSpotPriceAsPercentageOfOptimalOnDemandPrice`` can be specified. If you don't specify either, Amazon EC2 Auto Scaling will automatically apply optimal price protection to consistently select from a wide range of instance types. To indicate no price protection threshold for Spot Instances, meaning you want to consider all instance types that match your attributes, include one of these parameters and specify a high value, such as ``999999`` .
            :param total_local_storage_gb: The minimum and maximum total local storage size for an instance type, in GB. Default: No minimum or maximum limits
            :param v_cpu_count: The minimum and maximum number of vCPUs for an instance type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                instance_requirements_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.InstanceRequirementsProperty(
                    accelerator_count=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.AcceleratorCountRequestProperty(
                        max=123,
                        min=123
                    ),
                    accelerator_manufacturers=["acceleratorManufacturers"],
                    accelerator_names=["acceleratorNames"],
                    accelerator_total_memory_mi_b=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.AcceleratorTotalMemoryMiBRequestProperty(
                        max=123,
                        min=123
                    ),
                    accelerator_types=["acceleratorTypes"],
                    allowed_instance_types=["allowedInstanceTypes"],
                    bare_metal="bareMetal",
                    baseline_ebs_bandwidth_mbps=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.BaselineEbsBandwidthMbpsRequestProperty(
                        max=123,
                        min=123
                    ),
                    baseline_performance_factors=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.BaselinePerformanceFactorsRequestProperty(
                        cpu=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.CpuPerformanceFactorRequestProperty(
                            references=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.PerformanceFactorReferenceRequestProperty(
                                instance_family="instanceFamily"
                            )]
                        )
                    ),
                    burstable_performance="burstablePerformance",
                    cpu_manufacturers=["cpuManufacturers"],
                    excluded_instance_types=["excludedInstanceTypes"],
                    instance_generations=["instanceGenerations"],
                    local_storage="localStorage",
                    local_storage_types=["localStorageTypes"],
                    max_spot_price_as_percentage_of_optimal_on_demand_price=123,
                    memory_gi_bPer_vCpu=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.MemoryGiBPerVCpuRequestProperty(
                        max=123,
                        min=123
                    ),
                    memory_mi_b=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.MemoryMiBRequestProperty(
                        max=123,
                        min=123
                    ),
                    network_bandwidth_gbps=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.NetworkBandwidthGbpsRequestProperty(
                        max=123,
                        min=123
                    ),
                    network_interface_count=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.NetworkInterfaceCountRequestProperty(
                        max=123,
                        min=123
                    ),
                    on_demand_max_price_percentage_over_lowest_price=123,
                    require_hibernate_support=False,
                    spot_max_price_percentage_over_lowest_price=123,
                    total_local_storage_gb=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.TotalLocalStorageGBRequestProperty(
                        max=123,
                        min=123
                    ),
                    v_cpu_count=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.VCpuCountRequestProperty(
                        max=123,
                        min=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__87e43296d83349af86ca2cf253b8caa4a97d3c6cd4b61b588c492836f9a676cf)
                check_type(argname="argument accelerator_count", value=accelerator_count, expected_type=type_hints["accelerator_count"])
                check_type(argname="argument accelerator_manufacturers", value=accelerator_manufacturers, expected_type=type_hints["accelerator_manufacturers"])
                check_type(argname="argument accelerator_names", value=accelerator_names, expected_type=type_hints["accelerator_names"])
                check_type(argname="argument accelerator_total_memory_mib", value=accelerator_total_memory_mib, expected_type=type_hints["accelerator_total_memory_mib"])
                check_type(argname="argument accelerator_types", value=accelerator_types, expected_type=type_hints["accelerator_types"])
                check_type(argname="argument allowed_instance_types", value=allowed_instance_types, expected_type=type_hints["allowed_instance_types"])
                check_type(argname="argument bare_metal", value=bare_metal, expected_type=type_hints["bare_metal"])
                check_type(argname="argument baseline_ebs_bandwidth_mbps", value=baseline_ebs_bandwidth_mbps, expected_type=type_hints["baseline_ebs_bandwidth_mbps"])
                check_type(argname="argument baseline_performance_factors", value=baseline_performance_factors, expected_type=type_hints["baseline_performance_factors"])
                check_type(argname="argument burstable_performance", value=burstable_performance, expected_type=type_hints["burstable_performance"])
                check_type(argname="argument cpu_manufacturers", value=cpu_manufacturers, expected_type=type_hints["cpu_manufacturers"])
                check_type(argname="argument excluded_instance_types", value=excluded_instance_types, expected_type=type_hints["excluded_instance_types"])
                check_type(argname="argument instance_generations", value=instance_generations, expected_type=type_hints["instance_generations"])
                check_type(argname="argument local_storage", value=local_storage, expected_type=type_hints["local_storage"])
                check_type(argname="argument local_storage_types", value=local_storage_types, expected_type=type_hints["local_storage_types"])
                check_type(argname="argument max_spot_price_as_percentage_of_optimal_on_demand_price", value=max_spot_price_as_percentage_of_optimal_on_demand_price, expected_type=type_hints["max_spot_price_as_percentage_of_optimal_on_demand_price"])
                check_type(argname="argument memory_gib_per_v_cpu", value=memory_gib_per_v_cpu, expected_type=type_hints["memory_gib_per_v_cpu"])
                check_type(argname="argument memory_mib", value=memory_mib, expected_type=type_hints["memory_mib"])
                check_type(argname="argument network_bandwidth_gbps", value=network_bandwidth_gbps, expected_type=type_hints["network_bandwidth_gbps"])
                check_type(argname="argument network_interface_count", value=network_interface_count, expected_type=type_hints["network_interface_count"])
                check_type(argname="argument on_demand_max_price_percentage_over_lowest_price", value=on_demand_max_price_percentage_over_lowest_price, expected_type=type_hints["on_demand_max_price_percentage_over_lowest_price"])
                check_type(argname="argument require_hibernate_support", value=require_hibernate_support, expected_type=type_hints["require_hibernate_support"])
                check_type(argname="argument spot_max_price_percentage_over_lowest_price", value=spot_max_price_percentage_over_lowest_price, expected_type=type_hints["spot_max_price_percentage_over_lowest_price"])
                check_type(argname="argument total_local_storage_gb", value=total_local_storage_gb, expected_type=type_hints["total_local_storage_gb"])
                check_type(argname="argument v_cpu_count", value=v_cpu_count, expected_type=type_hints["v_cpu_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if accelerator_count is not None:
                self._values["accelerator_count"] = accelerator_count
            if accelerator_manufacturers is not None:
                self._values["accelerator_manufacturers"] = accelerator_manufacturers
            if accelerator_names is not None:
                self._values["accelerator_names"] = accelerator_names
            if accelerator_total_memory_mib is not None:
                self._values["accelerator_total_memory_mib"] = accelerator_total_memory_mib
            if accelerator_types is not None:
                self._values["accelerator_types"] = accelerator_types
            if allowed_instance_types is not None:
                self._values["allowed_instance_types"] = allowed_instance_types
            if bare_metal is not None:
                self._values["bare_metal"] = bare_metal
            if baseline_ebs_bandwidth_mbps is not None:
                self._values["baseline_ebs_bandwidth_mbps"] = baseline_ebs_bandwidth_mbps
            if baseline_performance_factors is not None:
                self._values["baseline_performance_factors"] = baseline_performance_factors
            if burstable_performance is not None:
                self._values["burstable_performance"] = burstable_performance
            if cpu_manufacturers is not None:
                self._values["cpu_manufacturers"] = cpu_manufacturers
            if excluded_instance_types is not None:
                self._values["excluded_instance_types"] = excluded_instance_types
            if instance_generations is not None:
                self._values["instance_generations"] = instance_generations
            if local_storage is not None:
                self._values["local_storage"] = local_storage
            if local_storage_types is not None:
                self._values["local_storage_types"] = local_storage_types
            if max_spot_price_as_percentage_of_optimal_on_demand_price is not None:
                self._values["max_spot_price_as_percentage_of_optimal_on_demand_price"] = max_spot_price_as_percentage_of_optimal_on_demand_price
            if memory_gib_per_v_cpu is not None:
                self._values["memory_gib_per_v_cpu"] = memory_gib_per_v_cpu
            if memory_mib is not None:
                self._values["memory_mib"] = memory_mib
            if network_bandwidth_gbps is not None:
                self._values["network_bandwidth_gbps"] = network_bandwidth_gbps
            if network_interface_count is not None:
                self._values["network_interface_count"] = network_interface_count
            if on_demand_max_price_percentage_over_lowest_price is not None:
                self._values["on_demand_max_price_percentage_over_lowest_price"] = on_demand_max_price_percentage_over_lowest_price
            if require_hibernate_support is not None:
                self._values["require_hibernate_support"] = require_hibernate_support
            if spot_max_price_percentage_over_lowest_price is not None:
                self._values["spot_max_price_percentage_over_lowest_price"] = spot_max_price_percentage_over_lowest_price
            if total_local_storage_gb is not None:
                self._values["total_local_storage_gb"] = total_local_storage_gb
            if v_cpu_count is not None:
                self._values["v_cpu_count"] = v_cpu_count

        @builtins.property
        def accelerator_count(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.AcceleratorCountRequestProperty"]]:
            '''The minimum and maximum number of accelerators (GPUs, FPGAs, or AWS Inferentia chips) for an instance type.

            To exclude accelerator-enabled instance types, set ``Max`` to ``0`` .

            Default: No minimum or maximum limits

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-acceleratorcount
            '''
            result = self._values.get("accelerator_count")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.AcceleratorCountRequestProperty"]], result)

        @builtins.property
        def accelerator_manufacturers(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''Indicates whether instance types must have accelerators by specific manufacturers.

            - For instance types with NVIDIA devices, specify ``nvidia`` .
            - For instance types with AMD devices, specify ``amd`` .
            - For instance types with AWS devices, specify ``amazon-web-services`` .
            - For instance types with Xilinx devices, specify ``xilinx`` .

            Default: Any manufacturer

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-acceleratormanufacturers
            '''
            result = self._values.get("accelerator_manufacturers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def accelerator_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Lists the accelerators that must be on an instance type.

            - For instance types with NVIDIA A100 GPUs, specify ``a100`` .
            - For instance types with NVIDIA V100 GPUs, specify ``v100`` .
            - For instance types with NVIDIA K80 GPUs, specify ``k80`` .
            - For instance types with NVIDIA T4 GPUs, specify ``t4`` .
            - For instance types with NVIDIA M60 GPUs, specify ``m60`` .
            - For instance types with AMD Radeon Pro V520 GPUs, specify ``radeon-pro-v520`` .
            - For instance types with Xilinx VU9P FPGAs, specify ``vu9p`` .

            Default: Any accelerator

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-acceleratornames
            '''
            result = self._values.get("accelerator_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def accelerator_total_memory_mib(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.AcceleratorTotalMemoryMiBRequestProperty"]]:
            '''The minimum and maximum total memory size for the accelerators on an instance type, in MiB.

            Default: No minimum or maximum limits

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-acceleratortotalmemorymib
            '''
            result = self._values.get("accelerator_total_memory_mib")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.AcceleratorTotalMemoryMiBRequestProperty"]], result)

        @builtins.property
        def accelerator_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Lists the accelerator types that must be on an instance type.

            - For instance types with GPU accelerators, specify ``gpu`` .
            - For instance types with FPGA accelerators, specify ``fpga`` .
            - For instance types with inference accelerators, specify ``inference`` .

            Default: Any accelerator type

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-acceleratortypes
            '''
            result = self._values.get("accelerator_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allowed_instance_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The instance types to apply your specified attributes against.

            All other instance types are ignored, even if they match your specified attributes.

            You can use strings with one or more wild cards, represented by an asterisk ( ``*`` ), to allow an instance type, size, or generation. The following are examples: ``m5.8xlarge`` , ``c5*.*`` , ``m5a.*`` , ``r*`` , ``*3*`` .

            For example, if you specify ``c5*`` , Amazon EC2 Auto Scaling will allow the entire C5 instance family, which includes all C5a and C5n instance types. If you specify ``m5a.*`` , Amazon EC2 Auto Scaling will allow all the M5a instance types, but not the M5n instance types.
            .. epigraph::

               If you specify ``AllowedInstanceTypes`` , you can't specify ``ExcludedInstanceTypes`` .

            Default: All instance types

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-allowedinstancetypes
            '''
            result = self._values.get("allowed_instance_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def bare_metal(self) -> typing.Optional[builtins.str]:
            '''Indicates whether bare metal instance types are included, excluded, or required.

            Default: ``excluded``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-baremetal
            '''
            result = self._values.get("bare_metal")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def baseline_ebs_bandwidth_mbps(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.BaselineEbsBandwidthMbpsRequestProperty"]]:
            '''The minimum and maximum baseline bandwidth performance for an instance type, in Mbps.

            For more information, see `Amazon EBS–optimized instances <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-optimized.html>`_ in the *Amazon EC2 User Guide* .

            Default: No minimum or maximum limits

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-baselineebsbandwidthmbps
            '''
            result = self._values.get("baseline_ebs_bandwidth_mbps")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.BaselineEbsBandwidthMbpsRequestProperty"]], result)

        @builtins.property
        def baseline_performance_factors(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.BaselinePerformanceFactorsRequestProperty"]]:
            '''The baseline performance factors for the instance requirements.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-baselineperformancefactors
            '''
            result = self._values.get("baseline_performance_factors")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.BaselinePerformanceFactorsRequestProperty"]], result)

        @builtins.property
        def burstable_performance(self) -> typing.Optional[builtins.str]:
            '''Indicates whether burstable performance instance types are included, excluded, or required.

            For more information, see `Burstable performance instances <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances.html>`_ in the *Amazon EC2 User Guide* .

            Default: ``excluded``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-burstableperformance
            '''
            result = self._values.get("burstable_performance")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cpu_manufacturers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Lists which specific CPU manufacturers to include.

            - For instance types with Intel CPUs, specify ``intel`` .
            - For instance types with AMD CPUs, specify ``amd`` .
            - For instance types with AWS CPUs, specify ``amazon-web-services`` .
            - For instance types with Apple CPUs, specify ``apple`` .

            .. epigraph::

               Don't confuse the CPU hardware manufacturer with the CPU hardware architecture. Instances will be launched with a compatible CPU architecture based on the Amazon Machine Image (AMI) that you specify in your launch template.

            Default: Any manufacturer

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-cpumanufacturers
            '''
            result = self._values.get("cpu_manufacturers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def excluded_instance_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The instance types to exclude.

            You can use strings with one or more wild cards, represented by an asterisk ( ``*`` ), to exclude an instance family, type, size, or generation. The following are examples: ``m5.8xlarge`` , ``c5*.*`` , ``m5a.*`` , ``r*`` , ``*3*`` .

            For example, if you specify ``c5*`` , you are excluding the entire C5 instance family, which includes all C5a and C5n instance types. If you specify ``m5a.*`` , Amazon EC2 Auto Scaling will exclude all the M5a instance types, but not the M5n instance types.
            .. epigraph::

               If you specify ``ExcludedInstanceTypes`` , you can't specify ``AllowedInstanceTypes`` .

            Default: No excluded instance types

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-excludedinstancetypes
            '''
            result = self._values.get("excluded_instance_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def instance_generations(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Indicates whether current or previous generation instance types are included.

            - For current generation instance types, specify ``current`` . The current generation includes EC2 instance types currently recommended for use. This typically includes the latest two to three generations in each instance family. For more information, see `Instance types <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html>`_ in the *Amazon EC2 User Guide* .
            - For previous generation instance types, specify ``previous`` .

            Default: Any current or previous generation

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-instancegenerations
            '''
            result = self._values.get("instance_generations")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def local_storage(self) -> typing.Optional[builtins.str]:
            '''Indicates whether instance types with instance store volumes are included, excluded, or required.

            For more information, see `Amazon EC2 instance store <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html>`_ in the *Amazon EC2 User Guide* .

            Default: ``included``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-localstorage
            '''
            result = self._values.get("local_storage")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def local_storage_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Indicates the type of local storage that is required.

            - For instance types with hard disk drive (HDD) storage, specify ``hdd`` .
            - For instance types with solid state drive (SSD) storage, specify ``ssd`` .

            Default: Any local storage type

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-localstoragetypes
            '''
            result = self._values.get("local_storage_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def max_spot_price_as_percentage_of_optimal_on_demand_price(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''[Price protection] The price protection threshold for Spot Instances, as a percentage of an identified On-Demand price.

            The identified On-Demand price is the price of the lowest priced current generation C, M, or R instance type with your specified attributes. If no current generation C, M, or R instance type matches your attributes, then the identified price is from either the lowest priced current generation instance types or, failing that, the lowest priced previous generation instance types that match your attributes. When Amazon EC2 Auto Scaling selects instance types with your attributes, we will exclude instance types whose price exceeds your specified threshold.

            The parameter accepts an integer, which Amazon EC2 Auto Scaling interprets as a percentage.

            If you set ``DesiredCapacityType`` to ``vcpu`` or ``memory-mib`` , the price protection threshold is based on the per-vCPU or per-memory price instead of the per instance price.
            .. epigraph::

               Only one of ``SpotMaxPricePercentageOverLowestPrice`` or ``MaxSpotPriceAsPercentageOfOptimalOnDemandPrice`` can be specified. If you don't specify either, Amazon EC2 Auto Scaling will automatically apply optimal price protection to consistently select from a wide range of instance types. To indicate no price protection threshold for Spot Instances, meaning you want to consider all instance types that match your attributes, include one of these parameters and specify a high value, such as ``999999`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-maxspotpriceaspercentageofoptimalondemandprice
            '''
            result = self._values.get("max_spot_price_as_percentage_of_optimal_on_demand_price")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def memory_gib_per_v_cpu(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.MemoryGiBPerVCpuRequestProperty"]]:
            '''The minimum and maximum amount of memory per vCPU for an instance type, in GiB.

            Default: No minimum or maximum limits

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-memorygibpervcpu
            '''
            result = self._values.get("memory_gib_per_v_cpu")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.MemoryGiBPerVCpuRequestProperty"]], result)

        @builtins.property
        def memory_mib(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.MemoryMiBRequestProperty"]]:
            '''The minimum and maximum instance memory size for an instance type, in MiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-memorymib
            '''
            result = self._values.get("memory_mib")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.MemoryMiBRequestProperty"]], result)

        @builtins.property
        def network_bandwidth_gbps(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.NetworkBandwidthGbpsRequestProperty"]]:
            '''The minimum and maximum amount of network bandwidth, in gigabits per second (Gbps).

            Default: No minimum or maximum limits

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-networkbandwidthgbps
            '''
            result = self._values.get("network_bandwidth_gbps")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.NetworkBandwidthGbpsRequestProperty"]], result)

        @builtins.property
        def network_interface_count(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.NetworkInterfaceCountRequestProperty"]]:
            '''The minimum and maximum number of network interfaces for an instance type.

            Default: No minimum or maximum limits

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-networkinterfacecount
            '''
            result = self._values.get("network_interface_count")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.NetworkInterfaceCountRequestProperty"]], result)

        @builtins.property
        def on_demand_max_price_percentage_over_lowest_price(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''[Price protection] The price protection threshold for On-Demand Instances, as a percentage higher than an identified On-Demand price.

            The identified On-Demand price is the price of the lowest priced current generation C, M, or R instance type with your specified attributes. If no current generation C, M, or R instance type matches your attributes, then the identified price is from either the lowest priced current generation instance types or, failing that, the lowest priced previous generation instance types that match your attributes. When Amazon EC2 Auto Scaling selects instance types with your attributes, we will exclude instance types whose price exceeds your specified threshold.

            The parameter accepts an integer, which Amazon EC2 Auto Scaling interprets as a percentage.

            To turn off price protection, specify a high value, such as ``999999`` .

            If you set ``DesiredCapacityType`` to ``vcpu`` or ``memory-mib`` , the price protection threshold is applied based on the per-vCPU or per-memory price instead of the per instance price.

            Default: ``20``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-ondemandmaxpricepercentageoverlowestprice
            '''
            result = self._values.get("on_demand_max_price_percentage_over_lowest_price")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def require_hibernate_support(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether instance types must provide On-Demand Instance hibernation support.

            Default: ``false``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-requirehibernatesupport
            '''
            result = self._values.get("require_hibernate_support")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def spot_max_price_percentage_over_lowest_price(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''[Price protection] The price protection threshold for Spot Instances, as a percentage higher than an identified Spot price.

            The identified Spot price is the price of the lowest priced current generation C, M, or R instance type with your specified attributes. If no current generation C, M, or R instance type matches your attributes, then the identified price is from either the lowest priced current generation instance types or, failing that, the lowest priced previous generation instance types that match your attributes. When Amazon EC2 Auto Scaling selects instance types with your attributes, we will exclude instance types whose price exceeds your specified threshold.

            The parameter accepts an integer, which Amazon EC2 Auto Scaling interprets as a percentage.

            If you set ``DesiredCapacityType`` to ``vcpu`` or ``memory-mib`` , the price protection threshold is based on the per-vCPU or per-memory price instead of the per instance price.
            .. epigraph::

               Only one of ``SpotMaxPricePercentageOverLowestPrice`` or ``MaxSpotPriceAsPercentageOfOptimalOnDemandPrice`` can be specified. If you don't specify either, Amazon EC2 Auto Scaling will automatically apply optimal price protection to consistently select from a wide range of instance types. To indicate no price protection threshold for Spot Instances, meaning you want to consider all instance types that match your attributes, include one of these parameters and specify a high value, such as ``999999`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-spotmaxpricepercentageoverlowestprice
            '''
            result = self._values.get("spot_max_price_percentage_over_lowest_price")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def total_local_storage_gb(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.TotalLocalStorageGBRequestProperty"]]:
            '''The minimum and maximum total local storage size for an instance type, in GB.

            Default: No minimum or maximum limits

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-totallocalstoragegb
            '''
            result = self._values.get("total_local_storage_gb")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.TotalLocalStorageGBRequestProperty"]], result)

        @builtins.property
        def v_cpu_count(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.VCpuCountRequestProperty"]]:
            '''The minimum and maximum number of vCPUs for an instance type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancerequirements.html#cfn-autoscaling-autoscalinggroup-instancerequirements-vcpucount
            '''
            result = self._values.get("v_cpu_count")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.VCpuCountRequestProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceRequirementsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.InstancesDistributionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "on_demand_allocation_strategy": "onDemandAllocationStrategy",
            "on_demand_base_capacity": "onDemandBaseCapacity",
            "on_demand_percentage_above_base_capacity": "onDemandPercentageAboveBaseCapacity",
            "spot_allocation_strategy": "spotAllocationStrategy",
            "spot_instance_pools": "spotInstancePools",
            "spot_max_price": "spotMaxPrice",
        },
    )
    class InstancesDistributionProperty:
        def __init__(
            self,
            *,
            on_demand_allocation_strategy: typing.Optional[builtins.str] = None,
            on_demand_base_capacity: typing.Optional[jsii.Number] = None,
            on_demand_percentage_above_base_capacity: typing.Optional[jsii.Number] = None,
            spot_allocation_strategy: typing.Optional[builtins.str] = None,
            spot_instance_pools: typing.Optional[jsii.Number] = None,
            spot_max_price: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use this structure to specify the distribution of On-Demand Instances and Spot Instances and the allocation strategies used to fulfill On-Demand and Spot capacities for a mixed instances policy.

            For more information, see `Auto Scaling groups with multiple instance types and purchase options <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-mixed-instances-groups.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

            ``InstancesDistribution`` is a property of the `AWS::AutoScaling::AutoScalingGroup MixedInstancesPolicy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-mixedinstancespolicy.html>`_ property type.

            :param on_demand_allocation_strategy: The allocation strategy to apply to your On-Demand Instances when they are launched. Possible instance types are determined by the launch template overrides that you specify. The following lists the valid values: - **lowest-price** - Uses price to determine which instance types are the highest priority, launching the lowest priced instance types within an Availability Zone first. This is the default value for Auto Scaling groups that specify ``InstanceRequirements`` . - **prioritized** - You set the order of instance types for the launch template overrides from highest to lowest priority (from first to last in the list). Amazon EC2 Auto Scaling launches your highest priority instance types first. If all your On-Demand capacity cannot be fulfilled using your highest priority instance type, then Amazon EC2 Auto Scaling launches the remaining capacity using the second priority instance type, and so on. This is the default value for Auto Scaling groups that don't specify ``InstanceRequirements`` and cannot be used for groups that do.
            :param on_demand_base_capacity: The minimum amount of the Auto Scaling group's capacity that must be fulfilled by On-Demand Instances. This base portion is launched first as your group scales. This number has the same unit of measurement as the group's desired capacity. If you change the default unit of measurement (number of instances) by specifying weighted capacity values in your launch template overrides list, or by changing the default desired capacity type setting of the group, you must specify this number using the same unit of measurement. Default: 0 .. epigraph:: An update to this setting means a gradual replacement of instances to adjust the current On-Demand Instance levels. When replacing instances, Amazon EC2 Auto Scaling launches new instances before terminating the previous ones.
            :param on_demand_percentage_above_base_capacity: Controls the percentages of On-Demand Instances and Spot Instances for your additional capacity beyond ``OnDemandBaseCapacity`` . Expressed as a number (for example, 20 specifies 20% On-Demand Instances, 80% Spot Instances). If set to 100, only On-Demand Instances are used. Default: 100 .. epigraph:: An update to this setting means a gradual replacement of instances to adjust the current On-Demand and Spot Instance levels for your additional capacity higher than the base capacity. When replacing instances, Amazon EC2 Auto Scaling launches new instances before terminating the previous ones.
            :param spot_allocation_strategy: The allocation strategy to apply to your Spot Instances when they are launched. Possible instance types are determined by the launch template overrides that you specify. The following lists the valid values: - **capacity-optimized** - Requests Spot Instances using pools that are optimally chosen based on the available Spot capacity. This strategy has the lowest risk of interruption. To give certain instance types a higher chance of launching first, use ``capacity-optimized-prioritized`` . - **capacity-optimized-prioritized** - You set the order of instance types for the launch template overrides from highest to lowest priority (from first to last in the list). Amazon EC2 Auto Scaling honors the instance type priorities on a best effort basis but optimizes for capacity first. Note that if the On-Demand allocation strategy is set to ``prioritized`` , the same priority is applied when fulfilling On-Demand capacity. This is not a valid value for Auto Scaling groups that specify ``InstanceRequirements`` . - **lowest-price** - Requests Spot Instances using the lowest priced pools within an Availability Zone, across the number of Spot pools that you specify for the ``SpotInstancePools`` property. To ensure that your desired capacity is met, you might receive Spot Instances from several pools. This is the default value, but it might lead to high interruption rates because this strategy only considers instance price and not available capacity. - **price-capacity-optimized (recommended)** - The price and capacity optimized allocation strategy looks at both price and capacity to select the Spot Instance pools that are the least likely to be interrupted and have the lowest possible price.
            :param spot_instance_pools: The number of Spot Instance pools across which to allocate your Spot Instances. The Spot pools are determined from the different instance types in the overrides. Valid only when the ``SpotAllocationStrategy`` is ``lowest-price`` . Value must be in the range of 1–20. Default: 2
            :param spot_max_price: The maximum price per unit hour that you are willing to pay for a Spot Instance. If your maximum price is lower than the Spot price for the instance types that you selected, your Spot Instances are not launched. We do not recommend specifying a maximum price because it can lead to increased interruptions. When Spot Instances launch, you pay the current Spot price. To remove a maximum price that you previously set, include the property but specify an empty string ("") for the value. .. epigraph:: If you specify a maximum price, your instances will be interrupted more frequently than if you do not specify one. Valid Range: Minimum value of 0.001

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancesdistribution.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                instances_distribution_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.InstancesDistributionProperty(
                    on_demand_allocation_strategy="onDemandAllocationStrategy",
                    on_demand_base_capacity=123,
                    on_demand_percentage_above_base_capacity=123,
                    spot_allocation_strategy="spotAllocationStrategy",
                    spot_instance_pools=123,
                    spot_max_price="spotMaxPrice"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__610ae3c0f0e10395c86ab0fd13d9546ce16d622da416b1600f9adae1c504b814)
                check_type(argname="argument on_demand_allocation_strategy", value=on_demand_allocation_strategy, expected_type=type_hints["on_demand_allocation_strategy"])
                check_type(argname="argument on_demand_base_capacity", value=on_demand_base_capacity, expected_type=type_hints["on_demand_base_capacity"])
                check_type(argname="argument on_demand_percentage_above_base_capacity", value=on_demand_percentage_above_base_capacity, expected_type=type_hints["on_demand_percentage_above_base_capacity"])
                check_type(argname="argument spot_allocation_strategy", value=spot_allocation_strategy, expected_type=type_hints["spot_allocation_strategy"])
                check_type(argname="argument spot_instance_pools", value=spot_instance_pools, expected_type=type_hints["spot_instance_pools"])
                check_type(argname="argument spot_max_price", value=spot_max_price, expected_type=type_hints["spot_max_price"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if on_demand_allocation_strategy is not None:
                self._values["on_demand_allocation_strategy"] = on_demand_allocation_strategy
            if on_demand_base_capacity is not None:
                self._values["on_demand_base_capacity"] = on_demand_base_capacity
            if on_demand_percentage_above_base_capacity is not None:
                self._values["on_demand_percentage_above_base_capacity"] = on_demand_percentage_above_base_capacity
            if spot_allocation_strategy is not None:
                self._values["spot_allocation_strategy"] = spot_allocation_strategy
            if spot_instance_pools is not None:
                self._values["spot_instance_pools"] = spot_instance_pools
            if spot_max_price is not None:
                self._values["spot_max_price"] = spot_max_price

        @builtins.property
        def on_demand_allocation_strategy(self) -> typing.Optional[builtins.str]:
            '''The allocation strategy to apply to your On-Demand Instances when they are launched.

            Possible instance types are determined by the launch template overrides that you specify.

            The following lists the valid values:

            - **lowest-price** - Uses price to determine which instance types are the highest priority, launching the lowest priced instance types within an Availability Zone first. This is the default value for Auto Scaling groups that specify ``InstanceRequirements`` .
            - **prioritized** - You set the order of instance types for the launch template overrides from highest to lowest priority (from first to last in the list). Amazon EC2 Auto Scaling launches your highest priority instance types first. If all your On-Demand capacity cannot be fulfilled using your highest priority instance type, then Amazon EC2 Auto Scaling launches the remaining capacity using the second priority instance type, and so on. This is the default value for Auto Scaling groups that don't specify ``InstanceRequirements`` and cannot be used for groups that do.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-ondemandallocationstrategy
            '''
            result = self._values.get("on_demand_allocation_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def on_demand_base_capacity(self) -> typing.Optional[jsii.Number]:
            '''The minimum amount of the Auto Scaling group's capacity that must be fulfilled by On-Demand Instances.

            This base portion is launched first as your group scales.

            This number has the same unit of measurement as the group's desired capacity. If you change the default unit of measurement (number of instances) by specifying weighted capacity values in your launch template overrides list, or by changing the default desired capacity type setting of the group, you must specify this number using the same unit of measurement.

            Default: 0
            .. epigraph::

               An update to this setting means a gradual replacement of instances to adjust the current On-Demand Instance levels. When replacing instances, Amazon EC2 Auto Scaling launches new instances before terminating the previous ones.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-ondemandbasecapacity
            '''
            result = self._values.get("on_demand_base_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def on_demand_percentage_above_base_capacity(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''Controls the percentages of On-Demand Instances and Spot Instances for your additional capacity beyond ``OnDemandBaseCapacity`` .

            Expressed as a number (for example, 20 specifies 20% On-Demand Instances, 80% Spot Instances). If set to 100, only On-Demand Instances are used.

            Default: 100
            .. epigraph::

               An update to this setting means a gradual replacement of instances to adjust the current On-Demand and Spot Instance levels for your additional capacity higher than the base capacity. When replacing instances, Amazon EC2 Auto Scaling launches new instances before terminating the previous ones.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-ondemandpercentageabovebasecapacity
            '''
            result = self._values.get("on_demand_percentage_above_base_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def spot_allocation_strategy(self) -> typing.Optional[builtins.str]:
            '''The allocation strategy to apply to your Spot Instances when they are launched.

            Possible instance types are determined by the launch template overrides that you specify.

            The following lists the valid values:

            - **capacity-optimized** - Requests Spot Instances using pools that are optimally chosen based on the available Spot capacity. This strategy has the lowest risk of interruption. To give certain instance types a higher chance of launching first, use ``capacity-optimized-prioritized`` .
            - **capacity-optimized-prioritized** - You set the order of instance types for the launch template overrides from highest to lowest priority (from first to last in the list). Amazon EC2 Auto Scaling honors the instance type priorities on a best effort basis but optimizes for capacity first. Note that if the On-Demand allocation strategy is set to ``prioritized`` , the same priority is applied when fulfilling On-Demand capacity. This is not a valid value for Auto Scaling groups that specify ``InstanceRequirements`` .
            - **lowest-price** - Requests Spot Instances using the lowest priced pools within an Availability Zone, across the number of Spot pools that you specify for the ``SpotInstancePools`` property. To ensure that your desired capacity is met, you might receive Spot Instances from several pools. This is the default value, but it might lead to high interruption rates because this strategy only considers instance price and not available capacity.
            - **price-capacity-optimized (recommended)** - The price and capacity optimized allocation strategy looks at both price and capacity to select the Spot Instance pools that are the least likely to be interrupted and have the lowest possible price.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-spotallocationstrategy
            '''
            result = self._values.get("spot_allocation_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def spot_instance_pools(self) -> typing.Optional[jsii.Number]:
            '''The number of Spot Instance pools across which to allocate your Spot Instances.

            The Spot pools are determined from the different instance types in the overrides. Valid only when the ``SpotAllocationStrategy`` is ``lowest-price`` . Value must be in the range of 1–20.

            Default: 2

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-spotinstancepools
            '''
            result = self._values.get("spot_instance_pools")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def spot_max_price(self) -> typing.Optional[builtins.str]:
            '''The maximum price per unit hour that you are willing to pay for a Spot Instance.

            If your maximum price is lower than the Spot price for the instance types that you selected, your Spot Instances are not launched. We do not recommend specifying a maximum price because it can lead to increased interruptions. When Spot Instances launch, you pay the current Spot price. To remove a maximum price that you previously set, include the property but specify an empty string ("") for the value.
            .. epigraph::

               If you specify a maximum price, your instances will be interrupted more frequently than if you do not specify one.

            Valid Range: Minimum value of 0.001

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-spotmaxprice
            '''
            result = self._values.get("spot_max_price")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstancesDistributionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateOverridesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instance_requirements": "instanceRequirements",
            "instance_type": "instanceType",
            "launch_template_specification": "launchTemplateSpecification",
            "weighted_capacity": "weightedCapacity",
        },
    )
    class LaunchTemplateOverridesProperty:
        def __init__(
            self,
            *,
            instance_requirements: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.InstanceRequirementsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            instance_type: typing.Optional[builtins.str] = None,
            launch_template_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            weighted_capacity: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use this structure to let Amazon EC2 Auto Scaling do the following when the Auto Scaling group has a mixed instances policy:  - Override the instance type that is specified in the launch template.

            - Use multiple instance types.

            Specify the instance types that you want, or define your instance requirements instead and let Amazon EC2 Auto Scaling provision the available instance types that meet your requirements. This can provide Amazon EC2 Auto Scaling with a larger selection of instance types to choose from when fulfilling Spot and On-Demand capacities. You can view which instance types are matched before you apply the instance requirements to your Auto Scaling group.

            After you define your instance requirements, you don't have to keep updating these settings to get new EC2 instance types automatically. Amazon EC2 Auto Scaling uses the instance requirements of the Auto Scaling group to determine whether a new EC2 instance type can be used.

            ``LaunchTemplateOverrides`` is a property of the `AWS::AutoScaling::AutoScalingGroup LaunchTemplate <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplate.html>`_ property type.

            :param instance_requirements: The instance requirements. Amazon EC2 Auto Scaling uses your specified requirements to identify instance types. Then, it uses your On-Demand and Spot allocation strategies to launch instances from these instance types. You can specify up to four separate sets of instance requirements per Auto Scaling group. This is useful for provisioning instances from different Amazon Machine Images (AMIs) in the same Auto Scaling group. To do this, create the AMIs and create a new launch template for each AMI. Then, create a compatible set of instance requirements for each launch template. .. epigraph:: If you specify ``InstanceRequirements`` , you can't specify ``InstanceType`` .
            :param instance_type: The instance type, such as ``m3.xlarge`` . You must specify an instance type that is supported in your requested Region and Availability Zones. For more information, see `Instance types <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html>`_ in the *Amazon EC2 User Guide* . You can specify up to 40 instance types per Auto Scaling group.
            :param launch_template_specification: Provides a launch template for the specified instance type or set of instance requirements. For example, some instance types might require a launch template with a different AMI. If not provided, Amazon EC2 Auto Scaling uses the launch template that's specified in the ``LaunchTemplate`` definition. For more information, see `Specifying a different launch template for an instance type <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-mixed-instances-groups-launch-template-overrides.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . You can specify up to 20 launch templates per Auto Scaling group. The launch templates specified in the overrides and in the ``LaunchTemplate`` definition count towards this limit.
            :param weighted_capacity: If you provide a list of instance types to use, you can specify the number of capacity units provided by each instance type in terms of virtual CPUs, memory, storage, throughput, or other relative performance characteristic. When a Spot or On-Demand Instance is launched, the capacity units count toward the desired capacity. Amazon EC2 Auto Scaling launches instances until the desired capacity is totally fulfilled, even if this results in an overage. For example, if there are two units remaining to fulfill capacity, and Amazon EC2 Auto Scaling can only launch an instance with a ``WeightedCapacity`` of five units, the instance is launched, and the desired capacity is exceeded by three units. For more information, see `Configure instance weighting for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-mixed-instances-groups-instance-weighting.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . Value must be in the range of 1-999. If you specify a value for ``WeightedCapacity`` for one instance type, you must specify a value for ``WeightedCapacity`` for all of them. .. epigraph:: Every Auto Scaling group has three size parameters ( ``DesiredCapacity`` , ``MaxSize`` , and ``MinSize`` ). Usually, you set these sizes based on a specific number of instances. However, if you configure a mixed instances policy that defines weights for the instance types, you must specify these sizes with the same units that you use for weighting instances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplateoverrides.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                launch_template_overrides_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateOverridesProperty(
                    instance_requirements=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.InstanceRequirementsProperty(
                        accelerator_count=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.AcceleratorCountRequestProperty(
                            max=123,
                            min=123
                        ),
                        accelerator_manufacturers=["acceleratorManufacturers"],
                        accelerator_names=["acceleratorNames"],
                        accelerator_total_memory_mi_b=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.AcceleratorTotalMemoryMiBRequestProperty(
                            max=123,
                            min=123
                        ),
                        accelerator_types=["acceleratorTypes"],
                        allowed_instance_types=["allowedInstanceTypes"],
                        bare_metal="bareMetal",
                        baseline_ebs_bandwidth_mbps=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.BaselineEbsBandwidthMbpsRequestProperty(
                            max=123,
                            min=123
                        ),
                        baseline_performance_factors=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.BaselinePerformanceFactorsRequestProperty(
                            cpu=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.CpuPerformanceFactorRequestProperty(
                                references=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.PerformanceFactorReferenceRequestProperty(
                                    instance_family="instanceFamily"
                                )]
                            )
                        ),
                        burstable_performance="burstablePerformance",
                        cpu_manufacturers=["cpuManufacturers"],
                        excluded_instance_types=["excludedInstanceTypes"],
                        instance_generations=["instanceGenerations"],
                        local_storage="localStorage",
                        local_storage_types=["localStorageTypes"],
                        max_spot_price_as_percentage_of_optimal_on_demand_price=123,
                        memory_gi_bPer_vCpu=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.MemoryGiBPerVCpuRequestProperty(
                            max=123,
                            min=123
                        ),
                        memory_mi_b=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.MemoryMiBRequestProperty(
                            max=123,
                            min=123
                        ),
                        network_bandwidth_gbps=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.NetworkBandwidthGbpsRequestProperty(
                            max=123,
                            min=123
                        ),
                        network_interface_count=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.NetworkInterfaceCountRequestProperty(
                            max=123,
                            min=123
                        ),
                        on_demand_max_price_percentage_over_lowest_price=123,
                        require_hibernate_support=False,
                        spot_max_price_percentage_over_lowest_price=123,
                        total_local_storage_gb=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.TotalLocalStorageGBRequestProperty(
                            max=123,
                            min=123
                        ),
                        v_cpu_count=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.VCpuCountRequestProperty(
                            max=123,
                            min=123
                        )
                    ),
                    instance_type="instanceType",
                    launch_template_specification=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty(
                        launch_template_id="launchTemplateId",
                        launch_template_name="launchTemplateName",
                        version="version"
                    ),
                    weighted_capacity="weightedCapacity"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5ec8399276e828b87e907129eb104baa65d299177eecadd4d33a5328e6ed888d)
                check_type(argname="argument instance_requirements", value=instance_requirements, expected_type=type_hints["instance_requirements"])
                check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                check_type(argname="argument launch_template_specification", value=launch_template_specification, expected_type=type_hints["launch_template_specification"])
                check_type(argname="argument weighted_capacity", value=weighted_capacity, expected_type=type_hints["weighted_capacity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_requirements is not None:
                self._values["instance_requirements"] = instance_requirements
            if instance_type is not None:
                self._values["instance_type"] = instance_type
            if launch_template_specification is not None:
                self._values["launch_template_specification"] = launch_template_specification
            if weighted_capacity is not None:
                self._values["weighted_capacity"] = weighted_capacity

        @builtins.property
        def instance_requirements(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.InstanceRequirementsProperty"]]:
            '''The instance requirements.

            Amazon EC2 Auto Scaling uses your specified requirements to identify instance types. Then, it uses your On-Demand and Spot allocation strategies to launch instances from these instance types.

            You can specify up to four separate sets of instance requirements per Auto Scaling group. This is useful for provisioning instances from different Amazon Machine Images (AMIs) in the same Auto Scaling group. To do this, create the AMIs and create a new launch template for each AMI. Then, create a compatible set of instance requirements for each launch template.
            .. epigraph::

               If you specify ``InstanceRequirements`` , you can't specify ``InstanceType`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplateoverrides.html#cfn-autoscaling-autoscalinggroup-launchtemplateoverrides-instancerequirements
            '''
            result = self._values.get("instance_requirements")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.InstanceRequirementsProperty"]], result)

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            '''The instance type, such as ``m3.xlarge`` . You must specify an instance type that is supported in your requested Region and Availability Zones. For more information, see `Instance types <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html>`_ in the *Amazon EC2 User Guide* .

            You can specify up to 40 instance types per Auto Scaling group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplateoverrides.html#cfn-autoscaling-autoscalinggroup-launchtemplateoverrides-instancetype
            '''
            result = self._values.get("instance_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def launch_template_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty"]]:
            '''Provides a launch template for the specified instance type or set of instance requirements.

            For example, some instance types might require a launch template with a different AMI. If not provided, Amazon EC2 Auto Scaling uses the launch template that's specified in the ``LaunchTemplate`` definition. For more information, see `Specifying a different launch template for an instance type <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-mixed-instances-groups-launch-template-overrides.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

            You can specify up to 20 launch templates per Auto Scaling group. The launch templates specified in the overrides and in the ``LaunchTemplate`` definition count towards this limit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplateoverrides.html#cfn-autoscaling-autoscalinggroup-launchtemplateoverrides-launchtemplatespecification
            '''
            result = self._values.get("launch_template_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty"]], result)

        @builtins.property
        def weighted_capacity(self) -> typing.Optional[builtins.str]:
            '''If you provide a list of instance types to use, you can specify the number of capacity units provided by each instance type in terms of virtual CPUs, memory, storage, throughput, or other relative performance characteristic.

            When a Spot or On-Demand Instance is launched, the capacity units count toward the desired capacity. Amazon EC2 Auto Scaling launches instances until the desired capacity is totally fulfilled, even if this results in an overage. For example, if there are two units remaining to fulfill capacity, and Amazon EC2 Auto Scaling can only launch an instance with a ``WeightedCapacity`` of five units, the instance is launched, and the desired capacity is exceeded by three units. For more information, see `Configure instance weighting for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-mixed-instances-groups-instance-weighting.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . Value must be in the range of 1-999.

            If you specify a value for ``WeightedCapacity`` for one instance type, you must specify a value for ``WeightedCapacity`` for all of them.
            .. epigraph::

               Every Auto Scaling group has three size parameters ( ``DesiredCapacity`` , ``MaxSize`` , and ``MinSize`` ). Usually, you set these sizes based on a specific number of instances. However, if you configure a mixed instances policy that defines weights for the instance types, you must specify these sizes with the same units that you use for weighting instances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplateoverrides.html#cfn-autoscaling-autoscalinggroup-launchtemplateoverrides-weightedcapacity
            '''
            result = self._values.get("weighted_capacity")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LaunchTemplateOverridesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "launch_template_specification": "launchTemplateSpecification",
            "overrides": "overrides",
        },
    )
    class LaunchTemplateProperty:
        def __init__(
            self,
            *,
            launch_template_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.LaunchTemplateOverridesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Use this structure to specify the launch templates and instance types (overrides) for a mixed instances policy.

            ``LaunchTemplate`` is a property of the `AWS::AutoScaling::AutoScalingGroup MixedInstancesPolicy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-mixedinstancespolicy.html>`_ property type.

            :param launch_template_specification: The launch template.
            :param overrides: Any properties that you specify override the same properties in the launch template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                launch_template_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateProperty(
                    launch_template_specification=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty(
                        launch_template_id="launchTemplateId",
                        launch_template_name="launchTemplateName",
                        version="version"
                    ),
                    overrides=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateOverridesProperty(
                        instance_requirements=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.InstanceRequirementsProperty(
                            accelerator_count=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.AcceleratorCountRequestProperty(
                                max=123,
                                min=123
                            ),
                            accelerator_manufacturers=["acceleratorManufacturers"],
                            accelerator_names=["acceleratorNames"],
                            accelerator_total_memory_mi_b=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.AcceleratorTotalMemoryMiBRequestProperty(
                                max=123,
                                min=123
                            ),
                            accelerator_types=["acceleratorTypes"],
                            allowed_instance_types=["allowedInstanceTypes"],
                            bare_metal="bareMetal",
                            baseline_ebs_bandwidth_mbps=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.BaselineEbsBandwidthMbpsRequestProperty(
                                max=123,
                                min=123
                            ),
                            baseline_performance_factors=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.BaselinePerformanceFactorsRequestProperty(
                                cpu=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.CpuPerformanceFactorRequestProperty(
                                    references=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.PerformanceFactorReferenceRequestProperty(
                                        instance_family="instanceFamily"
                                    )]
                                )
                            ),
                            burstable_performance="burstablePerformance",
                            cpu_manufacturers=["cpuManufacturers"],
                            excluded_instance_types=["excludedInstanceTypes"],
                            instance_generations=["instanceGenerations"],
                            local_storage="localStorage",
                            local_storage_types=["localStorageTypes"],
                            max_spot_price_as_percentage_of_optimal_on_demand_price=123,
                            memory_gi_bPer_vCpu=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.MemoryGiBPerVCpuRequestProperty(
                                max=123,
                                min=123
                            ),
                            memory_mi_b=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.MemoryMiBRequestProperty(
                                max=123,
                                min=123
                            ),
                            network_bandwidth_gbps=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.NetworkBandwidthGbpsRequestProperty(
                                max=123,
                                min=123
                            ),
                            network_interface_count=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.NetworkInterfaceCountRequestProperty(
                                max=123,
                                min=123
                            ),
                            on_demand_max_price_percentage_over_lowest_price=123,
                            require_hibernate_support=False,
                            spot_max_price_percentage_over_lowest_price=123,
                            total_local_storage_gb=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.TotalLocalStorageGBRequestProperty(
                                max=123,
                                min=123
                            ),
                            v_cpu_count=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.VCpuCountRequestProperty(
                                max=123,
                                min=123
                            )
                        ),
                        instance_type="instanceType",
                        launch_template_specification=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty(
                            launch_template_id="launchTemplateId",
                            launch_template_name="launchTemplateName",
                            version="version"
                        ),
                        weighted_capacity="weightedCapacity"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__971215471d62705af8d0d24e6d28edf1e817027a62dc14f25f1034f1994e96c2)
                check_type(argname="argument launch_template_specification", value=launch_template_specification, expected_type=type_hints["launch_template_specification"])
                check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if launch_template_specification is not None:
                self._values["launch_template_specification"] = launch_template_specification
            if overrides is not None:
                self._values["overrides"] = overrides

        @builtins.property
        def launch_template_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty"]]:
            '''The launch template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplate.html#cfn-autoscaling-autoscalinggroup-launchtemplate-launchtemplatespecification
            '''
            result = self._values.get("launch_template_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty"]], result)

        @builtins.property
        def overrides(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.LaunchTemplateOverridesProperty"]]]]:
            '''Any properties that you specify override the same properties in the launch template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplate.html#cfn-autoscaling-autoscalinggroup-launchtemplate-overrides
            '''
            result = self._values.get("overrides")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.LaunchTemplateOverridesProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LaunchTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "launch_template_id": "launchTemplateId",
            "launch_template_name": "launchTemplateName",
            "version": "version",
        },
    )
    class LaunchTemplateSpecificationProperty:
        def __init__(
            self,
            *,
            launch_template_id: typing.Optional[builtins.str] = None,
            launch_template_name: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a launch template to use when provisioning EC2 instances for an Auto Scaling group.

            You must specify the following:

            - The ID or the name of the launch template, but not both.
            - The version of the launch template.

            ``LaunchTemplateSpecification`` is property of the `AWS::AutoScaling::AutoScalingGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html>`_ resource. It is also a property of the `AWS::AutoScaling::AutoScalingGroup LaunchTemplate <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplate.html>`_ and `AWS::AutoScaling::AutoScalingGroup LaunchTemplateOverrides <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplateoverrides.html>`_ property types.

            For information about creating a launch template, see `AWS::EC2::LaunchTemplate <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-launchtemplate.html>`_ and `Create a launch template for an Auto Scaling group <https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-launch-template.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

            For examples of launch templates, see `Create launch templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-ec2-launch-templates.html>`_ .

            :param launch_template_id: The ID of the launch template. You must specify the ``LaunchTemplateID`` or the ``LaunchTemplateName`` , but not both.
            :param launch_template_name: The name of the launch template. You must specify the ``LaunchTemplateName`` or the ``LaunchTemplateID`` , but not both.
            :param version: The version number of the launch template. Specifying ``$Latest`` or ``$Default`` for the template version number is not supported. However, you can specify ``LatestVersionNumber`` or ``DefaultVersionNumber`` using the ``Fn::GetAtt`` intrinsic function. For more information, see `Fn::GetAtt <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html>`_ . .. epigraph:: For an example of using the ``Fn::GetAtt`` function, see the `Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#aws-resource-autoscaling-autoscalinggroup--examples>`_ section of the ``AWS::AutoScaling::AutoScalingGroup`` resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplatespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                launch_template_specification_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty(
                    launch_template_id="launchTemplateId",
                    launch_template_name="launchTemplateName",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__979ed91df33924ef97dd12ca874a081a977faa5426834d4e6a8ab245c0dbfa54)
                check_type(argname="argument launch_template_id", value=launch_template_id, expected_type=type_hints["launch_template_id"])
                check_type(argname="argument launch_template_name", value=launch_template_name, expected_type=type_hints["launch_template_name"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if launch_template_id is not None:
                self._values["launch_template_id"] = launch_template_id
            if launch_template_name is not None:
                self._values["launch_template_name"] = launch_template_name
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def launch_template_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the launch template.

            You must specify the ``LaunchTemplateID`` or the ``LaunchTemplateName`` , but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplatespecification.html#cfn-autoscaling-autoscalinggroup-launchtemplatespecification-launchtemplateid
            '''
            result = self._values.get("launch_template_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def launch_template_name(self) -> typing.Optional[builtins.str]:
            '''The name of the launch template.

            You must specify the ``LaunchTemplateName`` or the ``LaunchTemplateID`` , but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplatespecification.html#cfn-autoscaling-autoscalinggroup-launchtemplatespecification-launchtemplatename
            '''
            result = self._values.get("launch_template_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The version number of the launch template.

            Specifying ``$Latest`` or ``$Default`` for the template version number is not supported. However, you can specify ``LatestVersionNumber`` or ``DefaultVersionNumber`` using the ``Fn::GetAtt`` intrinsic function. For more information, see `Fn::GetAtt <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html>`_ .
            .. epigraph::

               For an example of using the ``Fn::GetAtt`` function, see the `Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#aws-resource-autoscaling-autoscalinggroup--examples>`_ section of the ``AWS::AutoScaling::AutoScalingGroup`` resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplatespecification.html#cfn-autoscaling-autoscalinggroup-launchtemplatespecification-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LaunchTemplateSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.LifecycleHookSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_result": "defaultResult",
            "heartbeat_timeout": "heartbeatTimeout",
            "lifecycle_hook_name": "lifecycleHookName",
            "lifecycle_transition": "lifecycleTransition",
            "notification_metadata": "notificationMetadata",
            "notification_target_arn": "notificationTargetArn",
            "role_arn": "roleArn",
        },
    )
    class LifecycleHookSpecificationProperty:
        def __init__(
            self,
            *,
            default_result: typing.Optional[builtins.str] = None,
            heartbeat_timeout: typing.Optional[jsii.Number] = None,
            lifecycle_hook_name: typing.Optional[builtins.str] = None,
            lifecycle_transition: typing.Optional[builtins.str] = None,
            notification_metadata: typing.Optional[builtins.str] = None,
            notification_target_arn: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``LifecycleHookSpecification`` specifies a lifecycle hook for the ``LifecycleHookSpecificationList`` property of the `AWS::AutoScaling::AutoScalingGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html>`_ resource. A lifecycle hook specifies actions to perform when Amazon EC2 Auto Scaling launches or terminates instances.

            For more information, see `Amazon EC2 Auto Scaling lifecycle hooks <https://docs.aws.amazon.com/autoscaling/ec2/userguide/lifecycle-hooks.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . You can find a sample template snippet in the `Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#aws-resource-as-lifecyclehook--examples>`_ section of the ``AWS::AutoScaling::LifecycleHook`` resource.

            :param default_result: The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs. The default value is ``ABANDON`` . Valid values: ``CONTINUE`` | ``ABANDON``
            :param heartbeat_timeout: The maximum time, in seconds, that can elapse before the lifecycle hook times out. The range is from ``30`` to ``7200`` seconds. The default value is ``3600`` seconds (1 hour).
            :param lifecycle_hook_name: The name of the lifecycle hook.
            :param lifecycle_transition: The lifecycle transition. For Auto Scaling groups, there are two major lifecycle transitions. - To create a lifecycle hook for scale-out events, specify ``autoscaling:EC2_INSTANCE_LAUNCHING`` . - To create a lifecycle hook for scale-in events, specify ``autoscaling:EC2_INSTANCE_TERMINATING`` .
            :param notification_metadata: Additional information that you want to include any time Amazon EC2 Auto Scaling sends a message to the notification target.
            :param notification_target_arn: The Amazon Resource Name (ARN) of the notification target that Amazon EC2 Auto Scaling sends notifications to when an instance is in a wait state for the lifecycle hook. You can specify an Amazon SNS topic or an Amazon SQS queue.
            :param role_arn: The ARN of the IAM role that allows the Auto Scaling group to publish to the specified notification target. For information about creating this role, see `Prepare to add a lifecycle hook to your Auto Scaling group <https://docs.aws.amazon.com/autoscaling/ec2/userguide/prepare-for-lifecycle-notifications.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . Valid only if the notification target is an Amazon SNS topic or an Amazon SQS queue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                lifecycle_hook_specification_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LifecycleHookSpecificationProperty(
                    default_result="defaultResult",
                    heartbeat_timeout=123,
                    lifecycle_hook_name="lifecycleHookName",
                    lifecycle_transition="lifecycleTransition",
                    notification_metadata="notificationMetadata",
                    notification_target_arn="notificationTargetArn",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7e52167b1ca0ea0d079768dad70bd5be7356fb1fcc18337014875e26137b04cf)
                check_type(argname="argument default_result", value=default_result, expected_type=type_hints["default_result"])
                check_type(argname="argument heartbeat_timeout", value=heartbeat_timeout, expected_type=type_hints["heartbeat_timeout"])
                check_type(argname="argument lifecycle_hook_name", value=lifecycle_hook_name, expected_type=type_hints["lifecycle_hook_name"])
                check_type(argname="argument lifecycle_transition", value=lifecycle_transition, expected_type=type_hints["lifecycle_transition"])
                check_type(argname="argument notification_metadata", value=notification_metadata, expected_type=type_hints["notification_metadata"])
                check_type(argname="argument notification_target_arn", value=notification_target_arn, expected_type=type_hints["notification_target_arn"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_result is not None:
                self._values["default_result"] = default_result
            if heartbeat_timeout is not None:
                self._values["heartbeat_timeout"] = heartbeat_timeout
            if lifecycle_hook_name is not None:
                self._values["lifecycle_hook_name"] = lifecycle_hook_name
            if lifecycle_transition is not None:
                self._values["lifecycle_transition"] = lifecycle_transition
            if notification_metadata is not None:
                self._values["notification_metadata"] = notification_metadata
            if notification_target_arn is not None:
                self._values["notification_target_arn"] = notification_target_arn
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def default_result(self) -> typing.Optional[builtins.str]:
            '''The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs.

            The default value is ``ABANDON`` .

            Valid values: ``CONTINUE`` | ``ABANDON``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-defaultresult
            '''
            result = self._values.get("default_result")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def heartbeat_timeout(self) -> typing.Optional[jsii.Number]:
            '''The maximum time, in seconds, that can elapse before the lifecycle hook times out.

            The range is from ``30`` to ``7200`` seconds. The default value is ``3600`` seconds (1 hour).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-heartbeattimeout
            '''
            result = self._values.get("heartbeat_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def lifecycle_hook_name(self) -> typing.Optional[builtins.str]:
            '''The name of the lifecycle hook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-lifecyclehookname
            '''
            result = self._values.get("lifecycle_hook_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def lifecycle_transition(self) -> typing.Optional[builtins.str]:
            '''The lifecycle transition. For Auto Scaling groups, there are two major lifecycle transitions.

            - To create a lifecycle hook for scale-out events, specify ``autoscaling:EC2_INSTANCE_LAUNCHING`` .
            - To create a lifecycle hook for scale-in events, specify ``autoscaling:EC2_INSTANCE_TERMINATING`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-lifecycletransition
            '''
            result = self._values.get("lifecycle_transition")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def notification_metadata(self) -> typing.Optional[builtins.str]:
            '''Additional information that you want to include any time Amazon EC2 Auto Scaling sends a message to the notification target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-notificationmetadata
            '''
            result = self._values.get("notification_metadata")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def notification_target_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the notification target that Amazon EC2 Auto Scaling sends notifications to when an instance is in a wait state for the lifecycle hook.

            You can specify an Amazon SNS topic or an Amazon SQS queue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-notificationtargetarn
            '''
            result = self._values.get("notification_target_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM role that allows the Auto Scaling group to publish to the specified notification target.

            For information about creating this role, see `Prepare to add a lifecycle hook to your Auto Scaling group <https://docs.aws.amazon.com/autoscaling/ec2/userguide/prepare-for-lifecycle-notifications.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

            Valid only if the notification target is an Amazon SNS topic or an Amazon SQS queue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LifecycleHookSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.MemoryGiBPerVCpuRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"max": "max", "min": "min"},
    )
    class MemoryGiBPerVCpuRequestProperty:
        def __init__(
            self,
            *,
            max: typing.Optional[jsii.Number] = None,
            min: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``MemoryGiBPerVCpuRequest`` is a property of the ``InstanceRequirements`` property of the `AWS::AutoScaling::AutoScalingGroup LaunchTemplateOverrides <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplateoverrides.html>`_ property type that describes the minimum and maximum amount of memory per vCPU for an instance type, in GiB.

            :param max: The memory maximum in GiB.
            :param min: The memory minimum in GiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-memorygibpervcpurequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                memory_gi_bPer_vCpu_request_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.MemoryGiBPerVCpuRequestProperty(
                    max=123,
                    min=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6327a360dc7cd47b7b5fe16775df21d0e16fcfc30de9811b6fc5e5b27c470c32)
                check_type(argname="argument max", value=max, expected_type=type_hints["max"])
                check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max is not None:
                self._values["max"] = max
            if min is not None:
                self._values["min"] = min

        @builtins.property
        def max(self) -> typing.Optional[jsii.Number]:
            '''The memory maximum in GiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-memorygibpervcpurequest.html#cfn-autoscaling-autoscalinggroup-memorygibpervcpurequest-max
            '''
            result = self._values.get("max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min(self) -> typing.Optional[jsii.Number]:
            '''The memory minimum in GiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-memorygibpervcpurequest.html#cfn-autoscaling-autoscalinggroup-memorygibpervcpurequest-min
            '''
            result = self._values.get("min")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MemoryGiBPerVCpuRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.MemoryMiBRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"max": "max", "min": "min"},
    )
    class MemoryMiBRequestProperty:
        def __init__(
            self,
            *,
            max: typing.Optional[jsii.Number] = None,
            min: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``MemoryMiBRequest`` is a property of the ``InstanceRequirements`` property of the `AWS::AutoScaling::AutoScalingGroup LaunchTemplateOverrides <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplateoverrides.html>`_ property type that describes the minimum and maximum instance memory size for an instance type, in MiB.

            :param max: The memory maximum in MiB.
            :param min: The memory minimum in MiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-memorymibrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                memory_mi_bRequest_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.MemoryMiBRequestProperty(
                    max=123,
                    min=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9ecf317383c2e29a0a7431ed73953a3a67f304b9b9c2cc34ba84546919a35b29)
                check_type(argname="argument max", value=max, expected_type=type_hints["max"])
                check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max is not None:
                self._values["max"] = max
            if min is not None:
                self._values["min"] = min

        @builtins.property
        def max(self) -> typing.Optional[jsii.Number]:
            '''The memory maximum in MiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-memorymibrequest.html#cfn-autoscaling-autoscalinggroup-memorymibrequest-max
            '''
            result = self._values.get("max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min(self) -> typing.Optional[jsii.Number]:
            '''The memory minimum in MiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-memorymibrequest.html#cfn-autoscaling-autoscalinggroup-memorymibrequest-min
            '''
            result = self._values.get("min")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MemoryMiBRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.MetricsCollectionProperty",
        jsii_struct_bases=[],
        name_mapping={"granularity": "granularity", "metrics": "metrics"},
    )
    class MetricsCollectionProperty:
        def __init__(
            self,
            *,
            granularity: typing.Optional[builtins.str] = None,
            metrics: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''``MetricsCollection`` is a property of the `AWS::AutoScaling::AutoScalingGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html>`_ resource that describes the group metrics that an Amazon EC2 Auto Scaling group sends to Amazon CloudWatch. These metrics describe the group rather than any of its instances.

            For more information, see `Monitor CloudWatch metrics for your Auto Scaling groups and instances <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-instance-monitoring.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . You can find a sample template snippet in the `Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#aws-resource-autoscaling-autoscalinggroup--examples>`_ section of the ``AWS::AutoScaling::AutoScalingGroup`` resource.

            :param granularity: The frequency at which Amazon EC2 Auto Scaling sends aggregated data to CloudWatch. The only valid value is ``1Minute`` .
            :param metrics: Identifies the metrics to enable. You can specify one or more of the following metrics: - ``GroupMinSize`` - ``GroupMaxSize`` - ``GroupDesiredCapacity`` - ``GroupInServiceInstances`` - ``GroupPendingInstances`` - ``GroupStandbyInstances`` - ``GroupTerminatingInstances`` - ``GroupTotalInstances`` - ``GroupInServiceCapacity`` - ``GroupPendingCapacity`` - ``GroupStandbyCapacity`` - ``GroupTerminatingCapacity`` - ``GroupTotalCapacity`` - ``WarmPoolDesiredCapacity`` - ``WarmPoolWarmedCapacity`` - ``WarmPoolPendingCapacity`` - ``WarmPoolTerminatingCapacity`` - ``WarmPoolTotalCapacity`` - ``GroupAndWarmPoolDesiredCapacity`` - ``GroupAndWarmPoolTotalCapacity`` If you specify ``Granularity`` and don't specify any metrics, all metrics are enabled. For more information, see `Amazon CloudWatch metrics for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-metrics.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-metricscollection.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                metrics_collection_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.MetricsCollectionProperty(
                    granularity="granularity",
                    metrics=["metrics"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ae69aee764a4c7a5c91fb540b9286a2ce22e88b0b4ce4817a4570d515f37152e)
                check_type(argname="argument granularity", value=granularity, expected_type=type_hints["granularity"])
                check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if granularity is not None:
                self._values["granularity"] = granularity
            if metrics is not None:
                self._values["metrics"] = metrics

        @builtins.property
        def granularity(self) -> typing.Optional[builtins.str]:
            '''The frequency at which Amazon EC2 Auto Scaling sends aggregated data to CloudWatch.

            The only valid value is ``1Minute`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-metricscollection.html#cfn-autoscaling-autoscalinggroup-metricscollection-granularity
            '''
            result = self._values.get("granularity")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metrics(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Identifies the metrics to enable.

            You can specify one or more of the following metrics:

            - ``GroupMinSize``
            - ``GroupMaxSize``
            - ``GroupDesiredCapacity``
            - ``GroupInServiceInstances``
            - ``GroupPendingInstances``
            - ``GroupStandbyInstances``
            - ``GroupTerminatingInstances``
            - ``GroupTotalInstances``
            - ``GroupInServiceCapacity``
            - ``GroupPendingCapacity``
            - ``GroupStandbyCapacity``
            - ``GroupTerminatingCapacity``
            - ``GroupTotalCapacity``
            - ``WarmPoolDesiredCapacity``
            - ``WarmPoolWarmedCapacity``
            - ``WarmPoolPendingCapacity``
            - ``WarmPoolTerminatingCapacity``
            - ``WarmPoolTotalCapacity``
            - ``GroupAndWarmPoolDesiredCapacity``
            - ``GroupAndWarmPoolTotalCapacity``

            If you specify ``Granularity`` and don't specify any metrics, all metrics are enabled.

            For more information, see `Amazon CloudWatch metrics for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-metrics.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-metricscollection.html#cfn-autoscaling-autoscalinggroup-metricscollection-metrics
            '''
            result = self._values.get("metrics")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricsCollectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.MixedInstancesPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instances_distribution": "instancesDistribution",
            "launch_template": "launchTemplate",
        },
    )
    class MixedInstancesPolicyProperty:
        def __init__(
            self,
            *,
            instances_distribution: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.InstancesDistributionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            launch_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutoScalingGroupPropsMixin.LaunchTemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Use this structure to launch multiple instance types and On-Demand Instances and Spot Instances within a single Auto Scaling group.

            A mixed instances policy contains information that Amazon EC2 Auto Scaling can use to launch instances and help optimize your costs. For more information, see `Auto Scaling groups with multiple instance types and purchase options <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-mixed-instances-groups.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

            You can create a mixed instances policy for new and existing Auto Scaling groups. You must use a launch template to configure the policy. You cannot use a launch configuration.

            There are key differences between Spot Instances and On-Demand Instances:

            - The price for Spot Instances varies based on demand
            - Amazon EC2 can terminate an individual Spot Instance as the availability of, or price for, Spot Instances changes

            When a Spot Instance is terminated, Amazon EC2 Auto Scaling group attempts to launch a replacement instance to maintain the desired capacity for the group.

            ``MixedInstancesPolicy`` is a property of the `AWS::AutoScaling::AutoScalingGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html>`_ resource.

            :param instances_distribution: The instances distribution.
            :param launch_template: One or more launch templates and the instance types (overrides) that are used to launch EC2 instances to fulfill On-Demand and Spot capacities.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-mixedinstancespolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                mixed_instances_policy_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.MixedInstancesPolicyProperty(
                    instances_distribution=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.InstancesDistributionProperty(
                        on_demand_allocation_strategy="onDemandAllocationStrategy",
                        on_demand_base_capacity=123,
                        on_demand_percentage_above_base_capacity=123,
                        spot_allocation_strategy="spotAllocationStrategy",
                        spot_instance_pools=123,
                        spot_max_price="spotMaxPrice"
                    ),
                    launch_template=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateProperty(
                        launch_template_specification=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty(
                            launch_template_id="launchTemplateId",
                            launch_template_name="launchTemplateName",
                            version="version"
                        ),
                        overrides=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateOverridesProperty(
                            instance_requirements=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.InstanceRequirementsProperty(
                                accelerator_count=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.AcceleratorCountRequestProperty(
                                    max=123,
                                    min=123
                                ),
                                accelerator_manufacturers=["acceleratorManufacturers"],
                                accelerator_names=["acceleratorNames"],
                                accelerator_total_memory_mi_b=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.AcceleratorTotalMemoryMiBRequestProperty(
                                    max=123,
                                    min=123
                                ),
                                accelerator_types=["acceleratorTypes"],
                                allowed_instance_types=["allowedInstanceTypes"],
                                bare_metal="bareMetal",
                                baseline_ebs_bandwidth_mbps=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.BaselineEbsBandwidthMbpsRequestProperty(
                                    max=123,
                                    min=123
                                ),
                                baseline_performance_factors=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.BaselinePerformanceFactorsRequestProperty(
                                    cpu=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.CpuPerformanceFactorRequestProperty(
                                        references=[autoscaling_mixins.CfnAutoScalingGroupPropsMixin.PerformanceFactorReferenceRequestProperty(
                                            instance_family="instanceFamily"
                                        )]
                                    )
                                ),
                                burstable_performance="burstablePerformance",
                                cpu_manufacturers=["cpuManufacturers"],
                                excluded_instance_types=["excludedInstanceTypes"],
                                instance_generations=["instanceGenerations"],
                                local_storage="localStorage",
                                local_storage_types=["localStorageTypes"],
                                max_spot_price_as_percentage_of_optimal_on_demand_price=123,
                                memory_gi_bPer_vCpu=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.MemoryGiBPerVCpuRequestProperty(
                                    max=123,
                                    min=123
                                ),
                                memory_mi_b=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.MemoryMiBRequestProperty(
                                    max=123,
                                    min=123
                                ),
                                network_bandwidth_gbps=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.NetworkBandwidthGbpsRequestProperty(
                                    max=123,
                                    min=123
                                ),
                                network_interface_count=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.NetworkInterfaceCountRequestProperty(
                                    max=123,
                                    min=123
                                ),
                                on_demand_max_price_percentage_over_lowest_price=123,
                                require_hibernate_support=False,
                                spot_max_price_percentage_over_lowest_price=123,
                                total_local_storage_gb=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.TotalLocalStorageGBRequestProperty(
                                    max=123,
                                    min=123
                                ),
                                v_cpu_count=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.VCpuCountRequestProperty(
                                    max=123,
                                    min=123
                                )
                            ),
                            instance_type="instanceType",
                            launch_template_specification=autoscaling_mixins.CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty(
                                launch_template_id="launchTemplateId",
                                launch_template_name="launchTemplateName",
                                version="version"
                            ),
                            weighted_capacity="weightedCapacity"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__37fc9065eaf8c38954e699966c0c74352be222946da46bc209661231af2a4d8f)
                check_type(argname="argument instances_distribution", value=instances_distribution, expected_type=type_hints["instances_distribution"])
                check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instances_distribution is not None:
                self._values["instances_distribution"] = instances_distribution
            if launch_template is not None:
                self._values["launch_template"] = launch_template

        @builtins.property
        def instances_distribution(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.InstancesDistributionProperty"]]:
            '''The instances distribution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-mixedinstancespolicy.html#cfn-autoscaling-autoscalinggroup-mixedinstancespolicy-instancesdistribution
            '''
            result = self._values.get("instances_distribution")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.InstancesDistributionProperty"]], result)

        @builtins.property
        def launch_template(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.LaunchTemplateProperty"]]:
            '''One or more launch templates and the instance types (overrides) that are used to launch EC2 instances to fulfill On-Demand and Spot capacities.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-mixedinstancespolicy.html#cfn-autoscaling-autoscalinggroup-mixedinstancespolicy-launchtemplate
            '''
            result = self._values.get("launch_template")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutoScalingGroupPropsMixin.LaunchTemplateProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MixedInstancesPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.NetworkBandwidthGbpsRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"max": "max", "min": "min"},
    )
    class NetworkBandwidthGbpsRequestProperty:
        def __init__(
            self,
            *,
            max: typing.Optional[jsii.Number] = None,
            min: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``NetworkBandwidthGbpsRequest`` is a property of the ``InstanceRequirements`` property of the `AWS::AutoScaling::AutoScalingGroup LaunchTemplateOverrides <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplateoverrides.html>`_ property type that describes the minimum and maximum network bandwidth for an instance type, in Gbps.

            .. epigraph::

               Setting the minimum bandwidth does not guarantee that your instance will achieve the minimum bandwidth. Amazon EC2 will identify instance types that support the specified minimum bandwidth, but the actual bandwidth of your instance might go below the specified minimum at times. For more information, see `Available instance bandwidth <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-network-bandwidth.html#available-instance-bandwidth>`_ in the *Amazon EC2 User Guide for Linux Instances* .

            :param max: The maximum amount of network bandwidth, in gigabits per second (Gbps).
            :param min: The minimum amount of network bandwidth, in gigabits per second (Gbps).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-networkbandwidthgbpsrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                network_bandwidth_gbps_request_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.NetworkBandwidthGbpsRequestProperty(
                    max=123,
                    min=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ca1dce81a2b0bba2e63f9036327e9475489563e7b4234c2d26728f3898005811)
                check_type(argname="argument max", value=max, expected_type=type_hints["max"])
                check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max is not None:
                self._values["max"] = max
            if min is not None:
                self._values["min"] = min

        @builtins.property
        def max(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of network bandwidth, in gigabits per second (Gbps).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-networkbandwidthgbpsrequest.html#cfn-autoscaling-autoscalinggroup-networkbandwidthgbpsrequest-max
            '''
            result = self._values.get("max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min(self) -> typing.Optional[jsii.Number]:
            '''The minimum amount of network bandwidth, in gigabits per second (Gbps).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-networkbandwidthgbpsrequest.html#cfn-autoscaling-autoscalinggroup-networkbandwidthgbpsrequest-min
            '''
            result = self._values.get("min")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkBandwidthGbpsRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.NetworkInterfaceCountRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"max": "max", "min": "min"},
    )
    class NetworkInterfaceCountRequestProperty:
        def __init__(
            self,
            *,
            max: typing.Optional[jsii.Number] = None,
            min: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``NetworkInterfaceCountRequest`` is a property of the ``InstanceRequirements`` property of the `AWS::AutoScaling::AutoScalingGroup LaunchTemplateOverrides <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplateoverrides.html>`_ property type that describes the minimum and maximum number of network interfaces for an instance type.

            :param max: The maximum number of network interfaces.
            :param min: The minimum number of network interfaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-networkinterfacecountrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                network_interface_count_request_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.NetworkInterfaceCountRequestProperty(
                    max=123,
                    min=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__49d4b00eb8cc6db6264ab2c0c332516656ac4ea34227c18b6ceb838450d3f97d)
                check_type(argname="argument max", value=max, expected_type=type_hints["max"])
                check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max is not None:
                self._values["max"] = max
            if min is not None:
                self._values["min"] = min

        @builtins.property
        def max(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of network interfaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-networkinterfacecountrequest.html#cfn-autoscaling-autoscalinggroup-networkinterfacecountrequest-max
            '''
            result = self._values.get("max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min(self) -> typing.Optional[jsii.Number]:
            '''The minimum number of network interfaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-networkinterfacecountrequest.html#cfn-autoscaling-autoscalinggroup-networkinterfacecountrequest-min
            '''
            result = self._values.get("min")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkInterfaceCountRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.NotificationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "notification_types": "notificationTypes",
            "topic_arn": "topicArn",
        },
    )
    class NotificationConfigurationProperty:
        def __init__(
            self,
            *,
            notification_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that specifies an Amazon SNS notification configuration for the ``NotificationConfigurations`` property of the `AWS::AutoScaling::AutoScalingGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html>`_ resource.

            For an example template snippet, see `Configure Amazon EC2 Auto Scaling resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-ec2-auto-scaling.html>`_ .

            For more information, see `Get Amazon SNS notifications when your Auto Scaling group scales <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ASGettingNotifications.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

            :param notification_types: A list of event types that send a notification. Event types can include any of the following types. *Allowed values* : - ``autoscaling:EC2_INSTANCE_LAUNCH`` - ``autoscaling:EC2_INSTANCE_LAUNCH_ERROR`` - ``autoscaling:EC2_INSTANCE_TERMINATE`` - ``autoscaling:EC2_INSTANCE_TERMINATE_ERROR`` - ``autoscaling:TEST_NOTIFICATION``
            :param topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-notificationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                notification_configuration_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.NotificationConfigurationProperty(
                    notification_types=["notificationTypes"],
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__13ef6da868c53097ca2537edb063fe2dfd3b817becc7a1e66d9c37c2e984fd0e)
                check_type(argname="argument notification_types", value=notification_types, expected_type=type_hints["notification_types"])
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if notification_types is not None:
                self._values["notification_types"] = notification_types
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def notification_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of event types that send a notification. Event types can include any of the following types.

            *Allowed values* :

            - ``autoscaling:EC2_INSTANCE_LAUNCH``
            - ``autoscaling:EC2_INSTANCE_LAUNCH_ERROR``
            - ``autoscaling:EC2_INSTANCE_TERMINATE``
            - ``autoscaling:EC2_INSTANCE_TERMINATE_ERROR``
            - ``autoscaling:TEST_NOTIFICATION``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-notificationconfiguration.html#cfn-autoscaling-autoscalinggroup-notificationconfiguration-notificationtypes
            '''
            result = self._values.get("notification_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon SNS topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-notificationconfiguration.html#cfn-autoscaling-autoscalinggroup-notificationconfiguration-topicarn
            '''
            result = self._values.get("topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.PerformanceFactorReferenceRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_family": "instanceFamily"},
    )
    class PerformanceFactorReferenceRequestProperty:
        def __init__(
            self,
            *,
            instance_family: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specify an instance family to use as the baseline reference for CPU performance.

            All instance types that All instance types that match your specified attributes will be compared against the CPU performance of the referenced instance family, regardless of CPU manufacturer or architecture differences.
            .. epigraph::

               Currently only one instance family can be specified in the list.

            :param instance_family: The instance family to use as a baseline reference. .. epigraph:: Make sure that you specify the correct value for the instance family. The instance family is everything before the period (.) in the instance type name. For example, in the instance ``c6i.large`` , the instance family is ``c6i`` , not ``c6`` . For more information, see `Amazon EC2 instance type naming conventions <https://docs.aws.amazon.com/ec2/latest/instancetypes/instance-type-names.html>`_ in *Amazon EC2 Instance Types* . The following instance types are *not supported* for performance protection. - ``c1`` - ``g3| g3s`` - ``hpc7g`` - ``m1| m2`` - ``mac1 | mac2 | mac2-m1ultra | mac2-m2 | mac2-m2pro`` - ``p3dn | p4d | p5`` - ``t1`` - ``u-12tb1 | u-18tb1 | u-24tb1 | u-3tb1 | u-6tb1 | u-9tb1 | u7i-12tb | u7in-16tb | u7in-24tb | u7in-32tb`` If you performance protection by specifying a supported instance family, the returned instance types will exclude the preceding unsupported instance families. If you specify an unsupported instance family as a value for baseline performance, the API returns an empty response.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-performancefactorreferencerequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                performance_factor_reference_request_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.PerformanceFactorReferenceRequestProperty(
                    instance_family="instanceFamily"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7a47b104e04a267ea129b2bbcfd48eb020e525123371472d4aeda16fe55cfe75)
                check_type(argname="argument instance_family", value=instance_family, expected_type=type_hints["instance_family"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_family is not None:
                self._values["instance_family"] = instance_family

        @builtins.property
        def instance_family(self) -> typing.Optional[builtins.str]:
            '''The instance family to use as a baseline reference.

            .. epigraph::

               Make sure that you specify the correct value for the instance family. The instance family is everything before the period (.) in the instance type name. For example, in the instance ``c6i.large`` , the instance family is ``c6i`` , not ``c6`` . For more information, see `Amazon EC2 instance type naming conventions <https://docs.aws.amazon.com/ec2/latest/instancetypes/instance-type-names.html>`_ in *Amazon EC2 Instance Types* .

            The following instance types are *not supported* for performance protection.

            - ``c1``
            - ``g3| g3s``
            - ``hpc7g``
            - ``m1| m2``
            - ``mac1 | mac2 | mac2-m1ultra | mac2-m2 | mac2-m2pro``
            - ``p3dn | p4d | p5``
            - ``t1``
            - ``u-12tb1 | u-18tb1 | u-24tb1 | u-3tb1 | u-6tb1 | u-9tb1 | u7i-12tb | u7in-16tb | u7in-24tb | u7in-32tb``

            If you performance protection by specifying a supported instance family, the returned instance types will exclude the preceding unsupported instance families.

            If you specify an unsupported instance family as a value for baseline performance, the API returns an empty response.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-performancefactorreferencerequest.html#cfn-autoscaling-autoscalinggroup-performancefactorreferencerequest-instancefamily
            '''
            result = self._values.get("instance_family")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PerformanceFactorReferenceRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.TagPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "key": "key",
            "propagate_at_launch": "propagateAtLaunch",
            "value": "value",
        },
    )
    class TagPropertyProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            propagate_at_launch: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that specifies a tag for the ``Tags`` property of `AWS::AutoScaling::AutoScalingGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html>`_ resource.

            For more information, see `Tag Auto Scaling groups and instances <https://docs.aws.amazon.com/autoscaling/ec2/userguide/autoscaling-tagging.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . You can find a sample template snippet in the `Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-autoscalinggroup.html#aws-resource-autoscaling-autoscalinggroup--examples>`_ section of the ``AWS::AutoScaling::AutoScalingGroup`` resource.

            CloudFormation adds the following tags to all Auto Scaling groups and associated instances:

            - aws:cloudformation:stack-name
            - aws:cloudformation:stack-id
            - aws:cloudformation:logical-id

            :param key: The tag key.
            :param propagate_at_launch: Set to ``true`` if you want CloudFormation to copy the tag to EC2 instances that are launched as part of the Auto Scaling group. Set to ``false`` if you want the tag attached only to the Auto Scaling group and not copied to any instances launched as part of the Auto Scaling group.
            :param value: The tag value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-tagproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                tag_property_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.TagPropertyProperty(
                    key="key",
                    propagate_at_launch=False,
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4bab725832f0738fea8da8639a2f7c7a557b63172fa8c1a40c29eb1a8826db7a)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument propagate_at_launch", value=propagate_at_launch, expected_type=type_hints["propagate_at_launch"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if propagate_at_launch is not None:
                self._values["propagate_at_launch"] = propagate_at_launch
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The tag key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-tagproperty.html#cfn-autoscaling-autoscalinggroup-tagproperty-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def propagate_at_launch(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set to ``true`` if you want CloudFormation to copy the tag to EC2 instances that are launched as part of the Auto Scaling group.

            Set to ``false`` if you want the tag attached only to the Auto Scaling group and not copied to any instances launched as part of the Auto Scaling group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-tagproperty.html#cfn-autoscaling-autoscalinggroup-tagproperty-propagateatlaunch
            '''
            result = self._values.get("propagate_at_launch")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The tag value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-tagproperty.html#cfn-autoscaling-autoscalinggroup-tagproperty-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.TotalLocalStorageGBRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"max": "max", "min": "min"},
    )
    class TotalLocalStorageGBRequestProperty:
        def __init__(
            self,
            *,
            max: typing.Optional[jsii.Number] = None,
            min: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``TotalLocalStorageGBRequest`` is a property of the ``InstanceRequirements`` property of the `AWS::AutoScaling::AutoScalingGroup LaunchTemplateOverrides <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplateoverrides.html>`_ property type that describes the minimum and maximum total local storage size for an instance type, in GB.

            :param max: The storage maximum in GB.
            :param min: The storage minimum in GB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-totallocalstoragegbrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                total_local_storage_gBRequest_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.TotalLocalStorageGBRequestProperty(
                    max=123,
                    min=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4b4eb62967665d8c2ddc02ce2fce2c7a5aaa11a17e82c5319d0a620f3793415a)
                check_type(argname="argument max", value=max, expected_type=type_hints["max"])
                check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max is not None:
                self._values["max"] = max
            if min is not None:
                self._values["min"] = min

        @builtins.property
        def max(self) -> typing.Optional[jsii.Number]:
            '''The storage maximum in GB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-totallocalstoragegbrequest.html#cfn-autoscaling-autoscalinggroup-totallocalstoragegbrequest-max
            '''
            result = self._values.get("max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min(self) -> typing.Optional[jsii.Number]:
            '''The storage minimum in GB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-totallocalstoragegbrequest.html#cfn-autoscaling-autoscalinggroup-totallocalstoragegbrequest-min
            '''
            result = self._values.get("min")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TotalLocalStorageGBRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.TrafficSourceIdentifierProperty",
        jsii_struct_bases=[],
        name_mapping={"identifier": "identifier", "type": "type"},
    )
    class TrafficSourceIdentifierProperty:
        def __init__(
            self,
            *,
            identifier: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Identifying information for a traffic source.

            :param identifier: Identifies the traffic source. For Application Load Balancers, Gateway Load Balancers, Network Load Balancers, and VPC Lattice, this will be the Amazon Resource Name (ARN) for a target group in this account and Region. For Classic Load Balancers, this will be the name of the Classic Load Balancer in this account and Region. For example: - Application Load Balancer ARN: ``arn:aws:elasticloadbalancing:us-west-2:123456789012:targetgroup/my-targets/1234567890123456`` - Classic Load Balancer name: ``my-classic-load-balancer`` - VPC Lattice ARN: ``arn:aws:vpc-lattice:us-west-2:123456789012:targetgroup/tg-1234567890123456`` To get the ARN of a target group for a Application Load Balancer, Gateway Load Balancer, or Network Load Balancer, or the name of a Classic Load Balancer, use the Elastic Load Balancing `DescribeTargetGroups <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeTargetGroups.html>`_ and `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html>`_ API operations. To get the ARN of a target group for VPC Lattice, use the VPC Lattice `GetTargetGroup <https://docs.aws.amazon.com/vpc-lattice/latest/APIReference/API_GetTargetGroup.html>`_ API operation.
            :param type: Provides additional context for the value of ``Identifier`` . The following lists the valid values: - ``elb`` if ``Identifier`` is the name of a Classic Load Balancer. - ``elbv2`` if ``Identifier`` is the ARN of an Application Load Balancer, Gateway Load Balancer, or Network Load Balancer target group. - ``vpc-lattice`` if ``Identifier`` is the ARN of a VPC Lattice target group. Required if the identifier is the name of a Classic Load Balancer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-trafficsourceidentifier.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                traffic_source_identifier_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.TrafficSourceIdentifierProperty(
                    identifier="identifier",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c5b8487d1a5f9987076b2ae5a130b6027d44209e3bc8f72b948c3574749c87c5)
                check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if identifier is not None:
                self._values["identifier"] = identifier
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def identifier(self) -> typing.Optional[builtins.str]:
            '''Identifies the traffic source.

            For Application Load Balancers, Gateway Load Balancers, Network Load Balancers, and VPC Lattice, this will be the Amazon Resource Name (ARN) for a target group in this account and Region. For Classic Load Balancers, this will be the name of the Classic Load Balancer in this account and Region.

            For example:

            - Application Load Balancer ARN: ``arn:aws:elasticloadbalancing:us-west-2:123456789012:targetgroup/my-targets/1234567890123456``
            - Classic Load Balancer name: ``my-classic-load-balancer``
            - VPC Lattice ARN: ``arn:aws:vpc-lattice:us-west-2:123456789012:targetgroup/tg-1234567890123456``

            To get the ARN of a target group for a Application Load Balancer, Gateway Load Balancer, or Network Load Balancer, or the name of a Classic Load Balancer, use the Elastic Load Balancing `DescribeTargetGroups <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeTargetGroups.html>`_ and `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html>`_ API operations.

            To get the ARN of a target group for VPC Lattice, use the VPC Lattice `GetTargetGroup <https://docs.aws.amazon.com/vpc-lattice/latest/APIReference/API_GetTargetGroup.html>`_ API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-trafficsourceidentifier.html#cfn-autoscaling-autoscalinggroup-trafficsourceidentifier-identifier
            '''
            result = self._values.get("identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Provides additional context for the value of ``Identifier`` .

            The following lists the valid values:

            - ``elb`` if ``Identifier`` is the name of a Classic Load Balancer.
            - ``elbv2`` if ``Identifier`` is the ARN of an Application Load Balancer, Gateway Load Balancer, or Network Load Balancer target group.
            - ``vpc-lattice`` if ``Identifier`` is the ARN of a VPC Lattice target group.

            Required if the identifier is the name of a Classic Load Balancer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-trafficsourceidentifier.html#cfn-autoscaling-autoscalinggroup-trafficsourceidentifier-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TrafficSourceIdentifierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnAutoScalingGroupPropsMixin.VCpuCountRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"max": "max", "min": "min"},
    )
    class VCpuCountRequestProperty:
        def __init__(
            self,
            *,
            max: typing.Optional[jsii.Number] = None,
            min: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``VCpuCountRequest`` is a property of the ``InstanceRequirements`` property of the `AWS::AutoScaling::AutoScalingGroup LaunchTemplateOverrides <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplateoverrides.html>`_ property type that describes the minimum and maximum number of vCPUs for an instance type.

            :param max: The maximum number of vCPUs.
            :param min: The minimum number of vCPUs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-vcpucountrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                v_cpu_count_request_property = autoscaling_mixins.CfnAutoScalingGroupPropsMixin.VCpuCountRequestProperty(
                    max=123,
                    min=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__46036d5996d93c96f2e87ac4774dbe2574531632440fb3230273e454919ae730)
                check_type(argname="argument max", value=max, expected_type=type_hints["max"])
                check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max is not None:
                self._values["max"] = max
            if min is not None:
                self._values["min"] = min

        @builtins.property
        def max(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of vCPUs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-vcpucountrequest.html#cfn-autoscaling-autoscalinggroup-vcpucountrequest-max
            '''
            result = self._values.get("max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min(self) -> typing.Optional[jsii.Number]:
            '''The minimum number of vCPUs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-vcpucountrequest.html#cfn-autoscaling-autoscalinggroup-vcpucountrequest-min
            '''
            result = self._values.get("min")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VCpuCountRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnLaunchConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "associate_public_ip_address": "associatePublicIpAddress",
        "block_device_mappings": "blockDeviceMappings",
        "classic_link_vpc_id": "classicLinkVpcId",
        "classic_link_vpc_security_groups": "classicLinkVpcSecurityGroups",
        "ebs_optimized": "ebsOptimized",
        "iam_instance_profile": "iamInstanceProfile",
        "image_id": "imageId",
        "instance_id": "instanceId",
        "instance_monitoring": "instanceMonitoring",
        "instance_type": "instanceType",
        "kernel_id": "kernelId",
        "key_name": "keyName",
        "launch_configuration_name": "launchConfigurationName",
        "metadata_options": "metadataOptions",
        "placement_tenancy": "placementTenancy",
        "ram_disk_id": "ramDiskId",
        "security_groups": "securityGroups",
        "spot_price": "spotPrice",
        "user_data": "userData",
    },
)
class CfnLaunchConfigurationMixinProps:
    def __init__(
        self,
        *,
        associate_public_ip_address: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        block_device_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLaunchConfigurationPropsMixin.BlockDeviceMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        classic_link_vpc_id: typing.Optional[builtins.str] = None,
        classic_link_vpc_security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        ebs_optimized: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        iam_instance_profile: typing.Optional[builtins.str] = None,
        image_id: typing.Optional[builtins.str] = None,
        instance_id: typing.Optional[builtins.str] = None,
        instance_monitoring: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        instance_type: typing.Optional[builtins.str] = None,
        kernel_id: typing.Optional[builtins.str] = None,
        key_name: typing.Optional[builtins.str] = None,
        launch_configuration_name: typing.Optional[builtins.str] = None,
        metadata_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLaunchConfigurationPropsMixin.MetadataOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        placement_tenancy: typing.Optional[builtins.str] = None,
        ram_disk_id: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        spot_price: typing.Optional[builtins.str] = None,
        user_data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnLaunchConfigurationPropsMixin.

        :param associate_public_ip_address: Specifies whether to assign a public IPv4 address to the group's instances. If the instance is launched into a default subnet, the default is to assign a public IPv4 address, unless you disabled the option to assign a public IPv4 address on the subnet. If the instance is launched into a nondefault subnet, the default is not to assign a public IPv4 address, unless you enabled the option to assign a public IPv4 address on the subnet. If you specify ``true`` , each instance in the Auto Scaling group receives a unique public IPv4 address. For more information, see `Provide network connectivity for your Auto Scaling instances using Amazon VPC <https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-in-vpc.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . If you specify this property, you must specify at least one subnet for ``VPCZoneIdentifier`` when you create your group.
        :param block_device_mappings: The block device mapping entries that define the block devices to attach to the instances at launch. By default, the block devices specified in the block device mapping for the AMI are used. For more information, see `Block device mappings <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-device-mapping-concepts.html>`_ in the *Amazon EC2 User Guide* .
        :param classic_link_vpc_id: Available for backward compatibility.
        :param classic_link_vpc_security_groups: Available for backward compatibility.
        :param ebs_optimized: Specifies whether the launch configuration is optimized for EBS I/O ( ``true`` ) or not ( ``false`` ). The optimization provides dedicated throughput to Amazon EBS and an optimized configuration stack to provide optimal I/O performance. This optimization is not available with all instance types. Additional fees are incurred when you enable EBS optimization for an instance type that is not EBS-optimized by default. For more information, see `Amazon EBS-optimized instances <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-optimized.html>`_ in the *Amazon EC2 User Guide* . The default value is ``false`` .
        :param iam_instance_profile: The name or the Amazon Resource Name (ARN) of the instance profile associated with the IAM role for the instance. The instance profile contains the IAM role. For more information, see `IAM role for applications that run on Amazon EC2 instances <https://docs.aws.amazon.com/autoscaling/ec2/userguide/us-iam-role.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .
        :param image_id: The ID of the Amazon Machine Image (AMI) that was assigned during registration. For more information, see `Find a Linux AMI <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/finding-an-ami.html>`_ in the *Amazon EC2 User Guide* . If you specify ``InstanceId`` , an ``ImageId`` is not required.
        :param instance_id: The ID of the Amazon EC2 instance to use to create the launch configuration. When you use an instance to create a launch configuration, all properties are derived from the instance with the exception of ``BlockDeviceMapping`` and ``AssociatePublicIpAddress`` . You can override any properties from the instance by specifying them in the launch configuration.
        :param instance_monitoring: Controls whether instances in this group are launched with detailed ( ``true`` ) or basic ( ``false`` ) monitoring. The default value is ``true`` (enabled). .. epigraph:: When detailed monitoring is enabled, Amazon CloudWatch generates metrics every minute and your account is charged a fee. When you disable detailed monitoring, CloudWatch generates metrics every 5 minutes. For more information, see `Configure monitoring for Auto Scaling instances <https://docs.aws.amazon.com/autoscaling/latest/userguide/enable-as-instance-metrics.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .
        :param instance_type: Specifies the instance type of the EC2 instance. For information about available instance types, see `Available instance types <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html#AvailableInstanceTypes>`_ in the *Amazon EC2 User Guide* . If you specify ``InstanceId`` , an ``InstanceType`` is not required.
        :param kernel_id: The ID of the kernel associated with the AMI. .. epigraph:: We recommend that you use PV-GRUB instead of kernels and RAM disks. For more information, see `User provided kernels <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/UserProvidedKernels.html>`_ in the *Amazon EC2 User Guide* .
        :param key_name: The name of the key pair. For more information, see `Amazon EC2 key pairs and Amazon EC2 instances <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html>`_ in the *Amazon EC2 User Guide* .
        :param launch_configuration_name: The name of the launch configuration. This name must be unique per Region per account.
        :param metadata_options: The metadata options for the instances. For more information, see `Configure the instance metadata options <https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-launch-config.html#launch-configurations-imds>`_ in the *Amazon EC2 Auto Scaling User Guide* .
        :param placement_tenancy: The tenancy of the instance, either ``default`` or ``dedicated`` . An instance with ``dedicated`` tenancy runs on isolated, single-tenant hardware and can only be launched into a VPC. To launch dedicated instances into a shared tenancy VPC (a VPC with the instance placement tenancy attribute set to ``default`` ), you must set the value of this property to ``dedicated`` . If you specify ``PlacementTenancy`` , you must specify at least one subnet for ``VPCZoneIdentifier`` when you create your group. Valid values: ``default`` | ``dedicated``
        :param ram_disk_id: The ID of the RAM disk to select. .. epigraph:: We recommend that you use PV-GRUB instead of kernels and RAM disks. For more information, see `User provided kernels <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/UserProvidedKernels.html>`_ in the *Amazon EC2 User Guide* .
        :param security_groups: A list that contains the security groups to assign to the instances in the Auto Scaling group. The list can contain both the IDs of existing security groups and references to `SecurityGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html>`_ resources created in the template. For more information, see `Control traffic to resources using security groups <https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_SecurityGroups.html>`_ in the *Amazon Virtual Private Cloud User Guide* .
        :param spot_price: The maximum hourly price to be paid for any Spot Instance launched to fulfill the request. Spot Instances are launched when the price you specify exceeds the current Spot price. For more information, see `Request Spot Instances for fault-tolerant and flexible applications <https://docs.aws.amazon.com/autoscaling/ec2/userguide/launch-template-spot-instances.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . Valid Range: Minimum value of 0.001 .. epigraph:: When you change your maximum price by creating a new launch configuration, running instances will continue to run as long as the maximum price for those running instances is higher than the current Spot price.
        :param user_data: The Base64-encoded user data to make available to the launched EC2 instances. For more information, see `Instance metadata and user data <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html>`_ in the *Amazon EC2 User Guide for Linux Instances* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
            
            cfn_launch_configuration_mixin_props = autoscaling_mixins.CfnLaunchConfigurationMixinProps(
                associate_public_ip_address=False,
                block_device_mappings=[autoscaling_mixins.CfnLaunchConfigurationPropsMixin.BlockDeviceMappingProperty(
                    device_name="deviceName",
                    ebs=autoscaling_mixins.CfnLaunchConfigurationPropsMixin.BlockDeviceProperty(
                        delete_on_termination=False,
                        encrypted=False,
                        iops=123,
                        snapshot_id="snapshotId",
                        throughput=123,
                        volume_size=123,
                        volume_type="volumeType"
                    ),
                    no_device=False,
                    virtual_name="virtualName"
                )],
                classic_link_vpc_id="classicLinkVpcId",
                classic_link_vpc_security_groups=["classicLinkVpcSecurityGroups"],
                ebs_optimized=False,
                iam_instance_profile="iamInstanceProfile",
                image_id="imageId",
                instance_id="instanceId",
                instance_monitoring=False,
                instance_type="instanceType",
                kernel_id="kernelId",
                key_name="keyName",
                launch_configuration_name="launchConfigurationName",
                metadata_options=autoscaling_mixins.CfnLaunchConfigurationPropsMixin.MetadataOptionsProperty(
                    http_endpoint="httpEndpoint",
                    http_put_response_hop_limit=123,
                    http_tokens="httpTokens"
                ),
                placement_tenancy="placementTenancy",
                ram_disk_id="ramDiskId",
                security_groups=["securityGroups"],
                spot_price="spotPrice",
                user_data="userData"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26638ba4aec28c99d6953d709e4c72649214324e6ded32772df26f94ce93dd5a)
            check_type(argname="argument associate_public_ip_address", value=associate_public_ip_address, expected_type=type_hints["associate_public_ip_address"])
            check_type(argname="argument block_device_mappings", value=block_device_mappings, expected_type=type_hints["block_device_mappings"])
            check_type(argname="argument classic_link_vpc_id", value=classic_link_vpc_id, expected_type=type_hints["classic_link_vpc_id"])
            check_type(argname="argument classic_link_vpc_security_groups", value=classic_link_vpc_security_groups, expected_type=type_hints["classic_link_vpc_security_groups"])
            check_type(argname="argument ebs_optimized", value=ebs_optimized, expected_type=type_hints["ebs_optimized"])
            check_type(argname="argument iam_instance_profile", value=iam_instance_profile, expected_type=type_hints["iam_instance_profile"])
            check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument instance_monitoring", value=instance_monitoring, expected_type=type_hints["instance_monitoring"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument kernel_id", value=kernel_id, expected_type=type_hints["kernel_id"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument launch_configuration_name", value=launch_configuration_name, expected_type=type_hints["launch_configuration_name"])
            check_type(argname="argument metadata_options", value=metadata_options, expected_type=type_hints["metadata_options"])
            check_type(argname="argument placement_tenancy", value=placement_tenancy, expected_type=type_hints["placement_tenancy"])
            check_type(argname="argument ram_disk_id", value=ram_disk_id, expected_type=type_hints["ram_disk_id"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument spot_price", value=spot_price, expected_type=type_hints["spot_price"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if associate_public_ip_address is not None:
            self._values["associate_public_ip_address"] = associate_public_ip_address
        if block_device_mappings is not None:
            self._values["block_device_mappings"] = block_device_mappings
        if classic_link_vpc_id is not None:
            self._values["classic_link_vpc_id"] = classic_link_vpc_id
        if classic_link_vpc_security_groups is not None:
            self._values["classic_link_vpc_security_groups"] = classic_link_vpc_security_groups
        if ebs_optimized is not None:
            self._values["ebs_optimized"] = ebs_optimized
        if iam_instance_profile is not None:
            self._values["iam_instance_profile"] = iam_instance_profile
        if image_id is not None:
            self._values["image_id"] = image_id
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if instance_monitoring is not None:
            self._values["instance_monitoring"] = instance_monitoring
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if kernel_id is not None:
            self._values["kernel_id"] = kernel_id
        if key_name is not None:
            self._values["key_name"] = key_name
        if launch_configuration_name is not None:
            self._values["launch_configuration_name"] = launch_configuration_name
        if metadata_options is not None:
            self._values["metadata_options"] = metadata_options
        if placement_tenancy is not None:
            self._values["placement_tenancy"] = placement_tenancy
        if ram_disk_id is not None:
            self._values["ram_disk_id"] = ram_disk_id
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if spot_price is not None:
            self._values["spot_price"] = spot_price
        if user_data is not None:
            self._values["user_data"] = user_data

    @builtins.property
    def associate_public_ip_address(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to assign a public IPv4 address to the group's instances.

        If the instance is launched into a default subnet, the default is to assign a public IPv4 address, unless you disabled the option to assign a public IPv4 address on the subnet. If the instance is launched into a nondefault subnet, the default is not to assign a public IPv4 address, unless you enabled the option to assign a public IPv4 address on the subnet.

        If you specify ``true`` , each instance in the Auto Scaling group receives a unique public IPv4 address. For more information, see `Provide network connectivity for your Auto Scaling instances using Amazon VPC <https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-in-vpc.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        If you specify this property, you must specify at least one subnet for ``VPCZoneIdentifier`` when you create your group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html#cfn-autoscaling-launchconfiguration-associatepublicipaddress
        '''
        result = self._values.get("associate_public_ip_address")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def block_device_mappings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchConfigurationPropsMixin.BlockDeviceMappingProperty"]]]]:
        '''The block device mapping entries that define the block devices to attach to the instances at launch.

        By default, the block devices specified in the block device mapping for the AMI are used. For more information, see `Block device mappings <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-device-mapping-concepts.html>`_ in the *Amazon EC2 User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html#cfn-autoscaling-launchconfiguration-blockdevicemappings
        '''
        result = self._values.get("block_device_mappings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchConfigurationPropsMixin.BlockDeviceMappingProperty"]]]], result)

    @builtins.property
    def classic_link_vpc_id(self) -> typing.Optional[builtins.str]:
        '''Available for backward compatibility.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html#cfn-autoscaling-launchconfiguration-classiclinkvpcid
        '''
        result = self._values.get("classic_link_vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def classic_link_vpc_security_groups(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Available for backward compatibility.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html#cfn-autoscaling-launchconfiguration-classiclinkvpcsecuritygroups
        '''
        result = self._values.get("classic_link_vpc_security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ebs_optimized(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the launch configuration is optimized for EBS I/O ( ``true`` ) or not ( ``false`` ).

        The optimization provides dedicated throughput to Amazon EBS and an optimized configuration stack to provide optimal I/O performance. This optimization is not available with all instance types. Additional fees are incurred when you enable EBS optimization for an instance type that is not EBS-optimized by default. For more information, see `Amazon EBS-optimized instances <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-optimized.html>`_ in the *Amazon EC2 User Guide* .

        The default value is ``false`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html#cfn-autoscaling-launchconfiguration-ebsoptimized
        '''
        result = self._values.get("ebs_optimized")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def iam_instance_profile(self) -> typing.Optional[builtins.str]:
        '''The name or the Amazon Resource Name (ARN) of the instance profile associated with the IAM role for the instance.

        The instance profile contains the IAM role. For more information, see `IAM role for applications that run on Amazon EC2 instances <https://docs.aws.amazon.com/autoscaling/ec2/userguide/us-iam-role.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html#cfn-autoscaling-launchconfiguration-iaminstanceprofile
        '''
        result = self._values.get("iam_instance_profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Amazon Machine Image (AMI) that was assigned during registration.

        For more information, see `Find a Linux AMI <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/finding-an-ami.html>`_ in the *Amazon EC2 User Guide* .

        If you specify ``InstanceId`` , an ``ImageId`` is not required.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html#cfn-autoscaling-launchconfiguration-imageid
        '''
        result = self._values.get("image_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Amazon EC2 instance to use to create the launch configuration.

        When you use an instance to create a launch configuration, all properties are derived from the instance with the exception of ``BlockDeviceMapping`` and ``AssociatePublicIpAddress`` . You can override any properties from the instance by specifying them in the launch configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html#cfn-autoscaling-launchconfiguration-instanceid
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_monitoring(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Controls whether instances in this group are launched with detailed ( ``true`` ) or basic ( ``false`` ) monitoring.

        The default value is ``true`` (enabled).
        .. epigraph::

           When detailed monitoring is enabled, Amazon CloudWatch generates metrics every minute and your account is charged a fee. When you disable detailed monitoring, CloudWatch generates metrics every 5 minutes. For more information, see `Configure monitoring for Auto Scaling instances <https://docs.aws.amazon.com/autoscaling/latest/userguide/enable-as-instance-metrics.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html#cfn-autoscaling-launchconfiguration-instancemonitoring
        '''
        result = self._values.get("instance_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the instance type of the EC2 instance.

        For information about available instance types, see `Available instance types <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html#AvailableInstanceTypes>`_ in the *Amazon EC2 User Guide* .

        If you specify ``InstanceId`` , an ``InstanceType`` is not required.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html#cfn-autoscaling-launchconfiguration-instancetype
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kernel_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the kernel associated with the AMI.

        .. epigraph::

           We recommend that you use PV-GRUB instead of kernels and RAM disks. For more information, see `User provided kernels <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/UserProvidedKernels.html>`_ in the *Amazon EC2 User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html#cfn-autoscaling-launchconfiguration-kernelid
        '''
        result = self._values.get("kernel_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        '''The name of the key pair.

        For more information, see `Amazon EC2 key pairs and Amazon EC2 instances <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html>`_ in the *Amazon EC2 User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html#cfn-autoscaling-launchconfiguration-keyname
        '''
        result = self._values.get("key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def launch_configuration_name(self) -> typing.Optional[builtins.str]:
        '''The name of the launch configuration.

        This name must be unique per Region per account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html#cfn-autoscaling-launchconfiguration-launchconfigurationname
        '''
        result = self._values.get("launch_configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchConfigurationPropsMixin.MetadataOptionsProperty"]]:
        '''The metadata options for the instances.

        For more information, see `Configure the instance metadata options <https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-launch-config.html#launch-configurations-imds>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html#cfn-autoscaling-launchconfiguration-metadataoptions
        '''
        result = self._values.get("metadata_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchConfigurationPropsMixin.MetadataOptionsProperty"]], result)

    @builtins.property
    def placement_tenancy(self) -> typing.Optional[builtins.str]:
        '''The tenancy of the instance, either ``default`` or ``dedicated`` .

        An instance with ``dedicated`` tenancy runs on isolated, single-tenant hardware and can only be launched into a VPC. To launch dedicated instances into a shared tenancy VPC (a VPC with the instance placement tenancy attribute set to ``default`` ), you must set the value of this property to ``dedicated`` .

        If you specify ``PlacementTenancy`` , you must specify at least one subnet for ``VPCZoneIdentifier`` when you create your group.

        Valid values: ``default`` | ``dedicated``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html#cfn-autoscaling-launchconfiguration-placementtenancy
        '''
        result = self._values.get("placement_tenancy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ram_disk_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the RAM disk to select.

        .. epigraph::

           We recommend that you use PV-GRUB instead of kernels and RAM disks. For more information, see `User provided kernels <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/UserProvidedKernels.html>`_ in the *Amazon EC2 User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html#cfn-autoscaling-launchconfiguration-ramdiskid
        '''
        result = self._values.get("ram_disk_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list that contains the security groups to assign to the instances in the Auto Scaling group.

        The list can contain both the IDs of existing security groups and references to `SecurityGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html>`_ resources created in the template.

        For more information, see `Control traffic to resources using security groups <https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_SecurityGroups.html>`_ in the *Amazon Virtual Private Cloud User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html#cfn-autoscaling-launchconfiguration-securitygroups
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def spot_price(self) -> typing.Optional[builtins.str]:
        '''The maximum hourly price to be paid for any Spot Instance launched to fulfill the request.

        Spot Instances are launched when the price you specify exceeds the current Spot price. For more information, see `Request Spot Instances for fault-tolerant and flexible applications <https://docs.aws.amazon.com/autoscaling/ec2/userguide/launch-template-spot-instances.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        Valid Range: Minimum value of 0.001
        .. epigraph::

           When you change your maximum price by creating a new launch configuration, running instances will continue to run as long as the maximum price for those running instances is higher than the current Spot price.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html#cfn-autoscaling-launchconfiguration-spotprice
        '''
        result = self._values.get("spot_price")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_data(self) -> typing.Optional[builtins.str]:
        '''The Base64-encoded user data to make available to the launched EC2 instances.

        For more information, see `Instance metadata and user data <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html>`_ in the *Amazon EC2 User Guide for Linux Instances* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html#cfn-autoscaling-launchconfiguration-userdata
        '''
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLaunchConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLaunchConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnLaunchConfigurationPropsMixin",
):
    '''The ``AWS::AutoScaling::LaunchConfiguration`` resource specifies the launch configuration that can be used by an Auto Scaling group to configure Amazon EC2 instances.

    When you update the launch configuration for an Auto Scaling group, CloudFormation deletes that resource and creates a new launch configuration with the updated properties and a new name. Existing instances are not affected. To update existing instances when you update the ``AWS::AutoScaling::LaunchConfiguration`` resource, you can specify an `UpdatePolicy attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html>`_ for the group. You can find sample update policies for rolling updates in `Configure Amazon EC2 Auto Scaling resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-ec2-auto-scaling.html>`_ .
    .. epigraph::

       Amazon EC2 Auto Scaling configures instances launched as part of an Auto Scaling group using either a `launch template <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-launchtemplate.html>`_ or a launch configuration. We strongly recommend that you do not use launch configurations. For more information, see `Launch configurations <https://docs.aws.amazon.com/autoscaling/ec2/userguide/launch-configurations.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

       For help migrating from launch configurations to launch templates, see `Migrate AWS CloudFormation stacks from launch configurations to launch templates <https://docs.aws.amazon.com/autoscaling/ec2/userguide/migrate-launch-configurations-with-cloudformation.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html
    :cloudformationResource: AWS::AutoScaling::LaunchConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
        
        cfn_launch_configuration_props_mixin = autoscaling_mixins.CfnLaunchConfigurationPropsMixin(autoscaling_mixins.CfnLaunchConfigurationMixinProps(
            associate_public_ip_address=False,
            block_device_mappings=[autoscaling_mixins.CfnLaunchConfigurationPropsMixin.BlockDeviceMappingProperty(
                device_name="deviceName",
                ebs=autoscaling_mixins.CfnLaunchConfigurationPropsMixin.BlockDeviceProperty(
                    delete_on_termination=False,
                    encrypted=False,
                    iops=123,
                    snapshot_id="snapshotId",
                    throughput=123,
                    volume_size=123,
                    volume_type="volumeType"
                ),
                no_device=False,
                virtual_name="virtualName"
            )],
            classic_link_vpc_id="classicLinkVpcId",
            classic_link_vpc_security_groups=["classicLinkVpcSecurityGroups"],
            ebs_optimized=False,
            iam_instance_profile="iamInstanceProfile",
            image_id="imageId",
            instance_id="instanceId",
            instance_monitoring=False,
            instance_type="instanceType",
            kernel_id="kernelId",
            key_name="keyName",
            launch_configuration_name="launchConfigurationName",
            metadata_options=autoscaling_mixins.CfnLaunchConfigurationPropsMixin.MetadataOptionsProperty(
                http_endpoint="httpEndpoint",
                http_put_response_hop_limit=123,
                http_tokens="httpTokens"
            ),
            placement_tenancy="placementTenancy",
            ram_disk_id="ramDiskId",
            security_groups=["securityGroups"],
            spot_price="spotPrice",
            user_data="userData"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLaunchConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AutoScaling::LaunchConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__291ca37c88883ecd8f8bb52e25d86c0d0949f2647e560fa7d04e8e9abf63a015)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        options = _CfnPropertyMixinOptions_9cbff649(strategy=strategy)

        jsii.create(self.__class__, self, [props, options])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply the mixin properties to the construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df01651555fa4a5b52f1c64c6a8f228783be1545dba024c33f9b37dc17e0cbb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57c2595566576f4ba66967c97ced5128828c0705b29b73e5a45e595b2942ab5a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLaunchConfigurationMixinProps:
        return typing.cast(CfnLaunchConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnLaunchConfigurationPropsMixin.BlockDeviceMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "device_name": "deviceName",
            "ebs": "ebs",
            "no_device": "noDevice",
            "virtual_name": "virtualName",
        },
    )
    class BlockDeviceMappingProperty:
        def __init__(
            self,
            *,
            device_name: typing.Optional[builtins.str] = None,
            ebs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLaunchConfigurationPropsMixin.BlockDeviceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            no_device: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            virtual_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``BlockDeviceMapping`` specifies a block device mapping for the ``BlockDeviceMappings`` property of the `AWS::AutoScaling::LaunchConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html>`_ resource.

            Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched.

            For more information, see `Example block device mapping <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-device-mapping-concepts.html#block-device-mapping-ex>`_ in the *Amazon EC2 User Guide for Linux Instances* .

            :param device_name: The device name assigned to the volume (for example, ``/dev/sdh`` or ``xvdh`` ). For more information, see `Device naming on Linux instances <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/device_naming.html>`_ in the *Amazon EC2 User Guide* . .. epigraph:: To define a block device mapping, set the device name and exactly one of the following properties: ``Ebs`` , ``NoDevice`` , or ``VirtualName`` .
            :param ebs: Information to attach an EBS volume to an instance at launch.
            :param no_device: Setting this value to ``true`` prevents a volume that is included in the block device mapping of the AMI from being mapped to the specified device name at launch. If ``NoDevice`` is ``true`` for the root device, instances might fail the EC2 health check. In that case, Amazon EC2 Auto Scaling launches replacement instances.
            :param virtual_name: The name of the instance store volume (virtual device) to attach to an instance at launch. The name must be in the form ephemeral *X* where *X* is a number starting from zero (0), for example, ``ephemeral0`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfiguration-blockdevicemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                block_device_mapping_property = autoscaling_mixins.CfnLaunchConfigurationPropsMixin.BlockDeviceMappingProperty(
                    device_name="deviceName",
                    ebs=autoscaling_mixins.CfnLaunchConfigurationPropsMixin.BlockDeviceProperty(
                        delete_on_termination=False,
                        encrypted=False,
                        iops=123,
                        snapshot_id="snapshotId",
                        throughput=123,
                        volume_size=123,
                        volume_type="volumeType"
                    ),
                    no_device=False,
                    virtual_name="virtualName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4db99c9dc1d78e8cec57b0f4fb2bc5a65ebf1d5277ee9ac947eda6630a50371a)
                check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
                check_type(argname="argument ebs", value=ebs, expected_type=type_hints["ebs"])
                check_type(argname="argument no_device", value=no_device, expected_type=type_hints["no_device"])
                check_type(argname="argument virtual_name", value=virtual_name, expected_type=type_hints["virtual_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if device_name is not None:
                self._values["device_name"] = device_name
            if ebs is not None:
                self._values["ebs"] = ebs
            if no_device is not None:
                self._values["no_device"] = no_device
            if virtual_name is not None:
                self._values["virtual_name"] = virtual_name

        @builtins.property
        def device_name(self) -> typing.Optional[builtins.str]:
            '''The device name assigned to the volume (for example, ``/dev/sdh`` or ``xvdh`` ).

            For more information, see `Device naming on Linux instances <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/device_naming.html>`_ in the *Amazon EC2 User Guide* .
            .. epigraph::

               To define a block device mapping, set the device name and exactly one of the following properties: ``Ebs`` , ``NoDevice`` , or ``VirtualName`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfiguration-blockdevicemapping.html#cfn-autoscaling-launchconfiguration-blockdevicemapping-devicename
            '''
            result = self._values.get("device_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ebs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchConfigurationPropsMixin.BlockDeviceProperty"]]:
            '''Information to attach an EBS volume to an instance at launch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfiguration-blockdevicemapping.html#cfn-autoscaling-launchconfiguration-blockdevicemapping-ebs
            '''
            result = self._values.get("ebs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchConfigurationPropsMixin.BlockDeviceProperty"]], result)

        @builtins.property
        def no_device(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Setting this value to ``true`` prevents a volume that is included in the block device mapping of the AMI from being mapped to the specified device name at launch.

            If ``NoDevice`` is ``true`` for the root device, instances might fail the EC2 health check. In that case, Amazon EC2 Auto Scaling launches replacement instances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfiguration-blockdevicemapping.html#cfn-autoscaling-launchconfiguration-blockdevicemapping-nodevice
            '''
            result = self._values.get("no_device")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def virtual_name(self) -> typing.Optional[builtins.str]:
            '''The name of the instance store volume (virtual device) to attach to an instance at launch.

            The name must be in the form ephemeral *X* where *X* is a number starting from zero (0), for example, ``ephemeral0`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfiguration-blockdevicemapping.html#cfn-autoscaling-launchconfiguration-blockdevicemapping-virtualname
            '''
            result = self._values.get("virtual_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BlockDeviceMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnLaunchConfigurationPropsMixin.BlockDeviceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delete_on_termination": "deleteOnTermination",
            "encrypted": "encrypted",
            "iops": "iops",
            "snapshot_id": "snapshotId",
            "throughput": "throughput",
            "volume_size": "volumeSize",
            "volume_type": "volumeType",
        },
    )
    class BlockDeviceProperty:
        def __init__(
            self,
            *,
            delete_on_termination: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            iops: typing.Optional[jsii.Number] = None,
            snapshot_id: typing.Optional[builtins.str] = None,
            throughput: typing.Optional[jsii.Number] = None,
            volume_size: typing.Optional[jsii.Number] = None,
            volume_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``BlockDevice`` is a property of the ``EBS`` property of the `AWS::AutoScaling::LaunchConfiguration BlockDeviceMapping <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfiguration-blockdevicemapping.html>`_ property type that describes an Amazon EBS volume.

            :param delete_on_termination: Indicates whether the volume is deleted on instance termination. For Amazon EC2 Auto Scaling, the default value is ``true`` .
            :param encrypted: Specifies whether the volume should be encrypted. Encrypted EBS volumes can only be attached to instances that support Amazon EBS encryption. For more information, see `Requirements for Amazon EBS encryption <https://docs.aws.amazon.com/ebs/latest/userguide/ebs-encryption-requirements.html>`_ in the *Amazon EBS User Guide* . If your AMI uses encrypted volumes, you can also only launch it on supported instance types. .. epigraph:: If you are creating a volume from a snapshot, you cannot create an unencrypted volume from an encrypted snapshot. Also, you cannot specify a KMS key ID when using a launch configuration. If you enable encryption by default, the EBS volumes that you create are always encrypted, either using the AWS managed KMS key or a customer-managed KMS key, regardless of whether the snapshot was encrypted. For more information, see `Use AWS KMS keys to encrypt Amazon EBS volumes <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-data-protection.html#encryption>`_ in the *Amazon EC2 Auto Scaling User Guide* .
            :param iops: The number of input/output (I/O) operations per second (IOPS) to provision for the volume. For ``gp3`` and ``io1`` volumes, this represents the number of IOPS that are provisioned for the volume. For ``gp2`` volumes, this represents the baseline performance of the volume and the rate at which the volume accumulates I/O credits for bursting. The following are the supported values for each volume type: - ``gp3`` : 3,000-16,000 IOPS - ``io1`` : 100-64,000 IOPS For ``io1`` volumes, we guarantee 64,000 IOPS only for `Instances built on the Nitro System <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html#ec2-nitro-instances>`_ . Other instance families guarantee performance up to 32,000 IOPS. ``Iops`` is supported when the volume type is ``gp3`` or ``io1`` and required only when the volume type is ``io1`` . (Not used with ``standard`` , ``gp2`` , ``st1`` , or ``sc1`` volumes.)
            :param snapshot_id: The snapshot ID of the volume to use. You must specify either a ``VolumeSize`` or a ``SnapshotId`` .
            :param throughput: The throughput (MiBps) to provision for a ``gp3`` volume.
            :param volume_size: The volume size, in GiBs. The following are the supported volumes sizes for each volume type:. - ``gp2`` and ``gp3`` : 1-16,384 - ``io1`` : 4-16,384 - ``st1`` and ``sc1`` : 125-16,384 - ``standard`` : 1-1,024 You must specify either a ``SnapshotId`` or a ``VolumeSize`` . If you specify both ``SnapshotId`` and ``VolumeSize`` , the volume size must be equal or greater than the size of the snapshot.
            :param volume_type: The volume type. For more information, see `Amazon EBS volume types <https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volume-types.html>`_ in the *Amazon EBS User Guide* . Valid values: ``standard`` | ``io1`` | ``gp2`` | ``st1`` | ``sc1`` | ``gp3``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfiguration-blockdevice.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                block_device_property = autoscaling_mixins.CfnLaunchConfigurationPropsMixin.BlockDeviceProperty(
                    delete_on_termination=False,
                    encrypted=False,
                    iops=123,
                    snapshot_id="snapshotId",
                    throughput=123,
                    volume_size=123,
                    volume_type="volumeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__297d5e975a56478f1b4e23756a19d37be35192e5099be3e81b995d49c9f0b377)
                check_type(argname="argument delete_on_termination", value=delete_on_termination, expected_type=type_hints["delete_on_termination"])
                check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
                check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
                check_type(argname="argument snapshot_id", value=snapshot_id, expected_type=type_hints["snapshot_id"])
                check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
                check_type(argname="argument volume_size", value=volume_size, expected_type=type_hints["volume_size"])
                check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delete_on_termination is not None:
                self._values["delete_on_termination"] = delete_on_termination
            if encrypted is not None:
                self._values["encrypted"] = encrypted
            if iops is not None:
                self._values["iops"] = iops
            if snapshot_id is not None:
                self._values["snapshot_id"] = snapshot_id
            if throughput is not None:
                self._values["throughput"] = throughput
            if volume_size is not None:
                self._values["volume_size"] = volume_size
            if volume_type is not None:
                self._values["volume_type"] = volume_type

        @builtins.property
        def delete_on_termination(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the volume is deleted on instance termination.

            For Amazon EC2 Auto Scaling, the default value is ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfiguration-blockdevice.html#cfn-autoscaling-launchconfiguration-blockdevice-deleteontermination
            '''
            result = self._values.get("delete_on_termination")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def encrypted(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the volume should be encrypted.

            Encrypted EBS volumes can only be attached to instances that support Amazon EBS encryption. For more information, see `Requirements for Amazon EBS encryption <https://docs.aws.amazon.com/ebs/latest/userguide/ebs-encryption-requirements.html>`_ in the *Amazon EBS User Guide* . If your AMI uses encrypted volumes, you can also only launch it on supported instance types.
            .. epigraph::

               If you are creating a volume from a snapshot, you cannot create an unencrypted volume from an encrypted snapshot. Also, you cannot specify a KMS key ID when using a launch configuration.

               If you enable encryption by default, the EBS volumes that you create are always encrypted, either using the AWS managed KMS key or a customer-managed KMS key, regardless of whether the snapshot was encrypted.

               For more information, see `Use AWS KMS keys to encrypt Amazon EBS volumes <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-data-protection.html#encryption>`_ in the *Amazon EC2 Auto Scaling User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfiguration-blockdevice.html#cfn-autoscaling-launchconfiguration-blockdevice-encrypted
            '''
            result = self._values.get("encrypted")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            '''The number of input/output (I/O) operations per second (IOPS) to provision for the volume.

            For ``gp3`` and ``io1`` volumes, this represents the number of IOPS that are provisioned for the volume. For ``gp2`` volumes, this represents the baseline performance of the volume and the rate at which the volume accumulates I/O credits for bursting.

            The following are the supported values for each volume type:

            - ``gp3`` : 3,000-16,000 IOPS
            - ``io1`` : 100-64,000 IOPS

            For ``io1`` volumes, we guarantee 64,000 IOPS only for `Instances built on the Nitro System <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html#ec2-nitro-instances>`_ . Other instance families guarantee performance up to 32,000 IOPS.

            ``Iops`` is supported when the volume type is ``gp3`` or ``io1`` and required only when the volume type is ``io1`` . (Not used with ``standard`` , ``gp2`` , ``st1`` , or ``sc1`` volumes.)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfiguration-blockdevice.html#cfn-autoscaling-launchconfiguration-blockdevice-iops
            '''
            result = self._values.get("iops")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def snapshot_id(self) -> typing.Optional[builtins.str]:
            '''The snapshot ID of the volume to use.

            You must specify either a ``VolumeSize`` or a ``SnapshotId`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfiguration-blockdevice.html#cfn-autoscaling-launchconfiguration-blockdevice-snapshotid
            '''
            result = self._values.get("snapshot_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def throughput(self) -> typing.Optional[jsii.Number]:
            '''The throughput (MiBps) to provision for a ``gp3`` volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfiguration-blockdevice.html#cfn-autoscaling-launchconfiguration-blockdevice-throughput
            '''
            result = self._values.get("throughput")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_size(self) -> typing.Optional[jsii.Number]:
            '''The volume size, in GiBs. The following are the supported volumes sizes for each volume type:.

            - ``gp2`` and ``gp3`` : 1-16,384
            - ``io1`` : 4-16,384
            - ``st1`` and ``sc1`` : 125-16,384
            - ``standard`` : 1-1,024

            You must specify either a ``SnapshotId`` or a ``VolumeSize`` . If you specify both ``SnapshotId`` and ``VolumeSize`` , the volume size must be equal or greater than the size of the snapshot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfiguration-blockdevice.html#cfn-autoscaling-launchconfiguration-blockdevice-volumesize
            '''
            result = self._values.get("volume_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_type(self) -> typing.Optional[builtins.str]:
            '''The volume type. For more information, see `Amazon EBS volume types <https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volume-types.html>`_ in the *Amazon EBS User Guide* .

            Valid values: ``standard`` | ``io1`` | ``gp2`` | ``st1`` | ``sc1`` | ``gp3``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfiguration-blockdevice.html#cfn-autoscaling-launchconfiguration-blockdevice-volumetype
            '''
            result = self._values.get("volume_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BlockDeviceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnLaunchConfigurationPropsMixin.MetadataOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "http_endpoint": "httpEndpoint",
            "http_put_response_hop_limit": "httpPutResponseHopLimit",
            "http_tokens": "httpTokens",
        },
    )
    class MetadataOptionsProperty:
        def __init__(
            self,
            *,
            http_endpoint: typing.Optional[builtins.str] = None,
            http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
            http_tokens: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``MetadataOptions`` is a property of `AWS::AutoScaling::LaunchConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-launchconfiguration.html>`_ that describes metadata options for the instances.

            For more information, see `Configure the instance metadata options <https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-launch-config.html#launch-configurations-imds>`_ in the *Amazon EC2 Auto Scaling User Guide* .

            :param http_endpoint: This parameter enables or disables the HTTP metadata endpoint on your instances. If the parameter is not specified, the default state is ``enabled`` . .. epigraph:: If you specify a value of ``disabled`` , you will not be able to access your instance metadata.
            :param http_put_response_hop_limit: The desired HTTP PUT response hop limit for instance metadata requests. The larger the number, the further instance metadata requests can travel. Default: 1
            :param http_tokens: The state of token usage for your instance metadata requests. If the parameter is not specified in the request, the default state is ``optional`` . If the state is ``optional`` , you can choose to retrieve instance metadata with or without a signed token header on your request. If you retrieve the IAM role credentials without a token, the version 1.0 role credentials are returned. If you retrieve the IAM role credentials using a valid signed token, the version 2.0 role credentials are returned. If the state is ``required`` , you must send a signed token header with any instance metadata retrieval requests. In this state, retrieving the IAM role credentials always returns the version 2.0 credentials; the version 1.0 credentials are not available.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfiguration-metadataoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                metadata_options_property = autoscaling_mixins.CfnLaunchConfigurationPropsMixin.MetadataOptionsProperty(
                    http_endpoint="httpEndpoint",
                    http_put_response_hop_limit=123,
                    http_tokens="httpTokens"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd9766befcdf389aa53bf8f87087474bb986df07ef90ac4366e56ab2c976c718)
                check_type(argname="argument http_endpoint", value=http_endpoint, expected_type=type_hints["http_endpoint"])
                check_type(argname="argument http_put_response_hop_limit", value=http_put_response_hop_limit, expected_type=type_hints["http_put_response_hop_limit"])
                check_type(argname="argument http_tokens", value=http_tokens, expected_type=type_hints["http_tokens"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if http_endpoint is not None:
                self._values["http_endpoint"] = http_endpoint
            if http_put_response_hop_limit is not None:
                self._values["http_put_response_hop_limit"] = http_put_response_hop_limit
            if http_tokens is not None:
                self._values["http_tokens"] = http_tokens

        @builtins.property
        def http_endpoint(self) -> typing.Optional[builtins.str]:
            '''This parameter enables or disables the HTTP metadata endpoint on your instances.

            If the parameter is not specified, the default state is ``enabled`` .
            .. epigraph::

               If you specify a value of ``disabled`` , you will not be able to access your instance metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfiguration-metadataoptions.html#cfn-autoscaling-launchconfiguration-metadataoptions-httpendpoint
            '''
            result = self._values.get("http_endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def http_put_response_hop_limit(self) -> typing.Optional[jsii.Number]:
            '''The desired HTTP PUT response hop limit for instance metadata requests.

            The larger the number, the further instance metadata requests can travel.

            Default: 1

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfiguration-metadataoptions.html#cfn-autoscaling-launchconfiguration-metadataoptions-httpputresponsehoplimit
            '''
            result = self._values.get("http_put_response_hop_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def http_tokens(self) -> typing.Optional[builtins.str]:
            '''The state of token usage for your instance metadata requests.

            If the parameter is not specified in the request, the default state is ``optional`` .

            If the state is ``optional`` , you can choose to retrieve instance metadata with or without a signed token header on your request. If you retrieve the IAM role credentials without a token, the version 1.0 role credentials are returned. If you retrieve the IAM role credentials using a valid signed token, the version 2.0 role credentials are returned.

            If the state is ``required`` , you must send a signed token header with any instance metadata retrieval requests. In this state, retrieving the IAM role credentials always returns the version 2.0 credentials; the version 1.0 credentials are not available.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-launchconfiguration-metadataoptions.html#cfn-autoscaling-launchconfiguration-metadataoptions-httptokens
            '''
            result = self._values.get("http_tokens")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetadataOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnLifecycleHookMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_group_name": "autoScalingGroupName",
        "default_result": "defaultResult",
        "heartbeat_timeout": "heartbeatTimeout",
        "lifecycle_hook_name": "lifecycleHookName",
        "lifecycle_transition": "lifecycleTransition",
        "notification_metadata": "notificationMetadata",
        "notification_target_arn": "notificationTargetArn",
        "role_arn": "roleArn",
    },
)
class CfnLifecycleHookMixinProps:
    def __init__(
        self,
        *,
        auto_scaling_group_name: typing.Optional[builtins.str] = None,
        default_result: typing.Optional[builtins.str] = None,
        heartbeat_timeout: typing.Optional[jsii.Number] = None,
        lifecycle_hook_name: typing.Optional[builtins.str] = None,
        lifecycle_transition: typing.Optional[builtins.str] = None,
        notification_metadata: typing.Optional[builtins.str] = None,
        notification_target_arn: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnLifecycleHookPropsMixin.

        :param auto_scaling_group_name: The name of the Auto Scaling group.
        :param default_result: The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs. The default value is ``ABANDON`` . Valid values: ``CONTINUE`` | ``ABANDON``
        :param heartbeat_timeout: The maximum time, in seconds, that can elapse before the lifecycle hook times out. The range is from ``30`` to ``7200`` seconds. The default value is ``3600`` seconds (1 hour).
        :param lifecycle_hook_name: The name of the lifecycle hook.
        :param lifecycle_transition: The lifecycle transition. For Auto Scaling groups, there are two major lifecycle transitions. - To create a lifecycle hook for scale-out events, specify ``autoscaling:EC2_INSTANCE_LAUNCHING`` . - To create a lifecycle hook for scale-in events, specify ``autoscaling:EC2_INSTANCE_TERMINATING`` .
        :param notification_metadata: Additional information that you want to include any time Amazon EC2 Auto Scaling sends a message to the notification target.
        :param notification_target_arn: The Amazon Resource Name (ARN) of the notification target that Amazon EC2 Auto Scaling sends notifications to when an instance is in a wait state for the lifecycle hook. You can specify an Amazon SNS topic or an Amazon SQS queue.
        :param role_arn: The ARN of the IAM role that allows the Auto Scaling group to publish to the specified notification target. For information about creating this role, see `Prepare to add a lifecycle hook to your Auto Scaling group <https://docs.aws.amazon.com/autoscaling/ec2/userguide/prepare-for-lifecycle-notifications.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . Valid only if the notification target is an Amazon SNS topic or an Amazon SQS queue.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-lifecyclehook.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
            
            cfn_lifecycle_hook_mixin_props = autoscaling_mixins.CfnLifecycleHookMixinProps(
                auto_scaling_group_name="autoScalingGroupName",
                default_result="defaultResult",
                heartbeat_timeout=123,
                lifecycle_hook_name="lifecycleHookName",
                lifecycle_transition="lifecycleTransition",
                notification_metadata="notificationMetadata",
                notification_target_arn="notificationTargetArn",
                role_arn="roleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39cf4fd87415a577af69696e67fc58b48c56e1acc5834a2b836fb9fa6412b1f2)
            check_type(argname="argument auto_scaling_group_name", value=auto_scaling_group_name, expected_type=type_hints["auto_scaling_group_name"])
            check_type(argname="argument default_result", value=default_result, expected_type=type_hints["default_result"])
            check_type(argname="argument heartbeat_timeout", value=heartbeat_timeout, expected_type=type_hints["heartbeat_timeout"])
            check_type(argname="argument lifecycle_hook_name", value=lifecycle_hook_name, expected_type=type_hints["lifecycle_hook_name"])
            check_type(argname="argument lifecycle_transition", value=lifecycle_transition, expected_type=type_hints["lifecycle_transition"])
            check_type(argname="argument notification_metadata", value=notification_metadata, expected_type=type_hints["notification_metadata"])
            check_type(argname="argument notification_target_arn", value=notification_target_arn, expected_type=type_hints["notification_target_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_scaling_group_name is not None:
            self._values["auto_scaling_group_name"] = auto_scaling_group_name
        if default_result is not None:
            self._values["default_result"] = default_result
        if heartbeat_timeout is not None:
            self._values["heartbeat_timeout"] = heartbeat_timeout
        if lifecycle_hook_name is not None:
            self._values["lifecycle_hook_name"] = lifecycle_hook_name
        if lifecycle_transition is not None:
            self._values["lifecycle_transition"] = lifecycle_transition
        if notification_metadata is not None:
            self._values["notification_metadata"] = notification_metadata
        if notification_target_arn is not None:
            self._values["notification_target_arn"] = notification_target_arn
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def auto_scaling_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Auto Scaling group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-lifecyclehook.html#cfn-autoscaling-lifecyclehook-autoscalinggroupname
        '''
        result = self._values.get("auto_scaling_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_result(self) -> typing.Optional[builtins.str]:
        '''The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs.

        The default value is ``ABANDON`` .

        Valid values: ``CONTINUE`` | ``ABANDON``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-lifecyclehook.html#cfn-autoscaling-lifecyclehook-defaultresult
        '''
        result = self._values.get("default_result")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def heartbeat_timeout(self) -> typing.Optional[jsii.Number]:
        '''The maximum time, in seconds, that can elapse before the lifecycle hook times out.

        The range is from ``30`` to ``7200`` seconds. The default value is ``3600`` seconds (1 hour).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-lifecyclehook.html#cfn-autoscaling-lifecyclehook-heartbeattimeout
        '''
        result = self._values.get("heartbeat_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lifecycle_hook_name(self) -> typing.Optional[builtins.str]:
        '''The name of the lifecycle hook.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-lifecyclehook.html#cfn-autoscaling-lifecyclehook-lifecyclehookname
        '''
        result = self._values.get("lifecycle_hook_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_transition(self) -> typing.Optional[builtins.str]:
        '''The lifecycle transition. For Auto Scaling groups, there are two major lifecycle transitions.

        - To create a lifecycle hook for scale-out events, specify ``autoscaling:EC2_INSTANCE_LAUNCHING`` .
        - To create a lifecycle hook for scale-in events, specify ``autoscaling:EC2_INSTANCE_TERMINATING`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-lifecyclehook.html#cfn-autoscaling-lifecyclehook-lifecycletransition
        '''
        result = self._values.get("lifecycle_transition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_metadata(self) -> typing.Optional[builtins.str]:
        '''Additional information that you want to include any time Amazon EC2 Auto Scaling sends a message to the notification target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-lifecyclehook.html#cfn-autoscaling-lifecyclehook-notificationmetadata
        '''
        result = self._values.get("notification_metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_target_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the notification target that Amazon EC2 Auto Scaling sends notifications to when an instance is in a wait state for the lifecycle hook.

        You can specify an Amazon SNS topic or an Amazon SQS queue.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-lifecyclehook.html#cfn-autoscaling-lifecyclehook-notificationtargetarn
        '''
        result = self._values.get("notification_target_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role that allows the Auto Scaling group to publish to the specified notification target.

        For information about creating this role, see `Prepare to add a lifecycle hook to your Auto Scaling group <https://docs.aws.amazon.com/autoscaling/ec2/userguide/prepare-for-lifecycle-notifications.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        Valid only if the notification target is an Amazon SNS topic or an Amazon SQS queue.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-lifecyclehook.html#cfn-autoscaling-lifecyclehook-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLifecycleHookMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLifecycleHookPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnLifecycleHookPropsMixin",
):
    '''The ``AWS::AutoScaling::LifecycleHook`` resource specifies lifecycle hooks for an Auto Scaling group.

    These hooks let you create solutions that are aware of events in the Auto Scaling instance lifecycle, and then perform a custom action on instances when the corresponding lifecycle event occurs. A lifecycle hook provides a specified amount of time (one hour by default) to wait for the action to complete before the instance transitions to the next state.

    Use lifecycle hooks to prepare new instances for use or to delay them from being registered behind a load balancer before their configuration has been applied completely. You can also use lifecycle hooks to prepare running instances to be terminated by, for example, downloading logs or other data.

    For more information, see `Amazon EC2 Auto Scaling lifecycle hooks <https://docs.aws.amazon.com/autoscaling/ec2/userguide/lifecycle-hooks.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-lifecyclehook.html
    :cloudformationResource: AWS::AutoScaling::LifecycleHook
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
        
        cfn_lifecycle_hook_props_mixin = autoscaling_mixins.CfnLifecycleHookPropsMixin(autoscaling_mixins.CfnLifecycleHookMixinProps(
            auto_scaling_group_name="autoScalingGroupName",
            default_result="defaultResult",
            heartbeat_timeout=123,
            lifecycle_hook_name="lifecycleHookName",
            lifecycle_transition="lifecycleTransition",
            notification_metadata="notificationMetadata",
            notification_target_arn="notificationTargetArn",
            role_arn="roleArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLifecycleHookMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AutoScaling::LifecycleHook``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e48590fc071dd71fddeeb617eaee2c4081a5708803d29f31422808e5d7af12ca)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        options = _CfnPropertyMixinOptions_9cbff649(strategy=strategy)

        jsii.create(self.__class__, self, [props, options])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply the mixin properties to the construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0420a3a0d08815154075a4451dbaca1fe0b6daaf446b26b5c83636244da901d9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0912d4453715d7e5f18ee8b48c21568b64ec6401b53922db67333da8b148a0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLifecycleHookMixinProps:
        return typing.cast(CfnLifecycleHookMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScalingPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "adjustment_type": "adjustmentType",
        "auto_scaling_group_name": "autoScalingGroupName",
        "cooldown": "cooldown",
        "estimated_instance_warmup": "estimatedInstanceWarmup",
        "metric_aggregation_type": "metricAggregationType",
        "min_adjustment_magnitude": "minAdjustmentMagnitude",
        "policy_type": "policyType",
        "predictive_scaling_configuration": "predictiveScalingConfiguration",
        "scaling_adjustment": "scalingAdjustment",
        "step_adjustments": "stepAdjustments",
        "target_tracking_configuration": "targetTrackingConfiguration",
    },
)
class CfnScalingPolicyMixinProps:
    def __init__(
        self,
        *,
        adjustment_type: typing.Optional[builtins.str] = None,
        auto_scaling_group_name: typing.Optional[builtins.str] = None,
        cooldown: typing.Optional[builtins.str] = None,
        estimated_instance_warmup: typing.Optional[jsii.Number] = None,
        metric_aggregation_type: typing.Optional[builtins.str] = None,
        min_adjustment_magnitude: typing.Optional[jsii.Number] = None,
        policy_type: typing.Optional[builtins.str] = None,
        predictive_scaling_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        scaling_adjustment: typing.Optional[jsii.Number] = None,
        step_adjustments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.StepAdjustmentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        target_tracking_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.TargetTrackingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnScalingPolicyPropsMixin.

        :param adjustment_type: Specifies how the scaling adjustment is interpreted (for example, an absolute number or a percentage). The valid values are ``ChangeInCapacity`` , ``ExactCapacity`` , and ``PercentChangeInCapacity`` . Required if the policy type is ``StepScaling`` or ``SimpleScaling`` . For more information, see `Scaling adjustment types <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html#as-scaling-adjustment>`_ in the *Amazon EC2 Auto Scaling User Guide* .
        :param auto_scaling_group_name: The name of the Auto Scaling group.
        :param cooldown: A cooldown period, in seconds, that applies to a specific simple scaling policy. When a cooldown period is specified here, it overrides the default cooldown. Valid only if the policy type is ``SimpleScaling`` . For more information, see `Scaling cooldowns for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-scaling-cooldowns.html>`_ in the *Amazon EC2 Auto Scaling User Guide* . Default: None
        :param estimated_instance_warmup: *Not needed if the default instance warmup is defined for the group.*. The estimated time, in seconds, until a newly launched instance can contribute to the CloudWatch metrics. This warm-up period applies to instances launched due to a specific target tracking or step scaling policy. When a warm-up period is specified here, it overrides the default instance warmup. Valid only if the policy type is ``TargetTrackingScaling`` or ``StepScaling`` . .. epigraph:: The default is to use the value for the default instance warmup defined for the group. If default instance warmup is null, then ``EstimatedInstanceWarmup`` falls back to the value of default cooldown.
        :param metric_aggregation_type: The aggregation type for the CloudWatch metrics. The valid values are ``Minimum`` , ``Maximum`` , and ``Average`` . If the aggregation type is null, the value is treated as ``Average`` . Valid only if the policy type is ``StepScaling`` .
        :param min_adjustment_magnitude: The minimum value to scale by when the adjustment type is ``PercentChangeInCapacity`` . For example, suppose that you create a step scaling policy to scale out an Auto Scaling group by 25 percent and you specify a ``MinAdjustmentMagnitude`` of 2. If the group has 4 instances and the scaling policy is performed, 25 percent of 4 is 1. However, because you specified a ``MinAdjustmentMagnitude`` of 2, Amazon EC2 Auto Scaling scales out the group by 2 instances. Valid only if the policy type is ``StepScaling`` or ``SimpleScaling`` . For more information, see `Scaling adjustment types <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html#as-scaling-adjustment>`_ in the *Amazon EC2 Auto Scaling User Guide* . .. epigraph:: Some Auto Scaling groups use instance weights. In this case, set the ``MinAdjustmentMagnitude`` to a value that is at least as large as your largest instance weight.
        :param policy_type: One of the following policy types:. - ``TargetTrackingScaling`` - ``StepScaling`` - ``SimpleScaling`` (default) - ``PredictiveScaling``
        :param predictive_scaling_configuration: A predictive scaling policy. Provides support for predefined and custom metrics. Predefined metrics include CPU utilization, network in/out, and the Application Load Balancer request count. Required if the policy type is ``PredictiveScaling`` .
        :param scaling_adjustment: The amount by which to scale, based on the specified adjustment type. A positive value adds to the current capacity while a negative number removes from the current capacity. For exact capacity, you must specify a non-negative value. Required if the policy type is ``SimpleScaling`` . (Not used with any other policy type.)
        :param step_adjustments: A set of adjustments that enable you to scale based on the size of the alarm breach. Required if the policy type is ``StepScaling`` . (Not used with any other policy type.)
        :param target_tracking_configuration: A target tracking scaling policy. Provides support for predefined or custom metrics. The following predefined metrics are available: - ``ASGAverageCPUUtilization`` - ``ASGAverageNetworkIn`` - ``ASGAverageNetworkOut`` - ``ALBRequestCountPerTarget`` If you specify ``ALBRequestCountPerTarget`` for the metric, you must specify the ``ResourceLabel`` property with the ``PredefinedMetricSpecification`` . Required if the policy type is ``TargetTrackingScaling`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scalingpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
            
            cfn_scaling_policy_mixin_props = autoscaling_mixins.CfnScalingPolicyMixinProps(
                adjustment_type="adjustmentType",
                auto_scaling_group_name="autoScalingGroupName",
                cooldown="cooldown",
                estimated_instance_warmup=123,
                metric_aggregation_type="metricAggregationType",
                min_adjustment_magnitude=123,
                policy_type="policyType",
                predictive_scaling_configuration=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingConfigurationProperty(
                    max_capacity_breach_behavior="maxCapacityBreachBehavior",
                    max_capacity_buffer=123,
                    metric_specifications=[autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricSpecificationProperty(
                        customized_capacity_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedCapacityMetricProperty(
                            metric_data_queries=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDataQueryProperty(
                                expression="expression",
                                id="id",
                                label="label",
                                metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricStatProperty(
                                    metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                                        dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                            name="name",
                                            value="value"
                                        )],
                                        metric_name="metricName",
                                        namespace="namespace"
                                    ),
                                    stat="stat",
                                    unit="unit"
                                ),
                                return_data=False
                            )]
                        ),
                        customized_load_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedLoadMetricProperty(
                            metric_data_queries=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDataQueryProperty(
                                expression="expression",
                                id="id",
                                label="label",
                                metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricStatProperty(
                                    metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                                        dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                            name="name",
                                            value="value"
                                        )],
                                        metric_name="metricName",
                                        namespace="namespace"
                                    ),
                                    stat="stat",
                                    unit="unit"
                                ),
                                return_data=False
                            )]
                        ),
                        customized_scaling_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedScalingMetricProperty(
                            metric_data_queries=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDataQueryProperty(
                                expression="expression",
                                id="id",
                                label="label",
                                metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricStatProperty(
                                    metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                                        dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                            name="name",
                                            value="value"
                                        )],
                                        metric_name="metricName",
                                        namespace="namespace"
                                    ),
                                    stat="stat",
                                    unit="unit"
                                ),
                                return_data=False
                            )]
                        ),
                        predefined_load_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedLoadMetricProperty(
                            predefined_metric_type="predefinedMetricType",
                            resource_label="resourceLabel"
                        ),
                        predefined_metric_pair_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedMetricPairProperty(
                            predefined_metric_type="predefinedMetricType",
                            resource_label="resourceLabel"
                        ),
                        predefined_scaling_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedScalingMetricProperty(
                            predefined_metric_type="predefinedMetricType",
                            resource_label="resourceLabel"
                        ),
                        target_value=123
                    )],
                    mode="mode",
                    scheduling_buffer_time=123
                ),
                scaling_adjustment=123,
                step_adjustments=[autoscaling_mixins.CfnScalingPolicyPropsMixin.StepAdjustmentProperty(
                    metric_interval_lower_bound=123,
                    metric_interval_upper_bound=123,
                    scaling_adjustment=123
                )],
                target_tracking_configuration=autoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingConfigurationProperty(
                    customized_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.CustomizedMetricSpecificationProperty(
                        dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                            name="name",
                            value="value"
                        )],
                        metric_name="metricName",
                        metrics=[autoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDataQueryProperty(
                            expression="expression",
                            id="id",
                            label="label",
                            metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty(
                                metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                                    dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                period=123,
                                stat="stat",
                                unit="unit"
                            ),
                            period=123,
                            return_data=False
                        )],
                        namespace="namespace",
                        period=123,
                        statistic="statistic",
                        unit="unit"
                    ),
                    disable_scale_in=False,
                    predefined_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredefinedMetricSpecificationProperty(
                        predefined_metric_type="predefinedMetricType",
                        resource_label="resourceLabel"
                    ),
                    target_value=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94c4008cce30233c624d71e27708e70d8950edef475caadec49de17a2aba1619)
            check_type(argname="argument adjustment_type", value=adjustment_type, expected_type=type_hints["adjustment_type"])
            check_type(argname="argument auto_scaling_group_name", value=auto_scaling_group_name, expected_type=type_hints["auto_scaling_group_name"])
            check_type(argname="argument cooldown", value=cooldown, expected_type=type_hints["cooldown"])
            check_type(argname="argument estimated_instance_warmup", value=estimated_instance_warmup, expected_type=type_hints["estimated_instance_warmup"])
            check_type(argname="argument metric_aggregation_type", value=metric_aggregation_type, expected_type=type_hints["metric_aggregation_type"])
            check_type(argname="argument min_adjustment_magnitude", value=min_adjustment_magnitude, expected_type=type_hints["min_adjustment_magnitude"])
            check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
            check_type(argname="argument predictive_scaling_configuration", value=predictive_scaling_configuration, expected_type=type_hints["predictive_scaling_configuration"])
            check_type(argname="argument scaling_adjustment", value=scaling_adjustment, expected_type=type_hints["scaling_adjustment"])
            check_type(argname="argument step_adjustments", value=step_adjustments, expected_type=type_hints["step_adjustments"])
            check_type(argname="argument target_tracking_configuration", value=target_tracking_configuration, expected_type=type_hints["target_tracking_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if adjustment_type is not None:
            self._values["adjustment_type"] = adjustment_type
        if auto_scaling_group_name is not None:
            self._values["auto_scaling_group_name"] = auto_scaling_group_name
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if estimated_instance_warmup is not None:
            self._values["estimated_instance_warmup"] = estimated_instance_warmup
        if metric_aggregation_type is not None:
            self._values["metric_aggregation_type"] = metric_aggregation_type
        if min_adjustment_magnitude is not None:
            self._values["min_adjustment_magnitude"] = min_adjustment_magnitude
        if policy_type is not None:
            self._values["policy_type"] = policy_type
        if predictive_scaling_configuration is not None:
            self._values["predictive_scaling_configuration"] = predictive_scaling_configuration
        if scaling_adjustment is not None:
            self._values["scaling_adjustment"] = scaling_adjustment
        if step_adjustments is not None:
            self._values["step_adjustments"] = step_adjustments
        if target_tracking_configuration is not None:
            self._values["target_tracking_configuration"] = target_tracking_configuration

    @builtins.property
    def adjustment_type(self) -> typing.Optional[builtins.str]:
        '''Specifies how the scaling adjustment is interpreted (for example, an absolute number or a percentage).

        The valid values are ``ChangeInCapacity`` , ``ExactCapacity`` , and ``PercentChangeInCapacity`` .

        Required if the policy type is ``StepScaling`` or ``SimpleScaling`` . For more information, see `Scaling adjustment types <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html#as-scaling-adjustment>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scalingpolicy.html#cfn-autoscaling-scalingpolicy-adjustmenttype
        '''
        result = self._values.get("adjustment_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_scaling_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Auto Scaling group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scalingpolicy.html#cfn-autoscaling-scalingpolicy-autoscalinggroupname
        '''
        result = self._values.get("auto_scaling_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cooldown(self) -> typing.Optional[builtins.str]:
        '''A cooldown period, in seconds, that applies to a specific simple scaling policy.

        When a cooldown period is specified here, it overrides the default cooldown.

        Valid only if the policy type is ``SimpleScaling`` . For more information, see `Scaling cooldowns for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-scaling-cooldowns.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

        Default: None

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scalingpolicy.html#cfn-autoscaling-scalingpolicy-cooldown
        '''
        result = self._values.get("cooldown")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def estimated_instance_warmup(self) -> typing.Optional[jsii.Number]:
        '''*Not needed if the default instance warmup is defined for the group.*.

        The estimated time, in seconds, until a newly launched instance can contribute to the CloudWatch metrics. This warm-up period applies to instances launched due to a specific target tracking or step scaling policy. When a warm-up period is specified here, it overrides the default instance warmup.

        Valid only if the policy type is ``TargetTrackingScaling`` or ``StepScaling`` .
        .. epigraph::

           The default is to use the value for the default instance warmup defined for the group. If default instance warmup is null, then ``EstimatedInstanceWarmup`` falls back to the value of default cooldown.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scalingpolicy.html#cfn-autoscaling-scalingpolicy-estimatedinstancewarmup
        '''
        result = self._values.get("estimated_instance_warmup")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metric_aggregation_type(self) -> typing.Optional[builtins.str]:
        '''The aggregation type for the CloudWatch metrics.

        The valid values are ``Minimum`` , ``Maximum`` , and ``Average`` . If the aggregation type is null, the value is treated as ``Average`` .

        Valid only if the policy type is ``StepScaling`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scalingpolicy.html#cfn-autoscaling-scalingpolicy-metricaggregationtype
        '''
        result = self._values.get("metric_aggregation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_adjustment_magnitude(self) -> typing.Optional[jsii.Number]:
        '''The minimum value to scale by when the adjustment type is ``PercentChangeInCapacity`` .

        For example, suppose that you create a step scaling policy to scale out an Auto Scaling group by 25 percent and you specify a ``MinAdjustmentMagnitude`` of 2. If the group has 4 instances and the scaling policy is performed, 25 percent of 4 is 1. However, because you specified a ``MinAdjustmentMagnitude`` of 2, Amazon EC2 Auto Scaling scales out the group by 2 instances.

        Valid only if the policy type is ``StepScaling`` or ``SimpleScaling`` . For more information, see `Scaling adjustment types <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html#as-scaling-adjustment>`_ in the *Amazon EC2 Auto Scaling User Guide* .
        .. epigraph::

           Some Auto Scaling groups use instance weights. In this case, set the ``MinAdjustmentMagnitude`` to a value that is at least as large as your largest instance weight.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scalingpolicy.html#cfn-autoscaling-scalingpolicy-minadjustmentmagnitude
        '''
        result = self._values.get("min_adjustment_magnitude")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def policy_type(self) -> typing.Optional[builtins.str]:
        '''One of the following policy types:.

        - ``TargetTrackingScaling``
        - ``StepScaling``
        - ``SimpleScaling`` (default)
        - ``PredictiveScaling``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scalingpolicy.html#cfn-autoscaling-scalingpolicy-policytype
        '''
        result = self._values.get("policy_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def predictive_scaling_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingConfigurationProperty"]]:
        '''A predictive scaling policy. Provides support for predefined and custom metrics.

        Predefined metrics include CPU utilization, network in/out, and the Application Load Balancer request count.

        Required if the policy type is ``PredictiveScaling`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scalingpolicy.html#cfn-autoscaling-scalingpolicy-predictivescalingconfiguration
        '''
        result = self._values.get("predictive_scaling_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingConfigurationProperty"]], result)

    @builtins.property
    def scaling_adjustment(self) -> typing.Optional[jsii.Number]:
        '''The amount by which to scale, based on the specified adjustment type.

        A positive value adds to the current capacity while a negative number removes from the current capacity. For exact capacity, you must specify a non-negative value.

        Required if the policy type is ``SimpleScaling`` . (Not used with any other policy type.)

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scalingpolicy.html#cfn-autoscaling-scalingpolicy-scalingadjustment
        '''
        result = self._values.get("scaling_adjustment")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def step_adjustments(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.StepAdjustmentProperty"]]]]:
        '''A set of adjustments that enable you to scale based on the size of the alarm breach.

        Required if the policy type is ``StepScaling`` . (Not used with any other policy type.)

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scalingpolicy.html#cfn-autoscaling-scalingpolicy-stepadjustments
        '''
        result = self._values.get("step_adjustments")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.StepAdjustmentProperty"]]]], result)

    @builtins.property
    def target_tracking_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.TargetTrackingConfigurationProperty"]]:
        '''A target tracking scaling policy. Provides support for predefined or custom metrics.

        The following predefined metrics are available:

        - ``ASGAverageCPUUtilization``
        - ``ASGAverageNetworkIn``
        - ``ASGAverageNetworkOut``
        - ``ALBRequestCountPerTarget``

        If you specify ``ALBRequestCountPerTarget`` for the metric, you must specify the ``ResourceLabel`` property with the ``PredefinedMetricSpecification`` .

        Required if the policy type is ``TargetTrackingScaling`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scalingpolicy.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration
        '''
        result = self._values.get("target_tracking_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.TargetTrackingConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnScalingPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnScalingPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScalingPolicyPropsMixin",
):
    '''The ``AWS::AutoScaling::ScalingPolicy`` resource specifies an Amazon EC2 Auto Scaling scaling policy so that the Auto Scaling group can scale the number of instances available for your application.

    For more information about using scaling policies to scale your Auto Scaling group automatically, see `Dynamic scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scale-based-on-demand.html>`_ and `Predictive scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-predictive-scaling.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scalingpolicy.html
    :cloudformationResource: AWS::AutoScaling::ScalingPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
        
        cfn_scaling_policy_props_mixin = autoscaling_mixins.CfnScalingPolicyPropsMixin(autoscaling_mixins.CfnScalingPolicyMixinProps(
            adjustment_type="adjustmentType",
            auto_scaling_group_name="autoScalingGroupName",
            cooldown="cooldown",
            estimated_instance_warmup=123,
            metric_aggregation_type="metricAggregationType",
            min_adjustment_magnitude=123,
            policy_type="policyType",
            predictive_scaling_configuration=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingConfigurationProperty(
                max_capacity_breach_behavior="maxCapacityBreachBehavior",
                max_capacity_buffer=123,
                metric_specifications=[autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricSpecificationProperty(
                    customized_capacity_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedCapacityMetricProperty(
                        metric_data_queries=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDataQueryProperty(
                            expression="expression",
                            id="id",
                            label="label",
                            metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricStatProperty(
                                metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                                    dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )]
                    ),
                    customized_load_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedLoadMetricProperty(
                        metric_data_queries=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDataQueryProperty(
                            expression="expression",
                            id="id",
                            label="label",
                            metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricStatProperty(
                                metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                                    dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )]
                    ),
                    customized_scaling_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedScalingMetricProperty(
                        metric_data_queries=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDataQueryProperty(
                            expression="expression",
                            id="id",
                            label="label",
                            metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricStatProperty(
                                metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                                    dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )]
                    ),
                    predefined_load_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedLoadMetricProperty(
                        predefined_metric_type="predefinedMetricType",
                        resource_label="resourceLabel"
                    ),
                    predefined_metric_pair_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedMetricPairProperty(
                        predefined_metric_type="predefinedMetricType",
                        resource_label="resourceLabel"
                    ),
                    predefined_scaling_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedScalingMetricProperty(
                        predefined_metric_type="predefinedMetricType",
                        resource_label="resourceLabel"
                    ),
                    target_value=123
                )],
                mode="mode",
                scheduling_buffer_time=123
            ),
            scaling_adjustment=123,
            step_adjustments=[autoscaling_mixins.CfnScalingPolicyPropsMixin.StepAdjustmentProperty(
                metric_interval_lower_bound=123,
                metric_interval_upper_bound=123,
                scaling_adjustment=123
            )],
            target_tracking_configuration=autoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingConfigurationProperty(
                customized_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.CustomizedMetricSpecificationProperty(
                    dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                        name="name",
                        value="value"
                    )],
                    metric_name="metricName",
                    metrics=[autoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDataQueryProperty(
                        expression="expression",
                        id="id",
                        label="label",
                        metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty(
                            metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                                dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                    name="name",
                                    value="value"
                                )],
                                metric_name="metricName",
                                namespace="namespace"
                            ),
                            period=123,
                            stat="stat",
                            unit="unit"
                        ),
                        period=123,
                        return_data=False
                    )],
                    namespace="namespace",
                    period=123,
                    statistic="statistic",
                    unit="unit"
                ),
                disable_scale_in=False,
                predefined_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredefinedMetricSpecificationProperty(
                    predefined_metric_type="predefinedMetricType",
                    resource_label="resourceLabel"
                ),
                target_value=123
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnScalingPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AutoScaling::ScalingPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__626f59fdada379cf43df75058ec2c21b0f11170327460ea379d56c3c99e87273)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        options = _CfnPropertyMixinOptions_9cbff649(strategy=strategy)

        jsii.create(self.__class__, self, [props, options])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply the mixin properties to the construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d2cbaca1650c158d9361d2ce0b38458633a60880d992d858c1cf7aa4ec5764b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c1b8f99162eeefd0d6586276c1976760ea9a048a4591472d53fdf184b98e94)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnScalingPolicyMixinProps:
        return typing.cast(CfnScalingPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScalingPolicyPropsMixin.CustomizedMetricSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimensions": "dimensions",
            "metric_name": "metricName",
            "metrics": "metrics",
            "namespace": "namespace",
            "period": "period",
            "statistic": "statistic",
            "unit": "unit",
        },
    )
    class CustomizedMetricSpecificationProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.MetricDimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            metric_name: typing.Optional[builtins.str] = None,
            metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.TargetTrackingMetricDataQueryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            namespace: typing.Optional[builtins.str] = None,
            period: typing.Optional[jsii.Number] = None,
            statistic: typing.Optional[builtins.str] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains customized metric specification information for a target tracking scaling policy for Amazon EC2 Auto Scaling.

            To create your customized metric specification:

            - Add values for each required property from CloudWatch. You can use an existing metric, or a new metric that you create. To use your own metric, you must first publish the metric to CloudWatch. For more information, see `Publish Custom Metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html>`_ in the *Amazon CloudWatch User Guide* .
            - Choose a metric that changes proportionally with capacity. The value of the metric should increase or decrease in inverse proportion to the number of capacity units. That is, the value of the metric should decrease when capacity increases.

            For more information about CloudWatch, see `Amazon CloudWatch Concepts <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html>`_ .

            ``CustomizedMetricSpecification`` is a property of the `AWS::AutoScaling::ScalingPolicy TargetTrackingConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html>`_ property type.

            :param dimensions: The dimensions of the metric. Conditional: If you published your metric with dimensions, you must specify the same dimensions in your scaling policy.
            :param metric_name: The name of the metric. To get the exact metric name, namespace, and dimensions, inspect the `Metric <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_Metric.html>`_ object that is returned by a call to `ListMetrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_ListMetrics.html>`_ .
            :param metrics: The metrics to include in the target tracking scaling policy, as a metric data query. This can include both raw metric and metric math expressions.
            :param namespace: The namespace of the metric.
            :param period: The period of the metric in seconds. The default value is 60. Accepted values are 10, 30, and 60. For high resolution metric, set the value to less than 60. For more information, see `Create a target tracking policy using high-resolution metrics for faster response <https://docs.aws.amazon.com/autoscaling/ec2/userguide/policy-creating-high-resolution-metrics.html>`_ .
            :param statistic: The statistic of the metric.
            :param unit: The unit of the metric. For a complete list of the units that CloudWatch supports, see the `MetricDatum <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDatum.html>`_ data type in the *Amazon CloudWatch API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                customized_metric_specification_property = autoscaling_mixins.CfnScalingPolicyPropsMixin.CustomizedMetricSpecificationProperty(
                    dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                        name="name",
                        value="value"
                    )],
                    metric_name="metricName",
                    metrics=[autoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDataQueryProperty(
                        expression="expression",
                        id="id",
                        label="label",
                        metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty(
                            metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                                dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                    name="name",
                                    value="value"
                                )],
                                metric_name="metricName",
                                namespace="namespace"
                            ),
                            period=123,
                            stat="stat",
                            unit="unit"
                        ),
                        period=123,
                        return_data=False
                    )],
                    namespace="namespace",
                    period=123,
                    statistic="statistic",
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3e12f006b0109585b541fe6aa803f6ba9ed04edae31812a9e04e813121530a96)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
                check_type(argname="argument period", value=period, expected_type=type_hints["period"])
                check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if metrics is not None:
                self._values["metrics"] = metrics
            if namespace is not None:
                self._values["namespace"] = namespace
            if period is not None:
                self._values["period"] = period
            if statistic is not None:
                self._values["statistic"] = statistic
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.MetricDimensionProperty"]]]]:
            '''The dimensions of the metric.

            Conditional: If you published your metric with dimensions, you must specify the same dimensions in your scaling policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.MetricDimensionProperty"]]]], result)

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''The name of the metric.

            To get the exact metric name, namespace, and dimensions, inspect the `Metric <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_Metric.html>`_ object that is returned by a call to `ListMetrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_ListMetrics.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.TargetTrackingMetricDataQueryProperty"]]]]:
            '''The metrics to include in the target tracking scaling policy, as a metric data query.

            This can include both raw metric and metric math expressions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-metrics
            '''
            result = self._values.get("metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.TargetTrackingMetricDataQueryProperty"]]]], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The namespace of the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def period(self) -> typing.Optional[jsii.Number]:
            '''The period of the metric in seconds.

            The default value is 60. Accepted values are 10, 30, and 60. For high resolution metric, set the value to less than 60. For more information, see `Create a target tracking policy using high-resolution metrics for faster response <https://docs.aws.amazon.com/autoscaling/ec2/userguide/policy-creating-high-resolution-metrics.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-period
            '''
            result = self._values.get("period")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def statistic(self) -> typing.Optional[builtins.str]:
            '''The statistic of the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-statistic
            '''
            result = self._values.get("statistic")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit of the metric.

            For a complete list of the units that CloudWatch supports, see the `MetricDatum <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDatum.html>`_ data type in the *Amazon CloudWatch API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomizedMetricSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScalingPolicyPropsMixin.MetricDataQueryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "expression": "expression",
            "id": "id",
            "label": "label",
            "metric_stat": "metricStat",
            "return_data": "returnData",
        },
    )
    class MetricDataQueryProperty:
        def __init__(
            self,
            *,
            expression: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            label: typing.Optional[builtins.str] = None,
            metric_stat: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.MetricStatProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            return_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The metric data to return.

            Also defines whether this call is returning data for one metric only, or whether it is performing a math expression on the values of returned metric statistics to create a new time series. A time series is a series of data points, each of which is associated with a timestamp.

            ``MetricDataQuery`` is a property of the following property types:

            - `AWS::AutoScaling::ScalingPolicy PredictiveScalingCustomizedScalingMetric <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingcustomizedscalingmetric.html>`_
            - `AWS::AutoScaling::ScalingPolicy PredictiveScalingCustomizedLoadMetric <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingcustomizedloadmetric.html>`_
            - `AWS::AutoScaling::ScalingPolicy PredictiveScalingCustomizedCapacityMetric <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingcustomizedcapacitymetric.html>`_

            Predictive scaling uses the time series data received from CloudWatch to understand how to schedule capacity based on your historical workload patterns.

            You can call for a single metric or perform math expressions on multiple metrics. Any expressions used in a metric specification must eventually return a single time series.

            For more information and examples, see `Advanced predictive scaling policy configurations using custom metrics <https://docs.aws.amazon.com/autoscaling/ec2/userguide/predictive-scaling-customized-metric-specification.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

            :param expression: The math expression to perform on the returned data, if this object is performing a math expression. This expression can use the ``Id`` of the other metrics to refer to those metrics, and can also use the ``Id`` of other expressions to use the result of those expressions. Conditional: Within each ``MetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` , but not both.
            :param id: A short name that identifies the object's results in the response. This name must be unique among all ``MetricDataQuery`` objects specified for a single scaling policy. If you are performing math expressions on this set of data, this name represents that data and can serve as a variable in the mathematical expression. The valid characters are letters, numbers, and underscores. The first character must be a lowercase letter.
            :param label: A human-readable label for this metric or expression. This is especially useful if this is a math expression, so that you know what the value represents.
            :param metric_stat: Information about the metric data to return. Conditional: Within each ``MetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` , but not both.
            :param return_data: Indicates whether to return the timestamps and raw data values of this metric. If you use any math expressions, specify ``true`` for this value for only the final math expression that the metric specification is based on. You must specify ``false`` for ``ReturnData`` for all the other metrics and expressions used in the metric specification. If you are only retrieving metrics and not performing any math expressions, do not specify anything for ``ReturnData`` . This sets it to its default ( ``true`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricdataquery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                metric_data_query_property = autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDataQueryProperty(
                    expression="expression",
                    id="id",
                    label="label",
                    metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricStatProperty(
                        metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                            dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                name="name",
                                value="value"
                            )],
                            metric_name="metricName",
                            namespace="namespace"
                        ),
                        stat="stat",
                        unit="unit"
                    ),
                    return_data=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7827e38e69fe15a8fd10b9b5f981f78729522faa0d2aa923a48f5cb2ae53b3e9)
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument label", value=label, expected_type=type_hints["label"])
                check_type(argname="argument metric_stat", value=metric_stat, expected_type=type_hints["metric_stat"])
                check_type(argname="argument return_data", value=return_data, expected_type=type_hints["return_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if expression is not None:
                self._values["expression"] = expression
            if id is not None:
                self._values["id"] = id
            if label is not None:
                self._values["label"] = label
            if metric_stat is not None:
                self._values["metric_stat"] = metric_stat
            if return_data is not None:
                self._values["return_data"] = return_data

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''The math expression to perform on the returned data, if this object is performing a math expression.

            This expression can use the ``Id`` of the other metrics to refer to those metrics, and can also use the ``Id`` of other expressions to use the result of those expressions.

            Conditional: Within each ``MetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` , but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricdataquery.html#cfn-autoscaling-scalingpolicy-metricdataquery-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A short name that identifies the object's results in the response.

            This name must be unique among all ``MetricDataQuery`` objects specified for a single scaling policy. If you are performing math expressions on this set of data, this name represents that data and can serve as a variable in the mathematical expression. The valid characters are letters, numbers, and underscores. The first character must be a lowercase letter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricdataquery.html#cfn-autoscaling-scalingpolicy-metricdataquery-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def label(self) -> typing.Optional[builtins.str]:
            '''A human-readable label for this metric or expression.

            This is especially useful if this is a math expression, so that you know what the value represents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricdataquery.html#cfn-autoscaling-scalingpolicy-metricdataquery-label
            '''
            result = self._values.get("label")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_stat(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.MetricStatProperty"]]:
            '''Information about the metric data to return.

            Conditional: Within each ``MetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` , but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricdataquery.html#cfn-autoscaling-scalingpolicy-metricdataquery-metricstat
            '''
            result = self._values.get("metric_stat")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.MetricStatProperty"]], result)

        @builtins.property
        def return_data(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether to return the timestamps and raw data values of this metric.

            If you use any math expressions, specify ``true`` for this value for only the final math expression that the metric specification is based on. You must specify ``false`` for ``ReturnData`` for all the other metrics and expressions used in the metric specification.

            If you are only retrieving metrics and not performing any math expressions, do not specify anything for ``ReturnData`` . This sets it to its default ( ``true`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricdataquery.html#cfn-autoscaling-scalingpolicy-metricdataquery-returndata
            '''
            result = self._values.get("return_data")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricDataQueryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class MetricDimensionProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``MetricDimension`` specifies a name/value pair that is part of the identity of a CloudWatch metric for the ``Dimensions`` property of the `AWS::AutoScaling::ScalingPolicy CustomizedMetricSpecification <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html>`_ property type. Duplicate dimensions are not allowed.

            :param name: The name of the dimension.
            :param value: The value of the dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricdimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                metric_dimension_property = autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b8b95e6fbe31e689335ef892f5b2cf8940ccd4eb1b9d1538da833dd88a1f27a1)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricdimension.html#cfn-autoscaling-scalingpolicy-metricdimension-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricdimension.html#cfn-autoscaling-scalingpolicy-metricdimension-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScalingPolicyPropsMixin.MetricProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimensions": "dimensions",
            "metric_name": "metricName",
            "namespace": "namespace",
        },
    )
    class MetricProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.MetricDimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            metric_name: typing.Optional[builtins.str] = None,
            namespace: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents a specific metric.

            ``Metric`` is a property of the `AWS::AutoScaling::ScalingPolicy MetricStat <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricstat.html>`_ property type.

            :param dimensions: The dimensions for the metric. For the list of available dimensions, see the AWS documentation available from the table in `AWS services that publish CloudWatch metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html>`_ in the *Amazon CloudWatch User Guide* . Conditional: If you published your metric with dimensions, you must specify the same dimensions in your scaling policy.
            :param metric_name: The name of the metric.
            :param namespace: The namespace of the metric. For more information, see the table in `AWS services that publish CloudWatch metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html>`_ in the *Amazon CloudWatch User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                metric_property = autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                    dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                        name="name",
                        value="value"
                    )],
                    metric_name="metricName",
                    namespace="namespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b6fa359a022d1779a019c46c53309cefc3e789ffb19c7be1db86c3fa633968da)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if namespace is not None:
                self._values["namespace"] = namespace

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.MetricDimensionProperty"]]]]:
            '''The dimensions for the metric.

            For the list of available dimensions, see the AWS documentation available from the table in `AWS services that publish CloudWatch metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html>`_ in the *Amazon CloudWatch User Guide* .

            Conditional: If you published your metric with dimensions, you must specify the same dimensions in your scaling policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metric.html#cfn-autoscaling-scalingpolicy-metric-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.MetricDimensionProperty"]]]], result)

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''The name of the metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metric.html#cfn-autoscaling-scalingpolicy-metric-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The namespace of the metric.

            For more information, see the table in `AWS services that publish CloudWatch metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html>`_ in the *Amazon CloudWatch User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metric.html#cfn-autoscaling-scalingpolicy-metric-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScalingPolicyPropsMixin.MetricStatProperty",
        jsii_struct_bases=[],
        name_mapping={"metric": "metric", "stat": "stat", "unit": "unit"},
    )
    class MetricStatProperty:
        def __init__(
            self,
            *,
            metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.MetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            stat: typing.Optional[builtins.str] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``MetricStat`` is a property of the `AWS::AutoScaling::ScalingPolicy MetricDataQuery <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricdataquery.html>`_ property type.

            This structure defines the CloudWatch metric to return, along with the statistic and unit.

            For more information about the CloudWatch terminology below, see `Amazon CloudWatch concepts <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html>`_ in the *Amazon CloudWatch User Guide* .

            :param metric: The CloudWatch metric to return, including the metric name, namespace, and dimensions. To get the exact metric name, namespace, and dimensions, inspect the `Metric <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_Metric.html>`_ object that is returned by a call to `ListMetrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_ListMetrics.html>`_ .
            :param stat: The statistic to return. It can include any CloudWatch statistic or extended statistic. For a list of valid values, see the table in `Statistics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Statistic>`_ in the *Amazon CloudWatch User Guide* . The most commonly used metrics for predictive scaling are ``Average`` and ``Sum`` .
            :param unit: The unit to use for the returned data points. For a complete list of the units that CloudWatch supports, see the `MetricDatum <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDatum.html>`_ data type in the *Amazon CloudWatch API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricstat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                metric_stat_property = autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricStatProperty(
                    metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                        dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                            name="name",
                            value="value"
                        )],
                        metric_name="metricName",
                        namespace="namespace"
                    ),
                    stat="stat",
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0325b9064c114ca27ca564659302b13797c5b8395fecc8b33da51c37f3d79f2e)
                check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
                check_type(argname="argument stat", value=stat, expected_type=type_hints["stat"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric is not None:
                self._values["metric"] = metric
            if stat is not None:
                self._values["stat"] = stat
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def metric(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.MetricProperty"]]:
            '''The CloudWatch metric to return, including the metric name, namespace, and dimensions.

            To get the exact metric name, namespace, and dimensions, inspect the `Metric <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_Metric.html>`_ object that is returned by a call to `ListMetrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_ListMetrics.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricstat.html#cfn-autoscaling-scalingpolicy-metricstat-metric
            '''
            result = self._values.get("metric")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.MetricProperty"]], result)

        @builtins.property
        def stat(self) -> typing.Optional[builtins.str]:
            '''The statistic to return.

            It can include any CloudWatch statistic or extended statistic. For a list of valid values, see the table in `Statistics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Statistic>`_ in the *Amazon CloudWatch User Guide* .

            The most commonly used metrics for predictive scaling are ``Average`` and ``Sum`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricstat.html#cfn-autoscaling-scalingpolicy-metricstat-stat
            '''
            result = self._values.get("stat")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit to use for the returned data points.

            For a complete list of the units that CloudWatch supports, see the `MetricDatum <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDatum.html>`_ data type in the *Amazon CloudWatch API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricstat.html#cfn-autoscaling-scalingpolicy-metricstat-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricStatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScalingPolicyPropsMixin.PredefinedMetricSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "predefined_metric_type": "predefinedMetricType",
            "resource_label": "resourceLabel",
        },
    )
    class PredefinedMetricSpecificationProperty:
        def __init__(
            self,
            *,
            predefined_metric_type: typing.Optional[builtins.str] = None,
            resource_label: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains predefined metric specification information for a target tracking scaling policy for Amazon EC2 Auto Scaling.

            ``PredefinedMetricSpecification`` is a property of the `AWS::AutoScaling::ScalingPolicy TargetTrackingConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html>`_ property type.

            :param predefined_metric_type: The metric type. The following predefined metrics are available:. - ``ASGAverageCPUUtilization`` - Average CPU utilization of the Auto Scaling group. - ``ASGAverageNetworkIn`` - Average number of bytes received on all network interfaces by the Auto Scaling group. - ``ASGAverageNetworkOut`` - Average number of bytes sent out on all network interfaces by the Auto Scaling group. - ``ALBRequestCountPerTarget`` - Average Application Load Balancer request count per target for your Auto Scaling group.
            :param resource_label: A label that uniquely identifies a specific Application Load Balancer target group from which to determine the average request count served by your Auto Scaling group. You can't specify a resource label unless the target group is attached to the Auto Scaling group. You create the resource label by appending the final portion of the load balancer ARN and the final portion of the target group ARN into a single value, separated by a forward slash (/). The format of the resource label is: ``app/my-alb/778d41231b141a0f/targetgroup/my-alb-target-group/943f017f100becff`` . Where: - app// is the final portion of the load balancer ARN - targetgroup// is the final portion of the target group ARN. To find the ARN for an Application Load Balancer, use the `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html>`_ API operation. To find the ARN for the target group, use the `DescribeTargetGroups <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeTargetGroups.html>`_ API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predefinedmetricspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                predefined_metric_specification_property = autoscaling_mixins.CfnScalingPolicyPropsMixin.PredefinedMetricSpecificationProperty(
                    predefined_metric_type="predefinedMetricType",
                    resource_label="resourceLabel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9c2d30fdbbe1726ab2d122f9228257cce204cc96aaa2a9985477f961a01d4595)
                check_type(argname="argument predefined_metric_type", value=predefined_metric_type, expected_type=type_hints["predefined_metric_type"])
                check_type(argname="argument resource_label", value=resource_label, expected_type=type_hints["resource_label"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if predefined_metric_type is not None:
                self._values["predefined_metric_type"] = predefined_metric_type
            if resource_label is not None:
                self._values["resource_label"] = resource_label

        @builtins.property
        def predefined_metric_type(self) -> typing.Optional[builtins.str]:
            '''The metric type. The following predefined metrics are available:.

            - ``ASGAverageCPUUtilization`` - Average CPU utilization of the Auto Scaling group.
            - ``ASGAverageNetworkIn`` - Average number of bytes received on all network interfaces by the Auto Scaling group.
            - ``ASGAverageNetworkOut`` - Average number of bytes sent out on all network interfaces by the Auto Scaling group.
            - ``ALBRequestCountPerTarget`` - Average Application Load Balancer request count per target for your Auto Scaling group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predefinedmetricspecification.html#cfn-autoscaling-scalingpolicy-predefinedmetricspecification-predefinedmetrictype
            '''
            result = self._values.get("predefined_metric_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_label(self) -> typing.Optional[builtins.str]:
            '''A label that uniquely identifies a specific Application Load Balancer target group from which to determine the average request count served by your Auto Scaling group.

            You can't specify a resource label unless the target group is attached to the Auto Scaling group.

            You create the resource label by appending the final portion of the load balancer ARN and the final portion of the target group ARN into a single value, separated by a forward slash (/). The format of the resource label is:

            ``app/my-alb/778d41231b141a0f/targetgroup/my-alb-target-group/943f017f100becff`` .

            Where:

            - app// is the final portion of the load balancer ARN
            - targetgroup// is the final portion of the target group ARN.

            To find the ARN for an Application Load Balancer, use the `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html>`_ API operation. To find the ARN for the target group, use the `DescribeTargetGroups <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeTargetGroups.html>`_ API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predefinedmetricspecification.html#cfn-autoscaling-scalingpolicy-predefinedmetricspecification-resourcelabel
            '''
            result = self._values.get("resource_label")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredefinedMetricSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScalingPolicyPropsMixin.PredictiveScalingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_capacity_breach_behavior": "maxCapacityBreachBehavior",
            "max_capacity_buffer": "maxCapacityBuffer",
            "metric_specifications": "metricSpecifications",
            "mode": "mode",
            "scheduling_buffer_time": "schedulingBufferTime",
        },
    )
    class PredictiveScalingConfigurationProperty:
        def __init__(
            self,
            *,
            max_capacity_breach_behavior: typing.Optional[builtins.str] = None,
            max_capacity_buffer: typing.Optional[jsii.Number] = None,
            metric_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingMetricSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            mode: typing.Optional[builtins.str] = None,
            scheduling_buffer_time: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``PredictiveScalingConfiguration`` is a property of the `AWS::AutoScaling::ScalingPolicy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scalingpolicy.html>`_ resource that specifies a predictive scaling policy for Amazon EC2 Auto Scaling.

            For more information, see `Predictive scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-predictive-scaling.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

            :param max_capacity_breach_behavior: Defines the behavior that should be applied if the forecast capacity approaches or exceeds the maximum capacity of the Auto Scaling group. Defaults to ``HonorMaxCapacity`` if not specified. The following are possible values: - ``HonorMaxCapacity`` - Amazon EC2 Auto Scaling can't increase the maximum capacity of the group when the forecast capacity is close to or exceeds the maximum capacity. - ``IncreaseMaxCapacity`` - Amazon EC2 Auto Scaling can increase the maximum capacity of the group when the forecast capacity is close to or exceeds the maximum capacity. The upper limit is determined by the forecasted capacity and the value for ``MaxCapacityBuffer`` . .. epigraph:: Use caution when allowing the maximum capacity to be automatically increased. This can lead to more instances being launched than intended if the increased maximum capacity is not monitored and managed. The increased maximum capacity then becomes the new normal maximum capacity for the Auto Scaling group until you manually update it. The maximum capacity does not automatically decrease back to the original maximum.
            :param max_capacity_buffer: The size of the capacity buffer to use when the forecast capacity is close to or exceeds the maximum capacity. The value is specified as a percentage relative to the forecast capacity. For example, if the buffer is 10, this means a 10 percent buffer, such that if the forecast capacity is 50, and the maximum capacity is 40, then the effective maximum capacity is 55. If set to 0, Amazon EC2 Auto Scaling may scale capacity higher than the maximum capacity to equal but not exceed forecast capacity. Required if the ``MaxCapacityBreachBehavior`` property is set to ``IncreaseMaxCapacity`` , and cannot be used otherwise.
            :param metric_specifications: This structure includes the metrics and target utilization to use for predictive scaling. This is an array, but we currently only support a single metric specification. That is, you can specify a target value and a single metric pair, or a target value and one scaling metric and one load metric.
            :param mode: The predictive scaling mode. Defaults to ``ForecastOnly`` if not specified.
            :param scheduling_buffer_time: The amount of time, in seconds, by which the instance launch time can be advanced. For example, the forecast says to add capacity at 10:00 AM, and you choose to pre-launch instances by 5 minutes. In that case, the instances will be launched at 9:55 AM. The intention is to give resources time to be provisioned. It can take a few minutes to launch an EC2 instance. The actual amount of time required depends on several factors, such as the size of the instance and whether there are startup scripts to complete. The value must be less than the forecast interval duration of 3600 seconds (60 minutes). Defaults to 300 seconds if not specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                predictive_scaling_configuration_property = autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingConfigurationProperty(
                    max_capacity_breach_behavior="maxCapacityBreachBehavior",
                    max_capacity_buffer=123,
                    metric_specifications=[autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricSpecificationProperty(
                        customized_capacity_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedCapacityMetricProperty(
                            metric_data_queries=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDataQueryProperty(
                                expression="expression",
                                id="id",
                                label="label",
                                metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricStatProperty(
                                    metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                                        dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                            name="name",
                                            value="value"
                                        )],
                                        metric_name="metricName",
                                        namespace="namespace"
                                    ),
                                    stat="stat",
                                    unit="unit"
                                ),
                                return_data=False
                            )]
                        ),
                        customized_load_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedLoadMetricProperty(
                            metric_data_queries=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDataQueryProperty(
                                expression="expression",
                                id="id",
                                label="label",
                                metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricStatProperty(
                                    metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                                        dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                            name="name",
                                            value="value"
                                        )],
                                        metric_name="metricName",
                                        namespace="namespace"
                                    ),
                                    stat="stat",
                                    unit="unit"
                                ),
                                return_data=False
                            )]
                        ),
                        customized_scaling_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedScalingMetricProperty(
                            metric_data_queries=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDataQueryProperty(
                                expression="expression",
                                id="id",
                                label="label",
                                metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricStatProperty(
                                    metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                                        dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                            name="name",
                                            value="value"
                                        )],
                                        metric_name="metricName",
                                        namespace="namespace"
                                    ),
                                    stat="stat",
                                    unit="unit"
                                ),
                                return_data=False
                            )]
                        ),
                        predefined_load_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedLoadMetricProperty(
                            predefined_metric_type="predefinedMetricType",
                            resource_label="resourceLabel"
                        ),
                        predefined_metric_pair_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedMetricPairProperty(
                            predefined_metric_type="predefinedMetricType",
                            resource_label="resourceLabel"
                        ),
                        predefined_scaling_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedScalingMetricProperty(
                            predefined_metric_type="predefinedMetricType",
                            resource_label="resourceLabel"
                        ),
                        target_value=123
                    )],
                    mode="mode",
                    scheduling_buffer_time=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7e469a14daceef9874db667bc97d0d4d1649ee15a59cf04c8d4d9665f9eb1cc4)
                check_type(argname="argument max_capacity_breach_behavior", value=max_capacity_breach_behavior, expected_type=type_hints["max_capacity_breach_behavior"])
                check_type(argname="argument max_capacity_buffer", value=max_capacity_buffer, expected_type=type_hints["max_capacity_buffer"])
                check_type(argname="argument metric_specifications", value=metric_specifications, expected_type=type_hints["metric_specifications"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument scheduling_buffer_time", value=scheduling_buffer_time, expected_type=type_hints["scheduling_buffer_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_capacity_breach_behavior is not None:
                self._values["max_capacity_breach_behavior"] = max_capacity_breach_behavior
            if max_capacity_buffer is not None:
                self._values["max_capacity_buffer"] = max_capacity_buffer
            if metric_specifications is not None:
                self._values["metric_specifications"] = metric_specifications
            if mode is not None:
                self._values["mode"] = mode
            if scheduling_buffer_time is not None:
                self._values["scheduling_buffer_time"] = scheduling_buffer_time

        @builtins.property
        def max_capacity_breach_behavior(self) -> typing.Optional[builtins.str]:
            '''Defines the behavior that should be applied if the forecast capacity approaches or exceeds the maximum capacity of the Auto Scaling group.

            Defaults to ``HonorMaxCapacity`` if not specified.

            The following are possible values:

            - ``HonorMaxCapacity`` - Amazon EC2 Auto Scaling can't increase the maximum capacity of the group when the forecast capacity is close to or exceeds the maximum capacity.
            - ``IncreaseMaxCapacity`` - Amazon EC2 Auto Scaling can increase the maximum capacity of the group when the forecast capacity is close to or exceeds the maximum capacity. The upper limit is determined by the forecasted capacity and the value for ``MaxCapacityBuffer`` .

            .. epigraph::

               Use caution when allowing the maximum capacity to be automatically increased. This can lead to more instances being launched than intended if the increased maximum capacity is not monitored and managed. The increased maximum capacity then becomes the new normal maximum capacity for the Auto Scaling group until you manually update it. The maximum capacity does not automatically decrease back to the original maximum.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingconfiguration.html#cfn-autoscaling-scalingpolicy-predictivescalingconfiguration-maxcapacitybreachbehavior
            '''
            result = self._values.get("max_capacity_breach_behavior")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_capacity_buffer(self) -> typing.Optional[jsii.Number]:
            '''The size of the capacity buffer to use when the forecast capacity is close to or exceeds the maximum capacity.

            The value is specified as a percentage relative to the forecast capacity. For example, if the buffer is 10, this means a 10 percent buffer, such that if the forecast capacity is 50, and the maximum capacity is 40, then the effective maximum capacity is 55.

            If set to 0, Amazon EC2 Auto Scaling may scale capacity higher than the maximum capacity to equal but not exceed forecast capacity.

            Required if the ``MaxCapacityBreachBehavior`` property is set to ``IncreaseMaxCapacity`` , and cannot be used otherwise.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingconfiguration.html#cfn-autoscaling-scalingpolicy-predictivescalingconfiguration-maxcapacitybuffer
            '''
            result = self._values.get("max_capacity_buffer")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def metric_specifications(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingMetricSpecificationProperty"]]]]:
            '''This structure includes the metrics and target utilization to use for predictive scaling.

            This is an array, but we currently only support a single metric specification. That is, you can specify a target value and a single metric pair, or a target value and one scaling metric and one load metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingconfiguration.html#cfn-autoscaling-scalingpolicy-predictivescalingconfiguration-metricspecifications
            '''
            result = self._values.get("metric_specifications")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingMetricSpecificationProperty"]]]], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''The predictive scaling mode.

            Defaults to ``ForecastOnly`` if not specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingconfiguration.html#cfn-autoscaling-scalingpolicy-predictivescalingconfiguration-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scheduling_buffer_time(self) -> typing.Optional[jsii.Number]:
            '''The amount of time, in seconds, by which the instance launch time can be advanced.

            For example, the forecast says to add capacity at 10:00 AM, and you choose to pre-launch instances by 5 minutes. In that case, the instances will be launched at 9:55 AM. The intention is to give resources time to be provisioned. It can take a few minutes to launch an EC2 instance. The actual amount of time required depends on several factors, such as the size of the instance and whether there are startup scripts to complete.

            The value must be less than the forecast interval duration of 3600 seconds (60 minutes). Defaults to 300 seconds if not specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingconfiguration.html#cfn-autoscaling-scalingpolicy-predictivescalingconfiguration-schedulingbuffertime
            '''
            result = self._values.get("scheduling_buffer_time")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveScalingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedCapacityMetricProperty",
        jsii_struct_bases=[],
        name_mapping={"metric_data_queries": "metricDataQueries"},
    )
    class PredictiveScalingCustomizedCapacityMetricProperty:
        def __init__(
            self,
            *,
            metric_data_queries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.MetricDataQueryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains capacity metric information for the ``CustomizedCapacityMetricSpecification`` property of the `AWS::AutoScaling::ScalingPolicy PredictiveScalingMetricSpecification <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingmetricspecification.html>`_ property type.

            :param metric_data_queries: One or more metric data queries to provide the data points for a capacity metric. Use multiple metric data queries only if you are performing a math expression on returned data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingcustomizedcapacitymetric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                predictive_scaling_customized_capacity_metric_property = autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedCapacityMetricProperty(
                    metric_data_queries=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDataQueryProperty(
                        expression="expression",
                        id="id",
                        label="label",
                        metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricStatProperty(
                            metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                                dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                    name="name",
                                    value="value"
                                )],
                                metric_name="metricName",
                                namespace="namespace"
                            ),
                            stat="stat",
                            unit="unit"
                        ),
                        return_data=False
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a31e98734bbaf4015651830a5fe49e1faa0195cbf477d09ee1aff48c18650133)
                check_type(argname="argument metric_data_queries", value=metric_data_queries, expected_type=type_hints["metric_data_queries"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric_data_queries is not None:
                self._values["metric_data_queries"] = metric_data_queries

        @builtins.property
        def metric_data_queries(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.MetricDataQueryProperty"]]]]:
            '''One or more metric data queries to provide the data points for a capacity metric.

            Use multiple metric data queries only if you are performing a math expression on returned data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingcustomizedcapacitymetric.html#cfn-autoscaling-scalingpolicy-predictivescalingcustomizedcapacitymetric-metricdataqueries
            '''
            result = self._values.get("metric_data_queries")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.MetricDataQueryProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveScalingCustomizedCapacityMetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedLoadMetricProperty",
        jsii_struct_bases=[],
        name_mapping={"metric_data_queries": "metricDataQueries"},
    )
    class PredictiveScalingCustomizedLoadMetricProperty:
        def __init__(
            self,
            *,
            metric_data_queries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.MetricDataQueryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains load metric information for the ``CustomizedLoadMetricSpecification`` property of the `AWS::AutoScaling::ScalingPolicy PredictiveScalingMetricSpecification <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingmetricspecification.html>`_ property type.

            :param metric_data_queries: One or more metric data queries to provide the data points for a load metric. Use multiple metric data queries only if you are performing a math expression on returned data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingcustomizedloadmetric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                predictive_scaling_customized_load_metric_property = autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedLoadMetricProperty(
                    metric_data_queries=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDataQueryProperty(
                        expression="expression",
                        id="id",
                        label="label",
                        metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricStatProperty(
                            metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                                dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                    name="name",
                                    value="value"
                                )],
                                metric_name="metricName",
                                namespace="namespace"
                            ),
                            stat="stat",
                            unit="unit"
                        ),
                        return_data=False
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__31ade36ca9544d2554d574311640f588409e85a6199bbfab6742a4a79523b9ca)
                check_type(argname="argument metric_data_queries", value=metric_data_queries, expected_type=type_hints["metric_data_queries"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric_data_queries is not None:
                self._values["metric_data_queries"] = metric_data_queries

        @builtins.property
        def metric_data_queries(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.MetricDataQueryProperty"]]]]:
            '''One or more metric data queries to provide the data points for a load metric.

            Use multiple metric data queries only if you are performing a math expression on returned data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingcustomizedloadmetric.html#cfn-autoscaling-scalingpolicy-predictivescalingcustomizedloadmetric-metricdataqueries
            '''
            result = self._values.get("metric_data_queries")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.MetricDataQueryProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveScalingCustomizedLoadMetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedScalingMetricProperty",
        jsii_struct_bases=[],
        name_mapping={"metric_data_queries": "metricDataQueries"},
    )
    class PredictiveScalingCustomizedScalingMetricProperty:
        def __init__(
            self,
            *,
            metric_data_queries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.MetricDataQueryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains scaling metric information for the ``CustomizedScalingMetricSpecification`` property of the `AWS::AutoScaling::ScalingPolicy PredictiveScalingMetricSpecification <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingmetricspecification.html>`_ property type.

            :param metric_data_queries: One or more metric data queries to provide the data points for a scaling metric. Use multiple metric data queries only if you are performing a math expression on returned data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingcustomizedscalingmetric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                predictive_scaling_customized_scaling_metric_property = autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedScalingMetricProperty(
                    metric_data_queries=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDataQueryProperty(
                        expression="expression",
                        id="id",
                        label="label",
                        metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricStatProperty(
                            metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                                dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                    name="name",
                                    value="value"
                                )],
                                metric_name="metricName",
                                namespace="namespace"
                            ),
                            stat="stat",
                            unit="unit"
                        ),
                        return_data=False
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a24ef42c8040877666fa98c98b8e283cad9d081843fa5b0af2c4cfd479221678)
                check_type(argname="argument metric_data_queries", value=metric_data_queries, expected_type=type_hints["metric_data_queries"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric_data_queries is not None:
                self._values["metric_data_queries"] = metric_data_queries

        @builtins.property
        def metric_data_queries(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.MetricDataQueryProperty"]]]]:
            '''One or more metric data queries to provide the data points for a scaling metric.

            Use multiple metric data queries only if you are performing a math expression on returned data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingcustomizedscalingmetric.html#cfn-autoscaling-scalingpolicy-predictivescalingcustomizedscalingmetric-metricdataqueries
            '''
            result = self._values.get("metric_data_queries")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.MetricDataQueryProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveScalingCustomizedScalingMetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "customized_capacity_metric_specification": "customizedCapacityMetricSpecification",
            "customized_load_metric_specification": "customizedLoadMetricSpecification",
            "customized_scaling_metric_specification": "customizedScalingMetricSpecification",
            "predefined_load_metric_specification": "predefinedLoadMetricSpecification",
            "predefined_metric_pair_specification": "predefinedMetricPairSpecification",
            "predefined_scaling_metric_specification": "predefinedScalingMetricSpecification",
            "target_value": "targetValue",
        },
    )
    class PredictiveScalingMetricSpecificationProperty:
        def __init__(
            self,
            *,
            customized_capacity_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedCapacityMetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            customized_load_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedLoadMetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            customized_scaling_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedScalingMetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            predefined_load_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedLoadMetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            predefined_metric_pair_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedMetricPairProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            predefined_scaling_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedScalingMetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            target_value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A structure that specifies a metric specification for the ``MetricSpecifications`` property of the `AWS::AutoScaling::ScalingPolicy PredictiveScalingConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingconfiguration.html>`_ property type.

            You must specify either a metric pair, or a load metric and a scaling metric individually. Specifying a metric pair instead of individual metrics provides a simpler way to configure metrics for a scaling policy. You choose the metric pair, and the policy automatically knows the correct sum and average statistics to use for the load metric and the scaling metric.

            Example

            - You create a predictive scaling policy and specify ``ALBRequestCount`` as the value for the metric pair and ``1000.0`` as the target value. For this type of metric, you must provide the metric dimension for the corresponding target group, so you also provide a resource label for the Application Load Balancer target group that is attached to your Auto Scaling group.
            - The number of requests the target group receives per minute provides the load metric, and the request count averaged between the members of the target group provides the scaling metric. In CloudWatch, this refers to the ``RequestCount`` and ``RequestCountPerTarget`` metrics, respectively.
            - For optimal use of predictive scaling, you adhere to the best practice of using a dynamic scaling policy to automatically scale between the minimum capacity and maximum capacity in response to real-time changes in resource utilization.
            - Amazon EC2 Auto Scaling consumes data points for the load metric over the last 14 days and creates an hourly load forecast for predictive scaling. (A minimum of 24 hours of data is required.)
            - After creating the load forecast, Amazon EC2 Auto Scaling determines when to reduce or increase the capacity of your Auto Scaling group in each hour of the forecast period so that the average number of requests received by each instance is as close to 1000 requests per minute as possible at all times.

            For information about using custom metrics with predictive scaling, see `Advanced predictive scaling policy configurations using custom metrics <https://docs.aws.amazon.com/autoscaling/ec2/userguide/predictive-scaling-customized-metric-specification.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

            :param customized_capacity_metric_specification: The customized capacity metric specification.
            :param customized_load_metric_specification: The customized load metric specification.
            :param customized_scaling_metric_specification: The customized scaling metric specification.
            :param predefined_load_metric_specification: The predefined load metric specification.
            :param predefined_metric_pair_specification: The predefined metric pair specification from which Amazon EC2 Auto Scaling determines the appropriate scaling metric and load metric to use.
            :param predefined_scaling_metric_specification: The predefined scaling metric specification.
            :param target_value: Specifies the target utilization. .. epigraph:: Some metrics are based on a count instead of a percentage, such as the request count for an Application Load Balancer or the number of messages in an SQS queue. If the scaling policy specifies one of these metrics, specify the target utilization as the optimal average request or message count per instance during any one-minute interval.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingmetricspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                predictive_scaling_metric_specification_property = autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingMetricSpecificationProperty(
                    customized_capacity_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedCapacityMetricProperty(
                        metric_data_queries=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDataQueryProperty(
                            expression="expression",
                            id="id",
                            label="label",
                            metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricStatProperty(
                                metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                                    dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )]
                    ),
                    customized_load_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedLoadMetricProperty(
                        metric_data_queries=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDataQueryProperty(
                            expression="expression",
                            id="id",
                            label="label",
                            metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricStatProperty(
                                metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                                    dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )]
                    ),
                    customized_scaling_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedScalingMetricProperty(
                        metric_data_queries=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDataQueryProperty(
                            expression="expression",
                            id="id",
                            label="label",
                            metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricStatProperty(
                                metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                                    dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )]
                    ),
                    predefined_load_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedLoadMetricProperty(
                        predefined_metric_type="predefinedMetricType",
                        resource_label="resourceLabel"
                    ),
                    predefined_metric_pair_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedMetricPairProperty(
                        predefined_metric_type="predefinedMetricType",
                        resource_label="resourceLabel"
                    ),
                    predefined_scaling_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedScalingMetricProperty(
                        predefined_metric_type="predefinedMetricType",
                        resource_label="resourceLabel"
                    ),
                    target_value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5e99268a01568fa2fa84222e5202606c46deba64e49be381c10783d37a72bc81)
                check_type(argname="argument customized_capacity_metric_specification", value=customized_capacity_metric_specification, expected_type=type_hints["customized_capacity_metric_specification"])
                check_type(argname="argument customized_load_metric_specification", value=customized_load_metric_specification, expected_type=type_hints["customized_load_metric_specification"])
                check_type(argname="argument customized_scaling_metric_specification", value=customized_scaling_metric_specification, expected_type=type_hints["customized_scaling_metric_specification"])
                check_type(argname="argument predefined_load_metric_specification", value=predefined_load_metric_specification, expected_type=type_hints["predefined_load_metric_specification"])
                check_type(argname="argument predefined_metric_pair_specification", value=predefined_metric_pair_specification, expected_type=type_hints["predefined_metric_pair_specification"])
                check_type(argname="argument predefined_scaling_metric_specification", value=predefined_scaling_metric_specification, expected_type=type_hints["predefined_scaling_metric_specification"])
                check_type(argname="argument target_value", value=target_value, expected_type=type_hints["target_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if customized_capacity_metric_specification is not None:
                self._values["customized_capacity_metric_specification"] = customized_capacity_metric_specification
            if customized_load_metric_specification is not None:
                self._values["customized_load_metric_specification"] = customized_load_metric_specification
            if customized_scaling_metric_specification is not None:
                self._values["customized_scaling_metric_specification"] = customized_scaling_metric_specification
            if predefined_load_metric_specification is not None:
                self._values["predefined_load_metric_specification"] = predefined_load_metric_specification
            if predefined_metric_pair_specification is not None:
                self._values["predefined_metric_pair_specification"] = predefined_metric_pair_specification
            if predefined_scaling_metric_specification is not None:
                self._values["predefined_scaling_metric_specification"] = predefined_scaling_metric_specification
            if target_value is not None:
                self._values["target_value"] = target_value

        @builtins.property
        def customized_capacity_metric_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedCapacityMetricProperty"]]:
            '''The customized capacity metric specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingmetricspecification.html#cfn-autoscaling-scalingpolicy-predictivescalingmetricspecification-customizedcapacitymetricspecification
            '''
            result = self._values.get("customized_capacity_metric_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedCapacityMetricProperty"]], result)

        @builtins.property
        def customized_load_metric_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedLoadMetricProperty"]]:
            '''The customized load metric specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingmetricspecification.html#cfn-autoscaling-scalingpolicy-predictivescalingmetricspecification-customizedloadmetricspecification
            '''
            result = self._values.get("customized_load_metric_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedLoadMetricProperty"]], result)

        @builtins.property
        def customized_scaling_metric_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedScalingMetricProperty"]]:
            '''The customized scaling metric specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingmetricspecification.html#cfn-autoscaling-scalingpolicy-predictivescalingmetricspecification-customizedscalingmetricspecification
            '''
            result = self._values.get("customized_scaling_metric_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedScalingMetricProperty"]], result)

        @builtins.property
        def predefined_load_metric_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedLoadMetricProperty"]]:
            '''The predefined load metric specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingmetricspecification.html#cfn-autoscaling-scalingpolicy-predictivescalingmetricspecification-predefinedloadmetricspecification
            '''
            result = self._values.get("predefined_load_metric_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedLoadMetricProperty"]], result)

        @builtins.property
        def predefined_metric_pair_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedMetricPairProperty"]]:
            '''The predefined metric pair specification from which Amazon EC2 Auto Scaling determines the appropriate scaling metric and load metric to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingmetricspecification.html#cfn-autoscaling-scalingpolicy-predictivescalingmetricspecification-predefinedmetricpairspecification
            '''
            result = self._values.get("predefined_metric_pair_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedMetricPairProperty"]], result)

        @builtins.property
        def predefined_scaling_metric_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedScalingMetricProperty"]]:
            '''The predefined scaling metric specification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingmetricspecification.html#cfn-autoscaling-scalingpolicy-predictivescalingmetricspecification-predefinedscalingmetricspecification
            '''
            result = self._values.get("predefined_scaling_metric_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedScalingMetricProperty"]], result)

        @builtins.property
        def target_value(self) -> typing.Optional[jsii.Number]:
            '''Specifies the target utilization.

            .. epigraph::

               Some metrics are based on a count instead of a percentage, such as the request count for an Application Load Balancer or the number of messages in an SQS queue. If the scaling policy specifies one of these metrics, specify the target utilization as the optimal average request or message count per instance during any one-minute interval.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingmetricspecification.html#cfn-autoscaling-scalingpolicy-predictivescalingmetricspecification-targetvalue
            '''
            result = self._values.get("target_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveScalingMetricSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedLoadMetricProperty",
        jsii_struct_bases=[],
        name_mapping={
            "predefined_metric_type": "predefinedMetricType",
            "resource_label": "resourceLabel",
        },
    )
    class PredictiveScalingPredefinedLoadMetricProperty:
        def __init__(
            self,
            *,
            predefined_metric_type: typing.Optional[builtins.str] = None,
            resource_label: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains load metric information for the ``PredefinedLoadMetricSpecification`` property of the `AWS::AutoScaling::ScalingPolicy PredictiveScalingMetricSpecification <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingmetricspecification.html>`_ property type.

            .. epigraph::

               Does not apply to policies that use a *metric pair* for the metric specification.

            :param predefined_metric_type: The metric type.
            :param resource_label: A label that uniquely identifies a specific Application Load Balancer target group from which to determine the request count served by your Auto Scaling group. You can't specify a resource label unless the target group is attached to the Auto Scaling group. You create the resource label by appending the final portion of the load balancer ARN and the final portion of the target group ARN into a single value, separated by a forward slash (/). The format of the resource label is: ``app/my-alb/778d41231b141a0f/targetgroup/my-alb-target-group/943f017f100becff`` . Where: - app// is the final portion of the load balancer ARN - targetgroup// is the final portion of the target group ARN. To find the ARN for an Application Load Balancer, use the `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html>`_ API operation. To find the ARN for the target group, use the `DescribeTargetGroups <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeTargetGroups.html>`_ API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingpredefinedloadmetric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                predictive_scaling_predefined_load_metric_property = autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedLoadMetricProperty(
                    predefined_metric_type="predefinedMetricType",
                    resource_label="resourceLabel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9ac9d2db0e4916aea7221b5277fcfff0d73afdb152a5e070a72b5f674641e80b)
                check_type(argname="argument predefined_metric_type", value=predefined_metric_type, expected_type=type_hints["predefined_metric_type"])
                check_type(argname="argument resource_label", value=resource_label, expected_type=type_hints["resource_label"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if predefined_metric_type is not None:
                self._values["predefined_metric_type"] = predefined_metric_type
            if resource_label is not None:
                self._values["resource_label"] = resource_label

        @builtins.property
        def predefined_metric_type(self) -> typing.Optional[builtins.str]:
            '''The metric type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingpredefinedloadmetric.html#cfn-autoscaling-scalingpolicy-predictivescalingpredefinedloadmetric-predefinedmetrictype
            '''
            result = self._values.get("predefined_metric_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_label(self) -> typing.Optional[builtins.str]:
            '''A label that uniquely identifies a specific Application Load Balancer target group from which to determine the request count served by your Auto Scaling group.

            You can't specify a resource label unless the target group is attached to the Auto Scaling group.

            You create the resource label by appending the final portion of the load balancer ARN and the final portion of the target group ARN into a single value, separated by a forward slash (/). The format of the resource label is:

            ``app/my-alb/778d41231b141a0f/targetgroup/my-alb-target-group/943f017f100becff`` .

            Where:

            - app// is the final portion of the load balancer ARN
            - targetgroup// is the final portion of the target group ARN.

            To find the ARN for an Application Load Balancer, use the `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html>`_ API operation. To find the ARN for the target group, use the `DescribeTargetGroups <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeTargetGroups.html>`_ API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingpredefinedloadmetric.html#cfn-autoscaling-scalingpolicy-predictivescalingpredefinedloadmetric-resourcelabel
            '''
            result = self._values.get("resource_label")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveScalingPredefinedLoadMetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedMetricPairProperty",
        jsii_struct_bases=[],
        name_mapping={
            "predefined_metric_type": "predefinedMetricType",
            "resource_label": "resourceLabel",
        },
    )
    class PredictiveScalingPredefinedMetricPairProperty:
        def __init__(
            self,
            *,
            predefined_metric_type: typing.Optional[builtins.str] = None,
            resource_label: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains metric pair information for the ``PredefinedMetricPairSpecification`` property of the `AWS::AutoScaling::ScalingPolicy PredictiveScalingMetricSpecification <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingmetricspecification.html>`_ property type.

            For more information, see `Predictive scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-predictive-scaling.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

            :param predefined_metric_type: Indicates which metrics to use. There are two different types of metrics for each metric type: one is a load metric and one is a scaling metric. For example, if the metric type is ``ASGCPUUtilization`` , the Auto Scaling group's total CPU metric is used as the load metric, and the average CPU metric is used for the scaling metric.
            :param resource_label: A label that uniquely identifies a specific Application Load Balancer target group from which to determine the total and average request count served by your Auto Scaling group. You can't specify a resource label unless the target group is attached to the Auto Scaling group. You create the resource label by appending the final portion of the load balancer ARN and the final portion of the target group ARN into a single value, separated by a forward slash (/). The format of the resource label is: ``app/my-alb/778d41231b141a0f/targetgroup/my-alb-target-group/943f017f100becff`` . Where: - app// is the final portion of the load balancer ARN - targetgroup// is the final portion of the target group ARN. To find the ARN for an Application Load Balancer, use the `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html>`_ API operation. To find the ARN for the target group, use the `DescribeTargetGroups <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeTargetGroups.html>`_ API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingpredefinedmetricpair.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                predictive_scaling_predefined_metric_pair_property = autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedMetricPairProperty(
                    predefined_metric_type="predefinedMetricType",
                    resource_label="resourceLabel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c3edab15d784b7230377431e9dab18551bbe27a78bc011bed7beeb2a5d31b8d8)
                check_type(argname="argument predefined_metric_type", value=predefined_metric_type, expected_type=type_hints["predefined_metric_type"])
                check_type(argname="argument resource_label", value=resource_label, expected_type=type_hints["resource_label"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if predefined_metric_type is not None:
                self._values["predefined_metric_type"] = predefined_metric_type
            if resource_label is not None:
                self._values["resource_label"] = resource_label

        @builtins.property
        def predefined_metric_type(self) -> typing.Optional[builtins.str]:
            '''Indicates which metrics to use.

            There are two different types of metrics for each metric type: one is a load metric and one is a scaling metric. For example, if the metric type is ``ASGCPUUtilization`` , the Auto Scaling group's total CPU metric is used as the load metric, and the average CPU metric is used for the scaling metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingpredefinedmetricpair.html#cfn-autoscaling-scalingpolicy-predictivescalingpredefinedmetricpair-predefinedmetrictype
            '''
            result = self._values.get("predefined_metric_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_label(self) -> typing.Optional[builtins.str]:
            '''A label that uniquely identifies a specific Application Load Balancer target group from which to determine the total and average request count served by your Auto Scaling group.

            You can't specify a resource label unless the target group is attached to the Auto Scaling group.

            You create the resource label by appending the final portion of the load balancer ARN and the final portion of the target group ARN into a single value, separated by a forward slash (/). The format of the resource label is:

            ``app/my-alb/778d41231b141a0f/targetgroup/my-alb-target-group/943f017f100becff`` .

            Where:

            - app// is the final portion of the load balancer ARN
            - targetgroup// is the final portion of the target group ARN.

            To find the ARN for an Application Load Balancer, use the `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html>`_ API operation. To find the ARN for the target group, use the `DescribeTargetGroups <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeTargetGroups.html>`_ API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingpredefinedmetricpair.html#cfn-autoscaling-scalingpolicy-predictivescalingpredefinedmetricpair-resourcelabel
            '''
            result = self._values.get("resource_label")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveScalingPredefinedMetricPairProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedScalingMetricProperty",
        jsii_struct_bases=[],
        name_mapping={
            "predefined_metric_type": "predefinedMetricType",
            "resource_label": "resourceLabel",
        },
    )
    class PredictiveScalingPredefinedScalingMetricProperty:
        def __init__(
            self,
            *,
            predefined_metric_type: typing.Optional[builtins.str] = None,
            resource_label: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains scaling metric information for the ``PredefinedScalingMetricSpecification`` property of the `AWS::AutoScaling::ScalingPolicy PredictiveScalingMetricSpecification <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingmetricspecification.html>`_ property type.

            .. epigraph::

               Does not apply to policies that use a *metric pair* for the metric specification.

            :param predefined_metric_type: The metric type.
            :param resource_label: A label that uniquely identifies a specific Application Load Balancer target group from which to determine the average request count served by your Auto Scaling group. You can't specify a resource label unless the target group is attached to the Auto Scaling group. You create the resource label by appending the final portion of the load balancer ARN and the final portion of the target group ARN into a single value, separated by a forward slash (/). The format of the resource label is: ``app/my-alb/778d41231b141a0f/targetgroup/my-alb-target-group/943f017f100becff`` . Where: - app// is the final portion of the load balancer ARN - targetgroup// is the final portion of the target group ARN. To find the ARN for an Application Load Balancer, use the `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html>`_ API operation. To find the ARN for the target group, use the `DescribeTargetGroups <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeTargetGroups.html>`_ API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingpredefinedscalingmetric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                predictive_scaling_predefined_scaling_metric_property = autoscaling_mixins.CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedScalingMetricProperty(
                    predefined_metric_type="predefinedMetricType",
                    resource_label="resourceLabel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3801a676f874b6a57ab2453f5a792bc523049ba2b1bb78ddb9f387c8bfe563ba)
                check_type(argname="argument predefined_metric_type", value=predefined_metric_type, expected_type=type_hints["predefined_metric_type"])
                check_type(argname="argument resource_label", value=resource_label, expected_type=type_hints["resource_label"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if predefined_metric_type is not None:
                self._values["predefined_metric_type"] = predefined_metric_type
            if resource_label is not None:
                self._values["resource_label"] = resource_label

        @builtins.property
        def predefined_metric_type(self) -> typing.Optional[builtins.str]:
            '''The metric type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingpredefinedscalingmetric.html#cfn-autoscaling-scalingpolicy-predictivescalingpredefinedscalingmetric-predefinedmetrictype
            '''
            result = self._values.get("predefined_metric_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_label(self) -> typing.Optional[builtins.str]:
            '''A label that uniquely identifies a specific Application Load Balancer target group from which to determine the average request count served by your Auto Scaling group.

            You can't specify a resource label unless the target group is attached to the Auto Scaling group.

            You create the resource label by appending the final portion of the load balancer ARN and the final portion of the target group ARN into a single value, separated by a forward slash (/). The format of the resource label is:

            ``app/my-alb/778d41231b141a0f/targetgroup/my-alb-target-group/943f017f100becff`` .

            Where:

            - app// is the final portion of the load balancer ARN
            - targetgroup// is the final portion of the target group ARN.

            To find the ARN for an Application Load Balancer, use the `DescribeLoadBalancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html>`_ API operation. To find the ARN for the target group, use the `DescribeTargetGroups <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeTargetGroups.html>`_ API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predictivescalingpredefinedscalingmetric.html#cfn-autoscaling-scalingpolicy-predictivescalingpredefinedscalingmetric-resourcelabel
            '''
            result = self._values.get("resource_label")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveScalingPredefinedScalingMetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScalingPolicyPropsMixin.StepAdjustmentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "metric_interval_lower_bound": "metricIntervalLowerBound",
            "metric_interval_upper_bound": "metricIntervalUpperBound",
            "scaling_adjustment": "scalingAdjustment",
        },
    )
    class StepAdjustmentProperty:
        def __init__(
            self,
            *,
            metric_interval_lower_bound: typing.Optional[jsii.Number] = None,
            metric_interval_upper_bound: typing.Optional[jsii.Number] = None,
            scaling_adjustment: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``StepAdjustment`` specifies a step adjustment for the ``StepAdjustments`` property of the `AWS::AutoScaling::ScalingPolicy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scalingpolicy.html>`_ resource.

            For the following examples, suppose that you have an alarm with a breach threshold of 50:

            - To trigger a step adjustment when the metric is greater than or equal to 50 and less than 60, specify a lower bound of 0 and an upper bound of 10.
            - To trigger a step adjustment when the metric is greater than 40 and less than or equal to 50, specify a lower bound of -10 and an upper bound of 0.

            There are a few rules for the step adjustments for your step policy:

            - The ranges of your step adjustments can't overlap or have a gap.
            - At most one step adjustment can have a null lower bound. If one step adjustment has a negative lower bound, then there must be a step adjustment with a null lower bound.
            - At most one step adjustment can have a null upper bound. If one step adjustment has a positive upper bound, then there must be a step adjustment with a null upper bound.
            - The upper and lower bound can't be null in the same step adjustment.

            For more information, see `Step adjustments <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html#as-scaling-steps>`_ in the *Amazon EC2 Auto Scaling User Guide* .

            You can find a sample template snippet in the `Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scalingpolicy.html#aws-resource-autoscaling-scalingpolicy--examples>`_ section of the ``AWS::AutoScaling::ScalingPolicy`` resource.

            :param metric_interval_lower_bound: The lower bound for the difference between the alarm threshold and the CloudWatch metric. If the metric value is above the breach threshold, the lower bound is inclusive (the metric must be greater than or equal to the threshold plus the lower bound). Otherwise, it is exclusive (the metric must be greater than the threshold plus the lower bound). A null value indicates negative infinity.
            :param metric_interval_upper_bound: The upper bound for the difference between the alarm threshold and the CloudWatch metric. If the metric value is above the breach threshold, the upper bound is exclusive (the metric must be less than the threshold plus the upper bound). Otherwise, it is inclusive (the metric must be less than or equal to the threshold plus the upper bound). A null value indicates positive infinity. The upper bound must be greater than the lower bound.
            :param scaling_adjustment: The amount by which to scale, based on the specified adjustment type. A positive value adds to the current capacity while a negative number removes from the current capacity. For exact capacity, you must specify a non-negative value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-stepadjustment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                step_adjustment_property = autoscaling_mixins.CfnScalingPolicyPropsMixin.StepAdjustmentProperty(
                    metric_interval_lower_bound=123,
                    metric_interval_upper_bound=123,
                    scaling_adjustment=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__36f8c7356e7d7a010a857d77381370ff2bf0351091b3af93cf098ca467ffca0c)
                check_type(argname="argument metric_interval_lower_bound", value=metric_interval_lower_bound, expected_type=type_hints["metric_interval_lower_bound"])
                check_type(argname="argument metric_interval_upper_bound", value=metric_interval_upper_bound, expected_type=type_hints["metric_interval_upper_bound"])
                check_type(argname="argument scaling_adjustment", value=scaling_adjustment, expected_type=type_hints["scaling_adjustment"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric_interval_lower_bound is not None:
                self._values["metric_interval_lower_bound"] = metric_interval_lower_bound
            if metric_interval_upper_bound is not None:
                self._values["metric_interval_upper_bound"] = metric_interval_upper_bound
            if scaling_adjustment is not None:
                self._values["scaling_adjustment"] = scaling_adjustment

        @builtins.property
        def metric_interval_lower_bound(self) -> typing.Optional[jsii.Number]:
            '''The lower bound for the difference between the alarm threshold and the CloudWatch metric.

            If the metric value is above the breach threshold, the lower bound is inclusive (the metric must be greater than or equal to the threshold plus the lower bound). Otherwise, it is exclusive (the metric must be greater than the threshold plus the lower bound). A null value indicates negative infinity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-stepadjustment.html#cfn-autoscaling-scalingpolicy-stepadjustment-metricintervallowerbound
            '''
            result = self._values.get("metric_interval_lower_bound")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def metric_interval_upper_bound(self) -> typing.Optional[jsii.Number]:
            '''The upper bound for the difference between the alarm threshold and the CloudWatch metric.

            If the metric value is above the breach threshold, the upper bound is exclusive (the metric must be less than the threshold plus the upper bound). Otherwise, it is inclusive (the metric must be less than or equal to the threshold plus the upper bound). A null value indicates positive infinity.

            The upper bound must be greater than the lower bound.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-stepadjustment.html#cfn-autoscaling-scalingpolicy-stepadjustment-metricintervalupperbound
            '''
            result = self._values.get("metric_interval_upper_bound")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def scaling_adjustment(self) -> typing.Optional[jsii.Number]:
            '''The amount by which to scale, based on the specified adjustment type.

            A positive value adds to the current capacity while a negative number removes from the current capacity. For exact capacity, you must specify a non-negative value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-stepadjustment.html#cfn-autoscaling-scalingpolicy-stepadjustment-scalingadjustment
            '''
            result = self._values.get("scaling_adjustment")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StepAdjustmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScalingPolicyPropsMixin.TargetTrackingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "customized_metric_specification": "customizedMetricSpecification",
            "disable_scale_in": "disableScaleIn",
            "predefined_metric_specification": "predefinedMetricSpecification",
            "target_value": "targetValue",
        },
    )
    class TargetTrackingConfigurationProperty:
        def __init__(
            self,
            *,
            customized_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.CustomizedMetricSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            disable_scale_in: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            predefined_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.PredefinedMetricSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            target_value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``TargetTrackingConfiguration`` is a property of the `AWS::AutoScaling::ScalingPolicy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scalingpolicy.html>`_ resource that specifies a target tracking scaling policy configuration for Amazon EC2 Auto Scaling.

            For more information about scaling policies, see `Dynamic scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scale-based-on-demand.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

            :param customized_metric_specification: A customized metric. You must specify either a predefined metric or a customized metric.
            :param disable_scale_in: Indicates whether scaling in by the target tracking scaling policy is disabled. If scaling in is disabled, the target tracking scaling policy doesn't remove instances from the Auto Scaling group. Otherwise, the target tracking scaling policy can remove instances from the Auto Scaling group. The default is ``false`` .
            :param predefined_metric_specification: A predefined metric. You must specify either a predefined metric or a customized metric.
            :param target_value: The target value for the metric. .. epigraph:: Some metrics are based on a count instead of a percentage, such as the request count for an Application Load Balancer or the number of messages in an SQS queue. If the scaling policy specifies one of these metrics, specify the target utilization as the optimal average request or message count per instance during any one-minute interval.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                target_tracking_configuration_property = autoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingConfigurationProperty(
                    customized_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.CustomizedMetricSpecificationProperty(
                        dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                            name="name",
                            value="value"
                        )],
                        metric_name="metricName",
                        metrics=[autoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDataQueryProperty(
                            expression="expression",
                            id="id",
                            label="label",
                            metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty(
                                metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                                    dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                period=123,
                                stat="stat",
                                unit="unit"
                            ),
                            period=123,
                            return_data=False
                        )],
                        namespace="namespace",
                        period=123,
                        statistic="statistic",
                        unit="unit"
                    ),
                    disable_scale_in=False,
                    predefined_metric_specification=autoscaling_mixins.CfnScalingPolicyPropsMixin.PredefinedMetricSpecificationProperty(
                        predefined_metric_type="predefinedMetricType",
                        resource_label="resourceLabel"
                    ),
                    target_value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1923583cd136397d741bea5979ce8de323fe3d064f0c6468f86f0936512e3986)
                check_type(argname="argument customized_metric_specification", value=customized_metric_specification, expected_type=type_hints["customized_metric_specification"])
                check_type(argname="argument disable_scale_in", value=disable_scale_in, expected_type=type_hints["disable_scale_in"])
                check_type(argname="argument predefined_metric_specification", value=predefined_metric_specification, expected_type=type_hints["predefined_metric_specification"])
                check_type(argname="argument target_value", value=target_value, expected_type=type_hints["target_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if customized_metric_specification is not None:
                self._values["customized_metric_specification"] = customized_metric_specification
            if disable_scale_in is not None:
                self._values["disable_scale_in"] = disable_scale_in
            if predefined_metric_specification is not None:
                self._values["predefined_metric_specification"] = predefined_metric_specification
            if target_value is not None:
                self._values["target_value"] = target_value

        @builtins.property
        def customized_metric_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.CustomizedMetricSpecificationProperty"]]:
            '''A customized metric.

            You must specify either a predefined metric or a customized metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration-customizedmetricspecification
            '''
            result = self._values.get("customized_metric_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.CustomizedMetricSpecificationProperty"]], result)

        @builtins.property
        def disable_scale_in(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether scaling in by the target tracking scaling policy is disabled.

            If scaling in is disabled, the target tracking scaling policy doesn't remove instances from the Auto Scaling group. Otherwise, the target tracking scaling policy can remove instances from the Auto Scaling group. The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration-disablescalein
            '''
            result = self._values.get("disable_scale_in")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def predefined_metric_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredefinedMetricSpecificationProperty"]]:
            '''A predefined metric.

            You must specify either a predefined metric or a customized metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration-predefinedmetricspecification
            '''
            result = self._values.get("predefined_metric_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.PredefinedMetricSpecificationProperty"]], result)

        @builtins.property
        def target_value(self) -> typing.Optional[jsii.Number]:
            '''The target value for the metric.

            .. epigraph::

               Some metrics are based on a count instead of a percentage, such as the request count for an Application Load Balancer or the number of messages in an SQS queue. If the scaling policy specifies one of these metrics, specify the target utilization as the optimal average request or message count per instance during any one-minute interval.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration-targetvalue
            '''
            result = self._values.get("target_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetTrackingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDataQueryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "expression": "expression",
            "id": "id",
            "label": "label",
            "metric_stat": "metricStat",
            "period": "period",
            "return_data": "returnData",
        },
    )
    class TargetTrackingMetricDataQueryProperty:
        def __init__(
            self,
            *,
            expression: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            label: typing.Optional[builtins.str] = None,
            metric_stat: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            period: typing.Optional[jsii.Number] = None,
            return_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The metric data to return.

            Also defines whether this call is returning data for one metric only, or whether it is performing a math expression on the values of returned metric statistics to create a new time series. A time series is a series of data points, each of which is associated with a timestamp.

            You can use ``TargetTrackingMetricDataQuery`` structures with a `PutScalingPolicy <https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_PutScalingPolicy.html>`_ operation when you specify a `TargetTrackingConfiguration <https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_TargetTrackingConfiguration.html>`_ in the request.

            You can call for a single metric or perform math expressions on multiple metrics. Any expressions used in a metric specification must eventually return a single time series.

            For more information, see the `Create a target tracking scaling policy for Amazon EC2 Auto Scaling using metric math <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-target-tracking-metric-math.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

            :param expression: The math expression to perform on the returned data, if this object is performing a math expression. This expression can use the ``Id`` of the other metrics to refer to those metrics, and can also use the ``Id`` of other expressions to use the result of those expressions. Conditional: Within each ``TargetTrackingMetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` , but not both.
            :param id: A short name that identifies the object's results in the response. This name must be unique among all ``TargetTrackingMetricDataQuery`` objects specified for a single scaling policy. If you are performing math expressions on this set of data, this name represents that data and can serve as a variable in the mathematical expression. The valid characters are letters, numbers, and underscores. The first character must be a lowercase letter.
            :param label: A human-readable label for this metric or expression. This is especially useful if this is a math expression, so that you know what the value represents.
            :param metric_stat: Information about the metric data to return. Conditional: Within each ``TargetTrackingMetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` , but not both.
            :param period: The period of the metric in seconds. The default value is 60. Accepted values are 10, 30, and 60. For high resolution metric, set the value to less than 60. For more information, see `Create a target tracking policy using high-resolution metrics for faster response <https://docs.aws.amazon.com/autoscaling/ec2/userguide/policy-creating-high-resolution-metrics.html>`_ .
            :param return_data: Indicates whether to return the timestamps and raw data values of this metric. If you use any math expressions, specify ``true`` for this value for only the final math expression that the metric specification is based on. You must specify ``false`` for ``ReturnData`` for all the other metrics and expressions used in the metric specification. If you are only retrieving metrics and not performing any math expressions, do not specify anything for ``ReturnData`` . This sets it to its default ( ``true`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingmetricdataquery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                target_tracking_metric_data_query_property = autoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricDataQueryProperty(
                    expression="expression",
                    id="id",
                    label="label",
                    metric_stat=autoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty(
                        metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                            dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                                name="name",
                                value="value"
                            )],
                            metric_name="metricName",
                            namespace="namespace"
                        ),
                        period=123,
                        stat="stat",
                        unit="unit"
                    ),
                    period=123,
                    return_data=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__094539f2946d1fe4f8d540fb200ef92e8e1d35629556cb2d77e3bd6765162bf9)
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument label", value=label, expected_type=type_hints["label"])
                check_type(argname="argument metric_stat", value=metric_stat, expected_type=type_hints["metric_stat"])
                check_type(argname="argument period", value=period, expected_type=type_hints["period"])
                check_type(argname="argument return_data", value=return_data, expected_type=type_hints["return_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if expression is not None:
                self._values["expression"] = expression
            if id is not None:
                self._values["id"] = id
            if label is not None:
                self._values["label"] = label
            if metric_stat is not None:
                self._values["metric_stat"] = metric_stat
            if period is not None:
                self._values["period"] = period
            if return_data is not None:
                self._values["return_data"] = return_data

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''The math expression to perform on the returned data, if this object is performing a math expression.

            This expression can use the ``Id`` of the other metrics to refer to those metrics, and can also use the ``Id`` of other expressions to use the result of those expressions.

            Conditional: Within each ``TargetTrackingMetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` , but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingmetricdataquery.html#cfn-autoscaling-scalingpolicy-targettrackingmetricdataquery-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A short name that identifies the object's results in the response.

            This name must be unique among all ``TargetTrackingMetricDataQuery`` objects specified for a single scaling policy. If you are performing math expressions on this set of data, this name represents that data and can serve as a variable in the mathematical expression. The valid characters are letters, numbers, and underscores. The first character must be a lowercase letter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingmetricdataquery.html#cfn-autoscaling-scalingpolicy-targettrackingmetricdataquery-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def label(self) -> typing.Optional[builtins.str]:
            '''A human-readable label for this metric or expression.

            This is especially useful if this is a math expression, so that you know what the value represents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingmetricdataquery.html#cfn-autoscaling-scalingpolicy-targettrackingmetricdataquery-label
            '''
            result = self._values.get("label")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_stat(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty"]]:
            '''Information about the metric data to return.

            Conditional: Within each ``TargetTrackingMetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` , but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingmetricdataquery.html#cfn-autoscaling-scalingpolicy-targettrackingmetricdataquery-metricstat
            '''
            result = self._values.get("metric_stat")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty"]], result)

        @builtins.property
        def period(self) -> typing.Optional[jsii.Number]:
            '''The period of the metric in seconds.

            The default value is 60. Accepted values are 10, 30, and 60. For high resolution metric, set the value to less than 60. For more information, see `Create a target tracking policy using high-resolution metrics for faster response <https://docs.aws.amazon.com/autoscaling/ec2/userguide/policy-creating-high-resolution-metrics.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingmetricdataquery.html#cfn-autoscaling-scalingpolicy-targettrackingmetricdataquery-period
            '''
            result = self._values.get("period")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def return_data(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether to return the timestamps and raw data values of this metric.

            If you use any math expressions, specify ``true`` for this value for only the final math expression that the metric specification is based on. You must specify ``false`` for ``ReturnData`` for all the other metrics and expressions used in the metric specification.

            If you are only retrieving metrics and not performing any math expressions, do not specify anything for ``ReturnData`` . This sets it to its default ( ``true`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingmetricdataquery.html#cfn-autoscaling-scalingpolicy-targettrackingmetricdataquery-returndata
            '''
            result = self._values.get("return_data")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetTrackingMetricDataQueryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty",
        jsii_struct_bases=[],
        name_mapping={
            "metric": "metric",
            "period": "period",
            "stat": "stat",
            "unit": "unit",
        },
    )
    class TargetTrackingMetricStatProperty:
        def __init__(
            self,
            *,
            metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScalingPolicyPropsMixin.MetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            period: typing.Optional[jsii.Number] = None,
            stat: typing.Optional[builtins.str] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This structure defines the CloudWatch metric to return, along with the statistic and unit.

            ``TargetTrackingMetricStat`` is a property of the `TargetTrackingMetricDataQuery <https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_TargetTrackingMetricDataQuery.html>`_ object.

            For more information about the CloudWatch terminology below, see `Amazon CloudWatch concepts <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html>`_ in the *Amazon CloudWatch User Guide* .

            :param metric: The metric to use.
            :param period: The period of the metric in seconds. The default value is 60. Accepted values are 10, 30, and 60. For high resolution metric, set the value to less than 60. For more information, see `Create a target tracking policy using high-resolution metrics for faster response <https://docs.aws.amazon.com/autoscaling/ec2/userguide/policy-creating-high-resolution-metrics.html>`_ .
            :param stat: The statistic to return. It can include any CloudWatch statistic or extended statistic. For a list of valid values, see the table in `Statistics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Statistic>`_ in the *Amazon CloudWatch User Guide* . The most commonly used metric for scaling is ``Average`` .
            :param unit: The unit to use for the returned data points. For a complete list of the units that CloudWatch supports, see the `MetricDatum <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDatum.html>`_ data type in the *Amazon CloudWatch API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingmetricstat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                target_tracking_metric_stat_property = autoscaling_mixins.CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty(
                    metric=autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricProperty(
                        dimensions=[autoscaling_mixins.CfnScalingPolicyPropsMixin.MetricDimensionProperty(
                            name="name",
                            value="value"
                        )],
                        metric_name="metricName",
                        namespace="namespace"
                    ),
                    period=123,
                    stat="stat",
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__02bb5a30f05747c467ea003d9e69c6f967bc07b941730a88469e0360954c105e)
                check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
                check_type(argname="argument period", value=period, expected_type=type_hints["period"])
                check_type(argname="argument stat", value=stat, expected_type=type_hints["stat"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric is not None:
                self._values["metric"] = metric
            if period is not None:
                self._values["period"] = period
            if stat is not None:
                self._values["stat"] = stat
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def metric(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.MetricProperty"]]:
            '''The metric to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingmetricstat.html#cfn-autoscaling-scalingpolicy-targettrackingmetricstat-metric
            '''
            result = self._values.get("metric")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScalingPolicyPropsMixin.MetricProperty"]], result)

        @builtins.property
        def period(self) -> typing.Optional[jsii.Number]:
            '''The period of the metric in seconds.

            The default value is 60. Accepted values are 10, 30, and 60. For high resolution metric, set the value to less than 60. For more information, see `Create a target tracking policy using high-resolution metrics for faster response <https://docs.aws.amazon.com/autoscaling/ec2/userguide/policy-creating-high-resolution-metrics.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingmetricstat.html#cfn-autoscaling-scalingpolicy-targettrackingmetricstat-period
            '''
            result = self._values.get("period")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stat(self) -> typing.Optional[builtins.str]:
            '''The statistic to return.

            It can include any CloudWatch statistic or extended statistic. For a list of valid values, see the table in `Statistics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Statistic>`_ in the *Amazon CloudWatch User Guide* .

            The most commonly used metric for scaling is ``Average`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingmetricstat.html#cfn-autoscaling-scalingpolicy-targettrackingmetricstat-stat
            '''
            result = self._values.get("stat")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit to use for the returned data points.

            For a complete list of the units that CloudWatch supports, see the `MetricDatum <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDatum.html>`_ data type in the *Amazon CloudWatch API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingmetricstat.html#cfn-autoscaling-scalingpolicy-targettrackingmetricstat-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetTrackingMetricStatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScheduledActionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_group_name": "autoScalingGroupName",
        "desired_capacity": "desiredCapacity",
        "end_time": "endTime",
        "max_size": "maxSize",
        "min_size": "minSize",
        "recurrence": "recurrence",
        "start_time": "startTime",
        "time_zone": "timeZone",
    },
)
class CfnScheduledActionMixinProps:
    def __init__(
        self,
        *,
        auto_scaling_group_name: typing.Optional[builtins.str] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        end_time: typing.Optional[builtins.str] = None,
        max_size: typing.Optional[jsii.Number] = None,
        min_size: typing.Optional[jsii.Number] = None,
        recurrence: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnScheduledActionPropsMixin.

        :param auto_scaling_group_name: The name of the Auto Scaling group.
        :param desired_capacity: The desired capacity is the initial capacity of the Auto Scaling group after the scheduled action runs and the capacity it attempts to maintain. It can scale beyond this capacity if you add more scaling conditions. .. epigraph:: You must specify at least one of the following properties: ``MaxSize`` , ``MinSize`` , or ``DesiredCapacity`` .
        :param end_time: The date and time for the recurring schedule to end, in UTC. For example, ``"2021-06-01T00:00:00Z"`` .
        :param max_size: The maximum size of the Auto Scaling group.
        :param min_size: The minimum size of the Auto Scaling group.
        :param recurrence: The recurring schedule for this action. This format consists of five fields separated by white spaces: [Minute] [Hour] [Day_of_Month] [Month_of_Year] [Day_of_Week]. The value must be in quotes (for example, ``"30 0 1 1,6,12 *"`` ). For more information about this format, see `Crontab <https://docs.aws.amazon.com/http://crontab.org>`_ . When ``StartTime`` and ``EndTime`` are specified with ``Recurrence`` , they form the boundaries of when the recurring action starts and stops. Cron expressions use Universal Coordinated Time (UTC) by default.
        :param start_time: The date and time for this action to start, in YYYY-MM-DDThh:mm:ssZ format in UTC/GMT only and in quotes (for example, ``"2021-06-01T00:00:00Z"`` ). If you specify ``Recurrence`` and ``StartTime`` , Amazon EC2 Auto Scaling performs the action at this time, and then performs the action based on the specified recurrence.
        :param time_zone: Specifies the time zone for a cron expression. If a time zone is not provided, UTC is used by default. Valid values are the canonical names of the IANA time zones, derived from the IANA Time Zone Database (such as ``Etc/GMT+9`` or ``Pacific/Tahiti`` ). For more information, see `https://en.wikipedia.org/wiki/List_of_tz_database_time_zones <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/List_of_tz_database_time_zones>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scheduledaction.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
            
            cfn_scheduled_action_mixin_props = autoscaling_mixins.CfnScheduledActionMixinProps(
                auto_scaling_group_name="autoScalingGroupName",
                desired_capacity=123,
                end_time="endTime",
                max_size=123,
                min_size=123,
                recurrence="recurrence",
                start_time="startTime",
                time_zone="timeZone"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e83a36efe0e01a18dccebae5abcc947df0d5ee0f5a071cf7e62e7ed96db002)
            check_type(argname="argument auto_scaling_group_name", value=auto_scaling_group_name, expected_type=type_hints["auto_scaling_group_name"])
            check_type(argname="argument desired_capacity", value=desired_capacity, expected_type=type_hints["desired_capacity"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument max_size", value=max_size, expected_type=type_hints["max_size"])
            check_type(argname="argument min_size", value=min_size, expected_type=type_hints["min_size"])
            check_type(argname="argument recurrence", value=recurrence, expected_type=type_hints["recurrence"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_scaling_group_name is not None:
            self._values["auto_scaling_group_name"] = auto_scaling_group_name
        if desired_capacity is not None:
            self._values["desired_capacity"] = desired_capacity
        if end_time is not None:
            self._values["end_time"] = end_time
        if max_size is not None:
            self._values["max_size"] = max_size
        if min_size is not None:
            self._values["min_size"] = min_size
        if recurrence is not None:
            self._values["recurrence"] = recurrence
        if start_time is not None:
            self._values["start_time"] = start_time
        if time_zone is not None:
            self._values["time_zone"] = time_zone

    @builtins.property
    def auto_scaling_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Auto Scaling group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scheduledaction.html#cfn-autoscaling-scheduledaction-autoscalinggroupname
        '''
        result = self._values.get("auto_scaling_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        '''The desired capacity is the initial capacity of the Auto Scaling group after the scheduled action runs and the capacity it attempts to maintain.

        It can scale beyond this capacity if you add more scaling conditions.
        .. epigraph::

           You must specify at least one of the following properties: ``MaxSize`` , ``MinSize`` , or ``DesiredCapacity`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scheduledaction.html#cfn-autoscaling-scheduledaction-desiredcapacity
        '''
        result = self._values.get("desired_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''The date and time for the recurring schedule to end, in UTC.

        For example, ``"2021-06-01T00:00:00Z"`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scheduledaction.html#cfn-autoscaling-scheduledaction-endtime
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_size(self) -> typing.Optional[jsii.Number]:
        '''The maximum size of the Auto Scaling group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scheduledaction.html#cfn-autoscaling-scheduledaction-maxsize
        '''
        result = self._values.get("max_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_size(self) -> typing.Optional[jsii.Number]:
        '''The minimum size of the Auto Scaling group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scheduledaction.html#cfn-autoscaling-scheduledaction-minsize
        '''
        result = self._values.get("min_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def recurrence(self) -> typing.Optional[builtins.str]:
        '''The recurring schedule for this action.

        This format consists of five fields separated by white spaces: [Minute] [Hour] [Day_of_Month] [Month_of_Year] [Day_of_Week]. The value must be in quotes (for example, ``"30 0 1 1,6,12 *"`` ). For more information about this format, see `Crontab <https://docs.aws.amazon.com/http://crontab.org>`_ .

        When ``StartTime`` and ``EndTime`` are specified with ``Recurrence`` , they form the boundaries of when the recurring action starts and stops.

        Cron expressions use Universal Coordinated Time (UTC) by default.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scheduledaction.html#cfn-autoscaling-scheduledaction-recurrence
        '''
        result = self._values.get("recurrence")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The date and time for this action to start, in YYYY-MM-DDThh:mm:ssZ format in UTC/GMT only and in quotes (for example, ``"2021-06-01T00:00:00Z"`` ).

        If you specify ``Recurrence`` and ``StartTime`` , Amazon EC2 Auto Scaling performs the action at this time, and then performs the action based on the specified recurrence.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scheduledaction.html#cfn-autoscaling-scheduledaction-starttime
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''Specifies the time zone for a cron expression.

        If a time zone is not provided, UTC is used by default.

        Valid values are the canonical names of the IANA time zones, derived from the IANA Time Zone Database (such as ``Etc/GMT+9`` or ``Pacific/Tahiti`` ). For more information, see `https://en.wikipedia.org/wiki/List_of_tz_database_time_zones <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/List_of_tz_database_time_zones>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scheduledaction.html#cfn-autoscaling-scheduledaction-timezone
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnScheduledActionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnScheduledActionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnScheduledActionPropsMixin",
):
    '''The ``AWS::AutoScaling::ScheduledAction`` resource specifies an Amazon EC2 Auto Scaling scheduled action so that the Auto Scaling group can change the number of instances available for your application in response to predictable load changes.

    When you update a stack with an Auto Scaling group and scheduled action, CloudFormation always sets the min size, max size, and desired capacity properties of your group to the values that are defined in the ``AWS::AutoScaling::AutoScalingGroup`` section of your template. However, you might not want CloudFormation to do that when you have a scheduled action in effect. You can use an `UpdatePolicy attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html>`_ to prevent CloudFormation from changing the min size, max size, or desired capacity property values during a stack update unless you modified the individual values in your template. If you have rolling updates enabled, before you can update the Auto Scaling group, you must suspend scheduled actions by specifying an `UpdatePolicy attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html>`_ for the Auto Scaling group. You can find a sample update policy for rolling updates in `Configure Amazon EC2 Auto Scaling resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-ec2-auto-scaling.html>`_ .

    For more information, see `Scheduled scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/schedule_time.html>`_ and `Suspending and resuming scaling processes <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-suspend-resume-processes.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scheduledaction.html
    :cloudformationResource: AWS::AutoScaling::ScheduledAction
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
        
        cfn_scheduled_action_props_mixin = autoscaling_mixins.CfnScheduledActionPropsMixin(autoscaling_mixins.CfnScheduledActionMixinProps(
            auto_scaling_group_name="autoScalingGroupName",
            desired_capacity=123,
            end_time="endTime",
            max_size=123,
            min_size=123,
            recurrence="recurrence",
            start_time="startTime",
            time_zone="timeZone"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnScheduledActionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AutoScaling::ScheduledAction``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__476df05d25605faeb057de0f69d66c56647a07832054471c6163cc19b5c42089)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        options = _CfnPropertyMixinOptions_9cbff649(strategy=strategy)

        jsii.create(self.__class__, self, [props, options])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply the mixin properties to the construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb00b1784478e57a3cfe4f3230f3d15fd7037bdec8585df4c4cb3130b7aa34f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc2e966a395f19c76c991a0c4943ca969c9bd7116bd3fffd79f80dfb28108da4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnScheduledActionMixinProps:
        return typing.cast(CfnScheduledActionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnWarmPoolMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_group_name": "autoScalingGroupName",
        "instance_reuse_policy": "instanceReusePolicy",
        "max_group_prepared_capacity": "maxGroupPreparedCapacity",
        "min_size": "minSize",
        "pool_state": "poolState",
    },
)
class CfnWarmPoolMixinProps:
    def __init__(
        self,
        *,
        auto_scaling_group_name: typing.Optional[builtins.str] = None,
        instance_reuse_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWarmPoolPropsMixin.InstanceReusePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        max_group_prepared_capacity: typing.Optional[jsii.Number] = None,
        min_size: typing.Optional[jsii.Number] = None,
        pool_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnWarmPoolPropsMixin.

        :param auto_scaling_group_name: The name of the Auto Scaling group.
        :param instance_reuse_policy: Indicates whether instances in the Auto Scaling group can be returned to the warm pool on scale in. The default is to terminate instances in the Auto Scaling group when the group scales in.
        :param max_group_prepared_capacity: Specifies the maximum number of instances that are allowed to be in the warm pool or in any state except ``Terminated`` for the Auto Scaling group. This is an optional property. Specify it only if you do not want the warm pool size to be determined by the difference between the group's maximum capacity and its desired capacity. .. epigraph:: If a value for ``MaxGroupPreparedCapacity`` is not specified, Amazon EC2 Auto Scaling launches and maintains the difference between the group's maximum capacity and its desired capacity. If you specify a value for ``MaxGroupPreparedCapacity`` , Amazon EC2 Auto Scaling uses the difference between the ``MaxGroupPreparedCapacity`` and the desired capacity instead. The size of the warm pool is dynamic. Only when ``MaxGroupPreparedCapacity`` and ``MinSize`` are set to the same value does the warm pool have an absolute size. If the desired capacity of the Auto Scaling group is higher than the ``MaxGroupPreparedCapacity`` , the capacity of the warm pool is 0, unless you specify a value for ``MinSize`` . To remove a value that you previously set, include the property but specify -1 for the value.
        :param min_size: Specifies the minimum number of instances to maintain in the warm pool. This helps you to ensure that there is always a certain number of warmed instances available to handle traffic spikes. Defaults to 0 if not specified.
        :param pool_state: Sets the instance state to transition to after the lifecycle actions are complete. Default is ``Stopped`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-warmpool.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
            
            cfn_warm_pool_mixin_props = autoscaling_mixins.CfnWarmPoolMixinProps(
                auto_scaling_group_name="autoScalingGroupName",
                instance_reuse_policy=autoscaling_mixins.CfnWarmPoolPropsMixin.InstanceReusePolicyProperty(
                    reuse_on_scale_in=False
                ),
                max_group_prepared_capacity=123,
                min_size=123,
                pool_state="poolState"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cde652ffdf3bee0d1ff5db9c374551126f7b645191aa20ab01fe3f58a56c2eb)
            check_type(argname="argument auto_scaling_group_name", value=auto_scaling_group_name, expected_type=type_hints["auto_scaling_group_name"])
            check_type(argname="argument instance_reuse_policy", value=instance_reuse_policy, expected_type=type_hints["instance_reuse_policy"])
            check_type(argname="argument max_group_prepared_capacity", value=max_group_prepared_capacity, expected_type=type_hints["max_group_prepared_capacity"])
            check_type(argname="argument min_size", value=min_size, expected_type=type_hints["min_size"])
            check_type(argname="argument pool_state", value=pool_state, expected_type=type_hints["pool_state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_scaling_group_name is not None:
            self._values["auto_scaling_group_name"] = auto_scaling_group_name
        if instance_reuse_policy is not None:
            self._values["instance_reuse_policy"] = instance_reuse_policy
        if max_group_prepared_capacity is not None:
            self._values["max_group_prepared_capacity"] = max_group_prepared_capacity
        if min_size is not None:
            self._values["min_size"] = min_size
        if pool_state is not None:
            self._values["pool_state"] = pool_state

    @builtins.property
    def auto_scaling_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Auto Scaling group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-warmpool.html#cfn-autoscaling-warmpool-autoscalinggroupname
        '''
        result = self._values.get("auto_scaling_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_reuse_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWarmPoolPropsMixin.InstanceReusePolicyProperty"]]:
        '''Indicates whether instances in the Auto Scaling group can be returned to the warm pool on scale in.

        The default is to terminate instances in the Auto Scaling group when the group scales in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-warmpool.html#cfn-autoscaling-warmpool-instancereusepolicy
        '''
        result = self._values.get("instance_reuse_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWarmPoolPropsMixin.InstanceReusePolicyProperty"]], result)

    @builtins.property
    def max_group_prepared_capacity(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum number of instances that are allowed to be in the warm pool or in any state except ``Terminated`` for the Auto Scaling group.

        This is an optional property. Specify it only if you do not want the warm pool size to be determined by the difference between the group's maximum capacity and its desired capacity.
        .. epigraph::

           If a value for ``MaxGroupPreparedCapacity`` is not specified, Amazon EC2 Auto Scaling launches and maintains the difference between the group's maximum capacity and its desired capacity. If you specify a value for ``MaxGroupPreparedCapacity`` , Amazon EC2 Auto Scaling uses the difference between the ``MaxGroupPreparedCapacity`` and the desired capacity instead.

           The size of the warm pool is dynamic. Only when ``MaxGroupPreparedCapacity`` and ``MinSize`` are set to the same value does the warm pool have an absolute size.

        If the desired capacity of the Auto Scaling group is higher than the ``MaxGroupPreparedCapacity`` , the capacity of the warm pool is 0, unless you specify a value for ``MinSize`` . To remove a value that you previously set, include the property but specify -1 for the value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-warmpool.html#cfn-autoscaling-warmpool-maxgrouppreparedcapacity
        '''
        result = self._values.get("max_group_prepared_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_size(self) -> typing.Optional[jsii.Number]:
        '''Specifies the minimum number of instances to maintain in the warm pool.

        This helps you to ensure that there is always a certain number of warmed instances available to handle traffic spikes. Defaults to 0 if not specified.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-warmpool.html#cfn-autoscaling-warmpool-minsize
        '''
        result = self._values.get("min_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pool_state(self) -> typing.Optional[builtins.str]:
        '''Sets the instance state to transition to after the lifecycle actions are complete.

        Default is ``Stopped`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-warmpool.html#cfn-autoscaling-warmpool-poolstate
        '''
        result = self._values.get("pool_state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWarmPoolMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWarmPoolPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnWarmPoolPropsMixin",
):
    '''The ``AWS::AutoScaling::WarmPool`` resource creates a pool of pre-initialized EC2 instances that sits alongside the Auto Scaling group.

    Whenever your application needs to scale out, the Auto Scaling group can draw on the warm pool to meet its new desired capacity.

    When you create a warm pool, you can define a minimum size. When your Auto Scaling group scales out and the size of the warm pool shrinks, Amazon EC2 Auto Scaling launches new instances into the warm pool to maintain its minimum size.

    For more information, see `Warm pools for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-warm-pools.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .
    .. epigraph::

       CloudFormation supports the ``UpdatePolicy`` attribute for Auto Scaling groups. During an update, if ``UpdatePolicy`` is set to ``AutoScalingRollingUpdate`` , CloudFormation replaces ``InService`` instances only. Instances in the warm pool are not replaced. The difference in which instances are replaced can potentially result in different instance configurations after the stack update completes. If ``UpdatePolicy`` is set to ``AutoScalingReplacingUpdate`` , you do not encounter this issue because CloudFormation replaces both the Auto Scaling group and the warm pool.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-warmpool.html
    :cloudformationResource: AWS::AutoScaling::WarmPool
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
        
        cfn_warm_pool_props_mixin = autoscaling_mixins.CfnWarmPoolPropsMixin(autoscaling_mixins.CfnWarmPoolMixinProps(
            auto_scaling_group_name="autoScalingGroupName",
            instance_reuse_policy=autoscaling_mixins.CfnWarmPoolPropsMixin.InstanceReusePolicyProperty(
                reuse_on_scale_in=False
            ),
            max_group_prepared_capacity=123,
            min_size=123,
            pool_state="poolState"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWarmPoolMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AutoScaling::WarmPool``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8707d4f34cd0e246d41848dc311bf46197e3913ba9867f3844b5cfdf53801602)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        options = _CfnPropertyMixinOptions_9cbff649(strategy=strategy)

        jsii.create(self.__class__, self, [props, options])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply the mixin properties to the construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eef686c017c7014b8e43a03ea9b57f100f41a4a4dad563a45355bdca65cdd7d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37e867b40070cc0eba579ba02f73deb8970325d06da4ea7b2e983b131c6f37c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWarmPoolMixinProps:
        return typing.cast(CfnWarmPoolMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_autoscaling.mixins.CfnWarmPoolPropsMixin.InstanceReusePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"reuse_on_scale_in": "reuseOnScaleIn"},
    )
    class InstanceReusePolicyProperty:
        def __init__(
            self,
            *,
            reuse_on_scale_in: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''A structure that specifies an instance reuse policy for the ``InstanceReusePolicy`` property of the `AWS::AutoScaling::WarmPool <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-warmpool.html>`_ resource.

            For more information, see `Warm pools for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-warm-pools.html>`_ in the *Amazon EC2 Auto Scaling User Guide* .

            :param reuse_on_scale_in: Specifies whether instances in the Auto Scaling group can be returned to the warm pool on scale in.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-warmpool-instancereusepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_autoscaling import mixins as autoscaling_mixins
                
                instance_reuse_policy_property = autoscaling_mixins.CfnWarmPoolPropsMixin.InstanceReusePolicyProperty(
                    reuse_on_scale_in=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dd5a5f58fe994dd0f6570fbb32d539933d97430e33503da4e4be7f56a13ded99)
                check_type(argname="argument reuse_on_scale_in", value=reuse_on_scale_in, expected_type=type_hints["reuse_on_scale_in"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if reuse_on_scale_in is not None:
                self._values["reuse_on_scale_in"] = reuse_on_scale_in

        @builtins.property
        def reuse_on_scale_in(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether instances in the Auto Scaling group can be returned to the warm pool on scale in.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-warmpool-instancereusepolicy.html#cfn-autoscaling-warmpool-instancereusepolicy-reuseonscalein
            '''
            result = self._values.get("reuse_on_scale_in")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceReusePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAutoScalingGroupMixinProps",
    "CfnAutoScalingGroupPropsMixin",
    "CfnLaunchConfigurationMixinProps",
    "CfnLaunchConfigurationPropsMixin",
    "CfnLifecycleHookMixinProps",
    "CfnLifecycleHookPropsMixin",
    "CfnScalingPolicyMixinProps",
    "CfnScalingPolicyPropsMixin",
    "CfnScheduledActionMixinProps",
    "CfnScheduledActionPropsMixin",
    "CfnWarmPoolMixinProps",
    "CfnWarmPoolPropsMixin",
]

publication.publish()

def _typecheckingstub__263f37d5b93143ba12d509ca54fb68af5089157d7dd9cd494eea2e39db8b522c(
    *,
    auto_scaling_group_name: typing.Optional[builtins.str] = None,
    availability_zone_distribution: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.AvailabilityZoneDistributionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    availability_zone_impairment_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.AvailabilityZoneImpairmentPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    capacity_rebalance: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    capacity_reservation_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.CapacityReservationSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    context: typing.Optional[builtins.str] = None,
    cooldown: typing.Optional[builtins.str] = None,
    default_instance_warmup: typing.Optional[jsii.Number] = None,
    desired_capacity: typing.Optional[builtins.str] = None,
    desired_capacity_type: typing.Optional[builtins.str] = None,
    health_check_grace_period: typing.Optional[jsii.Number] = None,
    health_check_type: typing.Optional[builtins.str] = None,
    instance_id: typing.Optional[builtins.str] = None,
    instance_maintenance_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.InstanceMaintenancePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    launch_configuration_name: typing.Optional[builtins.str] = None,
    launch_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lifecycle_hook_specification_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.LifecycleHookSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    load_balancer_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_instance_lifetime: typing.Optional[jsii.Number] = None,
    max_size: typing.Optional[builtins.str] = None,
    metrics_collection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.MetricsCollectionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    min_size: typing.Optional[builtins.str] = None,
    mixed_instances_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.MixedInstancesPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    new_instances_protected_from_scale_in: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    notification_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.NotificationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    notification_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.NotificationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    placement_group: typing.Optional[builtins.str] = None,
    service_linked_role_arn: typing.Optional[builtins.str] = None,
    skip_zonal_shift_validation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnAutoScalingGroupPropsMixin.TagPropertyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    termination_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    traffic_sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.TrafficSourceIdentifierProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    vpc_zone_identifier: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__112ae175d73915392830869d82f09263102006c659d735c41ef5d7c0fbc7b135(
    props: typing.Union[CfnAutoScalingGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f163fe4a672c71d5938e040e13052303459f5bd3fd5bc334834efcd0ea4a2fe8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d9440e844b7d7fefdd405d2533777a4d84411cb6c17495393f7519db2170f7b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ebde666f10b627fbe322c9fb13ff136d93d3be4d7f807c388f74f82ab008b3(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1de934747c7d6e959c704e34fd5e2de8e1c05d0f7dfdbc8e22c5c6481f9db37(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__561e51301a99db50db25aa514ed54308c62de8aa0a44d6446b703a0465c6c4d0(
    *,
    capacity_distribution_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e388abc303ec0216355bae8268a80a4d0bd1d9d9a42c9641199ea2bde0db517(
    *,
    impaired_zone_health_check_behavior: typing.Optional[builtins.str] = None,
    zonal_shift_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7a5dad1a6260ae7be680b9b919f7ff3ebd1598458bd6e379de89801a65125e3(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11466c41d569c969205ad479f837d22fb0ece6ce4d7d06ff9062c76f58332477(
    *,
    cpu: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.CpuPerformanceFactorRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f9584945e2608153728d61494b08ca3b13fedacfaf2fdd40268315dfe34794(
    *,
    capacity_reservation_preference: typing.Optional[builtins.str] = None,
    capacity_reservation_target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.CapacityReservationTargetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed7a417ad40a1eefcc9feed5a11525334481f52a8c295ef6f1b7ceffd88aa56(
    *,
    capacity_reservation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    capacity_reservation_resource_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53621c12a7067d137b4a17dcfa7c0c846a3544d472b367aafcfc0abf7a600cda(
    *,
    references: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.PerformanceFactorReferenceRequestProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005b347b6d1c8d4f505704ea90dad06ed58709850ff978bf05a6b3ceea64439e(
    *,
    max_healthy_percentage: typing.Optional[jsii.Number] = None,
    min_healthy_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e43296d83349af86ca2cf253b8caa4a97d3c6cd4b61b588c492836f9a676cf(
    *,
    accelerator_count: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.AcceleratorCountRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    accelerator_manufacturers: typing.Optional[typing.Sequence[builtins.str]] = None,
    accelerator_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    accelerator_total_memory_mib: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.AcceleratorTotalMemoryMiBRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    accelerator_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    bare_metal: typing.Optional[builtins.str] = None,
    baseline_ebs_bandwidth_mbps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.BaselineEbsBandwidthMbpsRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    baseline_performance_factors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.BaselinePerformanceFactorsRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    burstable_performance: typing.Optional[builtins.str] = None,
    cpu_manufacturers: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_generations: typing.Optional[typing.Sequence[builtins.str]] = None,
    local_storage: typing.Optional[builtins.str] = None,
    local_storage_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_spot_price_as_percentage_of_optimal_on_demand_price: typing.Optional[jsii.Number] = None,
    memory_gib_per_v_cpu: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.MemoryGiBPerVCpuRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    memory_mib: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.MemoryMiBRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    network_bandwidth_gbps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.NetworkBandwidthGbpsRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    network_interface_count: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.NetworkInterfaceCountRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    on_demand_max_price_percentage_over_lowest_price: typing.Optional[jsii.Number] = None,
    require_hibernate_support: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    spot_max_price_percentage_over_lowest_price: typing.Optional[jsii.Number] = None,
    total_local_storage_gb: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.TotalLocalStorageGBRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    v_cpu_count: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.VCpuCountRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610ae3c0f0e10395c86ab0fd13d9546ce16d622da416b1600f9adae1c504b814(
    *,
    on_demand_allocation_strategy: typing.Optional[builtins.str] = None,
    on_demand_base_capacity: typing.Optional[jsii.Number] = None,
    on_demand_percentage_above_base_capacity: typing.Optional[jsii.Number] = None,
    spot_allocation_strategy: typing.Optional[builtins.str] = None,
    spot_instance_pools: typing.Optional[jsii.Number] = None,
    spot_max_price: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec8399276e828b87e907129eb104baa65d299177eecadd4d33a5328e6ed888d(
    *,
    instance_requirements: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.InstanceRequirementsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_type: typing.Optional[builtins.str] = None,
    launch_template_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    weighted_capacity: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__971215471d62705af8d0d24e6d28edf1e817027a62dc14f25f1034f1994e96c2(
    *,
    launch_template_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.LaunchTemplateSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.LaunchTemplateOverridesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__979ed91df33924ef97dd12ca874a081a977faa5426834d4e6a8ab245c0dbfa54(
    *,
    launch_template_id: typing.Optional[builtins.str] = None,
    launch_template_name: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e52167b1ca0ea0d079768dad70bd5be7356fb1fcc18337014875e26137b04cf(
    *,
    default_result: typing.Optional[builtins.str] = None,
    heartbeat_timeout: typing.Optional[jsii.Number] = None,
    lifecycle_hook_name: typing.Optional[builtins.str] = None,
    lifecycle_transition: typing.Optional[builtins.str] = None,
    notification_metadata: typing.Optional[builtins.str] = None,
    notification_target_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6327a360dc7cd47b7b5fe16775df21d0e16fcfc30de9811b6fc5e5b27c470c32(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ecf317383c2e29a0a7431ed73953a3a67f304b9b9c2cc34ba84546919a35b29(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae69aee764a4c7a5c91fb540b9286a2ce22e88b0b4ce4817a4570d515f37152e(
    *,
    granularity: typing.Optional[builtins.str] = None,
    metrics: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37fc9065eaf8c38954e699966c0c74352be222946da46bc209661231af2a4d8f(
    *,
    instances_distribution: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.InstancesDistributionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    launch_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutoScalingGroupPropsMixin.LaunchTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca1dce81a2b0bba2e63f9036327e9475489563e7b4234c2d26728f3898005811(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d4b00eb8cc6db6264ab2c0c332516656ac4ea34227c18b6ceb838450d3f97d(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ef6da868c53097ca2537edb063fe2dfd3b817becc7a1e66d9c37c2e984fd0e(
    *,
    notification_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a47b104e04a267ea129b2bbcfd48eb020e525123371472d4aeda16fe55cfe75(
    *,
    instance_family: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bab725832f0738fea8da8639a2f7c7a557b63172fa8c1a40c29eb1a8826db7a(
    *,
    key: typing.Optional[builtins.str] = None,
    propagate_at_launch: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4eb62967665d8c2ddc02ce2fce2c7a5aaa11a17e82c5319d0a620f3793415a(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b8487d1a5f9987076b2ae5a130b6027d44209e3bc8f72b948c3574749c87c5(
    *,
    identifier: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46036d5996d93c96f2e87ac4774dbe2574531632440fb3230273e454919ae730(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26638ba4aec28c99d6953d709e4c72649214324e6ded32772df26f94ce93dd5a(
    *,
    associate_public_ip_address: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    block_device_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLaunchConfigurationPropsMixin.BlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    classic_link_vpc_id: typing.Optional[builtins.str] = None,
    classic_link_vpc_security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ebs_optimized: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    iam_instance_profile: typing.Optional[builtins.str] = None,
    image_id: typing.Optional[builtins.str] = None,
    instance_id: typing.Optional[builtins.str] = None,
    instance_monitoring: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    instance_type: typing.Optional[builtins.str] = None,
    kernel_id: typing.Optional[builtins.str] = None,
    key_name: typing.Optional[builtins.str] = None,
    launch_configuration_name: typing.Optional[builtins.str] = None,
    metadata_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLaunchConfigurationPropsMixin.MetadataOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    placement_tenancy: typing.Optional[builtins.str] = None,
    ram_disk_id: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    spot_price: typing.Optional[builtins.str] = None,
    user_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291ca37c88883ecd8f8bb52e25d86c0d0949f2647e560fa7d04e8e9abf63a015(
    props: typing.Union[CfnLaunchConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df01651555fa4a5b52f1c64c6a8f228783be1545dba024c33f9b37dc17e0cbb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c2595566576f4ba66967c97ced5128828c0705b29b73e5a45e595b2942ab5a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db99c9dc1d78e8cec57b0f4fb2bc5a65ebf1d5277ee9ac947eda6630a50371a(
    *,
    device_name: typing.Optional[builtins.str] = None,
    ebs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLaunchConfigurationPropsMixin.BlockDeviceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    no_device: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    virtual_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297d5e975a56478f1b4e23756a19d37be35192e5099be3e81b995d49c9f0b377(
    *,
    delete_on_termination: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    iops: typing.Optional[jsii.Number] = None,
    snapshot_id: typing.Optional[builtins.str] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_size: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9766befcdf389aa53bf8f87087474bb986df07ef90ac4366e56ab2c976c718(
    *,
    http_endpoint: typing.Optional[builtins.str] = None,
    http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
    http_tokens: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39cf4fd87415a577af69696e67fc58b48c56e1acc5834a2b836fb9fa6412b1f2(
    *,
    auto_scaling_group_name: typing.Optional[builtins.str] = None,
    default_result: typing.Optional[builtins.str] = None,
    heartbeat_timeout: typing.Optional[jsii.Number] = None,
    lifecycle_hook_name: typing.Optional[builtins.str] = None,
    lifecycle_transition: typing.Optional[builtins.str] = None,
    notification_metadata: typing.Optional[builtins.str] = None,
    notification_target_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48590fc071dd71fddeeb617eaee2c4081a5708803d29f31422808e5d7af12ca(
    props: typing.Union[CfnLifecycleHookMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0420a3a0d08815154075a4451dbaca1fe0b6daaf446b26b5c83636244da901d9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0912d4453715d7e5f18ee8b48c21568b64ec6401b53922db67333da8b148a0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c4008cce30233c624d71e27708e70d8950edef475caadec49de17a2aba1619(
    *,
    adjustment_type: typing.Optional[builtins.str] = None,
    auto_scaling_group_name: typing.Optional[builtins.str] = None,
    cooldown: typing.Optional[builtins.str] = None,
    estimated_instance_warmup: typing.Optional[jsii.Number] = None,
    metric_aggregation_type: typing.Optional[builtins.str] = None,
    min_adjustment_magnitude: typing.Optional[jsii.Number] = None,
    policy_type: typing.Optional[builtins.str] = None,
    predictive_scaling_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scaling_adjustment: typing.Optional[jsii.Number] = None,
    step_adjustments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.StepAdjustmentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    target_tracking_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.TargetTrackingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__626f59fdada379cf43df75058ec2c21b0f11170327460ea379d56c3c99e87273(
    props: typing.Union[CfnScalingPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d2cbaca1650c158d9361d2ce0b38458633a60880d992d858c1cf7aa4ec5764b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c1b8f99162eeefd0d6586276c1976760ea9a048a4591472d53fdf184b98e94(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e12f006b0109585b541fe6aa803f6ba9ed04edae31812a9e04e813121530a96(
    *,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.MetricDimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    metric_name: typing.Optional[builtins.str] = None,
    metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.TargetTrackingMetricDataQueryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    namespace: typing.Optional[builtins.str] = None,
    period: typing.Optional[jsii.Number] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7827e38e69fe15a8fd10b9b5f981f78729522faa0d2aa923a48f5cb2ae53b3e9(
    *,
    expression: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    label: typing.Optional[builtins.str] = None,
    metric_stat: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.MetricStatProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    return_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b95e6fbe31e689335ef892f5b2cf8940ccd4eb1b9d1538da833dd88a1f27a1(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6fa359a022d1779a019c46c53309cefc3e789ffb19c7be1db86c3fa633968da(
    *,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.MetricDimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    metric_name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0325b9064c114ca27ca564659302b13797c5b8395fecc8b33da51c37f3d79f2e(
    *,
    metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.MetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stat: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2d30fdbbe1726ab2d122f9228257cce204cc96aaa2a9985477f961a01d4595(
    *,
    predefined_metric_type: typing.Optional[builtins.str] = None,
    resource_label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e469a14daceef9874db667bc97d0d4d1649ee15a59cf04c8d4d9665f9eb1cc4(
    *,
    max_capacity_breach_behavior: typing.Optional[builtins.str] = None,
    max_capacity_buffer: typing.Optional[jsii.Number] = None,
    metric_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingMetricSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    mode: typing.Optional[builtins.str] = None,
    scheduling_buffer_time: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31e98734bbaf4015651830a5fe49e1faa0195cbf477d09ee1aff48c18650133(
    *,
    metric_data_queries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.MetricDataQueryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ade36ca9544d2554d574311640f588409e85a6199bbfab6742a4a79523b9ca(
    *,
    metric_data_queries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.MetricDataQueryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a24ef42c8040877666fa98c98b8e283cad9d081843fa5b0af2c4cfd479221678(
    *,
    metric_data_queries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.MetricDataQueryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e99268a01568fa2fa84222e5202606c46deba64e49be381c10783d37a72bc81(
    *,
    customized_capacity_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedCapacityMetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    customized_load_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedLoadMetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    customized_scaling_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingCustomizedScalingMetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    predefined_load_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedLoadMetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    predefined_metric_pair_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedMetricPairProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    predefined_scaling_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredictiveScalingPredefinedScalingMetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac9d2db0e4916aea7221b5277fcfff0d73afdb152a5e070a72b5f674641e80b(
    *,
    predefined_metric_type: typing.Optional[builtins.str] = None,
    resource_label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3edab15d784b7230377431e9dab18551bbe27a78bc011bed7beeb2a5d31b8d8(
    *,
    predefined_metric_type: typing.Optional[builtins.str] = None,
    resource_label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3801a676f874b6a57ab2453f5a792bc523049ba2b1bb78ddb9f387c8bfe563ba(
    *,
    predefined_metric_type: typing.Optional[builtins.str] = None,
    resource_label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f8c7356e7d7a010a857d77381370ff2bf0351091b3af93cf098ca467ffca0c(
    *,
    metric_interval_lower_bound: typing.Optional[jsii.Number] = None,
    metric_interval_upper_bound: typing.Optional[jsii.Number] = None,
    scaling_adjustment: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1923583cd136397d741bea5979ce8de323fe3d064f0c6468f86f0936512e3986(
    *,
    customized_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.CustomizedMetricSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    disable_scale_in: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    predefined_metric_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.PredefinedMetricSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__094539f2946d1fe4f8d540fb200ef92e8e1d35629556cb2d77e3bd6765162bf9(
    *,
    expression: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    label: typing.Optional[builtins.str] = None,
    metric_stat: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.TargetTrackingMetricStatProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    period: typing.Optional[jsii.Number] = None,
    return_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02bb5a30f05747c467ea003d9e69c6f967bc07b941730a88469e0360954c105e(
    *,
    metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScalingPolicyPropsMixin.MetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    period: typing.Optional[jsii.Number] = None,
    stat: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e83a36efe0e01a18dccebae5abcc947df0d5ee0f5a071cf7e62e7ed96db002(
    *,
    auto_scaling_group_name: typing.Optional[builtins.str] = None,
    desired_capacity: typing.Optional[jsii.Number] = None,
    end_time: typing.Optional[builtins.str] = None,
    max_size: typing.Optional[jsii.Number] = None,
    min_size: typing.Optional[jsii.Number] = None,
    recurrence: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__476df05d25605faeb057de0f69d66c56647a07832054471c6163cc19b5c42089(
    props: typing.Union[CfnScheduledActionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb00b1784478e57a3cfe4f3230f3d15fd7037bdec8585df4c4cb3130b7aa34f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2e966a395f19c76c991a0c4943ca969c9bd7116bd3fffd79f80dfb28108da4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cde652ffdf3bee0d1ff5db9c374551126f7b645191aa20ab01fe3f58a56c2eb(
    *,
    auto_scaling_group_name: typing.Optional[builtins.str] = None,
    instance_reuse_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWarmPoolPropsMixin.InstanceReusePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_group_prepared_capacity: typing.Optional[jsii.Number] = None,
    min_size: typing.Optional[jsii.Number] = None,
    pool_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8707d4f34cd0e246d41848dc311bf46197e3913ba9867f3844b5cfdf53801602(
    props: typing.Union[CfnWarmPoolMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eef686c017c7014b8e43a03ea9b57f100f41a4a4dad563a45355bdca65cdd7d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37e867b40070cc0eba579ba02f73deb8970325d06da4ea7b2e983b131c6f37c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd5a5f58fe994dd0f6570fbb32d539933d97430e33503da4e4be7f56a13ded99(
    *,
    reuse_on_scale_in: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
