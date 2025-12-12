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
    jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "additional_info": "additionalInfo",
        "applications": "applications",
        "auto_scaling_role": "autoScalingRole",
        "auto_termination_policy": "autoTerminationPolicy",
        "bootstrap_actions": "bootstrapActions",
        "configurations": "configurations",
        "custom_ami_id": "customAmiId",
        "ebs_root_volume_iops": "ebsRootVolumeIops",
        "ebs_root_volume_size": "ebsRootVolumeSize",
        "ebs_root_volume_throughput": "ebsRootVolumeThroughput",
        "instances": "instances",
        "job_flow_role": "jobFlowRole",
        "kerberos_attributes": "kerberosAttributes",
        "log_encryption_kms_key_id": "logEncryptionKmsKeyId",
        "log_uri": "logUri",
        "managed_scaling_policy": "managedScalingPolicy",
        "name": "name",
        "os_release_label": "osReleaseLabel",
        "placement_group_configs": "placementGroupConfigs",
        "release_label": "releaseLabel",
        "scale_down_behavior": "scaleDownBehavior",
        "security_configuration": "securityConfiguration",
        "service_role": "serviceRole",
        "step_concurrency_level": "stepConcurrencyLevel",
        "steps": "steps",
        "tags": "tags",
        "visible_to_all_users": "visibleToAllUsers",
    },
)
class CfnClusterMixinProps:
    def __init__(
        self,
        *,
        additional_info: typing.Any = None,
        applications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ApplicationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        auto_scaling_role: typing.Optional[builtins.str] = None,
        auto_termination_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.AutoTerminationPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        bootstrap_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.BootstrapActionConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        custom_ami_id: typing.Optional[builtins.str] = None,
        ebs_root_volume_iops: typing.Optional[jsii.Number] = None,
        ebs_root_volume_size: typing.Optional[jsii.Number] = None,
        ebs_root_volume_throughput: typing.Optional[jsii.Number] = None,
        instances: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.JobFlowInstancesConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        job_flow_role: typing.Optional[builtins.str] = None,
        kerberos_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.KerberosAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        log_encryption_kms_key_id: typing.Optional[builtins.str] = None,
        log_uri: typing.Optional[builtins.str] = None,
        managed_scaling_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ManagedScalingPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        os_release_label: typing.Optional[builtins.str] = None,
        placement_group_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.PlacementGroupConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        release_label: typing.Optional[builtins.str] = None,
        scale_down_behavior: typing.Optional[builtins.str] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        service_role: typing.Optional[builtins.str] = None,
        step_concurrency_level: typing.Optional[jsii.Number] = None,
        steps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.StepConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        visible_to_all_users: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''Properties for CfnClusterPropsMixin.

        :param additional_info: A JSON string for selecting additional features.
        :param applications: The applications to install on this cluster, for example, Spark, Flink, Oozie, Zeppelin, and so on.
        :param auto_scaling_role: An IAM role for automatic scaling policies. The default role is ``EMR_AutoScaling_DefaultRole`` . The IAM role provides permissions that the automatic scaling feature requires to launch and terminate Amazon EC2 instances in an instance group.
        :param auto_termination_policy: An auto-termination policy for an Amazon EMR cluster. An auto-termination policy defines the amount of idle time in seconds after which a cluster automatically terminates. For alternative cluster termination options, see `Control cluster termination <https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-plan-termination.html>`_ .
        :param bootstrap_actions: A list of bootstrap actions to run before Hadoop starts on the cluster nodes.
        :param configurations: Applies only to Amazon EMR releases 4.x and later. The list of configurations that are supplied to the Amazon EMR cluster.
        :param custom_ami_id: Available only in Amazon EMR releases 5.7.0 and later. The ID of a custom Amazon EBS-backed Linux AMI if the cluster uses a custom AMI.
        :param ebs_root_volume_iops: The IOPS, of the Amazon EBS root device volume of the Linux AMI that is used for each Amazon EC2 instance. Available in Amazon EMR releases 6.15.0 and later.
        :param ebs_root_volume_size: The size, in GiB, of the Amazon EBS root device volume of the Linux AMI that is used for each Amazon EC2 instance. Available in Amazon EMR releases 4.x and later.
        :param ebs_root_volume_throughput: The throughput, in MiB/s, of the Amazon EBS root device volume of the Linux AMI that is used for each Amazon EC2 instance. Available in Amazon EMR releases 6.15.0 and later.
        :param instances: A specification of the number and type of Amazon EC2 instances.
        :param job_flow_role: Also called instance profile and Amazon EC2 role. An IAM role for an Amazon EMR cluster. The Amazon EC2 instances of the cluster assume this role. The default role is ``EMR_EC2_DefaultRole`` . In order to use the default role, you must have already created it using the AWS CLI or console.
        :param kerberos_attributes: Attributes for Kerberos configuration when Kerberos authentication is enabled using a security configuration. For more information see `Use Kerberos Authentication <https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-kerberos.html>`_ in the *Amazon EMR Management Guide* .
        :param log_encryption_kms_key_id: The AWS KMS key used for encrypting log files. This attribute is only available with Amazon EMR 5.30.0 and later, excluding Amazon EMR 6.0.0.
        :param log_uri: The path to the Amazon S3 location where logs for this cluster are stored.
        :param managed_scaling_policy: Creates or updates a managed scaling policy for an Amazon EMR cluster. The managed scaling policy defines the limits for resources, such as Amazon EC2 instances that can be added or terminated from a cluster. The policy only applies to the core and task nodes. The master node cannot be scaled after initial configuration.
        :param name: The name of the cluster. This parameter can't contain the characters <, >, $, |, or ` (backtick).
        :param os_release_label: The Amazon Linux release specified in a cluster launch RunJobFlow request. If no Amazon Linux release was specified, the default Amazon Linux release is shown in the response.
        :param placement_group_configs: 
        :param release_label: The Amazon EMR release label, which determines the version of open-source application packages installed on the cluster. Release labels are in the form ``emr-x.x.x`` , where x.x.x is an Amazon EMR release version such as ``emr-5.14.0`` . For more information about Amazon EMR release versions and included application versions and features, see ` <https://docs.aws.amazon.com/emr/latest/ReleaseGuide/>`_ . The release label applies only to Amazon EMR releases version 4.0 and later. Earlier versions use ``AmiVersion`` .
        :param scale_down_behavior: The way that individual Amazon EC2 instances terminate when an automatic scale-in activity occurs or an instance group is resized. ``TERMINATE_AT_INSTANCE_HOUR`` indicates that Amazon EMR terminates nodes at the instance-hour boundary, regardless of when the request to terminate the instance was submitted. This option is only available with Amazon EMR 5.1.0 and later and is the default for clusters created using that version. ``TERMINATE_AT_TASK_COMPLETION`` indicates that Amazon EMR adds nodes to a deny list and drains tasks from nodes before terminating the Amazon EC2 instances, regardless of the instance-hour boundary. With either behavior, Amazon EMR removes the least active nodes first and blocks instance termination if it could lead to HDFS corruption. ``TERMINATE_AT_TASK_COMPLETION`` is available only in Amazon EMR releases 4.1.0 and later, and is the default for versions of Amazon EMR earlier than 5.1.0.
        :param security_configuration: The name of the security configuration applied to the cluster.
        :param service_role: The IAM role that Amazon EMR assumes in order to access AWS resources on your behalf.
        :param step_concurrency_level: Specifies the number of steps that can be executed concurrently. The default value is ``1`` . The maximum value is ``256`` .
        :param steps: A list of steps to run.
        :param tags: A list of tags associated with a cluster.
        :param visible_to_all_users: Indicates whether the cluster is visible to all IAM users of the AWS account associated with the cluster. If this value is set to ``true`` , all IAM users of that AWS account can view and manage the cluster if they have the proper policy permissions set. If this value is ``false`` , only the IAM user that created the cluster can view and manage it. This value can be changed using the SetVisibleToAllUsers action. .. epigraph:: When you create clusters directly through the EMR console or API, this value is set to ``true`` by default. However, for ``AWS::EMR::Cluster`` resources in CloudFormation, the default is ``false`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
            
            # additional_info: Any
            # configuration_property_: emr_mixins.CfnClusterPropsMixin.ConfigurationProperty
            
            cfn_cluster_mixin_props = emr_mixins.CfnClusterMixinProps(
                additional_info=additional_info,
                applications=[emr_mixins.CfnClusterPropsMixin.ApplicationProperty(
                    additional_info={
                        "additional_info_key": "additionalInfo"
                    },
                    args=["args"],
                    name="name",
                    version="version"
                )],
                auto_scaling_role="autoScalingRole",
                auto_termination_policy=emr_mixins.CfnClusterPropsMixin.AutoTerminationPolicyProperty(
                    idle_timeout=123
                ),
                bootstrap_actions=[emr_mixins.CfnClusterPropsMixin.BootstrapActionConfigProperty(
                    name="name",
                    script_bootstrap_action=emr_mixins.CfnClusterPropsMixin.ScriptBootstrapActionConfigProperty(
                        args=["args"],
                        path="path"
                    )
                )],
                configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                    classification="classification",
                    configuration_properties={
                        "configuration_properties_key": "configurationProperties"
                    },
                    configurations=[configuration_property_]
                )],
                custom_ami_id="customAmiId",
                ebs_root_volume_iops=123,
                ebs_root_volume_size=123,
                ebs_root_volume_throughput=123,
                instances=emr_mixins.CfnClusterPropsMixin.JobFlowInstancesConfigProperty(
                    additional_master_security_groups=["additionalMasterSecurityGroups"],
                    additional_slave_security_groups=["additionalSlaveSecurityGroups"],
                    core_instance_fleet=emr_mixins.CfnClusterPropsMixin.InstanceFleetConfigProperty(
                        instance_type_configs=[emr_mixins.CfnClusterPropsMixin.InstanceTypeConfigProperty(
                            bid_price="bidPrice",
                            bid_price_as_percentage_of_on_demand_price=123,
                            configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                                classification="classification",
                                configuration_properties={
                                    "configuration_properties_key": "configurationProperties"
                                },
                                configurations=[configuration_property_]
                            )],
                            custom_ami_id="customAmiId",
                            ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                                ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                                    volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                        iops=123,
                                        size_in_gb=123,
                                        throughput=123,
                                        volume_type="volumeType"
                                    ),
                                    volumes_per_instance=123
                                )],
                                ebs_optimized=False
                            ),
                            instance_type="instanceType",
                            priority=123,
                            weighted_capacity=123
                        )],
                        launch_specifications=emr_mixins.CfnClusterPropsMixin.InstanceFleetProvisioningSpecificationsProperty(
                            on_demand_specification=emr_mixins.CfnClusterPropsMixin.OnDemandProvisioningSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                                    capacity_reservation_preference="capacityReservationPreference",
                                    capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                                    usage_strategy="usageStrategy"
                                )
                            ),
                            spot_specification=emr_mixins.CfnClusterPropsMixin.SpotProvisioningSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                block_duration_minutes=123,
                                timeout_action="timeoutAction",
                                timeout_duration_minutes=123
                            )
                        ),
                        name="name",
                        resize_specifications=emr_mixins.CfnClusterPropsMixin.InstanceFleetResizingSpecificationsProperty(
                            on_demand_resize_specification=emr_mixins.CfnClusterPropsMixin.OnDemandResizingSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                                    capacity_reservation_preference="capacityReservationPreference",
                                    capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                                    usage_strategy="usageStrategy"
                                ),
                                timeout_duration_minutes=123
                            ),
                            spot_resize_specification=emr_mixins.CfnClusterPropsMixin.SpotResizingSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                timeout_duration_minutes=123
                            )
                        ),
                        target_on_demand_capacity=123,
                        target_spot_capacity=123
                    ),
                    core_instance_group=emr_mixins.CfnClusterPropsMixin.InstanceGroupConfigProperty(
                        auto_scaling_policy=emr_mixins.CfnClusterPropsMixin.AutoScalingPolicyProperty(
                            constraints=emr_mixins.CfnClusterPropsMixin.ScalingConstraintsProperty(
                                max_capacity=123,
                                min_capacity=123
                            ),
                            rules=[emr_mixins.CfnClusterPropsMixin.ScalingRuleProperty(
                                action=emr_mixins.CfnClusterPropsMixin.ScalingActionProperty(
                                    market="market",
                                    simple_scaling_policy_configuration=emr_mixins.CfnClusterPropsMixin.SimpleScalingPolicyConfigurationProperty(
                                        adjustment_type="adjustmentType",
                                        cool_down=123,
                                        scaling_adjustment=123
                                    )
                                ),
                                description="description",
                                name="name",
                                trigger=emr_mixins.CfnClusterPropsMixin.ScalingTriggerProperty(
                                    cloud_watch_alarm_definition=emr_mixins.CfnClusterPropsMixin.CloudWatchAlarmDefinitionProperty(
                                        comparison_operator="comparisonOperator",
                                        dimensions=[emr_mixins.CfnClusterPropsMixin.MetricDimensionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        evaluation_periods=123,
                                        metric_name="metricName",
                                        namespace="namespace",
                                        period=123,
                                        statistic="statistic",
                                        threshold=123,
                                        unit="unit"
                                    )
                                )
                            )]
                        ),
                        bid_price="bidPrice",
                        configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                            classification="classification",
                            configuration_properties={
                                "configuration_properties_key": "configurationProperties"
                            },
                            configurations=[configuration_property_]
                        )],
                        custom_ami_id="customAmiId",
                        ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                            ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                                volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                    iops=123,
                                    size_in_gb=123,
                                    throughput=123,
                                    volume_type="volumeType"
                                ),
                                volumes_per_instance=123
                            )],
                            ebs_optimized=False
                        ),
                        instance_count=123,
                        instance_type="instanceType",
                        market="market",
                        name="name"
                    ),
                    ec2_key_name="ec2KeyName",
                    ec2_subnet_id="ec2SubnetId",
                    ec2_subnet_ids=["ec2SubnetIds"],
                    emr_managed_master_security_group="emrManagedMasterSecurityGroup",
                    emr_managed_slave_security_group="emrManagedSlaveSecurityGroup",
                    hadoop_version="hadoopVersion",
                    keep_job_flow_alive_when_no_steps=False,
                    master_instance_fleet=emr_mixins.CfnClusterPropsMixin.InstanceFleetConfigProperty(
                        instance_type_configs=[emr_mixins.CfnClusterPropsMixin.InstanceTypeConfigProperty(
                            bid_price="bidPrice",
                            bid_price_as_percentage_of_on_demand_price=123,
                            configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                                classification="classification",
                                configuration_properties={
                                    "configuration_properties_key": "configurationProperties"
                                },
                                configurations=[configuration_property_]
                            )],
                            custom_ami_id="customAmiId",
                            ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                                ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                                    volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                        iops=123,
                                        size_in_gb=123,
                                        throughput=123,
                                        volume_type="volumeType"
                                    ),
                                    volumes_per_instance=123
                                )],
                                ebs_optimized=False
                            ),
                            instance_type="instanceType",
                            priority=123,
                            weighted_capacity=123
                        )],
                        launch_specifications=emr_mixins.CfnClusterPropsMixin.InstanceFleetProvisioningSpecificationsProperty(
                            on_demand_specification=emr_mixins.CfnClusterPropsMixin.OnDemandProvisioningSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                                    capacity_reservation_preference="capacityReservationPreference",
                                    capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                                    usage_strategy="usageStrategy"
                                )
                            ),
                            spot_specification=emr_mixins.CfnClusterPropsMixin.SpotProvisioningSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                block_duration_minutes=123,
                                timeout_action="timeoutAction",
                                timeout_duration_minutes=123
                            )
                        ),
                        name="name",
                        resize_specifications=emr_mixins.CfnClusterPropsMixin.InstanceFleetResizingSpecificationsProperty(
                            on_demand_resize_specification=emr_mixins.CfnClusterPropsMixin.OnDemandResizingSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                                    capacity_reservation_preference="capacityReservationPreference",
                                    capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                                    usage_strategy="usageStrategy"
                                ),
                                timeout_duration_minutes=123
                            ),
                            spot_resize_specification=emr_mixins.CfnClusterPropsMixin.SpotResizingSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                timeout_duration_minutes=123
                            )
                        ),
                        target_on_demand_capacity=123,
                        target_spot_capacity=123
                    ),
                    master_instance_group=emr_mixins.CfnClusterPropsMixin.InstanceGroupConfigProperty(
                        auto_scaling_policy=emr_mixins.CfnClusterPropsMixin.AutoScalingPolicyProperty(
                            constraints=emr_mixins.CfnClusterPropsMixin.ScalingConstraintsProperty(
                                max_capacity=123,
                                min_capacity=123
                            ),
                            rules=[emr_mixins.CfnClusterPropsMixin.ScalingRuleProperty(
                                action=emr_mixins.CfnClusterPropsMixin.ScalingActionProperty(
                                    market="market",
                                    simple_scaling_policy_configuration=emr_mixins.CfnClusterPropsMixin.SimpleScalingPolicyConfigurationProperty(
                                        adjustment_type="adjustmentType",
                                        cool_down=123,
                                        scaling_adjustment=123
                                    )
                                ),
                                description="description",
                                name="name",
                                trigger=emr_mixins.CfnClusterPropsMixin.ScalingTriggerProperty(
                                    cloud_watch_alarm_definition=emr_mixins.CfnClusterPropsMixin.CloudWatchAlarmDefinitionProperty(
                                        comparison_operator="comparisonOperator",
                                        dimensions=[emr_mixins.CfnClusterPropsMixin.MetricDimensionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        evaluation_periods=123,
                                        metric_name="metricName",
                                        namespace="namespace",
                                        period=123,
                                        statistic="statistic",
                                        threshold=123,
                                        unit="unit"
                                    )
                                )
                            )]
                        ),
                        bid_price="bidPrice",
                        configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                            classification="classification",
                            configuration_properties={
                                "configuration_properties_key": "configurationProperties"
                            },
                            configurations=[configuration_property_]
                        )],
                        custom_ami_id="customAmiId",
                        ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                            ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                                volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                    iops=123,
                                    size_in_gb=123,
                                    throughput=123,
                                    volume_type="volumeType"
                                ),
                                volumes_per_instance=123
                            )],
                            ebs_optimized=False
                        ),
                        instance_count=123,
                        instance_type="instanceType",
                        market="market",
                        name="name"
                    ),
                    placement=emr_mixins.CfnClusterPropsMixin.PlacementTypeProperty(
                        availability_zone="availabilityZone"
                    ),
                    service_access_security_group="serviceAccessSecurityGroup",
                    task_instance_fleets=[emr_mixins.CfnClusterPropsMixin.InstanceFleetConfigProperty(
                        instance_type_configs=[emr_mixins.CfnClusterPropsMixin.InstanceTypeConfigProperty(
                            bid_price="bidPrice",
                            bid_price_as_percentage_of_on_demand_price=123,
                            configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                                classification="classification",
                                configuration_properties={
                                    "configuration_properties_key": "configurationProperties"
                                },
                                configurations=[configuration_property_]
                            )],
                            custom_ami_id="customAmiId",
                            ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                                ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                                    volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                        iops=123,
                                        size_in_gb=123,
                                        throughput=123,
                                        volume_type="volumeType"
                                    ),
                                    volumes_per_instance=123
                                )],
                                ebs_optimized=False
                            ),
                            instance_type="instanceType",
                            priority=123,
                            weighted_capacity=123
                        )],
                        launch_specifications=emr_mixins.CfnClusterPropsMixin.InstanceFleetProvisioningSpecificationsProperty(
                            on_demand_specification=emr_mixins.CfnClusterPropsMixin.OnDemandProvisioningSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                                    capacity_reservation_preference="capacityReservationPreference",
                                    capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                                    usage_strategy="usageStrategy"
                                )
                            ),
                            spot_specification=emr_mixins.CfnClusterPropsMixin.SpotProvisioningSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                block_duration_minutes=123,
                                timeout_action="timeoutAction",
                                timeout_duration_minutes=123
                            )
                        ),
                        name="name",
                        resize_specifications=emr_mixins.CfnClusterPropsMixin.InstanceFleetResizingSpecificationsProperty(
                            on_demand_resize_specification=emr_mixins.CfnClusterPropsMixin.OnDemandResizingSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                                    capacity_reservation_preference="capacityReservationPreference",
                                    capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                                    usage_strategy="usageStrategy"
                                ),
                                timeout_duration_minutes=123
                            ),
                            spot_resize_specification=emr_mixins.CfnClusterPropsMixin.SpotResizingSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                timeout_duration_minutes=123
                            )
                        ),
                        target_on_demand_capacity=123,
                        target_spot_capacity=123
                    )],
                    task_instance_groups=[emr_mixins.CfnClusterPropsMixin.InstanceGroupConfigProperty(
                        auto_scaling_policy=emr_mixins.CfnClusterPropsMixin.AutoScalingPolicyProperty(
                            constraints=emr_mixins.CfnClusterPropsMixin.ScalingConstraintsProperty(
                                max_capacity=123,
                                min_capacity=123
                            ),
                            rules=[emr_mixins.CfnClusterPropsMixin.ScalingRuleProperty(
                                action=emr_mixins.CfnClusterPropsMixin.ScalingActionProperty(
                                    market="market",
                                    simple_scaling_policy_configuration=emr_mixins.CfnClusterPropsMixin.SimpleScalingPolicyConfigurationProperty(
                                        adjustment_type="adjustmentType",
                                        cool_down=123,
                                        scaling_adjustment=123
                                    )
                                ),
                                description="description",
                                name="name",
                                trigger=emr_mixins.CfnClusterPropsMixin.ScalingTriggerProperty(
                                    cloud_watch_alarm_definition=emr_mixins.CfnClusterPropsMixin.CloudWatchAlarmDefinitionProperty(
                                        comparison_operator="comparisonOperator",
                                        dimensions=[emr_mixins.CfnClusterPropsMixin.MetricDimensionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        evaluation_periods=123,
                                        metric_name="metricName",
                                        namespace="namespace",
                                        period=123,
                                        statistic="statistic",
                                        threshold=123,
                                        unit="unit"
                                    )
                                )
                            )]
                        ),
                        bid_price="bidPrice",
                        configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                            classification="classification",
                            configuration_properties={
                                "configuration_properties_key": "configurationProperties"
                            },
                            configurations=[configuration_property_]
                        )],
                        custom_ami_id="customAmiId",
                        ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                            ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                                volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                    iops=123,
                                    size_in_gb=123,
                                    throughput=123,
                                    volume_type="volumeType"
                                ),
                                volumes_per_instance=123
                            )],
                            ebs_optimized=False
                        ),
                        instance_count=123,
                        instance_type="instanceType",
                        market="market",
                        name="name"
                    )],
                    termination_protected=False,
                    unhealthy_node_replacement=False
                ),
                job_flow_role="jobFlowRole",
                kerberos_attributes=emr_mixins.CfnClusterPropsMixin.KerberosAttributesProperty(
                    ad_domain_join_password="adDomainJoinPassword",
                    ad_domain_join_user="adDomainJoinUser",
                    cross_realm_trust_principal_password="crossRealmTrustPrincipalPassword",
                    kdc_admin_password="kdcAdminPassword",
                    realm="realm"
                ),
                log_encryption_kms_key_id="logEncryptionKmsKeyId",
                log_uri="logUri",
                managed_scaling_policy=emr_mixins.CfnClusterPropsMixin.ManagedScalingPolicyProperty(
                    compute_limits=emr_mixins.CfnClusterPropsMixin.ComputeLimitsProperty(
                        maximum_capacity_units=123,
                        maximum_core_capacity_units=123,
                        maximum_on_demand_capacity_units=123,
                        minimum_capacity_units=123,
                        unit_type="unitType"
                    ),
                    scaling_strategy="scalingStrategy",
                    utilization_performance_index=123
                ),
                name="name",
                os_release_label="osReleaseLabel",
                placement_group_configs=[emr_mixins.CfnClusterPropsMixin.PlacementGroupConfigProperty(
                    instance_role="instanceRole",
                    placement_strategy="placementStrategy"
                )],
                release_label="releaseLabel",
                scale_down_behavior="scaleDownBehavior",
                security_configuration="securityConfiguration",
                service_role="serviceRole",
                step_concurrency_level=123,
                steps=[emr_mixins.CfnClusterPropsMixin.StepConfigProperty(
                    action_on_failure="actionOnFailure",
                    hadoop_jar_step=emr_mixins.CfnClusterPropsMixin.HadoopJarStepConfigProperty(
                        args=["args"],
                        jar="jar",
                        main_class="mainClass",
                        step_properties=[emr_mixins.CfnClusterPropsMixin.KeyValueProperty(
                            key="key",
                            value="value"
                        )]
                    ),
                    name="name"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                visible_to_all_users=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__374ecef1a8ce47b143e5bb688cdefd4145db6e3fbded3fc66feb170c2f4f5f2d)
            check_type(argname="argument additional_info", value=additional_info, expected_type=type_hints["additional_info"])
            check_type(argname="argument applications", value=applications, expected_type=type_hints["applications"])
            check_type(argname="argument auto_scaling_role", value=auto_scaling_role, expected_type=type_hints["auto_scaling_role"])
            check_type(argname="argument auto_termination_policy", value=auto_termination_policy, expected_type=type_hints["auto_termination_policy"])
            check_type(argname="argument bootstrap_actions", value=bootstrap_actions, expected_type=type_hints["bootstrap_actions"])
            check_type(argname="argument configurations", value=configurations, expected_type=type_hints["configurations"])
            check_type(argname="argument custom_ami_id", value=custom_ami_id, expected_type=type_hints["custom_ami_id"])
            check_type(argname="argument ebs_root_volume_iops", value=ebs_root_volume_iops, expected_type=type_hints["ebs_root_volume_iops"])
            check_type(argname="argument ebs_root_volume_size", value=ebs_root_volume_size, expected_type=type_hints["ebs_root_volume_size"])
            check_type(argname="argument ebs_root_volume_throughput", value=ebs_root_volume_throughput, expected_type=type_hints["ebs_root_volume_throughput"])
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
            check_type(argname="argument job_flow_role", value=job_flow_role, expected_type=type_hints["job_flow_role"])
            check_type(argname="argument kerberos_attributes", value=kerberos_attributes, expected_type=type_hints["kerberos_attributes"])
            check_type(argname="argument log_encryption_kms_key_id", value=log_encryption_kms_key_id, expected_type=type_hints["log_encryption_kms_key_id"])
            check_type(argname="argument log_uri", value=log_uri, expected_type=type_hints["log_uri"])
            check_type(argname="argument managed_scaling_policy", value=managed_scaling_policy, expected_type=type_hints["managed_scaling_policy"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument os_release_label", value=os_release_label, expected_type=type_hints["os_release_label"])
            check_type(argname="argument placement_group_configs", value=placement_group_configs, expected_type=type_hints["placement_group_configs"])
            check_type(argname="argument release_label", value=release_label, expected_type=type_hints["release_label"])
            check_type(argname="argument scale_down_behavior", value=scale_down_behavior, expected_type=type_hints["scale_down_behavior"])
            check_type(argname="argument security_configuration", value=security_configuration, expected_type=type_hints["security_configuration"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
            check_type(argname="argument step_concurrency_level", value=step_concurrency_level, expected_type=type_hints["step_concurrency_level"])
            check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument visible_to_all_users", value=visible_to_all_users, expected_type=type_hints["visible_to_all_users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_info is not None:
            self._values["additional_info"] = additional_info
        if applications is not None:
            self._values["applications"] = applications
        if auto_scaling_role is not None:
            self._values["auto_scaling_role"] = auto_scaling_role
        if auto_termination_policy is not None:
            self._values["auto_termination_policy"] = auto_termination_policy
        if bootstrap_actions is not None:
            self._values["bootstrap_actions"] = bootstrap_actions
        if configurations is not None:
            self._values["configurations"] = configurations
        if custom_ami_id is not None:
            self._values["custom_ami_id"] = custom_ami_id
        if ebs_root_volume_iops is not None:
            self._values["ebs_root_volume_iops"] = ebs_root_volume_iops
        if ebs_root_volume_size is not None:
            self._values["ebs_root_volume_size"] = ebs_root_volume_size
        if ebs_root_volume_throughput is not None:
            self._values["ebs_root_volume_throughput"] = ebs_root_volume_throughput
        if instances is not None:
            self._values["instances"] = instances
        if job_flow_role is not None:
            self._values["job_flow_role"] = job_flow_role
        if kerberos_attributes is not None:
            self._values["kerberos_attributes"] = kerberos_attributes
        if log_encryption_kms_key_id is not None:
            self._values["log_encryption_kms_key_id"] = log_encryption_kms_key_id
        if log_uri is not None:
            self._values["log_uri"] = log_uri
        if managed_scaling_policy is not None:
            self._values["managed_scaling_policy"] = managed_scaling_policy
        if name is not None:
            self._values["name"] = name
        if os_release_label is not None:
            self._values["os_release_label"] = os_release_label
        if placement_group_configs is not None:
            self._values["placement_group_configs"] = placement_group_configs
        if release_label is not None:
            self._values["release_label"] = release_label
        if scale_down_behavior is not None:
            self._values["scale_down_behavior"] = scale_down_behavior
        if security_configuration is not None:
            self._values["security_configuration"] = security_configuration
        if service_role is not None:
            self._values["service_role"] = service_role
        if step_concurrency_level is not None:
            self._values["step_concurrency_level"] = step_concurrency_level
        if steps is not None:
            self._values["steps"] = steps
        if tags is not None:
            self._values["tags"] = tags
        if visible_to_all_users is not None:
            self._values["visible_to_all_users"] = visible_to_all_users

    @builtins.property
    def additional_info(self) -> typing.Any:
        '''A JSON string for selecting additional features.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-additionalinfo
        '''
        result = self._values.get("additional_info")
        return typing.cast(typing.Any, result)

    @builtins.property
    def applications(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ApplicationProperty"]]]]:
        '''The applications to install on this cluster, for example, Spark, Flink, Oozie, Zeppelin, and so on.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-applications
        '''
        result = self._values.get("applications")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ApplicationProperty"]]]], result)

    @builtins.property
    def auto_scaling_role(self) -> typing.Optional[builtins.str]:
        '''An IAM role for automatic scaling policies.

        The default role is ``EMR_AutoScaling_DefaultRole`` . The IAM role provides permissions that the automatic scaling feature requires to launch and terminate Amazon EC2 instances in an instance group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-autoscalingrole
        '''
        result = self._values.get("auto_scaling_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_termination_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.AutoTerminationPolicyProperty"]]:
        '''An auto-termination policy for an Amazon EMR cluster.

        An auto-termination policy defines the amount of idle time in seconds after which a cluster automatically terminates. For alternative cluster termination options, see `Control cluster termination <https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-plan-termination.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-autoterminationpolicy
        '''
        result = self._values.get("auto_termination_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.AutoTerminationPolicyProperty"]], result)

    @builtins.property
    def bootstrap_actions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.BootstrapActionConfigProperty"]]]]:
        '''A list of bootstrap actions to run before Hadoop starts on the cluster nodes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-bootstrapactions
        '''
        result = self._values.get("bootstrap_actions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.BootstrapActionConfigProperty"]]]], result)

    @builtins.property
    def configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ConfigurationProperty"]]]]:
        '''Applies only to Amazon EMR releases 4.x and later. The list of configurations that are supplied to the Amazon EMR cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-configurations
        '''
        result = self._values.get("configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ConfigurationProperty"]]]], result)

    @builtins.property
    def custom_ami_id(self) -> typing.Optional[builtins.str]:
        '''Available only in Amazon EMR releases 5.7.0 and later. The ID of a custom Amazon EBS-backed Linux AMI if the cluster uses a custom AMI.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-customamiid
        '''
        result = self._values.get("custom_ami_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ebs_root_volume_iops(self) -> typing.Optional[jsii.Number]:
        '''The IOPS, of the Amazon EBS root device volume of the Linux AMI that is used for each Amazon EC2 instance.

        Available in Amazon EMR releases 6.15.0 and later.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-ebsrootvolumeiops
        '''
        result = self._values.get("ebs_root_volume_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ebs_root_volume_size(self) -> typing.Optional[jsii.Number]:
        '''The size, in GiB, of the Amazon EBS root device volume of the Linux AMI that is used for each Amazon EC2 instance.

        Available in Amazon EMR releases 4.x and later.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-ebsrootvolumesize
        '''
        result = self._values.get("ebs_root_volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ebs_root_volume_throughput(self) -> typing.Optional[jsii.Number]:
        '''The throughput, in MiB/s, of the Amazon EBS root device volume of the Linux AMI that is used for each Amazon EC2 instance.

        Available in Amazon EMR releases 6.15.0 and later.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-ebsrootvolumethroughput
        '''
        result = self._values.get("ebs_root_volume_throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instances(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.JobFlowInstancesConfigProperty"]]:
        '''A specification of the number and type of Amazon EC2 instances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-instances
        '''
        result = self._values.get("instances")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.JobFlowInstancesConfigProperty"]], result)

    @builtins.property
    def job_flow_role(self) -> typing.Optional[builtins.str]:
        '''Also called instance profile and Amazon EC2 role.

        An IAM role for an Amazon EMR cluster. The Amazon EC2 instances of the cluster assume this role. The default role is ``EMR_EC2_DefaultRole`` . In order to use the default role, you must have already created it using the AWS CLI or console.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-jobflowrole
        '''
        result = self._values.get("job_flow_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kerberos_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.KerberosAttributesProperty"]]:
        '''Attributes for Kerberos configuration when Kerberos authentication is enabled using a security configuration.

        For more information see `Use Kerberos Authentication <https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-kerberos.html>`_ in the *Amazon EMR Management Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-kerberosattributes
        '''
        result = self._values.get("kerberos_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.KerberosAttributesProperty"]], result)

    @builtins.property
    def log_encryption_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The AWS KMS key used for encrypting log files.

        This attribute is only available with Amazon EMR 5.30.0 and later, excluding Amazon EMR 6.0.0.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-logencryptionkmskeyid
        '''
        result = self._values.get("log_encryption_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_uri(self) -> typing.Optional[builtins.str]:
        '''The path to the Amazon S3 location where logs for this cluster are stored.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-loguri
        '''
        result = self._values.get("log_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_scaling_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ManagedScalingPolicyProperty"]]:
        '''Creates or updates a managed scaling policy for an Amazon EMR cluster.

        The managed scaling policy defines the limits for resources, such as Amazon EC2 instances that can be added or terminated from a cluster. The policy only applies to the core and task nodes. The master node cannot be scaled after initial configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-managedscalingpolicy
        '''
        result = self._values.get("managed_scaling_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ManagedScalingPolicyProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the cluster.

        This parameter can't contain the characters <, >, $, |, or ` (backtick).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_release_label(self) -> typing.Optional[builtins.str]:
        '''The Amazon Linux release specified in a cluster launch RunJobFlow request.

        If no Amazon Linux release was specified, the default Amazon Linux release is shown in the response.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-osreleaselabel
        '''
        result = self._values.get("os_release_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def placement_group_configs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.PlacementGroupConfigProperty"]]]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-placementgroupconfigs
        '''
        result = self._values.get("placement_group_configs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.PlacementGroupConfigProperty"]]]], result)

    @builtins.property
    def release_label(self) -> typing.Optional[builtins.str]:
        '''The Amazon EMR release label, which determines the version of open-source application packages installed on the cluster.

        Release labels are in the form ``emr-x.x.x`` , where x.x.x is an Amazon EMR release version such as ``emr-5.14.0`` . For more information about Amazon EMR release versions and included application versions and features, see ` <https://docs.aws.amazon.com/emr/latest/ReleaseGuide/>`_ . The release label applies only to Amazon EMR releases version 4.0 and later. Earlier versions use ``AmiVersion`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-releaselabel
        '''
        result = self._values.get("release_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scale_down_behavior(self) -> typing.Optional[builtins.str]:
        '''The way that individual Amazon EC2 instances terminate when an automatic scale-in activity occurs or an instance group is resized.

        ``TERMINATE_AT_INSTANCE_HOUR`` indicates that Amazon EMR terminates nodes at the instance-hour boundary, regardless of when the request to terminate the instance was submitted. This option is only available with Amazon EMR 5.1.0 and later and is the default for clusters created using that version. ``TERMINATE_AT_TASK_COMPLETION`` indicates that Amazon EMR adds nodes to a deny list and drains tasks from nodes before terminating the Amazon EC2 instances, regardless of the instance-hour boundary. With either behavior, Amazon EMR removes the least active nodes first and blocks instance termination if it could lead to HDFS corruption. ``TERMINATE_AT_TASK_COMPLETION`` is available only in Amazon EMR releases 4.1.0 and later, and is the default for versions of Amazon EMR earlier than 5.1.0.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-scaledownbehavior
        '''
        result = self._values.get("scale_down_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_configuration(self) -> typing.Optional[builtins.str]:
        '''The name of the security configuration applied to the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-securityconfiguration
        '''
        result = self._values.get("security_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_role(self) -> typing.Optional[builtins.str]:
        '''The IAM role that Amazon EMR assumes in order to access AWS resources on your behalf.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-servicerole
        '''
        result = self._values.get("service_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def step_concurrency_level(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of steps that can be executed concurrently.

        The default value is ``1`` . The maximum value is ``256`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-stepconcurrencylevel
        '''
        result = self._values.get("step_concurrency_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def steps(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.StepConfigProperty"]]]]:
        '''A list of steps to run.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-steps
        '''
        result = self._values.get("steps")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.StepConfigProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags associated with a cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def visible_to_all_users(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether the cluster is visible to all IAM users of the AWS account associated with the cluster.

        If this value is set to ``true`` , all IAM users of that AWS account can view and manage the cluster if they have the proper policy permissions set. If this value is ``false`` , only the IAM user that created the cluster can view and manage it. This value can be changed using the SetVisibleToAllUsers action.
        .. epigraph::

           When you create clusters directly through the EMR console or API, this value is set to ``true`` by default. However, for ``AWS::EMR::Cluster`` resources in CloudFormation, the default is ``false`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html#cfn-emr-cluster-visibletoallusers
        '''
        result = self._values.get("visible_to_all_users")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnClusterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin",
):
    '''The ``AWS::EMR::Cluster`` resource specifies an Amazon EMR cluster.

    This cluster is a collection of Amazon EC2 instances that run open source big data frameworks and applications to process and analyze vast amounts of data. For more information, see the `Amazon EMR Management Guide <https://docs.aws.amazon.com//emr/latest/ManagementGuide/>`_ .

    Amazon EMR now supports launching task instance groups and task instance fleets as part of the ``AWS::EMR::Cluster`` resource. This can be done by using the ``JobFlowInstancesConfig`` property type's ``TaskInstanceGroups`` and ``TaskInstanceFleets`` subproperties. Using these subproperties reduces delays in provisioning task nodes compared to specifying task nodes with the ``AWS::EMR::InstanceGroupConfig`` and ``AWS::EMR::InstanceFleetConfig`` resources. Please refer to the examples at the bottom of this page to learn how to use these subproperties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-cluster.html
    :cloudformationResource: AWS::EMR::Cluster
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
        
        # additional_info: Any
        # configuration_property_: emr_mixins.CfnClusterPropsMixin.ConfigurationProperty
        
        cfn_cluster_props_mixin = emr_mixins.CfnClusterPropsMixin(emr_mixins.CfnClusterMixinProps(
            additional_info=additional_info,
            applications=[emr_mixins.CfnClusterPropsMixin.ApplicationProperty(
                additional_info={
                    "additional_info_key": "additionalInfo"
                },
                args=["args"],
                name="name",
                version="version"
            )],
            auto_scaling_role="autoScalingRole",
            auto_termination_policy=emr_mixins.CfnClusterPropsMixin.AutoTerminationPolicyProperty(
                idle_timeout=123
            ),
            bootstrap_actions=[emr_mixins.CfnClusterPropsMixin.BootstrapActionConfigProperty(
                name="name",
                script_bootstrap_action=emr_mixins.CfnClusterPropsMixin.ScriptBootstrapActionConfigProperty(
                    args=["args"],
                    path="path"
                )
            )],
            configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                classification="classification",
                configuration_properties={
                    "configuration_properties_key": "configurationProperties"
                },
                configurations=[configuration_property_]
            )],
            custom_ami_id="customAmiId",
            ebs_root_volume_iops=123,
            ebs_root_volume_size=123,
            ebs_root_volume_throughput=123,
            instances=emr_mixins.CfnClusterPropsMixin.JobFlowInstancesConfigProperty(
                additional_master_security_groups=["additionalMasterSecurityGroups"],
                additional_slave_security_groups=["additionalSlaveSecurityGroups"],
                core_instance_fleet=emr_mixins.CfnClusterPropsMixin.InstanceFleetConfigProperty(
                    instance_type_configs=[emr_mixins.CfnClusterPropsMixin.InstanceTypeConfigProperty(
                        bid_price="bidPrice",
                        bid_price_as_percentage_of_on_demand_price=123,
                        configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                            classification="classification",
                            configuration_properties={
                                "configuration_properties_key": "configurationProperties"
                            },
                            configurations=[configuration_property_]
                        )],
                        custom_ami_id="customAmiId",
                        ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                            ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                                volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                    iops=123,
                                    size_in_gb=123,
                                    throughput=123,
                                    volume_type="volumeType"
                                ),
                                volumes_per_instance=123
                            )],
                            ebs_optimized=False
                        ),
                        instance_type="instanceType",
                        priority=123,
                        weighted_capacity=123
                    )],
                    launch_specifications=emr_mixins.CfnClusterPropsMixin.InstanceFleetProvisioningSpecificationsProperty(
                        on_demand_specification=emr_mixins.CfnClusterPropsMixin.OnDemandProvisioningSpecificationProperty(
                            allocation_strategy="allocationStrategy",
                            capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                                capacity_reservation_preference="capacityReservationPreference",
                                capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                                usage_strategy="usageStrategy"
                            )
                        ),
                        spot_specification=emr_mixins.CfnClusterPropsMixin.SpotProvisioningSpecificationProperty(
                            allocation_strategy="allocationStrategy",
                            block_duration_minutes=123,
                            timeout_action="timeoutAction",
                            timeout_duration_minutes=123
                        )
                    ),
                    name="name",
                    resize_specifications=emr_mixins.CfnClusterPropsMixin.InstanceFleetResizingSpecificationsProperty(
                        on_demand_resize_specification=emr_mixins.CfnClusterPropsMixin.OnDemandResizingSpecificationProperty(
                            allocation_strategy="allocationStrategy",
                            capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                                capacity_reservation_preference="capacityReservationPreference",
                                capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                                usage_strategy="usageStrategy"
                            ),
                            timeout_duration_minutes=123
                        ),
                        spot_resize_specification=emr_mixins.CfnClusterPropsMixin.SpotResizingSpecificationProperty(
                            allocation_strategy="allocationStrategy",
                            timeout_duration_minutes=123
                        )
                    ),
                    target_on_demand_capacity=123,
                    target_spot_capacity=123
                ),
                core_instance_group=emr_mixins.CfnClusterPropsMixin.InstanceGroupConfigProperty(
                    auto_scaling_policy=emr_mixins.CfnClusterPropsMixin.AutoScalingPolicyProperty(
                        constraints=emr_mixins.CfnClusterPropsMixin.ScalingConstraintsProperty(
                            max_capacity=123,
                            min_capacity=123
                        ),
                        rules=[emr_mixins.CfnClusterPropsMixin.ScalingRuleProperty(
                            action=emr_mixins.CfnClusterPropsMixin.ScalingActionProperty(
                                market="market",
                                simple_scaling_policy_configuration=emr_mixins.CfnClusterPropsMixin.SimpleScalingPolicyConfigurationProperty(
                                    adjustment_type="adjustmentType",
                                    cool_down=123,
                                    scaling_adjustment=123
                                )
                            ),
                            description="description",
                            name="name",
                            trigger=emr_mixins.CfnClusterPropsMixin.ScalingTriggerProperty(
                                cloud_watch_alarm_definition=emr_mixins.CfnClusterPropsMixin.CloudWatchAlarmDefinitionProperty(
                                    comparison_operator="comparisonOperator",
                                    dimensions=[emr_mixins.CfnClusterPropsMixin.MetricDimensionProperty(
                                        key="key",
                                        value="value"
                                    )],
                                    evaluation_periods=123,
                                    metric_name="metricName",
                                    namespace="namespace",
                                    period=123,
                                    statistic="statistic",
                                    threshold=123,
                                    unit="unit"
                                )
                            )
                        )]
                    ),
                    bid_price="bidPrice",
                    configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                        classification="classification",
                        configuration_properties={
                            "configuration_properties_key": "configurationProperties"
                        },
                        configurations=[configuration_property_]
                    )],
                    custom_ami_id="customAmiId",
                    ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                        ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                            volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                iops=123,
                                size_in_gb=123,
                                throughput=123,
                                volume_type="volumeType"
                            ),
                            volumes_per_instance=123
                        )],
                        ebs_optimized=False
                    ),
                    instance_count=123,
                    instance_type="instanceType",
                    market="market",
                    name="name"
                ),
                ec2_key_name="ec2KeyName",
                ec2_subnet_id="ec2SubnetId",
                ec2_subnet_ids=["ec2SubnetIds"],
                emr_managed_master_security_group="emrManagedMasterSecurityGroup",
                emr_managed_slave_security_group="emrManagedSlaveSecurityGroup",
                hadoop_version="hadoopVersion",
                keep_job_flow_alive_when_no_steps=False,
                master_instance_fleet=emr_mixins.CfnClusterPropsMixin.InstanceFleetConfigProperty(
                    instance_type_configs=[emr_mixins.CfnClusterPropsMixin.InstanceTypeConfigProperty(
                        bid_price="bidPrice",
                        bid_price_as_percentage_of_on_demand_price=123,
                        configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                            classification="classification",
                            configuration_properties={
                                "configuration_properties_key": "configurationProperties"
                            },
                            configurations=[configuration_property_]
                        )],
                        custom_ami_id="customAmiId",
                        ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                            ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                                volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                    iops=123,
                                    size_in_gb=123,
                                    throughput=123,
                                    volume_type="volumeType"
                                ),
                                volumes_per_instance=123
                            )],
                            ebs_optimized=False
                        ),
                        instance_type="instanceType",
                        priority=123,
                        weighted_capacity=123
                    )],
                    launch_specifications=emr_mixins.CfnClusterPropsMixin.InstanceFleetProvisioningSpecificationsProperty(
                        on_demand_specification=emr_mixins.CfnClusterPropsMixin.OnDemandProvisioningSpecificationProperty(
                            allocation_strategy="allocationStrategy",
                            capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                                capacity_reservation_preference="capacityReservationPreference",
                                capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                                usage_strategy="usageStrategy"
                            )
                        ),
                        spot_specification=emr_mixins.CfnClusterPropsMixin.SpotProvisioningSpecificationProperty(
                            allocation_strategy="allocationStrategy",
                            block_duration_minutes=123,
                            timeout_action="timeoutAction",
                            timeout_duration_minutes=123
                        )
                    ),
                    name="name",
                    resize_specifications=emr_mixins.CfnClusterPropsMixin.InstanceFleetResizingSpecificationsProperty(
                        on_demand_resize_specification=emr_mixins.CfnClusterPropsMixin.OnDemandResizingSpecificationProperty(
                            allocation_strategy="allocationStrategy",
                            capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                                capacity_reservation_preference="capacityReservationPreference",
                                capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                                usage_strategy="usageStrategy"
                            ),
                            timeout_duration_minutes=123
                        ),
                        spot_resize_specification=emr_mixins.CfnClusterPropsMixin.SpotResizingSpecificationProperty(
                            allocation_strategy="allocationStrategy",
                            timeout_duration_minutes=123
                        )
                    ),
                    target_on_demand_capacity=123,
                    target_spot_capacity=123
                ),
                master_instance_group=emr_mixins.CfnClusterPropsMixin.InstanceGroupConfigProperty(
                    auto_scaling_policy=emr_mixins.CfnClusterPropsMixin.AutoScalingPolicyProperty(
                        constraints=emr_mixins.CfnClusterPropsMixin.ScalingConstraintsProperty(
                            max_capacity=123,
                            min_capacity=123
                        ),
                        rules=[emr_mixins.CfnClusterPropsMixin.ScalingRuleProperty(
                            action=emr_mixins.CfnClusterPropsMixin.ScalingActionProperty(
                                market="market",
                                simple_scaling_policy_configuration=emr_mixins.CfnClusterPropsMixin.SimpleScalingPolicyConfigurationProperty(
                                    adjustment_type="adjustmentType",
                                    cool_down=123,
                                    scaling_adjustment=123
                                )
                            ),
                            description="description",
                            name="name",
                            trigger=emr_mixins.CfnClusterPropsMixin.ScalingTriggerProperty(
                                cloud_watch_alarm_definition=emr_mixins.CfnClusterPropsMixin.CloudWatchAlarmDefinitionProperty(
                                    comparison_operator="comparisonOperator",
                                    dimensions=[emr_mixins.CfnClusterPropsMixin.MetricDimensionProperty(
                                        key="key",
                                        value="value"
                                    )],
                                    evaluation_periods=123,
                                    metric_name="metricName",
                                    namespace="namespace",
                                    period=123,
                                    statistic="statistic",
                                    threshold=123,
                                    unit="unit"
                                )
                            )
                        )]
                    ),
                    bid_price="bidPrice",
                    configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                        classification="classification",
                        configuration_properties={
                            "configuration_properties_key": "configurationProperties"
                        },
                        configurations=[configuration_property_]
                    )],
                    custom_ami_id="customAmiId",
                    ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                        ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                            volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                iops=123,
                                size_in_gb=123,
                                throughput=123,
                                volume_type="volumeType"
                            ),
                            volumes_per_instance=123
                        )],
                        ebs_optimized=False
                    ),
                    instance_count=123,
                    instance_type="instanceType",
                    market="market",
                    name="name"
                ),
                placement=emr_mixins.CfnClusterPropsMixin.PlacementTypeProperty(
                    availability_zone="availabilityZone"
                ),
                service_access_security_group="serviceAccessSecurityGroup",
                task_instance_fleets=[emr_mixins.CfnClusterPropsMixin.InstanceFleetConfigProperty(
                    instance_type_configs=[emr_mixins.CfnClusterPropsMixin.InstanceTypeConfigProperty(
                        bid_price="bidPrice",
                        bid_price_as_percentage_of_on_demand_price=123,
                        configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                            classification="classification",
                            configuration_properties={
                                "configuration_properties_key": "configurationProperties"
                            },
                            configurations=[configuration_property_]
                        )],
                        custom_ami_id="customAmiId",
                        ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                            ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                                volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                    iops=123,
                                    size_in_gb=123,
                                    throughput=123,
                                    volume_type="volumeType"
                                ),
                                volumes_per_instance=123
                            )],
                            ebs_optimized=False
                        ),
                        instance_type="instanceType",
                        priority=123,
                        weighted_capacity=123
                    )],
                    launch_specifications=emr_mixins.CfnClusterPropsMixin.InstanceFleetProvisioningSpecificationsProperty(
                        on_demand_specification=emr_mixins.CfnClusterPropsMixin.OnDemandProvisioningSpecificationProperty(
                            allocation_strategy="allocationStrategy",
                            capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                                capacity_reservation_preference="capacityReservationPreference",
                                capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                                usage_strategy="usageStrategy"
                            )
                        ),
                        spot_specification=emr_mixins.CfnClusterPropsMixin.SpotProvisioningSpecificationProperty(
                            allocation_strategy="allocationStrategy",
                            block_duration_minutes=123,
                            timeout_action="timeoutAction",
                            timeout_duration_minutes=123
                        )
                    ),
                    name="name",
                    resize_specifications=emr_mixins.CfnClusterPropsMixin.InstanceFleetResizingSpecificationsProperty(
                        on_demand_resize_specification=emr_mixins.CfnClusterPropsMixin.OnDemandResizingSpecificationProperty(
                            allocation_strategy="allocationStrategy",
                            capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                                capacity_reservation_preference="capacityReservationPreference",
                                capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                                usage_strategy="usageStrategy"
                            ),
                            timeout_duration_minutes=123
                        ),
                        spot_resize_specification=emr_mixins.CfnClusterPropsMixin.SpotResizingSpecificationProperty(
                            allocation_strategy="allocationStrategy",
                            timeout_duration_minutes=123
                        )
                    ),
                    target_on_demand_capacity=123,
                    target_spot_capacity=123
                )],
                task_instance_groups=[emr_mixins.CfnClusterPropsMixin.InstanceGroupConfigProperty(
                    auto_scaling_policy=emr_mixins.CfnClusterPropsMixin.AutoScalingPolicyProperty(
                        constraints=emr_mixins.CfnClusterPropsMixin.ScalingConstraintsProperty(
                            max_capacity=123,
                            min_capacity=123
                        ),
                        rules=[emr_mixins.CfnClusterPropsMixin.ScalingRuleProperty(
                            action=emr_mixins.CfnClusterPropsMixin.ScalingActionProperty(
                                market="market",
                                simple_scaling_policy_configuration=emr_mixins.CfnClusterPropsMixin.SimpleScalingPolicyConfigurationProperty(
                                    adjustment_type="adjustmentType",
                                    cool_down=123,
                                    scaling_adjustment=123
                                )
                            ),
                            description="description",
                            name="name",
                            trigger=emr_mixins.CfnClusterPropsMixin.ScalingTriggerProperty(
                                cloud_watch_alarm_definition=emr_mixins.CfnClusterPropsMixin.CloudWatchAlarmDefinitionProperty(
                                    comparison_operator="comparisonOperator",
                                    dimensions=[emr_mixins.CfnClusterPropsMixin.MetricDimensionProperty(
                                        key="key",
                                        value="value"
                                    )],
                                    evaluation_periods=123,
                                    metric_name="metricName",
                                    namespace="namespace",
                                    period=123,
                                    statistic="statistic",
                                    threshold=123,
                                    unit="unit"
                                )
                            )
                        )]
                    ),
                    bid_price="bidPrice",
                    configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                        classification="classification",
                        configuration_properties={
                            "configuration_properties_key": "configurationProperties"
                        },
                        configurations=[configuration_property_]
                    )],
                    custom_ami_id="customAmiId",
                    ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                        ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                            volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                iops=123,
                                size_in_gb=123,
                                throughput=123,
                                volume_type="volumeType"
                            ),
                            volumes_per_instance=123
                        )],
                        ebs_optimized=False
                    ),
                    instance_count=123,
                    instance_type="instanceType",
                    market="market",
                    name="name"
                )],
                termination_protected=False,
                unhealthy_node_replacement=False
            ),
            job_flow_role="jobFlowRole",
            kerberos_attributes=emr_mixins.CfnClusterPropsMixin.KerberosAttributesProperty(
                ad_domain_join_password="adDomainJoinPassword",
                ad_domain_join_user="adDomainJoinUser",
                cross_realm_trust_principal_password="crossRealmTrustPrincipalPassword",
                kdc_admin_password="kdcAdminPassword",
                realm="realm"
            ),
            log_encryption_kms_key_id="logEncryptionKmsKeyId",
            log_uri="logUri",
            managed_scaling_policy=emr_mixins.CfnClusterPropsMixin.ManagedScalingPolicyProperty(
                compute_limits=emr_mixins.CfnClusterPropsMixin.ComputeLimitsProperty(
                    maximum_capacity_units=123,
                    maximum_core_capacity_units=123,
                    maximum_on_demand_capacity_units=123,
                    minimum_capacity_units=123,
                    unit_type="unitType"
                ),
                scaling_strategy="scalingStrategy",
                utilization_performance_index=123
            ),
            name="name",
            os_release_label="osReleaseLabel",
            placement_group_configs=[emr_mixins.CfnClusterPropsMixin.PlacementGroupConfigProperty(
                instance_role="instanceRole",
                placement_strategy="placementStrategy"
            )],
            release_label="releaseLabel",
            scale_down_behavior="scaleDownBehavior",
            security_configuration="securityConfiguration",
            service_role="serviceRole",
            step_concurrency_level=123,
            steps=[emr_mixins.CfnClusterPropsMixin.StepConfigProperty(
                action_on_failure="actionOnFailure",
                hadoop_jar_step=emr_mixins.CfnClusterPropsMixin.HadoopJarStepConfigProperty(
                    args=["args"],
                    jar="jar",
                    main_class="mainClass",
                    step_properties=[emr_mixins.CfnClusterPropsMixin.KeyValueProperty(
                        key="key",
                        value="value"
                    )]
                ),
                name="name"
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            visible_to_all_users=False
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EMR::Cluster``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8be0e3815d56c8d94e32e954f5182272836bd577c1a862227385c407f4c429cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30250d2a222cb04deeadeb41cdb4bb86c5afd046c3678e049c587f83843c3046)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5a6af80959e75ef46f2337b2b13e93d317b68ac58d9a0c93628e5492e61ced7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnClusterMixinProps:
        return typing.cast(CfnClusterMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.ApplicationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_info": "additionalInfo",
            "args": "args",
            "name": "name",
            "version": "version",
        },
    )
    class ApplicationProperty:
        def __init__(
            self,
            *,
            additional_info: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            args: typing.Optional[typing.Sequence[builtins.str]] = None,
            name: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``Application`` is a property of ``AWS::EMR::Cluster`` .

            The ``Application`` property type defines the open-source big data applications for EMR to install and configure when a cluster is created.

            With Amazon EMR release version 4.0 and later, the only accepted parameter is the application ``Name`` . To pass arguments to these applications, you use configuration classifications specified using JSON objects in a ``Configuration`` property. For more information, see `Configuring Applications <https://docs.aws.amazon.com//emr/latest/ReleaseGuide/emr-configure-apps.html>`_ .

            With earlier Amazon EMR releases, the application is any AWS or third-party software that you can add to the cluster. You can specify the version of the application and arguments to pass to it. Amazon EMR accepts and forwards the argument list to the corresponding installation script as a bootstrap action argument.

            :param additional_info: This option is for advanced users only. This is meta information about clusters and applications that are used for testing and troubleshooting.
            :param args: Arguments for Amazon EMR to pass to the application.
            :param name: The name of the application.
            :param version: The version of the application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-application.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                application_property = emr_mixins.CfnClusterPropsMixin.ApplicationProperty(
                    additional_info={
                        "additional_info_key": "additionalInfo"
                    },
                    args=["args"],
                    name="name",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e6b972970d54dc28e719d3571ef5311f50da4a5ca3958705ff06e0d0d6e4544d)
                check_type(argname="argument additional_info", value=additional_info, expected_type=type_hints["additional_info"])
                check_type(argname="argument args", value=args, expected_type=type_hints["args"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if additional_info is not None:
                self._values["additional_info"] = additional_info
            if args is not None:
                self._values["args"] = args
            if name is not None:
                self._values["name"] = name
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def additional_info(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''This option is for advanced users only.

            This is meta information about clusters and applications that are used for testing and troubleshooting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-application.html#cfn-emr-cluster-application-additionalinfo
            '''
            result = self._values.get("additional_info")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def args(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Arguments for Amazon EMR to pass to the application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-application.html#cfn-emr-cluster-application-args
            '''
            result = self._values.get("args")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-application.html#cfn-emr-cluster-application-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The version of the application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-application.html#cfn-emr-cluster-application-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.AutoScalingPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"constraints": "constraints", "rules": "rules"},
    )
    class AutoScalingPolicyProperty:
        def __init__(
            self,
            *,
            constraints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ScalingConstraintsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ScalingRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''``AutoScalingPolicy`` is a subproperty of ``InstanceGroupConfig`` .

            ``AutoScalingPolicy`` defines how an instance group dynamically adds and terminates EC2 instances in response to the value of a CloudWatch metric. For more information, see `Using Automatic Scaling in Amazon EMR <https://docs.aws.amazon.com//emr/latest/ManagementGuide/emr-automatic-scaling.html>`_ in the *Amazon EMR Management Guide* .

            :param constraints: The upper and lower Amazon EC2 instance limits for an automatic scaling policy. Automatic scaling activity will not cause an instance group to grow above or below these limits.
            :param rules: The scale-in and scale-out rules that comprise the automatic scaling policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-autoscalingpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                auto_scaling_policy_property = emr_mixins.CfnClusterPropsMixin.AutoScalingPolicyProperty(
                    constraints=emr_mixins.CfnClusterPropsMixin.ScalingConstraintsProperty(
                        max_capacity=123,
                        min_capacity=123
                    ),
                    rules=[emr_mixins.CfnClusterPropsMixin.ScalingRuleProperty(
                        action=emr_mixins.CfnClusterPropsMixin.ScalingActionProperty(
                            market="market",
                            simple_scaling_policy_configuration=emr_mixins.CfnClusterPropsMixin.SimpleScalingPolicyConfigurationProperty(
                                adjustment_type="adjustmentType",
                                cool_down=123,
                                scaling_adjustment=123
                            )
                        ),
                        description="description",
                        name="name",
                        trigger=emr_mixins.CfnClusterPropsMixin.ScalingTriggerProperty(
                            cloud_watch_alarm_definition=emr_mixins.CfnClusterPropsMixin.CloudWatchAlarmDefinitionProperty(
                                comparison_operator="comparisonOperator",
                                dimensions=[emr_mixins.CfnClusterPropsMixin.MetricDimensionProperty(
                                    key="key",
                                    value="value"
                                )],
                                evaluation_periods=123,
                                metric_name="metricName",
                                namespace="namespace",
                                period=123,
                                statistic="statistic",
                                threshold=123,
                                unit="unit"
                            )
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__90423eee746a6352a1e7b6faa2b7022e2bcb3ce66963ac69bc3d53a6bf45af7a)
                check_type(argname="argument constraints", value=constraints, expected_type=type_hints["constraints"])
                check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if constraints is not None:
                self._values["constraints"] = constraints
            if rules is not None:
                self._values["rules"] = rules

        @builtins.property
        def constraints(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ScalingConstraintsProperty"]]:
            '''The upper and lower Amazon EC2 instance limits for an automatic scaling policy.

            Automatic scaling activity will not cause an instance group to grow above or below these limits.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-autoscalingpolicy.html#cfn-emr-cluster-autoscalingpolicy-constraints
            '''
            result = self._values.get("constraints")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ScalingConstraintsProperty"]], result)

        @builtins.property
        def rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ScalingRuleProperty"]]]]:
            '''The scale-in and scale-out rules that comprise the automatic scaling policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-autoscalingpolicy.html#cfn-emr-cluster-autoscalingpolicy-rules
            '''
            result = self._values.get("rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ScalingRuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoScalingPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.AutoTerminationPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"idle_timeout": "idleTimeout"},
    )
    class AutoTerminationPolicyProperty:
        def __init__(
            self,
            *,
            idle_timeout: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An auto-termination policy for an Amazon EMR cluster.

            An auto-termination policy defines the amount of idle time in seconds after which a cluster automatically terminates. For alternative cluster termination options, see `Control cluster termination <https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-plan-termination.html>`_ .

            :param idle_timeout: Specifies the amount of idle time in seconds after which the cluster automatically terminates. You can specify a minimum of 60 seconds and a maximum of 604800 seconds (seven days).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-autoterminationpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                auto_termination_policy_property = emr_mixins.CfnClusterPropsMixin.AutoTerminationPolicyProperty(
                    idle_timeout=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f3744fc65af35fe1bf1985614d6b914688348f2f698b7bb9bade56ea26c8b433)
                check_type(argname="argument idle_timeout", value=idle_timeout, expected_type=type_hints["idle_timeout"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if idle_timeout is not None:
                self._values["idle_timeout"] = idle_timeout

        @builtins.property
        def idle_timeout(self) -> typing.Optional[jsii.Number]:
            '''Specifies the amount of idle time in seconds after which the cluster automatically terminates.

            You can specify a minimum of 60 seconds and a maximum of 604800 seconds (seven days).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-autoterminationpolicy.html#cfn-emr-cluster-autoterminationpolicy-idletimeout
            '''
            result = self._values.get("idle_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoTerminationPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.BootstrapActionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "script_bootstrap_action": "scriptBootstrapAction",
        },
    )
    class BootstrapActionConfigProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            script_bootstrap_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ScriptBootstrapActionConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''``BootstrapActionConfig`` is a property of ``AWS::EMR::Cluster`` that can be used to run bootstrap actions on EMR clusters.

            You can use a bootstrap action to install software and configure EC2 instances for all cluster nodes before EMR installs and configures open-source big data applications on cluster instances. For more information, see `Create Bootstrap Actions to Install Additional Software <https://docs.aws.amazon.com//emr/latest/ManagementGuide/emr-plan-bootstrap.html>`_ in the *Amazon EMR Management Guide* .

            :param name: The name of the bootstrap action.
            :param script_bootstrap_action: The script run by the bootstrap action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-bootstrapactionconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                bootstrap_action_config_property = emr_mixins.CfnClusterPropsMixin.BootstrapActionConfigProperty(
                    name="name",
                    script_bootstrap_action=emr_mixins.CfnClusterPropsMixin.ScriptBootstrapActionConfigProperty(
                        args=["args"],
                        path="path"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ddbdce83a7051bc19988968c2bfc9cb21364cc336174208be38f020e4aef3b01)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument script_bootstrap_action", value=script_bootstrap_action, expected_type=type_hints["script_bootstrap_action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if script_bootstrap_action is not None:
                self._values["script_bootstrap_action"] = script_bootstrap_action

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the bootstrap action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-bootstrapactionconfig.html#cfn-emr-cluster-bootstrapactionconfig-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def script_bootstrap_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ScriptBootstrapActionConfigProperty"]]:
            '''The script run by the bootstrap action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-bootstrapactionconfig.html#cfn-emr-cluster-bootstrapactionconfig-scriptbootstrapaction
            '''
            result = self._values.get("script_bootstrap_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ScriptBootstrapActionConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BootstrapActionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.CloudWatchAlarmDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "comparison_operator": "comparisonOperator",
            "dimensions": "dimensions",
            "evaluation_periods": "evaluationPeriods",
            "metric_name": "metricName",
            "namespace": "namespace",
            "period": "period",
            "statistic": "statistic",
            "threshold": "threshold",
            "unit": "unit",
        },
    )
    class CloudWatchAlarmDefinitionProperty:
        def __init__(
            self,
            *,
            comparison_operator: typing.Optional[builtins.str] = None,
            dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.MetricDimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            evaluation_periods: typing.Optional[jsii.Number] = None,
            metric_name: typing.Optional[builtins.str] = None,
            namespace: typing.Optional[builtins.str] = None,
            period: typing.Optional[jsii.Number] = None,
            statistic: typing.Optional[builtins.str] = None,
            threshold: typing.Optional[jsii.Number] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``CloudWatchAlarmDefinition`` is a subproperty of the ``ScalingTrigger`` property, which determines when to trigger an automatic scaling activity.

            Scaling activity begins when you satisfy the defined alarm conditions.

            :param comparison_operator: Determines how the metric specified by ``MetricName`` is compared to the value specified by ``Threshold`` .
            :param dimensions: A CloudWatch metric dimension.
            :param evaluation_periods: The number of periods, in five-minute increments, during which the alarm condition must exist before the alarm triggers automatic scaling activity. The default value is ``1`` .
            :param metric_name: The name of the CloudWatch metric that is watched to determine an alarm condition.
            :param namespace: The namespace for the CloudWatch metric. The default is ``AWS/ElasticMapReduce`` .
            :param period: The period, in seconds, over which the statistic is applied. CloudWatch metrics for Amazon EMR are emitted every five minutes (300 seconds), so if you specify a CloudWatch metric, specify ``300`` .
            :param statistic: The statistic to apply to the metric associated with the alarm. The default is ``AVERAGE`` .
            :param threshold: The value against which the specified statistic is compared.
            :param unit: The unit of measure associated with the CloudWatch metric being watched. The value specified for ``Unit`` must correspond to the units specified in the CloudWatch metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-cloudwatchalarmdefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                cloud_watch_alarm_definition_property = emr_mixins.CfnClusterPropsMixin.CloudWatchAlarmDefinitionProperty(
                    comparison_operator="comparisonOperator",
                    dimensions=[emr_mixins.CfnClusterPropsMixin.MetricDimensionProperty(
                        key="key",
                        value="value"
                    )],
                    evaluation_periods=123,
                    metric_name="metricName",
                    namespace="namespace",
                    period=123,
                    statistic="statistic",
                    threshold=123,
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d74e79a40522922435770eef174ae8d6b82d2e0734bfddc665ec7364d3da16e)
                check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
                check_type(argname="argument period", value=period, expected_type=type_hints["period"])
                check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
                check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparison_operator is not None:
                self._values["comparison_operator"] = comparison_operator
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if evaluation_periods is not None:
                self._values["evaluation_periods"] = evaluation_periods
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if namespace is not None:
                self._values["namespace"] = namespace
            if period is not None:
                self._values["period"] = period
            if statistic is not None:
                self._values["statistic"] = statistic
            if threshold is not None:
                self._values["threshold"] = threshold
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def comparison_operator(self) -> typing.Optional[builtins.str]:
            '''Determines how the metric specified by ``MetricName`` is compared to the value specified by ``Threshold`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-cloudwatchalarmdefinition.html#cfn-emr-cluster-cloudwatchalarmdefinition-comparisonoperator
            '''
            result = self._values.get("comparison_operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.MetricDimensionProperty"]]]]:
            '''A CloudWatch metric dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-cloudwatchalarmdefinition.html#cfn-emr-cluster-cloudwatchalarmdefinition-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.MetricDimensionProperty"]]]], result)

        @builtins.property
        def evaluation_periods(self) -> typing.Optional[jsii.Number]:
            '''The number of periods, in five-minute increments, during which the alarm condition must exist before the alarm triggers automatic scaling activity.

            The default value is ``1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-cloudwatchalarmdefinition.html#cfn-emr-cluster-cloudwatchalarmdefinition-evaluationperiods
            '''
            result = self._values.get("evaluation_periods")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''The name of the CloudWatch metric that is watched to determine an alarm condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-cloudwatchalarmdefinition.html#cfn-emr-cluster-cloudwatchalarmdefinition-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The namespace for the CloudWatch metric.

            The default is ``AWS/ElasticMapReduce`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-cloudwatchalarmdefinition.html#cfn-emr-cluster-cloudwatchalarmdefinition-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def period(self) -> typing.Optional[jsii.Number]:
            '''The period, in seconds, over which the statistic is applied.

            CloudWatch metrics for Amazon EMR are emitted every five minutes (300 seconds), so if you specify a CloudWatch metric, specify ``300`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-cloudwatchalarmdefinition.html#cfn-emr-cluster-cloudwatchalarmdefinition-period
            '''
            result = self._values.get("period")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def statistic(self) -> typing.Optional[builtins.str]:
            '''The statistic to apply to the metric associated with the alarm.

            The default is ``AVERAGE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-cloudwatchalarmdefinition.html#cfn-emr-cluster-cloudwatchalarmdefinition-statistic
            '''
            result = self._values.get("statistic")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def threshold(self) -> typing.Optional[jsii.Number]:
            '''The value against which the specified statistic is compared.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-cloudwatchalarmdefinition.html#cfn-emr-cluster-cloudwatchalarmdefinition-threshold
            '''
            result = self._values.get("threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit of measure associated with the CloudWatch metric being watched.

            The value specified for ``Unit`` must correspond to the units specified in the CloudWatch metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-cloudwatchalarmdefinition.html#cfn-emr-cluster-cloudwatchalarmdefinition-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchAlarmDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.ComputeLimitsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "maximum_capacity_units": "maximumCapacityUnits",
            "maximum_core_capacity_units": "maximumCoreCapacityUnits",
            "maximum_on_demand_capacity_units": "maximumOnDemandCapacityUnits",
            "minimum_capacity_units": "minimumCapacityUnits",
            "unit_type": "unitType",
        },
    )
    class ComputeLimitsProperty:
        def __init__(
            self,
            *,
            maximum_capacity_units: typing.Optional[jsii.Number] = None,
            maximum_core_capacity_units: typing.Optional[jsii.Number] = None,
            maximum_on_demand_capacity_units: typing.Optional[jsii.Number] = None,
            minimum_capacity_units: typing.Optional[jsii.Number] = None,
            unit_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Amazon EC2 unit limits for a managed scaling policy.

            The managed scaling activity of a cluster can not be above or below these limits. The limit only applies to the core and task nodes. The master node cannot be scaled after initial configuration.

            :param maximum_capacity_units: The upper boundary of Amazon EC2 units. It is measured through vCPU cores or instances for instance groups and measured through units for instance fleets. Managed scaling activities are not allowed beyond this boundary. The limit only applies to the core and task nodes. The master node cannot be scaled after initial configuration.
            :param maximum_core_capacity_units: The upper boundary of Amazon EC2 units for core node type in a cluster. It is measured through vCPU cores or instances for instance groups and measured through units for instance fleets. The core units are not allowed to scale beyond this boundary. The parameter is used to split capacity allocation between core and task nodes.
            :param maximum_on_demand_capacity_units: The upper boundary of On-Demand Amazon EC2 units. It is measured through vCPU cores or instances for instance groups and measured through units for instance fleets. The On-Demand units are not allowed to scale beyond this boundary. The parameter is used to split capacity allocation between On-Demand and Spot Instances.
            :param minimum_capacity_units: The lower boundary of Amazon EC2 units. It is measured through vCPU cores or instances for instance groups and measured through units for instance fleets. Managed scaling activities are not allowed beyond this boundary. The limit only applies to the core and task nodes. The master node cannot be scaled after initial configuration.
            :param unit_type: The unit type used for specifying a managed scaling policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-computelimits.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                compute_limits_property = emr_mixins.CfnClusterPropsMixin.ComputeLimitsProperty(
                    maximum_capacity_units=123,
                    maximum_core_capacity_units=123,
                    maximum_on_demand_capacity_units=123,
                    minimum_capacity_units=123,
                    unit_type="unitType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c7f419eca790e3fe3daf30619c1eceff7cc7c1d61868a2417872391f835dd01f)
                check_type(argname="argument maximum_capacity_units", value=maximum_capacity_units, expected_type=type_hints["maximum_capacity_units"])
                check_type(argname="argument maximum_core_capacity_units", value=maximum_core_capacity_units, expected_type=type_hints["maximum_core_capacity_units"])
                check_type(argname="argument maximum_on_demand_capacity_units", value=maximum_on_demand_capacity_units, expected_type=type_hints["maximum_on_demand_capacity_units"])
                check_type(argname="argument minimum_capacity_units", value=minimum_capacity_units, expected_type=type_hints["minimum_capacity_units"])
                check_type(argname="argument unit_type", value=unit_type, expected_type=type_hints["unit_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if maximum_capacity_units is not None:
                self._values["maximum_capacity_units"] = maximum_capacity_units
            if maximum_core_capacity_units is not None:
                self._values["maximum_core_capacity_units"] = maximum_core_capacity_units
            if maximum_on_demand_capacity_units is not None:
                self._values["maximum_on_demand_capacity_units"] = maximum_on_demand_capacity_units
            if minimum_capacity_units is not None:
                self._values["minimum_capacity_units"] = minimum_capacity_units
            if unit_type is not None:
                self._values["unit_type"] = unit_type

        @builtins.property
        def maximum_capacity_units(self) -> typing.Optional[jsii.Number]:
            '''The upper boundary of Amazon EC2 units.

            It is measured through vCPU cores or instances for instance groups and measured through units for instance fleets. Managed scaling activities are not allowed beyond this boundary. The limit only applies to the core and task nodes. The master node cannot be scaled after initial configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-computelimits.html#cfn-emr-cluster-computelimits-maximumcapacityunits
            '''
            result = self._values.get("maximum_capacity_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_core_capacity_units(self) -> typing.Optional[jsii.Number]:
            '''The upper boundary of Amazon EC2 units for core node type in a cluster.

            It is measured through vCPU cores or instances for instance groups and measured through units for instance fleets. The core units are not allowed to scale beyond this boundary. The parameter is used to split capacity allocation between core and task nodes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-computelimits.html#cfn-emr-cluster-computelimits-maximumcorecapacityunits
            '''
            result = self._values.get("maximum_core_capacity_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_on_demand_capacity_units(self) -> typing.Optional[jsii.Number]:
            '''The upper boundary of On-Demand Amazon EC2 units.

            It is measured through vCPU cores or instances for instance groups and measured through units for instance fleets. The On-Demand units are not allowed to scale beyond this boundary. The parameter is used to split capacity allocation between On-Demand and Spot Instances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-computelimits.html#cfn-emr-cluster-computelimits-maximumondemandcapacityunits
            '''
            result = self._values.get("maximum_on_demand_capacity_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def minimum_capacity_units(self) -> typing.Optional[jsii.Number]:
            '''The lower boundary of Amazon EC2 units.

            It is measured through vCPU cores or instances for instance groups and measured through units for instance fleets. Managed scaling activities are not allowed beyond this boundary. The limit only applies to the core and task nodes. The master node cannot be scaled after initial configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-computelimits.html#cfn-emr-cluster-computelimits-minimumcapacityunits
            '''
            result = self._values.get("minimum_capacity_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unit_type(self) -> typing.Optional[builtins.str]:
            '''The unit type used for specifying a managed scaling policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-computelimits.html#cfn-emr-cluster-computelimits-unittype
            '''
            result = self._values.get("unit_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComputeLimitsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "classification": "classification",
            "configuration_properties": "configurationProperties",
            "configurations": "configurations",
        },
    )
    class ConfigurationProperty:
        def __init__(
            self,
            *,
            classification: typing.Optional[builtins.str] = None,
            configuration_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''.. epigraph::

   Used only with Amazon EMR release 4.0 and later.

            ``Configuration`` is a subproperty of ``InstanceFleetConfig`` or ``InstanceGroupConfig`` . ``Configuration`` specifies optional configurations for customizing open-source big data applications and environment parameters. A configuration consists of a classification, properties, and optional nested configurations. A classification refers to an application-specific configuration file. Properties are the settings you want to change in that file. For more information, see `Configuring Applications <https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-configure-apps.html>`_ in the *Amazon EMR Release Guide* .

            :param classification: The classification within a configuration.
            :param configuration_properties: A list of additional configurations to apply within a configuration object.
            :param configurations: A list of additional configurations to apply within a configuration object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                # configuration_property_: emr_mixins.CfnClusterPropsMixin.ConfigurationProperty
                
                configuration_property = emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                    classification="classification",
                    configuration_properties={
                        "configuration_properties_key": "configurationProperties"
                    },
                    configurations=[configuration_property_]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__adf72058db79dd58a33c7009dc2e8b680074e3bef0f9ca22e7dbb1ba7eb17388)
                check_type(argname="argument classification", value=classification, expected_type=type_hints["classification"])
                check_type(argname="argument configuration_properties", value=configuration_properties, expected_type=type_hints["configuration_properties"])
                check_type(argname="argument configurations", value=configurations, expected_type=type_hints["configurations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if classification is not None:
                self._values["classification"] = classification
            if configuration_properties is not None:
                self._values["configuration_properties"] = configuration_properties
            if configurations is not None:
                self._values["configurations"] = configurations

        @builtins.property
        def classification(self) -> typing.Optional[builtins.str]:
            '''The classification within a configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-configuration.html#cfn-emr-cluster-configuration-classification
            '''
            result = self._values.get("classification")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def configuration_properties(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''A list of additional configurations to apply within a configuration object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-configuration.html#cfn-emr-cluster-configuration-configurationproperties
            '''
            result = self._values.get("configuration_properties")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ConfigurationProperty"]]]]:
            '''A list of additional configurations to apply within a configuration object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-configuration.html#cfn-emr-cluster-configuration-configurations
            '''
            result = self._values.get("configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ConfigurationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "volume_specification": "volumeSpecification",
            "volumes_per_instance": "volumesPerInstance",
        },
    )
    class EbsBlockDeviceConfigProperty:
        def __init__(
            self,
            *,
            volume_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.VolumeSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            volumes_per_instance: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``EbsBlockDeviceConfig`` is a subproperty of the ``EbsConfiguration`` property type.

            ``EbsBlockDeviceConfig`` defines the number and type of EBS volumes to associate with all EC2 instances in an EMR cluster.

            :param volume_specification: EBS volume specifications such as volume type, IOPS, size (GiB) and throughput (MiB/s) that are requested for the EBS volume attached to an Amazon EC2 instance in the cluster.
            :param volumes_per_instance: Number of EBS volumes with a specific volume configuration that are associated with every instance in the instance group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-ebsblockdeviceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                ebs_block_device_config_property = emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                    volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                        iops=123,
                        size_in_gb=123,
                        throughput=123,
                        volume_type="volumeType"
                    ),
                    volumes_per_instance=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a5b07931a38b8b97d5694e60592e817680e02e9b368c6dd300c2ca100eae108b)
                check_type(argname="argument volume_specification", value=volume_specification, expected_type=type_hints["volume_specification"])
                check_type(argname="argument volumes_per_instance", value=volumes_per_instance, expected_type=type_hints["volumes_per_instance"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if volume_specification is not None:
                self._values["volume_specification"] = volume_specification
            if volumes_per_instance is not None:
                self._values["volumes_per_instance"] = volumes_per_instance

        @builtins.property
        def volume_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.VolumeSpecificationProperty"]]:
            '''EBS volume specifications such as volume type, IOPS, size (GiB) and throughput (MiB/s) that are requested for the EBS volume attached to an Amazon EC2 instance in the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-ebsblockdeviceconfig.html#cfn-emr-cluster-ebsblockdeviceconfig-volumespecification
            '''
            result = self._values.get("volume_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.VolumeSpecificationProperty"]], result)

        @builtins.property
        def volumes_per_instance(self) -> typing.Optional[jsii.Number]:
            '''Number of EBS volumes with a specific volume configuration that are associated with every instance in the instance group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-ebsblockdeviceconfig.html#cfn-emr-cluster-ebsblockdeviceconfig-volumesperinstance
            '''
            result = self._values.get("volumes_per_instance")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EbsBlockDeviceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.EbsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ebs_block_device_configs": "ebsBlockDeviceConfigs",
            "ebs_optimized": "ebsOptimized",
        },
    )
    class EbsConfigurationProperty:
        def __init__(
            self,
            *,
            ebs_block_device_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.EbsBlockDeviceConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ebs_optimized: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''``EbsConfiguration`` is a subproperty of ``InstanceFleetConfig`` or ``InstanceGroupConfig`` .

            ``EbsConfiguration`` determines the EBS volumes to attach to EMR cluster instances.

            :param ebs_block_device_configs: An array of Amazon EBS volume specifications attached to a cluster instance.
            :param ebs_optimized: Indicates whether an Amazon EBS volume is EBS-optimized. The default is false. You should explicitly set this value to true to enable the Amazon EBS-optimized setting for an EC2 instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-ebsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                ebs_configuration_property = emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                    ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                        volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                            iops=123,
                            size_in_gb=123,
                            throughput=123,
                            volume_type="volumeType"
                        ),
                        volumes_per_instance=123
                    )],
                    ebs_optimized=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b2a429a617d970c3ca67459990b41d71da688cb2425955ab43d0c8373e73f73)
                check_type(argname="argument ebs_block_device_configs", value=ebs_block_device_configs, expected_type=type_hints["ebs_block_device_configs"])
                check_type(argname="argument ebs_optimized", value=ebs_optimized, expected_type=type_hints["ebs_optimized"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ebs_block_device_configs is not None:
                self._values["ebs_block_device_configs"] = ebs_block_device_configs
            if ebs_optimized is not None:
                self._values["ebs_optimized"] = ebs_optimized

        @builtins.property
        def ebs_block_device_configs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.EbsBlockDeviceConfigProperty"]]]]:
            '''An array of Amazon EBS volume specifications attached to a cluster instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-ebsconfiguration.html#cfn-emr-cluster-ebsconfiguration-ebsblockdeviceconfigs
            '''
            result = self._values.get("ebs_block_device_configs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.EbsBlockDeviceConfigProperty"]]]], result)

        @builtins.property
        def ebs_optimized(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether an Amazon EBS volume is EBS-optimized.

            The default is false. You should explicitly set this value to true to enable the Amazon EBS-optimized setting for an EC2 instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-ebsconfiguration.html#cfn-emr-cluster-ebsconfiguration-ebsoptimized
            '''
            result = self._values.get("ebs_optimized")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EbsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.HadoopJarStepConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "args": "args",
            "jar": "jar",
            "main_class": "mainClass",
            "step_properties": "stepProperties",
        },
    )
    class HadoopJarStepConfigProperty:
        def __init__(
            self,
            *,
            args: typing.Optional[typing.Sequence[builtins.str]] = None,
            jar: typing.Optional[builtins.str] = None,
            main_class: typing.Optional[builtins.str] = None,
            step_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.KeyValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``HadoopJarStepConfig`` property type specifies a job flow step consisting of a JAR file whose main function will be executed.

            The main function submits a job for the cluster to execute as a step on the master node, and then waits for the job to finish or fail before executing subsequent steps.

            :param args: A list of command line arguments passed to the JAR file's main function when executed.
            :param jar: A path to a JAR file run during the step.
            :param main_class: The name of the main class in the specified Java file. If not specified, the JAR file should specify a Main-Class in its manifest file.
            :param step_properties: A list of Java properties that are set when the step runs. You can use these properties to pass key-value pairs to your main function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-hadoopjarstepconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                hadoop_jar_step_config_property = emr_mixins.CfnClusterPropsMixin.HadoopJarStepConfigProperty(
                    args=["args"],
                    jar="jar",
                    main_class="mainClass",
                    step_properties=[emr_mixins.CfnClusterPropsMixin.KeyValueProperty(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4fc366d15f8089d695d4625a1ba2c2e0ed8e08311dbb1e86b6cfd548166f42d6)
                check_type(argname="argument args", value=args, expected_type=type_hints["args"])
                check_type(argname="argument jar", value=jar, expected_type=type_hints["jar"])
                check_type(argname="argument main_class", value=main_class, expected_type=type_hints["main_class"])
                check_type(argname="argument step_properties", value=step_properties, expected_type=type_hints["step_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if args is not None:
                self._values["args"] = args
            if jar is not None:
                self._values["jar"] = jar
            if main_class is not None:
                self._values["main_class"] = main_class
            if step_properties is not None:
                self._values["step_properties"] = step_properties

        @builtins.property
        def args(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of command line arguments passed to the JAR file's main function when executed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-hadoopjarstepconfig.html#cfn-emr-cluster-hadoopjarstepconfig-args
            '''
            result = self._values.get("args")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def jar(self) -> typing.Optional[builtins.str]:
            '''A path to a JAR file run during the step.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-hadoopjarstepconfig.html#cfn-emr-cluster-hadoopjarstepconfig-jar
            '''
            result = self._values.get("jar")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def main_class(self) -> typing.Optional[builtins.str]:
            '''The name of the main class in the specified Java file.

            If not specified, the JAR file should specify a Main-Class in its manifest file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-hadoopjarstepconfig.html#cfn-emr-cluster-hadoopjarstepconfig-mainclass
            '''
            result = self._values.get("main_class")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def step_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.KeyValueProperty"]]]]:
            '''A list of Java properties that are set when the step runs.

            You can use these properties to pass key-value pairs to your main function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-hadoopjarstepconfig.html#cfn-emr-cluster-hadoopjarstepconfig-stepproperties
            '''
            result = self._values.get("step_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.KeyValueProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HadoopJarStepConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.InstanceFleetConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instance_type_configs": "instanceTypeConfigs",
            "launch_specifications": "launchSpecifications",
            "name": "name",
            "resize_specifications": "resizeSpecifications",
            "target_on_demand_capacity": "targetOnDemandCapacity",
            "target_spot_capacity": "targetSpotCapacity",
        },
    )
    class InstanceFleetConfigProperty:
        def __init__(
            self,
            *,
            instance_type_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.InstanceTypeConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            launch_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.InstanceFleetProvisioningSpecificationsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
            resize_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.InstanceFleetResizingSpecificationsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            target_on_demand_capacity: typing.Optional[jsii.Number] = None,
            target_spot_capacity: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Use ``InstanceFleetConfig`` to define instance fleets for an EMR cluster.

            A cluster can not use both instance fleets and instance groups. For more information, see `Configure Instance Fleets <https://docs.aws.amazon.com//emr/latest/ManagementGuide/emr-instance-group-configuration.html>`_ in the *Amazon EMR Management Guide* .
            .. epigraph::

               The instance fleet configuration is available only in Amazon EMR versions 4.8.0 and later, excluding 5.0.x versions.

            :param instance_type_configs: The instance type configurations that define the Amazon EC2 instances in the instance fleet.
            :param launch_specifications: The launch specification for the instance fleet.
            :param name: The friendly name of the instance fleet.
            :param resize_specifications: The resize specification for the instance fleet.
            :param target_on_demand_capacity: The target capacity of On-Demand units for the instance fleet, which determines how many On-Demand instances to provision. When the instance fleet launches, Amazon EMR tries to provision On-Demand instances as specified by ``InstanceTypeConfig`` . Each instance configuration has a specified ``WeightedCapacity`` . When an On-Demand instance is provisioned, the ``WeightedCapacity`` units count toward the target capacity. Amazon EMR provisions instances until the target capacity is totally fulfilled, even if this results in an overage. For example, if there are 2 units remaining to fulfill capacity, and Amazon EMR can only provision an instance with a ``WeightedCapacity`` of 5 units, the instance is provisioned, and the target capacity is exceeded by 3 units. .. epigraph:: If not specified or set to 0, only Spot instances are provisioned for the instance fleet using ``TargetSpotCapacity`` . At least one of ``TargetSpotCapacity`` and ``TargetOnDemandCapacity`` should be greater than 0. For a master instance fleet, only one of ``TargetSpotCapacity`` and ``TargetOnDemandCapacity`` can be specified, and its value must be 1.
            :param target_spot_capacity: The target capacity of Spot units for the instance fleet, which determines how many Spot instances to provision. When the instance fleet launches, Amazon EMR tries to provision Spot instances as specified by ``InstanceTypeConfig`` . Each instance configuration has a specified ``WeightedCapacity`` . When a Spot instance is provisioned, the ``WeightedCapacity`` units count toward the target capacity. Amazon EMR provisions instances until the target capacity is totally fulfilled, even if this results in an overage. For example, if there are 2 units remaining to fulfill capacity, and Amazon EMR can only provision an instance with a ``WeightedCapacity`` of 5 units, the instance is provisioned, and the target capacity is exceeded by 3 units. .. epigraph:: If not specified or set to 0, only On-Demand instances are provisioned for the instance fleet. At least one of ``TargetSpotCapacity`` and ``TargetOnDemandCapacity`` should be greater than 0. For a master instance fleet, only one of ``TargetSpotCapacity`` and ``TargetOnDemandCapacity`` can be specified, and its value must be 1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancefleetconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                # configuration_property_: emr_mixins.CfnClusterPropsMixin.ConfigurationProperty
                
                instance_fleet_config_property = emr_mixins.CfnClusterPropsMixin.InstanceFleetConfigProperty(
                    instance_type_configs=[emr_mixins.CfnClusterPropsMixin.InstanceTypeConfigProperty(
                        bid_price="bidPrice",
                        bid_price_as_percentage_of_on_demand_price=123,
                        configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                            classification="classification",
                            configuration_properties={
                                "configuration_properties_key": "configurationProperties"
                            },
                            configurations=[configuration_property_]
                        )],
                        custom_ami_id="customAmiId",
                        ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                            ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                                volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                    iops=123,
                                    size_in_gb=123,
                                    throughput=123,
                                    volume_type="volumeType"
                                ),
                                volumes_per_instance=123
                            )],
                            ebs_optimized=False
                        ),
                        instance_type="instanceType",
                        priority=123,
                        weighted_capacity=123
                    )],
                    launch_specifications=emr_mixins.CfnClusterPropsMixin.InstanceFleetProvisioningSpecificationsProperty(
                        on_demand_specification=emr_mixins.CfnClusterPropsMixin.OnDemandProvisioningSpecificationProperty(
                            allocation_strategy="allocationStrategy",
                            capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                                capacity_reservation_preference="capacityReservationPreference",
                                capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                                usage_strategy="usageStrategy"
                            )
                        ),
                        spot_specification=emr_mixins.CfnClusterPropsMixin.SpotProvisioningSpecificationProperty(
                            allocation_strategy="allocationStrategy",
                            block_duration_minutes=123,
                            timeout_action="timeoutAction",
                            timeout_duration_minutes=123
                        )
                    ),
                    name="name",
                    resize_specifications=emr_mixins.CfnClusterPropsMixin.InstanceFleetResizingSpecificationsProperty(
                        on_demand_resize_specification=emr_mixins.CfnClusterPropsMixin.OnDemandResizingSpecificationProperty(
                            allocation_strategy="allocationStrategy",
                            capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                                capacity_reservation_preference="capacityReservationPreference",
                                capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                                usage_strategy="usageStrategy"
                            ),
                            timeout_duration_minutes=123
                        ),
                        spot_resize_specification=emr_mixins.CfnClusterPropsMixin.SpotResizingSpecificationProperty(
                            allocation_strategy="allocationStrategy",
                            timeout_duration_minutes=123
                        )
                    ),
                    target_on_demand_capacity=123,
                    target_spot_capacity=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e32126c64841a5f2e79ff4c4abb5516688e8cc7bd9c99850d4a2c4edcc9ca242)
                check_type(argname="argument instance_type_configs", value=instance_type_configs, expected_type=type_hints["instance_type_configs"])
                check_type(argname="argument launch_specifications", value=launch_specifications, expected_type=type_hints["launch_specifications"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument resize_specifications", value=resize_specifications, expected_type=type_hints["resize_specifications"])
                check_type(argname="argument target_on_demand_capacity", value=target_on_demand_capacity, expected_type=type_hints["target_on_demand_capacity"])
                check_type(argname="argument target_spot_capacity", value=target_spot_capacity, expected_type=type_hints["target_spot_capacity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_type_configs is not None:
                self._values["instance_type_configs"] = instance_type_configs
            if launch_specifications is not None:
                self._values["launch_specifications"] = launch_specifications
            if name is not None:
                self._values["name"] = name
            if resize_specifications is not None:
                self._values["resize_specifications"] = resize_specifications
            if target_on_demand_capacity is not None:
                self._values["target_on_demand_capacity"] = target_on_demand_capacity
            if target_spot_capacity is not None:
                self._values["target_spot_capacity"] = target_spot_capacity

        @builtins.property
        def instance_type_configs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.InstanceTypeConfigProperty"]]]]:
            '''The instance type configurations that define the Amazon EC2 instances in the instance fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancefleetconfig.html#cfn-emr-cluster-instancefleetconfig-instancetypeconfigs
            '''
            result = self._values.get("instance_type_configs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.InstanceTypeConfigProperty"]]]], result)

        @builtins.property
        def launch_specifications(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.InstanceFleetProvisioningSpecificationsProperty"]]:
            '''The launch specification for the instance fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancefleetconfig.html#cfn-emr-cluster-instancefleetconfig-launchspecifications
            '''
            result = self._values.get("launch_specifications")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.InstanceFleetProvisioningSpecificationsProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The friendly name of the instance fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancefleetconfig.html#cfn-emr-cluster-instancefleetconfig-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resize_specifications(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.InstanceFleetResizingSpecificationsProperty"]]:
            '''The resize specification for the instance fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancefleetconfig.html#cfn-emr-cluster-instancefleetconfig-resizespecifications
            '''
            result = self._values.get("resize_specifications")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.InstanceFleetResizingSpecificationsProperty"]], result)

        @builtins.property
        def target_on_demand_capacity(self) -> typing.Optional[jsii.Number]:
            '''The target capacity of On-Demand units for the instance fleet, which determines how many On-Demand instances to provision.

            When the instance fleet launches, Amazon EMR tries to provision On-Demand instances as specified by ``InstanceTypeConfig`` . Each instance configuration has a specified ``WeightedCapacity`` . When an On-Demand instance is provisioned, the ``WeightedCapacity`` units count toward the target capacity. Amazon EMR provisions instances until the target capacity is totally fulfilled, even if this results in an overage. For example, if there are 2 units remaining to fulfill capacity, and Amazon EMR can only provision an instance with a ``WeightedCapacity`` of 5 units, the instance is provisioned, and the target capacity is exceeded by 3 units.
            .. epigraph::

               If not specified or set to 0, only Spot instances are provisioned for the instance fleet using ``TargetSpotCapacity`` . At least one of ``TargetSpotCapacity`` and ``TargetOnDemandCapacity`` should be greater than 0. For a master instance fleet, only one of ``TargetSpotCapacity`` and ``TargetOnDemandCapacity`` can be specified, and its value must be 1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancefleetconfig.html#cfn-emr-cluster-instancefleetconfig-targetondemandcapacity
            '''
            result = self._values.get("target_on_demand_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def target_spot_capacity(self) -> typing.Optional[jsii.Number]:
            '''The target capacity of Spot units for the instance fleet, which determines how many Spot instances to provision.

            When the instance fleet launches, Amazon EMR tries to provision Spot instances as specified by ``InstanceTypeConfig`` . Each instance configuration has a specified ``WeightedCapacity`` . When a Spot instance is provisioned, the ``WeightedCapacity`` units count toward the target capacity. Amazon EMR provisions instances until the target capacity is totally fulfilled, even if this results in an overage. For example, if there are 2 units remaining to fulfill capacity, and Amazon EMR can only provision an instance with a ``WeightedCapacity`` of 5 units, the instance is provisioned, and the target capacity is exceeded by 3 units.
            .. epigraph::

               If not specified or set to 0, only On-Demand instances are provisioned for the instance fleet. At least one of ``TargetSpotCapacity`` and ``TargetOnDemandCapacity`` should be greater than 0. For a master instance fleet, only one of ``TargetSpotCapacity`` and ``TargetOnDemandCapacity`` can be specified, and its value must be 1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancefleetconfig.html#cfn-emr-cluster-instancefleetconfig-targetspotcapacity
            '''
            result = self._values.get("target_spot_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceFleetConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.InstanceFleetProvisioningSpecificationsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "on_demand_specification": "onDemandSpecification",
            "spot_specification": "spotSpecification",
        },
    )
    class InstanceFleetProvisioningSpecificationsProperty:
        def __init__(
            self,
            *,
            on_demand_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.OnDemandProvisioningSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            spot_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.SpotProvisioningSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''``InstanceFleetProvisioningSpecification`` is a subproperty of ``InstanceFleetConfig`` .

            ``InstanceFleetProvisioningSpecification`` defines the launch specification for Spot instances in an instance fleet, which determines the defined duration and provisioning timeout behavior for Spot instances.
            .. epigraph::

               The instance fleet configuration is available only in Amazon EMR versions 4.8.0 and later, excluding 5.0.x versions.

            :param on_demand_specification: The launch specification for On-Demand Instances in the instance fleet, which determines the allocation strategy and capacity reservation options. .. epigraph:: The instance fleet configuration is available only in Amazon EMR releases 4.8.0 and later, excluding 5.0.x versions. On-Demand Instances allocation strategy is available in Amazon EMR releases 5.12.1 and later.
            :param spot_specification: The launch specification for Spot instances in the fleet, which determines the allocation strategy, defined duration, and provisioning timeout behavior.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancefleetprovisioningspecifications.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                instance_fleet_provisioning_specifications_property = emr_mixins.CfnClusterPropsMixin.InstanceFleetProvisioningSpecificationsProperty(
                    on_demand_specification=emr_mixins.CfnClusterPropsMixin.OnDemandProvisioningSpecificationProperty(
                        allocation_strategy="allocationStrategy",
                        capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                            capacity_reservation_preference="capacityReservationPreference",
                            capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                            usage_strategy="usageStrategy"
                        )
                    ),
                    spot_specification=emr_mixins.CfnClusterPropsMixin.SpotProvisioningSpecificationProperty(
                        allocation_strategy="allocationStrategy",
                        block_duration_minutes=123,
                        timeout_action="timeoutAction",
                        timeout_duration_minutes=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d7b22e3487ab445732197a935e1de936dd2775195cfb50e42304a742efb207cf)
                check_type(argname="argument on_demand_specification", value=on_demand_specification, expected_type=type_hints["on_demand_specification"])
                check_type(argname="argument spot_specification", value=spot_specification, expected_type=type_hints["spot_specification"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if on_demand_specification is not None:
                self._values["on_demand_specification"] = on_demand_specification
            if spot_specification is not None:
                self._values["spot_specification"] = spot_specification

        @builtins.property
        def on_demand_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.OnDemandProvisioningSpecificationProperty"]]:
            '''The launch specification for On-Demand Instances in the instance fleet, which determines the allocation strategy and capacity reservation options.

            .. epigraph::

               The instance fleet configuration is available only in Amazon EMR releases 4.8.0 and later, excluding 5.0.x versions. On-Demand Instances allocation strategy is available in Amazon EMR releases 5.12.1 and later.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancefleetprovisioningspecifications.html#cfn-emr-cluster-instancefleetprovisioningspecifications-ondemandspecification
            '''
            result = self._values.get("on_demand_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.OnDemandProvisioningSpecificationProperty"]], result)

        @builtins.property
        def spot_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.SpotProvisioningSpecificationProperty"]]:
            '''The launch specification for Spot instances in the fleet, which determines the allocation strategy, defined duration, and provisioning timeout behavior.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancefleetprovisioningspecifications.html#cfn-emr-cluster-instancefleetprovisioningspecifications-spotspecification
            '''
            result = self._values.get("spot_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.SpotProvisioningSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceFleetProvisioningSpecificationsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.InstanceFleetResizingSpecificationsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "on_demand_resize_specification": "onDemandResizeSpecification",
            "spot_resize_specification": "spotResizeSpecification",
        },
    )
    class InstanceFleetResizingSpecificationsProperty:
        def __init__(
            self,
            *,
            on_demand_resize_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.OnDemandResizingSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            spot_resize_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.SpotResizingSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The resize specification for On-Demand and Spot Instances in the fleet.

            :param on_demand_resize_specification: The resize specification for On-Demand Instances in the instance fleet, which contains the allocation strategy, capacity reservation options, and the resize timeout period.
            :param spot_resize_specification: The resize specification for Spot Instances in the instance fleet, which contains the allocation strategy and the resize timeout period.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancefleetresizingspecifications.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                instance_fleet_resizing_specifications_property = emr_mixins.CfnClusterPropsMixin.InstanceFleetResizingSpecificationsProperty(
                    on_demand_resize_specification=emr_mixins.CfnClusterPropsMixin.OnDemandResizingSpecificationProperty(
                        allocation_strategy="allocationStrategy",
                        capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                            capacity_reservation_preference="capacityReservationPreference",
                            capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                            usage_strategy="usageStrategy"
                        ),
                        timeout_duration_minutes=123
                    ),
                    spot_resize_specification=emr_mixins.CfnClusterPropsMixin.SpotResizingSpecificationProperty(
                        allocation_strategy="allocationStrategy",
                        timeout_duration_minutes=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__efa44fe8693d380822026d857053af5c73c799c2c788531957b52f4230a95f09)
                check_type(argname="argument on_demand_resize_specification", value=on_demand_resize_specification, expected_type=type_hints["on_demand_resize_specification"])
                check_type(argname="argument spot_resize_specification", value=spot_resize_specification, expected_type=type_hints["spot_resize_specification"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if on_demand_resize_specification is not None:
                self._values["on_demand_resize_specification"] = on_demand_resize_specification
            if spot_resize_specification is not None:
                self._values["spot_resize_specification"] = spot_resize_specification

        @builtins.property
        def on_demand_resize_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.OnDemandResizingSpecificationProperty"]]:
            '''The resize specification for On-Demand Instances in the instance fleet, which contains the allocation strategy, capacity reservation options, and the resize timeout period.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancefleetresizingspecifications.html#cfn-emr-cluster-instancefleetresizingspecifications-ondemandresizespecification
            '''
            result = self._values.get("on_demand_resize_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.OnDemandResizingSpecificationProperty"]], result)

        @builtins.property
        def spot_resize_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.SpotResizingSpecificationProperty"]]:
            '''The resize specification for Spot Instances in the instance fleet, which contains the allocation strategy and the resize timeout period.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancefleetresizingspecifications.html#cfn-emr-cluster-instancefleetresizingspecifications-spotresizespecification
            '''
            result = self._values.get("spot_resize_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.SpotResizingSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceFleetResizingSpecificationsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.InstanceGroupConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_scaling_policy": "autoScalingPolicy",
            "bid_price": "bidPrice",
            "configurations": "configurations",
            "custom_ami_id": "customAmiId",
            "ebs_configuration": "ebsConfiguration",
            "instance_count": "instanceCount",
            "instance_type": "instanceType",
            "market": "market",
            "name": "name",
        },
    )
    class InstanceGroupConfigProperty:
        def __init__(
            self,
            *,
            auto_scaling_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.AutoScalingPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            bid_price: typing.Optional[builtins.str] = None,
            configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            custom_ami_id: typing.Optional[builtins.str] = None,
            ebs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.EbsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            instance_count: typing.Optional[jsii.Number] = None,
            instance_type: typing.Optional[builtins.str] = None,
            market: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use ``InstanceGroupConfig`` to define instance groups for an EMR cluster.

            A cluster can not use both instance groups and instance fleets. For more information, see `Create a Cluster with Instance Fleets or Uniform Instance Groups <https://docs.aws.amazon.com//emr/latest/ManagementGuide/emr-instance-group-configuration.html>`_ in the *Amazon EMR Management Guide* .

            :param auto_scaling_policy: ``AutoScalingPolicy`` is a subproperty of the `InstanceGroupConfig <https://docs.aws.amazon.com//AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig-instancegroupconfig.html>`_ property type that specifies the constraints and rules of an automatic scaling policy in Amazon EMR . The automatic scaling policy defines how an instance group dynamically adds and terminates EC2 instances in response to the value of a CloudWatch metric. Only core and task instance groups can use automatic scaling policies. For more information, see `Using Automatic Scaling in Amazon EMR <https://docs.aws.amazon.com//emr/latest/ManagementGuide/emr-automatic-scaling.html>`_ .
            :param bid_price: If specified, indicates that the instance group uses Spot Instances. This is the maximum price you are willing to pay for Spot Instances. Specify ``OnDemandPrice`` to set the amount equal to the On-Demand price, or specify an amount in USD.
            :param configurations: .. epigraph:: Amazon EMR releases 4.x or later. The list of configurations supplied for an Amazon EMR cluster instance group. You can specify a separate configuration for each instance group (master, core, and task).
            :param custom_ami_id: The custom AMI ID to use for the provisioned instance group.
            :param ebs_configuration: EBS configurations that will be attached to each Amazon EC2 instance in the instance group.
            :param instance_count: Target number of instances for the instance group.
            :param instance_type: The Amazon EC2 instance type for all instances in the instance group.
            :param market: Market type of the Amazon EC2 instances used to create a cluster node.
            :param name: Friendly name given to the instance group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancegroupconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                # configuration_property_: emr_mixins.CfnClusterPropsMixin.ConfigurationProperty
                
                instance_group_config_property = emr_mixins.CfnClusterPropsMixin.InstanceGroupConfigProperty(
                    auto_scaling_policy=emr_mixins.CfnClusterPropsMixin.AutoScalingPolicyProperty(
                        constraints=emr_mixins.CfnClusterPropsMixin.ScalingConstraintsProperty(
                            max_capacity=123,
                            min_capacity=123
                        ),
                        rules=[emr_mixins.CfnClusterPropsMixin.ScalingRuleProperty(
                            action=emr_mixins.CfnClusterPropsMixin.ScalingActionProperty(
                                market="market",
                                simple_scaling_policy_configuration=emr_mixins.CfnClusterPropsMixin.SimpleScalingPolicyConfigurationProperty(
                                    adjustment_type="adjustmentType",
                                    cool_down=123,
                                    scaling_adjustment=123
                                )
                            ),
                            description="description",
                            name="name",
                            trigger=emr_mixins.CfnClusterPropsMixin.ScalingTriggerProperty(
                                cloud_watch_alarm_definition=emr_mixins.CfnClusterPropsMixin.CloudWatchAlarmDefinitionProperty(
                                    comparison_operator="comparisonOperator",
                                    dimensions=[emr_mixins.CfnClusterPropsMixin.MetricDimensionProperty(
                                        key="key",
                                        value="value"
                                    )],
                                    evaluation_periods=123,
                                    metric_name="metricName",
                                    namespace="namespace",
                                    period=123,
                                    statistic="statistic",
                                    threshold=123,
                                    unit="unit"
                                )
                            )
                        )]
                    ),
                    bid_price="bidPrice",
                    configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                        classification="classification",
                        configuration_properties={
                            "configuration_properties_key": "configurationProperties"
                        },
                        configurations=[configuration_property_]
                    )],
                    custom_ami_id="customAmiId",
                    ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                        ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                            volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                iops=123,
                                size_in_gb=123,
                                throughput=123,
                                volume_type="volumeType"
                            ),
                            volumes_per_instance=123
                        )],
                        ebs_optimized=False
                    ),
                    instance_count=123,
                    instance_type="instanceType",
                    market="market",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f53e704834a5666e3a90e9b39ed367c5bc0f9e0b3e6ce7050f8de57a113138ce)
                check_type(argname="argument auto_scaling_policy", value=auto_scaling_policy, expected_type=type_hints["auto_scaling_policy"])
                check_type(argname="argument bid_price", value=bid_price, expected_type=type_hints["bid_price"])
                check_type(argname="argument configurations", value=configurations, expected_type=type_hints["configurations"])
                check_type(argname="argument custom_ami_id", value=custom_ami_id, expected_type=type_hints["custom_ami_id"])
                check_type(argname="argument ebs_configuration", value=ebs_configuration, expected_type=type_hints["ebs_configuration"])
                check_type(argname="argument instance_count", value=instance_count, expected_type=type_hints["instance_count"])
                check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                check_type(argname="argument market", value=market, expected_type=type_hints["market"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_scaling_policy is not None:
                self._values["auto_scaling_policy"] = auto_scaling_policy
            if bid_price is not None:
                self._values["bid_price"] = bid_price
            if configurations is not None:
                self._values["configurations"] = configurations
            if custom_ami_id is not None:
                self._values["custom_ami_id"] = custom_ami_id
            if ebs_configuration is not None:
                self._values["ebs_configuration"] = ebs_configuration
            if instance_count is not None:
                self._values["instance_count"] = instance_count
            if instance_type is not None:
                self._values["instance_type"] = instance_type
            if market is not None:
                self._values["market"] = market
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def auto_scaling_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.AutoScalingPolicyProperty"]]:
            '''``AutoScalingPolicy`` is a subproperty of the `InstanceGroupConfig <https://docs.aws.amazon.com//AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig-instancegroupconfig.html>`_ property type that specifies the constraints and rules of an automatic scaling policy in Amazon EMR . The automatic scaling policy defines how an instance group dynamically adds and terminates EC2 instances in response to the value of a CloudWatch metric. Only core and task instance groups can use automatic scaling policies. For more information, see `Using Automatic Scaling in Amazon EMR <https://docs.aws.amazon.com//emr/latest/ManagementGuide/emr-automatic-scaling.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancegroupconfig.html#cfn-emr-cluster-instancegroupconfig-autoscalingpolicy
            '''
            result = self._values.get("auto_scaling_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.AutoScalingPolicyProperty"]], result)

        @builtins.property
        def bid_price(self) -> typing.Optional[builtins.str]:
            '''If specified, indicates that the instance group uses Spot Instances.

            This is the maximum price you are willing to pay for Spot Instances. Specify ``OnDemandPrice`` to set the amount equal to the On-Demand price, or specify an amount in USD.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancegroupconfig.html#cfn-emr-cluster-instancegroupconfig-bidprice
            '''
            result = self._values.get("bid_price")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ConfigurationProperty"]]]]:
            '''.. epigraph::

   Amazon EMR releases 4.x or later.

            The list of configurations supplied for an Amazon EMR cluster instance group. You can specify a separate configuration for each instance group (master, core, and task).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancegroupconfig.html#cfn-emr-cluster-instancegroupconfig-configurations
            '''
            result = self._values.get("configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ConfigurationProperty"]]]], result)

        @builtins.property
        def custom_ami_id(self) -> typing.Optional[builtins.str]:
            '''The custom AMI ID to use for the provisioned instance group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancegroupconfig.html#cfn-emr-cluster-instancegroupconfig-customamiid
            '''
            result = self._values.get("custom_ami_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ebs_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.EbsConfigurationProperty"]]:
            '''EBS configurations that will be attached to each Amazon EC2 instance in the instance group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancegroupconfig.html#cfn-emr-cluster-instancegroupconfig-ebsconfiguration
            '''
            result = self._values.get("ebs_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.EbsConfigurationProperty"]], result)

        @builtins.property
        def instance_count(self) -> typing.Optional[jsii.Number]:
            '''Target number of instances for the instance group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancegroupconfig.html#cfn-emr-cluster-instancegroupconfig-instancecount
            '''
            result = self._values.get("instance_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            '''The Amazon EC2 instance type for all instances in the instance group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancegroupconfig.html#cfn-emr-cluster-instancegroupconfig-instancetype
            '''
            result = self._values.get("instance_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def market(self) -> typing.Optional[builtins.str]:
            '''Market type of the Amazon EC2 instances used to create a cluster node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancegroupconfig.html#cfn-emr-cluster-instancegroupconfig-market
            '''
            result = self._values.get("market")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Friendly name given to the instance group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancegroupconfig.html#cfn-emr-cluster-instancegroupconfig-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceGroupConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.InstanceTypeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bid_price": "bidPrice",
            "bid_price_as_percentage_of_on_demand_price": "bidPriceAsPercentageOfOnDemandPrice",
            "configurations": "configurations",
            "custom_ami_id": "customAmiId",
            "ebs_configuration": "ebsConfiguration",
            "instance_type": "instanceType",
            "priority": "priority",
            "weighted_capacity": "weightedCapacity",
        },
    )
    class InstanceTypeConfigProperty:
        def __init__(
            self,
            *,
            bid_price: typing.Optional[builtins.str] = None,
            bid_price_as_percentage_of_on_demand_price: typing.Optional[jsii.Number] = None,
            configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            custom_ami_id: typing.Optional[builtins.str] = None,
            ebs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.EbsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            instance_type: typing.Optional[builtins.str] = None,
            priority: typing.Optional[jsii.Number] = None,
            weighted_capacity: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''.. epigraph::

   The instance fleet configuration is available only in Amazon EMR versions 4.8.0 and later, excluding 5.0.x versions.

            ``InstanceTypeConfig`` is a sub-property of ``InstanceFleetConfig`` . ``InstanceTypeConfig`` determines the EC2 instances that Amazon EMR attempts to provision to fulfill On-Demand and Spot target capacities.

            :param bid_price: The bid price for each Amazon EC2 Spot Instance type as defined by ``InstanceType`` . Expressed in USD. If neither ``BidPrice`` nor ``BidPriceAsPercentageOfOnDemandPrice`` is provided, ``BidPriceAsPercentageOfOnDemandPrice`` defaults to 100%.
            :param bid_price_as_percentage_of_on_demand_price: The bid price, as a percentage of On-Demand price, for each Amazon EC2 Spot Instance as defined by ``InstanceType`` . Expressed as a number (for example, 20 specifies 20%). If neither ``BidPrice`` nor ``BidPriceAsPercentageOfOnDemandPrice`` is provided, ``BidPriceAsPercentageOfOnDemandPrice`` defaults to 100%.
            :param configurations: A configuration classification that applies when provisioning cluster instances, which can include configurations for applications and software that run on the cluster.
            :param custom_ami_id: The custom AMI ID to use for the instance type.
            :param ebs_configuration: The configuration of Amazon Elastic Block Store (Amazon EBS) attached to each instance as defined by ``InstanceType`` .
            :param instance_type: An Amazon EC2 instance type, such as ``m3.xlarge`` .
            :param priority: The priority at which Amazon EMR launches the Amazon EC2 instances with this instance type. Priority starts at 0, which is the highest priority. Amazon EMR considers the highest priority first.
            :param weighted_capacity: The number of units that a provisioned instance of this type provides toward fulfilling the target capacities defined in ``InstanceFleetConfig`` . This value is 1 for a master instance fleet, and must be 1 or greater for core and task instance fleets. Defaults to 1 if not specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancetypeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                # configuration_property_: emr_mixins.CfnClusterPropsMixin.ConfigurationProperty
                
                instance_type_config_property = emr_mixins.CfnClusterPropsMixin.InstanceTypeConfigProperty(
                    bid_price="bidPrice",
                    bid_price_as_percentage_of_on_demand_price=123,
                    configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                        classification="classification",
                        configuration_properties={
                            "configuration_properties_key": "configurationProperties"
                        },
                        configurations=[configuration_property_]
                    )],
                    custom_ami_id="customAmiId",
                    ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                        ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                            volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                iops=123,
                                size_in_gb=123,
                                throughput=123,
                                volume_type="volumeType"
                            ),
                            volumes_per_instance=123
                        )],
                        ebs_optimized=False
                    ),
                    instance_type="instanceType",
                    priority=123,
                    weighted_capacity=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8ae7c2d9cdf83102c76b38012e28092a75ee0b560545c0c6a2495b10fd2e061f)
                check_type(argname="argument bid_price", value=bid_price, expected_type=type_hints["bid_price"])
                check_type(argname="argument bid_price_as_percentage_of_on_demand_price", value=bid_price_as_percentage_of_on_demand_price, expected_type=type_hints["bid_price_as_percentage_of_on_demand_price"])
                check_type(argname="argument configurations", value=configurations, expected_type=type_hints["configurations"])
                check_type(argname="argument custom_ami_id", value=custom_ami_id, expected_type=type_hints["custom_ami_id"])
                check_type(argname="argument ebs_configuration", value=ebs_configuration, expected_type=type_hints["ebs_configuration"])
                check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument weighted_capacity", value=weighted_capacity, expected_type=type_hints["weighted_capacity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bid_price is not None:
                self._values["bid_price"] = bid_price
            if bid_price_as_percentage_of_on_demand_price is not None:
                self._values["bid_price_as_percentage_of_on_demand_price"] = bid_price_as_percentage_of_on_demand_price
            if configurations is not None:
                self._values["configurations"] = configurations
            if custom_ami_id is not None:
                self._values["custom_ami_id"] = custom_ami_id
            if ebs_configuration is not None:
                self._values["ebs_configuration"] = ebs_configuration
            if instance_type is not None:
                self._values["instance_type"] = instance_type
            if priority is not None:
                self._values["priority"] = priority
            if weighted_capacity is not None:
                self._values["weighted_capacity"] = weighted_capacity

        @builtins.property
        def bid_price(self) -> typing.Optional[builtins.str]:
            '''The bid price for each Amazon EC2 Spot Instance type as defined by ``InstanceType`` .

            Expressed in USD. If neither ``BidPrice`` nor ``BidPriceAsPercentageOfOnDemandPrice`` is provided, ``BidPriceAsPercentageOfOnDemandPrice`` defaults to 100%.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancetypeconfig.html#cfn-emr-cluster-instancetypeconfig-bidprice
            '''
            result = self._values.get("bid_price")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bid_price_as_percentage_of_on_demand_price(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''The bid price, as a percentage of On-Demand price, for each Amazon EC2 Spot Instance as defined by ``InstanceType`` .

            Expressed as a number (for example, 20 specifies 20%). If neither ``BidPrice`` nor ``BidPriceAsPercentageOfOnDemandPrice`` is provided, ``BidPriceAsPercentageOfOnDemandPrice`` defaults to 100%.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancetypeconfig.html#cfn-emr-cluster-instancetypeconfig-bidpriceaspercentageofondemandprice
            '''
            result = self._values.get("bid_price_as_percentage_of_on_demand_price")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ConfigurationProperty"]]]]:
            '''A configuration classification that applies when provisioning cluster instances, which can include configurations for applications and software that run on the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancetypeconfig.html#cfn-emr-cluster-instancetypeconfig-configurations
            '''
            result = self._values.get("configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ConfigurationProperty"]]]], result)

        @builtins.property
        def custom_ami_id(self) -> typing.Optional[builtins.str]:
            '''The custom AMI ID to use for the instance type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancetypeconfig.html#cfn-emr-cluster-instancetypeconfig-customamiid
            '''
            result = self._values.get("custom_ami_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ebs_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.EbsConfigurationProperty"]]:
            '''The configuration of Amazon Elastic Block Store (Amazon EBS) attached to each instance as defined by ``InstanceType`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancetypeconfig.html#cfn-emr-cluster-instancetypeconfig-ebsconfiguration
            '''
            result = self._values.get("ebs_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.EbsConfigurationProperty"]], result)

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            '''An Amazon EC2 instance type, such as ``m3.xlarge`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancetypeconfig.html#cfn-emr-cluster-instancetypeconfig-instancetype
            '''
            result = self._values.get("instance_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            '''The priority at which Amazon EMR launches the Amazon EC2 instances with this instance type.

            Priority starts at 0, which is the highest priority. Amazon EMR considers the highest priority first.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancetypeconfig.html#cfn-emr-cluster-instancetypeconfig-priority
            '''
            result = self._values.get("priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def weighted_capacity(self) -> typing.Optional[jsii.Number]:
            '''The number of units that a provisioned instance of this type provides toward fulfilling the target capacities defined in ``InstanceFleetConfig`` .

            This value is 1 for a master instance fleet, and must be 1 or greater for core and task instance fleets. Defaults to 1 if not specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-instancetypeconfig.html#cfn-emr-cluster-instancetypeconfig-weightedcapacity
            '''
            result = self._values.get("weighted_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceTypeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.JobFlowInstancesConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_master_security_groups": "additionalMasterSecurityGroups",
            "additional_slave_security_groups": "additionalSlaveSecurityGroups",
            "core_instance_fleet": "coreInstanceFleet",
            "core_instance_group": "coreInstanceGroup",
            "ec2_key_name": "ec2KeyName",
            "ec2_subnet_id": "ec2SubnetId",
            "ec2_subnet_ids": "ec2SubnetIds",
            "emr_managed_master_security_group": "emrManagedMasterSecurityGroup",
            "emr_managed_slave_security_group": "emrManagedSlaveSecurityGroup",
            "hadoop_version": "hadoopVersion",
            "keep_job_flow_alive_when_no_steps": "keepJobFlowAliveWhenNoSteps",
            "master_instance_fleet": "masterInstanceFleet",
            "master_instance_group": "masterInstanceGroup",
            "placement": "placement",
            "service_access_security_group": "serviceAccessSecurityGroup",
            "task_instance_fleets": "taskInstanceFleets",
            "task_instance_groups": "taskInstanceGroups",
            "termination_protected": "terminationProtected",
            "unhealthy_node_replacement": "unhealthyNodeReplacement",
        },
    )
    class JobFlowInstancesConfigProperty:
        def __init__(
            self,
            *,
            additional_master_security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
            additional_slave_security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
            core_instance_fleet: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.InstanceFleetConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            core_instance_group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.InstanceGroupConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ec2_key_name: typing.Optional[builtins.str] = None,
            ec2_subnet_id: typing.Optional[builtins.str] = None,
            ec2_subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            emr_managed_master_security_group: typing.Optional[builtins.str] = None,
            emr_managed_slave_security_group: typing.Optional[builtins.str] = None,
            hadoop_version: typing.Optional[builtins.str] = None,
            keep_job_flow_alive_when_no_steps: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            master_instance_fleet: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.InstanceFleetConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            master_instance_group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.InstanceGroupConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            placement: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.PlacementTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_access_security_group: typing.Optional[builtins.str] = None,
            task_instance_fleets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.InstanceFleetConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            task_instance_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.InstanceGroupConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            termination_protected: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            unhealthy_node_replacement: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''``JobFlowInstancesConfig`` is a property of the ``AWS::EMR::Cluster`` resource.

            ``JobFlowInstancesConfig`` defines the instance groups or instance fleets that comprise the cluster. ``JobFlowInstancesConfig`` must contain either ``InstanceFleetConfig`` or ``InstanceGroupConfig`` . They cannot be used together.

            You can now define task instance groups or task instance fleets using the ``TaskInstanceGroups`` and ``TaskInstanceFleets`` subproperties. Using these subproperties reduces delays in provisioning task nodes compared to specifying task nodes with the ``InstanceFleetConfig`` and ``InstanceGroupConfig`` resources.

            :param additional_master_security_groups: A list of additional Amazon EC2 security group IDs for the master node.
            :param additional_slave_security_groups: A list of additional Amazon EC2 security group IDs for the core and task nodes.
            :param core_instance_fleet: Describes the EC2 instances and instance configurations for the core instance fleet when using clusters with the instance fleet configuration.
            :param core_instance_group: Describes the EC2 instances and instance configurations for core instance groups when using clusters with the uniform instance group configuration.
            :param ec2_key_name: The name of the Amazon EC2 key pair that can be used to connect to the master node using SSH as the user called "hadoop.".
            :param ec2_subnet_id: Applies to clusters that use the uniform instance group configuration. To launch the cluster in Amazon Virtual Private Cloud (Amazon VPC), set this parameter to the identifier of the Amazon VPC subnet where you want the cluster to launch. If you do not specify this value and your account supports EC2-Classic, the cluster launches in EC2-Classic.
            :param ec2_subnet_ids: Applies to clusters that use the instance fleet configuration. When multiple Amazon EC2 subnet IDs are specified, Amazon EMR evaluates them and launches instances in the optimal subnet. .. epigraph:: The instance fleet configuration is available only in Amazon EMR releases 4.8.0 and later, excluding 5.0.x versions.
            :param emr_managed_master_security_group: The identifier of the Amazon EC2 security group for the master node. If you specify ``EmrManagedMasterSecurityGroup`` , you must also specify ``EmrManagedSlaveSecurityGroup`` .
            :param emr_managed_slave_security_group: The identifier of the Amazon EC2 security group for the core and task nodes. If you specify ``EmrManagedSlaveSecurityGroup`` , you must also specify ``EmrManagedMasterSecurityGroup`` .
            :param hadoop_version: Applies only to Amazon EMR release versions earlier than 4.0. The Hadoop version for the cluster. Valid inputs are "0.18" (no longer maintained), "0.20" (no longer maintained), "0.20.205" (no longer maintained), "1.0.3", "2.2.0", or "2.4.0". If you do not set this value, the default of 0.18 is used, unless the ``AmiVersion`` parameter is set in the RunJobFlow call, in which case the default version of Hadoop for that AMI version is used.
            :param keep_job_flow_alive_when_no_steps: Specifies whether the cluster should remain available after completing all steps. Defaults to ``false`` . For more information about configuring cluster termination, see `Control Cluster Termination <https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-plan-termination.html>`_ in the *EMR Management Guide* .
            :param master_instance_fleet: Describes the EC2 instances and instance configurations for the master instance fleet when using clusters with the instance fleet configuration.
            :param master_instance_group: Describes the EC2 instances and instance configurations for the master instance group when using clusters with the uniform instance group configuration.
            :param placement: The Availability Zone in which the cluster runs.
            :param service_access_security_group: The identifier of the Amazon EC2 security group for the Amazon EMR service to access clusters in VPC private subnets.
            :param task_instance_fleets: Describes the EC2 instances and instance configurations for the task instance fleets when using clusters with the instance fleet configuration. These task instance fleets are added to the cluster as part of the cluster launch. Each task instance fleet must have a unique name specified so that CloudFormation can differentiate between the task instance fleets. .. epigraph:: You can currently specify only one task instance fleet for a cluster. After creating the cluster, you can only modify the mutable properties of ``InstanceFleetConfig`` , which are ``TargetOnDemandCapacity`` and ``TargetSpotCapacity`` . Modifying any other property results in cluster replacement. > To allow a maximum of 30 Amazon EC2 instance types per fleet, include ``TaskInstanceFleets`` when you create your cluster. If you create your cluster without ``TaskInstanceFleets`` , Amazon EMR uses its default allocation strategy, which allows for a maximum of five Amazon EC2 instance types.
            :param task_instance_groups: Describes the EC2 instances and instance configurations for task instance groups when using clusters with the uniform instance group configuration. These task instance groups are added to the cluster as part of the cluster launch. Each task instance group must have a unique name specified so that CloudFormation can differentiate between the task instance groups. .. epigraph:: After creating the cluster, you can only modify the mutable properties of ``InstanceGroupConfig`` , which are ``AutoScalingPolicy`` and ``InstanceCount`` . Modifying any other property results in cluster replacement.
            :param termination_protected: Specifies whether to lock the cluster to prevent the Amazon EC2 instances from being terminated by API call, user intervention, or in the event of a job-flow error.
            :param unhealthy_node_replacement: Indicates whether Amazon EMR should gracefully replace core nodes that have degraded within the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                # configuration_property_: emr_mixins.CfnClusterPropsMixin.ConfigurationProperty
                
                job_flow_instances_config_property = emr_mixins.CfnClusterPropsMixin.JobFlowInstancesConfigProperty(
                    additional_master_security_groups=["additionalMasterSecurityGroups"],
                    additional_slave_security_groups=["additionalSlaveSecurityGroups"],
                    core_instance_fleet=emr_mixins.CfnClusterPropsMixin.InstanceFleetConfigProperty(
                        instance_type_configs=[emr_mixins.CfnClusterPropsMixin.InstanceTypeConfigProperty(
                            bid_price="bidPrice",
                            bid_price_as_percentage_of_on_demand_price=123,
                            configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                                classification="classification",
                                configuration_properties={
                                    "configuration_properties_key": "configurationProperties"
                                },
                                configurations=[configuration_property_]
                            )],
                            custom_ami_id="customAmiId",
                            ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                                ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                                    volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                        iops=123,
                                        size_in_gb=123,
                                        throughput=123,
                                        volume_type="volumeType"
                                    ),
                                    volumes_per_instance=123
                                )],
                                ebs_optimized=False
                            ),
                            instance_type="instanceType",
                            priority=123,
                            weighted_capacity=123
                        )],
                        launch_specifications=emr_mixins.CfnClusterPropsMixin.InstanceFleetProvisioningSpecificationsProperty(
                            on_demand_specification=emr_mixins.CfnClusterPropsMixin.OnDemandProvisioningSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                                    capacity_reservation_preference="capacityReservationPreference",
                                    capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                                    usage_strategy="usageStrategy"
                                )
                            ),
                            spot_specification=emr_mixins.CfnClusterPropsMixin.SpotProvisioningSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                block_duration_minutes=123,
                                timeout_action="timeoutAction",
                                timeout_duration_minutes=123
                            )
                        ),
                        name="name",
                        resize_specifications=emr_mixins.CfnClusterPropsMixin.InstanceFleetResizingSpecificationsProperty(
                            on_demand_resize_specification=emr_mixins.CfnClusterPropsMixin.OnDemandResizingSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                                    capacity_reservation_preference="capacityReservationPreference",
                                    capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                                    usage_strategy="usageStrategy"
                                ),
                                timeout_duration_minutes=123
                            ),
                            spot_resize_specification=emr_mixins.CfnClusterPropsMixin.SpotResizingSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                timeout_duration_minutes=123
                            )
                        ),
                        target_on_demand_capacity=123,
                        target_spot_capacity=123
                    ),
                    core_instance_group=emr_mixins.CfnClusterPropsMixin.InstanceGroupConfigProperty(
                        auto_scaling_policy=emr_mixins.CfnClusterPropsMixin.AutoScalingPolicyProperty(
                            constraints=emr_mixins.CfnClusterPropsMixin.ScalingConstraintsProperty(
                                max_capacity=123,
                                min_capacity=123
                            ),
                            rules=[emr_mixins.CfnClusterPropsMixin.ScalingRuleProperty(
                                action=emr_mixins.CfnClusterPropsMixin.ScalingActionProperty(
                                    market="market",
                                    simple_scaling_policy_configuration=emr_mixins.CfnClusterPropsMixin.SimpleScalingPolicyConfigurationProperty(
                                        adjustment_type="adjustmentType",
                                        cool_down=123,
                                        scaling_adjustment=123
                                    )
                                ),
                                description="description",
                                name="name",
                                trigger=emr_mixins.CfnClusterPropsMixin.ScalingTriggerProperty(
                                    cloud_watch_alarm_definition=emr_mixins.CfnClusterPropsMixin.CloudWatchAlarmDefinitionProperty(
                                        comparison_operator="comparisonOperator",
                                        dimensions=[emr_mixins.CfnClusterPropsMixin.MetricDimensionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        evaluation_periods=123,
                                        metric_name="metricName",
                                        namespace="namespace",
                                        period=123,
                                        statistic="statistic",
                                        threshold=123,
                                        unit="unit"
                                    )
                                )
                            )]
                        ),
                        bid_price="bidPrice",
                        configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                            classification="classification",
                            configuration_properties={
                                "configuration_properties_key": "configurationProperties"
                            },
                            configurations=[configuration_property_]
                        )],
                        custom_ami_id="customAmiId",
                        ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                            ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                                volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                    iops=123,
                                    size_in_gb=123,
                                    throughput=123,
                                    volume_type="volumeType"
                                ),
                                volumes_per_instance=123
                            )],
                            ebs_optimized=False
                        ),
                        instance_count=123,
                        instance_type="instanceType",
                        market="market",
                        name="name"
                    ),
                    ec2_key_name="ec2KeyName",
                    ec2_subnet_id="ec2SubnetId",
                    ec2_subnet_ids=["ec2SubnetIds"],
                    emr_managed_master_security_group="emrManagedMasterSecurityGroup",
                    emr_managed_slave_security_group="emrManagedSlaveSecurityGroup",
                    hadoop_version="hadoopVersion",
                    keep_job_flow_alive_when_no_steps=False,
                    master_instance_fleet=emr_mixins.CfnClusterPropsMixin.InstanceFleetConfigProperty(
                        instance_type_configs=[emr_mixins.CfnClusterPropsMixin.InstanceTypeConfigProperty(
                            bid_price="bidPrice",
                            bid_price_as_percentage_of_on_demand_price=123,
                            configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                                classification="classification",
                                configuration_properties={
                                    "configuration_properties_key": "configurationProperties"
                                },
                                configurations=[configuration_property_]
                            )],
                            custom_ami_id="customAmiId",
                            ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                                ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                                    volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                        iops=123,
                                        size_in_gb=123,
                                        throughput=123,
                                        volume_type="volumeType"
                                    ),
                                    volumes_per_instance=123
                                )],
                                ebs_optimized=False
                            ),
                            instance_type="instanceType",
                            priority=123,
                            weighted_capacity=123
                        )],
                        launch_specifications=emr_mixins.CfnClusterPropsMixin.InstanceFleetProvisioningSpecificationsProperty(
                            on_demand_specification=emr_mixins.CfnClusterPropsMixin.OnDemandProvisioningSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                                    capacity_reservation_preference="capacityReservationPreference",
                                    capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                                    usage_strategy="usageStrategy"
                                )
                            ),
                            spot_specification=emr_mixins.CfnClusterPropsMixin.SpotProvisioningSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                block_duration_minutes=123,
                                timeout_action="timeoutAction",
                                timeout_duration_minutes=123
                            )
                        ),
                        name="name",
                        resize_specifications=emr_mixins.CfnClusterPropsMixin.InstanceFleetResizingSpecificationsProperty(
                            on_demand_resize_specification=emr_mixins.CfnClusterPropsMixin.OnDemandResizingSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                                    capacity_reservation_preference="capacityReservationPreference",
                                    capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                                    usage_strategy="usageStrategy"
                                ),
                                timeout_duration_minutes=123
                            ),
                            spot_resize_specification=emr_mixins.CfnClusterPropsMixin.SpotResizingSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                timeout_duration_minutes=123
                            )
                        ),
                        target_on_demand_capacity=123,
                        target_spot_capacity=123
                    ),
                    master_instance_group=emr_mixins.CfnClusterPropsMixin.InstanceGroupConfigProperty(
                        auto_scaling_policy=emr_mixins.CfnClusterPropsMixin.AutoScalingPolicyProperty(
                            constraints=emr_mixins.CfnClusterPropsMixin.ScalingConstraintsProperty(
                                max_capacity=123,
                                min_capacity=123
                            ),
                            rules=[emr_mixins.CfnClusterPropsMixin.ScalingRuleProperty(
                                action=emr_mixins.CfnClusterPropsMixin.ScalingActionProperty(
                                    market="market",
                                    simple_scaling_policy_configuration=emr_mixins.CfnClusterPropsMixin.SimpleScalingPolicyConfigurationProperty(
                                        adjustment_type="adjustmentType",
                                        cool_down=123,
                                        scaling_adjustment=123
                                    )
                                ),
                                description="description",
                                name="name",
                                trigger=emr_mixins.CfnClusterPropsMixin.ScalingTriggerProperty(
                                    cloud_watch_alarm_definition=emr_mixins.CfnClusterPropsMixin.CloudWatchAlarmDefinitionProperty(
                                        comparison_operator="comparisonOperator",
                                        dimensions=[emr_mixins.CfnClusterPropsMixin.MetricDimensionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        evaluation_periods=123,
                                        metric_name="metricName",
                                        namespace="namespace",
                                        period=123,
                                        statistic="statistic",
                                        threshold=123,
                                        unit="unit"
                                    )
                                )
                            )]
                        ),
                        bid_price="bidPrice",
                        configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                            classification="classification",
                            configuration_properties={
                                "configuration_properties_key": "configurationProperties"
                            },
                            configurations=[configuration_property_]
                        )],
                        custom_ami_id="customAmiId",
                        ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                            ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                                volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                    iops=123,
                                    size_in_gb=123,
                                    throughput=123,
                                    volume_type="volumeType"
                                ),
                                volumes_per_instance=123
                            )],
                            ebs_optimized=False
                        ),
                        instance_count=123,
                        instance_type="instanceType",
                        market="market",
                        name="name"
                    ),
                    placement=emr_mixins.CfnClusterPropsMixin.PlacementTypeProperty(
                        availability_zone="availabilityZone"
                    ),
                    service_access_security_group="serviceAccessSecurityGroup",
                    task_instance_fleets=[emr_mixins.CfnClusterPropsMixin.InstanceFleetConfigProperty(
                        instance_type_configs=[emr_mixins.CfnClusterPropsMixin.InstanceTypeConfigProperty(
                            bid_price="bidPrice",
                            bid_price_as_percentage_of_on_demand_price=123,
                            configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                                classification="classification",
                                configuration_properties={
                                    "configuration_properties_key": "configurationProperties"
                                },
                                configurations=[configuration_property_]
                            )],
                            custom_ami_id="customAmiId",
                            ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                                ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                                    volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                        iops=123,
                                        size_in_gb=123,
                                        throughput=123,
                                        volume_type="volumeType"
                                    ),
                                    volumes_per_instance=123
                                )],
                                ebs_optimized=False
                            ),
                            instance_type="instanceType",
                            priority=123,
                            weighted_capacity=123
                        )],
                        launch_specifications=emr_mixins.CfnClusterPropsMixin.InstanceFleetProvisioningSpecificationsProperty(
                            on_demand_specification=emr_mixins.CfnClusterPropsMixin.OnDemandProvisioningSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                                    capacity_reservation_preference="capacityReservationPreference",
                                    capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                                    usage_strategy="usageStrategy"
                                )
                            ),
                            spot_specification=emr_mixins.CfnClusterPropsMixin.SpotProvisioningSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                block_duration_minutes=123,
                                timeout_action="timeoutAction",
                                timeout_duration_minutes=123
                            )
                        ),
                        name="name",
                        resize_specifications=emr_mixins.CfnClusterPropsMixin.InstanceFleetResizingSpecificationsProperty(
                            on_demand_resize_specification=emr_mixins.CfnClusterPropsMixin.OnDemandResizingSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                                    capacity_reservation_preference="capacityReservationPreference",
                                    capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                                    usage_strategy="usageStrategy"
                                ),
                                timeout_duration_minutes=123
                            ),
                            spot_resize_specification=emr_mixins.CfnClusterPropsMixin.SpotResizingSpecificationProperty(
                                allocation_strategy="allocationStrategy",
                                timeout_duration_minutes=123
                            )
                        ),
                        target_on_demand_capacity=123,
                        target_spot_capacity=123
                    )],
                    task_instance_groups=[emr_mixins.CfnClusterPropsMixin.InstanceGroupConfigProperty(
                        auto_scaling_policy=emr_mixins.CfnClusterPropsMixin.AutoScalingPolicyProperty(
                            constraints=emr_mixins.CfnClusterPropsMixin.ScalingConstraintsProperty(
                                max_capacity=123,
                                min_capacity=123
                            ),
                            rules=[emr_mixins.CfnClusterPropsMixin.ScalingRuleProperty(
                                action=emr_mixins.CfnClusterPropsMixin.ScalingActionProperty(
                                    market="market",
                                    simple_scaling_policy_configuration=emr_mixins.CfnClusterPropsMixin.SimpleScalingPolicyConfigurationProperty(
                                        adjustment_type="adjustmentType",
                                        cool_down=123,
                                        scaling_adjustment=123
                                    )
                                ),
                                description="description",
                                name="name",
                                trigger=emr_mixins.CfnClusterPropsMixin.ScalingTriggerProperty(
                                    cloud_watch_alarm_definition=emr_mixins.CfnClusterPropsMixin.CloudWatchAlarmDefinitionProperty(
                                        comparison_operator="comparisonOperator",
                                        dimensions=[emr_mixins.CfnClusterPropsMixin.MetricDimensionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        evaluation_periods=123,
                                        metric_name="metricName",
                                        namespace="namespace",
                                        period=123,
                                        statistic="statistic",
                                        threshold=123,
                                        unit="unit"
                                    )
                                )
                            )]
                        ),
                        bid_price="bidPrice",
                        configurations=[emr_mixins.CfnClusterPropsMixin.ConfigurationProperty(
                            classification="classification",
                            configuration_properties={
                                "configuration_properties_key": "configurationProperties"
                            },
                            configurations=[configuration_property_]
                        )],
                        custom_ami_id="customAmiId",
                        ebs_configuration=emr_mixins.CfnClusterPropsMixin.EbsConfigurationProperty(
                            ebs_block_device_configs=[emr_mixins.CfnClusterPropsMixin.EbsBlockDeviceConfigProperty(
                                volume_specification=emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                                    iops=123,
                                    size_in_gb=123,
                                    throughput=123,
                                    volume_type="volumeType"
                                ),
                                volumes_per_instance=123
                            )],
                            ebs_optimized=False
                        ),
                        instance_count=123,
                        instance_type="instanceType",
                        market="market",
                        name="name"
                    )],
                    termination_protected=False,
                    unhealthy_node_replacement=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__58fd405a49bf1b47baa02460259843f664e5a7f8fecaa14d7738928c18a30871)
                check_type(argname="argument additional_master_security_groups", value=additional_master_security_groups, expected_type=type_hints["additional_master_security_groups"])
                check_type(argname="argument additional_slave_security_groups", value=additional_slave_security_groups, expected_type=type_hints["additional_slave_security_groups"])
                check_type(argname="argument core_instance_fleet", value=core_instance_fleet, expected_type=type_hints["core_instance_fleet"])
                check_type(argname="argument core_instance_group", value=core_instance_group, expected_type=type_hints["core_instance_group"])
                check_type(argname="argument ec2_key_name", value=ec2_key_name, expected_type=type_hints["ec2_key_name"])
                check_type(argname="argument ec2_subnet_id", value=ec2_subnet_id, expected_type=type_hints["ec2_subnet_id"])
                check_type(argname="argument ec2_subnet_ids", value=ec2_subnet_ids, expected_type=type_hints["ec2_subnet_ids"])
                check_type(argname="argument emr_managed_master_security_group", value=emr_managed_master_security_group, expected_type=type_hints["emr_managed_master_security_group"])
                check_type(argname="argument emr_managed_slave_security_group", value=emr_managed_slave_security_group, expected_type=type_hints["emr_managed_slave_security_group"])
                check_type(argname="argument hadoop_version", value=hadoop_version, expected_type=type_hints["hadoop_version"])
                check_type(argname="argument keep_job_flow_alive_when_no_steps", value=keep_job_flow_alive_when_no_steps, expected_type=type_hints["keep_job_flow_alive_when_no_steps"])
                check_type(argname="argument master_instance_fleet", value=master_instance_fleet, expected_type=type_hints["master_instance_fleet"])
                check_type(argname="argument master_instance_group", value=master_instance_group, expected_type=type_hints["master_instance_group"])
                check_type(argname="argument placement", value=placement, expected_type=type_hints["placement"])
                check_type(argname="argument service_access_security_group", value=service_access_security_group, expected_type=type_hints["service_access_security_group"])
                check_type(argname="argument task_instance_fleets", value=task_instance_fleets, expected_type=type_hints["task_instance_fleets"])
                check_type(argname="argument task_instance_groups", value=task_instance_groups, expected_type=type_hints["task_instance_groups"])
                check_type(argname="argument termination_protected", value=termination_protected, expected_type=type_hints["termination_protected"])
                check_type(argname="argument unhealthy_node_replacement", value=unhealthy_node_replacement, expected_type=type_hints["unhealthy_node_replacement"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if additional_master_security_groups is not None:
                self._values["additional_master_security_groups"] = additional_master_security_groups
            if additional_slave_security_groups is not None:
                self._values["additional_slave_security_groups"] = additional_slave_security_groups
            if core_instance_fleet is not None:
                self._values["core_instance_fleet"] = core_instance_fleet
            if core_instance_group is not None:
                self._values["core_instance_group"] = core_instance_group
            if ec2_key_name is not None:
                self._values["ec2_key_name"] = ec2_key_name
            if ec2_subnet_id is not None:
                self._values["ec2_subnet_id"] = ec2_subnet_id
            if ec2_subnet_ids is not None:
                self._values["ec2_subnet_ids"] = ec2_subnet_ids
            if emr_managed_master_security_group is not None:
                self._values["emr_managed_master_security_group"] = emr_managed_master_security_group
            if emr_managed_slave_security_group is not None:
                self._values["emr_managed_slave_security_group"] = emr_managed_slave_security_group
            if hadoop_version is not None:
                self._values["hadoop_version"] = hadoop_version
            if keep_job_flow_alive_when_no_steps is not None:
                self._values["keep_job_flow_alive_when_no_steps"] = keep_job_flow_alive_when_no_steps
            if master_instance_fleet is not None:
                self._values["master_instance_fleet"] = master_instance_fleet
            if master_instance_group is not None:
                self._values["master_instance_group"] = master_instance_group
            if placement is not None:
                self._values["placement"] = placement
            if service_access_security_group is not None:
                self._values["service_access_security_group"] = service_access_security_group
            if task_instance_fleets is not None:
                self._values["task_instance_fleets"] = task_instance_fleets
            if task_instance_groups is not None:
                self._values["task_instance_groups"] = task_instance_groups
            if termination_protected is not None:
                self._values["termination_protected"] = termination_protected
            if unhealthy_node_replacement is not None:
                self._values["unhealthy_node_replacement"] = unhealthy_node_replacement

        @builtins.property
        def additional_master_security_groups(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of additional Amazon EC2 security group IDs for the master node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig.html#cfn-emr-cluster-jobflowinstancesconfig-additionalmastersecuritygroups
            '''
            result = self._values.get("additional_master_security_groups")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def additional_slave_security_groups(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of additional Amazon EC2 security group IDs for the core and task nodes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig.html#cfn-emr-cluster-jobflowinstancesconfig-additionalslavesecuritygroups
            '''
            result = self._values.get("additional_slave_security_groups")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def core_instance_fleet(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.InstanceFleetConfigProperty"]]:
            '''Describes the EC2 instances and instance configurations for the core instance fleet when using clusters with the instance fleet configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig.html#cfn-emr-cluster-jobflowinstancesconfig-coreinstancefleet
            '''
            result = self._values.get("core_instance_fleet")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.InstanceFleetConfigProperty"]], result)

        @builtins.property
        def core_instance_group(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.InstanceGroupConfigProperty"]]:
            '''Describes the EC2 instances and instance configurations for core instance groups when using clusters with the uniform instance group configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig.html#cfn-emr-cluster-jobflowinstancesconfig-coreinstancegroup
            '''
            result = self._values.get("core_instance_group")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.InstanceGroupConfigProperty"]], result)

        @builtins.property
        def ec2_key_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon EC2 key pair that can be used to connect to the master node using SSH as the user called "hadoop.".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig.html#cfn-emr-cluster-jobflowinstancesconfig-ec2keyname
            '''
            result = self._values.get("ec2_key_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ec2_subnet_id(self) -> typing.Optional[builtins.str]:
            '''Applies to clusters that use the uniform instance group configuration.

            To launch the cluster in Amazon Virtual Private Cloud (Amazon VPC), set this parameter to the identifier of the Amazon VPC subnet where you want the cluster to launch. If you do not specify this value and your account supports EC2-Classic, the cluster launches in EC2-Classic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig.html#cfn-emr-cluster-jobflowinstancesconfig-ec2subnetid
            '''
            result = self._values.get("ec2_subnet_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ec2_subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Applies to clusters that use the instance fleet configuration.

            When multiple Amazon EC2 subnet IDs are specified, Amazon EMR evaluates them and launches instances in the optimal subnet.
            .. epigraph::

               The instance fleet configuration is available only in Amazon EMR releases 4.8.0 and later, excluding 5.0.x versions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig.html#cfn-emr-cluster-jobflowinstancesconfig-ec2subnetids
            '''
            result = self._values.get("ec2_subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def emr_managed_master_security_group(self) -> typing.Optional[builtins.str]:
            '''The identifier of the Amazon EC2 security group for the master node.

            If you specify ``EmrManagedMasterSecurityGroup`` , you must also specify ``EmrManagedSlaveSecurityGroup`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig.html#cfn-emr-cluster-jobflowinstancesconfig-emrmanagedmastersecuritygroup
            '''
            result = self._values.get("emr_managed_master_security_group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def emr_managed_slave_security_group(self) -> typing.Optional[builtins.str]:
            '''The identifier of the Amazon EC2 security group for the core and task nodes.

            If you specify ``EmrManagedSlaveSecurityGroup`` , you must also specify ``EmrManagedMasterSecurityGroup`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig.html#cfn-emr-cluster-jobflowinstancesconfig-emrmanagedslavesecuritygroup
            '''
            result = self._values.get("emr_managed_slave_security_group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hadoop_version(self) -> typing.Optional[builtins.str]:
            '''Applies only to Amazon EMR release versions earlier than 4.0. The Hadoop version for the cluster. Valid inputs are "0.18" (no longer maintained), "0.20" (no longer maintained), "0.20.205" (no longer maintained), "1.0.3", "2.2.0", or "2.4.0". If you do not set this value, the default of 0.18 is used, unless the ``AmiVersion`` parameter is set in the RunJobFlow call, in which case the default version of Hadoop for that AMI version is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig.html#cfn-emr-cluster-jobflowinstancesconfig-hadoopversion
            '''
            result = self._values.get("hadoop_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def keep_job_flow_alive_when_no_steps(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the cluster should remain available after completing all steps.

            Defaults to ``false`` . For more information about configuring cluster termination, see `Control Cluster Termination <https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-plan-termination.html>`_ in the *EMR Management Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig.html#cfn-emr-cluster-jobflowinstancesconfig-keepjobflowalivewhennosteps
            '''
            result = self._values.get("keep_job_flow_alive_when_no_steps")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def master_instance_fleet(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.InstanceFleetConfigProperty"]]:
            '''Describes the EC2 instances and instance configurations for the master instance fleet when using clusters with the instance fleet configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig.html#cfn-emr-cluster-jobflowinstancesconfig-masterinstancefleet
            '''
            result = self._values.get("master_instance_fleet")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.InstanceFleetConfigProperty"]], result)

        @builtins.property
        def master_instance_group(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.InstanceGroupConfigProperty"]]:
            '''Describes the EC2 instances and instance configurations for the master instance group when using clusters with the uniform instance group configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig.html#cfn-emr-cluster-jobflowinstancesconfig-masterinstancegroup
            '''
            result = self._values.get("master_instance_group")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.InstanceGroupConfigProperty"]], result)

        @builtins.property
        def placement(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.PlacementTypeProperty"]]:
            '''The Availability Zone in which the cluster runs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig.html#cfn-emr-cluster-jobflowinstancesconfig-placement
            '''
            result = self._values.get("placement")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.PlacementTypeProperty"]], result)

        @builtins.property
        def service_access_security_group(self) -> typing.Optional[builtins.str]:
            '''The identifier of the Amazon EC2 security group for the Amazon EMR service to access clusters in VPC private subnets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig.html#cfn-emr-cluster-jobflowinstancesconfig-serviceaccesssecuritygroup
            '''
            result = self._values.get("service_access_security_group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def task_instance_fleets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.InstanceFleetConfigProperty"]]]]:
            '''Describes the EC2 instances and instance configurations for the task instance fleets when using clusters with the instance fleet configuration.

            These task instance fleets are added to the cluster as part of the cluster launch. Each task instance fleet must have a unique name specified so that CloudFormation can differentiate between the task instance fleets.
            .. epigraph::

               You can currently specify only one task instance fleet for a cluster. After creating the cluster, you can only modify the mutable properties of ``InstanceFleetConfig`` , which are ``TargetOnDemandCapacity`` and ``TargetSpotCapacity`` . Modifying any other property results in cluster replacement. > To allow a maximum of 30 Amazon EC2 instance types per fleet, include ``TaskInstanceFleets`` when you create your cluster. If you create your cluster without ``TaskInstanceFleets`` , Amazon EMR uses its default allocation strategy, which allows for a maximum of five Amazon EC2 instance types.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig.html#cfn-emr-cluster-jobflowinstancesconfig-taskinstancefleets
            '''
            result = self._values.get("task_instance_fleets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.InstanceFleetConfigProperty"]]]], result)

        @builtins.property
        def task_instance_groups(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.InstanceGroupConfigProperty"]]]]:
            '''Describes the EC2 instances and instance configurations for task instance groups when using clusters with the uniform instance group configuration.

            These task instance groups are added to the cluster as part of the cluster launch. Each task instance group must have a unique name specified so that CloudFormation can differentiate between the task instance groups.
            .. epigraph::

               After creating the cluster, you can only modify the mutable properties of ``InstanceGroupConfig`` , which are ``AutoScalingPolicy`` and ``InstanceCount`` . Modifying any other property results in cluster replacement.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig.html#cfn-emr-cluster-jobflowinstancesconfig-taskinstancegroups
            '''
            result = self._values.get("task_instance_groups")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.InstanceGroupConfigProperty"]]]], result)

        @builtins.property
        def termination_protected(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to lock the cluster to prevent the Amazon EC2 instances from being terminated by API call, user intervention, or in the event of a job-flow error.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig.html#cfn-emr-cluster-jobflowinstancesconfig-terminationprotected
            '''
            result = self._values.get("termination_protected")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def unhealthy_node_replacement(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether Amazon EMR should gracefully replace core nodes that have degraded within the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-jobflowinstancesconfig.html#cfn-emr-cluster-jobflowinstancesconfig-unhealthynodereplacement
            '''
            result = self._values.get("unhealthy_node_replacement")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JobFlowInstancesConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.KerberosAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ad_domain_join_password": "adDomainJoinPassword",
            "ad_domain_join_user": "adDomainJoinUser",
            "cross_realm_trust_principal_password": "crossRealmTrustPrincipalPassword",
            "kdc_admin_password": "kdcAdminPassword",
            "realm": "realm",
        },
    )
    class KerberosAttributesProperty:
        def __init__(
            self,
            *,
            ad_domain_join_password: typing.Optional[builtins.str] = None,
            ad_domain_join_user: typing.Optional[builtins.str] = None,
            cross_realm_trust_principal_password: typing.Optional[builtins.str] = None,
            kdc_admin_password: typing.Optional[builtins.str] = None,
            realm: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``KerberosAttributes`` is a property of the ``AWS::EMR::Cluster`` resource.

            ``KerberosAttributes`` define the cluster-specific Kerberos configuration when Kerberos authentication is enabled using a security configuration. The cluster-specific configuration must be compatible with the security configuration. For more information see `Use Kerberos Authentication <https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-kerberos.html>`_ in the *EMR Management Guide* .

            :param ad_domain_join_password: The Active Directory password for ``ADDomainJoinUser`` .
            :param ad_domain_join_user: Required only when establishing a cross-realm trust with an Active Directory domain. A user with sufficient privileges to join resources to the domain.
            :param cross_realm_trust_principal_password: Required only when establishing a cross-realm trust with a KDC in a different realm. The cross-realm principal password, which must be identical across realms.
            :param kdc_admin_password: The password used within the cluster for the kadmin service on the cluster-dedicated KDC, which maintains Kerberos principals, password policies, and keytabs for the cluster.
            :param realm: The name of the Kerberos realm to which all nodes in a cluster belong. For example, ``EC2.INTERNAL`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-kerberosattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                kerberos_attributes_property = emr_mixins.CfnClusterPropsMixin.KerberosAttributesProperty(
                    ad_domain_join_password="adDomainJoinPassword",
                    ad_domain_join_user="adDomainJoinUser",
                    cross_realm_trust_principal_password="crossRealmTrustPrincipalPassword",
                    kdc_admin_password="kdcAdminPassword",
                    realm="realm"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fdecf83a3c77dfb530ebef148c0d5a3162482486ff1472c85dae44799dbab925)
                check_type(argname="argument ad_domain_join_password", value=ad_domain_join_password, expected_type=type_hints["ad_domain_join_password"])
                check_type(argname="argument ad_domain_join_user", value=ad_domain_join_user, expected_type=type_hints["ad_domain_join_user"])
                check_type(argname="argument cross_realm_trust_principal_password", value=cross_realm_trust_principal_password, expected_type=type_hints["cross_realm_trust_principal_password"])
                check_type(argname="argument kdc_admin_password", value=kdc_admin_password, expected_type=type_hints["kdc_admin_password"])
                check_type(argname="argument realm", value=realm, expected_type=type_hints["realm"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ad_domain_join_password is not None:
                self._values["ad_domain_join_password"] = ad_domain_join_password
            if ad_domain_join_user is not None:
                self._values["ad_domain_join_user"] = ad_domain_join_user
            if cross_realm_trust_principal_password is not None:
                self._values["cross_realm_trust_principal_password"] = cross_realm_trust_principal_password
            if kdc_admin_password is not None:
                self._values["kdc_admin_password"] = kdc_admin_password
            if realm is not None:
                self._values["realm"] = realm

        @builtins.property
        def ad_domain_join_password(self) -> typing.Optional[builtins.str]:
            '''The Active Directory password for ``ADDomainJoinUser`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-kerberosattributes.html#cfn-emr-cluster-kerberosattributes-addomainjoinpassword
            '''
            result = self._values.get("ad_domain_join_password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ad_domain_join_user(self) -> typing.Optional[builtins.str]:
            '''Required only when establishing a cross-realm trust with an Active Directory domain.

            A user with sufficient privileges to join resources to the domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-kerberosattributes.html#cfn-emr-cluster-kerberosattributes-addomainjoinuser
            '''
            result = self._values.get("ad_domain_join_user")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cross_realm_trust_principal_password(self) -> typing.Optional[builtins.str]:
            '''Required only when establishing a cross-realm trust with a KDC in a different realm.

            The cross-realm principal password, which must be identical across realms.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-kerberosattributes.html#cfn-emr-cluster-kerberosattributes-crossrealmtrustprincipalpassword
            '''
            result = self._values.get("cross_realm_trust_principal_password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kdc_admin_password(self) -> typing.Optional[builtins.str]:
            '''The password used within the cluster for the kadmin service on the cluster-dedicated KDC, which maintains Kerberos principals, password policies, and keytabs for the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-kerberosattributes.html#cfn-emr-cluster-kerberosattributes-kdcadminpassword
            '''
            result = self._values.get("kdc_admin_password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def realm(self) -> typing.Optional[builtins.str]:
            '''The name of the Kerberos realm to which all nodes in a cluster belong.

            For example, ``EC2.INTERNAL`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-kerberosattributes.html#cfn-emr-cluster-kerberosattributes-realm
            '''
            result = self._values.get("realm")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KerberosAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.KeyValueProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class KeyValueProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``KeyValue`` is a subproperty of the ``HadoopJarStepConfig`` property type.

            ``KeyValue`` is used to pass parameters to a step.

            :param key: The unique identifier of a key-value pair.
            :param value: The value part of the identified key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-keyvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                key_value_property = emr_mixins.CfnClusterPropsMixin.KeyValueProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2466f4d7f058132dbdeac60b33ad52549cb4ce1ae153180e7b947587407d9ecb)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The unique identifier of a key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-keyvalue.html#cfn-emr-cluster-keyvalue-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value part of the identified key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-keyvalue.html#cfn-emr-cluster-keyvalue-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeyValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.ManagedScalingPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "compute_limits": "computeLimits",
            "scaling_strategy": "scalingStrategy",
            "utilization_performance_index": "utilizationPerformanceIndex",
        },
    )
    class ManagedScalingPolicyProperty:
        def __init__(
            self,
            *,
            compute_limits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ComputeLimitsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            scaling_strategy: typing.Optional[builtins.str] = None,
            utilization_performance_index: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Managed scaling policy for an Amazon EMR cluster.

            The policy specifies the limits for resources that can be added or terminated from a cluster. The policy only applies to the core and task nodes. The master node cannot be scaled after initial configuration.

            :param compute_limits: The Amazon EC2 unit limits for a managed scaling policy. The managed scaling activity of a cluster is not allowed to go above or below these limits. The limit only applies to the core and task nodes. The master node cannot be scaled after initial configuration.
            :param scaling_strategy: Determines whether a custom scaling utilization performance index can be set. Possible values include *ADVANCED* or *DEFAULT* .
            :param utilization_performance_index: An integer value that represents an advanced scaling strategy. Setting a higher value optimizes for performance. Setting a lower value optimizes for resource conservation. Setting the value to 50 balances performance and resource conservation. Possible values are 1, 25, 50, 75, and 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-managedscalingpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                managed_scaling_policy_property = emr_mixins.CfnClusterPropsMixin.ManagedScalingPolicyProperty(
                    compute_limits=emr_mixins.CfnClusterPropsMixin.ComputeLimitsProperty(
                        maximum_capacity_units=123,
                        maximum_core_capacity_units=123,
                        maximum_on_demand_capacity_units=123,
                        minimum_capacity_units=123,
                        unit_type="unitType"
                    ),
                    scaling_strategy="scalingStrategy",
                    utilization_performance_index=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__33434479f88dce99aa8fb85076a0dfb1c14daa5db3a46d4e59c62d75ccfaa764)
                check_type(argname="argument compute_limits", value=compute_limits, expected_type=type_hints["compute_limits"])
                check_type(argname="argument scaling_strategy", value=scaling_strategy, expected_type=type_hints["scaling_strategy"])
                check_type(argname="argument utilization_performance_index", value=utilization_performance_index, expected_type=type_hints["utilization_performance_index"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if compute_limits is not None:
                self._values["compute_limits"] = compute_limits
            if scaling_strategy is not None:
                self._values["scaling_strategy"] = scaling_strategy
            if utilization_performance_index is not None:
                self._values["utilization_performance_index"] = utilization_performance_index

        @builtins.property
        def compute_limits(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ComputeLimitsProperty"]]:
            '''The Amazon EC2 unit limits for a managed scaling policy.

            The managed scaling activity of a cluster is not allowed to go above or below these limits. The limit only applies to the core and task nodes. The master node cannot be scaled after initial configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-managedscalingpolicy.html#cfn-emr-cluster-managedscalingpolicy-computelimits
            '''
            result = self._values.get("compute_limits")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ComputeLimitsProperty"]], result)

        @builtins.property
        def scaling_strategy(self) -> typing.Optional[builtins.str]:
            '''Determines whether a custom scaling utilization performance index can be set.

            Possible values include *ADVANCED* or *DEFAULT* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-managedscalingpolicy.html#cfn-emr-cluster-managedscalingpolicy-scalingstrategy
            '''
            result = self._values.get("scaling_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def utilization_performance_index(self) -> typing.Optional[jsii.Number]:
            '''An integer value that represents an advanced scaling strategy.

            Setting a higher value optimizes for performance. Setting a lower value optimizes for resource conservation. Setting the value to 50 balances performance and resource conservation. Possible values are 1, 25, 50, 75, and 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-managedscalingpolicy.html#cfn-emr-cluster-managedscalingpolicy-utilizationperformanceindex
            '''
            result = self._values.get("utilization_performance_index")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManagedScalingPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.MetricDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class MetricDimensionProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``MetricDimension`` is a subproperty of the ``CloudWatchAlarmDefinition`` property type.

            ``MetricDimension`` specifies a CloudWatch dimension, which is specified with a ``Key`` ``Value`` pair. The key is known as a ``Name`` in CloudWatch. By default, Amazon EMR uses one dimension whose ``Key`` is ``JobFlowID`` and ``Value`` is a variable representing the cluster ID, which is ``${emr.clusterId}`` . This enables the automatic scaling rule for EMR to bootstrap when the cluster ID becomes available during cluster creation.

            :param key: The dimension name.
            :param value: The dimension value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-metricdimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                metric_dimension_property = emr_mixins.CfnClusterPropsMixin.MetricDimensionProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__661a4920ca327c5300421ff364a59b1d94ea0fc2e56aee406e22d10fbd2bbb55)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The dimension name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-metricdimension.html#cfn-emr-cluster-metricdimension-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The dimension value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-metricdimension.html#cfn-emr-cluster-metricdimension-value
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
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capacity_reservation_preference": "capacityReservationPreference",
            "capacity_reservation_resource_group_arn": "capacityReservationResourceGroupArn",
            "usage_strategy": "usageStrategy",
        },
    )
    class OnDemandCapacityReservationOptionsProperty:
        def __init__(
            self,
            *,
            capacity_reservation_preference: typing.Optional[builtins.str] = None,
            capacity_reservation_resource_group_arn: typing.Optional[builtins.str] = None,
            usage_strategy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the strategy for using unused Capacity Reservations for fulfilling On-Demand capacity.

            :param capacity_reservation_preference: Indicates the instance's Capacity Reservation preferences. Possible preferences include:. - ``open`` - The instance can run in any open Capacity Reservation that has matching attributes (instance type, platform, Availability Zone). - ``none`` - The instance avoids running in a Capacity Reservation even if one is available. The instance runs as an On-Demand Instance.
            :param capacity_reservation_resource_group_arn: The ARN of the Capacity Reservation resource group in which to run the instance.
            :param usage_strategy: Indicates whether to use unused Capacity Reservations for fulfilling On-Demand capacity. If you specify ``use-capacity-reservations-first`` , the fleet uses unused Capacity Reservations to fulfill On-Demand capacity up to the target On-Demand capacity. If multiple instance pools have unused Capacity Reservations, the On-Demand allocation strategy ( ``lowest-price`` ) is applied. If the number of unused Capacity Reservations is less than the On-Demand target capacity, the remaining On-Demand target capacity is launched according to the On-Demand allocation strategy ( ``lowest-price`` ). If you do not specify a value, the fleet fulfills the On-Demand capacity according to the chosen On-Demand allocation strategy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-ondemandcapacityreservationoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                on_demand_capacity_reservation_options_property = emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                    capacity_reservation_preference="capacityReservationPreference",
                    capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                    usage_strategy="usageStrategy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4d5266e3d048e658d8e35e6ac7a8bbdcd50eaf16dcb491f70b917395e70db778)
                check_type(argname="argument capacity_reservation_preference", value=capacity_reservation_preference, expected_type=type_hints["capacity_reservation_preference"])
                check_type(argname="argument capacity_reservation_resource_group_arn", value=capacity_reservation_resource_group_arn, expected_type=type_hints["capacity_reservation_resource_group_arn"])
                check_type(argname="argument usage_strategy", value=usage_strategy, expected_type=type_hints["usage_strategy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capacity_reservation_preference is not None:
                self._values["capacity_reservation_preference"] = capacity_reservation_preference
            if capacity_reservation_resource_group_arn is not None:
                self._values["capacity_reservation_resource_group_arn"] = capacity_reservation_resource_group_arn
            if usage_strategy is not None:
                self._values["usage_strategy"] = usage_strategy

        @builtins.property
        def capacity_reservation_preference(self) -> typing.Optional[builtins.str]:
            '''Indicates the instance's Capacity Reservation preferences. Possible preferences include:.

            - ``open`` - The instance can run in any open Capacity Reservation that has matching attributes (instance type, platform, Availability Zone).
            - ``none`` - The instance avoids running in a Capacity Reservation even if one is available. The instance runs as an On-Demand Instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-ondemandcapacityreservationoptions.html#cfn-emr-cluster-ondemandcapacityreservationoptions-capacityreservationpreference
            '''
            result = self._values.get("capacity_reservation_preference")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def capacity_reservation_resource_group_arn(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The ARN of the Capacity Reservation resource group in which to run the instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-ondemandcapacityreservationoptions.html#cfn-emr-cluster-ondemandcapacityreservationoptions-capacityreservationresourcegrouparn
            '''
            result = self._values.get("capacity_reservation_resource_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def usage_strategy(self) -> typing.Optional[builtins.str]:
            '''Indicates whether to use unused Capacity Reservations for fulfilling On-Demand capacity.

            If you specify ``use-capacity-reservations-first`` , the fleet uses unused Capacity Reservations to fulfill On-Demand capacity up to the target On-Demand capacity. If multiple instance pools have unused Capacity Reservations, the On-Demand allocation strategy ( ``lowest-price`` ) is applied. If the number of unused Capacity Reservations is less than the On-Demand target capacity, the remaining On-Demand target capacity is launched according to the On-Demand allocation strategy ( ``lowest-price`` ).

            If you do not specify a value, the fleet fulfills the On-Demand capacity according to the chosen On-Demand allocation strategy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-ondemandcapacityreservationoptions.html#cfn-emr-cluster-ondemandcapacityreservationoptions-usagestrategy
            '''
            result = self._values.get("usage_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnDemandCapacityReservationOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.OnDemandProvisioningSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allocation_strategy": "allocationStrategy",
            "capacity_reservation_options": "capacityReservationOptions",
        },
    )
    class OnDemandProvisioningSpecificationProperty:
        def __init__(
            self,
            *,
            allocation_strategy: typing.Optional[builtins.str] = None,
            capacity_reservation_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The launch specification for On-Demand Instances in the instance fleet, which determines the allocation strategy.

            .. epigraph::

               The instance fleet configuration is available only in Amazon EMR releases 4.8.0 and later, excluding 5.0.x versions. On-Demand Instances allocation strategy is available in Amazon EMR releases 5.12.1 and later.

            :param allocation_strategy: Specifies the strategy to use in launching On-Demand instance fleets. Available options are ``lowest-price`` and ``prioritized`` . ``lowest-price`` specifies to launch the instances with the lowest price first, and ``prioritized`` specifies that Amazon EMR should launch the instances with the highest priority first. The default is ``lowest-price`` .
            :param capacity_reservation_options: The launch specification for On-Demand instances in the instance fleet, which determines the allocation strategy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-ondemandprovisioningspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                on_demand_provisioning_specification_property = emr_mixins.CfnClusterPropsMixin.OnDemandProvisioningSpecificationProperty(
                    allocation_strategy="allocationStrategy",
                    capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                        capacity_reservation_preference="capacityReservationPreference",
                        capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                        usage_strategy="usageStrategy"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ca82542666625d2d1f351c5d3d64c633b55d41df9b963a43595eb6684987da76)
                check_type(argname="argument allocation_strategy", value=allocation_strategy, expected_type=type_hints["allocation_strategy"])
                check_type(argname="argument capacity_reservation_options", value=capacity_reservation_options, expected_type=type_hints["capacity_reservation_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allocation_strategy is not None:
                self._values["allocation_strategy"] = allocation_strategy
            if capacity_reservation_options is not None:
                self._values["capacity_reservation_options"] = capacity_reservation_options

        @builtins.property
        def allocation_strategy(self) -> typing.Optional[builtins.str]:
            '''Specifies the strategy to use in launching On-Demand instance fleets.

            Available options are ``lowest-price`` and ``prioritized`` . ``lowest-price`` specifies to launch the instances with the lowest price first, and ``prioritized`` specifies that Amazon EMR should launch the instances with the highest priority first. The default is ``lowest-price`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-ondemandprovisioningspecification.html#cfn-emr-cluster-ondemandprovisioningspecification-allocationstrategy
            '''
            result = self._values.get("allocation_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def capacity_reservation_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty"]]:
            '''The launch specification for On-Demand instances in the instance fleet, which determines the allocation strategy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-ondemandprovisioningspecification.html#cfn-emr-cluster-ondemandprovisioningspecification-capacityreservationoptions
            '''
            result = self._values.get("capacity_reservation_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnDemandProvisioningSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.OnDemandResizingSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allocation_strategy": "allocationStrategy",
            "capacity_reservation_options": "capacityReservationOptions",
            "timeout_duration_minutes": "timeoutDurationMinutes",
        },
    )
    class OnDemandResizingSpecificationProperty:
        def __init__(
            self,
            *,
            allocation_strategy: typing.Optional[builtins.str] = None,
            capacity_reservation_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timeout_duration_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The resize specification for On-Demand Instances in the instance fleet, which contains the resize timeout period.

            :param allocation_strategy: Specifies the allocation strategy to use to launch On-Demand instances during a resize. The default is ``lowest-price`` .
            :param capacity_reservation_options: 
            :param timeout_duration_minutes: On-Demand resize timeout in minutes. If On-Demand Instances are not provisioned within this time, the resize workflow stops. The minimum value is 5 minutes, and the maximum value is 10,080 minutes (7 days). The timeout applies to all resize workflows on the Instance Fleet. The resize could be triggered by Amazon EMR Managed Scaling or by the customer (via Amazon EMR Console, Amazon EMR CLI modify-instance-fleet or Amazon EMR SDK ModifyInstanceFleet API) or by Amazon EMR due to Amazon EC2 Spot Reclamation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-ondemandresizingspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                on_demand_resizing_specification_property = emr_mixins.CfnClusterPropsMixin.OnDemandResizingSpecificationProperty(
                    allocation_strategy="allocationStrategy",
                    capacity_reservation_options=emr_mixins.CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty(
                        capacity_reservation_preference="capacityReservationPreference",
                        capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                        usage_strategy="usageStrategy"
                    ),
                    timeout_duration_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1ccc3dd9af2174d0a98ce152c9d1446c4ae9c584c86ded46762fc1d570253bfc)
                check_type(argname="argument allocation_strategy", value=allocation_strategy, expected_type=type_hints["allocation_strategy"])
                check_type(argname="argument capacity_reservation_options", value=capacity_reservation_options, expected_type=type_hints["capacity_reservation_options"])
                check_type(argname="argument timeout_duration_minutes", value=timeout_duration_minutes, expected_type=type_hints["timeout_duration_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allocation_strategy is not None:
                self._values["allocation_strategy"] = allocation_strategy
            if capacity_reservation_options is not None:
                self._values["capacity_reservation_options"] = capacity_reservation_options
            if timeout_duration_minutes is not None:
                self._values["timeout_duration_minutes"] = timeout_duration_minutes

        @builtins.property
        def allocation_strategy(self) -> typing.Optional[builtins.str]:
            '''Specifies the allocation strategy to use to launch On-Demand instances during a resize.

            The default is ``lowest-price`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-ondemandresizingspecification.html#cfn-emr-cluster-ondemandresizingspecification-allocationstrategy
            '''
            result = self._values.get("allocation_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def capacity_reservation_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-ondemandresizingspecification.html#cfn-emr-cluster-ondemandresizingspecification-capacityreservationoptions
            '''
            result = self._values.get("capacity_reservation_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty"]], result)

        @builtins.property
        def timeout_duration_minutes(self) -> typing.Optional[jsii.Number]:
            '''On-Demand resize timeout in minutes.

            If On-Demand Instances are not provisioned within this time, the resize workflow stops. The minimum value is 5 minutes, and the maximum value is 10,080 minutes (7 days). The timeout applies to all resize workflows on the Instance Fleet. The resize could be triggered by Amazon EMR Managed Scaling or by the customer (via Amazon EMR Console, Amazon EMR CLI modify-instance-fleet or Amazon EMR SDK ModifyInstanceFleet API) or by Amazon EMR due to Amazon EC2 Spot Reclamation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-ondemandresizingspecification.html#cfn-emr-cluster-ondemandresizingspecification-timeoutdurationminutes
            '''
            result = self._values.get("timeout_duration_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnDemandResizingSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.PlacementGroupConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instance_role": "instanceRole",
            "placement_strategy": "placementStrategy",
        },
    )
    class PlacementGroupConfigProperty:
        def __init__(
            self,
            *,
            instance_role: typing.Optional[builtins.str] = None,
            placement_strategy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Placement group configuration for an Amazon EMR cluster.

            The configuration specifies the placement strategy that can be applied to instance roles during cluster creation.

            To use this configuration, consider attaching managed policy AmazonElasticMapReducePlacementGroupPolicy to the Amazon EMR role.

            :param instance_role: Role of the instance in the cluster. Starting with Amazon EMR release 5.23.0, the only supported instance role is ``MASTER`` .
            :param placement_strategy: Amazon EC2 Placement Group strategy associated with instance role. Starting with Amazon EMR release 5.23.0, the only supported placement strategy is ``SPREAD`` for the ``MASTER`` instance role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-placementgroupconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                placement_group_config_property = emr_mixins.CfnClusterPropsMixin.PlacementGroupConfigProperty(
                    instance_role="instanceRole",
                    placement_strategy="placementStrategy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__382a1dad5ad1d6e934e292f66c4516ee7ec57781153e5372df9100a4a7622bf6)
                check_type(argname="argument instance_role", value=instance_role, expected_type=type_hints["instance_role"])
                check_type(argname="argument placement_strategy", value=placement_strategy, expected_type=type_hints["placement_strategy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_role is not None:
                self._values["instance_role"] = instance_role
            if placement_strategy is not None:
                self._values["placement_strategy"] = placement_strategy

        @builtins.property
        def instance_role(self) -> typing.Optional[builtins.str]:
            '''Role of the instance in the cluster.

            Starting with Amazon EMR release 5.23.0, the only supported instance role is ``MASTER`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-placementgroupconfig.html#cfn-emr-cluster-placementgroupconfig-instancerole
            '''
            result = self._values.get("instance_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def placement_strategy(self) -> typing.Optional[builtins.str]:
            '''Amazon EC2 Placement Group strategy associated with instance role.

            Starting with Amazon EMR release 5.23.0, the only supported placement strategy is ``SPREAD`` for the ``MASTER`` instance role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-placementgroupconfig.html#cfn-emr-cluster-placementgroupconfig-placementstrategy
            '''
            result = self._values.get("placement_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PlacementGroupConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.PlacementTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"availability_zone": "availabilityZone"},
    )
    class PlacementTypeProperty:
        def __init__(
            self,
            *,
            availability_zone: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``PlacementType`` is a property of the ``AWS::EMR::Cluster`` resource.

            ``PlacementType`` determines the Amazon EC2 Availability Zone configuration of the cluster (job flow).

            :param availability_zone: The Amazon EC2 Availability Zone for the cluster. ``AvailabilityZone`` is used for uniform instance groups, while ``AvailabilityZones`` (plural) is used for instance fleets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-placementtype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                placement_type_property = emr_mixins.CfnClusterPropsMixin.PlacementTypeProperty(
                    availability_zone="availabilityZone"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b1853633435e424bde42c85a2f8cf573f96bd538e8ccd8f152cd0df6a9753d75)
                check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_zone is not None:
                self._values["availability_zone"] = availability_zone

        @builtins.property
        def availability_zone(self) -> typing.Optional[builtins.str]:
            '''The Amazon EC2 Availability Zone for the cluster.

            ``AvailabilityZone`` is used for uniform instance groups, while ``AvailabilityZones`` (plural) is used for instance fleets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-placementtype.html#cfn-emr-cluster-placementtype-availabilityzone
            '''
            result = self._values.get("availability_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PlacementTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.ScalingActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "market": "market",
            "simple_scaling_policy_configuration": "simpleScalingPolicyConfiguration",
        },
    )
    class ScalingActionProperty:
        def __init__(
            self,
            *,
            market: typing.Optional[builtins.str] = None,
            simple_scaling_policy_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.SimpleScalingPolicyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''``ScalingAction`` is a subproperty of the ``ScalingRule`` property type.

            ``ScalingAction`` determines the type of adjustment the automatic scaling activity makes when triggered, and the periodicity of the adjustment.

            :param market: Not available for instance groups. Instance groups use the market type specified for the group.
            :param simple_scaling_policy_configuration: The type of adjustment the automatic scaling activity makes when triggered, and the periodicity of the adjustment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-scalingaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                scaling_action_property = emr_mixins.CfnClusterPropsMixin.ScalingActionProperty(
                    market="market",
                    simple_scaling_policy_configuration=emr_mixins.CfnClusterPropsMixin.SimpleScalingPolicyConfigurationProperty(
                        adjustment_type="adjustmentType",
                        cool_down=123,
                        scaling_adjustment=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f6c18c3893105179056e97fc73e55d0ebfe42807f32837c8e0d40f19b2f98039)
                check_type(argname="argument market", value=market, expected_type=type_hints["market"])
                check_type(argname="argument simple_scaling_policy_configuration", value=simple_scaling_policy_configuration, expected_type=type_hints["simple_scaling_policy_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if market is not None:
                self._values["market"] = market
            if simple_scaling_policy_configuration is not None:
                self._values["simple_scaling_policy_configuration"] = simple_scaling_policy_configuration

        @builtins.property
        def market(self) -> typing.Optional[builtins.str]:
            '''Not available for instance groups.

            Instance groups use the market type specified for the group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-scalingaction.html#cfn-emr-cluster-scalingaction-market
            '''
            result = self._values.get("market")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def simple_scaling_policy_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.SimpleScalingPolicyConfigurationProperty"]]:
            '''The type of adjustment the automatic scaling activity makes when triggered, and the periodicity of the adjustment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-scalingaction.html#cfn-emr-cluster-scalingaction-simplescalingpolicyconfiguration
            '''
            result = self._values.get("simple_scaling_policy_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.SimpleScalingPolicyConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.ScalingConstraintsProperty",
        jsii_struct_bases=[],
        name_mapping={"max_capacity": "maxCapacity", "min_capacity": "minCapacity"},
    )
    class ScalingConstraintsProperty:
        def __init__(
            self,
            *,
            max_capacity: typing.Optional[jsii.Number] = None,
            min_capacity: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``ScalingConstraints`` is a subproperty of the ``AutoScalingPolicy`` property type.

            ``ScalingConstraints`` defines the upper and lower EC2 instance limits for an automatic scaling policy. Automatic scaling activities triggered by automatic scaling rules will not cause an instance group to grow above or shrink below these limits.

            :param max_capacity: The upper boundary of Amazon EC2 instances in an instance group beyond which scaling activities are not allowed to grow. Scale-out activities will not add instances beyond this boundary.
            :param min_capacity: The lower boundary of Amazon EC2 instances in an instance group below which scaling activities are not allowed to shrink. Scale-in activities will not terminate instances below this boundary.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-scalingconstraints.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                scaling_constraints_property = emr_mixins.CfnClusterPropsMixin.ScalingConstraintsProperty(
                    max_capacity=123,
                    min_capacity=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2b810ae7b44182a110ee8bde00e682add15fd8abc30f2b03528a7ff55b6e3e90)
                check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
                check_type(argname="argument min_capacity", value=min_capacity, expected_type=type_hints["min_capacity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_capacity is not None:
                self._values["max_capacity"] = max_capacity
            if min_capacity is not None:
                self._values["min_capacity"] = min_capacity

        @builtins.property
        def max_capacity(self) -> typing.Optional[jsii.Number]:
            '''The upper boundary of Amazon EC2 instances in an instance group beyond which scaling activities are not allowed to grow.

            Scale-out activities will not add instances beyond this boundary.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-scalingconstraints.html#cfn-emr-cluster-scalingconstraints-maxcapacity
            '''
            result = self._values.get("max_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_capacity(self) -> typing.Optional[jsii.Number]:
            '''The lower boundary of Amazon EC2 instances in an instance group below which scaling activities are not allowed to shrink.

            Scale-in activities will not terminate instances below this boundary.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-scalingconstraints.html#cfn-emr-cluster-scalingconstraints-mincapacity
            '''
            result = self._values.get("min_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingConstraintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.ScalingRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "description": "description",
            "name": "name",
            "trigger": "trigger",
        },
    )
    class ScalingRuleProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ScalingActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            description: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            trigger: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ScalingTriggerProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''``ScalingRule`` is a subproperty of the ``AutoScalingPolicy`` property type.

            ``ScalingRule`` defines the scale-in or scale-out rules for scaling activity, including the CloudWatch metric alarm that triggers activity, how EC2 instances are added or removed, and the periodicity of adjustments. The automatic scaling policy for an instance group can comprise one or more automatic scaling rules.

            :param action: The conditions that trigger an automatic scaling activity.
            :param description: A friendly, more verbose description of the automatic scaling rule.
            :param name: The name used to identify an automatic scaling rule. Rule names must be unique within a scaling policy.
            :param trigger: The CloudWatch alarm definition that determines when automatic scaling activity is triggered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-scalingrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                scaling_rule_property = emr_mixins.CfnClusterPropsMixin.ScalingRuleProperty(
                    action=emr_mixins.CfnClusterPropsMixin.ScalingActionProperty(
                        market="market",
                        simple_scaling_policy_configuration=emr_mixins.CfnClusterPropsMixin.SimpleScalingPolicyConfigurationProperty(
                            adjustment_type="adjustmentType",
                            cool_down=123,
                            scaling_adjustment=123
                        )
                    ),
                    description="description",
                    name="name",
                    trigger=emr_mixins.CfnClusterPropsMixin.ScalingTriggerProperty(
                        cloud_watch_alarm_definition=emr_mixins.CfnClusterPropsMixin.CloudWatchAlarmDefinitionProperty(
                            comparison_operator="comparisonOperator",
                            dimensions=[emr_mixins.CfnClusterPropsMixin.MetricDimensionProperty(
                                key="key",
                                value="value"
                            )],
                            evaluation_periods=123,
                            metric_name="metricName",
                            namespace="namespace",
                            period=123,
                            statistic="statistic",
                            threshold=123,
                            unit="unit"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9488aa63484f7d50d2a03a2368060860a30d899ae57d1fc6ca6fcca3fc0c49cf)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if description is not None:
                self._values["description"] = description
            if name is not None:
                self._values["name"] = name
            if trigger is not None:
                self._values["trigger"] = trigger

        @builtins.property
        def action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ScalingActionProperty"]]:
            '''The conditions that trigger an automatic scaling activity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-scalingrule.html#cfn-emr-cluster-scalingrule-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ScalingActionProperty"]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A friendly, more verbose description of the automatic scaling rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-scalingrule.html#cfn-emr-cluster-scalingrule-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name used to identify an automatic scaling rule.

            Rule names must be unique within a scaling policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-scalingrule.html#cfn-emr-cluster-scalingrule-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def trigger(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ScalingTriggerProperty"]]:
            '''The CloudWatch alarm definition that determines when automatic scaling activity is triggered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-scalingrule.html#cfn-emr-cluster-scalingrule-trigger
            '''
            result = self._values.get("trigger")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ScalingTriggerProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.ScalingTriggerProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_watch_alarm_definition": "cloudWatchAlarmDefinition"},
    )
    class ScalingTriggerProperty:
        def __init__(
            self,
            *,
            cloud_watch_alarm_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.CloudWatchAlarmDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''``ScalingTrigger`` is a subproperty of the ``ScalingRule`` property type.

            ``ScalingTrigger`` determines the conditions that trigger an automatic scaling activity.

            :param cloud_watch_alarm_definition: The definition of a CloudWatch metric alarm. When the defined alarm conditions are met along with other trigger parameters, scaling activity begins.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-scalingtrigger.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                scaling_trigger_property = emr_mixins.CfnClusterPropsMixin.ScalingTriggerProperty(
                    cloud_watch_alarm_definition=emr_mixins.CfnClusterPropsMixin.CloudWatchAlarmDefinitionProperty(
                        comparison_operator="comparisonOperator",
                        dimensions=[emr_mixins.CfnClusterPropsMixin.MetricDimensionProperty(
                            key="key",
                            value="value"
                        )],
                        evaluation_periods=123,
                        metric_name="metricName",
                        namespace="namespace",
                        period=123,
                        statistic="statistic",
                        threshold=123,
                        unit="unit"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b83dbb701cecd175bdeceb4aa6e69172ca4e01b50c2691ae8dca65fe1fb12769)
                check_type(argname="argument cloud_watch_alarm_definition", value=cloud_watch_alarm_definition, expected_type=type_hints["cloud_watch_alarm_definition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_alarm_definition is not None:
                self._values["cloud_watch_alarm_definition"] = cloud_watch_alarm_definition

        @builtins.property
        def cloud_watch_alarm_definition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.CloudWatchAlarmDefinitionProperty"]]:
            '''The definition of a CloudWatch metric alarm.

            When the defined alarm conditions are met along with other trigger parameters, scaling activity begins.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-scalingtrigger.html#cfn-emr-cluster-scalingtrigger-cloudwatchalarmdefinition
            '''
            result = self._values.get("cloud_watch_alarm_definition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.CloudWatchAlarmDefinitionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingTriggerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.ScriptBootstrapActionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"args": "args", "path": "path"},
    )
    class ScriptBootstrapActionConfigProperty:
        def __init__(
            self,
            *,
            args: typing.Optional[typing.Sequence[builtins.str]] = None,
            path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``ScriptBootstrapActionConfig`` is a subproperty of the ``BootstrapActionConfig`` property type.

            ``ScriptBootstrapActionConfig`` specifies the arguments and location of the bootstrap script for EMR to run on all cluster nodes before it installs open-source big data applications on them.

            :param args: A list of command line arguments to pass to the bootstrap action script.
            :param path: Location in Amazon S3 of the script to run during a bootstrap action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-scriptbootstrapactionconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                script_bootstrap_action_config_property = emr_mixins.CfnClusterPropsMixin.ScriptBootstrapActionConfigProperty(
                    args=["args"],
                    path="path"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__57ca6c935da0cbc1942b938c1ff463c4461323a10e2de71df2c86379da576a49)
                check_type(argname="argument args", value=args, expected_type=type_hints["args"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if args is not None:
                self._values["args"] = args
            if path is not None:
                self._values["path"] = path

        @builtins.property
        def args(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of command line arguments to pass to the bootstrap action script.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-scriptbootstrapactionconfig.html#cfn-emr-cluster-scriptbootstrapactionconfig-args
            '''
            result = self._values.get("args")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''Location in Amazon S3 of the script to run during a bootstrap action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-scriptbootstrapactionconfig.html#cfn-emr-cluster-scriptbootstrapactionconfig-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScriptBootstrapActionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.SimpleScalingPolicyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "adjustment_type": "adjustmentType",
            "cool_down": "coolDown",
            "scaling_adjustment": "scalingAdjustment",
        },
    )
    class SimpleScalingPolicyConfigurationProperty:
        def __init__(
            self,
            *,
            adjustment_type: typing.Optional[builtins.str] = None,
            cool_down: typing.Optional[jsii.Number] = None,
            scaling_adjustment: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``SimpleScalingPolicyConfiguration`` is a subproperty of the ``ScalingAction`` property type.

            ``SimpleScalingPolicyConfiguration`` determines how an automatic scaling action adds or removes instances, the cooldown period, and the number of EC2 instances that are added each time the CloudWatch metric alarm condition is satisfied.

            :param adjustment_type: The way in which Amazon EC2 instances are added (if ``ScalingAdjustment`` is a positive number) or terminated (if ``ScalingAdjustment`` is a negative number) each time the scaling activity is triggered. ``CHANGE_IN_CAPACITY`` is the default. ``CHANGE_IN_CAPACITY`` indicates that the Amazon EC2 instance count increments or decrements by ``ScalingAdjustment`` , which should be expressed as an integer. ``PERCENT_CHANGE_IN_CAPACITY`` indicates the instance count increments or decrements by the percentage specified by ``ScalingAdjustment`` , which should be expressed as an integer. For example, 20 indicates an increase in 20% increments of cluster capacity. ``EXACT_CAPACITY`` indicates the scaling activity results in an instance group with the number of Amazon EC2 instances specified by ``ScalingAdjustment`` , which should be expressed as a positive integer.
            :param cool_down: The amount of time, in seconds, after a scaling activity completes before any further trigger-related scaling activities can start. The default value is 0.
            :param scaling_adjustment: The amount by which to scale in or scale out, based on the specified ``AdjustmentType`` . A positive value adds to the instance group's Amazon EC2 instance count while a negative number removes instances. If ``AdjustmentType`` is set to ``EXACT_CAPACITY`` , the number should only be a positive integer. If ``AdjustmentType`` is set to ``PERCENT_CHANGE_IN_CAPACITY`` , the value should express the percentage as an integer. For example, -20 indicates a decrease in 20% increments of cluster capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-simplescalingpolicyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                simple_scaling_policy_configuration_property = emr_mixins.CfnClusterPropsMixin.SimpleScalingPolicyConfigurationProperty(
                    adjustment_type="adjustmentType",
                    cool_down=123,
                    scaling_adjustment=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4db4a9f3caa94e09a9abf74b632962d0d52306311c4549c6c0aaeb6c0ef1b84f)
                check_type(argname="argument adjustment_type", value=adjustment_type, expected_type=type_hints["adjustment_type"])
                check_type(argname="argument cool_down", value=cool_down, expected_type=type_hints["cool_down"])
                check_type(argname="argument scaling_adjustment", value=scaling_adjustment, expected_type=type_hints["scaling_adjustment"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if adjustment_type is not None:
                self._values["adjustment_type"] = adjustment_type
            if cool_down is not None:
                self._values["cool_down"] = cool_down
            if scaling_adjustment is not None:
                self._values["scaling_adjustment"] = scaling_adjustment

        @builtins.property
        def adjustment_type(self) -> typing.Optional[builtins.str]:
            '''The way in which Amazon EC2 instances are added (if ``ScalingAdjustment`` is a positive number) or terminated (if ``ScalingAdjustment`` is a negative number) each time the scaling activity is triggered.

            ``CHANGE_IN_CAPACITY`` is the default. ``CHANGE_IN_CAPACITY`` indicates that the Amazon EC2 instance count increments or decrements by ``ScalingAdjustment`` , which should be expressed as an integer. ``PERCENT_CHANGE_IN_CAPACITY`` indicates the instance count increments or decrements by the percentage specified by ``ScalingAdjustment`` , which should be expressed as an integer. For example, 20 indicates an increase in 20% increments of cluster capacity. ``EXACT_CAPACITY`` indicates the scaling activity results in an instance group with the number of Amazon EC2 instances specified by ``ScalingAdjustment`` , which should be expressed as a positive integer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-simplescalingpolicyconfiguration.html#cfn-emr-cluster-simplescalingpolicyconfiguration-adjustmenttype
            '''
            result = self._values.get("adjustment_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cool_down(self) -> typing.Optional[jsii.Number]:
            '''The amount of time, in seconds, after a scaling activity completes before any further trigger-related scaling activities can start.

            The default value is 0.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-simplescalingpolicyconfiguration.html#cfn-emr-cluster-simplescalingpolicyconfiguration-cooldown
            '''
            result = self._values.get("cool_down")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def scaling_adjustment(self) -> typing.Optional[jsii.Number]:
            '''The amount by which to scale in or scale out, based on the specified ``AdjustmentType`` .

            A positive value adds to the instance group's Amazon EC2 instance count while a negative number removes instances. If ``AdjustmentType`` is set to ``EXACT_CAPACITY`` , the number should only be a positive integer. If ``AdjustmentType`` is set to ``PERCENT_CHANGE_IN_CAPACITY`` , the value should express the percentage as an integer. For example, -20 indicates a decrease in 20% increments of cluster capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-simplescalingpolicyconfiguration.html#cfn-emr-cluster-simplescalingpolicyconfiguration-scalingadjustment
            '''
            result = self._values.get("scaling_adjustment")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SimpleScalingPolicyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.SpotProvisioningSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allocation_strategy": "allocationStrategy",
            "block_duration_minutes": "blockDurationMinutes",
            "timeout_action": "timeoutAction",
            "timeout_duration_minutes": "timeoutDurationMinutes",
        },
    )
    class SpotProvisioningSpecificationProperty:
        def __init__(
            self,
            *,
            allocation_strategy: typing.Optional[builtins.str] = None,
            block_duration_minutes: typing.Optional[jsii.Number] = None,
            timeout_action: typing.Optional[builtins.str] = None,
            timeout_duration_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``SpotProvisioningSpecification`` is a subproperty of the ``InstanceFleetProvisioningSpecifications`` property type.

            ``SpotProvisioningSpecification`` determines the launch specification for Spot instances in the instance fleet, which includes the defined duration and provisioning timeout behavior.
            .. epigraph::

               The instance fleet configuration is available only in Amazon EMR versions 4.8.0 and later, excluding 5.0.x versions.

            :param allocation_strategy: Specifies one of the following strategies to launch Spot Instance fleets: ``capacity-optimized`` , ``price-capacity-optimized`` , ``lowest-price`` , or ``diversified`` , and ``capacity-optimized-prioritized`` . For more information on the provisioning strategies, see `Allocation strategies for Spot Instances <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-fleet-allocation-strategy.html>`_ in the *Amazon EC2 User Guide for Linux Instances* . .. epigraph:: When you launch a Spot Instance fleet with the old console, it automatically launches with the ``capacity-optimized`` strategy. You can't change the allocation strategy from the old console.
            :param block_duration_minutes: The defined duration for Spot Instances (also known as Spot blocks) in minutes. When specified, the Spot Instance does not terminate before the defined duration expires, and defined duration pricing for Spot Instances applies. Valid values are 60, 120, 180, 240, 300, or 360. The duration period starts as soon as a Spot Instance receives its instance ID. At the end of the duration, Amazon EC2 marks the Spot Instance for termination and provides a Spot Instance termination notice, which gives the instance a two-minute warning before it terminates. .. epigraph:: Spot Instances with a defined duration (also known as Spot blocks) are no longer available to new customers from July 1, 2021. For customers who have previously used the feature, we will continue to support Spot Instances with a defined duration until December 31, 2022.
            :param timeout_action: The action to take when ``TargetSpotCapacity`` has not been fulfilled when the ``TimeoutDurationMinutes`` has expired; that is, when all Spot Instances could not be provisioned within the Spot provisioning timeout. Valid values are ``TERMINATE_CLUSTER`` and ``SWITCH_TO_ON_DEMAND`` . SWITCH_TO_ON_DEMAND specifies that if no Spot Instances are available, On-Demand Instances should be provisioned to fulfill any remaining Spot capacity.
            :param timeout_duration_minutes: The Spot provisioning timeout period in minutes. If Spot Instances are not provisioned within this time period, the ``TimeOutAction`` is taken. Minimum value is 5 and maximum value is 1440. The timeout applies only during initial provisioning, when the cluster is first created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-spotprovisioningspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                spot_provisioning_specification_property = emr_mixins.CfnClusterPropsMixin.SpotProvisioningSpecificationProperty(
                    allocation_strategy="allocationStrategy",
                    block_duration_minutes=123,
                    timeout_action="timeoutAction",
                    timeout_duration_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__32b630f3f74349123a69baae2eac1aebc57e52911a25a763793c6a0929de4c74)
                check_type(argname="argument allocation_strategy", value=allocation_strategy, expected_type=type_hints["allocation_strategy"])
                check_type(argname="argument block_duration_minutes", value=block_duration_minutes, expected_type=type_hints["block_duration_minutes"])
                check_type(argname="argument timeout_action", value=timeout_action, expected_type=type_hints["timeout_action"])
                check_type(argname="argument timeout_duration_minutes", value=timeout_duration_minutes, expected_type=type_hints["timeout_duration_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allocation_strategy is not None:
                self._values["allocation_strategy"] = allocation_strategy
            if block_duration_minutes is not None:
                self._values["block_duration_minutes"] = block_duration_minutes
            if timeout_action is not None:
                self._values["timeout_action"] = timeout_action
            if timeout_duration_minutes is not None:
                self._values["timeout_duration_minutes"] = timeout_duration_minutes

        @builtins.property
        def allocation_strategy(self) -> typing.Optional[builtins.str]:
            '''Specifies one of the following strategies to launch Spot Instance fleets: ``capacity-optimized`` , ``price-capacity-optimized`` , ``lowest-price`` , or ``diversified`` , and ``capacity-optimized-prioritized`` .

            For more information on the provisioning strategies, see `Allocation strategies for Spot Instances <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-fleet-allocation-strategy.html>`_ in the *Amazon EC2 User Guide for Linux Instances* .
            .. epigraph::

               When you launch a Spot Instance fleet with the old console, it automatically launches with the ``capacity-optimized`` strategy. You can't change the allocation strategy from the old console.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-spotprovisioningspecification.html#cfn-emr-cluster-spotprovisioningspecification-allocationstrategy
            '''
            result = self._values.get("allocation_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def block_duration_minutes(self) -> typing.Optional[jsii.Number]:
            '''The defined duration for Spot Instances (also known as Spot blocks) in minutes.

            When specified, the Spot Instance does not terminate before the defined duration expires, and defined duration pricing for Spot Instances applies. Valid values are 60, 120, 180, 240, 300, or 360. The duration period starts as soon as a Spot Instance receives its instance ID. At the end of the duration, Amazon EC2 marks the Spot Instance for termination and provides a Spot Instance termination notice, which gives the instance a two-minute warning before it terminates.
            .. epigraph::

               Spot Instances with a defined duration (also known as Spot blocks) are no longer available to new customers from July 1, 2021. For customers who have previously used the feature, we will continue to support Spot Instances with a defined duration until December 31, 2022.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-spotprovisioningspecification.html#cfn-emr-cluster-spotprovisioningspecification-blockdurationminutes
            '''
            result = self._values.get("block_duration_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def timeout_action(self) -> typing.Optional[builtins.str]:
            '''The action to take when ``TargetSpotCapacity`` has not been fulfilled when the ``TimeoutDurationMinutes`` has expired;

            that is, when all Spot Instances could not be provisioned within the Spot provisioning timeout. Valid values are ``TERMINATE_CLUSTER`` and ``SWITCH_TO_ON_DEMAND`` . SWITCH_TO_ON_DEMAND specifies that if no Spot Instances are available, On-Demand Instances should be provisioned to fulfill any remaining Spot capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-spotprovisioningspecification.html#cfn-emr-cluster-spotprovisioningspecification-timeoutaction
            '''
            result = self._values.get("timeout_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timeout_duration_minutes(self) -> typing.Optional[jsii.Number]:
            '''The Spot provisioning timeout period in minutes.

            If Spot Instances are not provisioned within this time period, the ``TimeOutAction`` is taken. Minimum value is 5 and maximum value is 1440. The timeout applies only during initial provisioning, when the cluster is first created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-spotprovisioningspecification.html#cfn-emr-cluster-spotprovisioningspecification-timeoutdurationminutes
            '''
            result = self._values.get("timeout_duration_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SpotProvisioningSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.SpotResizingSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allocation_strategy": "allocationStrategy",
            "timeout_duration_minutes": "timeoutDurationMinutes",
        },
    )
    class SpotResizingSpecificationProperty:
        def __init__(
            self,
            *,
            allocation_strategy: typing.Optional[builtins.str] = None,
            timeout_duration_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The resize specification for Spot Instances in the instance fleet, which contains the resize timeout period.

            :param allocation_strategy: Specifies the allocation strategy to use to launch Spot instances during a resize. If you run Amazon EMR releases 6.9.0 or higher, the default is ``price-capacity-optimized`` . If you run Amazon EMR releases 6.8.0 or lower, the default is ``capacity-optimized`` .
            :param timeout_duration_minutes: Spot resize timeout in minutes. If Spot Instances are not provisioned within this time, the resize workflow will stop provisioning of Spot instances. Minimum value is 5 minutes and maximum value is 10,080 minutes (7 days). The timeout applies to all resize workflows on the Instance Fleet. The resize could be triggered by Amazon EMR Managed Scaling or by the customer (via Amazon EMR Console, Amazon EMR CLI modify-instance-fleet or Amazon EMR SDK ModifyInstanceFleet API) or by Amazon EMR due to Amazon EC2 Spot Reclamation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-spotresizingspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                spot_resizing_specification_property = emr_mixins.CfnClusterPropsMixin.SpotResizingSpecificationProperty(
                    allocation_strategy="allocationStrategy",
                    timeout_duration_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ed49dad4fd51a980e414310a80c0469508fbd66697f6e56239b008a65c61b384)
                check_type(argname="argument allocation_strategy", value=allocation_strategy, expected_type=type_hints["allocation_strategy"])
                check_type(argname="argument timeout_duration_minutes", value=timeout_duration_minutes, expected_type=type_hints["timeout_duration_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allocation_strategy is not None:
                self._values["allocation_strategy"] = allocation_strategy
            if timeout_duration_minutes is not None:
                self._values["timeout_duration_minutes"] = timeout_duration_minutes

        @builtins.property
        def allocation_strategy(self) -> typing.Optional[builtins.str]:
            '''Specifies the allocation strategy to use to launch Spot instances during a resize.

            If you run Amazon EMR releases 6.9.0 or higher, the default is ``price-capacity-optimized`` . If you run Amazon EMR releases 6.8.0 or lower, the default is ``capacity-optimized`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-spotresizingspecification.html#cfn-emr-cluster-spotresizingspecification-allocationstrategy
            '''
            result = self._values.get("allocation_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timeout_duration_minutes(self) -> typing.Optional[jsii.Number]:
            '''Spot resize timeout in minutes.

            If Spot Instances are not provisioned within this time, the resize workflow will stop provisioning of Spot instances. Minimum value is 5 minutes and maximum value is 10,080 minutes (7 days). The timeout applies to all resize workflows on the Instance Fleet. The resize could be triggered by Amazon EMR Managed Scaling or by the customer (via Amazon EMR Console, Amazon EMR CLI modify-instance-fleet or Amazon EMR SDK ModifyInstanceFleet API) or by Amazon EMR due to Amazon EC2 Spot Reclamation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-spotresizingspecification.html#cfn-emr-cluster-spotresizingspecification-timeoutdurationminutes
            '''
            result = self._values.get("timeout_duration_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SpotResizingSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.StepConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_on_failure": "actionOnFailure",
            "hadoop_jar_step": "hadoopJarStep",
            "name": "name",
        },
    )
    class StepConfigProperty:
        def __init__(
            self,
            *,
            action_on_failure: typing.Optional[builtins.str] = None,
            hadoop_jar_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.HadoopJarStepConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``StepConfig`` is a property of the ``AWS::EMR::Cluster`` resource.

            The ``StepConfig`` property type specifies a cluster (job flow) step, which runs only on the master node. Steps are used to submit data processing jobs to the cluster.

            :param action_on_failure: The action to take when the cluster step fails. Possible values are ``CANCEL_AND_WAIT`` and ``CONTINUE`` .
            :param hadoop_jar_step: The JAR file used for the step.
            :param name: The name of the step.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-stepconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                step_config_property = emr_mixins.CfnClusterPropsMixin.StepConfigProperty(
                    action_on_failure="actionOnFailure",
                    hadoop_jar_step=emr_mixins.CfnClusterPropsMixin.HadoopJarStepConfigProperty(
                        args=["args"],
                        jar="jar",
                        main_class="mainClass",
                        step_properties=[emr_mixins.CfnClusterPropsMixin.KeyValueProperty(
                            key="key",
                            value="value"
                        )]
                    ),
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b90fb8504a2f9076a8db6d2658693f23e31a993bd6c28ebcc65999a2fbea5747)
                check_type(argname="argument action_on_failure", value=action_on_failure, expected_type=type_hints["action_on_failure"])
                check_type(argname="argument hadoop_jar_step", value=hadoop_jar_step, expected_type=type_hints["hadoop_jar_step"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action_on_failure is not None:
                self._values["action_on_failure"] = action_on_failure
            if hadoop_jar_step is not None:
                self._values["hadoop_jar_step"] = hadoop_jar_step
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def action_on_failure(self) -> typing.Optional[builtins.str]:
            '''The action to take when the cluster step fails.

            Possible values are ``CANCEL_AND_WAIT`` and ``CONTINUE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-stepconfig.html#cfn-emr-cluster-stepconfig-actiononfailure
            '''
            result = self._values.get("action_on_failure")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hadoop_jar_step(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.HadoopJarStepConfigProperty"]]:
            '''The JAR file used for the step.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-stepconfig.html#cfn-emr-cluster-stepconfig-hadoopjarstep
            '''
            result = self._values.get("hadoop_jar_step")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.HadoopJarStepConfigProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the step.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-stepconfig.html#cfn-emr-cluster-stepconfig-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StepConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnClusterPropsMixin.VolumeSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "iops": "iops",
            "size_in_gb": "sizeInGb",
            "throughput": "throughput",
            "volume_type": "volumeType",
        },
    )
    class VolumeSpecificationProperty:
        def __init__(
            self,
            *,
            iops: typing.Optional[jsii.Number] = None,
            size_in_gb: typing.Optional[jsii.Number] = None,
            throughput: typing.Optional[jsii.Number] = None,
            volume_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``VolumeSpecification`` is a subproperty of the ``EbsBlockDeviceConfig`` property type.

            ``VolumeSecification`` determines the volume type, IOPS, and size (GiB) for EBS volumes attached to EC2 instances.

            :param iops: The number of I/O operations per second (IOPS) that the volume supports.
            :param size_in_gb: The volume size, in gibibytes (GiB). This can be a number from 1 - 1024. If the volume type is EBS-optimized, the minimum value is 10.
            :param throughput: The throughput, in mebibyte per second (MiB/s). This optional parameter can be a number from 125 - 1000 and is valid only for gp3 volumes.
            :param volume_type: The volume type. Volume types supported are gp3, gp2, io1, st1, sc1, and standard.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-volumespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                volume_specification_property = emr_mixins.CfnClusterPropsMixin.VolumeSpecificationProperty(
                    iops=123,
                    size_in_gb=123,
                    throughput=123,
                    volume_type="volumeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__548f9410a6db8a31ba45e3c4453340916c5d37795c2ce9dd5c08e80281982f53)
                check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
                check_type(argname="argument size_in_gb", value=size_in_gb, expected_type=type_hints["size_in_gb"])
                check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
                check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iops is not None:
                self._values["iops"] = iops
            if size_in_gb is not None:
                self._values["size_in_gb"] = size_in_gb
            if throughput is not None:
                self._values["throughput"] = throughput
            if volume_type is not None:
                self._values["volume_type"] = volume_type

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            '''The number of I/O operations per second (IOPS) that the volume supports.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-volumespecification.html#cfn-emr-cluster-volumespecification-iops
            '''
            result = self._values.get("iops")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def size_in_gb(self) -> typing.Optional[jsii.Number]:
            '''The volume size, in gibibytes (GiB).

            This can be a number from 1 - 1024. If the volume type is EBS-optimized, the minimum value is 10.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-volumespecification.html#cfn-emr-cluster-volumespecification-sizeingb
            '''
            result = self._values.get("size_in_gb")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throughput(self) -> typing.Optional[jsii.Number]:
            '''The throughput, in mebibyte per second (MiB/s).

            This optional parameter can be a number from 125 - 1000 and is valid only for gp3 volumes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-volumespecification.html#cfn-emr-cluster-volumespecification-throughput
            '''
            result = self._values.get("throughput")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_type(self) -> typing.Optional[builtins.str]:
            '''The volume type.

            Volume types supported are gp3, gp2, io1, st1, sc1, and standard.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-cluster-volumespecification.html#cfn-emr-cluster-volumespecification-volumetype
            '''
            result = self._values.get("volume_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VolumeSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceFleetConfigMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_id": "clusterId",
        "instance_fleet_type": "instanceFleetType",
        "instance_type_configs": "instanceTypeConfigs",
        "launch_specifications": "launchSpecifications",
        "name": "name",
        "resize_specifications": "resizeSpecifications",
        "target_on_demand_capacity": "targetOnDemandCapacity",
        "target_spot_capacity": "targetSpotCapacity",
    },
)
class CfnInstanceFleetConfigMixinProps:
    def __init__(
        self,
        *,
        cluster_id: typing.Optional[builtins.str] = None,
        instance_fleet_type: typing.Optional[builtins.str] = None,
        instance_type_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceFleetConfigPropsMixin.InstanceTypeConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        launch_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceFleetConfigPropsMixin.InstanceFleetProvisioningSpecificationsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        resize_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceFleetConfigPropsMixin.InstanceFleetResizingSpecificationsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        target_on_demand_capacity: typing.Optional[jsii.Number] = None,
        target_spot_capacity: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnInstanceFleetConfigPropsMixin.

        :param cluster_id: The unique identifier of the EMR cluster.
        :param instance_fleet_type: The node type that the instance fleet hosts. *Allowed Values* : TASK
        :param instance_type_configs: ``InstanceTypeConfigs`` determine the EC2 instances that Amazon EMR attempts to provision to fulfill On-Demand and Spot target capacities. .. epigraph:: The instance fleet configuration is available only in Amazon EMR versions 4.8.0 and later, excluding 5.0.x versions.
        :param launch_specifications: The launch specification for the instance fleet.
        :param name: The friendly name of the instance fleet.
        :param resize_specifications: The resize specification for the instance fleet.
        :param target_on_demand_capacity: The target capacity of On-Demand units for the instance fleet, which determines how many On-Demand instances to provision. When the instance fleet launches, Amazon EMR tries to provision On-Demand instances as specified by ``InstanceTypeConfig`` . Each instance configuration has a specified ``WeightedCapacity`` . When an On-Demand instance is provisioned, the ``WeightedCapacity`` units count toward the target capacity. Amazon EMR provisions instances until the target capacity is totally fulfilled, even if this results in an overage. For example, if there are 2 units remaining to fulfill capacity, and Amazon EMR can only provision an instance with a ``WeightedCapacity`` of 5 units, the instance is provisioned, and the target capacity is exceeded by 3 units. .. epigraph:: If not specified or set to 0, only Spot instances are provisioned for the instance fleet using ``TargetSpotCapacity`` . At least one of ``TargetSpotCapacity`` and ``TargetOnDemandCapacity`` should be greater than 0. For a master instance fleet, only one of ``TargetSpotCapacity`` and ``TargetOnDemandCapacity`` can be specified, and its value must be 1.
        :param target_spot_capacity: The target capacity of Spot units for the instance fleet, which determines how many Spot instances to provision. When the instance fleet launches, Amazon EMR tries to provision Spot instances as specified by ``InstanceTypeConfig`` . Each instance configuration has a specified ``WeightedCapacity`` . When a Spot instance is provisioned, the ``WeightedCapacity`` units count toward the target capacity. Amazon EMR provisions instances until the target capacity is totally fulfilled, even if this results in an overage. For example, if there are 2 units remaining to fulfill capacity, and Amazon EMR can only provision an instance with a ``WeightedCapacity`` of 5 units, the instance is provisioned, and the target capacity is exceeded by 3 units. .. epigraph:: If not specified or set to 0, only On-Demand instances are provisioned for the instance fleet. At least one of ``TargetSpotCapacity`` and ``TargetOnDemandCapacity`` should be greater than 0. For a master instance fleet, only one of ``TargetSpotCapacity`` and ``TargetOnDemandCapacity`` can be specified, and its value must be 1.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancefleetconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
            
            # configuration_property_: emr_mixins.CfnInstanceFleetConfigPropsMixin.ConfigurationProperty
            
            cfn_instance_fleet_config_mixin_props = emr_mixins.CfnInstanceFleetConfigMixinProps(
                cluster_id="clusterId",
                instance_fleet_type="instanceFleetType",
                instance_type_configs=[emr_mixins.CfnInstanceFleetConfigPropsMixin.InstanceTypeConfigProperty(
                    bid_price="bidPrice",
                    bid_price_as_percentage_of_on_demand_price=123,
                    configurations=[emr_mixins.CfnInstanceFleetConfigPropsMixin.ConfigurationProperty(
                        classification="classification",
                        configuration_properties={
                            "configuration_properties_key": "configurationProperties"
                        },
                        configurations=[configuration_property_]
                    )],
                    custom_ami_id="customAmiId",
                    ebs_configuration=emr_mixins.CfnInstanceFleetConfigPropsMixin.EbsConfigurationProperty(
                        ebs_block_device_configs=[emr_mixins.CfnInstanceFleetConfigPropsMixin.EbsBlockDeviceConfigProperty(
                            volume_specification=emr_mixins.CfnInstanceFleetConfigPropsMixin.VolumeSpecificationProperty(
                                iops=123,
                                size_in_gb=123,
                                throughput=123,
                                volume_type="volumeType"
                            ),
                            volumes_per_instance=123
                        )],
                        ebs_optimized=False
                    ),
                    instance_type="instanceType",
                    priority=123,
                    weighted_capacity=123
                )],
                launch_specifications=emr_mixins.CfnInstanceFleetConfigPropsMixin.InstanceFleetProvisioningSpecificationsProperty(
                    on_demand_specification=emr_mixins.CfnInstanceFleetConfigPropsMixin.OnDemandProvisioningSpecificationProperty(
                        allocation_strategy="allocationStrategy",
                        capacity_reservation_options=emr_mixins.CfnInstanceFleetConfigPropsMixin.OnDemandCapacityReservationOptionsProperty(
                            capacity_reservation_preference="capacityReservationPreference",
                            capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                            usage_strategy="usageStrategy"
                        )
                    ),
                    spot_specification=emr_mixins.CfnInstanceFleetConfigPropsMixin.SpotProvisioningSpecificationProperty(
                        allocation_strategy="allocationStrategy",
                        block_duration_minutes=123,
                        timeout_action="timeoutAction",
                        timeout_duration_minutes=123
                    )
                ),
                name="name",
                resize_specifications=emr_mixins.CfnInstanceFleetConfigPropsMixin.InstanceFleetResizingSpecificationsProperty(
                    on_demand_resize_specification=emr_mixins.CfnInstanceFleetConfigPropsMixin.OnDemandResizingSpecificationProperty(
                        allocation_strategy="allocationStrategy",
                        capacity_reservation_options=emr_mixins.CfnInstanceFleetConfigPropsMixin.OnDemandCapacityReservationOptionsProperty(
                            capacity_reservation_preference="capacityReservationPreference",
                            capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                            usage_strategy="usageStrategy"
                        ),
                        timeout_duration_minutes=123
                    ),
                    spot_resize_specification=emr_mixins.CfnInstanceFleetConfigPropsMixin.SpotResizingSpecificationProperty(
                        allocation_strategy="allocationStrategy",
                        timeout_duration_minutes=123
                    )
                ),
                target_on_demand_capacity=123,
                target_spot_capacity=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c25525f13258292b10717b73e94026e2c3e0657c443840ca5048bcbf5a463109)
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument instance_fleet_type", value=instance_fleet_type, expected_type=type_hints["instance_fleet_type"])
            check_type(argname="argument instance_type_configs", value=instance_type_configs, expected_type=type_hints["instance_type_configs"])
            check_type(argname="argument launch_specifications", value=launch_specifications, expected_type=type_hints["launch_specifications"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resize_specifications", value=resize_specifications, expected_type=type_hints["resize_specifications"])
            check_type(argname="argument target_on_demand_capacity", value=target_on_demand_capacity, expected_type=type_hints["target_on_demand_capacity"])
            check_type(argname="argument target_spot_capacity", value=target_spot_capacity, expected_type=type_hints["target_spot_capacity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster_id is not None:
            self._values["cluster_id"] = cluster_id
        if instance_fleet_type is not None:
            self._values["instance_fleet_type"] = instance_fleet_type
        if instance_type_configs is not None:
            self._values["instance_type_configs"] = instance_type_configs
        if launch_specifications is not None:
            self._values["launch_specifications"] = launch_specifications
        if name is not None:
            self._values["name"] = name
        if resize_specifications is not None:
            self._values["resize_specifications"] = resize_specifications
        if target_on_demand_capacity is not None:
            self._values["target_on_demand_capacity"] = target_on_demand_capacity
        if target_spot_capacity is not None:
            self._values["target_spot_capacity"] = target_spot_capacity

    @builtins.property
    def cluster_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the EMR cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancefleetconfig.html#cfn-emr-instancefleetconfig-clusterid
        '''
        result = self._values.get("cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_fleet_type(self) -> typing.Optional[builtins.str]:
        '''The node type that the instance fleet hosts.

        *Allowed Values* : TASK

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancefleetconfig.html#cfn-emr-instancefleetconfig-instancefleettype
        '''
        result = self._values.get("instance_fleet_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type_configs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.InstanceTypeConfigProperty"]]]]:
        '''``InstanceTypeConfigs`` determine the EC2 instances that Amazon EMR attempts to provision to fulfill On-Demand and Spot target capacities.

        .. epigraph::

           The instance fleet configuration is available only in Amazon EMR versions 4.8.0 and later, excluding 5.0.x versions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancefleetconfig.html#cfn-emr-instancefleetconfig-instancetypeconfigs
        '''
        result = self._values.get("instance_type_configs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.InstanceTypeConfigProperty"]]]], result)

    @builtins.property
    def launch_specifications(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.InstanceFleetProvisioningSpecificationsProperty"]]:
        '''The launch specification for the instance fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancefleetconfig.html#cfn-emr-instancefleetconfig-launchspecifications
        '''
        result = self._values.get("launch_specifications")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.InstanceFleetProvisioningSpecificationsProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The friendly name of the instance fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancefleetconfig.html#cfn-emr-instancefleetconfig-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resize_specifications(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.InstanceFleetResizingSpecificationsProperty"]]:
        '''The resize specification for the instance fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancefleetconfig.html#cfn-emr-instancefleetconfig-resizespecifications
        '''
        result = self._values.get("resize_specifications")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.InstanceFleetResizingSpecificationsProperty"]], result)

    @builtins.property
    def target_on_demand_capacity(self) -> typing.Optional[jsii.Number]:
        '''The target capacity of On-Demand units for the instance fleet, which determines how many On-Demand instances to provision.

        When the instance fleet launches, Amazon EMR tries to provision On-Demand instances as specified by ``InstanceTypeConfig`` . Each instance configuration has a specified ``WeightedCapacity`` . When an On-Demand instance is provisioned, the ``WeightedCapacity`` units count toward the target capacity. Amazon EMR provisions instances until the target capacity is totally fulfilled, even if this results in an overage. For example, if there are 2 units remaining to fulfill capacity, and Amazon EMR can only provision an instance with a ``WeightedCapacity`` of 5 units, the instance is provisioned, and the target capacity is exceeded by 3 units.
        .. epigraph::

           If not specified or set to 0, only Spot instances are provisioned for the instance fleet using ``TargetSpotCapacity`` . At least one of ``TargetSpotCapacity`` and ``TargetOnDemandCapacity`` should be greater than 0. For a master instance fleet, only one of ``TargetSpotCapacity`` and ``TargetOnDemandCapacity`` can be specified, and its value must be 1.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancefleetconfig.html#cfn-emr-instancefleetconfig-targetondemandcapacity
        '''
        result = self._values.get("target_on_demand_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_spot_capacity(self) -> typing.Optional[jsii.Number]:
        '''The target capacity of Spot units for the instance fleet, which determines how many Spot instances to provision.

        When the instance fleet launches, Amazon EMR tries to provision Spot instances as specified by ``InstanceTypeConfig`` . Each instance configuration has a specified ``WeightedCapacity`` . When a Spot instance is provisioned, the ``WeightedCapacity`` units count toward the target capacity. Amazon EMR provisions instances until the target capacity is totally fulfilled, even if this results in an overage. For example, if there are 2 units remaining to fulfill capacity, and Amazon EMR can only provision an instance with a ``WeightedCapacity`` of 5 units, the instance is provisioned, and the target capacity is exceeded by 3 units.
        .. epigraph::

           If not specified or set to 0, only On-Demand instances are provisioned for the instance fleet. At least one of ``TargetSpotCapacity`` and ``TargetOnDemandCapacity`` should be greater than 0. For a master instance fleet, only one of ``TargetSpotCapacity`` and ``TargetOnDemandCapacity`` can be specified, and its value must be 1.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancefleetconfig.html#cfn-emr-instancefleetconfig-targetspotcapacity
        '''
        result = self._values.get("target_spot_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceFleetConfigMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInstanceFleetConfigPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceFleetConfigPropsMixin",
):
    '''Use ``InstanceFleetConfig`` to define instance fleets for an EMR cluster.

    A cluster can not use both instance fleets and instance groups. For more information, see `Configure Instance Fleets <https://docs.aws.amazon.com//emr/latest/ManagementGuide/emr-instance-group-configuration.html>`_ in the *Amazon EMR Management Guide* .
    .. epigraph::

       The instance fleet configuration is available only in Amazon EMR versions 4.8.0 and later, excluding 5.0.x versions. > You can currently only add a task instance fleet to a cluster with this resource. If you use this resource, CloudFormation waits for the cluster launch to complete before adding the task instance fleet to the cluster. In order to add a task instance fleet to the cluster as part of the cluster launch and minimize delays in provisioning task nodes, use the ``TaskInstanceFleets`` subproperty for the `AWS::EMR::Cluster JobFlowInstancesConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticmapreduce-cluster-jobflowinstancesconfig.html>`_ property instead. To use this subproperty, see `AWS::EMR::Cluster <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticmapreduce-cluster.html>`_ for examples.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancefleetconfig.html
    :cloudformationResource: AWS::EMR::InstanceFleetConfig
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
        
        # configuration_property_: emr_mixins.CfnInstanceFleetConfigPropsMixin.ConfigurationProperty
        
        cfn_instance_fleet_config_props_mixin = emr_mixins.CfnInstanceFleetConfigPropsMixin(emr_mixins.CfnInstanceFleetConfigMixinProps(
            cluster_id="clusterId",
            instance_fleet_type="instanceFleetType",
            instance_type_configs=[emr_mixins.CfnInstanceFleetConfigPropsMixin.InstanceTypeConfigProperty(
                bid_price="bidPrice",
                bid_price_as_percentage_of_on_demand_price=123,
                configurations=[emr_mixins.CfnInstanceFleetConfigPropsMixin.ConfigurationProperty(
                    classification="classification",
                    configuration_properties={
                        "configuration_properties_key": "configurationProperties"
                    },
                    configurations=[configuration_property_]
                )],
                custom_ami_id="customAmiId",
                ebs_configuration=emr_mixins.CfnInstanceFleetConfigPropsMixin.EbsConfigurationProperty(
                    ebs_block_device_configs=[emr_mixins.CfnInstanceFleetConfigPropsMixin.EbsBlockDeviceConfigProperty(
                        volume_specification=emr_mixins.CfnInstanceFleetConfigPropsMixin.VolumeSpecificationProperty(
                            iops=123,
                            size_in_gb=123,
                            throughput=123,
                            volume_type="volumeType"
                        ),
                        volumes_per_instance=123
                    )],
                    ebs_optimized=False
                ),
                instance_type="instanceType",
                priority=123,
                weighted_capacity=123
            )],
            launch_specifications=emr_mixins.CfnInstanceFleetConfigPropsMixin.InstanceFleetProvisioningSpecificationsProperty(
                on_demand_specification=emr_mixins.CfnInstanceFleetConfigPropsMixin.OnDemandProvisioningSpecificationProperty(
                    allocation_strategy="allocationStrategy",
                    capacity_reservation_options=emr_mixins.CfnInstanceFleetConfigPropsMixin.OnDemandCapacityReservationOptionsProperty(
                        capacity_reservation_preference="capacityReservationPreference",
                        capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                        usage_strategy="usageStrategy"
                    )
                ),
                spot_specification=emr_mixins.CfnInstanceFleetConfigPropsMixin.SpotProvisioningSpecificationProperty(
                    allocation_strategy="allocationStrategy",
                    block_duration_minutes=123,
                    timeout_action="timeoutAction",
                    timeout_duration_minutes=123
                )
            ),
            name="name",
            resize_specifications=emr_mixins.CfnInstanceFleetConfigPropsMixin.InstanceFleetResizingSpecificationsProperty(
                on_demand_resize_specification=emr_mixins.CfnInstanceFleetConfigPropsMixin.OnDemandResizingSpecificationProperty(
                    allocation_strategy="allocationStrategy",
                    capacity_reservation_options=emr_mixins.CfnInstanceFleetConfigPropsMixin.OnDemandCapacityReservationOptionsProperty(
                        capacity_reservation_preference="capacityReservationPreference",
                        capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                        usage_strategy="usageStrategy"
                    ),
                    timeout_duration_minutes=123
                ),
                spot_resize_specification=emr_mixins.CfnInstanceFleetConfigPropsMixin.SpotResizingSpecificationProperty(
                    allocation_strategy="allocationStrategy",
                    timeout_duration_minutes=123
                )
            ),
            target_on_demand_capacity=123,
            target_spot_capacity=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnInstanceFleetConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EMR::InstanceFleetConfig``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f0ec28349b2ee19965a9604a8ada1f2012aa21ed0e93123b7a049430ca3da3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__947f608159942e74bf5016e3d20e0b3816207dbab55fe44b11ab18c3c1d98e69)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8903b94c1f045f2ead59b1d8ed169e859fee49d94b2416f5dfb8aee5efb5e452)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInstanceFleetConfigMixinProps:
        return typing.cast(CfnInstanceFleetConfigMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceFleetConfigPropsMixin.ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "classification": "classification",
            "configuration_properties": "configurationProperties",
            "configurations": "configurations",
        },
    )
    class ConfigurationProperty:
        def __init__(
            self,
            *,
            classification: typing.Optional[builtins.str] = None,
            configuration_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceFleetConfigPropsMixin.ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''.. epigraph::

   Used only with Amazon EMR release 4.0 and later.

            ``Configuration`` specifies optional configurations for customizing open-source big data applications and environment parameters. A configuration consists of a classification, properties, and optional nested configurations. A classification refers to an application-specific configuration file. Properties are the settings you want to change in that file. For more information, see `Configuring Applications <https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-configure-apps.html>`_ in the *Amazon EMR Release Guide* .

            :param classification: The classification within a configuration.
            :param configuration_properties: Within a configuration classification, a set of properties that represent the settings that you want to change in the configuration file. Duplicates not allowed.
            :param configurations: A list of additional configurations to apply within a configuration object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                # configuration_property_: emr_mixins.CfnInstanceFleetConfigPropsMixin.ConfigurationProperty
                
                configuration_property = emr_mixins.CfnInstanceFleetConfigPropsMixin.ConfigurationProperty(
                    classification="classification",
                    configuration_properties={
                        "configuration_properties_key": "configurationProperties"
                    },
                    configurations=[configuration_property_]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__98c958fa2feee31edf1e79d2fb97e23c9b01fd5b4327969feee13644a4786bd3)
                check_type(argname="argument classification", value=classification, expected_type=type_hints["classification"])
                check_type(argname="argument configuration_properties", value=configuration_properties, expected_type=type_hints["configuration_properties"])
                check_type(argname="argument configurations", value=configurations, expected_type=type_hints["configurations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if classification is not None:
                self._values["classification"] = classification
            if configuration_properties is not None:
                self._values["configuration_properties"] = configuration_properties
            if configurations is not None:
                self._values["configurations"] = configurations

        @builtins.property
        def classification(self) -> typing.Optional[builtins.str]:
            '''The classification within a configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-configuration.html#cfn-emr-instancefleetconfig-configuration-classification
            '''
            result = self._values.get("classification")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def configuration_properties(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Within a configuration classification, a set of properties that represent the settings that you want to change in the configuration file.

            Duplicates not allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-configuration.html#cfn-emr-instancefleetconfig-configuration-configurationproperties
            '''
            result = self._values.get("configuration_properties")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.ConfigurationProperty"]]]]:
            '''A list of additional configurations to apply within a configuration object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-configuration.html#cfn-emr-instancefleetconfig-configuration-configurations
            '''
            result = self._values.get("configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.ConfigurationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceFleetConfigPropsMixin.EbsBlockDeviceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "volume_specification": "volumeSpecification",
            "volumes_per_instance": "volumesPerInstance",
        },
    )
    class EbsBlockDeviceConfigProperty:
        def __init__(
            self,
            *,
            volume_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceFleetConfigPropsMixin.VolumeSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            volumes_per_instance: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``EbsBlockDeviceConfig`` is a subproperty of the ``EbsConfiguration`` property type.

            ``EbsBlockDeviceConfig`` defines the number and type of EBS volumes to associate with all EC2 instances in an EMR cluster.

            :param volume_specification: EBS volume specifications such as volume type, IOPS, size (GiB) and throughput (MiB/s) that are requested for the EBS volume attached to an Amazon EC2 instance in the cluster.
            :param volumes_per_instance: Number of EBS volumes with a specific volume configuration that are associated with every instance in the instance group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-ebsblockdeviceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                ebs_block_device_config_property = emr_mixins.CfnInstanceFleetConfigPropsMixin.EbsBlockDeviceConfigProperty(
                    volume_specification=emr_mixins.CfnInstanceFleetConfigPropsMixin.VolumeSpecificationProperty(
                        iops=123,
                        size_in_gb=123,
                        throughput=123,
                        volume_type="volumeType"
                    ),
                    volumes_per_instance=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__50c60c231d36473e20ef16bd809b04a6886f4cab7a24774958d0ca2da7ab728a)
                check_type(argname="argument volume_specification", value=volume_specification, expected_type=type_hints["volume_specification"])
                check_type(argname="argument volumes_per_instance", value=volumes_per_instance, expected_type=type_hints["volumes_per_instance"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if volume_specification is not None:
                self._values["volume_specification"] = volume_specification
            if volumes_per_instance is not None:
                self._values["volumes_per_instance"] = volumes_per_instance

        @builtins.property
        def volume_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.VolumeSpecificationProperty"]]:
            '''EBS volume specifications such as volume type, IOPS, size (GiB) and throughput (MiB/s) that are requested for the EBS volume attached to an Amazon EC2 instance in the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-ebsblockdeviceconfig.html#cfn-emr-instancefleetconfig-ebsblockdeviceconfig-volumespecification
            '''
            result = self._values.get("volume_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.VolumeSpecificationProperty"]], result)

        @builtins.property
        def volumes_per_instance(self) -> typing.Optional[jsii.Number]:
            '''Number of EBS volumes with a specific volume configuration that are associated with every instance in the instance group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-ebsblockdeviceconfig.html#cfn-emr-instancefleetconfig-ebsblockdeviceconfig-volumesperinstance
            '''
            result = self._values.get("volumes_per_instance")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EbsBlockDeviceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceFleetConfigPropsMixin.EbsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ebs_block_device_configs": "ebsBlockDeviceConfigs",
            "ebs_optimized": "ebsOptimized",
        },
    )
    class EbsConfigurationProperty:
        def __init__(
            self,
            *,
            ebs_block_device_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceFleetConfigPropsMixin.EbsBlockDeviceConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ebs_optimized: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''``EbsConfiguration`` determines the EBS volumes to attach to EMR cluster instances.

            :param ebs_block_device_configs: An array of Amazon EBS volume specifications attached to a cluster instance.
            :param ebs_optimized: Indicates whether an Amazon EBS volume is EBS-optimized. The default is false. You should explicitly set this value to true to enable the Amazon EBS-optimized setting for an EC2 instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-ebsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                ebs_configuration_property = emr_mixins.CfnInstanceFleetConfigPropsMixin.EbsConfigurationProperty(
                    ebs_block_device_configs=[emr_mixins.CfnInstanceFleetConfigPropsMixin.EbsBlockDeviceConfigProperty(
                        volume_specification=emr_mixins.CfnInstanceFleetConfigPropsMixin.VolumeSpecificationProperty(
                            iops=123,
                            size_in_gb=123,
                            throughput=123,
                            volume_type="volumeType"
                        ),
                        volumes_per_instance=123
                    )],
                    ebs_optimized=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__007ef7f5ed2b35f010821e909137e24ca02ab286af64ec07c7fb8e08f74b14aa)
                check_type(argname="argument ebs_block_device_configs", value=ebs_block_device_configs, expected_type=type_hints["ebs_block_device_configs"])
                check_type(argname="argument ebs_optimized", value=ebs_optimized, expected_type=type_hints["ebs_optimized"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ebs_block_device_configs is not None:
                self._values["ebs_block_device_configs"] = ebs_block_device_configs
            if ebs_optimized is not None:
                self._values["ebs_optimized"] = ebs_optimized

        @builtins.property
        def ebs_block_device_configs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.EbsBlockDeviceConfigProperty"]]]]:
            '''An array of Amazon EBS volume specifications attached to a cluster instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-ebsconfiguration.html#cfn-emr-instancefleetconfig-ebsconfiguration-ebsblockdeviceconfigs
            '''
            result = self._values.get("ebs_block_device_configs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.EbsBlockDeviceConfigProperty"]]]], result)

        @builtins.property
        def ebs_optimized(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether an Amazon EBS volume is EBS-optimized.

            The default is false. You should explicitly set this value to true to enable the Amazon EBS-optimized setting for an EC2 instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-ebsconfiguration.html#cfn-emr-instancefleetconfig-ebsconfiguration-ebsoptimized
            '''
            result = self._values.get("ebs_optimized")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EbsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceFleetConfigPropsMixin.InstanceFleetProvisioningSpecificationsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "on_demand_specification": "onDemandSpecification",
            "spot_specification": "spotSpecification",
        },
    )
    class InstanceFleetProvisioningSpecificationsProperty:
        def __init__(
            self,
            *,
            on_demand_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceFleetConfigPropsMixin.OnDemandProvisioningSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            spot_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceFleetConfigPropsMixin.SpotProvisioningSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''.. epigraph::

   The instance fleet configuration is available only in Amazon EMR versions 4.8.0 and later, excluding 5.0.x versions.

            ``InstanceTypeConfig`` is a sub-property of ``InstanceFleetConfig`` . ``InstanceTypeConfig`` determines the EC2 instances that Amazon EMR attempts to provision to fulfill On-Demand and Spot target capacities.

            :param on_demand_specification: The launch specification for On-Demand Instances in the instance fleet, which determines the allocation strategy and capacity reservation options. .. epigraph:: The instance fleet configuration is available only in Amazon EMR releases 4.8.0 and later, excluding 5.0.x versions. On-Demand Instances allocation strategy is available in Amazon EMR releases 5.12.1 and later.
            :param spot_specification: The launch specification for Spot instances in the fleet, which determines the allocation strategy, defined duration, and provisioning timeout behavior.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-instancefleetprovisioningspecifications.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                instance_fleet_provisioning_specifications_property = emr_mixins.CfnInstanceFleetConfigPropsMixin.InstanceFleetProvisioningSpecificationsProperty(
                    on_demand_specification=emr_mixins.CfnInstanceFleetConfigPropsMixin.OnDemandProvisioningSpecificationProperty(
                        allocation_strategy="allocationStrategy",
                        capacity_reservation_options=emr_mixins.CfnInstanceFleetConfigPropsMixin.OnDemandCapacityReservationOptionsProperty(
                            capacity_reservation_preference="capacityReservationPreference",
                            capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                            usage_strategy="usageStrategy"
                        )
                    ),
                    spot_specification=emr_mixins.CfnInstanceFleetConfigPropsMixin.SpotProvisioningSpecificationProperty(
                        allocation_strategy="allocationStrategy",
                        block_duration_minutes=123,
                        timeout_action="timeoutAction",
                        timeout_duration_minutes=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__824a305f1337655b9890ad64259308c6cc91d484ce19d5340fdd3ebd65c4d238)
                check_type(argname="argument on_demand_specification", value=on_demand_specification, expected_type=type_hints["on_demand_specification"])
                check_type(argname="argument spot_specification", value=spot_specification, expected_type=type_hints["spot_specification"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if on_demand_specification is not None:
                self._values["on_demand_specification"] = on_demand_specification
            if spot_specification is not None:
                self._values["spot_specification"] = spot_specification

        @builtins.property
        def on_demand_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.OnDemandProvisioningSpecificationProperty"]]:
            '''The launch specification for On-Demand Instances in the instance fleet, which determines the allocation strategy and capacity reservation options.

            .. epigraph::

               The instance fleet configuration is available only in Amazon EMR releases 4.8.0 and later, excluding 5.0.x versions. On-Demand Instances allocation strategy is available in Amazon EMR releases 5.12.1 and later.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-instancefleetprovisioningspecifications.html#cfn-emr-instancefleetconfig-instancefleetprovisioningspecifications-ondemandspecification
            '''
            result = self._values.get("on_demand_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.OnDemandProvisioningSpecificationProperty"]], result)

        @builtins.property
        def spot_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.SpotProvisioningSpecificationProperty"]]:
            '''The launch specification for Spot instances in the fleet, which determines the allocation strategy, defined duration, and provisioning timeout behavior.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-instancefleetprovisioningspecifications.html#cfn-emr-instancefleetconfig-instancefleetprovisioningspecifications-spotspecification
            '''
            result = self._values.get("spot_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.SpotProvisioningSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceFleetProvisioningSpecificationsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceFleetConfigPropsMixin.InstanceFleetResizingSpecificationsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "on_demand_resize_specification": "onDemandResizeSpecification",
            "spot_resize_specification": "spotResizeSpecification",
        },
    )
    class InstanceFleetResizingSpecificationsProperty:
        def __init__(
            self,
            *,
            on_demand_resize_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceFleetConfigPropsMixin.OnDemandResizingSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            spot_resize_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceFleetConfigPropsMixin.SpotResizingSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The resize specification for On-Demand and Spot Instances in the fleet.

            :param on_demand_resize_specification: The resize specification for On-Demand Instances in the instance fleet, which contains the allocation strategy, capacity reservation options, and the resize timeout period.
            :param spot_resize_specification: The resize specification for Spot Instances in the instance fleet, which contains the allocation strategy and the resize timeout period.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-instancefleetresizingspecifications.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                instance_fleet_resizing_specifications_property = emr_mixins.CfnInstanceFleetConfigPropsMixin.InstanceFleetResizingSpecificationsProperty(
                    on_demand_resize_specification=emr_mixins.CfnInstanceFleetConfigPropsMixin.OnDemandResizingSpecificationProperty(
                        allocation_strategy="allocationStrategy",
                        capacity_reservation_options=emr_mixins.CfnInstanceFleetConfigPropsMixin.OnDemandCapacityReservationOptionsProperty(
                            capacity_reservation_preference="capacityReservationPreference",
                            capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                            usage_strategy="usageStrategy"
                        ),
                        timeout_duration_minutes=123
                    ),
                    spot_resize_specification=emr_mixins.CfnInstanceFleetConfigPropsMixin.SpotResizingSpecificationProperty(
                        allocation_strategy="allocationStrategy",
                        timeout_duration_minutes=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f8131c3271f9372ca290fcdd039df1ec9d6b7507aedefd7b337123aaa6ec0ae2)
                check_type(argname="argument on_demand_resize_specification", value=on_demand_resize_specification, expected_type=type_hints["on_demand_resize_specification"])
                check_type(argname="argument spot_resize_specification", value=spot_resize_specification, expected_type=type_hints["spot_resize_specification"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if on_demand_resize_specification is not None:
                self._values["on_demand_resize_specification"] = on_demand_resize_specification
            if spot_resize_specification is not None:
                self._values["spot_resize_specification"] = spot_resize_specification

        @builtins.property
        def on_demand_resize_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.OnDemandResizingSpecificationProperty"]]:
            '''The resize specification for On-Demand Instances in the instance fleet, which contains the allocation strategy, capacity reservation options, and the resize timeout period.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-instancefleetresizingspecifications.html#cfn-emr-instancefleetconfig-instancefleetresizingspecifications-ondemandresizespecification
            '''
            result = self._values.get("on_demand_resize_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.OnDemandResizingSpecificationProperty"]], result)

        @builtins.property
        def spot_resize_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.SpotResizingSpecificationProperty"]]:
            '''The resize specification for Spot Instances in the instance fleet, which contains the allocation strategy and the resize timeout period.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-instancefleetresizingspecifications.html#cfn-emr-instancefleetconfig-instancefleetresizingspecifications-spotresizespecification
            '''
            result = self._values.get("spot_resize_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.SpotResizingSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceFleetResizingSpecificationsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceFleetConfigPropsMixin.InstanceTypeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bid_price": "bidPrice",
            "bid_price_as_percentage_of_on_demand_price": "bidPriceAsPercentageOfOnDemandPrice",
            "configurations": "configurations",
            "custom_ami_id": "customAmiId",
            "ebs_configuration": "ebsConfiguration",
            "instance_type": "instanceType",
            "priority": "priority",
            "weighted_capacity": "weightedCapacity",
        },
    )
    class InstanceTypeConfigProperty:
        def __init__(
            self,
            *,
            bid_price: typing.Optional[builtins.str] = None,
            bid_price_as_percentage_of_on_demand_price: typing.Optional[jsii.Number] = None,
            configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceFleetConfigPropsMixin.ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            custom_ami_id: typing.Optional[builtins.str] = None,
            ebs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceFleetConfigPropsMixin.EbsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            instance_type: typing.Optional[builtins.str] = None,
            priority: typing.Optional[jsii.Number] = None,
            weighted_capacity: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``InstanceType`` config is a subproperty of ``InstanceFleetConfig`` .

            An instance type configuration specifies each instance type in an instance fleet. The configuration determines the EC2 instances Amazon EMR attempts to provision to fulfill On-Demand and Spot target capacities.
            .. epigraph::

               The instance fleet configuration is available only in Amazon EMR versions 4.8.0 and later, excluding 5.0.x versions.

            :param bid_price: The bid price for each Amazon EC2 Spot Instance type as defined by ``InstanceType`` . Expressed in USD. If neither ``BidPrice`` nor ``BidPriceAsPercentageOfOnDemandPrice`` is provided, ``BidPriceAsPercentageOfOnDemandPrice`` defaults to 100%.
            :param bid_price_as_percentage_of_on_demand_price: The bid price, as a percentage of On-Demand price, for each Amazon EC2 Spot Instance as defined by ``InstanceType`` . Expressed as a number (for example, 20 specifies 20%). If neither ``BidPrice`` nor ``BidPriceAsPercentageOfOnDemandPrice`` is provided, ``BidPriceAsPercentageOfOnDemandPrice`` defaults to 100%.
            :param configurations: .. epigraph:: Amazon EMR releases 4.x or later. An optional configuration specification to be used when provisioning cluster instances, which can include configurations for applications and software bundled with Amazon EMR. A configuration consists of a classification, properties, and optional nested configurations. A classification refers to an application-specific configuration file. Properties are the settings you want to change in that file. For more information, see `Configuring Applications <https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-configure-apps.html>`_ .
            :param custom_ami_id: The custom AMI ID to use for the instance type.
            :param ebs_configuration: The configuration of Amazon Elastic Block Store (Amazon EBS) attached to each instance as defined by ``InstanceType`` .
            :param instance_type: An Amazon EC2 instance type, such as ``m3.xlarge`` .
            :param priority: The priority at which Amazon EMR launches the Amazon EC2 instances with this instance type. Priority starts at 0, which is the highest priority. Amazon EMR considers the highest priority first.
            :param weighted_capacity: The number of units that a provisioned instance of this type provides toward fulfilling the target capacities defined in ``InstanceFleetConfig`` . This value is 1 for a master instance fleet, and must be 1 or greater for core and task instance fleets. Defaults to 1 if not specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-instancetypeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                # configuration_property_: emr_mixins.CfnInstanceFleetConfigPropsMixin.ConfigurationProperty
                
                instance_type_config_property = emr_mixins.CfnInstanceFleetConfigPropsMixin.InstanceTypeConfigProperty(
                    bid_price="bidPrice",
                    bid_price_as_percentage_of_on_demand_price=123,
                    configurations=[emr_mixins.CfnInstanceFleetConfigPropsMixin.ConfigurationProperty(
                        classification="classification",
                        configuration_properties={
                            "configuration_properties_key": "configurationProperties"
                        },
                        configurations=[configuration_property_]
                    )],
                    custom_ami_id="customAmiId",
                    ebs_configuration=emr_mixins.CfnInstanceFleetConfigPropsMixin.EbsConfigurationProperty(
                        ebs_block_device_configs=[emr_mixins.CfnInstanceFleetConfigPropsMixin.EbsBlockDeviceConfigProperty(
                            volume_specification=emr_mixins.CfnInstanceFleetConfigPropsMixin.VolumeSpecificationProperty(
                                iops=123,
                                size_in_gb=123,
                                throughput=123,
                                volume_type="volumeType"
                            ),
                            volumes_per_instance=123
                        )],
                        ebs_optimized=False
                    ),
                    instance_type="instanceType",
                    priority=123,
                    weighted_capacity=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e7aec96c366f7c1b79465405d41d777a0b59ae3a172afd754792e2bdfe5ecbab)
                check_type(argname="argument bid_price", value=bid_price, expected_type=type_hints["bid_price"])
                check_type(argname="argument bid_price_as_percentage_of_on_demand_price", value=bid_price_as_percentage_of_on_demand_price, expected_type=type_hints["bid_price_as_percentage_of_on_demand_price"])
                check_type(argname="argument configurations", value=configurations, expected_type=type_hints["configurations"])
                check_type(argname="argument custom_ami_id", value=custom_ami_id, expected_type=type_hints["custom_ami_id"])
                check_type(argname="argument ebs_configuration", value=ebs_configuration, expected_type=type_hints["ebs_configuration"])
                check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument weighted_capacity", value=weighted_capacity, expected_type=type_hints["weighted_capacity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bid_price is not None:
                self._values["bid_price"] = bid_price
            if bid_price_as_percentage_of_on_demand_price is not None:
                self._values["bid_price_as_percentage_of_on_demand_price"] = bid_price_as_percentage_of_on_demand_price
            if configurations is not None:
                self._values["configurations"] = configurations
            if custom_ami_id is not None:
                self._values["custom_ami_id"] = custom_ami_id
            if ebs_configuration is not None:
                self._values["ebs_configuration"] = ebs_configuration
            if instance_type is not None:
                self._values["instance_type"] = instance_type
            if priority is not None:
                self._values["priority"] = priority
            if weighted_capacity is not None:
                self._values["weighted_capacity"] = weighted_capacity

        @builtins.property
        def bid_price(self) -> typing.Optional[builtins.str]:
            '''The bid price for each Amazon EC2 Spot Instance type as defined by ``InstanceType`` .

            Expressed in USD. If neither ``BidPrice`` nor ``BidPriceAsPercentageOfOnDemandPrice`` is provided, ``BidPriceAsPercentageOfOnDemandPrice`` defaults to 100%.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-instancetypeconfig.html#cfn-emr-instancefleetconfig-instancetypeconfig-bidprice
            '''
            result = self._values.get("bid_price")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bid_price_as_percentage_of_on_demand_price(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''The bid price, as a percentage of On-Demand price, for each Amazon EC2 Spot Instance as defined by ``InstanceType`` .

            Expressed as a number (for example, 20 specifies 20%). If neither ``BidPrice`` nor ``BidPriceAsPercentageOfOnDemandPrice`` is provided, ``BidPriceAsPercentageOfOnDemandPrice`` defaults to 100%.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-instancetypeconfig.html#cfn-emr-instancefleetconfig-instancetypeconfig-bidpriceaspercentageofondemandprice
            '''
            result = self._values.get("bid_price_as_percentage_of_on_demand_price")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.ConfigurationProperty"]]]]:
            '''.. epigraph::

   Amazon EMR releases 4.x or later.

            An optional configuration specification to be used when provisioning cluster instances, which can include configurations for applications and software bundled with Amazon EMR. A configuration consists of a classification, properties, and optional nested configurations. A classification refers to an application-specific configuration file. Properties are the settings you want to change in that file. For more information, see `Configuring Applications <https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-configure-apps.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-instancetypeconfig.html#cfn-emr-instancefleetconfig-instancetypeconfig-configurations
            '''
            result = self._values.get("configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.ConfigurationProperty"]]]], result)

        @builtins.property
        def custom_ami_id(self) -> typing.Optional[builtins.str]:
            '''The custom AMI ID to use for the instance type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-instancetypeconfig.html#cfn-emr-instancefleetconfig-instancetypeconfig-customamiid
            '''
            result = self._values.get("custom_ami_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ebs_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.EbsConfigurationProperty"]]:
            '''The configuration of Amazon Elastic Block Store (Amazon EBS) attached to each instance as defined by ``InstanceType`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-instancetypeconfig.html#cfn-emr-instancefleetconfig-instancetypeconfig-ebsconfiguration
            '''
            result = self._values.get("ebs_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.EbsConfigurationProperty"]], result)

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            '''An Amazon EC2 instance type, such as ``m3.xlarge`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-instancetypeconfig.html#cfn-emr-instancefleetconfig-instancetypeconfig-instancetype
            '''
            result = self._values.get("instance_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            '''The priority at which Amazon EMR launches the Amazon EC2 instances with this instance type.

            Priority starts at 0, which is the highest priority. Amazon EMR considers the highest priority first.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-instancetypeconfig.html#cfn-emr-instancefleetconfig-instancetypeconfig-priority
            '''
            result = self._values.get("priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def weighted_capacity(self) -> typing.Optional[jsii.Number]:
            '''The number of units that a provisioned instance of this type provides toward fulfilling the target capacities defined in ``InstanceFleetConfig`` .

            This value is 1 for a master instance fleet, and must be 1 or greater for core and task instance fleets. Defaults to 1 if not specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-instancetypeconfig.html#cfn-emr-instancefleetconfig-instancetypeconfig-weightedcapacity
            '''
            result = self._values.get("weighted_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceTypeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceFleetConfigPropsMixin.OnDemandCapacityReservationOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capacity_reservation_preference": "capacityReservationPreference",
            "capacity_reservation_resource_group_arn": "capacityReservationResourceGroupArn",
            "usage_strategy": "usageStrategy",
        },
    )
    class OnDemandCapacityReservationOptionsProperty:
        def __init__(
            self,
            *,
            capacity_reservation_preference: typing.Optional[builtins.str] = None,
            capacity_reservation_resource_group_arn: typing.Optional[builtins.str] = None,
            usage_strategy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the strategy for using unused Capacity Reservations for fulfilling On-Demand capacity.

            :param capacity_reservation_preference: Indicates the instance's Capacity Reservation preferences. Possible preferences include:. - ``open`` - The instance can run in any open Capacity Reservation that has matching attributes (instance type, platform, Availability Zone). - ``none`` - The instance avoids running in a Capacity Reservation even if one is available. The instance runs as an On-Demand Instance.
            :param capacity_reservation_resource_group_arn: The ARN of the Capacity Reservation resource group in which to run the instance.
            :param usage_strategy: Indicates whether to use unused Capacity Reservations for fulfilling On-Demand capacity. If you specify ``use-capacity-reservations-first`` , the fleet uses unused Capacity Reservations to fulfill On-Demand capacity up to the target On-Demand capacity. If multiple instance pools have unused Capacity Reservations, the On-Demand allocation strategy ( ``lowest-price`` ) is applied. If the number of unused Capacity Reservations is less than the On-Demand target capacity, the remaining On-Demand target capacity is launched according to the On-Demand allocation strategy ( ``lowest-price`` ). If you do not specify a value, the fleet fulfills the On-Demand capacity according to the chosen On-Demand allocation strategy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-ondemandcapacityreservationoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                on_demand_capacity_reservation_options_property = emr_mixins.CfnInstanceFleetConfigPropsMixin.OnDemandCapacityReservationOptionsProperty(
                    capacity_reservation_preference="capacityReservationPreference",
                    capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                    usage_strategy="usageStrategy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a1779717221e0c46d662923457f1836ab9087ad798fd5a684975b725e2447c92)
                check_type(argname="argument capacity_reservation_preference", value=capacity_reservation_preference, expected_type=type_hints["capacity_reservation_preference"])
                check_type(argname="argument capacity_reservation_resource_group_arn", value=capacity_reservation_resource_group_arn, expected_type=type_hints["capacity_reservation_resource_group_arn"])
                check_type(argname="argument usage_strategy", value=usage_strategy, expected_type=type_hints["usage_strategy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capacity_reservation_preference is not None:
                self._values["capacity_reservation_preference"] = capacity_reservation_preference
            if capacity_reservation_resource_group_arn is not None:
                self._values["capacity_reservation_resource_group_arn"] = capacity_reservation_resource_group_arn
            if usage_strategy is not None:
                self._values["usage_strategy"] = usage_strategy

        @builtins.property
        def capacity_reservation_preference(self) -> typing.Optional[builtins.str]:
            '''Indicates the instance's Capacity Reservation preferences. Possible preferences include:.

            - ``open`` - The instance can run in any open Capacity Reservation that has matching attributes (instance type, platform, Availability Zone).
            - ``none`` - The instance avoids running in a Capacity Reservation even if one is available. The instance runs as an On-Demand Instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-ondemandcapacityreservationoptions.html#cfn-emr-instancefleetconfig-ondemandcapacityreservationoptions-capacityreservationpreference
            '''
            result = self._values.get("capacity_reservation_preference")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def capacity_reservation_resource_group_arn(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The ARN of the Capacity Reservation resource group in which to run the instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-ondemandcapacityreservationoptions.html#cfn-emr-instancefleetconfig-ondemandcapacityreservationoptions-capacityreservationresourcegrouparn
            '''
            result = self._values.get("capacity_reservation_resource_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def usage_strategy(self) -> typing.Optional[builtins.str]:
            '''Indicates whether to use unused Capacity Reservations for fulfilling On-Demand capacity.

            If you specify ``use-capacity-reservations-first`` , the fleet uses unused Capacity Reservations to fulfill On-Demand capacity up to the target On-Demand capacity. If multiple instance pools have unused Capacity Reservations, the On-Demand allocation strategy ( ``lowest-price`` ) is applied. If the number of unused Capacity Reservations is less than the On-Demand target capacity, the remaining On-Demand target capacity is launched according to the On-Demand allocation strategy ( ``lowest-price`` ).

            If you do not specify a value, the fleet fulfills the On-Demand capacity according to the chosen On-Demand allocation strategy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-ondemandcapacityreservationoptions.html#cfn-emr-instancefleetconfig-ondemandcapacityreservationoptions-usagestrategy
            '''
            result = self._values.get("usage_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnDemandCapacityReservationOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceFleetConfigPropsMixin.OnDemandProvisioningSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allocation_strategy": "allocationStrategy",
            "capacity_reservation_options": "capacityReservationOptions",
        },
    )
    class OnDemandProvisioningSpecificationProperty:
        def __init__(
            self,
            *,
            allocation_strategy: typing.Optional[builtins.str] = None,
            capacity_reservation_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceFleetConfigPropsMixin.OnDemandCapacityReservationOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The launch specification for On-Demand Instances in the instance fleet, which determines the allocation strategy.

            .. epigraph::

               The instance fleet configuration is available only in Amazon EMR releases 4.8.0 and later, excluding 5.0.x versions. On-Demand Instances allocation strategy is available in Amazon EMR releases 5.12.1 and later.

            :param allocation_strategy: Specifies the strategy to use in launching On-Demand instance fleets. Available options are ``lowest-price`` and ``prioritized`` . ``lowest-price`` specifies to launch the instances with the lowest price first, and ``prioritized`` specifies that Amazon EMR should launch the instances with the highest priority first. The default is ``lowest-price`` .
            :param capacity_reservation_options: The launch specification for On-Demand instances in the instance fleet, which determines the allocation strategy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-ondemandprovisioningspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                on_demand_provisioning_specification_property = emr_mixins.CfnInstanceFleetConfigPropsMixin.OnDemandProvisioningSpecificationProperty(
                    allocation_strategy="allocationStrategy",
                    capacity_reservation_options=emr_mixins.CfnInstanceFleetConfigPropsMixin.OnDemandCapacityReservationOptionsProperty(
                        capacity_reservation_preference="capacityReservationPreference",
                        capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                        usage_strategy="usageStrategy"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__454db275cf78fd0ed8afc77f5e22d73a576e6f5a6e4c1d6dc62163c6f810f2a8)
                check_type(argname="argument allocation_strategy", value=allocation_strategy, expected_type=type_hints["allocation_strategy"])
                check_type(argname="argument capacity_reservation_options", value=capacity_reservation_options, expected_type=type_hints["capacity_reservation_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allocation_strategy is not None:
                self._values["allocation_strategy"] = allocation_strategy
            if capacity_reservation_options is not None:
                self._values["capacity_reservation_options"] = capacity_reservation_options

        @builtins.property
        def allocation_strategy(self) -> typing.Optional[builtins.str]:
            '''Specifies the strategy to use in launching On-Demand instance fleets.

            Available options are ``lowest-price`` and ``prioritized`` . ``lowest-price`` specifies to launch the instances with the lowest price first, and ``prioritized`` specifies that Amazon EMR should launch the instances with the highest priority first. The default is ``lowest-price`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-ondemandprovisioningspecification.html#cfn-emr-instancefleetconfig-ondemandprovisioningspecification-allocationstrategy
            '''
            result = self._values.get("allocation_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def capacity_reservation_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.OnDemandCapacityReservationOptionsProperty"]]:
            '''The launch specification for On-Demand instances in the instance fleet, which determines the allocation strategy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-ondemandprovisioningspecification.html#cfn-emr-instancefleetconfig-ondemandprovisioningspecification-capacityreservationoptions
            '''
            result = self._values.get("capacity_reservation_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.OnDemandCapacityReservationOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnDemandProvisioningSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceFleetConfigPropsMixin.OnDemandResizingSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allocation_strategy": "allocationStrategy",
            "capacity_reservation_options": "capacityReservationOptions",
            "timeout_duration_minutes": "timeoutDurationMinutes",
        },
    )
    class OnDemandResizingSpecificationProperty:
        def __init__(
            self,
            *,
            allocation_strategy: typing.Optional[builtins.str] = None,
            capacity_reservation_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceFleetConfigPropsMixin.OnDemandCapacityReservationOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timeout_duration_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The resize specification for On-Demand Instances in the instance fleet, which contains the resize timeout period.

            :param allocation_strategy: Specifies the allocation strategy to use to launch On-Demand instances during a resize. The default is ``lowest-price`` .
            :param capacity_reservation_options: 
            :param timeout_duration_minutes: On-Demand resize timeout in minutes. If On-Demand Instances are not provisioned within this time, the resize workflow stops. The minimum value is 5 minutes, and the maximum value is 10,080 minutes (7 days). The timeout applies to all resize workflows on the Instance Fleet. The resize could be triggered by Amazon EMR Managed Scaling or by the customer (via Amazon EMR Console, Amazon EMR CLI modify-instance-fleet or Amazon EMR SDK ModifyInstanceFleet API) or by Amazon EMR due to Amazon EC2 Spot Reclamation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-ondemandresizingspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                on_demand_resizing_specification_property = emr_mixins.CfnInstanceFleetConfigPropsMixin.OnDemandResizingSpecificationProperty(
                    allocation_strategy="allocationStrategy",
                    capacity_reservation_options=emr_mixins.CfnInstanceFleetConfigPropsMixin.OnDemandCapacityReservationOptionsProperty(
                        capacity_reservation_preference="capacityReservationPreference",
                        capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn",
                        usage_strategy="usageStrategy"
                    ),
                    timeout_duration_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__261f7cf4b78b932eb7c5744d763200575aeb1c946aeecc5e413ac5ab59fbb7fc)
                check_type(argname="argument allocation_strategy", value=allocation_strategy, expected_type=type_hints["allocation_strategy"])
                check_type(argname="argument capacity_reservation_options", value=capacity_reservation_options, expected_type=type_hints["capacity_reservation_options"])
                check_type(argname="argument timeout_duration_minutes", value=timeout_duration_minutes, expected_type=type_hints["timeout_duration_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allocation_strategy is not None:
                self._values["allocation_strategy"] = allocation_strategy
            if capacity_reservation_options is not None:
                self._values["capacity_reservation_options"] = capacity_reservation_options
            if timeout_duration_minutes is not None:
                self._values["timeout_duration_minutes"] = timeout_duration_minutes

        @builtins.property
        def allocation_strategy(self) -> typing.Optional[builtins.str]:
            '''Specifies the allocation strategy to use to launch On-Demand instances during a resize.

            The default is ``lowest-price`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-ondemandresizingspecification.html#cfn-emr-instancefleetconfig-ondemandresizingspecification-allocationstrategy
            '''
            result = self._values.get("allocation_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def capacity_reservation_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.OnDemandCapacityReservationOptionsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-ondemandresizingspecification.html#cfn-emr-instancefleetconfig-ondemandresizingspecification-capacityreservationoptions
            '''
            result = self._values.get("capacity_reservation_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceFleetConfigPropsMixin.OnDemandCapacityReservationOptionsProperty"]], result)

        @builtins.property
        def timeout_duration_minutes(self) -> typing.Optional[jsii.Number]:
            '''On-Demand resize timeout in minutes.

            If On-Demand Instances are not provisioned within this time, the resize workflow stops. The minimum value is 5 minutes, and the maximum value is 10,080 minutes (7 days). The timeout applies to all resize workflows on the Instance Fleet. The resize could be triggered by Amazon EMR Managed Scaling or by the customer (via Amazon EMR Console, Amazon EMR CLI modify-instance-fleet or Amazon EMR SDK ModifyInstanceFleet API) or by Amazon EMR due to Amazon EC2 Spot Reclamation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-ondemandresizingspecification.html#cfn-emr-instancefleetconfig-ondemandresizingspecification-timeoutdurationminutes
            '''
            result = self._values.get("timeout_duration_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnDemandResizingSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceFleetConfigPropsMixin.SpotProvisioningSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allocation_strategy": "allocationStrategy",
            "block_duration_minutes": "blockDurationMinutes",
            "timeout_action": "timeoutAction",
            "timeout_duration_minutes": "timeoutDurationMinutes",
        },
    )
    class SpotProvisioningSpecificationProperty:
        def __init__(
            self,
            *,
            allocation_strategy: typing.Optional[builtins.str] = None,
            block_duration_minutes: typing.Optional[jsii.Number] = None,
            timeout_action: typing.Optional[builtins.str] = None,
            timeout_duration_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``SpotProvisioningSpecification`` is a subproperty of the ``InstanceFleetProvisioningSpecifications`` property type.

            ``SpotProvisioningSpecification`` determines the launch specification for Spot instances in the instance fleet, which includes the defined duration and provisioning timeout behavior.
            .. epigraph::

               The instance fleet configuration is available only in Amazon EMR versions 4.8.0 and later, excluding 5.0.x versions.

            :param allocation_strategy: Specifies one of the following strategies to launch Spot Instance fleets: ``capacity-optimized`` , ``price-capacity-optimized`` , ``lowest-price`` , or ``diversified`` , and ``capacity-optimized-prioritized`` . For more information on the provisioning strategies, see `Allocation strategies for Spot Instances <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-fleet-allocation-strategy.html>`_ in the *Amazon EC2 User Guide for Linux Instances* . .. epigraph:: When you launch a Spot Instance fleet with the old console, it automatically launches with the ``capacity-optimized`` strategy. You can't change the allocation strategy from the old console.
            :param block_duration_minutes: The defined duration for Spot Instances (also known as Spot blocks) in minutes. When specified, the Spot Instance does not terminate before the defined duration expires, and defined duration pricing for Spot Instances applies. Valid values are 60, 120, 180, 240, 300, or 360. The duration period starts as soon as a Spot Instance receives its instance ID. At the end of the duration, Amazon EC2 marks the Spot Instance for termination and provides a Spot Instance termination notice, which gives the instance a two-minute warning before it terminates. .. epigraph:: Spot Instances with a defined duration (also known as Spot blocks) are no longer available to new customers from July 1, 2021. For customers who have previously used the feature, we will continue to support Spot Instances with a defined duration until December 31, 2022.
            :param timeout_action: The action to take when ``TargetSpotCapacity`` has not been fulfilled when the ``TimeoutDurationMinutes`` has expired; that is, when all Spot Instances could not be provisioned within the Spot provisioning timeout. Valid values are ``TERMINATE_CLUSTER`` and ``SWITCH_TO_ON_DEMAND`` . SWITCH_TO_ON_DEMAND specifies that if no Spot Instances are available, On-Demand Instances should be provisioned to fulfill any remaining Spot capacity.
            :param timeout_duration_minutes: The Spot provisioning timeout period in minutes. If Spot Instances are not provisioned within this time period, the ``TimeOutAction`` is taken. Minimum value is 5 and maximum value is 1440. The timeout applies only during initial provisioning, when the cluster is first created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-spotprovisioningspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                spot_provisioning_specification_property = emr_mixins.CfnInstanceFleetConfigPropsMixin.SpotProvisioningSpecificationProperty(
                    allocation_strategy="allocationStrategy",
                    block_duration_minutes=123,
                    timeout_action="timeoutAction",
                    timeout_duration_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__be301fbd3c39b22e02a5a97b76f96ce69b6b6bdbbf6e0d731d162587d780da82)
                check_type(argname="argument allocation_strategy", value=allocation_strategy, expected_type=type_hints["allocation_strategy"])
                check_type(argname="argument block_duration_minutes", value=block_duration_minutes, expected_type=type_hints["block_duration_minutes"])
                check_type(argname="argument timeout_action", value=timeout_action, expected_type=type_hints["timeout_action"])
                check_type(argname="argument timeout_duration_minutes", value=timeout_duration_minutes, expected_type=type_hints["timeout_duration_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allocation_strategy is not None:
                self._values["allocation_strategy"] = allocation_strategy
            if block_duration_minutes is not None:
                self._values["block_duration_minutes"] = block_duration_minutes
            if timeout_action is not None:
                self._values["timeout_action"] = timeout_action
            if timeout_duration_minutes is not None:
                self._values["timeout_duration_minutes"] = timeout_duration_minutes

        @builtins.property
        def allocation_strategy(self) -> typing.Optional[builtins.str]:
            '''Specifies one of the following strategies to launch Spot Instance fleets: ``capacity-optimized`` , ``price-capacity-optimized`` , ``lowest-price`` , or ``diversified`` , and ``capacity-optimized-prioritized`` .

            For more information on the provisioning strategies, see `Allocation strategies for Spot Instances <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-fleet-allocation-strategy.html>`_ in the *Amazon EC2 User Guide for Linux Instances* .
            .. epigraph::

               When you launch a Spot Instance fleet with the old console, it automatically launches with the ``capacity-optimized`` strategy. You can't change the allocation strategy from the old console.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-spotprovisioningspecification.html#cfn-emr-instancefleetconfig-spotprovisioningspecification-allocationstrategy
            '''
            result = self._values.get("allocation_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def block_duration_minutes(self) -> typing.Optional[jsii.Number]:
            '''The defined duration for Spot Instances (also known as Spot blocks) in minutes.

            When specified, the Spot Instance does not terminate before the defined duration expires, and defined duration pricing for Spot Instances applies. Valid values are 60, 120, 180, 240, 300, or 360. The duration period starts as soon as a Spot Instance receives its instance ID. At the end of the duration, Amazon EC2 marks the Spot Instance for termination and provides a Spot Instance termination notice, which gives the instance a two-minute warning before it terminates.
            .. epigraph::

               Spot Instances with a defined duration (also known as Spot blocks) are no longer available to new customers from July 1, 2021. For customers who have previously used the feature, we will continue to support Spot Instances with a defined duration until December 31, 2022.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-spotprovisioningspecification.html#cfn-emr-instancefleetconfig-spotprovisioningspecification-blockdurationminutes
            '''
            result = self._values.get("block_duration_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def timeout_action(self) -> typing.Optional[builtins.str]:
            '''The action to take when ``TargetSpotCapacity`` has not been fulfilled when the ``TimeoutDurationMinutes`` has expired;

            that is, when all Spot Instances could not be provisioned within the Spot provisioning timeout. Valid values are ``TERMINATE_CLUSTER`` and ``SWITCH_TO_ON_DEMAND`` . SWITCH_TO_ON_DEMAND specifies that if no Spot Instances are available, On-Demand Instances should be provisioned to fulfill any remaining Spot capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-spotprovisioningspecification.html#cfn-emr-instancefleetconfig-spotprovisioningspecification-timeoutaction
            '''
            result = self._values.get("timeout_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timeout_duration_minutes(self) -> typing.Optional[jsii.Number]:
            '''The Spot provisioning timeout period in minutes.

            If Spot Instances are not provisioned within this time period, the ``TimeOutAction`` is taken. Minimum value is 5 and maximum value is 1440. The timeout applies only during initial provisioning, when the cluster is first created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-spotprovisioningspecification.html#cfn-emr-instancefleetconfig-spotprovisioningspecification-timeoutdurationminutes
            '''
            result = self._values.get("timeout_duration_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SpotProvisioningSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceFleetConfigPropsMixin.SpotResizingSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allocation_strategy": "allocationStrategy",
            "timeout_duration_minutes": "timeoutDurationMinutes",
        },
    )
    class SpotResizingSpecificationProperty:
        def __init__(
            self,
            *,
            allocation_strategy: typing.Optional[builtins.str] = None,
            timeout_duration_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The resize specification for Spot Instances in the instance fleet, which contains the resize timeout period.

            :param allocation_strategy: Specifies the allocation strategy to use to launch Spot instances during a resize. If you run Amazon EMR releases 6.9.0 or higher, the default is ``price-capacity-optimized`` . If you run Amazon EMR releases 6.8.0 or lower, the default is ``capacity-optimized`` .
            :param timeout_duration_minutes: Spot resize timeout in minutes. If Spot Instances are not provisioned within this time, the resize workflow will stop provisioning of Spot instances. Minimum value is 5 minutes and maximum value is 10,080 minutes (7 days). The timeout applies to all resize workflows on the Instance Fleet. The resize could be triggered by Amazon EMR Managed Scaling or by the customer (via Amazon EMR Console, Amazon EMR CLI modify-instance-fleet or Amazon EMR SDK ModifyInstanceFleet API) or by Amazon EMR due to Amazon EC2 Spot Reclamation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-spotresizingspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                spot_resizing_specification_property = emr_mixins.CfnInstanceFleetConfigPropsMixin.SpotResizingSpecificationProperty(
                    allocation_strategy="allocationStrategy",
                    timeout_duration_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5ab2b8b769bb61af19778fb8f7461f34fdb0a39d3e2f9ba4eecd71cbe3055469)
                check_type(argname="argument allocation_strategy", value=allocation_strategy, expected_type=type_hints["allocation_strategy"])
                check_type(argname="argument timeout_duration_minutes", value=timeout_duration_minutes, expected_type=type_hints["timeout_duration_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allocation_strategy is not None:
                self._values["allocation_strategy"] = allocation_strategy
            if timeout_duration_minutes is not None:
                self._values["timeout_duration_minutes"] = timeout_duration_minutes

        @builtins.property
        def allocation_strategy(self) -> typing.Optional[builtins.str]:
            '''Specifies the allocation strategy to use to launch Spot instances during a resize.

            If you run Amazon EMR releases 6.9.0 or higher, the default is ``price-capacity-optimized`` . If you run Amazon EMR releases 6.8.0 or lower, the default is ``capacity-optimized`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-spotresizingspecification.html#cfn-emr-instancefleetconfig-spotresizingspecification-allocationstrategy
            '''
            result = self._values.get("allocation_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timeout_duration_minutes(self) -> typing.Optional[jsii.Number]:
            '''Spot resize timeout in minutes.

            If Spot Instances are not provisioned within this time, the resize workflow will stop provisioning of Spot instances. Minimum value is 5 minutes and maximum value is 10,080 minutes (7 days). The timeout applies to all resize workflows on the Instance Fleet. The resize could be triggered by Amazon EMR Managed Scaling or by the customer (via Amazon EMR Console, Amazon EMR CLI modify-instance-fleet or Amazon EMR SDK ModifyInstanceFleet API) or by Amazon EMR due to Amazon EC2 Spot Reclamation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-spotresizingspecification.html#cfn-emr-instancefleetconfig-spotresizingspecification-timeoutdurationminutes
            '''
            result = self._values.get("timeout_duration_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SpotResizingSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceFleetConfigPropsMixin.VolumeSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "iops": "iops",
            "size_in_gb": "sizeInGb",
            "throughput": "throughput",
            "volume_type": "volumeType",
        },
    )
    class VolumeSpecificationProperty:
        def __init__(
            self,
            *,
            iops: typing.Optional[jsii.Number] = None,
            size_in_gb: typing.Optional[jsii.Number] = None,
            throughput: typing.Optional[jsii.Number] = None,
            volume_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``VolumeSpecification`` is a subproperty of the ``EbsBlockDeviceConfig`` property type.

            ``VolumeSecification`` determines the volume type, IOPS, and size (GiB) for EBS volumes attached to EC2 instances.

            :param iops: The number of I/O operations per second (IOPS) that the volume supports.
            :param size_in_gb: The volume size, in gibibytes (GiB). This can be a number from 1 - 1024. If the volume type is EBS-optimized, the minimum value is 10.
            :param throughput: The throughput, in mebibyte per second (MiB/s). This optional parameter can be a number from 125 - 1000 and is valid only for gp3 volumes.
            :param volume_type: The volume type. Volume types supported are gp3, gp2, io1, st1, sc1, and standard.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-volumespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                volume_specification_property = emr_mixins.CfnInstanceFleetConfigPropsMixin.VolumeSpecificationProperty(
                    iops=123,
                    size_in_gb=123,
                    throughput=123,
                    volume_type="volumeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__868c99c393df3d0b0719b0753f78923ab39ddb79edf99d55095c56b1c6ef0e10)
                check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
                check_type(argname="argument size_in_gb", value=size_in_gb, expected_type=type_hints["size_in_gb"])
                check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
                check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iops is not None:
                self._values["iops"] = iops
            if size_in_gb is not None:
                self._values["size_in_gb"] = size_in_gb
            if throughput is not None:
                self._values["throughput"] = throughput
            if volume_type is not None:
                self._values["volume_type"] = volume_type

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            '''The number of I/O operations per second (IOPS) that the volume supports.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-volumespecification.html#cfn-emr-instancefleetconfig-volumespecification-iops
            '''
            result = self._values.get("iops")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def size_in_gb(self) -> typing.Optional[jsii.Number]:
            '''The volume size, in gibibytes (GiB).

            This can be a number from 1 - 1024. If the volume type is EBS-optimized, the minimum value is 10.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-volumespecification.html#cfn-emr-instancefleetconfig-volumespecification-sizeingb
            '''
            result = self._values.get("size_in_gb")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throughput(self) -> typing.Optional[jsii.Number]:
            '''The throughput, in mebibyte per second (MiB/s).

            This optional parameter can be a number from 125 - 1000 and is valid only for gp3 volumes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-volumespecification.html#cfn-emr-instancefleetconfig-volumespecification-throughput
            '''
            result = self._values.get("throughput")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_type(self) -> typing.Optional[builtins.str]:
            '''The volume type.

            Volume types supported are gp3, gp2, io1, st1, sc1, and standard.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancefleetconfig-volumespecification.html#cfn-emr-instancefleetconfig-volumespecification-volumetype
            '''
            result = self._values.get("volume_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VolumeSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceGroupConfigMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_policy": "autoScalingPolicy",
        "bid_price": "bidPrice",
        "configurations": "configurations",
        "custom_ami_id": "customAmiId",
        "ebs_configuration": "ebsConfiguration",
        "instance_count": "instanceCount",
        "instance_role": "instanceRole",
        "instance_type": "instanceType",
        "job_flow_id": "jobFlowId",
        "market": "market",
        "name": "name",
    },
)
class CfnInstanceGroupConfigMixinProps:
    def __init__(
        self,
        *,
        auto_scaling_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceGroupConfigPropsMixin.AutoScalingPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        bid_price: typing.Optional[builtins.str] = None,
        configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceGroupConfigPropsMixin.ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        custom_ami_id: typing.Optional[builtins.str] = None,
        ebs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceGroupConfigPropsMixin.EbsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_count: typing.Optional[jsii.Number] = None,
        instance_role: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[builtins.str] = None,
        job_flow_id: typing.Optional[builtins.str] = None,
        market: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnInstanceGroupConfigPropsMixin.

        :param auto_scaling_policy: ``AutoScalingPolicy`` is a subproperty of ``InstanceGroupConfig`` . ``AutoScalingPolicy`` defines how an instance group dynamically adds and terminates EC2 instances in response to the value of a CloudWatch metric. For more information, see `Using Automatic Scaling in Amazon EMR <https://docs.aws.amazon.com//emr/latest/ManagementGuide/emr-automatic-scaling.html>`_ in the *Amazon EMR Management Guide* .
        :param bid_price: If specified, indicates that the instance group uses Spot Instances. This is the maximum price you are willing to pay for Spot Instances. Specify ``OnDemandPrice`` to set the amount equal to the On-Demand price, or specify an amount in USD.
        :param configurations: .. epigraph:: Amazon EMR releases 4.x or later. The list of configurations supplied for an Amazon EMR cluster instance group. You can specify a separate configuration for each instance group (master, core, and task).
        :param custom_ami_id: The custom AMI ID to use for the provisioned instance group.
        :param ebs_configuration: ``EbsConfiguration`` determines the EBS volumes to attach to EMR cluster instances.
        :param instance_count: Target number of instances for the instance group.
        :param instance_role: The role of the instance group in the cluster. *Allowed Values* : TASK
        :param instance_type: The Amazon EC2 instance type for all instances in the instance group.
        :param job_flow_id: The ID of an Amazon EMR cluster that you want to associate this instance group with.
        :param market: Market type of the Amazon EC2 instances used to create a cluster node.
        :param name: Friendly name given to the instance group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancegroupconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
            
            # configuration_property_: emr_mixins.CfnInstanceGroupConfigPropsMixin.ConfigurationProperty
            
            cfn_instance_group_config_mixin_props = emr_mixins.CfnInstanceGroupConfigMixinProps(
                auto_scaling_policy=emr_mixins.CfnInstanceGroupConfigPropsMixin.AutoScalingPolicyProperty(
                    constraints=emr_mixins.CfnInstanceGroupConfigPropsMixin.ScalingConstraintsProperty(
                        max_capacity=123,
                        min_capacity=123
                    ),
                    rules=[emr_mixins.CfnInstanceGroupConfigPropsMixin.ScalingRuleProperty(
                        action=emr_mixins.CfnInstanceGroupConfigPropsMixin.ScalingActionProperty(
                            market="market",
                            simple_scaling_policy_configuration=emr_mixins.CfnInstanceGroupConfigPropsMixin.SimpleScalingPolicyConfigurationProperty(
                                adjustment_type="adjustmentType",
                                cool_down=123,
                                scaling_adjustment=123
                            )
                        ),
                        description="description",
                        name="name",
                        trigger=emr_mixins.CfnInstanceGroupConfigPropsMixin.ScalingTriggerProperty(
                            cloud_watch_alarm_definition=emr_mixins.CfnInstanceGroupConfigPropsMixin.CloudWatchAlarmDefinitionProperty(
                                comparison_operator="comparisonOperator",
                                dimensions=[emr_mixins.CfnInstanceGroupConfigPropsMixin.MetricDimensionProperty(
                                    key="key",
                                    value="value"
                                )],
                                evaluation_periods=123,
                                metric_name="metricName",
                                namespace="namespace",
                                period=123,
                                statistic="statistic",
                                threshold=123,
                                unit="unit"
                            )
                        )
                    )]
                ),
                bid_price="bidPrice",
                configurations=[emr_mixins.CfnInstanceGroupConfigPropsMixin.ConfigurationProperty(
                    classification="classification",
                    configuration_properties={
                        "configuration_properties_key": "configurationProperties"
                    },
                    configurations=[configuration_property_]
                )],
                custom_ami_id="customAmiId",
                ebs_configuration=emr_mixins.CfnInstanceGroupConfigPropsMixin.EbsConfigurationProperty(
                    ebs_block_device_configs=[emr_mixins.CfnInstanceGroupConfigPropsMixin.EbsBlockDeviceConfigProperty(
                        volume_specification=emr_mixins.CfnInstanceGroupConfigPropsMixin.VolumeSpecificationProperty(
                            iops=123,
                            size_in_gb=123,
                            throughput=123,
                            volume_type="volumeType"
                        ),
                        volumes_per_instance=123
                    )],
                    ebs_optimized=False
                ),
                instance_count=123,
                instance_role="instanceRole",
                instance_type="instanceType",
                job_flow_id="jobFlowId",
                market="market",
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba8c45d610388120b6072a6eb4cc2c313a4ff23f2ee92e3719a5eac6fe2c2a54)
            check_type(argname="argument auto_scaling_policy", value=auto_scaling_policy, expected_type=type_hints["auto_scaling_policy"])
            check_type(argname="argument bid_price", value=bid_price, expected_type=type_hints["bid_price"])
            check_type(argname="argument configurations", value=configurations, expected_type=type_hints["configurations"])
            check_type(argname="argument custom_ami_id", value=custom_ami_id, expected_type=type_hints["custom_ami_id"])
            check_type(argname="argument ebs_configuration", value=ebs_configuration, expected_type=type_hints["ebs_configuration"])
            check_type(argname="argument instance_count", value=instance_count, expected_type=type_hints["instance_count"])
            check_type(argname="argument instance_role", value=instance_role, expected_type=type_hints["instance_role"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument job_flow_id", value=job_flow_id, expected_type=type_hints["job_flow_id"])
            check_type(argname="argument market", value=market, expected_type=type_hints["market"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_scaling_policy is not None:
            self._values["auto_scaling_policy"] = auto_scaling_policy
        if bid_price is not None:
            self._values["bid_price"] = bid_price
        if configurations is not None:
            self._values["configurations"] = configurations
        if custom_ami_id is not None:
            self._values["custom_ami_id"] = custom_ami_id
        if ebs_configuration is not None:
            self._values["ebs_configuration"] = ebs_configuration
        if instance_count is not None:
            self._values["instance_count"] = instance_count
        if instance_role is not None:
            self._values["instance_role"] = instance_role
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if job_flow_id is not None:
            self._values["job_flow_id"] = job_flow_id
        if market is not None:
            self._values["market"] = market
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def auto_scaling_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.AutoScalingPolicyProperty"]]:
        '''``AutoScalingPolicy`` is a subproperty of ``InstanceGroupConfig`` .

        ``AutoScalingPolicy`` defines how an instance group dynamically adds and terminates EC2 instances in response to the value of a CloudWatch metric. For more information, see `Using Automatic Scaling in Amazon EMR <https://docs.aws.amazon.com//emr/latest/ManagementGuide/emr-automatic-scaling.html>`_ in the *Amazon EMR Management Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancegroupconfig.html#cfn-emr-instancegroupconfig-autoscalingpolicy
        '''
        result = self._values.get("auto_scaling_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.AutoScalingPolicyProperty"]], result)

    @builtins.property
    def bid_price(self) -> typing.Optional[builtins.str]:
        '''If specified, indicates that the instance group uses Spot Instances.

        This is the maximum price you are willing to pay for Spot Instances. Specify ``OnDemandPrice`` to set the amount equal to the On-Demand price, or specify an amount in USD.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancegroupconfig.html#cfn-emr-instancegroupconfig-bidprice
        '''
        result = self._values.get("bid_price")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.ConfigurationProperty"]]]]:
        '''.. epigraph::

   Amazon EMR releases 4.x or later.

        The list of configurations supplied for an Amazon EMR cluster instance group. You can specify a separate configuration for each instance group (master, core, and task).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancegroupconfig.html#cfn-emr-instancegroupconfig-configurations
        '''
        result = self._values.get("configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.ConfigurationProperty"]]]], result)

    @builtins.property
    def custom_ami_id(self) -> typing.Optional[builtins.str]:
        '''The custom AMI ID to use for the provisioned instance group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancegroupconfig.html#cfn-emr-instancegroupconfig-customamiid
        '''
        result = self._values.get("custom_ami_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ebs_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.EbsConfigurationProperty"]]:
        '''``EbsConfiguration`` determines the EBS volumes to attach to EMR cluster instances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancegroupconfig.html#cfn-emr-instancegroupconfig-ebsconfiguration
        '''
        result = self._values.get("ebs_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.EbsConfigurationProperty"]], result)

    @builtins.property
    def instance_count(self) -> typing.Optional[jsii.Number]:
        '''Target number of instances for the instance group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancegroupconfig.html#cfn-emr-instancegroupconfig-instancecount
        '''
        result = self._values.get("instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instance_role(self) -> typing.Optional[builtins.str]:
        '''The role of the instance group in the cluster.

        *Allowed Values* : TASK

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancegroupconfig.html#cfn-emr-instancegroupconfig-instancerole
        '''
        result = self._values.get("instance_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''The Amazon EC2 instance type for all instances in the instance group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancegroupconfig.html#cfn-emr-instancegroupconfig-instancetype
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_flow_id(self) -> typing.Optional[builtins.str]:
        '''The ID of an Amazon EMR cluster that you want to associate this instance group with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancegroupconfig.html#cfn-emr-instancegroupconfig-jobflowid
        '''
        result = self._values.get("job_flow_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def market(self) -> typing.Optional[builtins.str]:
        '''Market type of the Amazon EC2 instances used to create a cluster node.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancegroupconfig.html#cfn-emr-instancegroupconfig-market
        '''
        result = self._values.get("market")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Friendly name given to the instance group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancegroupconfig.html#cfn-emr-instancegroupconfig-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceGroupConfigMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInstanceGroupConfigPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceGroupConfigPropsMixin",
):
    '''Use ``InstanceGroupConfig`` to define instance groups for an EMR cluster.

    A cluster can not use both instance groups and instance fleets. For more information, see `Create a Cluster with Instance Fleets or Uniform Instance Groups <https://docs.aws.amazon.com//emr/latest/ManagementGuide/emr-instance-group-configuration.html>`_ in the *Amazon EMR Management Guide* .
    .. epigraph::

       You can currently only add task instance groups to a cluster with this resource. If you use this resource, CloudFormation waits for the cluster launch to complete before adding the task instance group to the cluster. In order to add task instance groups to the cluster as part of the cluster launch and minimize delays in provisioning task nodes, use the ``TaskInstanceGroups`` subproperty for the `AWS::EMR::Cluster JobFlowInstancesConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticmapreduce-cluster-jobflowinstancesconfig.html>`_ property instead. To use this subproperty, see `AWS::EMR::Cluster <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticmapreduce-cluster.html>`_ for examples.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancegroupconfig.html
    :cloudformationResource: AWS::EMR::InstanceGroupConfig
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
        
        # configuration_property_: emr_mixins.CfnInstanceGroupConfigPropsMixin.ConfigurationProperty
        
        cfn_instance_group_config_props_mixin = emr_mixins.CfnInstanceGroupConfigPropsMixin(emr_mixins.CfnInstanceGroupConfigMixinProps(
            auto_scaling_policy=emr_mixins.CfnInstanceGroupConfigPropsMixin.AutoScalingPolicyProperty(
                constraints=emr_mixins.CfnInstanceGroupConfigPropsMixin.ScalingConstraintsProperty(
                    max_capacity=123,
                    min_capacity=123
                ),
                rules=[emr_mixins.CfnInstanceGroupConfigPropsMixin.ScalingRuleProperty(
                    action=emr_mixins.CfnInstanceGroupConfigPropsMixin.ScalingActionProperty(
                        market="market",
                        simple_scaling_policy_configuration=emr_mixins.CfnInstanceGroupConfigPropsMixin.SimpleScalingPolicyConfigurationProperty(
                            adjustment_type="adjustmentType",
                            cool_down=123,
                            scaling_adjustment=123
                        )
                    ),
                    description="description",
                    name="name",
                    trigger=emr_mixins.CfnInstanceGroupConfigPropsMixin.ScalingTriggerProperty(
                        cloud_watch_alarm_definition=emr_mixins.CfnInstanceGroupConfigPropsMixin.CloudWatchAlarmDefinitionProperty(
                            comparison_operator="comparisonOperator",
                            dimensions=[emr_mixins.CfnInstanceGroupConfigPropsMixin.MetricDimensionProperty(
                                key="key",
                                value="value"
                            )],
                            evaluation_periods=123,
                            metric_name="metricName",
                            namespace="namespace",
                            period=123,
                            statistic="statistic",
                            threshold=123,
                            unit="unit"
                        )
                    )
                )]
            ),
            bid_price="bidPrice",
            configurations=[emr_mixins.CfnInstanceGroupConfigPropsMixin.ConfigurationProperty(
                classification="classification",
                configuration_properties={
                    "configuration_properties_key": "configurationProperties"
                },
                configurations=[configuration_property_]
            )],
            custom_ami_id="customAmiId",
            ebs_configuration=emr_mixins.CfnInstanceGroupConfigPropsMixin.EbsConfigurationProperty(
                ebs_block_device_configs=[emr_mixins.CfnInstanceGroupConfigPropsMixin.EbsBlockDeviceConfigProperty(
                    volume_specification=emr_mixins.CfnInstanceGroupConfigPropsMixin.VolumeSpecificationProperty(
                        iops=123,
                        size_in_gb=123,
                        throughput=123,
                        volume_type="volumeType"
                    ),
                    volumes_per_instance=123
                )],
                ebs_optimized=False
            ),
            instance_count=123,
            instance_role="instanceRole",
            instance_type="instanceType",
            job_flow_id="jobFlowId",
            market="market",
            name="name"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnInstanceGroupConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EMR::InstanceGroupConfig``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92c8bad74698eab157a1334a4fc571ed3feaea415b26bef90dbf1e13e1dff671)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1810de87179afe13e195ee7e2c0aa2b08041ba1a74fd195b6f393c2c9bb66964)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd08b24c721ea167a7c7c45b59a89d3dbddf0ab8769abc23471e2bf8b40adb82)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInstanceGroupConfigMixinProps:
        return typing.cast(CfnInstanceGroupConfigMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceGroupConfigPropsMixin.AutoScalingPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"constraints": "constraints", "rules": "rules"},
    )
    class AutoScalingPolicyProperty:
        def __init__(
            self,
            *,
            constraints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceGroupConfigPropsMixin.ScalingConstraintsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceGroupConfigPropsMixin.ScalingRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''``AutoScalingPolicy`` defines how an instance group dynamically adds and terminates EC2 instances in response to the value of a CloudWatch metric.

            For more information, see `Using Automatic Scaling in Amazon EMR <https://docs.aws.amazon.com//emr/latest/ManagementGuide/emr-automatic-scaling.html>`_ in the *Amazon EMR Management Guide* .

            :param constraints: The upper and lower Amazon EC2 instance limits for an automatic scaling policy. Automatic scaling activity will not cause an instance group to grow above or below these limits.
            :param rules: The scale-in and scale-out rules that comprise the automatic scaling policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-autoscalingpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                auto_scaling_policy_property = emr_mixins.CfnInstanceGroupConfigPropsMixin.AutoScalingPolicyProperty(
                    constraints=emr_mixins.CfnInstanceGroupConfigPropsMixin.ScalingConstraintsProperty(
                        max_capacity=123,
                        min_capacity=123
                    ),
                    rules=[emr_mixins.CfnInstanceGroupConfigPropsMixin.ScalingRuleProperty(
                        action=emr_mixins.CfnInstanceGroupConfigPropsMixin.ScalingActionProperty(
                            market="market",
                            simple_scaling_policy_configuration=emr_mixins.CfnInstanceGroupConfigPropsMixin.SimpleScalingPolicyConfigurationProperty(
                                adjustment_type="adjustmentType",
                                cool_down=123,
                                scaling_adjustment=123
                            )
                        ),
                        description="description",
                        name="name",
                        trigger=emr_mixins.CfnInstanceGroupConfigPropsMixin.ScalingTriggerProperty(
                            cloud_watch_alarm_definition=emr_mixins.CfnInstanceGroupConfigPropsMixin.CloudWatchAlarmDefinitionProperty(
                                comparison_operator="comparisonOperator",
                                dimensions=[emr_mixins.CfnInstanceGroupConfigPropsMixin.MetricDimensionProperty(
                                    key="key",
                                    value="value"
                                )],
                                evaluation_periods=123,
                                metric_name="metricName",
                                namespace="namespace",
                                period=123,
                                statistic="statistic",
                                threshold=123,
                                unit="unit"
                            )
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__02e2127602c48f6a9789f991bfacae18cc7e4298a234ee9a475c6300e7bd56ab)
                check_type(argname="argument constraints", value=constraints, expected_type=type_hints["constraints"])
                check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if constraints is not None:
                self._values["constraints"] = constraints
            if rules is not None:
                self._values["rules"] = rules

        @builtins.property
        def constraints(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.ScalingConstraintsProperty"]]:
            '''The upper and lower Amazon EC2 instance limits for an automatic scaling policy.

            Automatic scaling activity will not cause an instance group to grow above or below these limits.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-autoscalingpolicy.html#cfn-emr-instancegroupconfig-autoscalingpolicy-constraints
            '''
            result = self._values.get("constraints")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.ScalingConstraintsProperty"]], result)

        @builtins.property
        def rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.ScalingRuleProperty"]]]]:
            '''The scale-in and scale-out rules that comprise the automatic scaling policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-autoscalingpolicy.html#cfn-emr-instancegroupconfig-autoscalingpolicy-rules
            '''
            result = self._values.get("rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.ScalingRuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoScalingPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceGroupConfigPropsMixin.CloudWatchAlarmDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "comparison_operator": "comparisonOperator",
            "dimensions": "dimensions",
            "evaluation_periods": "evaluationPeriods",
            "metric_name": "metricName",
            "namespace": "namespace",
            "period": "period",
            "statistic": "statistic",
            "threshold": "threshold",
            "unit": "unit",
        },
    )
    class CloudWatchAlarmDefinitionProperty:
        def __init__(
            self,
            *,
            comparison_operator: typing.Optional[builtins.str] = None,
            dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceGroupConfigPropsMixin.MetricDimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            evaluation_periods: typing.Optional[jsii.Number] = None,
            metric_name: typing.Optional[builtins.str] = None,
            namespace: typing.Optional[builtins.str] = None,
            period: typing.Optional[jsii.Number] = None,
            statistic: typing.Optional[builtins.str] = None,
            threshold: typing.Optional[jsii.Number] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``CloudWatchAlarmDefinition`` is a subproperty of the ``ScalingTrigger`` property, which determines when to trigger an automatic scaling activity.

            Scaling activity begins when you satisfy the defined alarm conditions.

            :param comparison_operator: Determines how the metric specified by ``MetricName`` is compared to the value specified by ``Threshold`` .
            :param dimensions: A CloudWatch metric dimension.
            :param evaluation_periods: The number of periods, in five-minute increments, during which the alarm condition must exist before the alarm triggers automatic scaling activity. The default value is ``1`` .
            :param metric_name: The name of the CloudWatch metric that is watched to determine an alarm condition.
            :param namespace: The namespace for the CloudWatch metric. The default is ``AWS/ElasticMapReduce`` .
            :param period: The period, in seconds, over which the statistic is applied. CloudWatch metrics for Amazon EMR are emitted every five minutes (300 seconds), so if you specify a CloudWatch metric, specify ``300`` .
            :param statistic: The statistic to apply to the metric associated with the alarm. The default is ``AVERAGE`` .
            :param threshold: The value against which the specified statistic is compared.
            :param unit: The unit of measure associated with the CloudWatch metric being watched. The value specified for ``Unit`` must correspond to the units specified in the CloudWatch metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-cloudwatchalarmdefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                cloud_watch_alarm_definition_property = emr_mixins.CfnInstanceGroupConfigPropsMixin.CloudWatchAlarmDefinitionProperty(
                    comparison_operator="comparisonOperator",
                    dimensions=[emr_mixins.CfnInstanceGroupConfigPropsMixin.MetricDimensionProperty(
                        key="key",
                        value="value"
                    )],
                    evaluation_periods=123,
                    metric_name="metricName",
                    namespace="namespace",
                    period=123,
                    statistic="statistic",
                    threshold=123,
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4c4fe73e99c87da252b9d05b1f3a132c6321654ba5ad84310cb25cb5430b8ffa)
                check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
                check_type(argname="argument period", value=period, expected_type=type_hints["period"])
                check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
                check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparison_operator is not None:
                self._values["comparison_operator"] = comparison_operator
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if evaluation_periods is not None:
                self._values["evaluation_periods"] = evaluation_periods
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if namespace is not None:
                self._values["namespace"] = namespace
            if period is not None:
                self._values["period"] = period
            if statistic is not None:
                self._values["statistic"] = statistic
            if threshold is not None:
                self._values["threshold"] = threshold
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def comparison_operator(self) -> typing.Optional[builtins.str]:
            '''Determines how the metric specified by ``MetricName`` is compared to the value specified by ``Threshold`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-cloudwatchalarmdefinition.html#cfn-emr-instancegroupconfig-cloudwatchalarmdefinition-comparisonoperator
            '''
            result = self._values.get("comparison_operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.MetricDimensionProperty"]]]]:
            '''A CloudWatch metric dimension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-cloudwatchalarmdefinition.html#cfn-emr-instancegroupconfig-cloudwatchalarmdefinition-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.MetricDimensionProperty"]]]], result)

        @builtins.property
        def evaluation_periods(self) -> typing.Optional[jsii.Number]:
            '''The number of periods, in five-minute increments, during which the alarm condition must exist before the alarm triggers automatic scaling activity.

            The default value is ``1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-cloudwatchalarmdefinition.html#cfn-emr-instancegroupconfig-cloudwatchalarmdefinition-evaluationperiods
            '''
            result = self._values.get("evaluation_periods")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''The name of the CloudWatch metric that is watched to determine an alarm condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-cloudwatchalarmdefinition.html#cfn-emr-instancegroupconfig-cloudwatchalarmdefinition-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The namespace for the CloudWatch metric.

            The default is ``AWS/ElasticMapReduce`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-cloudwatchalarmdefinition.html#cfn-emr-instancegroupconfig-cloudwatchalarmdefinition-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def period(self) -> typing.Optional[jsii.Number]:
            '''The period, in seconds, over which the statistic is applied.

            CloudWatch metrics for Amazon EMR are emitted every five minutes (300 seconds), so if you specify a CloudWatch metric, specify ``300`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-cloudwatchalarmdefinition.html#cfn-emr-instancegroupconfig-cloudwatchalarmdefinition-period
            '''
            result = self._values.get("period")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def statistic(self) -> typing.Optional[builtins.str]:
            '''The statistic to apply to the metric associated with the alarm.

            The default is ``AVERAGE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-cloudwatchalarmdefinition.html#cfn-emr-instancegroupconfig-cloudwatchalarmdefinition-statistic
            '''
            result = self._values.get("statistic")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def threshold(self) -> typing.Optional[jsii.Number]:
            '''The value against which the specified statistic is compared.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-cloudwatchalarmdefinition.html#cfn-emr-instancegroupconfig-cloudwatchalarmdefinition-threshold
            '''
            result = self._values.get("threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit of measure associated with the CloudWatch metric being watched.

            The value specified for ``Unit`` must correspond to the units specified in the CloudWatch metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-cloudwatchalarmdefinition.html#cfn-emr-instancegroupconfig-cloudwatchalarmdefinition-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchAlarmDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceGroupConfigPropsMixin.ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "classification": "classification",
            "configuration_properties": "configurationProperties",
            "configurations": "configurations",
        },
    )
    class ConfigurationProperty:
        def __init__(
            self,
            *,
            classification: typing.Optional[builtins.str] = None,
            configuration_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceGroupConfigPropsMixin.ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''``Configurations`` is a property of the ``AWS::EMR::Cluster`` resource that specifies the configuration of applications on an Amazon EMR cluster.

            Configurations are optional. You can use them to have EMR customize applications and software bundled with Amazon EMR when a cluster is created. A configuration consists of a classification, properties, and optional nested configurations. A classification refers to an application-specific configuration file. Properties are the settings you want to change in that file. For more information, see `Configuring Applications <https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-configure-apps.html>`_ .
            .. epigraph::

               Applies only to Amazon EMR releases 4.0 and later.

            :param classification: The classification within a configuration.
            :param configuration_properties: Within a configuration classification, a set of properties that represent the settings that you want to change in the configuration file. Duplicates not allowed.
            :param configurations: A list of additional configurations to apply within a configuration object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                # configuration_property_: emr_mixins.CfnInstanceGroupConfigPropsMixin.ConfigurationProperty
                
                configuration_property = emr_mixins.CfnInstanceGroupConfigPropsMixin.ConfigurationProperty(
                    classification="classification",
                    configuration_properties={
                        "configuration_properties_key": "configurationProperties"
                    },
                    configurations=[configuration_property_]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__be08ddf5e29ff6827032687ee20da9cd788e48745f4e52946c3e4e78fc70c0bb)
                check_type(argname="argument classification", value=classification, expected_type=type_hints["classification"])
                check_type(argname="argument configuration_properties", value=configuration_properties, expected_type=type_hints["configuration_properties"])
                check_type(argname="argument configurations", value=configurations, expected_type=type_hints["configurations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if classification is not None:
                self._values["classification"] = classification
            if configuration_properties is not None:
                self._values["configuration_properties"] = configuration_properties
            if configurations is not None:
                self._values["configurations"] = configurations

        @builtins.property
        def classification(self) -> typing.Optional[builtins.str]:
            '''The classification within a configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-configuration.html#cfn-emr-instancegroupconfig-configuration-classification
            '''
            result = self._values.get("classification")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def configuration_properties(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Within a configuration classification, a set of properties that represent the settings that you want to change in the configuration file.

            Duplicates not allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-configuration.html#cfn-emr-instancegroupconfig-configuration-configurationproperties
            '''
            result = self._values.get("configuration_properties")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.ConfigurationProperty"]]]]:
            '''A list of additional configurations to apply within a configuration object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-configuration.html#cfn-emr-instancegroupconfig-configuration-configurations
            '''
            result = self._values.get("configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.ConfigurationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceGroupConfigPropsMixin.EbsBlockDeviceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "volume_specification": "volumeSpecification",
            "volumes_per_instance": "volumesPerInstance",
        },
    )
    class EbsBlockDeviceConfigProperty:
        def __init__(
            self,
            *,
            volume_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceGroupConfigPropsMixin.VolumeSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            volumes_per_instance: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configuration of requested EBS block device associated with the instance group with count of volumes that are associated to every instance.

            :param volume_specification: EBS volume specifications such as volume type, IOPS, size (GiB) and throughput (MiB/s) that are requested for the EBS volume attached to an Amazon EC2 instance in the cluster.
            :param volumes_per_instance: Number of EBS volumes with a specific volume configuration that are associated with every instance in the instance group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-ebsblockdeviceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                ebs_block_device_config_property = emr_mixins.CfnInstanceGroupConfigPropsMixin.EbsBlockDeviceConfigProperty(
                    volume_specification=emr_mixins.CfnInstanceGroupConfigPropsMixin.VolumeSpecificationProperty(
                        iops=123,
                        size_in_gb=123,
                        throughput=123,
                        volume_type="volumeType"
                    ),
                    volumes_per_instance=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5fbad35a8fbfca26d939b0d13bb20d300cbb1bc31b7c51b322f2561cd88ff917)
                check_type(argname="argument volume_specification", value=volume_specification, expected_type=type_hints["volume_specification"])
                check_type(argname="argument volumes_per_instance", value=volumes_per_instance, expected_type=type_hints["volumes_per_instance"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if volume_specification is not None:
                self._values["volume_specification"] = volume_specification
            if volumes_per_instance is not None:
                self._values["volumes_per_instance"] = volumes_per_instance

        @builtins.property
        def volume_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.VolumeSpecificationProperty"]]:
            '''EBS volume specifications such as volume type, IOPS, size (GiB) and throughput (MiB/s) that are requested for the EBS volume attached to an Amazon EC2 instance in the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-ebsblockdeviceconfig.html#cfn-emr-instancegroupconfig-ebsblockdeviceconfig-volumespecification
            '''
            result = self._values.get("volume_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.VolumeSpecificationProperty"]], result)

        @builtins.property
        def volumes_per_instance(self) -> typing.Optional[jsii.Number]:
            '''Number of EBS volumes with a specific volume configuration that are associated with every instance in the instance group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-ebsblockdeviceconfig.html#cfn-emr-instancegroupconfig-ebsblockdeviceconfig-volumesperinstance
            '''
            result = self._values.get("volumes_per_instance")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EbsBlockDeviceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceGroupConfigPropsMixin.EbsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ebs_block_device_configs": "ebsBlockDeviceConfigs",
            "ebs_optimized": "ebsOptimized",
        },
    )
    class EbsConfigurationProperty:
        def __init__(
            self,
            *,
            ebs_block_device_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceGroupConfigPropsMixin.EbsBlockDeviceConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ebs_optimized: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The Amazon EBS configuration of a cluster instance.

            :param ebs_block_device_configs: An array of Amazon EBS volume specifications attached to a cluster instance.
            :param ebs_optimized: Indicates whether an Amazon EBS volume is EBS-optimized. The default is false. You should explicitly set this value to true to enable the Amazon EBS-optimized setting for an EC2 instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-ebsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                ebs_configuration_property = emr_mixins.CfnInstanceGroupConfigPropsMixin.EbsConfigurationProperty(
                    ebs_block_device_configs=[emr_mixins.CfnInstanceGroupConfigPropsMixin.EbsBlockDeviceConfigProperty(
                        volume_specification=emr_mixins.CfnInstanceGroupConfigPropsMixin.VolumeSpecificationProperty(
                            iops=123,
                            size_in_gb=123,
                            throughput=123,
                            volume_type="volumeType"
                        ),
                        volumes_per_instance=123
                    )],
                    ebs_optimized=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__38e35402cebf22e1a6d350090c5fd68f1e54e328e701642ee9216b74b10ba2b6)
                check_type(argname="argument ebs_block_device_configs", value=ebs_block_device_configs, expected_type=type_hints["ebs_block_device_configs"])
                check_type(argname="argument ebs_optimized", value=ebs_optimized, expected_type=type_hints["ebs_optimized"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ebs_block_device_configs is not None:
                self._values["ebs_block_device_configs"] = ebs_block_device_configs
            if ebs_optimized is not None:
                self._values["ebs_optimized"] = ebs_optimized

        @builtins.property
        def ebs_block_device_configs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.EbsBlockDeviceConfigProperty"]]]]:
            '''An array of Amazon EBS volume specifications attached to a cluster instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-ebsconfiguration.html#cfn-emr-instancegroupconfig-ebsconfiguration-ebsblockdeviceconfigs
            '''
            result = self._values.get("ebs_block_device_configs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.EbsBlockDeviceConfigProperty"]]]], result)

        @builtins.property
        def ebs_optimized(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether an Amazon EBS volume is EBS-optimized.

            The default is false. You should explicitly set this value to true to enable the Amazon EBS-optimized setting for an EC2 instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-ebsconfiguration.html#cfn-emr-instancegroupconfig-ebsconfiguration-ebsoptimized
            '''
            result = self._values.get("ebs_optimized")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EbsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceGroupConfigPropsMixin.MetricDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class MetricDimensionProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``MetricDimension`` is a subproperty of the ``CloudWatchAlarmDefinition`` property type.

            ``MetricDimension`` specifies a CloudWatch dimension, which is specified with a ``Key`` ``Value`` pair. The key is known as a ``Name`` in CloudWatch. By default, Amazon EMR uses one dimension whose ``Key`` is ``JobFlowID`` and ``Value`` is a variable representing the cluster ID, which is ``${emr.clusterId}`` . This enables the automatic scaling rule for EMR to bootstrap when the cluster ID becomes available during cluster creation.

            :param key: The dimension name.
            :param value: The dimension value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-metricdimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                metric_dimension_property = emr_mixins.CfnInstanceGroupConfigPropsMixin.MetricDimensionProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0498619f042b9ad22fc1fc2053b365f9df8632fafebe62648bb2487e2dd9da72)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The dimension name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-metricdimension.html#cfn-emr-instancegroupconfig-metricdimension-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The dimension value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-metricdimension.html#cfn-emr-instancegroupconfig-metricdimension-value
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
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceGroupConfigPropsMixin.ScalingActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "market": "market",
            "simple_scaling_policy_configuration": "simpleScalingPolicyConfiguration",
        },
    )
    class ScalingActionProperty:
        def __init__(
            self,
            *,
            market: typing.Optional[builtins.str] = None,
            simple_scaling_policy_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceGroupConfigPropsMixin.SimpleScalingPolicyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''``ScalingAction`` is a subproperty of the ``ScalingRule`` property type.

            ``ScalingAction`` determines the type of adjustment the automatic scaling activity makes when triggered, and the periodicity of the adjustment.

            :param market: Not available for instance groups. Instance groups use the market type specified for the group.
            :param simple_scaling_policy_configuration: The type of adjustment the automatic scaling activity makes when triggered, and the periodicity of the adjustment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-scalingaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                scaling_action_property = emr_mixins.CfnInstanceGroupConfigPropsMixin.ScalingActionProperty(
                    market="market",
                    simple_scaling_policy_configuration=emr_mixins.CfnInstanceGroupConfigPropsMixin.SimpleScalingPolicyConfigurationProperty(
                        adjustment_type="adjustmentType",
                        cool_down=123,
                        scaling_adjustment=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b1386810dc0232ed5f87b1d0138663d98eb5998c1d31b7cd318a3372154fcb1)
                check_type(argname="argument market", value=market, expected_type=type_hints["market"])
                check_type(argname="argument simple_scaling_policy_configuration", value=simple_scaling_policy_configuration, expected_type=type_hints["simple_scaling_policy_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if market is not None:
                self._values["market"] = market
            if simple_scaling_policy_configuration is not None:
                self._values["simple_scaling_policy_configuration"] = simple_scaling_policy_configuration

        @builtins.property
        def market(self) -> typing.Optional[builtins.str]:
            '''Not available for instance groups.

            Instance groups use the market type specified for the group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-scalingaction.html#cfn-emr-instancegroupconfig-scalingaction-market
            '''
            result = self._values.get("market")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def simple_scaling_policy_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.SimpleScalingPolicyConfigurationProperty"]]:
            '''The type of adjustment the automatic scaling activity makes when triggered, and the periodicity of the adjustment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-scalingaction.html#cfn-emr-instancegroupconfig-scalingaction-simplescalingpolicyconfiguration
            '''
            result = self._values.get("simple_scaling_policy_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.SimpleScalingPolicyConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceGroupConfigPropsMixin.ScalingConstraintsProperty",
        jsii_struct_bases=[],
        name_mapping={"max_capacity": "maxCapacity", "min_capacity": "minCapacity"},
    )
    class ScalingConstraintsProperty:
        def __init__(
            self,
            *,
            max_capacity: typing.Optional[jsii.Number] = None,
            min_capacity: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``ScalingConstraints`` is a subproperty of the ``AutoScalingPolicy`` property type.

            ``ScalingConstraints`` defines the upper and lower EC2 instance limits for an automatic scaling policy. Automatic scaling activities triggered by automatic scaling rules will not cause an instance group to grow above or shrink below these limits.

            :param max_capacity: The upper boundary of Amazon EC2 instances in an instance group beyond which scaling activities are not allowed to grow. Scale-out activities will not add instances beyond this boundary.
            :param min_capacity: The lower boundary of Amazon EC2 instances in an instance group below which scaling activities are not allowed to shrink. Scale-in activities will not terminate instances below this boundary.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-scalingconstraints.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                scaling_constraints_property = emr_mixins.CfnInstanceGroupConfigPropsMixin.ScalingConstraintsProperty(
                    max_capacity=123,
                    min_capacity=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aee3f470a7334cd82e04064db78127b415bea3aceb5c966d8f004ab8c706c7eb)
                check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
                check_type(argname="argument min_capacity", value=min_capacity, expected_type=type_hints["min_capacity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_capacity is not None:
                self._values["max_capacity"] = max_capacity
            if min_capacity is not None:
                self._values["min_capacity"] = min_capacity

        @builtins.property
        def max_capacity(self) -> typing.Optional[jsii.Number]:
            '''The upper boundary of Amazon EC2 instances in an instance group beyond which scaling activities are not allowed to grow.

            Scale-out activities will not add instances beyond this boundary.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-scalingconstraints.html#cfn-emr-instancegroupconfig-scalingconstraints-maxcapacity
            '''
            result = self._values.get("max_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_capacity(self) -> typing.Optional[jsii.Number]:
            '''The lower boundary of Amazon EC2 instances in an instance group below which scaling activities are not allowed to shrink.

            Scale-in activities will not terminate instances below this boundary.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-scalingconstraints.html#cfn-emr-instancegroupconfig-scalingconstraints-mincapacity
            '''
            result = self._values.get("min_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingConstraintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceGroupConfigPropsMixin.ScalingRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "description": "description",
            "name": "name",
            "trigger": "trigger",
        },
    )
    class ScalingRuleProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceGroupConfigPropsMixin.ScalingActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            description: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            trigger: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceGroupConfigPropsMixin.ScalingTriggerProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''``ScalingRule`` is a subproperty of the ``AutoScalingPolicy`` property type.

            ``ScalingRule`` defines the scale-in or scale-out rules for scaling activity, including the CloudWatch metric alarm that triggers activity, how EC2 instances are added or removed, and the periodicity of adjustments. The automatic scaling policy for an instance group can comprise one or more automatic scaling rules.

            :param action: The conditions that trigger an automatic scaling activity.
            :param description: A friendly, more verbose description of the automatic scaling rule.
            :param name: The name used to identify an automatic scaling rule. Rule names must be unique within a scaling policy.
            :param trigger: The CloudWatch alarm definition that determines when automatic scaling activity is triggered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-scalingrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                scaling_rule_property = emr_mixins.CfnInstanceGroupConfigPropsMixin.ScalingRuleProperty(
                    action=emr_mixins.CfnInstanceGroupConfigPropsMixin.ScalingActionProperty(
                        market="market",
                        simple_scaling_policy_configuration=emr_mixins.CfnInstanceGroupConfigPropsMixin.SimpleScalingPolicyConfigurationProperty(
                            adjustment_type="adjustmentType",
                            cool_down=123,
                            scaling_adjustment=123
                        )
                    ),
                    description="description",
                    name="name",
                    trigger=emr_mixins.CfnInstanceGroupConfigPropsMixin.ScalingTriggerProperty(
                        cloud_watch_alarm_definition=emr_mixins.CfnInstanceGroupConfigPropsMixin.CloudWatchAlarmDefinitionProperty(
                            comparison_operator="comparisonOperator",
                            dimensions=[emr_mixins.CfnInstanceGroupConfigPropsMixin.MetricDimensionProperty(
                                key="key",
                                value="value"
                            )],
                            evaluation_periods=123,
                            metric_name="metricName",
                            namespace="namespace",
                            period=123,
                            statistic="statistic",
                            threshold=123,
                            unit="unit"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f3cfb6269ca3b56614ba8218b68681cc78d34c43669a873313c58fc57f91692c)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if description is not None:
                self._values["description"] = description
            if name is not None:
                self._values["name"] = name
            if trigger is not None:
                self._values["trigger"] = trigger

        @builtins.property
        def action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.ScalingActionProperty"]]:
            '''The conditions that trigger an automatic scaling activity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-scalingrule.html#cfn-emr-instancegroupconfig-scalingrule-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.ScalingActionProperty"]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A friendly, more verbose description of the automatic scaling rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-scalingrule.html#cfn-emr-instancegroupconfig-scalingrule-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name used to identify an automatic scaling rule.

            Rule names must be unique within a scaling policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-scalingrule.html#cfn-emr-instancegroupconfig-scalingrule-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def trigger(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.ScalingTriggerProperty"]]:
            '''The CloudWatch alarm definition that determines when automatic scaling activity is triggered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-scalingrule.html#cfn-emr-instancegroupconfig-scalingrule-trigger
            '''
            result = self._values.get("trigger")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.ScalingTriggerProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceGroupConfigPropsMixin.ScalingTriggerProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_watch_alarm_definition": "cloudWatchAlarmDefinition"},
    )
    class ScalingTriggerProperty:
        def __init__(
            self,
            *,
            cloud_watch_alarm_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceGroupConfigPropsMixin.CloudWatchAlarmDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''``ScalingTrigger`` is a subproperty of the ``ScalingRule`` property type.

            ``ScalingTrigger`` determines the conditions that trigger an automatic scaling activity.

            :param cloud_watch_alarm_definition: The definition of a CloudWatch metric alarm. When the defined alarm conditions are met along with other trigger parameters, scaling activity begins.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-scalingtrigger.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                scaling_trigger_property = emr_mixins.CfnInstanceGroupConfigPropsMixin.ScalingTriggerProperty(
                    cloud_watch_alarm_definition=emr_mixins.CfnInstanceGroupConfigPropsMixin.CloudWatchAlarmDefinitionProperty(
                        comparison_operator="comparisonOperator",
                        dimensions=[emr_mixins.CfnInstanceGroupConfigPropsMixin.MetricDimensionProperty(
                            key="key",
                            value="value"
                        )],
                        evaluation_periods=123,
                        metric_name="metricName",
                        namespace="namespace",
                        period=123,
                        statistic="statistic",
                        threshold=123,
                        unit="unit"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a6e90fcd70c649a4df2e253380d66f6d95bec57e2666628c65d600893e1d35d9)
                check_type(argname="argument cloud_watch_alarm_definition", value=cloud_watch_alarm_definition, expected_type=type_hints["cloud_watch_alarm_definition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_alarm_definition is not None:
                self._values["cloud_watch_alarm_definition"] = cloud_watch_alarm_definition

        @builtins.property
        def cloud_watch_alarm_definition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.CloudWatchAlarmDefinitionProperty"]]:
            '''The definition of a CloudWatch metric alarm.

            When the defined alarm conditions are met along with other trigger parameters, scaling activity begins.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-scalingtrigger.html#cfn-emr-instancegroupconfig-scalingtrigger-cloudwatchalarmdefinition
            '''
            result = self._values.get("cloud_watch_alarm_definition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceGroupConfigPropsMixin.CloudWatchAlarmDefinitionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingTriggerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceGroupConfigPropsMixin.SimpleScalingPolicyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "adjustment_type": "adjustmentType",
            "cool_down": "coolDown",
            "scaling_adjustment": "scalingAdjustment",
        },
    )
    class SimpleScalingPolicyConfigurationProperty:
        def __init__(
            self,
            *,
            adjustment_type: typing.Optional[builtins.str] = None,
            cool_down: typing.Optional[jsii.Number] = None,
            scaling_adjustment: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``SimpleScalingPolicyConfiguration`` is a subproperty of the ``ScalingAction`` property type.

            ``SimpleScalingPolicyConfiguration`` determines how an automatic scaling action adds or removes instances, the cooldown period, and the number of EC2 instances that are added each time the CloudWatch metric alarm condition is satisfied.

            :param adjustment_type: The way in which Amazon EC2 instances are added (if ``ScalingAdjustment`` is a positive number) or terminated (if ``ScalingAdjustment`` is a negative number) each time the scaling activity is triggered. ``CHANGE_IN_CAPACITY`` is the default. ``CHANGE_IN_CAPACITY`` indicates that the Amazon EC2 instance count increments or decrements by ``ScalingAdjustment`` , which should be expressed as an integer. ``PERCENT_CHANGE_IN_CAPACITY`` indicates the instance count increments or decrements by the percentage specified by ``ScalingAdjustment`` , which should be expressed as an integer. For example, 20 indicates an increase in 20% increments of cluster capacity. ``EXACT_CAPACITY`` indicates the scaling activity results in an instance group with the number of Amazon EC2 instances specified by ``ScalingAdjustment`` , which should be expressed as a positive integer.
            :param cool_down: The amount of time, in seconds, after a scaling activity completes before any further trigger-related scaling activities can start. The default value is 0.
            :param scaling_adjustment: The amount by which to scale in or scale out, based on the specified ``AdjustmentType`` . A positive value adds to the instance group's Amazon EC2 instance count while a negative number removes instances. If ``AdjustmentType`` is set to ``EXACT_CAPACITY`` , the number should only be a positive integer. If ``AdjustmentType`` is set to ``PERCENT_CHANGE_IN_CAPACITY`` , the value should express the percentage as an integer. For example, -20 indicates a decrease in 20% increments of cluster capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-simplescalingpolicyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                simple_scaling_policy_configuration_property = emr_mixins.CfnInstanceGroupConfigPropsMixin.SimpleScalingPolicyConfigurationProperty(
                    adjustment_type="adjustmentType",
                    cool_down=123,
                    scaling_adjustment=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9684490f0a184807a78c7d936f77be4e156167e2f8091e554eabde6825562745)
                check_type(argname="argument adjustment_type", value=adjustment_type, expected_type=type_hints["adjustment_type"])
                check_type(argname="argument cool_down", value=cool_down, expected_type=type_hints["cool_down"])
                check_type(argname="argument scaling_adjustment", value=scaling_adjustment, expected_type=type_hints["scaling_adjustment"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if adjustment_type is not None:
                self._values["adjustment_type"] = adjustment_type
            if cool_down is not None:
                self._values["cool_down"] = cool_down
            if scaling_adjustment is not None:
                self._values["scaling_adjustment"] = scaling_adjustment

        @builtins.property
        def adjustment_type(self) -> typing.Optional[builtins.str]:
            '''The way in which Amazon EC2 instances are added (if ``ScalingAdjustment`` is a positive number) or terminated (if ``ScalingAdjustment`` is a negative number) each time the scaling activity is triggered.

            ``CHANGE_IN_CAPACITY`` is the default. ``CHANGE_IN_CAPACITY`` indicates that the Amazon EC2 instance count increments or decrements by ``ScalingAdjustment`` , which should be expressed as an integer. ``PERCENT_CHANGE_IN_CAPACITY`` indicates the instance count increments or decrements by the percentage specified by ``ScalingAdjustment`` , which should be expressed as an integer. For example, 20 indicates an increase in 20% increments of cluster capacity. ``EXACT_CAPACITY`` indicates the scaling activity results in an instance group with the number of Amazon EC2 instances specified by ``ScalingAdjustment`` , which should be expressed as a positive integer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-simplescalingpolicyconfiguration.html#cfn-emr-instancegroupconfig-simplescalingpolicyconfiguration-adjustmenttype
            '''
            result = self._values.get("adjustment_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cool_down(self) -> typing.Optional[jsii.Number]:
            '''The amount of time, in seconds, after a scaling activity completes before any further trigger-related scaling activities can start.

            The default value is 0.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-simplescalingpolicyconfiguration.html#cfn-emr-instancegroupconfig-simplescalingpolicyconfiguration-cooldown
            '''
            result = self._values.get("cool_down")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def scaling_adjustment(self) -> typing.Optional[jsii.Number]:
            '''The amount by which to scale in or scale out, based on the specified ``AdjustmentType`` .

            A positive value adds to the instance group's Amazon EC2 instance count while a negative number removes instances. If ``AdjustmentType`` is set to ``EXACT_CAPACITY`` , the number should only be a positive integer. If ``AdjustmentType`` is set to ``PERCENT_CHANGE_IN_CAPACITY`` , the value should express the percentage as an integer. For example, -20 indicates a decrease in 20% increments of cluster capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-simplescalingpolicyconfiguration.html#cfn-emr-instancegroupconfig-simplescalingpolicyconfiguration-scalingadjustment
            '''
            result = self._values.get("scaling_adjustment")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SimpleScalingPolicyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnInstanceGroupConfigPropsMixin.VolumeSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "iops": "iops",
            "size_in_gb": "sizeInGb",
            "throughput": "throughput",
            "volume_type": "volumeType",
        },
    )
    class VolumeSpecificationProperty:
        def __init__(
            self,
            *,
            iops: typing.Optional[jsii.Number] = None,
            size_in_gb: typing.Optional[jsii.Number] = None,
            throughput: typing.Optional[jsii.Number] = None,
            volume_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``VolumeSpecification`` is a subproperty of the ``EbsBlockDeviceConfig`` property type.

            ``VolumeSecification`` determines the volume type, IOPS, and size (GiB) for EBS volumes attached to EC2 instances.

            :param iops: The number of I/O operations per second (IOPS) that the volume supports.
            :param size_in_gb: The volume size, in gibibytes (GiB). This can be a number from 1 - 1024. If the volume type is EBS-optimized, the minimum value is 10.
            :param throughput: The throughput, in mebibyte per second (MiB/s). This optional parameter can be a number from 125 - 1000 and is valid only for gp3 volumes.
            :param volume_type: The volume type. Volume types supported are gp3, gp2, io1, st1, sc1, and standard.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-volumespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                volume_specification_property = emr_mixins.CfnInstanceGroupConfigPropsMixin.VolumeSpecificationProperty(
                    iops=123,
                    size_in_gb=123,
                    throughput=123,
                    volume_type="volumeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a71ee40222aaecb78c0f90d17f5ee4556e9812c231f7dc2096822c4602bd0b98)
                check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
                check_type(argname="argument size_in_gb", value=size_in_gb, expected_type=type_hints["size_in_gb"])
                check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
                check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iops is not None:
                self._values["iops"] = iops
            if size_in_gb is not None:
                self._values["size_in_gb"] = size_in_gb
            if throughput is not None:
                self._values["throughput"] = throughput
            if volume_type is not None:
                self._values["volume_type"] = volume_type

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            '''The number of I/O operations per second (IOPS) that the volume supports.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-volumespecification.html#cfn-emr-instancegroupconfig-volumespecification-iops
            '''
            result = self._values.get("iops")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def size_in_gb(self) -> typing.Optional[jsii.Number]:
            '''The volume size, in gibibytes (GiB).

            This can be a number from 1 - 1024. If the volume type is EBS-optimized, the minimum value is 10.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-volumespecification.html#cfn-emr-instancegroupconfig-volumespecification-sizeingb
            '''
            result = self._values.get("size_in_gb")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throughput(self) -> typing.Optional[jsii.Number]:
            '''The throughput, in mebibyte per second (MiB/s).

            This optional parameter can be a number from 125 - 1000 and is valid only for gp3 volumes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-volumespecification.html#cfn-emr-instancegroupconfig-volumespecification-throughput
            '''
            result = self._values.get("throughput")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_type(self) -> typing.Optional[builtins.str]:
            '''The volume type.

            Volume types supported are gp3, gp2, io1, st1, sc1, and standard.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-instancegroupconfig-volumespecification.html#cfn-emr-instancegroupconfig-volumespecification-volumetype
            '''
            result = self._values.get("volume_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VolumeSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnSecurityConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "security_configuration": "securityConfiguration"},
)
class CfnSecurityConfigurationMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        security_configuration: typing.Any = None,
    ) -> None:
        '''Properties for CfnSecurityConfigurationPropsMixin.

        :param name: The name of the security configuration.
        :param security_configuration: The security configuration details in JSON format. For JSON parameters and examples, see `Use Security Configurations to Set Up Cluster Security <https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-security-configurations.html>`_ in the *Amazon EMR Management Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-securityconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
            
            # security_configuration: Any
            
            cfn_security_configuration_mixin_props = emr_mixins.CfnSecurityConfigurationMixinProps(
                name="name",
                security_configuration=security_configuration
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24f94ae925d3a79ed74c0d6e33edbfd124fc28186e48eb59049e886563b8eab4)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument security_configuration", value=security_configuration, expected_type=type_hints["security_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if security_configuration is not None:
            self._values["security_configuration"] = security_configuration

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the security configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-securityconfiguration.html#cfn-emr-securityconfiguration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_configuration(self) -> typing.Any:
        '''The security configuration details in JSON format.

        For JSON parameters and examples, see `Use Security Configurations to Set Up Cluster Security <https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-security-configurations.html>`_ in the *Amazon EMR Management Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-securityconfiguration.html#cfn-emr-securityconfiguration-securityconfiguration
        '''
        result = self._values.get("security_configuration")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecurityConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSecurityConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnSecurityConfigurationPropsMixin",
):
    '''Use a ``SecurityConfiguration`` resource to configure data encryption, Kerberos authentication (available in Amazon EMR release version 5.10.0 and later), and Amazon S3 authorization for EMRFS (available in EMR 5.10.0 and later). You can re-use a security configuration for any number of clusters in your account. For more information and example security configuration JSON objects, see `Create a Security Configuration <https://docs.aws.amazon.com//emr/latest/ManagementGuide/emr-create-security-configuration.html>`_ in the *Amazon EMR Management Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-securityconfiguration.html
    :cloudformationResource: AWS::EMR::SecurityConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
        
        # security_configuration: Any
        
        cfn_security_configuration_props_mixin = emr_mixins.CfnSecurityConfigurationPropsMixin(emr_mixins.CfnSecurityConfigurationMixinProps(
            name="name",
            security_configuration=security_configuration
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSecurityConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EMR::SecurityConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__552c3d60cdabe23cb108032a0949dfc7a02ff44850559c5369c165cd33730a98)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fac1fbc78ca6908625f179ec2efd0c678a5ec341886c93fe3ca7fb382ea70c26)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a530b48da0584077fdfd5f87b3bb98255b399fb5d2010085ec98cf242896b1fa)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSecurityConfigurationMixinProps:
        return typing.cast(CfnSecurityConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnStepMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "action_on_failure": "actionOnFailure",
        "hadoop_jar_step": "hadoopJarStep",
        "job_flow_id": "jobFlowId",
        "name": "name",
    },
)
class CfnStepMixinProps:
    def __init__(
        self,
        *,
        action_on_failure: typing.Optional[builtins.str] = None,
        hadoop_jar_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStepPropsMixin.HadoopJarStepConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        job_flow_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnStepPropsMixin.

        :param action_on_failure: This specifies what action to take when the cluster step fails. Possible values are ``CANCEL_AND_WAIT`` and ``CONTINUE`` .
        :param hadoop_jar_step: The ``HadoopJarStepConfig`` property type specifies a job flow step consisting of a JAR file whose main function will be executed. The main function submits a job for the cluster to execute as a step on the master node, and then waits for the job to finish or fail before executing subsequent steps.
        :param job_flow_id: A string that uniquely identifies the cluster (job flow).
        :param name: The name of the cluster step.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-step.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
            
            cfn_step_mixin_props = emr_mixins.CfnStepMixinProps(
                action_on_failure="actionOnFailure",
                hadoop_jar_step=emr_mixins.CfnStepPropsMixin.HadoopJarStepConfigProperty(
                    args=["args"],
                    jar="jar",
                    main_class="mainClass",
                    step_properties=[emr_mixins.CfnStepPropsMixin.KeyValueProperty(
                        key="key",
                        value="value"
                    )]
                ),
                job_flow_id="jobFlowId",
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96859f2b71b2d15232c6d6382e5b9b9ad69c3ac20a78c2463fb2296ce4c6a62b)
            check_type(argname="argument action_on_failure", value=action_on_failure, expected_type=type_hints["action_on_failure"])
            check_type(argname="argument hadoop_jar_step", value=hadoop_jar_step, expected_type=type_hints["hadoop_jar_step"])
            check_type(argname="argument job_flow_id", value=job_flow_id, expected_type=type_hints["job_flow_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action_on_failure is not None:
            self._values["action_on_failure"] = action_on_failure
        if hadoop_jar_step is not None:
            self._values["hadoop_jar_step"] = hadoop_jar_step
        if job_flow_id is not None:
            self._values["job_flow_id"] = job_flow_id
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def action_on_failure(self) -> typing.Optional[builtins.str]:
        '''This specifies what action to take when the cluster step fails.

        Possible values are ``CANCEL_AND_WAIT`` and ``CONTINUE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-step.html#cfn-emr-step-actiononfailure
        '''
        result = self._values.get("action_on_failure")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hadoop_jar_step(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStepPropsMixin.HadoopJarStepConfigProperty"]]:
        '''The ``HadoopJarStepConfig`` property type specifies a job flow step consisting of a JAR file whose main function will be executed.

        The main function submits a job for the cluster to execute as a step on the master node, and then waits for the job to finish or fail before executing subsequent steps.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-step.html#cfn-emr-step-hadoopjarstep
        '''
        result = self._values.get("hadoop_jar_step")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStepPropsMixin.HadoopJarStepConfigProperty"]], result)

    @builtins.property
    def job_flow_id(self) -> typing.Optional[builtins.str]:
        '''A string that uniquely identifies the cluster (job flow).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-step.html#cfn-emr-step-jobflowid
        '''
        result = self._values.get("job_flow_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the cluster step.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-step.html#cfn-emr-step-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStepMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStepPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnStepPropsMixin",
):
    '''Use ``Step`` to specify a cluster (job flow) step, which runs only on the master node.

    Steps are used to submit data processing jobs to a cluster.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-step.html
    :cloudformationResource: AWS::EMR::Step
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
        
        cfn_step_props_mixin = emr_mixins.CfnStepPropsMixin(emr_mixins.CfnStepMixinProps(
            action_on_failure="actionOnFailure",
            hadoop_jar_step=emr_mixins.CfnStepPropsMixin.HadoopJarStepConfigProperty(
                args=["args"],
                jar="jar",
                main_class="mainClass",
                step_properties=[emr_mixins.CfnStepPropsMixin.KeyValueProperty(
                    key="key",
                    value="value"
                )]
            ),
            job_flow_id="jobFlowId",
            name="name"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStepMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EMR::Step``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90bf5f5b208fc06a8aa867a1733ae5ede81006ade422abaad7db8efd642a241a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e5232e54ca264e523ad2d208c6e4ab8c71792fe674eafd86902dd96186602db)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41c7b4807638479dd3844e131fef720d2d44c6d2963b05e2d03a6e4958297c14)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStepMixinProps:
        return typing.cast(CfnStepMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnStepPropsMixin.HadoopJarStepConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "args": "args",
            "jar": "jar",
            "main_class": "mainClass",
            "step_properties": "stepProperties",
        },
    )
    class HadoopJarStepConfigProperty:
        def __init__(
            self,
            *,
            args: typing.Optional[typing.Sequence[builtins.str]] = None,
            jar: typing.Optional[builtins.str] = None,
            main_class: typing.Optional[builtins.str] = None,
            step_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStepPropsMixin.KeyValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A job flow step consisting of a JAR file whose main function will be executed.

            The main function submits a job for Hadoop to execute and waits for the job to finish or fail.

            :param args: A list of command line arguments passed to the JAR file's main function when executed.
            :param jar: A path to a JAR file run during the step.
            :param main_class: The name of the main class in the specified Java file. If not specified, the JAR file should specify a Main-Class in its manifest file.
            :param step_properties: A list of Java properties that are set when the step runs. You can use these properties to pass key value pairs to your main function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-step-hadoopjarstepconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                hadoop_jar_step_config_property = emr_mixins.CfnStepPropsMixin.HadoopJarStepConfigProperty(
                    args=["args"],
                    jar="jar",
                    main_class="mainClass",
                    step_properties=[emr_mixins.CfnStepPropsMixin.KeyValueProperty(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__47c9e69c8042d8b17dbac8c2525fbe42bfebd0f4753ea97c6581c9af015304fe)
                check_type(argname="argument args", value=args, expected_type=type_hints["args"])
                check_type(argname="argument jar", value=jar, expected_type=type_hints["jar"])
                check_type(argname="argument main_class", value=main_class, expected_type=type_hints["main_class"])
                check_type(argname="argument step_properties", value=step_properties, expected_type=type_hints["step_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if args is not None:
                self._values["args"] = args
            if jar is not None:
                self._values["jar"] = jar
            if main_class is not None:
                self._values["main_class"] = main_class
            if step_properties is not None:
                self._values["step_properties"] = step_properties

        @builtins.property
        def args(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of command line arguments passed to the JAR file's main function when executed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-step-hadoopjarstepconfig.html#cfn-emr-step-hadoopjarstepconfig-args
            '''
            result = self._values.get("args")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def jar(self) -> typing.Optional[builtins.str]:
            '''A path to a JAR file run during the step.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-step-hadoopjarstepconfig.html#cfn-emr-step-hadoopjarstepconfig-jar
            '''
            result = self._values.get("jar")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def main_class(self) -> typing.Optional[builtins.str]:
            '''The name of the main class in the specified Java file.

            If not specified, the JAR file should specify a Main-Class in its manifest file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-step-hadoopjarstepconfig.html#cfn-emr-step-hadoopjarstepconfig-mainclass
            '''
            result = self._values.get("main_class")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def step_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStepPropsMixin.KeyValueProperty"]]]]:
            '''A list of Java properties that are set when the step runs.

            You can use these properties to pass key value pairs to your main function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-step-hadoopjarstepconfig.html#cfn-emr-step-hadoopjarstepconfig-stepproperties
            '''
            result = self._values.get("step_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStepPropsMixin.KeyValueProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HadoopJarStepConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnStepPropsMixin.KeyValueProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class KeyValueProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``KeyValue`` is a subproperty of the ``HadoopJarStepConfig`` property type.

            ``KeyValue`` is used to pass parameters to a step.

            :param key: The unique identifier of a key-value pair.
            :param value: The value part of the identified key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-step-keyvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
                
                key_value_property = emr_mixins.CfnStepPropsMixin.KeyValueProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c3eb52491c61fdd14963a366149c8c25d0e9e085390d2995f96109b4b2f83ed2)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The unique identifier of a key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-step-keyvalue.html#cfn-emr-step-keyvalue-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value part of the identified key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emr-step-keyvalue.html#cfn-emr-step-keyvalue-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeyValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnStudioMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auth_mode": "authMode",
        "default_s3_location": "defaultS3Location",
        "description": "description",
        "encryption_key_arn": "encryptionKeyArn",
        "engine_security_group_id": "engineSecurityGroupId",
        "idc_instance_arn": "idcInstanceArn",
        "idc_user_assignment": "idcUserAssignment",
        "idp_auth_url": "idpAuthUrl",
        "idp_relay_state_parameter_name": "idpRelayStateParameterName",
        "name": "name",
        "service_role": "serviceRole",
        "subnet_ids": "subnetIds",
        "tags": "tags",
        "trusted_identity_propagation_enabled": "trustedIdentityPropagationEnabled",
        "user_role": "userRole",
        "vpc_id": "vpcId",
        "workspace_security_group_id": "workspaceSecurityGroupId",
    },
)
class CfnStudioMixinProps:
    def __init__(
        self,
        *,
        auth_mode: typing.Optional[builtins.str] = None,
        default_s3_location: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_key_arn: typing.Optional[builtins.str] = None,
        engine_security_group_id: typing.Optional[builtins.str] = None,
        idc_instance_arn: typing.Optional[builtins.str] = None,
        idc_user_assignment: typing.Optional[builtins.str] = None,
        idp_auth_url: typing.Optional[builtins.str] = None,
        idp_relay_state_parameter_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        service_role: typing.Optional[builtins.str] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        trusted_identity_propagation_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        user_role: typing.Optional[builtins.str] = None,
        vpc_id: typing.Optional[builtins.str] = None,
        workspace_security_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnStudioPropsMixin.

        :param auth_mode: Specifies whether the Studio authenticates users using IAM Identity Center or IAM.
        :param default_s3_location: The Amazon S3 location to back up EMR Studio Workspaces and notebook files.
        :param description: A detailed description of the Amazon EMR Studio.
        :param encryption_key_arn: The AWS key identifier (ARN) used to encrypt Amazon EMR Studio workspace and notebook files when backed up to Amazon S3.
        :param engine_security_group_id: The ID of the Amazon EMR Studio Engine security group. The Engine security group allows inbound network traffic from the Workspace security group, and it must be in the same VPC specified by ``VpcId`` .
        :param idc_instance_arn: The ARN of the IAM Identity Center instance the Studio application belongs to.
        :param idc_user_assignment: Indicates whether the Studio has ``REQUIRED`` or ``OPTIONAL`` IAM Identity Center user assignment. If the value is set to ``REQUIRED`` , users must be explicitly assigned to the Studio application to access the Studio.
        :param idp_auth_url: Your identity provider's authentication endpoint. Amazon EMR Studio redirects federated users to this endpoint for authentication when logging in to a Studio with the Studio URL.
        :param idp_relay_state_parameter_name: The name of your identity provider's ``RelayState`` parameter.
        :param name: A descriptive name for the Amazon EMR Studio.
        :param service_role: The Amazon Resource Name (ARN) of the IAM role that will be assumed by the Amazon EMR Studio. The service role provides a way for Amazon EMR Studio to interoperate with other AWS services.
        :param subnet_ids: A list of subnet IDs to associate with the Amazon EMR Studio. A Studio can have a maximum of 5 subnets. The subnets must belong to the VPC specified by ``VpcId`` . Studio users can create a Workspace in any of the specified subnets.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param trusted_identity_propagation_enabled: Indicates whether the Studio has Trusted identity propagation enabled. The default value is ``false`` .
        :param user_role: The Amazon Resource Name (ARN) of the IAM user role that will be assumed by users and groups logged in to a Studio. The permissions attached to this IAM role can be scoped down for each user or group using session policies. You only need to specify ``UserRole`` when you set ``AuthMode`` to ``SSO`` .
        :param vpc_id: The ID of the Amazon Virtual Private Cloud (Amazon VPC) to associate with the Studio.
        :param workspace_security_group_id: The ID of the Workspace security group associated with the Amazon EMR Studio. The Workspace security group allows outbound network traffic to resources in the Engine security group and to the internet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studio.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
            
            cfn_studio_mixin_props = emr_mixins.CfnStudioMixinProps(
                auth_mode="authMode",
                default_s3_location="defaultS3Location",
                description="description",
                encryption_key_arn="encryptionKeyArn",
                engine_security_group_id="engineSecurityGroupId",
                idc_instance_arn="idcInstanceArn",
                idc_user_assignment="idcUserAssignment",
                idp_auth_url="idpAuthUrl",
                idp_relay_state_parameter_name="idpRelayStateParameterName",
                name="name",
                service_role="serviceRole",
                subnet_ids=["subnetIds"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                trusted_identity_propagation_enabled=False,
                user_role="userRole",
                vpc_id="vpcId",
                workspace_security_group_id="workspaceSecurityGroupId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8260a0531455655cfc01de93da840dcd13148c961f30ea0d6506bbcf0aa7c14)
            check_type(argname="argument auth_mode", value=auth_mode, expected_type=type_hints["auth_mode"])
            check_type(argname="argument default_s3_location", value=default_s3_location, expected_type=type_hints["default_s3_location"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encryption_key_arn", value=encryption_key_arn, expected_type=type_hints["encryption_key_arn"])
            check_type(argname="argument engine_security_group_id", value=engine_security_group_id, expected_type=type_hints["engine_security_group_id"])
            check_type(argname="argument idc_instance_arn", value=idc_instance_arn, expected_type=type_hints["idc_instance_arn"])
            check_type(argname="argument idc_user_assignment", value=idc_user_assignment, expected_type=type_hints["idc_user_assignment"])
            check_type(argname="argument idp_auth_url", value=idp_auth_url, expected_type=type_hints["idp_auth_url"])
            check_type(argname="argument idp_relay_state_parameter_name", value=idp_relay_state_parameter_name, expected_type=type_hints["idp_relay_state_parameter_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument trusted_identity_propagation_enabled", value=trusted_identity_propagation_enabled, expected_type=type_hints["trusted_identity_propagation_enabled"])
            check_type(argname="argument user_role", value=user_role, expected_type=type_hints["user_role"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument workspace_security_group_id", value=workspace_security_group_id, expected_type=type_hints["workspace_security_group_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_mode is not None:
            self._values["auth_mode"] = auth_mode
        if default_s3_location is not None:
            self._values["default_s3_location"] = default_s3_location
        if description is not None:
            self._values["description"] = description
        if encryption_key_arn is not None:
            self._values["encryption_key_arn"] = encryption_key_arn
        if engine_security_group_id is not None:
            self._values["engine_security_group_id"] = engine_security_group_id
        if idc_instance_arn is not None:
            self._values["idc_instance_arn"] = idc_instance_arn
        if idc_user_assignment is not None:
            self._values["idc_user_assignment"] = idc_user_assignment
        if idp_auth_url is not None:
            self._values["idp_auth_url"] = idp_auth_url
        if idp_relay_state_parameter_name is not None:
            self._values["idp_relay_state_parameter_name"] = idp_relay_state_parameter_name
        if name is not None:
            self._values["name"] = name
        if service_role is not None:
            self._values["service_role"] = service_role
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags
        if trusted_identity_propagation_enabled is not None:
            self._values["trusted_identity_propagation_enabled"] = trusted_identity_propagation_enabled
        if user_role is not None:
            self._values["user_role"] = user_role
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id
        if workspace_security_group_id is not None:
            self._values["workspace_security_group_id"] = workspace_security_group_id

    @builtins.property
    def auth_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the Studio authenticates users using IAM Identity Center or IAM.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studio.html#cfn-emr-studio-authmode
        '''
        result = self._values.get("auth_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_s3_location(self) -> typing.Optional[builtins.str]:
        '''The Amazon S3 location to back up EMR Studio Workspaces and notebook files.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studio.html#cfn-emr-studio-defaults3location
        '''
        result = self._values.get("default_s3_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A detailed description of the Amazon EMR Studio.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studio.html#cfn-emr-studio-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key_arn(self) -> typing.Optional[builtins.str]:
        '''The AWS  key identifier (ARN) used to encrypt Amazon EMR Studio workspace and notebook files when backed up to Amazon S3.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studio.html#cfn-emr-studio-encryptionkeyarn
        '''
        result = self._values.get("encryption_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_security_group_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Amazon EMR Studio Engine security group.

        The Engine security group allows inbound network traffic from the Workspace security group, and it must be in the same VPC specified by ``VpcId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studio.html#cfn-emr-studio-enginesecuritygroupid
        '''
        result = self._values.get("engine_security_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idc_instance_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM Identity Center instance the Studio application belongs to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studio.html#cfn-emr-studio-idcinstancearn
        '''
        result = self._values.get("idc_instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idc_user_assignment(self) -> typing.Optional[builtins.str]:
        '''Indicates whether the Studio has ``REQUIRED`` or ``OPTIONAL`` IAM Identity Center user assignment.

        If the value is set to ``REQUIRED`` , users must be explicitly assigned to the Studio application to access the Studio.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studio.html#cfn-emr-studio-idcuserassignment
        '''
        result = self._values.get("idc_user_assignment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idp_auth_url(self) -> typing.Optional[builtins.str]:
        '''Your identity provider's authentication endpoint.

        Amazon EMR Studio redirects federated users to this endpoint for authentication when logging in to a Studio with the Studio URL.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studio.html#cfn-emr-studio-idpauthurl
        '''
        result = self._values.get("idp_auth_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idp_relay_state_parameter_name(self) -> typing.Optional[builtins.str]:
        '''The name of your identity provider's ``RelayState`` parameter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studio.html#cfn-emr-studio-idprelaystateparametername
        '''
        result = self._values.get("idp_relay_state_parameter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A descriptive name for the Amazon EMR Studio.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studio.html#cfn-emr-studio-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_role(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role that will be assumed by the Amazon EMR Studio.

        The service role provides a way for Amazon EMR Studio to interoperate with other AWS services.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studio.html#cfn-emr-studio-servicerole
        '''
        result = self._values.get("service_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of subnet IDs to associate with the Amazon EMR Studio.

        A Studio can have a maximum of 5 subnets. The subnets must belong to the VPC specified by ``VpcId`` . Studio users can create a Workspace in any of the specified subnets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studio.html#cfn-emr-studio-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studio.html#cfn-emr-studio-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def trusted_identity_propagation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether the Studio has Trusted identity propagation enabled.

        The default value is ``false`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studio.html#cfn-emr-studio-trustedidentitypropagationenabled
        '''
        result = self._values.get("trusted_identity_propagation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def user_role(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM user role that will be assumed by users and groups logged in to a Studio.

        The permissions attached to this IAM role can be scoped down for each user or group using session policies. You only need to specify ``UserRole`` when you set ``AuthMode`` to ``SSO`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studio.html#cfn-emr-studio-userrole
        '''
        result = self._values.get("user_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Amazon Virtual Private Cloud (Amazon VPC) to associate with the Studio.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studio.html#cfn-emr-studio-vpcid
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspace_security_group_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Workspace security group associated with the Amazon EMR Studio.

        The Workspace security group allows outbound network traffic to resources in the Engine security group and to the internet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studio.html#cfn-emr-studio-workspacesecuritygroupid
        '''
        result = self._values.get("workspace_security_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStudioMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStudioPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnStudioPropsMixin",
):
    '''The ``AWS::EMR::Studio`` resource specifies an Amazon EMR Studio.

    An EMR Studio is a web-based, integrated development environment for fully managed Jupyter notebooks that run on Amazon EMR clusters. For more information, see the `*Amazon EMR Management Guide* <https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-studio.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studio.html
    :cloudformationResource: AWS::EMR::Studio
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
        
        cfn_studio_props_mixin = emr_mixins.CfnStudioPropsMixin(emr_mixins.CfnStudioMixinProps(
            auth_mode="authMode",
            default_s3_location="defaultS3Location",
            description="description",
            encryption_key_arn="encryptionKeyArn",
            engine_security_group_id="engineSecurityGroupId",
            idc_instance_arn="idcInstanceArn",
            idc_user_assignment="idcUserAssignment",
            idp_auth_url="idpAuthUrl",
            idp_relay_state_parameter_name="idpRelayStateParameterName",
            name="name",
            service_role="serviceRole",
            subnet_ids=["subnetIds"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            trusted_identity_propagation_enabled=False,
            user_role="userRole",
            vpc_id="vpcId",
            workspace_security_group_id="workspaceSecurityGroupId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStudioMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EMR::Studio``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e36335ec2c97ce0928e933952e3bc052a72223322dd13bf60764ef6b669e2b84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b9283e18b0712dc32cd929dc9087b902cd8870da9502f6e1de2fbc791500e80)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3224b6509b4d3aa9aee4c70ddf78cef44d54660a2b8af4ea6202c6f340d2254e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStudioMixinProps:
        return typing.cast(CfnStudioMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnStudioSessionMappingMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "identity_name": "identityName",
        "identity_type": "identityType",
        "session_policy_arn": "sessionPolicyArn",
        "studio_id": "studioId",
    },
)
class CfnStudioSessionMappingMixinProps:
    def __init__(
        self,
        *,
        identity_name: typing.Optional[builtins.str] = None,
        identity_type: typing.Optional[builtins.str] = None,
        session_policy_arn: typing.Optional[builtins.str] = None,
        studio_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnStudioSessionMappingPropsMixin.

        :param identity_name: The name of the user or group. For more information, see `UserName <https://docs.aws.amazon.com/singlesignon/latest/IdentityStoreAPIReference/API_User.html#singlesignon-Type-User-UserName>`_ and `DisplayName <https://docs.aws.amazon.com/singlesignon/latest/IdentityStoreAPIReference/API_Group.html#singlesignon-Type-Group-DisplayName>`_ in the *IAM Identity Center Identity Store API Reference* .
        :param identity_type: Specifies whether the identity to map to the Amazon EMR Studio is a user or a group.
        :param session_policy_arn: The Amazon Resource Name (ARN) for the session policy that will be applied to the user or group. Session policies refine Studio user permissions without the need to use multiple IAM user roles. For more information, see `Create an EMR Studio user role with session policies <https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-studio-user-role.html>`_ in the *Amazon EMR Management Guide* .
        :param studio_id: The ID of the Amazon EMR Studio to which the user or group will be mapped.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studiosessionmapping.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
            
            cfn_studio_session_mapping_mixin_props = emr_mixins.CfnStudioSessionMappingMixinProps(
                identity_name="identityName",
                identity_type="identityType",
                session_policy_arn="sessionPolicyArn",
                studio_id="studioId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e3fb7d872edee89a8d3bf295eb734906f069ca4565fd69c681fb003e1d1bb45)
            check_type(argname="argument identity_name", value=identity_name, expected_type=type_hints["identity_name"])
            check_type(argname="argument identity_type", value=identity_type, expected_type=type_hints["identity_type"])
            check_type(argname="argument session_policy_arn", value=session_policy_arn, expected_type=type_hints["session_policy_arn"])
            check_type(argname="argument studio_id", value=studio_id, expected_type=type_hints["studio_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identity_name is not None:
            self._values["identity_name"] = identity_name
        if identity_type is not None:
            self._values["identity_type"] = identity_type
        if session_policy_arn is not None:
            self._values["session_policy_arn"] = session_policy_arn
        if studio_id is not None:
            self._values["studio_id"] = studio_id

    @builtins.property
    def identity_name(self) -> typing.Optional[builtins.str]:
        '''The name of the user or group.

        For more information, see `UserName <https://docs.aws.amazon.com/singlesignon/latest/IdentityStoreAPIReference/API_User.html#singlesignon-Type-User-UserName>`_ and `DisplayName <https://docs.aws.amazon.com/singlesignon/latest/IdentityStoreAPIReference/API_Group.html#singlesignon-Type-Group-DisplayName>`_ in the *IAM Identity Center Identity Store API Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studiosessionmapping.html#cfn-emr-studiosessionmapping-identityname
        '''
        result = self._values.get("identity_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_type(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the identity to map to the Amazon EMR Studio is a user or a group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studiosessionmapping.html#cfn-emr-studiosessionmapping-identitytype
        '''
        result = self._values.get("identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_policy_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) for the session policy that will be applied to the user or group.

        Session policies refine Studio user permissions without the need to use multiple IAM user roles. For more information, see `Create an EMR Studio user role with session policies <https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-studio-user-role.html>`_ in the *Amazon EMR Management Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studiosessionmapping.html#cfn-emr-studiosessionmapping-sessionpolicyarn
        '''
        result = self._values.get("session_policy_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def studio_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Amazon EMR Studio to which the user or group will be mapped.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studiosessionmapping.html#cfn-emr-studiosessionmapping-studioid
        '''
        result = self._values.get("studio_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStudioSessionMappingMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStudioSessionMappingPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnStudioSessionMappingPropsMixin",
):
    '''The ``AWS::EMR::StudioSessionMapping`` resource is an Amazon EMR resource type that maps a user or group to the Amazon EMR Studio specified by ``StudioId`` , and applies a session policy that defines Studio permissions for that user or group.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studiosessionmapping.html
    :cloudformationResource: AWS::EMR::StudioSessionMapping
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
        
        cfn_studio_session_mapping_props_mixin = emr_mixins.CfnStudioSessionMappingPropsMixin(emr_mixins.CfnStudioSessionMappingMixinProps(
            identity_name="identityName",
            identity_type="identityType",
            session_policy_arn="sessionPolicyArn",
            studio_id="studioId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStudioSessionMappingMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EMR::StudioSessionMapping``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24bc7e9b49238c5aeebaa283f4cff15030355f6f3f12716f2e7e27855a761a67)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6defc92c67b1718d25b0ab3211e2a6f9f9ff74bbb0e361dd2d0930e72c4afc99)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__affe7abef0671569b8faa7e30a97d0c942cf717552555af72f3b7c4dda9b28ba)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStudioSessionMappingMixinProps:
        return typing.cast(CfnStudioSessionMappingMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnWALWorkspaceMixinProps",
    jsii_struct_bases=[],
    name_mapping={"tags": "tags", "wal_workspace_name": "walWorkspaceName"},
)
class CfnWALWorkspaceMixinProps:
    def __init__(
        self,
        *,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        wal_workspace_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnWALWorkspacePropsMixin.

        :param tags: An array of key-value pairs to apply to this resource.
        :param wal_workspace_name: The name of the emrwal container.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-walworkspace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
            
            cfn_wALWorkspace_mixin_props = emr_mixins.CfnWALWorkspaceMixinProps(
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                wal_workspace_name="walWorkspaceName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d16ea27f58bade02ffda73860f7a0230620270a16f509f4fe4992a0ce01ae9a1)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument wal_workspace_name", value=wal_workspace_name, expected_type=type_hints["wal_workspace_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tags is not None:
            self._values["tags"] = tags
        if wal_workspace_name is not None:
            self._values["wal_workspace_name"] = wal_workspace_name

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-walworkspace.html#cfn-emr-walworkspace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def wal_workspace_name(self) -> typing.Optional[builtins.str]:
        '''The name of the emrwal container.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-walworkspace.html#cfn-emr-walworkspace-walworkspacename
        '''
        result = self._values.get("wal_workspace_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWALWorkspaceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWALWorkspacePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_emr.mixins.CfnWALWorkspacePropsMixin",
):
    '''http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-walworkspace.html.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-walworkspace.html
    :cloudformationResource: AWS::EMR::WALWorkspace
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_emr import mixins as emr_mixins
        
        cfn_wALWorkspace_props_mixin = emr_mixins.CfnWALWorkspacePropsMixin(emr_mixins.CfnWALWorkspaceMixinProps(
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            wal_workspace_name="walWorkspaceName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWALWorkspaceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EMR::WALWorkspace``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5edfc4a2b13ea9251e7fff378e07d99e3d31a98aa84c9c994f084232e7af325)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70dee9c33c846bbe17e7005e0b66827e2805791e08c77cfe582ce5619de529a3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__779406d641d8b5ce3a14d6fee5c33b9087040506734f116b011bd6bc0f48c824)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWALWorkspaceMixinProps:
        return typing.cast(CfnWALWorkspaceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnClusterMixinProps",
    "CfnClusterPropsMixin",
    "CfnInstanceFleetConfigMixinProps",
    "CfnInstanceFleetConfigPropsMixin",
    "CfnInstanceGroupConfigMixinProps",
    "CfnInstanceGroupConfigPropsMixin",
    "CfnSecurityConfigurationMixinProps",
    "CfnSecurityConfigurationPropsMixin",
    "CfnStepMixinProps",
    "CfnStepPropsMixin",
    "CfnStudioMixinProps",
    "CfnStudioPropsMixin",
    "CfnStudioSessionMappingMixinProps",
    "CfnStudioSessionMappingPropsMixin",
    "CfnWALWorkspaceMixinProps",
    "CfnWALWorkspacePropsMixin",
]

publication.publish()

def _typecheckingstub__374ecef1a8ce47b143e5bb688cdefd4145db6e3fbded3fc66feb170c2f4f5f2d(
    *,
    additional_info: typing.Any = None,
    applications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ApplicationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    auto_scaling_role: typing.Optional[builtins.str] = None,
    auto_termination_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.AutoTerminationPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    bootstrap_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.BootstrapActionConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    custom_ami_id: typing.Optional[builtins.str] = None,
    ebs_root_volume_iops: typing.Optional[jsii.Number] = None,
    ebs_root_volume_size: typing.Optional[jsii.Number] = None,
    ebs_root_volume_throughput: typing.Optional[jsii.Number] = None,
    instances: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.JobFlowInstancesConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    job_flow_role: typing.Optional[builtins.str] = None,
    kerberos_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.KerberosAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    log_encryption_kms_key_id: typing.Optional[builtins.str] = None,
    log_uri: typing.Optional[builtins.str] = None,
    managed_scaling_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ManagedScalingPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    os_release_label: typing.Optional[builtins.str] = None,
    placement_group_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.PlacementGroupConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    release_label: typing.Optional[builtins.str] = None,
    scale_down_behavior: typing.Optional[builtins.str] = None,
    security_configuration: typing.Optional[builtins.str] = None,
    service_role: typing.Optional[builtins.str] = None,
    step_concurrency_level: typing.Optional[jsii.Number] = None,
    steps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.StepConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    visible_to_all_users: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be0e3815d56c8d94e32e954f5182272836bd577c1a862227385c407f4c429cb(
    props: typing.Union[CfnClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30250d2a222cb04deeadeb41cdb4bb86c5afd046c3678e049c587f83843c3046(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a6af80959e75ef46f2337b2b13e93d317b68ac58d9a0c93628e5492e61ced7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b972970d54dc28e719d3571ef5311f50da4a5ca3958705ff06e0d0d6e4544d(
    *,
    additional_info: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90423eee746a6352a1e7b6faa2b7022e2bcb3ce66963ac69bc3d53a6bf45af7a(
    *,
    constraints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ScalingConstraintsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ScalingRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3744fc65af35fe1bf1985614d6b914688348f2f698b7bb9bade56ea26c8b433(
    *,
    idle_timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddbdce83a7051bc19988968c2bfc9cb21364cc336174208be38f020e4aef3b01(
    *,
    name: typing.Optional[builtins.str] = None,
    script_bootstrap_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ScriptBootstrapActionConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d74e79a40522922435770eef174ae8d6b82d2e0734bfddc665ec7364d3da16e(
    *,
    comparison_operator: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.MetricDimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    metric_name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    period: typing.Optional[jsii.Number] = None,
    statistic: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7f419eca790e3fe3daf30619c1eceff7cc7c1d61868a2417872391f835dd01f(
    *,
    maximum_capacity_units: typing.Optional[jsii.Number] = None,
    maximum_core_capacity_units: typing.Optional[jsii.Number] = None,
    maximum_on_demand_capacity_units: typing.Optional[jsii.Number] = None,
    minimum_capacity_units: typing.Optional[jsii.Number] = None,
    unit_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf72058db79dd58a33c7009dc2e8b680074e3bef0f9ca22e7dbb1ba7eb17388(
    *,
    classification: typing.Optional[builtins.str] = None,
    configuration_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b07931a38b8b97d5694e60592e817680e02e9b368c6dd300c2ca100eae108b(
    *,
    volume_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.VolumeSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    volumes_per_instance: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b2a429a617d970c3ca67459990b41d71da688cb2425955ab43d0c8373e73f73(
    *,
    ebs_block_device_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.EbsBlockDeviceConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ebs_optimized: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc366d15f8089d695d4625a1ba2c2e0ed8e08311dbb1e86b6cfd548166f42d6(
    *,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    jar: typing.Optional[builtins.str] = None,
    main_class: typing.Optional[builtins.str] = None,
    step_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.KeyValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e32126c64841a5f2e79ff4c4abb5516688e8cc7bd9c99850d4a2c4edcc9ca242(
    *,
    instance_type_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.InstanceTypeConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    launch_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.InstanceFleetProvisioningSpecificationsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    resize_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.InstanceFleetResizingSpecificationsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_on_demand_capacity: typing.Optional[jsii.Number] = None,
    target_spot_capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b22e3487ab445732197a935e1de936dd2775195cfb50e42304a742efb207cf(
    *,
    on_demand_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.OnDemandProvisioningSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    spot_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.SpotProvisioningSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa44fe8693d380822026d857053af5c73c799c2c788531957b52f4230a95f09(
    *,
    on_demand_resize_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.OnDemandResizingSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    spot_resize_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.SpotResizingSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53e704834a5666e3a90e9b39ed367c5bc0f9e0b3e6ce7050f8de57a113138ce(
    *,
    auto_scaling_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.AutoScalingPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    bid_price: typing.Optional[builtins.str] = None,
    configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    custom_ami_id: typing.Optional[builtins.str] = None,
    ebs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.EbsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_count: typing.Optional[jsii.Number] = None,
    instance_type: typing.Optional[builtins.str] = None,
    market: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae7c2d9cdf83102c76b38012e28092a75ee0b560545c0c6a2495b10fd2e061f(
    *,
    bid_price: typing.Optional[builtins.str] = None,
    bid_price_as_percentage_of_on_demand_price: typing.Optional[jsii.Number] = None,
    configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    custom_ami_id: typing.Optional[builtins.str] = None,
    ebs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.EbsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_type: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    weighted_capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58fd405a49bf1b47baa02460259843f664e5a7f8fecaa14d7738928c18a30871(
    *,
    additional_master_security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    additional_slave_security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    core_instance_fleet: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.InstanceFleetConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    core_instance_group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.InstanceGroupConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ec2_key_name: typing.Optional[builtins.str] = None,
    ec2_subnet_id: typing.Optional[builtins.str] = None,
    ec2_subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    emr_managed_master_security_group: typing.Optional[builtins.str] = None,
    emr_managed_slave_security_group: typing.Optional[builtins.str] = None,
    hadoop_version: typing.Optional[builtins.str] = None,
    keep_job_flow_alive_when_no_steps: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    master_instance_fleet: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.InstanceFleetConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    master_instance_group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.InstanceGroupConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    placement: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.PlacementTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_access_security_group: typing.Optional[builtins.str] = None,
    task_instance_fleets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.InstanceFleetConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    task_instance_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.InstanceGroupConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    termination_protected: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    unhealthy_node_replacement: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdecf83a3c77dfb530ebef148c0d5a3162482486ff1472c85dae44799dbab925(
    *,
    ad_domain_join_password: typing.Optional[builtins.str] = None,
    ad_domain_join_user: typing.Optional[builtins.str] = None,
    cross_realm_trust_principal_password: typing.Optional[builtins.str] = None,
    kdc_admin_password: typing.Optional[builtins.str] = None,
    realm: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2466f4d7f058132dbdeac60b33ad52549cb4ce1ae153180e7b947587407d9ecb(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33434479f88dce99aa8fb85076a0dfb1c14daa5db3a46d4e59c62d75ccfaa764(
    *,
    compute_limits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ComputeLimitsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scaling_strategy: typing.Optional[builtins.str] = None,
    utilization_performance_index: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661a4920ca327c5300421ff364a59b1d94ea0fc2e56aee406e22d10fbd2bbb55(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d5266e3d048e658d8e35e6ac7a8bbdcd50eaf16dcb491f70b917395e70db778(
    *,
    capacity_reservation_preference: typing.Optional[builtins.str] = None,
    capacity_reservation_resource_group_arn: typing.Optional[builtins.str] = None,
    usage_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca82542666625d2d1f351c5d3d64c633b55d41df9b963a43595eb6684987da76(
    *,
    allocation_strategy: typing.Optional[builtins.str] = None,
    capacity_reservation_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ccc3dd9af2174d0a98ce152c9d1446c4ae9c584c86ded46762fc1d570253bfc(
    *,
    allocation_strategy: typing.Optional[builtins.str] = None,
    capacity_reservation_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.OnDemandCapacityReservationOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_duration_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382a1dad5ad1d6e934e292f66c4516ee7ec57781153e5372df9100a4a7622bf6(
    *,
    instance_role: typing.Optional[builtins.str] = None,
    placement_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1853633435e424bde42c85a2f8cf573f96bd538e8ccd8f152cd0df6a9753d75(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c18c3893105179056e97fc73e55d0ebfe42807f32837c8e0d40f19b2f98039(
    *,
    market: typing.Optional[builtins.str] = None,
    simple_scaling_policy_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.SimpleScalingPolicyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b810ae7b44182a110ee8bde00e682add15fd8abc30f2b03528a7ff55b6e3e90(
    *,
    max_capacity: typing.Optional[jsii.Number] = None,
    min_capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9488aa63484f7d50d2a03a2368060860a30d899ae57d1fc6ca6fcca3fc0c49cf(
    *,
    action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ScalingActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    trigger: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ScalingTriggerProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83dbb701cecd175bdeceb4aa6e69172ca4e01b50c2691ae8dca65fe1fb12769(
    *,
    cloud_watch_alarm_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.CloudWatchAlarmDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ca6c935da0cbc1942b938c1ff463c4461323a10e2de71df2c86379da576a49(
    *,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db4a9f3caa94e09a9abf74b632962d0d52306311c4549c6c0aaeb6c0ef1b84f(
    *,
    adjustment_type: typing.Optional[builtins.str] = None,
    cool_down: typing.Optional[jsii.Number] = None,
    scaling_adjustment: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b630f3f74349123a69baae2eac1aebc57e52911a25a763793c6a0929de4c74(
    *,
    allocation_strategy: typing.Optional[builtins.str] = None,
    block_duration_minutes: typing.Optional[jsii.Number] = None,
    timeout_action: typing.Optional[builtins.str] = None,
    timeout_duration_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed49dad4fd51a980e414310a80c0469508fbd66697f6e56239b008a65c61b384(
    *,
    allocation_strategy: typing.Optional[builtins.str] = None,
    timeout_duration_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90fb8504a2f9076a8db6d2658693f23e31a993bd6c28ebcc65999a2fbea5747(
    *,
    action_on_failure: typing.Optional[builtins.str] = None,
    hadoop_jar_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.HadoopJarStepConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__548f9410a6db8a31ba45e3c4453340916c5d37795c2ce9dd5c08e80281982f53(
    *,
    iops: typing.Optional[jsii.Number] = None,
    size_in_gb: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c25525f13258292b10717b73e94026e2c3e0657c443840ca5048bcbf5a463109(
    *,
    cluster_id: typing.Optional[builtins.str] = None,
    instance_fleet_type: typing.Optional[builtins.str] = None,
    instance_type_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceFleetConfigPropsMixin.InstanceTypeConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    launch_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceFleetConfigPropsMixin.InstanceFleetProvisioningSpecificationsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    resize_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceFleetConfigPropsMixin.InstanceFleetResizingSpecificationsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_on_demand_capacity: typing.Optional[jsii.Number] = None,
    target_spot_capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f0ec28349b2ee19965a9604a8ada1f2012aa21ed0e93123b7a049430ca3da3(
    props: typing.Union[CfnInstanceFleetConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947f608159942e74bf5016e3d20e0b3816207dbab55fe44b11ab18c3c1d98e69(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8903b94c1f045f2ead59b1d8ed169e859fee49d94b2416f5dfb8aee5efb5e452(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c958fa2feee31edf1e79d2fb97e23c9b01fd5b4327969feee13644a4786bd3(
    *,
    classification: typing.Optional[builtins.str] = None,
    configuration_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceFleetConfigPropsMixin.ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c60c231d36473e20ef16bd809b04a6886f4cab7a24774958d0ca2da7ab728a(
    *,
    volume_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceFleetConfigPropsMixin.VolumeSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    volumes_per_instance: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__007ef7f5ed2b35f010821e909137e24ca02ab286af64ec07c7fb8e08f74b14aa(
    *,
    ebs_block_device_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceFleetConfigPropsMixin.EbsBlockDeviceConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ebs_optimized: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824a305f1337655b9890ad64259308c6cc91d484ce19d5340fdd3ebd65c4d238(
    *,
    on_demand_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceFleetConfigPropsMixin.OnDemandProvisioningSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    spot_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceFleetConfigPropsMixin.SpotProvisioningSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8131c3271f9372ca290fcdd039df1ec9d6b7507aedefd7b337123aaa6ec0ae2(
    *,
    on_demand_resize_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceFleetConfigPropsMixin.OnDemandResizingSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    spot_resize_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceFleetConfigPropsMixin.SpotResizingSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7aec96c366f7c1b79465405d41d777a0b59ae3a172afd754792e2bdfe5ecbab(
    *,
    bid_price: typing.Optional[builtins.str] = None,
    bid_price_as_percentage_of_on_demand_price: typing.Optional[jsii.Number] = None,
    configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceFleetConfigPropsMixin.ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    custom_ami_id: typing.Optional[builtins.str] = None,
    ebs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceFleetConfigPropsMixin.EbsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_type: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    weighted_capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1779717221e0c46d662923457f1836ab9087ad798fd5a684975b725e2447c92(
    *,
    capacity_reservation_preference: typing.Optional[builtins.str] = None,
    capacity_reservation_resource_group_arn: typing.Optional[builtins.str] = None,
    usage_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__454db275cf78fd0ed8afc77f5e22d73a576e6f5a6e4c1d6dc62163c6f810f2a8(
    *,
    allocation_strategy: typing.Optional[builtins.str] = None,
    capacity_reservation_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceFleetConfigPropsMixin.OnDemandCapacityReservationOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__261f7cf4b78b932eb7c5744d763200575aeb1c946aeecc5e413ac5ab59fbb7fc(
    *,
    allocation_strategy: typing.Optional[builtins.str] = None,
    capacity_reservation_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceFleetConfigPropsMixin.OnDemandCapacityReservationOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_duration_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be301fbd3c39b22e02a5a97b76f96ce69b6b6bdbbf6e0d731d162587d780da82(
    *,
    allocation_strategy: typing.Optional[builtins.str] = None,
    block_duration_minutes: typing.Optional[jsii.Number] = None,
    timeout_action: typing.Optional[builtins.str] = None,
    timeout_duration_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab2b8b769bb61af19778fb8f7461f34fdb0a39d3e2f9ba4eecd71cbe3055469(
    *,
    allocation_strategy: typing.Optional[builtins.str] = None,
    timeout_duration_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868c99c393df3d0b0719b0753f78923ab39ddb79edf99d55095c56b1c6ef0e10(
    *,
    iops: typing.Optional[jsii.Number] = None,
    size_in_gb: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba8c45d610388120b6072a6eb4cc2c313a4ff23f2ee92e3719a5eac6fe2c2a54(
    *,
    auto_scaling_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceGroupConfigPropsMixin.AutoScalingPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    bid_price: typing.Optional[builtins.str] = None,
    configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceGroupConfigPropsMixin.ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    custom_ami_id: typing.Optional[builtins.str] = None,
    ebs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceGroupConfigPropsMixin.EbsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_count: typing.Optional[jsii.Number] = None,
    instance_role: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[builtins.str] = None,
    job_flow_id: typing.Optional[builtins.str] = None,
    market: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c8bad74698eab157a1334a4fc571ed3feaea415b26bef90dbf1e13e1dff671(
    props: typing.Union[CfnInstanceGroupConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1810de87179afe13e195ee7e2c0aa2b08041ba1a74fd195b6f393c2c9bb66964(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd08b24c721ea167a7c7c45b59a89d3dbddf0ab8769abc23471e2bf8b40adb82(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e2127602c48f6a9789f991bfacae18cc7e4298a234ee9a475c6300e7bd56ab(
    *,
    constraints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceGroupConfigPropsMixin.ScalingConstraintsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceGroupConfigPropsMixin.ScalingRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c4fe73e99c87da252b9d05b1f3a132c6321654ba5ad84310cb25cb5430b8ffa(
    *,
    comparison_operator: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceGroupConfigPropsMixin.MetricDimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    metric_name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    period: typing.Optional[jsii.Number] = None,
    statistic: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be08ddf5e29ff6827032687ee20da9cd788e48745f4e52946c3e4e78fc70c0bb(
    *,
    classification: typing.Optional[builtins.str] = None,
    configuration_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceGroupConfigPropsMixin.ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fbad35a8fbfca26d939b0d13bb20d300cbb1bc31b7c51b322f2561cd88ff917(
    *,
    volume_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceGroupConfigPropsMixin.VolumeSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    volumes_per_instance: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e35402cebf22e1a6d350090c5fd68f1e54e328e701642ee9216b74b10ba2b6(
    *,
    ebs_block_device_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceGroupConfigPropsMixin.EbsBlockDeviceConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ebs_optimized: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0498619f042b9ad22fc1fc2053b365f9df8632fafebe62648bb2487e2dd9da72(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b1386810dc0232ed5f87b1d0138663d98eb5998c1d31b7cd318a3372154fcb1(
    *,
    market: typing.Optional[builtins.str] = None,
    simple_scaling_policy_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceGroupConfigPropsMixin.SimpleScalingPolicyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee3f470a7334cd82e04064db78127b415bea3aceb5c966d8f004ab8c706c7eb(
    *,
    max_capacity: typing.Optional[jsii.Number] = None,
    min_capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3cfb6269ca3b56614ba8218b68681cc78d34c43669a873313c58fc57f91692c(
    *,
    action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceGroupConfigPropsMixin.ScalingActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    trigger: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceGroupConfigPropsMixin.ScalingTriggerProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e90fcd70c649a4df2e253380d66f6d95bec57e2666628c65d600893e1d35d9(
    *,
    cloud_watch_alarm_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceGroupConfigPropsMixin.CloudWatchAlarmDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9684490f0a184807a78c7d936f77be4e156167e2f8091e554eabde6825562745(
    *,
    adjustment_type: typing.Optional[builtins.str] = None,
    cool_down: typing.Optional[jsii.Number] = None,
    scaling_adjustment: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71ee40222aaecb78c0f90d17f5ee4556e9812c231f7dc2096822c4602bd0b98(
    *,
    iops: typing.Optional[jsii.Number] = None,
    size_in_gb: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f94ae925d3a79ed74c0d6e33edbfd124fc28186e48eb59049e886563b8eab4(
    *,
    name: typing.Optional[builtins.str] = None,
    security_configuration: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552c3d60cdabe23cb108032a0949dfc7a02ff44850559c5369c165cd33730a98(
    props: typing.Union[CfnSecurityConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac1fbc78ca6908625f179ec2efd0c678a5ec341886c93fe3ca7fb382ea70c26(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a530b48da0584077fdfd5f87b3bb98255b399fb5d2010085ec98cf242896b1fa(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96859f2b71b2d15232c6d6382e5b9b9ad69c3ac20a78c2463fb2296ce4c6a62b(
    *,
    action_on_failure: typing.Optional[builtins.str] = None,
    hadoop_jar_step: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStepPropsMixin.HadoopJarStepConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    job_flow_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90bf5f5b208fc06a8aa867a1733ae5ede81006ade422abaad7db8efd642a241a(
    props: typing.Union[CfnStepMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e5232e54ca264e523ad2d208c6e4ab8c71792fe674eafd86902dd96186602db(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c7b4807638479dd3844e131fef720d2d44c6d2963b05e2d03a6e4958297c14(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c9e69c8042d8b17dbac8c2525fbe42bfebd0f4753ea97c6581c9af015304fe(
    *,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    jar: typing.Optional[builtins.str] = None,
    main_class: typing.Optional[builtins.str] = None,
    step_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStepPropsMixin.KeyValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3eb52491c61fdd14963a366149c8c25d0e9e085390d2995f96109b4b2f83ed2(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8260a0531455655cfc01de93da840dcd13148c961f30ea0d6506bbcf0aa7c14(
    *,
    auth_mode: typing.Optional[builtins.str] = None,
    default_s3_location: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    encryption_key_arn: typing.Optional[builtins.str] = None,
    engine_security_group_id: typing.Optional[builtins.str] = None,
    idc_instance_arn: typing.Optional[builtins.str] = None,
    idc_user_assignment: typing.Optional[builtins.str] = None,
    idp_auth_url: typing.Optional[builtins.str] = None,
    idp_relay_state_parameter_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    service_role: typing.Optional[builtins.str] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    trusted_identity_propagation_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    user_role: typing.Optional[builtins.str] = None,
    vpc_id: typing.Optional[builtins.str] = None,
    workspace_security_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e36335ec2c97ce0928e933952e3bc052a72223322dd13bf60764ef6b669e2b84(
    props: typing.Union[CfnStudioMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b9283e18b0712dc32cd929dc9087b902cd8870da9502f6e1de2fbc791500e80(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3224b6509b4d3aa9aee4c70ddf78cef44d54660a2b8af4ea6202c6f340d2254e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3fb7d872edee89a8d3bf295eb734906f069ca4565fd69c681fb003e1d1bb45(
    *,
    identity_name: typing.Optional[builtins.str] = None,
    identity_type: typing.Optional[builtins.str] = None,
    session_policy_arn: typing.Optional[builtins.str] = None,
    studio_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24bc7e9b49238c5aeebaa283f4cff15030355f6f3f12716f2e7e27855a761a67(
    props: typing.Union[CfnStudioSessionMappingMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6defc92c67b1718d25b0ab3211e2a6f9f9ff74bbb0e361dd2d0930e72c4afc99(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__affe7abef0671569b8faa7e30a97d0c942cf717552555af72f3b7c4dda9b28ba(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16ea27f58bade02ffda73860f7a0230620270a16f509f4fe4992a0ce01ae9a1(
    *,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    wal_workspace_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5edfc4a2b13ea9251e7fff378e07d99e3d31a98aa84c9c994f084232e7af325(
    props: typing.Union[CfnWALWorkspaceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70dee9c33c846bbe17e7005e0b66827e2805791e08c77cfe582ce5619de529a3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__779406d641d8b5ce3a14d6fee5c33b9087040506734f116b011bd6bc0f48c824(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
