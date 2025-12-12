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
    jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnComputeEnvironmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_environment_name": "computeEnvironmentName",
        "compute_resources": "computeResources",
        "context": "context",
        "eks_configuration": "eksConfiguration",
        "replace_compute_environment": "replaceComputeEnvironment",
        "service_role": "serviceRole",
        "state": "state",
        "tags": "tags",
        "type": "type",
        "unmanagedv_cpus": "unmanagedvCpus",
        "update_policy": "updatePolicy",
    },
)
class CfnComputeEnvironmentMixinProps:
    def __init__(
        self,
        *,
        compute_environment_name: typing.Optional[builtins.str] = None,
        compute_resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComputeEnvironmentPropsMixin.ComputeResourcesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        context: typing.Optional[builtins.str] = None,
        eks_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComputeEnvironmentPropsMixin.EksConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        replace_compute_environment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        service_role: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
        unmanagedv_cpus: typing.Optional[jsii.Number] = None,
        update_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComputeEnvironmentPropsMixin.UpdatePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnComputeEnvironmentPropsMixin.

        :param compute_environment_name: The name for your compute environment. It can be up to 128 characters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_).
        :param compute_resources: The ComputeResources property type specifies details of the compute resources managed by the compute environment. This parameter is required for managed compute environments. For more information, see `Compute Environments <https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html>`_ in the ** .
        :param context: Reserved.
        :param eks_configuration: The details for the Amazon EKS cluster that supports the compute environment. .. epigraph:: To create a compute environment that uses EKS resources, the caller must have permissions to call ``eks:DescribeCluster`` .
        :param replace_compute_environment: Specifies whether the compute environment is replaced if an update is made that requires replacing the instances in the compute environment. The default value is ``true`` . To enable more properties to be updated, set this property to ``false`` . When changing the value of this property to ``false`` , do not change any other properties at the same time. If other properties are changed at the same time, and the change needs to be rolled back but it can't, it's possible for the stack to go into the ``UPDATE_ROLLBACK_FAILED`` state. You can't update a stack that is in the ``UPDATE_ROLLBACK_FAILED`` state. However, if you can continue to roll it back, you can return the stack to its original settings and then try to update it again. For more information, see `Continue rolling back an update <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-continueupdaterollback.html>`_ in the *AWS CloudFormation User Guide* . ``ReplaceComputeEnvironment`` is not applicable for Fargate compute environments. Fargate compute environments are always updated without interruption. The properties that can't be changed without replacing the compute environment are in the ```ComputeResources`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html>`_ property type: ```AllocationStrategy`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-allocationstrategy>`_ , ```BidPercentage`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-bidpercentage>`_ , ```Ec2Configuration`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2configuration>`_ , ```Ec2KeyPair`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2keypair>`_ , ```Ec2KeyPair`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2keypair>`_ , ```ImageId`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-imageid>`_ , ```InstanceRole`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-instancerole>`_ , ```InstanceTypes`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-instancetypes>`_ , ```LaunchTemplate`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-launchtemplate>`_ , ```MaxvCpus`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-maxvcpus>`_ , ```MinvCpus`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-minvcpus>`_ , ```PlacementGroup`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-placementgroup>`_ , ```SecurityGroupIds`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-securitygroupids>`_ , ```Subnets`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-subnets>`_ , `Tags <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-tags>`_ , ```Type`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-type>`_ , and ```UpdateToLatestImageVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-updatetolatestimageversion>`_ . Default: - true
        :param service_role: The full Amazon Resource Name (ARN) of the IAM role that allows AWS Batch to make calls to other AWS services on your behalf. For more information, see `AWS Batch service IAM role <https://docs.aws.amazon.com/batch/latest/userguide/service_IAM_role.html>`_ in the *AWS Batch User Guide* . .. epigraph:: If your account already created the AWS Batch service-linked role, that role is used by default for your compute environment unless you specify a different role here. If the AWS Batch service-linked role doesn't exist in your account, and no role is specified here, the service attempts to create the AWS Batch service-linked role in your account. If your specified role has a path other than ``/`` , then you must specify either the full role ARN (recommended) or prefix the role name with the path. For example, if a role with the name ``bar`` has a path of ``/foo/`` , specify ``/foo/bar`` as the role name. For more information, see `Friendly names and paths <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-friendly-names>`_ in the *IAM User Guide* . .. epigraph:: Depending on how you created your AWS Batch service role, its ARN might contain the ``service-role`` path prefix. When you only specify the name of the service role, AWS Batch assumes that your ARN doesn't use the ``service-role`` path prefix. Because of this, we recommend that you specify the full ARN of your service role when you create compute environments.
        :param state: The state of the compute environment. If the state is ``ENABLED`` , then the compute environment accepts jobs from a queue and can scale out automatically based on queues. If the state is ``ENABLED`` , then the AWS Batch scheduler can attempt to place jobs from an associated job queue on the compute resources within the environment. If the compute environment is managed, then it can scale its instances out or in automatically, based on the job queue demand. If the state is ``DISABLED`` , then the AWS Batch scheduler doesn't attempt to place jobs within the environment. Jobs in a ``STARTING`` or ``RUNNING`` state continue to progress normally. Managed compute environments in the ``DISABLED`` state don't scale out. .. epigraph:: Compute environments in a ``DISABLED`` state may continue to incur billing charges. To prevent additional charges, turn off and then delete the compute environment. For more information, see `State <https://docs.aws.amazon.com/batch/latest/userguide/compute_environment_parameters.html#compute_environment_state>`_ in the *AWS Batch User Guide* . When an instance is idle, the instance scales down to the ``minvCpus`` value. However, the instance size doesn't change. For example, consider a ``c5.8xlarge`` instance with a ``minvCpus`` value of ``4`` and a ``desiredvCpus`` value of ``36`` . This instance doesn't scale down to a ``c5.large`` instance.
        :param tags: The tags applied to the compute environment.
        :param type: The type of the compute environment: ``MANAGED`` or ``UNMANAGED`` . For more information, see `Compute Environments <https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html>`_ in the *AWS Batch User Guide* .
        :param unmanagedv_cpus: The maximum number of vCPUs for an unmanaged compute environment. This parameter is only used for fair-share scheduling to reserve vCPU capacity for new share identifiers. If this parameter isn't provided for a fair-share job queue, no vCPU capacity is reserved. .. epigraph:: This parameter is only supported when the ``type`` parameter is set to ``UNMANAGED`` .
        :param update_policy: Specifies the infrastructure update policy for the compute environment. For more information about infrastructure updates, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
            
            cfn_compute_environment_mixin_props = batch_mixins.CfnComputeEnvironmentMixinProps(
                compute_environment_name="computeEnvironmentName",
                compute_resources=batch_mixins.CfnComputeEnvironmentPropsMixin.ComputeResourcesProperty(
                    allocation_strategy="allocationStrategy",
                    bid_percentage=123,
                    desiredv_cpus=123,
                    ec2_configuration=[batch_mixins.CfnComputeEnvironmentPropsMixin.Ec2ConfigurationObjectProperty(
                        image_id_override="imageIdOverride",
                        image_kubernetes_version="imageKubernetesVersion",
                        image_type="imageType"
                    )],
                    ec2_key_pair="ec2KeyPair",
                    image_id="imageId",
                    instance_role="instanceRole",
                    instance_types=["instanceTypes"],
                    launch_template=batch_mixins.CfnComputeEnvironmentPropsMixin.LaunchTemplateSpecificationProperty(
                        launch_template_id="launchTemplateId",
                        launch_template_name="launchTemplateName",
                        overrides=[batch_mixins.CfnComputeEnvironmentPropsMixin.LaunchTemplateSpecificationOverrideProperty(
                            launch_template_id="launchTemplateId",
                            launch_template_name="launchTemplateName",
                            target_instance_types=["targetInstanceTypes"],
                            userdata_type="userdataType",
                            version="version"
                        )],
                        userdata_type="userdataType",
                        version="version"
                    ),
                    maxv_cpus=123,
                    minv_cpus=123,
                    placement_group="placementGroup",
                    security_group_ids=["securityGroupIds"],
                    spot_iam_fleet_role="spotIamFleetRole",
                    subnets=["subnets"],
                    tags={
                        "tags_key": "tags"
                    },
                    type="type",
                    update_to_latest_image_version=False
                ),
                context="context",
                eks_configuration=batch_mixins.CfnComputeEnvironmentPropsMixin.EksConfigurationProperty(
                    eks_cluster_arn="eksClusterArn",
                    kubernetes_namespace="kubernetesNamespace"
                ),
                replace_compute_environment=False,
                service_role="serviceRole",
                state="state",
                tags={
                    "tags_key": "tags"
                },
                type="type",
                unmanagedv_cpus=123,
                update_policy=batch_mixins.CfnComputeEnvironmentPropsMixin.UpdatePolicyProperty(
                    job_execution_timeout_minutes=123,
                    terminate_jobs_on_update=False
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eca7e9bb48dc8c53779233c34c1b3b48f3f81bb63409ee78547b5426f4a0abe)
            check_type(argname="argument compute_environment_name", value=compute_environment_name, expected_type=type_hints["compute_environment_name"])
            check_type(argname="argument compute_resources", value=compute_resources, expected_type=type_hints["compute_resources"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument eks_configuration", value=eks_configuration, expected_type=type_hints["eks_configuration"])
            check_type(argname="argument replace_compute_environment", value=replace_compute_environment, expected_type=type_hints["replace_compute_environment"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument unmanagedv_cpus", value=unmanagedv_cpus, expected_type=type_hints["unmanagedv_cpus"])
            check_type(argname="argument update_policy", value=update_policy, expected_type=type_hints["update_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compute_environment_name is not None:
            self._values["compute_environment_name"] = compute_environment_name
        if compute_resources is not None:
            self._values["compute_resources"] = compute_resources
        if context is not None:
            self._values["context"] = context
        if eks_configuration is not None:
            self._values["eks_configuration"] = eks_configuration
        if replace_compute_environment is not None:
            self._values["replace_compute_environment"] = replace_compute_environment
        if service_role is not None:
            self._values["service_role"] = service_role
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type
        if unmanagedv_cpus is not None:
            self._values["unmanagedv_cpus"] = unmanagedv_cpus
        if update_policy is not None:
            self._values["update_policy"] = update_policy

    @builtins.property
    def compute_environment_name(self) -> typing.Optional[builtins.str]:
        '''The name for your compute environment.

        It can be up to 128 characters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-computeenvironmentname
        '''
        result = self._values.get("compute_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_resources(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeEnvironmentPropsMixin.ComputeResourcesProperty"]]:
        '''The ComputeResources property type specifies details of the compute resources managed by the compute environment.

        This parameter is required for managed compute environments. For more information, see `Compute Environments <https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html>`_ in the ** .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-computeresources
        '''
        result = self._values.get("compute_resources")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeEnvironmentPropsMixin.ComputeResourcesProperty"]], result)

    @builtins.property
    def context(self) -> typing.Optional[builtins.str]:
        '''Reserved.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-context
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eks_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeEnvironmentPropsMixin.EksConfigurationProperty"]]:
        '''The details for the Amazon EKS cluster that supports the compute environment.

        .. epigraph::

           To create a compute environment that uses EKS resources, the caller must have permissions to call ``eks:DescribeCluster`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-eksconfiguration
        '''
        result = self._values.get("eks_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeEnvironmentPropsMixin.EksConfigurationProperty"]], result)

    @builtins.property
    def replace_compute_environment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the compute environment is replaced if an update is made that requires replacing the instances in the compute environment.

        The default value is ``true`` . To enable more properties to be updated, set this property to ``false`` . When changing the value of this property to ``false`` , do not change any other properties at the same time. If other properties are changed at the same time, and the change needs to be rolled back but it can't, it's possible for the stack to go into the ``UPDATE_ROLLBACK_FAILED`` state. You can't update a stack that is in the ``UPDATE_ROLLBACK_FAILED`` state. However, if you can continue to roll it back, you can return the stack to its original settings and then try to update it again. For more information, see `Continue rolling back an update <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-continueupdaterollback.html>`_ in the *AWS CloudFormation User Guide* .

        ``ReplaceComputeEnvironment`` is not applicable for Fargate compute environments. Fargate compute environments are always updated without interruption.

        The properties that can't be changed without replacing the compute environment are in the ```ComputeResources`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html>`_ property type: ```AllocationStrategy`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-allocationstrategy>`_ , ```BidPercentage`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-bidpercentage>`_ , ```Ec2Configuration`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2configuration>`_ , ```Ec2KeyPair`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2keypair>`_ , ```Ec2KeyPair`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2keypair>`_ , ```ImageId`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-imageid>`_ , ```InstanceRole`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-instancerole>`_ , ```InstanceTypes`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-instancetypes>`_ , ```LaunchTemplate`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-launchtemplate>`_ , ```MaxvCpus`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-maxvcpus>`_ , ```MinvCpus`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-minvcpus>`_ , ```PlacementGroup`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-placementgroup>`_ , ```SecurityGroupIds`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-securitygroupids>`_ , ```Subnets`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-subnets>`_ , `Tags <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-tags>`_ , ```Type`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-type>`_ , and ```UpdateToLatestImageVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-updatetolatestimageversion>`_ .

        :default: - true

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-replacecomputeenvironment
        '''
        result = self._values.get("replace_compute_environment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def service_role(self) -> typing.Optional[builtins.str]:
        '''The full Amazon Resource Name (ARN) of the IAM role that allows AWS Batch to make calls to other AWS services on your behalf.

        For more information, see `AWS Batch service IAM role <https://docs.aws.amazon.com/batch/latest/userguide/service_IAM_role.html>`_ in the *AWS Batch User Guide* .
        .. epigraph::

           If your account already created the AWS Batch service-linked role, that role is used by default for your compute environment unless you specify a different role here. If the AWS Batch service-linked role doesn't exist in your account, and no role is specified here, the service attempts to create the AWS Batch service-linked role in your account.

        If your specified role has a path other than ``/`` , then you must specify either the full role ARN (recommended) or prefix the role name with the path. For example, if a role with the name ``bar`` has a path of ``/foo/`` , specify ``/foo/bar`` as the role name. For more information, see `Friendly names and paths <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-friendly-names>`_ in the *IAM User Guide* .
        .. epigraph::

           Depending on how you created your AWS Batch service role, its ARN might contain the ``service-role`` path prefix. When you only specify the name of the service role, AWS Batch assumes that your ARN doesn't use the ``service-role`` path prefix. Because of this, we recommend that you specify the full ARN of your service role when you create compute environments.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-servicerole
        '''
        result = self._values.get("service_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the compute environment.

        If the state is ``ENABLED`` , then the compute environment accepts jobs from a queue and can scale out automatically based on queues.

        If the state is ``ENABLED`` , then the AWS Batch scheduler can attempt to place jobs from an associated job queue on the compute resources within the environment. If the compute environment is managed, then it can scale its instances out or in automatically, based on the job queue demand.

        If the state is ``DISABLED`` , then the AWS Batch scheduler doesn't attempt to place jobs within the environment. Jobs in a ``STARTING`` or ``RUNNING`` state continue to progress normally. Managed compute environments in the ``DISABLED`` state don't scale out.
        .. epigraph::

           Compute environments in a ``DISABLED`` state may continue to incur billing charges. To prevent additional charges, turn off and then delete the compute environment. For more information, see `State <https://docs.aws.amazon.com/batch/latest/userguide/compute_environment_parameters.html#compute_environment_state>`_ in the *AWS Batch User Guide* .

        When an instance is idle, the instance scales down to the ``minvCpus`` value. However, the instance size doesn't change. For example, consider a ``c5.8xlarge`` instance with a ``minvCpus`` value of ``4`` and a ``desiredvCpus`` value of ``36`` . This instance doesn't scale down to a ``c5.large`` instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags applied to the compute environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the compute environment: ``MANAGED`` or ``UNMANAGED`` .

        For more information, see `Compute Environments <https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html>`_ in the *AWS Batch User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unmanagedv_cpus(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of vCPUs for an unmanaged compute environment.

        This parameter is only used for fair-share scheduling to reserve vCPU capacity for new share identifiers. If this parameter isn't provided for a fair-share job queue, no vCPU capacity is reserved.
        .. epigraph::

           This parameter is only supported when the ``type`` parameter is set to ``UNMANAGED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-unmanagedvcpus
        '''
        result = self._values.get("unmanagedv_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def update_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeEnvironmentPropsMixin.UpdatePolicyProperty"]]:
        '''Specifies the infrastructure update policy for the compute environment.

        For more information about infrastructure updates, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-updatepolicy
        '''
        result = self._values.get("update_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeEnvironmentPropsMixin.UpdatePolicyProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnComputeEnvironmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnComputeEnvironmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnComputeEnvironmentPropsMixin",
):
    '''The ``AWS::Batch::ComputeEnvironment`` resource defines your AWS Batch compute environment.

    You can define ``MANAGED`` or ``UNMANAGED`` compute environments. ``MANAGED`` compute environments can use Amazon EC2 or AWS Fargate resources. ``UNMANAGED`` compute environments can only use EC2 resources. For more information, see `Compute Environments <https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html>`_ in the ** .

    In a managed compute environment, AWS Batch manages the capacity and instance types of the compute resources within the environment. This is based on the compute resource specification that you define or the `launch template <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-templates.html>`_ that you specify when you create the compute environment. You can choose either to use EC2 On-Demand Instances and EC2 Spot Instances, or to use Fargate and Fargate Spot capacity in your managed compute environment. You can optionally set a maximum price so that Spot Instances only launch when the Spot Instance price is below a specified percentage of the On-Demand price.
    .. epigraph::

       Multi-node parallel jobs are not supported on Spot Instances.

    In an unmanaged compute environment, you can manage your own EC2 compute resources and have a lot of flexibility with how you configure your compute resources. For example, you can use custom AMI. However, you need to verify that your AMI meets the Amazon ECS container instance AMI specification. For more information, see `container instance AMIs <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container_instance_AMIs.html>`_ in the *Amazon Elastic Container Service Developer Guide* . After you have created your unmanaged compute environment, you can use the `DescribeComputeEnvironments <https://docs.aws.amazon.com/batch/latest/APIReference/API_DescribeComputeEnvironments.html>`_ operation to find the Amazon ECS cluster that is associated with it. Then, manually launch your container instances into that Amazon ECS cluster. For more information, see `Launching an Amazon ECS container instance <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/launch_container_instance.html>`_ in the *Amazon Elastic Container Service Developer Guide* .
    .. epigraph::

       To create a compute environment that uses EKS resources, the caller must have permissions to call ``eks:DescribeCluster`` . > AWS Batch doesn't upgrade the AMIs in a compute environment after it's created except under specific conditions. For example, it doesn't automatically update the AMIs when a newer version of the Amazon ECS optimized AMI is available. Therefore, you're responsible for the management of the guest operating system (including updates and security patches) and any additional application software or utilities that you install on the compute resources. There are two ways to use a new AMI for your AWS Batch jobs. The original method is to complete these steps:

       - Create a new compute environment with the new AMI.
       - Add the compute environment to an existing job queue.
       - Remove the earlier compute environment from your job queue.
       - Delete the earlier compute environment.

       In April 2022, AWS Batch added enhanced support for updating compute environments. For example, the ``UpdateComputeEnvironent`` API lets you use the ``ReplaceComputeEnvironment`` property to dynamically update compute environment parameters such as the launch template or instance type without replacement. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .

       To use the enhanced updating of compute environments to update AMIs, follow these rules:

       - Either do not set the `ServiceRole <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-servicerole>`_ property or set it to the *AWSServiceRoleForBatch* service-linked role.
       - Set the `AllocationStrategy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-allocationstrategy>`_ property to ``BEST_FIT_PROGRESSIVE`` or ``SPOT_CAPACITY_OPTIMIZED`` .
       - Set the `ReplaceComputeEnvironment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-replacecomputeenvironment>`_ property to ``false`` .

       .. epigraph::

          Set the ``ReplaceComputeEnvironment`` property to ``true`` if the compute environment uses the ``BEST_FIT`` allocation strategy. > If the ``ReplaceComputeEnvironment`` property is set to ``false`` , you might receive an error message when you update the CFN template for a compute environment. This issue occurs if the updated ``desiredvcpus`` value is less than the current ``desiredvcpus`` value. As a workaround, delete the ``desiredvcpus`` value from the updated template or use the ``minvcpus`` property to manage the number of vCPUs. For information, see `Error message when you update the ``DesiredvCpus`` setting <https://docs.aws.amazon.com/batch/latest/userguide/troubleshooting.html#error-desired-vcpus-update>`_ .

       - Set the `UpdateToLatestImageVersion <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-updatetolatestimageversion>`_ property to ``true`` . This property is used when you update a compute environment. The `UpdateToLatestImageVersion <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-updatetolatestimageversion>`_ property is ignored when you create a compute environment.
       - Either do not specify an image ID in `ImageId <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-imageid>`_ or `ImageIdOverride <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-ec2configurationobject.html#cfn-batch-computeenvironment-ec2configurationobject-imageidoverride>`_ properties, or in the launch template identified by the `Launch Template <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-launchtemplate>`_ property. In that case AWS Batch will select the latest Amazon ECS optimized AMI supported by AWS Batch at the time the infrastructure update is initiated. Alternatively you can specify the AMI ID in the ``ImageId`` or ``ImageIdOverride`` properties, or the launch template identified by the ``LaunchTemplate`` properties. Changing any of these properties will trigger an infrastructure update.

       If these rules are followed, any update that triggers an infrastructure update will cause the AMI ID to be re-selected. If the `Version <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html#cfn-batch-computeenvironment-launchtemplatespecification-version>`_ property of the `LaunchTemplateSpecification <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html>`_ is set to ``$Latest`` or ``$Default`` , the latest or default version of the launch template will be evaluated up at the time of the infrastructure update, even if the ``LaunchTemplateSpecification`` was not updated.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html
    :cloudformationResource: AWS::Batch::ComputeEnvironment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
        
        cfn_compute_environment_props_mixin = batch_mixins.CfnComputeEnvironmentPropsMixin(batch_mixins.CfnComputeEnvironmentMixinProps(
            compute_environment_name="computeEnvironmentName",
            compute_resources=batch_mixins.CfnComputeEnvironmentPropsMixin.ComputeResourcesProperty(
                allocation_strategy="allocationStrategy",
                bid_percentage=123,
                desiredv_cpus=123,
                ec2_configuration=[batch_mixins.CfnComputeEnvironmentPropsMixin.Ec2ConfigurationObjectProperty(
                    image_id_override="imageIdOverride",
                    image_kubernetes_version="imageKubernetesVersion",
                    image_type="imageType"
                )],
                ec2_key_pair="ec2KeyPair",
                image_id="imageId",
                instance_role="instanceRole",
                instance_types=["instanceTypes"],
                launch_template=batch_mixins.CfnComputeEnvironmentPropsMixin.LaunchTemplateSpecificationProperty(
                    launch_template_id="launchTemplateId",
                    launch_template_name="launchTemplateName",
                    overrides=[batch_mixins.CfnComputeEnvironmentPropsMixin.LaunchTemplateSpecificationOverrideProperty(
                        launch_template_id="launchTemplateId",
                        launch_template_name="launchTemplateName",
                        target_instance_types=["targetInstanceTypes"],
                        userdata_type="userdataType",
                        version="version"
                    )],
                    userdata_type="userdataType",
                    version="version"
                ),
                maxv_cpus=123,
                minv_cpus=123,
                placement_group="placementGroup",
                security_group_ids=["securityGroupIds"],
                spot_iam_fleet_role="spotIamFleetRole",
                subnets=["subnets"],
                tags={
                    "tags_key": "tags"
                },
                type="type",
                update_to_latest_image_version=False
            ),
            context="context",
            eks_configuration=batch_mixins.CfnComputeEnvironmentPropsMixin.EksConfigurationProperty(
                eks_cluster_arn="eksClusterArn",
                kubernetes_namespace="kubernetesNamespace"
            ),
            replace_compute_environment=False,
            service_role="serviceRole",
            state="state",
            tags={
                "tags_key": "tags"
            },
            type="type",
            unmanagedv_cpus=123,
            update_policy=batch_mixins.CfnComputeEnvironmentPropsMixin.UpdatePolicyProperty(
                job_execution_timeout_minutes=123,
                terminate_jobs_on_update=False
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnComputeEnvironmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Batch::ComputeEnvironment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88f5a15200eb018b614f82e670428401d704579f42ebf5c43cbb03513967c248)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26728de17ad0822af3ddd19021f263835ac6e85e611335e832b007e0eaf024b1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daadb6113f0a1945dc1e65345283e4250bc7f3fd0e119cd0978f2e308d23a739)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnComputeEnvironmentMixinProps:
        return typing.cast(CfnComputeEnvironmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnComputeEnvironmentPropsMixin.ComputeResourcesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allocation_strategy": "allocationStrategy",
            "bid_percentage": "bidPercentage",
            "desiredv_cpus": "desiredvCpus",
            "ec2_configuration": "ec2Configuration",
            "ec2_key_pair": "ec2KeyPair",
            "image_id": "imageId",
            "instance_role": "instanceRole",
            "instance_types": "instanceTypes",
            "launch_template": "launchTemplate",
            "maxv_cpus": "maxvCpus",
            "minv_cpus": "minvCpus",
            "placement_group": "placementGroup",
            "security_group_ids": "securityGroupIds",
            "spot_iam_fleet_role": "spotIamFleetRole",
            "subnets": "subnets",
            "tags": "tags",
            "type": "type",
            "update_to_latest_image_version": "updateToLatestImageVersion",
        },
    )
    class ComputeResourcesProperty:
        def __init__(
            self,
            *,
            allocation_strategy: typing.Optional[builtins.str] = None,
            bid_percentage: typing.Optional[jsii.Number] = None,
            desiredv_cpus: typing.Optional[jsii.Number] = None,
            ec2_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComputeEnvironmentPropsMixin.Ec2ConfigurationObjectProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ec2_key_pair: typing.Optional[builtins.str] = None,
            image_id: typing.Optional[builtins.str] = None,
            instance_role: typing.Optional[builtins.str] = None,
            instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            launch_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComputeEnvironmentPropsMixin.LaunchTemplateSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            maxv_cpus: typing.Optional[jsii.Number] = None,
            minv_cpus: typing.Optional[jsii.Number] = None,
            placement_group: typing.Optional[builtins.str] = None,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            spot_iam_fleet_role: typing.Optional[builtins.str] = None,
            subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
            tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
            type: typing.Optional[builtins.str] = None,
            update_to_latest_image_version: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Details about the compute resources managed by the compute environment.

            This parameter is required for managed compute environments. For more information, see `Compute Environments <https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html>`_ in the *AWS Batch User Guide* .

            :param allocation_strategy: The allocation strategy to use for the compute resource if not enough instances of the best fitting instance type can be allocated. This might be because of availability of the instance type in the Region or `Amazon EC2 service limits <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html>`_ . For more information, see `Allocation strategies <https://docs.aws.amazon.com/batch/latest/userguide/allocation-strategies.html>`_ in the *AWS Batch User Guide* . When updating a compute environment, changing the allocation strategy requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . ``BEST_FIT`` is not supported when updating a compute environment. .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources, and shouldn't be specified. - **BEST_FIT (default)** - AWS Batch selects an instance type that best fits the needs of the jobs with a preference for the lowest-cost instance type. If additional instances of the selected instance type aren't available, AWS Batch waits for the additional instances to be available. If there aren't enough instances available, or if the user is reaching `Amazon EC2 service limits <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html>`_ then additional jobs aren't run until the currently running jobs have completed. This allocation strategy keeps costs lower but can limit scaling. If you are using Spot Fleets with ``BEST_FIT`` then the Spot Fleet IAM role must be specified. - **BEST_FIT_PROGRESSIVE** - AWS Batch will select additional instance types that are large enough to meet the requirements of the jobs in the queue, with a preference for instance types with a lower cost per unit vCPU. If additional instances of the previously selected instance types aren't available, AWS Batch will select new instance types. - **SPOT_CAPACITY_OPTIMIZED** - AWS Batch will select one or more instance types that are large enough to meet the requirements of the jobs in the queue, with a preference for instance types that are less likely to be interrupted. This allocation strategy is only available for Spot Instance compute resources. - **SPOT_PRICE_CAPACITY_OPTIMIZED** - The price and capacity optimized allocation strategy looks at both price and capacity to select the Spot Instance pools that are the least likely to be interrupted and have the lowest possible price. This allocation strategy is only available for Spot Instance compute resources. .. epigraph:: We recommend that you use ``SPOT_PRICE_CAPACITY_OPTIMIZED`` rather than ``SPOT_CAPACITY_OPTIMIZED`` in most instances. With ``BEST_FIT_PROGRESSIVE`` , ``SPOT_CAPACITY_OPTIMIZED`` , and ``SPOT_PRICE_CAPACITY_OPTIMIZED`` allocation strategies using On-Demand or Spot Instances, and the ``BEST_FIT`` strategy using Spot Instances, AWS Batch might need to go above ``maxvCpus`` to meet your capacity requirements. In this event, AWS Batch never exceeds ``maxvCpus`` by more than a single instance.
            :param bid_percentage: The maximum percentage that a Spot Instance price can be when compared with the On-Demand price for that instance type before instances are launched. For example, if your maximum percentage is 20%, the Spot price must be less than 20% of the current On-Demand price for that Amazon EC2 instance. You always pay the lowest (market) price and never more than your maximum percentage. For most use cases, we recommend leaving this field empty. When updating a compute environment, changing the bid percentage requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.
            :param desiredv_cpus: The desired number of vCPUS in the compute environment. AWS Batch modifies this value between the minimum and maximum values based on job queue demand. .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it. > AWS Batch doesn't support changing the desired number of vCPUs of an existing compute environment. Don't specify this parameter for compute environments using Amazon EKS clusters. > When you update the ``desiredvCpus`` setting, the value must be between the ``minvCpus`` and ``maxvCpus`` values. Additionally, the updated ``desiredvCpus`` value must be greater than or equal to the current ``desiredvCpus`` value. For more information, see `Troubleshooting AWS Batch <https://docs.aws.amazon.com/batch/latest/userguide/troubleshooting.html#error-desired-vcpus-update>`_ in the *AWS Batch User Guide* .
            :param ec2_configuration: Provides information used to select Amazon Machine Images (AMIs) for Amazon EC2 instances in the compute environment. If ``Ec2Configuration`` isn't specified, the default is ``ECS_AL2`` . When updating a compute environment, changing this setting requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . To remove the Amazon EC2 configuration and any custom AMI ID specified in ``imageIdOverride`` , set this value to an empty string. One or two values can be provided. .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.
            :param ec2_key_pair: The Amazon EC2 key pair that's used for instances launched in the compute environment. You can use this key pair to log in to your instances with SSH. To remove the Amazon EC2 key pair, set this value to an empty string. When updating a compute environment, changing the Amazon EC2 key pair requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.
            :param image_id: The Amazon Machine Image (AMI) ID used for instances launched in the compute environment. This parameter is overridden by the ``imageIdOverride`` member of the ``Ec2Configuration`` structure. To remove the custom AMI ID and use the default AMI ID, set this value to an empty string. When updating a compute environment, changing the AMI ID requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it. > The AMI that you choose for a compute environment must match the architecture of the instance types that you intend to use for that compute environment. For example, if your compute environment uses A1 instance types, the compute resource AMI that you choose must support ARM instances. Amazon ECS vends both x86 and ARM versions of the Amazon ECS-optimized Amazon Linux 2 AMI. For more information, see `Amazon ECS-optimized Amazon Linux 2 AMI <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#ecs-optimized-ami-linux-variants.html>`_ in the *Amazon Elastic Container Service Developer Guide* .
            :param instance_role: The Amazon ECS instance profile applied to Amazon EC2 instances in a compute environment. Required for Amazon EC2 instances. You can specify the short name or full Amazon Resource Name (ARN) of an instance profile. For example, ``*ecsInstanceRole*`` or ``arn:aws:iam:: *<aws_account_id>* :instance-profile/ *ecsInstanceRole*`` . For more information, see `Amazon ECS instance role <https://docs.aws.amazon.com/batch/latest/userguide/instance_IAM_role.html>`_ in the *AWS Batch User Guide* . When updating a compute environment, changing this setting requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.
            :param instance_types: The instances types that can be launched. You can specify instance families to launch any instance type within those families (for example, ``c5`` or ``p3`` ), or you can specify specific sizes within a family (such as ``c5.8xlarge`` ). AWS Batch can select the instance type for you if you choose one of the following: - ``optimal`` to select instance types (from the ``c4`` , ``m4`` , ``r4`` , ``c5`` , ``m5`` , and ``r5`` instance families) that match the demand of your job queues. - ``default_x86_64`` to choose x86 based instance types (from the ``m6i`` , ``c6i`` , ``r6i`` , and ``c7i`` instance families) that matches the resource demands of the job queue. - ``default_arm64`` to choose x86 based instance types (from the ``m6g`` , ``c6g`` , ``r6g`` , and ``c7g`` instance families) that matches the resource demands of the job queue. .. epigraph:: Starting on 11/01/2025 the behavior of ``optimal`` is going to be changed to match ``default_x86_64`` . During the change your instance families could be updated to a newer generation. You do not need to perform any actions for the upgrade to happen. For more information about change, see `Optimal instance type configuration to receive automatic instance family updates <https://docs.aws.amazon.com/batch/latest/userguide/optimal-default-instance-troubleshooting.html>`_ . > Instance family availability varies by AWS Region . For example, some AWS Region s may not have any fourth generation instance families but have fifth and sixth generation instance families. When using ``default_x86_64`` or ``default_arm64`` instance bundles, AWS Batch selects instance families based on a balance of cost-effectiveness and performance. While newer generation instances often provide better price-performance, AWS Batch may choose an earlier generation instance family if it provides the optimal combination of availability, cost, and performance for your workload. For example, in an AWS Region where both c6i and c7i instances are available, AWS Batch might select c6i instances if they offer better cost-effectiveness for your specific job requirements. For more information on AWS Batch instance types and AWS Region availability, see `Instance type compute table <https://docs.aws.amazon.com/batch/latest/userguide/instance-type-compute-table.html>`_ in the *AWS Batch User Guide* . AWS Batch periodically updates your instances in default bundles to newer, more cost-effective options. Updates happen automatically without requiring any action from you. Your workloads continue running during updates with no interruption > This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it. > When you create a compute environment, the instance types that you select for the compute environment must share the same architecture. For example, you can't mix x86 and ARM instances in the same compute environment.
            :param launch_template: The launch template to use for your compute resources. Any other compute resource parameters that you specify in a `CreateComputeEnvironment <https://docs.aws.amazon.com/batch/latest/APIReference/API_CreateComputeEnvironment.html>`_ API operation override the same parameters in the launch template. You must specify either the launch template ID or launch template name in the request, but not both. For more information, see `Launch Template Support <https://docs.aws.amazon.com/batch/latest/userguide/launch-templates.html>`_ in the ** . Removing the launch template from a compute environment will not remove the AMI specified in the launch template. In order to update the AMI specified in a launch template, the ``updateToLatestImageVersion`` parameter must be set to ``true`` . When updating a compute environment, changing the launch template requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the ** . .. epigraph:: This parameter isn't applicable to jobs running on Fargate resources, and shouldn't be specified.
            :param maxv_cpus: The maximum number of Amazon EC2 vCPUs that an environment can reach. .. epigraph:: With ``BEST_FIT_PROGRESSIVE`` , ``SPOT_CAPACITY_OPTIMIZED`` and ``SPOT_PRICE_CAPACITY_OPTIMIZED`` (recommended) strategies using On-Demand or Spot Instances, and the ``BEST_FIT`` strategy using Spot Instances, AWS Batch might need to exceed ``maxvCpus`` to meet your capacity requirements. In this event, AWS Batch never exceeds ``maxvCpus`` by more than a single instance.
            :param minv_cpus: The minimum number of vCPUs that an environment should maintain (even if the compute environment is ``DISABLED`` ). .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.
            :param placement_group: The Amazon EC2 placement group to associate with your compute resources. If you intend to submit multi-node parallel jobs to your compute environment, you should consider creating a cluster placement group and associate it with your compute resources. This keeps your multi-node parallel job on a logical grouping of instances within a single Availability Zone with high network flow potential. For more information, see `Placement groups <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html>`_ in the *Amazon EC2 User Guide for Linux Instances* . When updating a compute environment, changing the placement group requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.
            :param security_group_ids: The Amazon EC2 security groups that are associated with instances launched in the compute environment. This parameter is required for Fargate compute resources, where it can contain up to 5 security groups. For Fargate compute resources, providing an empty list is handled as if this parameter wasn't specified and no change is made. For Amazon EC2 compute resources, providing an empty list removes the security groups from the compute resource. When updating a compute environment, changing the Amazon EC2 security groups requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .
            :param spot_iam_fleet_role: The Amazon Resource Name (ARN) of the Amazon EC2 Spot Fleet IAM role applied to a ``SPOT`` compute environment. This role is required if the allocation strategy set to ``BEST_FIT`` or if the allocation strategy isn't specified. For more information, see `Amazon EC2 spot fleet role <https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html>`_ in the *AWS Batch User Guide* . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it. > To tag your Spot Instances on creation, the Spot Fleet IAM role specified here must use the newer *AmazonEC2SpotFleetTaggingRole* managed policy. The previously recommended *AmazonEC2SpotFleetRole* managed policy doesn't have the required permissions to tag Spot Instances. For more information, see `Spot instances not tagged on creation <https://docs.aws.amazon.com/batch/latest/userguide/troubleshooting.html#spot-instance-no-tag>`_ in the *AWS Batch User Guide* .
            :param subnets: The VPC subnets where the compute resources are launched. Fargate compute resources can contain up to 16 subnets. For Fargate compute resources, providing an empty list will be handled as if this parameter wasn't specified and no change is made. For Amazon EC2 compute resources, providing an empty list removes the VPC subnets from the compute resource. For more information, see `VPCs and subnets <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`_ in the *Amazon VPC User Guide* . When updating a compute environment, changing the VPC subnets requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . .. epigraph:: AWS Batch on Amazon EC2 and AWS Batch on Amazon EKS support Local Zones. For more information, see `Local Zones <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-local-zones>`_ in the *Amazon EC2 User Guide for Linux Instances* , `Amazon EKS and AWS Local Zones <https://docs.aws.amazon.com/eks/latest/userguide/local-zones.html>`_ in the *Amazon EKS User Guide* and `Amazon ECS clusters in Local Zones, Wavelength Zones, and AWS Outposts <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-regions-zones.html#clusters-local-zones>`_ in the *Amazon ECS Developer Guide* . AWS Batch on Fargate doesn't currently support Local Zones.
            :param tags: Key-value pair tags to be applied to Amazon EC2 resources that are launched in the compute environment. For AWS Batch , these take the form of ``"String1": "String2"`` , where ``String1`` is the tag key and ``String2`` is the tag value (for example, ``{ "Name": "Batch Instance - C4OnDemand" }`` ). This is helpful for recognizing your Batch instances in the Amazon EC2 console. These tags aren't seen when using the AWS Batch ``ListTagsForResource`` API operation. When updating a compute environment, changing this setting requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.
            :param type: The type of compute environment: ``EC2`` , ``SPOT`` , ``FARGATE`` , or ``FARGATE_SPOT`` . For more information, see `Compute environments <https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html>`_ in the *AWS Batch User Guide* . If you choose ``SPOT`` , you must also specify an Amazon EC2 Spot Fleet role with the ``spotIamFleetRole`` parameter. For more information, see `Amazon EC2 spot fleet role <https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html>`_ in the *AWS Batch User Guide* . When updating compute environment, changing the type of a compute environment requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . When updating the type of a compute environment, changing between ``EC2`` and ``SPOT`` or between ``FARGATE`` and ``FARGATE_SPOT`` will initiate an infrastructure update, but if you switch between ``EC2`` and ``FARGATE`` , CloudFormation will create a new compute environment.
            :param update_to_latest_image_version: Specifies whether the AMI ID is updated to the latest one that's supported by AWS Batch when the compute environment has an infrastructure update. The default value is ``false`` . .. epigraph:: An AMI ID can either be specified in the ``imageId`` or ``imageIdOverride`` parameters or be determined by the launch template that's specified in the ``launchTemplate`` parameter. If an AMI ID is specified any of these ways, this parameter is ignored. For more information about to update AMI IDs during an infrastructure update, see `Updating the AMI ID <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html#updating-compute-environments-ami>`_ in the *AWS Batch User Guide* . When updating a compute environment, changing this setting requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . Default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                compute_resources_property = batch_mixins.CfnComputeEnvironmentPropsMixin.ComputeResourcesProperty(
                    allocation_strategy="allocationStrategy",
                    bid_percentage=123,
                    desiredv_cpus=123,
                    ec2_configuration=[batch_mixins.CfnComputeEnvironmentPropsMixin.Ec2ConfigurationObjectProperty(
                        image_id_override="imageIdOverride",
                        image_kubernetes_version="imageKubernetesVersion",
                        image_type="imageType"
                    )],
                    ec2_key_pair="ec2KeyPair",
                    image_id="imageId",
                    instance_role="instanceRole",
                    instance_types=["instanceTypes"],
                    launch_template=batch_mixins.CfnComputeEnvironmentPropsMixin.LaunchTemplateSpecificationProperty(
                        launch_template_id="launchTemplateId",
                        launch_template_name="launchTemplateName",
                        overrides=[batch_mixins.CfnComputeEnvironmentPropsMixin.LaunchTemplateSpecificationOverrideProperty(
                            launch_template_id="launchTemplateId",
                            launch_template_name="launchTemplateName",
                            target_instance_types=["targetInstanceTypes"],
                            userdata_type="userdataType",
                            version="version"
                        )],
                        userdata_type="userdataType",
                        version="version"
                    ),
                    maxv_cpus=123,
                    minv_cpus=123,
                    placement_group="placementGroup",
                    security_group_ids=["securityGroupIds"],
                    spot_iam_fleet_role="spotIamFleetRole",
                    subnets=["subnets"],
                    tags={
                        "tags_key": "tags"
                    },
                    type="type",
                    update_to_latest_image_version=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5d66f10fa1b3e88b935bc597bc33872c12fbbc3eafb16866ae2d40e801c98a64)
                check_type(argname="argument allocation_strategy", value=allocation_strategy, expected_type=type_hints["allocation_strategy"])
                check_type(argname="argument bid_percentage", value=bid_percentage, expected_type=type_hints["bid_percentage"])
                check_type(argname="argument desiredv_cpus", value=desiredv_cpus, expected_type=type_hints["desiredv_cpus"])
                check_type(argname="argument ec2_configuration", value=ec2_configuration, expected_type=type_hints["ec2_configuration"])
                check_type(argname="argument ec2_key_pair", value=ec2_key_pair, expected_type=type_hints["ec2_key_pair"])
                check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
                check_type(argname="argument instance_role", value=instance_role, expected_type=type_hints["instance_role"])
                check_type(argname="argument instance_types", value=instance_types, expected_type=type_hints["instance_types"])
                check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
                check_type(argname="argument maxv_cpus", value=maxv_cpus, expected_type=type_hints["maxv_cpus"])
                check_type(argname="argument minv_cpus", value=minv_cpus, expected_type=type_hints["minv_cpus"])
                check_type(argname="argument placement_group", value=placement_group, expected_type=type_hints["placement_group"])
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument spot_iam_fleet_role", value=spot_iam_fleet_role, expected_type=type_hints["spot_iam_fleet_role"])
                check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument update_to_latest_image_version", value=update_to_latest_image_version, expected_type=type_hints["update_to_latest_image_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allocation_strategy is not None:
                self._values["allocation_strategy"] = allocation_strategy
            if bid_percentage is not None:
                self._values["bid_percentage"] = bid_percentage
            if desiredv_cpus is not None:
                self._values["desiredv_cpus"] = desiredv_cpus
            if ec2_configuration is not None:
                self._values["ec2_configuration"] = ec2_configuration
            if ec2_key_pair is not None:
                self._values["ec2_key_pair"] = ec2_key_pair
            if image_id is not None:
                self._values["image_id"] = image_id
            if instance_role is not None:
                self._values["instance_role"] = instance_role
            if instance_types is not None:
                self._values["instance_types"] = instance_types
            if launch_template is not None:
                self._values["launch_template"] = launch_template
            if maxv_cpus is not None:
                self._values["maxv_cpus"] = maxv_cpus
            if minv_cpus is not None:
                self._values["minv_cpus"] = minv_cpus
            if placement_group is not None:
                self._values["placement_group"] = placement_group
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if spot_iam_fleet_role is not None:
                self._values["spot_iam_fleet_role"] = spot_iam_fleet_role
            if subnets is not None:
                self._values["subnets"] = subnets
            if tags is not None:
                self._values["tags"] = tags
            if type is not None:
                self._values["type"] = type
            if update_to_latest_image_version is not None:
                self._values["update_to_latest_image_version"] = update_to_latest_image_version

        @builtins.property
        def allocation_strategy(self) -> typing.Optional[builtins.str]:
            '''The allocation strategy to use for the compute resource if not enough instances of the best fitting instance type can be allocated.

            This might be because of availability of the instance type in the Region or `Amazon EC2 service limits <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html>`_ . For more information, see `Allocation strategies <https://docs.aws.amazon.com/batch/latest/userguide/allocation-strategies.html>`_ in the *AWS Batch User Guide* .

            When updating a compute environment, changing the allocation strategy requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . ``BEST_FIT`` is not supported when updating a compute environment.
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources, and shouldn't be specified.

            - **BEST_FIT (default)** - AWS Batch selects an instance type that best fits the needs of the jobs with a preference for the lowest-cost instance type. If additional instances of the selected instance type aren't available, AWS Batch waits for the additional instances to be available. If there aren't enough instances available, or if the user is reaching `Amazon EC2 service limits <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html>`_ then additional jobs aren't run until the currently running jobs have completed. This allocation strategy keeps costs lower but can limit scaling. If you are using Spot Fleets with ``BEST_FIT`` then the Spot Fleet IAM role must be specified.
            - **BEST_FIT_PROGRESSIVE** - AWS Batch will select additional instance types that are large enough to meet the requirements of the jobs in the queue, with a preference for instance types with a lower cost per unit vCPU. If additional instances of the previously selected instance types aren't available, AWS Batch will select new instance types.
            - **SPOT_CAPACITY_OPTIMIZED** - AWS Batch will select one or more instance types that are large enough to meet the requirements of the jobs in the queue, with a preference for instance types that are less likely to be interrupted. This allocation strategy is only available for Spot Instance compute resources.
            - **SPOT_PRICE_CAPACITY_OPTIMIZED** - The price and capacity optimized allocation strategy looks at both price and capacity to select the Spot Instance pools that are the least likely to be interrupted and have the lowest possible price. This allocation strategy is only available for Spot Instance compute resources.

            .. epigraph::

               We recommend that you use ``SPOT_PRICE_CAPACITY_OPTIMIZED`` rather than ``SPOT_CAPACITY_OPTIMIZED`` in most instances.

            With ``BEST_FIT_PROGRESSIVE`` , ``SPOT_CAPACITY_OPTIMIZED`` , and ``SPOT_PRICE_CAPACITY_OPTIMIZED`` allocation strategies using On-Demand or Spot Instances, and the ``BEST_FIT`` strategy using Spot Instances, AWS Batch might need to go above ``maxvCpus`` to meet your capacity requirements. In this event, AWS Batch never exceeds ``maxvCpus`` by more than a single instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-allocationstrategy
            '''
            result = self._values.get("allocation_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bid_percentage(self) -> typing.Optional[jsii.Number]:
            '''The maximum percentage that a Spot Instance price can be when compared with the On-Demand price for that instance type before instances are launched.

            For example, if your maximum percentage is 20%, the Spot price must be less than 20% of the current On-Demand price for that Amazon EC2 instance. You always pay the lowest (market) price and never more than your maximum percentage. For most use cases, we recommend leaving this field empty.

            When updating a compute environment, changing the bid percentage requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-bidpercentage
            '''
            result = self._values.get("bid_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def desiredv_cpus(self) -> typing.Optional[jsii.Number]:
            '''The desired number of vCPUS in the compute environment.

            AWS Batch modifies this value between the minimum and maximum values based on job queue demand.
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it. > AWS Batch doesn't support changing the desired number of vCPUs of an existing compute environment. Don't specify this parameter for compute environments using Amazon EKS clusters. > When you update the ``desiredvCpus`` setting, the value must be between the ``minvCpus`` and ``maxvCpus`` values.

               Additionally, the updated ``desiredvCpus`` value must be greater than or equal to the current ``desiredvCpus`` value. For more information, see `Troubleshooting AWS Batch <https://docs.aws.amazon.com/batch/latest/userguide/troubleshooting.html#error-desired-vcpus-update>`_ in the *AWS Batch User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-desiredvcpus
            '''
            result = self._values.get("desiredv_cpus")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def ec2_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeEnvironmentPropsMixin.Ec2ConfigurationObjectProperty"]]]]:
            '''Provides information used to select Amazon Machine Images (AMIs) for Amazon EC2 instances in the compute environment.

            If ``Ec2Configuration`` isn't specified, the default is ``ECS_AL2`` .

            When updating a compute environment, changing this setting requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . To remove the Amazon EC2 configuration and any custom AMI ID specified in ``imageIdOverride`` , set this value to an empty string.

            One or two values can be provided.
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2configuration
            '''
            result = self._values.get("ec2_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeEnvironmentPropsMixin.Ec2ConfigurationObjectProperty"]]]], result)

        @builtins.property
        def ec2_key_pair(self) -> typing.Optional[builtins.str]:
            '''The Amazon EC2 key pair that's used for instances launched in the compute environment.

            You can use this key pair to log in to your instances with SSH. To remove the Amazon EC2 key pair, set this value to an empty string.

            When updating a compute environment, changing the Amazon EC2 key pair requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2keypair
            '''
            result = self._values.get("ec2_key_pair")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon Machine Image (AMI) ID used for instances launched in the compute environment.

            This parameter is overridden by the ``imageIdOverride`` member of the ``Ec2Configuration`` structure. To remove the custom AMI ID and use the default AMI ID, set this value to an empty string.

            When updating a compute environment, changing the AMI ID requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it. > The AMI that you choose for a compute environment must match the architecture of the instance types that you intend to use for that compute environment. For example, if your compute environment uses A1 instance types, the compute resource AMI that you choose must support ARM instances. Amazon ECS vends both x86 and ARM versions of the Amazon ECS-optimized Amazon Linux 2 AMI. For more information, see `Amazon ECS-optimized Amazon Linux 2 AMI <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#ecs-optimized-ami-linux-variants.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-imageid
            '''
            result = self._values.get("image_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_role(self) -> typing.Optional[builtins.str]:
            '''The Amazon ECS instance profile applied to Amazon EC2 instances in a compute environment.

            Required for Amazon EC2 instances. You can specify the short name or full Amazon Resource Name (ARN) of an instance profile. For example, ``*ecsInstanceRole*`` or ``arn:aws:iam:: *<aws_account_id>* :instance-profile/ *ecsInstanceRole*`` . For more information, see `Amazon ECS instance role <https://docs.aws.amazon.com/batch/latest/userguide/instance_IAM_role.html>`_ in the *AWS Batch User Guide* .

            When updating a compute environment, changing this setting requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-instancerole
            '''
            result = self._values.get("instance_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The instances types that can be launched.

            You can specify instance families to launch any instance type within those families (for example, ``c5`` or ``p3`` ), or you can specify specific sizes within a family (such as ``c5.8xlarge`` ).

            AWS Batch can select the instance type for you if you choose one of the following:

            - ``optimal`` to select instance types (from the ``c4`` , ``m4`` , ``r4`` , ``c5`` , ``m5`` , and ``r5`` instance families) that match the demand of your job queues.
            - ``default_x86_64`` to choose x86 based instance types (from the ``m6i`` , ``c6i`` , ``r6i`` , and ``c7i`` instance families) that matches the resource demands of the job queue.
            - ``default_arm64`` to choose x86 based instance types (from the ``m6g`` , ``c6g`` , ``r6g`` , and ``c7g`` instance families) that matches the resource demands of the job queue.

            .. epigraph::

               Starting on 11/01/2025 the behavior of ``optimal`` is going to be changed to match ``default_x86_64`` . During the change your instance families could be updated to a newer generation. You do not need to perform any actions for the upgrade to happen. For more information about change, see `Optimal instance type configuration to receive automatic instance family updates <https://docs.aws.amazon.com/batch/latest/userguide/optimal-default-instance-troubleshooting.html>`_ . > Instance family availability varies by AWS Region . For example, some AWS Region s may not have any fourth generation instance families but have fifth and sixth generation instance families.

               When using ``default_x86_64`` or ``default_arm64`` instance bundles, AWS Batch selects instance families based on a balance of cost-effectiveness and performance. While newer generation instances often provide better price-performance, AWS Batch may choose an earlier generation instance family if it provides the optimal combination of availability, cost, and performance for your workload. For example, in an AWS Region where both c6i and c7i instances are available, AWS Batch might select c6i instances if they offer better cost-effectiveness for your specific job requirements. For more information on AWS Batch instance types and AWS Region availability, see `Instance type compute table <https://docs.aws.amazon.com/batch/latest/userguide/instance-type-compute-table.html>`_ in the *AWS Batch User Guide* .

               AWS Batch periodically updates your instances in default bundles to newer, more cost-effective options. Updates happen automatically without requiring any action from you. Your workloads continue running during updates with no interruption > This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it. > When you create a compute environment, the instance types that you select for the compute environment must share the same architecture. For example, you can't mix x86 and ARM instances in the same compute environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-instancetypes
            '''
            result = self._values.get("instance_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def launch_template(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeEnvironmentPropsMixin.LaunchTemplateSpecificationProperty"]]:
            '''The launch template to use for your compute resources.

            Any other compute resource parameters that you specify in a `CreateComputeEnvironment <https://docs.aws.amazon.com/batch/latest/APIReference/API_CreateComputeEnvironment.html>`_ API operation override the same parameters in the launch template. You must specify either the launch template ID or launch template name in the request, but not both. For more information, see `Launch Template Support <https://docs.aws.amazon.com/batch/latest/userguide/launch-templates.html>`_ in the ** . Removing the launch template from a compute environment will not remove the AMI specified in the launch template. In order to update the AMI specified in a launch template, the ``updateToLatestImageVersion`` parameter must be set to ``true`` .

            When updating a compute environment, changing the launch template requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the ** .
            .. epigraph::

               This parameter isn't applicable to jobs running on Fargate resources, and shouldn't be specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-launchtemplate
            '''
            result = self._values.get("launch_template")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeEnvironmentPropsMixin.LaunchTemplateSpecificationProperty"]], result)

        @builtins.property
        def maxv_cpus(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of Amazon EC2 vCPUs that an environment can reach.

            .. epigraph::

               With ``BEST_FIT_PROGRESSIVE`` , ``SPOT_CAPACITY_OPTIMIZED`` and ``SPOT_PRICE_CAPACITY_OPTIMIZED`` (recommended) strategies using On-Demand or Spot Instances, and the ``BEST_FIT`` strategy using Spot Instances, AWS Batch might need to exceed ``maxvCpus`` to meet your capacity requirements. In this event, AWS Batch never exceeds ``maxvCpus`` by more than a single instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-maxvcpus
            '''
            result = self._values.get("maxv_cpus")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def minv_cpus(self) -> typing.Optional[jsii.Number]:
            '''The minimum number of vCPUs that an environment should maintain (even if the compute environment is ``DISABLED`` ).

            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-minvcpus
            '''
            result = self._values.get("minv_cpus")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def placement_group(self) -> typing.Optional[builtins.str]:
            '''The Amazon EC2 placement group to associate with your compute resources.

            If you intend to submit multi-node parallel jobs to your compute environment, you should consider creating a cluster placement group and associate it with your compute resources. This keeps your multi-node parallel job on a logical grouping of instances within a single Availability Zone with high network flow potential. For more information, see `Placement groups <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html>`_ in the *Amazon EC2 User Guide for Linux Instances* .

            When updating a compute environment, changing the placement group requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-placementgroup
            '''
            result = self._values.get("placement_group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The Amazon EC2 security groups that are associated with instances launched in the compute environment.

            This parameter is required for Fargate compute resources, where it can contain up to 5 security groups. For Fargate compute resources, providing an empty list is handled as if this parameter wasn't specified and no change is made. For Amazon EC2 compute resources, providing an empty list removes the security groups from the compute resource.

            When updating a compute environment, changing the Amazon EC2 security groups requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def spot_iam_fleet_role(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon EC2 Spot Fleet IAM role applied to a ``SPOT`` compute environment.

            This role is required if the allocation strategy set to ``BEST_FIT`` or if the allocation strategy isn't specified. For more information, see `Amazon EC2 spot fleet role <https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html>`_ in the *AWS Batch User Guide* .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it. > To tag your Spot Instances on creation, the Spot Fleet IAM role specified here must use the newer *AmazonEC2SpotFleetTaggingRole* managed policy. The previously recommended *AmazonEC2SpotFleetRole* managed policy doesn't have the required permissions to tag Spot Instances. For more information, see `Spot instances not tagged on creation <https://docs.aws.amazon.com/batch/latest/userguide/troubleshooting.html#spot-instance-no-tag>`_ in the *AWS Batch User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-spotiamfleetrole
            '''
            result = self._values.get("spot_iam_fleet_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The VPC subnets where the compute resources are launched.

            Fargate compute resources can contain up to 16 subnets. For Fargate compute resources, providing an empty list will be handled as if this parameter wasn't specified and no change is made. For Amazon EC2 compute resources, providing an empty list removes the VPC subnets from the compute resource. For more information, see `VPCs and subnets <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`_ in the *Amazon VPC User Guide* .

            When updating a compute environment, changing the VPC subnets requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .
            .. epigraph::

               AWS Batch on Amazon EC2 and AWS Batch on Amazon EKS support Local Zones. For more information, see `Local Zones <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-local-zones>`_ in the *Amazon EC2 User Guide for Linux Instances* , `Amazon EKS and AWS Local Zones <https://docs.aws.amazon.com/eks/latest/userguide/local-zones.html>`_ in the *Amazon EKS User Guide* and `Amazon ECS clusters in Local Zones, Wavelength Zones, and AWS Outposts <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-regions-zones.html#clusters-local-zones>`_ in the *Amazon ECS Developer Guide* .

               AWS Batch on Fargate doesn't currently support Local Zones.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-subnets
            '''
            result = self._values.get("subnets")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
            '''Key-value pair tags to be applied to Amazon EC2 resources that are launched in the compute environment.

            For AWS Batch , these take the form of ``"String1": "String2"`` , where ``String1`` is the tag key and ``String2`` is the tag value (for example, ``{ "Name": "Batch Instance - C4OnDemand" }`` ). This is helpful for recognizing your Batch instances in the Amazon EC2 console. These tags aren't seen when using the AWS Batch ``ListTagsForResource`` API operation.

            When updating a compute environment, changing this setting requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of compute environment: ``EC2`` , ``SPOT`` , ``FARGATE`` , or ``FARGATE_SPOT`` .

            For more information, see `Compute environments <https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html>`_ in the *AWS Batch User Guide* .

            If you choose ``SPOT`` , you must also specify an Amazon EC2 Spot Fleet role with the ``spotIamFleetRole`` parameter. For more information, see `Amazon EC2 spot fleet role <https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html>`_ in the *AWS Batch User Guide* .

            When updating compute environment, changing the type of a compute environment requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .

            When updating the type of a compute environment, changing between ``EC2`` and ``SPOT`` or between ``FARGATE`` and ``FARGATE_SPOT`` will initiate an infrastructure update, but if you switch between ``EC2`` and ``FARGATE`` , CloudFormation will create a new compute environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def update_to_latest_image_version(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the AMI ID is updated to the latest one that's supported by AWS Batch when the compute environment has an infrastructure update.

            The default value is ``false`` .
            .. epigraph::

               An AMI ID can either be specified in the ``imageId`` or ``imageIdOverride`` parameters or be determined by the launch template that's specified in the ``launchTemplate`` parameter. If an AMI ID is specified any of these ways, this parameter is ignored. For more information about to update AMI IDs during an infrastructure update, see `Updating the AMI ID <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html#updating-compute-environments-ami>`_ in the *AWS Batch User Guide* .

            When updating a compute environment, changing this setting requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-updatetolatestimageversion
            '''
            result = self._values.get("update_to_latest_image_version")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComputeResourcesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnComputeEnvironmentPropsMixin.Ec2ConfigurationObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "image_id_override": "imageIdOverride",
            "image_kubernetes_version": "imageKubernetesVersion",
            "image_type": "imageType",
        },
    )
    class Ec2ConfigurationObjectProperty:
        def __init__(
            self,
            *,
            image_id_override: typing.Optional[builtins.str] = None,
            image_kubernetes_version: typing.Optional[builtins.str] = None,
            image_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information used to select Amazon Machine Images (AMIs) for instances in the compute environment.

            If ``Ec2Configuration`` isn't specified, the default is ``ECS_AL2`` ( `Amazon Linux 2 <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#al2ami>`_ ).
            .. epigraph::

               This object isn't applicable to jobs that are running on Fargate resources.

            :param image_id_override: The AMI ID used for instances launched in the compute environment that match the image type. This setting overrides the ``imageId`` set in the ``computeResource`` object. .. epigraph:: The AMI that you choose for a compute environment must match the architecture of the instance types that you intend to use for that compute environment. For example, if your compute environment uses A1 instance types, the compute resource AMI that you choose must support ARM instances. Amazon ECS vends both x86 and ARM versions of the Amazon ECS-optimized Amazon Linux 2 AMI. For more information, see `Amazon ECS-optimized Amazon Linux 2 AMI <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#ecs-optimized-ami-linux-variants.html>`_ in the *Amazon Elastic Container Service Developer Guide* .
            :param image_kubernetes_version: The Kubernetes version for the compute environment. If you don't specify a value, the latest version that AWS Batch supports is used.
            :param image_type: The image type to match with the instance type to select an AMI. The supported values are different for ``ECS`` and ``EKS`` resources. - **ECS** - If the ``imageIdOverride`` parameter isn't specified, then a recent `Amazon ECS-optimized Amazon Linux 2 AMI <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#al2ami>`_ ( ``ECS_AL2`` ) is used. If a new image type is specified in an update, but neither an ``imageId`` nor a ``imageIdOverride`` parameter is specified, then the latest Amazon ECS optimized AMI for that image type that's supported by AWS Batch is used. .. epigraph:: AWS will end support for Amazon ECS optimized AL2-optimized and AL2-accelerated AMIs. Starting in January 2026, AWS Batch will change the default AMI for new Amazon ECS compute environments from Amazon Linux 2 to Amazon Linux 2023. We recommend migrating AWS Batch Amazon ECS compute environments to Amazon Linux 2023 to maintain optimal performance and security. For more information on upgrading from AL2 to AL2023, see `How to migrate from ECS AL2 to ECS AL2023 <https://docs.aws.amazon.com/batch/latest/userguide/ecs-migration-2023.html>`_ in the *AWS Batch User Guide* . - **ECS_AL2** - `Amazon Linux 2 <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#al2ami>`_ : Default for all non-GPU instance families. - **ECS_AL2_NVIDIA** - `Amazon Linux 2 (GPU) <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#gpuami>`_ : Default for all GPU instance families (for example ``P4`` and ``G4`` ) and can be used for all non AWS Graviton-based instance types. - **ECS_AL2023** - `Amazon Linux 2023 <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html>`_ : AWS Batch supports Amazon Linux 2023. .. epigraph:: Amazon Linux 2023 does not support ``A1`` instances. - **ECS_AL2023_NVIDIA** - `Amazon Linux 2023 (GPU) <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#gpuami>`_ : For all GPU instance families and can be used for all non AWS Graviton-based instance types. .. epigraph:: ECS_AL2023_NVIDIA doesn't support ``p3`` and ``g3`` instance types. - **EKS** - If the ``imageIdOverride`` parameter isn't specified, then a recent `Amazon EKS-optimized Amazon Linux 2023 AMI <https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html>`_ ( ``EKS_AL2023`` ) is used. If a new image type is specified in an update, but neither an ``imageId`` nor a ``imageIdOverride`` parameter is specified, then the latest Amazon EKS optimized AMI for that image type that AWS Batch supports is used. .. epigraph:: Amazon Linux 2023 AMIs are the default on AWS Batch for Amazon EKS. AWS will end support for Amazon EKS AL2-optimized and AL2-accelerated AMIs, starting 11/26/25. You can continue using AWS Batch -provided Amazon EKS optimized Amazon Linux 2 AMIs on your Amazon EKS compute environments beyond the 11/26/25 end-of-support date, these compute environments will no longer receive any new software updates, security patches, or bug fixes from AWS . For more information on upgrading from AL2 to AL2023, see `How to upgrade from EKS AL2 to EKS AL2023 <https://docs.aws.amazon.com/batch/latest/userguide/eks-migration-2023.html>`_ in the *AWS Batch User Guide* . - **EKS_AL2** - `Amazon Linux 2 <https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html>`_ : Used for non-GPU instance families. - **EKS_AL2_NVIDIA** - `Amazon Linux 2 (accelerated) <https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html>`_ : Used for GPU instance families (for example, ``P4`` and ``G4`` ) and can be used for all non AWS Graviton-based instance types. - **EKS_AL2023** - `Amazon Linux 2023 <https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html>`_ : Default for non-GPU instance families. .. epigraph:: Amazon Linux 2023 does not support ``A1`` instances. - **EKS_AL2023_NVIDIA** - `Amazon Linux 2023 (accelerated) <https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html>`_ : Default for GPU instance families and can be used for all non AWS Graviton-based instance types.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-ec2configurationobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                ec2_configuration_object_property = batch_mixins.CfnComputeEnvironmentPropsMixin.Ec2ConfigurationObjectProperty(
                    image_id_override="imageIdOverride",
                    image_kubernetes_version="imageKubernetesVersion",
                    image_type="imageType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__00023ed80a08e816151f9b1563df188d68d5a889926e8e3c4085b54c3ad37c7b)
                check_type(argname="argument image_id_override", value=image_id_override, expected_type=type_hints["image_id_override"])
                check_type(argname="argument image_kubernetes_version", value=image_kubernetes_version, expected_type=type_hints["image_kubernetes_version"])
                check_type(argname="argument image_type", value=image_type, expected_type=type_hints["image_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if image_id_override is not None:
                self._values["image_id_override"] = image_id_override
            if image_kubernetes_version is not None:
                self._values["image_kubernetes_version"] = image_kubernetes_version
            if image_type is not None:
                self._values["image_type"] = image_type

        @builtins.property
        def image_id_override(self) -> typing.Optional[builtins.str]:
            '''The AMI ID used for instances launched in the compute environment that match the image type.

            This setting overrides the ``imageId`` set in the ``computeResource`` object.
            .. epigraph::

               The AMI that you choose for a compute environment must match the architecture of the instance types that you intend to use for that compute environment. For example, if your compute environment uses A1 instance types, the compute resource AMI that you choose must support ARM instances. Amazon ECS vends both x86 and ARM versions of the Amazon ECS-optimized Amazon Linux 2 AMI. For more information, see `Amazon ECS-optimized Amazon Linux 2 AMI <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#ecs-optimized-ami-linux-variants.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-ec2configurationobject.html#cfn-batch-computeenvironment-ec2configurationobject-imageidoverride
            '''
            result = self._values.get("image_id_override")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_kubernetes_version(self) -> typing.Optional[builtins.str]:
            '''The Kubernetes version for the compute environment.

            If you don't specify a value, the latest version that AWS Batch supports is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-ec2configurationobject.html#cfn-batch-computeenvironment-ec2configurationobject-imagekubernetesversion
            '''
            result = self._values.get("image_kubernetes_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_type(self) -> typing.Optional[builtins.str]:
            '''The image type to match with the instance type to select an AMI.

            The supported values are different for ``ECS`` and ``EKS`` resources.

            - **ECS** - If the ``imageIdOverride`` parameter isn't specified, then a recent `Amazon ECS-optimized Amazon Linux 2 AMI <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#al2ami>`_ ( ``ECS_AL2`` ) is used. If a new image type is specified in an update, but neither an ``imageId`` nor a ``imageIdOverride`` parameter is specified, then the latest Amazon ECS optimized AMI for that image type that's supported by AWS Batch is used.

            .. epigraph::

               AWS will end support for Amazon ECS optimized AL2-optimized and AL2-accelerated AMIs. Starting in January 2026, AWS Batch will change the default AMI for new Amazon ECS compute environments from Amazon Linux 2 to Amazon Linux 2023. We recommend migrating AWS Batch Amazon ECS compute environments to Amazon Linux 2023 to maintain optimal performance and security. For more information on upgrading from AL2 to AL2023, see `How to migrate from ECS AL2 to ECS AL2023 <https://docs.aws.amazon.com/batch/latest/userguide/ecs-migration-2023.html>`_ in the *AWS Batch User Guide* .

            - **ECS_AL2** - `Amazon Linux 2 <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#al2ami>`_ : Default for all non-GPU instance families.
            - **ECS_AL2_NVIDIA** - `Amazon Linux 2 (GPU) <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#gpuami>`_ : Default for all GPU instance families (for example ``P4`` and ``G4`` ) and can be used for all non AWS Graviton-based instance types.
            - **ECS_AL2023** - `Amazon Linux 2023 <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html>`_ : AWS Batch supports Amazon Linux 2023.

            .. epigraph::

               Amazon Linux 2023 does not support ``A1`` instances.

            - **ECS_AL2023_NVIDIA** - `Amazon Linux 2023 (GPU) <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#gpuami>`_ : For all GPU instance families and can be used for all non AWS Graviton-based instance types.

            .. epigraph::

               ECS_AL2023_NVIDIA doesn't support ``p3`` and ``g3`` instance types.

            - **EKS** - If the ``imageIdOverride`` parameter isn't specified, then a recent `Amazon EKS-optimized Amazon Linux 2023 AMI <https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html>`_ ( ``EKS_AL2023`` ) is used. If a new image type is specified in an update, but neither an ``imageId`` nor a ``imageIdOverride`` parameter is specified, then the latest Amazon EKS optimized AMI for that image type that AWS Batch supports is used.

            .. epigraph::

               Amazon Linux 2023 AMIs are the default on AWS Batch for Amazon EKS.

               AWS will end support for Amazon EKS AL2-optimized and AL2-accelerated AMIs, starting 11/26/25. You can continue using AWS Batch -provided Amazon EKS optimized Amazon Linux 2 AMIs on your Amazon EKS compute environments beyond the 11/26/25 end-of-support date, these compute environments will no longer receive any new software updates, security patches, or bug fixes from AWS . For more information on upgrading from AL2 to AL2023, see `How to upgrade from EKS AL2 to EKS AL2023 <https://docs.aws.amazon.com/batch/latest/userguide/eks-migration-2023.html>`_ in the *AWS Batch User Guide* .

            - **EKS_AL2** - `Amazon Linux 2 <https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html>`_ : Used for non-GPU instance families.
            - **EKS_AL2_NVIDIA** - `Amazon Linux 2 (accelerated) <https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html>`_ : Used for GPU instance families (for example, ``P4`` and ``G4`` ) and can be used for all non AWS Graviton-based instance types.
            - **EKS_AL2023** - `Amazon Linux 2023 <https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html>`_ : Default for non-GPU instance families.

            .. epigraph::

               Amazon Linux 2023 does not support ``A1`` instances.

            - **EKS_AL2023_NVIDIA** - `Amazon Linux 2023 (accelerated) <https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html>`_ : Default for GPU instance families and can be used for all non AWS Graviton-based instance types.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-ec2configurationobject.html#cfn-batch-computeenvironment-ec2configurationobject-imagetype
            '''
            result = self._values.get("image_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "Ec2ConfigurationObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnComputeEnvironmentPropsMixin.EksConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "eks_cluster_arn": "eksClusterArn",
            "kubernetes_namespace": "kubernetesNamespace",
        },
    )
    class EksConfigurationProperty:
        def __init__(
            self,
            *,
            eks_cluster_arn: typing.Optional[builtins.str] = None,
            kubernetes_namespace: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for the Amazon EKS cluster that supports the AWS Batch compute environment.

            The cluster must exist before the compute environment can be created.

            :param eks_cluster_arn: The Amazon Resource Name (ARN) of the Amazon EKS cluster. An example is ``arn: *aws* :eks: *us-east-1* : *123456789012* :cluster/ *ClusterForBatch*`` .
            :param kubernetes_namespace: The namespace of the Amazon EKS cluster. AWS Batch manages pods in this namespace. The value can't left empty or null. It must be fewer than 64 characters long, can't be set to ``default`` , can't start with " ``kube-`` ," and must match this regular expression: ``^[a-z0-9]([-a-z0-9]*[a-z0-9])?$`` . For more information, see `Namespaces <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/>`_ in the Kubernetes documentation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-eksconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                eks_configuration_property = batch_mixins.CfnComputeEnvironmentPropsMixin.EksConfigurationProperty(
                    eks_cluster_arn="eksClusterArn",
                    kubernetes_namespace="kubernetesNamespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7b8d407ca69cf2ff1009c4f05a24470c07dbeb2a4979c43bb859742ebd24c00b)
                check_type(argname="argument eks_cluster_arn", value=eks_cluster_arn, expected_type=type_hints["eks_cluster_arn"])
                check_type(argname="argument kubernetes_namespace", value=kubernetes_namespace, expected_type=type_hints["kubernetes_namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if eks_cluster_arn is not None:
                self._values["eks_cluster_arn"] = eks_cluster_arn
            if kubernetes_namespace is not None:
                self._values["kubernetes_namespace"] = kubernetes_namespace

        @builtins.property
        def eks_cluster_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon EKS cluster.

            An example is ``arn: *aws* :eks: *us-east-1* : *123456789012* :cluster/ *ClusterForBatch*`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-eksconfiguration.html#cfn-batch-computeenvironment-eksconfiguration-eksclusterarn
            '''
            result = self._values.get("eks_cluster_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kubernetes_namespace(self) -> typing.Optional[builtins.str]:
            '''The namespace of the Amazon EKS cluster.

            AWS Batch manages pods in this namespace. The value can't left empty or null. It must be fewer than 64 characters long, can't be set to ``default`` , can't start with " ``kube-`` ," and must match this regular expression: ``^[a-z0-9]([-a-z0-9]*[a-z0-9])?$`` . For more information, see `Namespaces <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/>`_ in the Kubernetes documentation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-eksconfiguration.html#cfn-batch-computeenvironment-eksconfiguration-kubernetesnamespace
            '''
            result = self._values.get("kubernetes_namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnComputeEnvironmentPropsMixin.LaunchTemplateSpecificationOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={
            "launch_template_id": "launchTemplateId",
            "launch_template_name": "launchTemplateName",
            "target_instance_types": "targetInstanceTypes",
            "userdata_type": "userdataType",
            "version": "version",
        },
    )
    class LaunchTemplateSpecificationOverrideProperty:
        def __init__(
            self,
            *,
            launch_template_id: typing.Optional[builtins.str] = None,
            launch_template_name: typing.Optional[builtins.str] = None,
            target_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            userdata_type: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents a launch template to use in place of the default launch template.

            You must specify either the launch template ID or launch template name in the request, but not both.

            If security groups are specified using both the ``securityGroupIds`` parameter of ``CreateComputeEnvironment`` and the launch template, the values in the ``securityGroupIds`` parameter of ``CreateComputeEnvironment`` will be used.

            You can define up to ten (10) overrides for each compute environment.
            .. epigraph::

               This object isn't applicable to jobs that are running on Fargate resources. > To unset all override templates for a compute environment, you can pass an empty array to the `UpdateComputeEnvironment.overrides <https://docs.aws.amazon.com/batch/latest/APIReference/API_UpdateComputeEnvironment.html>`_ parameter, or not include the ``overrides`` parameter when submitting the ``UpdateComputeEnvironment`` API operation.

            :param launch_template_id: The ID of the launch template. *Note:* If you specify the ``launchTemplateId`` you can't specify the ``launchTemplateName`` as well.
            :param launch_template_name: The name of the launch template. *Note:* If you specify the ``launchTemplateName`` you can't specify the ``launchTemplateId`` as well.
            :param target_instance_types: The instance type or family that this override launch template should be applied to. This parameter is required when defining a launch template override. Information included in this parameter must meet the following requirements: - Must be a valid Amazon EC2 instance type or family. - The following AWS Batch ``InstanceTypes`` are not allowed: ``optimal`` , ``default_x86_64`` , and ``default_arm64`` . - ``targetInstanceTypes`` can target only instance types and families that are included within the ```ComputeResource.instanceTypes`` <https://docs.aws.amazon.com/batch/latest/APIReference/API_ComputeResource.html#Batch-Type-ComputeResource-instanceTypes>`_ set. ``targetInstanceTypes`` doesn't need to include all of the instances from the ``instanceType`` set, but at least a subset. For example, if ``ComputeResource.instanceTypes`` includes ``[m5, g5]`` , ``targetInstanceTypes`` can include ``[m5.2xlarge]`` and ``[m5.large]`` but not ``[c5.large]`` . - ``targetInstanceTypes`` included within the same launch template override or across launch template overrides can't overlap for the same compute environment. For example, you can't define one launch template override to target an instance family and another define an instance type within this same family.
            :param userdata_type: The EKS node initialization process to use. You only need to specify this value if you are using a custom AMI. The default value is ``EKS_BOOTSTRAP_SH`` . If *imageType* is a custom AMI based on EKS_AL2023 or EKS_AL2023_NVIDIA then you must choose ``EKS_NODEADM`` .
            :param version: The version number of the launch template, ``$Default`` , or ``$Latest`` . If the value is ``$Default`` , the default version of the launch template is used. If the value is ``$Latest`` , the latest version of the launch template is used. .. epigraph:: If the AMI ID that's used in a compute environment is from the launch template, the AMI isn't changed when the compute environment is updated. It's only changed if the ``updateToLatestImageVersion`` parameter for the compute environment is set to ``true`` . During an infrastructure update, if either ``$Default`` or ``$Latest`` is specified, AWS Batch re-evaluates the launch template version, and it might use a different version of the launch template. This is the case even if the launch template isn't specified in the update. When updating a compute environment, changing the launch template requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . Default: ``$Default`` Latest: ``$Latest``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecificationoverride.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                launch_template_specification_override_property = batch_mixins.CfnComputeEnvironmentPropsMixin.LaunchTemplateSpecificationOverrideProperty(
                    launch_template_id="launchTemplateId",
                    launch_template_name="launchTemplateName",
                    target_instance_types=["targetInstanceTypes"],
                    userdata_type="userdataType",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__83068de22d881a95f456528ce0e40a31cf96232d6ffbfd9972cca6ca8117eab3)
                check_type(argname="argument launch_template_id", value=launch_template_id, expected_type=type_hints["launch_template_id"])
                check_type(argname="argument launch_template_name", value=launch_template_name, expected_type=type_hints["launch_template_name"])
                check_type(argname="argument target_instance_types", value=target_instance_types, expected_type=type_hints["target_instance_types"])
                check_type(argname="argument userdata_type", value=userdata_type, expected_type=type_hints["userdata_type"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if launch_template_id is not None:
                self._values["launch_template_id"] = launch_template_id
            if launch_template_name is not None:
                self._values["launch_template_name"] = launch_template_name
            if target_instance_types is not None:
                self._values["target_instance_types"] = target_instance_types
            if userdata_type is not None:
                self._values["userdata_type"] = userdata_type
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def launch_template_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the launch template.

            *Note:* If you specify the ``launchTemplateId`` you can't specify the ``launchTemplateName`` as well.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecificationoverride.html#cfn-batch-computeenvironment-launchtemplatespecificationoverride-launchtemplateid
            '''
            result = self._values.get("launch_template_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def launch_template_name(self) -> typing.Optional[builtins.str]:
            '''The name of the launch template.

            *Note:* If you specify the ``launchTemplateName`` you can't specify the ``launchTemplateId`` as well.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecificationoverride.html#cfn-batch-computeenvironment-launchtemplatespecificationoverride-launchtemplatename
            '''
            result = self._values.get("launch_template_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_instance_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The instance type or family that this override launch template should be applied to.

            This parameter is required when defining a launch template override.

            Information included in this parameter must meet the following requirements:

            - Must be a valid Amazon EC2 instance type or family.
            - The following AWS Batch ``InstanceTypes`` are not allowed: ``optimal`` , ``default_x86_64`` , and ``default_arm64`` .
            - ``targetInstanceTypes`` can target only instance types and families that are included within the ```ComputeResource.instanceTypes`` <https://docs.aws.amazon.com/batch/latest/APIReference/API_ComputeResource.html#Batch-Type-ComputeResource-instanceTypes>`_ set. ``targetInstanceTypes`` doesn't need to include all of the instances from the ``instanceType`` set, but at least a subset. For example, if ``ComputeResource.instanceTypes`` includes ``[m5, g5]`` , ``targetInstanceTypes`` can include ``[m5.2xlarge]`` and ``[m5.large]`` but not ``[c5.large]`` .
            - ``targetInstanceTypes`` included within the same launch template override or across launch template overrides can't overlap for the same compute environment. For example, you can't define one launch template override to target an instance family and another define an instance type within this same family.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecificationoverride.html#cfn-batch-computeenvironment-launchtemplatespecificationoverride-targetinstancetypes
            '''
            result = self._values.get("target_instance_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def userdata_type(self) -> typing.Optional[builtins.str]:
            '''The EKS node initialization process to use.

            You only need to specify this value if you are using a custom AMI. The default value is ``EKS_BOOTSTRAP_SH`` . If *imageType* is a custom AMI based on EKS_AL2023 or EKS_AL2023_NVIDIA then you must choose ``EKS_NODEADM`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecificationoverride.html#cfn-batch-computeenvironment-launchtemplatespecificationoverride-userdatatype
            '''
            result = self._values.get("userdata_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The version number of the launch template, ``$Default`` , or ``$Latest`` .

            If the value is ``$Default`` , the default version of the launch template is used. If the value is ``$Latest`` , the latest version of the launch template is used.
            .. epigraph::

               If the AMI ID that's used in a compute environment is from the launch template, the AMI isn't changed when the compute environment is updated. It's only changed if the ``updateToLatestImageVersion`` parameter for the compute environment is set to ``true`` . During an infrastructure update, if either ``$Default`` or ``$Latest`` is specified, AWS Batch re-evaluates the launch template version, and it might use a different version of the launch template. This is the case even if the launch template isn't specified in the update. When updating a compute environment, changing the launch template requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .

            Default: ``$Default``

            Latest: ``$Latest``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecificationoverride.html#cfn-batch-computeenvironment-launchtemplatespecificationoverride-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LaunchTemplateSpecificationOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnComputeEnvironmentPropsMixin.LaunchTemplateSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "launch_template_id": "launchTemplateId",
            "launch_template_name": "launchTemplateName",
            "overrides": "overrides",
            "userdata_type": "userdataType",
            "version": "version",
        },
    )
    class LaunchTemplateSpecificationProperty:
        def __init__(
            self,
            *,
            launch_template_id: typing.Optional[builtins.str] = None,
            launch_template_name: typing.Optional[builtins.str] = None,
            overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComputeEnvironmentPropsMixin.LaunchTemplateSpecificationOverrideProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            userdata_type: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents a launch template that's associated with a compute resource.

            You must specify either the launch template ID or launch template name in the request, but not both.

            If security groups are specified using both the ``securityGroupIds`` parameter of ``CreateComputeEnvironment`` and the launch template, the values in the ``securityGroupIds`` parameter of ``CreateComputeEnvironment`` will be used.
            .. epigraph::

               This object isn't applicable to jobs that are running on Fargate resources.

            :param launch_template_id: The ID of the launch template.
            :param launch_template_name: The name of the launch template.
            :param overrides: A launch template to use in place of the default launch template. You must specify either the launch template ID or launch template name in the request, but not both. You can specify up to ten (10) launch template overrides that are associated to unique instance types or families for each compute environment. .. epigraph:: To unset all override templates for a compute environment, you can pass an empty array to the `UpdateComputeEnvironment.overrides <https://docs.aws.amazon.com/batch/latest/APIReference/API_UpdateComputeEnvironment.html>`_ parameter, or not include the ``overrides`` parameter when submitting the ``UpdateComputeEnvironment`` API operation.
            :param userdata_type: The EKS node initialization process to use. You only need to specify this value if you are using a custom AMI. The default value is ``EKS_BOOTSTRAP_SH`` . If *imageType* is a custom AMI based on EKS_AL2023 or EKS_AL2023_NVIDIA then you must choose ``EKS_NODEADM`` .
            :param version: The version number of the launch template, ``$Default`` , or ``$Latest`` . If the value is ``$Default`` , the default version of the launch template is used. If the value is ``$Latest`` , the latest version of the launch template is used. .. epigraph:: If the AMI ID that's used in a compute environment is from the launch template, the AMI isn't changed when the compute environment is updated. It's only changed if the ``updateToLatestImageVersion`` parameter for the compute environment is set to ``true`` . During an infrastructure update, if either ``$Default`` or ``$Latest`` is specified, AWS Batch re-evaluates the launch template version, and it might use a different version of the launch template. This is the case even if the launch template isn't specified in the update. When updating a compute environment, changing the launch template requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . Default: ``$Default`` Latest: ``$Latest``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                launch_template_specification_property = batch_mixins.CfnComputeEnvironmentPropsMixin.LaunchTemplateSpecificationProperty(
                    launch_template_id="launchTemplateId",
                    launch_template_name="launchTemplateName",
                    overrides=[batch_mixins.CfnComputeEnvironmentPropsMixin.LaunchTemplateSpecificationOverrideProperty(
                        launch_template_id="launchTemplateId",
                        launch_template_name="launchTemplateName",
                        target_instance_types=["targetInstanceTypes"],
                        userdata_type="userdataType",
                        version="version"
                    )],
                    userdata_type="userdataType",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b340d5a80f630c040ca1d13f63a7423fd51f51dde53cf391c5a002e89eb59b6b)
                check_type(argname="argument launch_template_id", value=launch_template_id, expected_type=type_hints["launch_template_id"])
                check_type(argname="argument launch_template_name", value=launch_template_name, expected_type=type_hints["launch_template_name"])
                check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
                check_type(argname="argument userdata_type", value=userdata_type, expected_type=type_hints["userdata_type"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if launch_template_id is not None:
                self._values["launch_template_id"] = launch_template_id
            if launch_template_name is not None:
                self._values["launch_template_name"] = launch_template_name
            if overrides is not None:
                self._values["overrides"] = overrides
            if userdata_type is not None:
                self._values["userdata_type"] = userdata_type
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def launch_template_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the launch template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html#cfn-batch-computeenvironment-launchtemplatespecification-launchtemplateid
            '''
            result = self._values.get("launch_template_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def launch_template_name(self) -> typing.Optional[builtins.str]:
            '''The name of the launch template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html#cfn-batch-computeenvironment-launchtemplatespecification-launchtemplatename
            '''
            result = self._values.get("launch_template_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def overrides(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeEnvironmentPropsMixin.LaunchTemplateSpecificationOverrideProperty"]]]]:
            '''A launch template to use in place of the default launch template.

            You must specify either the launch template ID or launch template name in the request, but not both.

            You can specify up to ten (10) launch template overrides that are associated to unique instance types or families for each compute environment.
            .. epigraph::

               To unset all override templates for a compute environment, you can pass an empty array to the `UpdateComputeEnvironment.overrides <https://docs.aws.amazon.com/batch/latest/APIReference/API_UpdateComputeEnvironment.html>`_ parameter, or not include the ``overrides`` parameter when submitting the ``UpdateComputeEnvironment`` API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html#cfn-batch-computeenvironment-launchtemplatespecification-overrides
            '''
            result = self._values.get("overrides")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeEnvironmentPropsMixin.LaunchTemplateSpecificationOverrideProperty"]]]], result)

        @builtins.property
        def userdata_type(self) -> typing.Optional[builtins.str]:
            '''The EKS node initialization process to use.

            You only need to specify this value if you are using a custom AMI. The default value is ``EKS_BOOTSTRAP_SH`` . If *imageType* is a custom AMI based on EKS_AL2023 or EKS_AL2023_NVIDIA then you must choose ``EKS_NODEADM`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html#cfn-batch-computeenvironment-launchtemplatespecification-userdatatype
            '''
            result = self._values.get("userdata_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The version number of the launch template, ``$Default`` , or ``$Latest`` .

            If the value is ``$Default`` , the default version of the launch template is used. If the value is ``$Latest`` , the latest version of the launch template is used.
            .. epigraph::

               If the AMI ID that's used in a compute environment is from the launch template, the AMI isn't changed when the compute environment is updated. It's only changed if the ``updateToLatestImageVersion`` parameter for the compute environment is set to ``true`` . During an infrastructure update, if either ``$Default`` or ``$Latest`` is specified, AWS Batch re-evaluates the launch template version, and it might use a different version of the launch template. This is the case even if the launch template isn't specified in the update. When updating a compute environment, changing the launch template requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .

            Default: ``$Default``

            Latest: ``$Latest``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html#cfn-batch-computeenvironment-launchtemplatespecification-version
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
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnComputeEnvironmentPropsMixin.UpdatePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "job_execution_timeout_minutes": "jobExecutionTimeoutMinutes",
            "terminate_jobs_on_update": "terminateJobsOnUpdate",
        },
    )
    class UpdatePolicyProperty:
        def __init__(
            self,
            *,
            job_execution_timeout_minutes: typing.Optional[jsii.Number] = None,
            terminate_jobs_on_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Specifies the infrastructure update policy for the Amazon EC2 compute environment.

            For more information about infrastructure updates, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .

            :param job_execution_timeout_minutes: Specifies the job timeout (in minutes) when the compute environment infrastructure is updated. The default value is 30. Default: - 30
            :param terminate_jobs_on_update: Specifies whether jobs are automatically terminated when the compute environment infrastructure is updated. The default value is ``false`` . Default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-updatepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                update_policy_property = batch_mixins.CfnComputeEnvironmentPropsMixin.UpdatePolicyProperty(
                    job_execution_timeout_minutes=123,
                    terminate_jobs_on_update=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c73efe81a7ee75c6cc3527b46b16e6b3dc00282503701ea44a66d7873535a434)
                check_type(argname="argument job_execution_timeout_minutes", value=job_execution_timeout_minutes, expected_type=type_hints["job_execution_timeout_minutes"])
                check_type(argname="argument terminate_jobs_on_update", value=terminate_jobs_on_update, expected_type=type_hints["terminate_jobs_on_update"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if job_execution_timeout_minutes is not None:
                self._values["job_execution_timeout_minutes"] = job_execution_timeout_minutes
            if terminate_jobs_on_update is not None:
                self._values["terminate_jobs_on_update"] = terminate_jobs_on_update

        @builtins.property
        def job_execution_timeout_minutes(self) -> typing.Optional[jsii.Number]:
            '''Specifies the job timeout (in minutes) when the compute environment infrastructure is updated.

            The default value is 30.

            :default: - 30

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-updatepolicy.html#cfn-batch-computeenvironment-updatepolicy-jobexecutiontimeoutminutes
            '''
            result = self._values.get("job_execution_timeout_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def terminate_jobs_on_update(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether jobs are automatically terminated when the compute environment infrastructure is updated.

            The default value is ``false`` .

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-updatepolicy.html#cfn-batch-computeenvironment-updatepolicy-terminatejobsonupdate
            '''
            result = self._values.get("terminate_jobs_on_update")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UpdatePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnConsumableResourceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "consumable_resource_name": "consumableResourceName",
        "resource_type": "resourceType",
        "tags": "tags",
        "total_quantity": "totalQuantity",
    },
)
class CfnConsumableResourceMixinProps:
    def __init__(
        self,
        *,
        consumable_resource_name: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        total_quantity: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnConsumableResourcePropsMixin.

        :param consumable_resource_name: The name of the consumable resource.
        :param resource_type: Indicates whether the resource is available to be re-used after a job completes. Can be one of:. - ``REPLENISHABLE`` - ``NON_REPLENISHABLE``
        :param tags: The tags that you apply to the consumable resource to help you categorize and organize your resources. Each tag consists of a key and an optional value. For more information, see `Tagging your AWS Batch resources <https://docs.aws.amazon.com/batch/latest/userguide/using-tags.html>`_ .
        :param total_quantity: The total amount of the consumable resource that is available.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-consumableresource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
            
            cfn_consumable_resource_mixin_props = batch_mixins.CfnConsumableResourceMixinProps(
                consumable_resource_name="consumableResourceName",
                resource_type="resourceType",
                tags={
                    "tags_key": "tags"
                },
                total_quantity=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21179910b253b4a582cb266d454cec991cd5e54fa3074696b95ca84774ca2d16)
            check_type(argname="argument consumable_resource_name", value=consumable_resource_name, expected_type=type_hints["consumable_resource_name"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument total_quantity", value=total_quantity, expected_type=type_hints["total_quantity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if consumable_resource_name is not None:
            self._values["consumable_resource_name"] = consumable_resource_name
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if tags is not None:
            self._values["tags"] = tags
        if total_quantity is not None:
            self._values["total_quantity"] = total_quantity

    @builtins.property
    def consumable_resource_name(self) -> typing.Optional[builtins.str]:
        '''The name of the consumable resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-consumableresource.html#cfn-batch-consumableresource-consumableresourcename
        '''
        result = self._values.get("consumable_resource_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''Indicates whether the resource is available to be re-used after a job completes. Can be one of:.

        - ``REPLENISHABLE``
        - ``NON_REPLENISHABLE``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-consumableresource.html#cfn-batch-consumableresource-resourcetype
        '''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags that you apply to the consumable resource to help you categorize and organize your resources.

        Each tag consists of a key and an optional value. For more information, see `Tagging your AWS Batch resources <https://docs.aws.amazon.com/batch/latest/userguide/using-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-consumableresource.html#cfn-batch-consumableresource-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def total_quantity(self) -> typing.Optional[jsii.Number]:
        '''The total amount of the consumable resource that is available.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-consumableresource.html#cfn-batch-consumableresource-totalquantity
        '''
        result = self._values.get("total_quantity")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConsumableResourceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConsumableResourcePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnConsumableResourcePropsMixin",
):
    '''The ``AWS::Batch::ConsumableResource`` resource specifies the parameters for an AWS Batch consumable resource.

    For more information, see `Resource-aware scheduling <https://docs.aws.amazon.com/batch/latest/userguide/resource-aware-scheduling.html>`_ in the ** .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-consumableresource.html
    :cloudformationResource: AWS::Batch::ConsumableResource
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
        
        cfn_consumable_resource_props_mixin = batch_mixins.CfnConsumableResourcePropsMixin(batch_mixins.CfnConsumableResourceMixinProps(
            consumable_resource_name="consumableResourceName",
            resource_type="resourceType",
            tags={
                "tags_key": "tags"
            },
            total_quantity=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnConsumableResourceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Batch::ConsumableResource``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b366079b0bc8b5d7d242a928465c0e3fbfcc5aec27504186b02cc5fc84b4a95d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5318b54fa86b435e3b22cfe586581f60aac0fbf439ded168ad9897198f88f4b3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f42a786dc8973a572c356eb280104e2c9e605f11685288a7dbd6152ce879bc2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConsumableResourceMixinProps:
        return typing.cast(CfnConsumableResourceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "consumable_resource_properties": "consumableResourceProperties",
        "container_properties": "containerProperties",
        "ecs_properties": "ecsProperties",
        "eks_properties": "eksProperties",
        "job_definition_name": "jobDefinitionName",
        "node_properties": "nodeProperties",
        "parameters": "parameters",
        "platform_capabilities": "platformCapabilities",
        "propagate_tags": "propagateTags",
        "resource_retention_policy": "resourceRetentionPolicy",
        "retry_strategy": "retryStrategy",
        "scheduling_priority": "schedulingPriority",
        "tags": "tags",
        "timeout": "timeout",
        "type": "type",
    },
)
class CfnJobDefinitionMixinProps:
    def __init__(
        self,
        *,
        consumable_resource_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.ConsumableResourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        container_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.ContainerPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ecs_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.EcsPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        eks_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.EksPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        job_definition_name: typing.Optional[builtins.str] = None,
        node_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.NodePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        parameters: typing.Any = None,
        platform_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        propagate_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        resource_retention_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.ResourceRetentionPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        retry_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.RetryStrategyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        scheduling_priority: typing.Optional[jsii.Number] = None,
        tags: typing.Any = None,
        timeout: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.TimeoutProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnJobDefinitionPropsMixin.

        :param consumable_resource_properties: Contains a list of consumable resources required by the job.
        :param container_properties: An object with properties specific to Amazon ECS-based jobs. When ``containerProperties`` is used in the job definition, it can't be used in addition to ``eksProperties`` , ``ecsProperties`` , or ``nodeProperties`` .
        :param ecs_properties: An object that contains the properties for the Amazon ECS resources of a job.When ``ecsProperties`` is used in the job definition, it can't be used in addition to ``containerProperties`` , ``eksProperties`` , or ``nodeProperties`` .
        :param eks_properties: An object with properties that are specific to Amazon EKS-based jobs. When ``eksProperties`` is used in the job definition, it can't be used in addition to ``containerProperties`` , ``ecsProperties`` , or ``nodeProperties`` .
        :param job_definition_name: The name of the job definition.
        :param node_properties: An object with properties that are specific to multi-node parallel jobs. When ``nodeProperties`` is used in the job definition, it can't be used in addition to ``containerProperties`` , ``ecsProperties`` , or ``eksProperties`` . .. epigraph:: If the job runs on Fargate resources, don't specify ``nodeProperties`` . Use ``containerProperties`` instead.
        :param parameters: Default parameters or parameter substitution placeholders that are set in the job definition. Parameters are specified as a key-value pair mapping. Parameters in a ``SubmitJob`` request override any corresponding parameter defaults from the job definition. For more information about specifying parameters, see `Job definition parameters <https://docs.aws.amazon.com/batch/latest/userguide/job_definition_parameters.html>`_ in the *AWS Batch User Guide* .
        :param platform_capabilities: The platform capabilities required by the job definition. If no value is specified, it defaults to ``EC2`` . Jobs run on Fargate resources specify ``FARGATE`` .
        :param propagate_tags: Specifies whether to propagate the tags from the job or job definition to the corresponding Amazon ECS task. If no value is specified, the tags aren't propagated. Tags can only be propagated to the tasks when the tasks are created. For tags with the same name, job tags are given priority over job definitions tags. If the total number of combined tags from the job and job definition is over 50, the job is moved to the ``FAILED`` state.
        :param resource_retention_policy: Specifies the resource retention policy settings for the job definition.
        :param retry_strategy: The retry strategy to use for failed jobs that are submitted with this job definition.
        :param scheduling_priority: The scheduling priority of the job definition. This only affects jobs in job queues with a fair-share policy. Jobs with a higher scheduling priority are scheduled before jobs with a lower scheduling priority.
        :param tags: The tags that are applied to the job definition.
        :param timeout: The timeout time for jobs that are submitted with this job definition. After the amount of time you specify passes, AWS Batch terminates your jobs if they aren't finished.
        :param type: The type of job definition. For more information about multi-node parallel jobs, see `Creating a multi-node parallel job definition <https://docs.aws.amazon.com/batch/latest/userguide/multi-node-job-def.html>`_ in the *AWS Batch User Guide* . - If the value is ``container`` , then one of the following is required: ``containerProperties`` , ``ecsProperties`` , or ``eksProperties`` . - If the value is ``multinode`` , then ``nodeProperties`` is required. .. epigraph:: If the job is run on Fargate resources, then ``multinode`` isn't supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8dbe65ec91d17ee6b06ec4341b531c757a3e0222e2e238001f2d50cba11d245)
            check_type(argname="argument consumable_resource_properties", value=consumable_resource_properties, expected_type=type_hints["consumable_resource_properties"])
            check_type(argname="argument container_properties", value=container_properties, expected_type=type_hints["container_properties"])
            check_type(argname="argument ecs_properties", value=ecs_properties, expected_type=type_hints["ecs_properties"])
            check_type(argname="argument eks_properties", value=eks_properties, expected_type=type_hints["eks_properties"])
            check_type(argname="argument job_definition_name", value=job_definition_name, expected_type=type_hints["job_definition_name"])
            check_type(argname="argument node_properties", value=node_properties, expected_type=type_hints["node_properties"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument platform_capabilities", value=platform_capabilities, expected_type=type_hints["platform_capabilities"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument resource_retention_policy", value=resource_retention_policy, expected_type=type_hints["resource_retention_policy"])
            check_type(argname="argument retry_strategy", value=retry_strategy, expected_type=type_hints["retry_strategy"])
            check_type(argname="argument scheduling_priority", value=scheduling_priority, expected_type=type_hints["scheduling_priority"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if consumable_resource_properties is not None:
            self._values["consumable_resource_properties"] = consumable_resource_properties
        if container_properties is not None:
            self._values["container_properties"] = container_properties
        if ecs_properties is not None:
            self._values["ecs_properties"] = ecs_properties
        if eks_properties is not None:
            self._values["eks_properties"] = eks_properties
        if job_definition_name is not None:
            self._values["job_definition_name"] = job_definition_name
        if node_properties is not None:
            self._values["node_properties"] = node_properties
        if parameters is not None:
            self._values["parameters"] = parameters
        if platform_capabilities is not None:
            self._values["platform_capabilities"] = platform_capabilities
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if resource_retention_policy is not None:
            self._values["resource_retention_policy"] = resource_retention_policy
        if retry_strategy is not None:
            self._values["retry_strategy"] = retry_strategy
        if scheduling_priority is not None:
            self._values["scheduling_priority"] = scheduling_priority
        if tags is not None:
            self._values["tags"] = tags
        if timeout is not None:
            self._values["timeout"] = timeout
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def consumable_resource_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.ConsumableResourcePropertiesProperty"]]:
        '''Contains a list of consumable resources required by the job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-consumableresourceproperties
        '''
        result = self._values.get("consumable_resource_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.ConsumableResourcePropertiesProperty"]], result)

    @builtins.property
    def container_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.ContainerPropertiesProperty"]]:
        '''An object with properties specific to Amazon ECS-based jobs.

        When ``containerProperties`` is used in the job definition, it can't be used in addition to ``eksProperties`` , ``ecsProperties`` , or ``nodeProperties`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-containerproperties
        '''
        result = self._values.get("container_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.ContainerPropertiesProperty"]], result)

    @builtins.property
    def ecs_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EcsPropertiesProperty"]]:
        '''An object that contains the properties for the Amazon ECS resources of a job.When ``ecsProperties`` is used in the job definition, it can't be used in addition to ``containerProperties`` , ``eksProperties`` , or ``nodeProperties`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-ecsproperties
        '''
        result = self._values.get("ecs_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EcsPropertiesProperty"]], result)

    @builtins.property
    def eks_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EksPropertiesProperty"]]:
        '''An object with properties that are specific to Amazon EKS-based jobs.

        When ``eksProperties`` is used in the job definition, it can't be used in addition to ``containerProperties`` , ``ecsProperties`` , or ``nodeProperties`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-eksproperties
        '''
        result = self._values.get("eks_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EksPropertiesProperty"]], result)

    @builtins.property
    def job_definition_name(self) -> typing.Optional[builtins.str]:
        '''The name of the job definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-jobdefinitionname
        '''
        result = self._values.get("job_definition_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.NodePropertiesProperty"]]:
        '''An object with properties that are specific to multi-node parallel jobs.

        When ``nodeProperties`` is used in the job definition, it can't be used in addition to ``containerProperties`` , ``ecsProperties`` , or ``eksProperties`` .
        .. epigraph::

           If the job runs on Fargate resources, don't specify ``nodeProperties`` . Use ``containerProperties`` instead.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-nodeproperties
        '''
        result = self._values.get("node_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.NodePropertiesProperty"]], result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''Default parameters or parameter substitution placeholders that are set in the job definition.

        Parameters are specified as a key-value pair mapping. Parameters in a ``SubmitJob`` request override any corresponding parameter defaults from the job definition. For more information about specifying parameters, see `Job definition parameters <https://docs.aws.amazon.com/batch/latest/userguide/job_definition_parameters.html>`_ in the *AWS Batch User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    @builtins.property
    def platform_capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The platform capabilities required by the job definition.

        If no value is specified, it defaults to ``EC2`` . Jobs run on Fargate resources specify ``FARGATE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-platformcapabilities
        '''
        result = self._values.get("platform_capabilities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def propagate_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to propagate the tags from the job or job definition to the corresponding Amazon ECS task.

        If no value is specified, the tags aren't propagated. Tags can only be propagated to the tasks when the tasks are created. For tags with the same name, job tags are given priority over job definitions tags. If the total number of combined tags from the job and job definition is over 50, the job is moved to the ``FAILED`` state.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-propagatetags
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def resource_retention_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.ResourceRetentionPolicyProperty"]]:
        '''Specifies the resource retention policy settings for the job definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-resourceretentionpolicy
        '''
        result = self._values.get("resource_retention_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.ResourceRetentionPolicyProperty"]], result)

    @builtins.property
    def retry_strategy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.RetryStrategyProperty"]]:
        '''The retry strategy to use for failed jobs that are submitted with this job definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-retrystrategy
        '''
        result = self._values.get("retry_strategy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.RetryStrategyProperty"]], result)

    @builtins.property
    def scheduling_priority(self) -> typing.Optional[jsii.Number]:
        '''The scheduling priority of the job definition.

        This only affects jobs in job queues with a fair-share policy. Jobs with a higher scheduling priority are scheduled before jobs with a lower scheduling priority.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-schedulingpriority
        '''
        result = self._values.get("scheduling_priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''The tags that are applied to the job definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def timeout(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.TimeoutProperty"]]:
        '''The timeout time for jobs that are submitted with this job definition.

        After the amount of time you specify passes, AWS Batch terminates your jobs if they aren't finished.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-timeout
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.TimeoutProperty"]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of job definition.

        For more information about multi-node parallel jobs, see `Creating a multi-node parallel job definition <https://docs.aws.amazon.com/batch/latest/userguide/multi-node-job-def.html>`_ in the *AWS Batch User Guide* .

        - If the value is ``container`` , then one of the following is required: ``containerProperties`` , ``ecsProperties`` , or ``eksProperties`` .
        - If the value is ``multinode`` , then ``nodeProperties`` is required.

        .. epigraph::

           If the job is run on Fargate resources, then ``multinode`` isn't supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnJobDefinitionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnJobDefinitionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin",
):
    '''The ``AWS::Batch::JobDefinition`` resource specifies the parameters for an AWS Batch job definition.

    For more information, see `Job Definitions <https://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html>`_ in the ** .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html
    :cloudformationResource: AWS::Batch::JobDefinition
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        
    '''

    def __init__(
        self,
        props: typing.Union[CfnJobDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Batch::JobDefinition``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b87abfbcd1852552990b06a57c912fd73ccc3116bbd9eef194078801f24666bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8337b26b1f946e02bd1a11c59396c3d67594216d66b0b2f807fddad35dd940b4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d2d34aca74bf95fffa06e556b45bc8f4fb593d8537ed3505bd29f9f95ad120e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnJobDefinitionMixinProps:
        return typing.cast(CfnJobDefinitionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.AuthorizationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"access_point_id": "accessPointId", "iam": "iam"},
    )
    class AuthorizationConfigProperty:
        def __init__(
            self,
            *,
            access_point_id: typing.Optional[builtins.str] = None,
            iam: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param access_point_id: 
            :param iam: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-authorizationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                authorization_config_property = batch_mixins.CfnJobDefinitionPropsMixin.AuthorizationConfigProperty(
                    access_point_id="accessPointId",
                    iam="iam"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c808feda9afa8f364208a37522654fc65160163e1ece1ac2e2b8c07b10aa4452)
                check_type(argname="argument access_point_id", value=access_point_id, expected_type=type_hints["access_point_id"])
                check_type(argname="argument iam", value=iam, expected_type=type_hints["iam"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_point_id is not None:
                self._values["access_point_id"] = access_point_id
            if iam is not None:
                self._values["iam"] = iam

        @builtins.property
        def access_point_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-authorizationconfig.html#cfn-batch-jobdefinition-authorizationconfig-accesspointid
            '''
            result = self._values.get("access_point_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def iam(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-authorizationconfig.html#cfn-batch-jobdefinition-authorizationconfig-iam
            '''
            result = self._values.get("iam")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthorizationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.ConsumableResourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"consumable_resource_list": "consumableResourceList"},
    )
    class ConsumableResourcePropertiesProperty:
        def __init__(
            self,
            *,
            consumable_resource_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.ConsumableResourceRequirementProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains a list of consumable resources required by a job.

            :param consumable_resource_list: The list of consumable resources required by a job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-consumableresourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                consumable_resource_properties_property = batch_mixins.CfnJobDefinitionPropsMixin.ConsumableResourcePropertiesProperty(
                    consumable_resource_list=[batch_mixins.CfnJobDefinitionPropsMixin.ConsumableResourceRequirementProperty(
                        consumable_resource="consumableResource",
                        quantity=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__188f31c82213bad51eaa19f67e62c4062b1dac049edcce7e4b8583e28248c6f2)
                check_type(argname="argument consumable_resource_list", value=consumable_resource_list, expected_type=type_hints["consumable_resource_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if consumable_resource_list is not None:
                self._values["consumable_resource_list"] = consumable_resource_list

        @builtins.property
        def consumable_resource_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.ConsumableResourceRequirementProperty"]]]]:
            '''The list of consumable resources required by a job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-consumableresourceproperties.html#cfn-batch-jobdefinition-consumableresourceproperties-consumableresourcelist
            '''
            result = self._values.get("consumable_resource_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.ConsumableResourceRequirementProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConsumableResourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.ConsumableResourceRequirementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "consumable_resource": "consumableResource",
            "quantity": "quantity",
        },
    )
    class ConsumableResourceRequirementProperty:
        def __init__(
            self,
            *,
            consumable_resource: typing.Optional[builtins.str] = None,
            quantity: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about a consumable resource required to run a job.

            :param consumable_resource: The name or ARN of the consumable resource.
            :param quantity: The quantity of the consumable resource that is needed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-consumableresourcerequirement.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                consumable_resource_requirement_property = batch_mixins.CfnJobDefinitionPropsMixin.ConsumableResourceRequirementProperty(
                    consumable_resource="consumableResource",
                    quantity=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2283572e826c7e3cced44564e73ffffb3021d9e0011f613f5def44ca8fcb3587)
                check_type(argname="argument consumable_resource", value=consumable_resource, expected_type=type_hints["consumable_resource"])
                check_type(argname="argument quantity", value=quantity, expected_type=type_hints["quantity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if consumable_resource is not None:
                self._values["consumable_resource"] = consumable_resource
            if quantity is not None:
                self._values["quantity"] = quantity

        @builtins.property
        def consumable_resource(self) -> typing.Optional[builtins.str]:
            '''The name or ARN of the consumable resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-consumableresourcerequirement.html#cfn-batch-jobdefinition-consumableresourcerequirement-consumableresource
            '''
            result = self._values.get("consumable_resource")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def quantity(self) -> typing.Optional[jsii.Number]:
            '''The quantity of the consumable resource that is needed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-consumableresourcerequirement.html#cfn-batch-jobdefinition-consumableresourcerequirement-quantity
            '''
            result = self._values.get("quantity")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConsumableResourceRequirementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.ContainerPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "command": "command",
            "enable_execute_command": "enableExecuteCommand",
            "environment": "environment",
            "ephemeral_storage": "ephemeralStorage",
            "execution_role_arn": "executionRoleArn",
            "fargate_platform_configuration": "fargatePlatformConfiguration",
            "image": "image",
            "instance_type": "instanceType",
            "job_role_arn": "jobRoleArn",
            "linux_parameters": "linuxParameters",
            "log_configuration": "logConfiguration",
            "memory": "memory",
            "mount_points": "mountPoints",
            "network_configuration": "networkConfiguration",
            "privileged": "privileged",
            "readonly_root_filesystem": "readonlyRootFilesystem",
            "repository_credentials": "repositoryCredentials",
            "resource_requirements": "resourceRequirements",
            "runtime_platform": "runtimePlatform",
            "secrets": "secrets",
            "ulimits": "ulimits",
            "user": "user",
            "vcpus": "vcpus",
            "volumes": "volumes",
        },
    )
    class ContainerPropertiesProperty:
        def __init__(
            self,
            *,
            command: typing.Optional[typing.Sequence[builtins.str]] = None,
            enable_execute_command: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.EnvironmentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ephemeral_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.EphemeralStorageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            execution_role_arn: typing.Optional[builtins.str] = None,
            fargate_platform_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.FargatePlatformConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            image: typing.Optional[builtins.str] = None,
            instance_type: typing.Optional[builtins.str] = None,
            job_role_arn: typing.Optional[builtins.str] = None,
            linux_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.LinuxParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            log_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.LogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            memory: typing.Optional[jsii.Number] = None,
            mount_points: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.MountPointsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.NetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            privileged: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            readonly_root_filesystem: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            repository_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.RepositoryCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resource_requirements: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.ResourceRequirementProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            runtime_platform: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.RuntimePlatformProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secrets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.SecretProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ulimits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.UlimitProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            user: typing.Optional[builtins.str] = None,
            vcpus: typing.Optional[jsii.Number] = None,
            volumes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.VolumesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Container properties are used for Amazon ECS based job definitions.

            These properties to describe the container that's launched as part of a job.

            :param command: The command that's passed to the container. This parameter maps to ``Cmd`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``COMMAND`` parameter to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . For more information, see `https://docs.docker.com/engine/reference/builder/#cmd <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/builder/#cmd>`_ .
            :param enable_execute_command: Determines whether execute command functionality is turned on for this task. If ``true`` , execute command functionality is turned on all the containers in the task.
            :param environment: The environment variables to pass to a container. This parameter maps to ``Env`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--env`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . .. epigraph:: We don't recommend using plaintext environment variables for sensitive information, such as credential data. > Environment variables cannot start with " ``AWS_BATCH`` ". This naming convention is reserved for variables that AWS Batch sets.
            :param ephemeral_storage: The amount of ephemeral storage to allocate for the task. This parameter is used to expand the total amount of ephemeral storage available, beyond the default amount, for tasks hosted on AWS Fargate .
            :param execution_role_arn: The Amazon Resource Name (ARN) of the execution role that AWS Batch can assume. For jobs that run on Fargate resources, you must provide an execution role. For more information, see `AWS Batch execution IAM role <https://docs.aws.amazon.com/batch/latest/userguide/execution-IAM-role.html>`_ in the *AWS Batch User Guide* .
            :param fargate_platform_configuration: The platform configuration for jobs that are running on Fargate resources. Jobs that are running on Amazon EC2 resources must not specify this parameter.
            :param image: Required. The image used to start a container. This string is passed directly to the Docker daemon. Images in the Docker Hub registry are available by default. Other repositories are specified with ``*repository-url* / *image* : *tag*`` . It can be 255 characters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), underscores (_), colons (:), periods (.), forward slashes (/), and number signs (#). This parameter maps to ``Image`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``IMAGE`` parameter of `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . .. epigraph:: Docker image architecture must match the processor architecture of the compute resources that they're scheduled on. For example, ARM-based Docker images can only run on ARM-based compute resources. - Images in Amazon ECR Public repositories use the full ``registry/repository[:tag]`` or ``registry/repository[@digest]`` naming conventions. For example, ``public.ecr.aws/ *registry_alias* / *my-web-app* : *latest*`` . - Images in Amazon ECR repositories use the full registry and repository URI (for example, ``123456789012.dkr.ecr.<region-name>.amazonaws.com/<repository-name>`` ). - Images in official repositories on Docker Hub use a single name (for example, ``ubuntu`` or ``mongo`` ). - Images in other repositories on Docker Hub are qualified with an organization name (for example, ``amazon/amazon-ecs-agent`` ). - Images in other online repositories are qualified further by a domain name (for example, ``quay.io/assemblyline/ubuntu`` ).
            :param instance_type: 
            :param job_role_arn: The Amazon Resource Name (ARN) of the IAM role that the container can assume for AWS permissions. For more information, see `IAM roles for tasks <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html>`_ in the *Amazon Elastic Container Service Developer Guide* .
            :param linux_parameters: Linux-specific modifications that are applied to the container, such as details for device mappings.
            :param log_configuration: The log configuration specification for the container. This parameter maps to ``LogConfig`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--log-driver`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . By default, containers use the same logging driver that the Docker daemon uses. However the container might use a different logging driver than the Docker daemon by specifying a log driver with this parameter in the container definition. To use a different logging driver for a container, the log system must be configured properly on the container instance (or on a different log server for remote logging options). For more information on the options for different supported log drivers, see `Configure logging drivers <https://docs.aws.amazon.com/https://docs.docker.com/engine/admin/logging/overview/>`_ in the Docker documentation. .. epigraph:: AWS Batch currently supports a subset of the logging drivers available to the Docker daemon (shown in the `LogConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-logconfiguration.html>`_ data type). This parameter requires version 1.18 of the Docker Remote API or greater on your container instance. To check the Docker Remote API version on your container instance, log in to your container instance and run the following command: ``sudo docker version | grep "Server API version"`` .. epigraph:: The Amazon ECS container agent running on a container instance must register the logging drivers available on that instance with the ``ECS_AVAILABLE_LOGGING_DRIVERS`` environment variable before containers placed on that instance can use these log configuration options. For more information, see `Amazon ECS container agent configuration <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-config.html>`_ in the *Amazon Elastic Container Service Developer Guide* .
            :param memory: This parameter is deprecated, use ``resourceRequirements`` to specify the memory requirements for the job definition. It's not supported for jobs running on Fargate resources. For jobs that run on Amazon EC2 resources, it specifies the memory hard limit (in MiB) for a container. If your container attempts to exceed the specified number, it's terminated. You must specify at least 4 MiB of memory for a job using this parameter. The memory hard limit can be specified in several places. It must be specified for each node at least once.
            :param mount_points: The mount points for data volumes in your container. This parameter maps to ``Volumes`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--volume`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .
            :param network_configuration: The network configuration for jobs that are running on Fargate resources. Jobs that are running on Amazon EC2 resources must not specify this parameter.
            :param privileged: When this parameter is true, the container is given elevated permissions on the host container instance (similar to the ``root`` user). This parameter maps to ``Privileged`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--privileged`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . The default value is false. .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources and shouldn't be provided, or specified as false.
            :param readonly_root_filesystem: When this parameter is true, the container is given read-only access to its root file system. This parameter maps to ``ReadonlyRootfs`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--read-only`` option to ``docker run`` .
            :param repository_credentials: The private repository authentication credentials to use.
            :param resource_requirements: The type and amount of resources to assign to a container. The supported resources include ``GPU`` , ``MEMORY`` , and ``VCPU`` .
            :param runtime_platform: An object that represents the compute environment architecture for AWS Batch jobs on Fargate.
            :param secrets: The secrets for the container. For more information, see `Specifying sensitive data <https://docs.aws.amazon.com/batch/latest/userguide/specifying-sensitive-data.html>`_ in the *AWS Batch User Guide* .
            :param ulimits: A list of ``ulimits`` to set in the container. This parameter maps to ``Ulimits`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--ulimit`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources and shouldn't be provided.
            :param user: The user name to use inside the container. This parameter maps to ``User`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--user`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .
            :param vcpus: This parameter is deprecated, use ``resourceRequirements`` to specify the vCPU requirements for the job definition. It's not supported for jobs running on Fargate resources. For jobs running on Amazon EC2 resources, it specifies the number of vCPUs reserved for the job. Each vCPU is equivalent to 1,024 CPU shares. This parameter maps to ``CpuShares`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--cpu-shares`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . The number of vCPUs must be specified but can be specified in several places. You must specify it at least once for each node.
            :param volumes: A list of data volumes used in a job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                # options: Any
                
                container_properties_property = batch_mixins.CfnJobDefinitionPropsMixin.ContainerPropertiesProperty(
                    command=["command"],
                    enable_execute_command=False,
                    environment=[batch_mixins.CfnJobDefinitionPropsMixin.EnvironmentProperty(
                        name="name",
                        value="value"
                    )],
                    ephemeral_storage=batch_mixins.CfnJobDefinitionPropsMixin.EphemeralStorageProperty(
                        size_in_gi_b=123
                    ),
                    execution_role_arn="executionRoleArn",
                    fargate_platform_configuration=batch_mixins.CfnJobDefinitionPropsMixin.FargatePlatformConfigurationProperty(
                        platform_version="platformVersion"
                    ),
                    image="image",
                    instance_type="instanceType",
                    job_role_arn="jobRoleArn",
                    linux_parameters=batch_mixins.CfnJobDefinitionPropsMixin.LinuxParametersProperty(
                        devices=[batch_mixins.CfnJobDefinitionPropsMixin.DeviceProperty(
                            container_path="containerPath",
                            host_path="hostPath",
                            permissions=["permissions"]
                        )],
                        init_process_enabled=False,
                        max_swap=123,
                        shared_memory_size=123,
                        swappiness=123,
                        tmpfs=[batch_mixins.CfnJobDefinitionPropsMixin.TmpfsProperty(
                            container_path="containerPath",
                            mount_options=["mountOptions"],
                            size=123
                        )]
                    ),
                    log_configuration=batch_mixins.CfnJobDefinitionPropsMixin.LogConfigurationProperty(
                        log_driver="logDriver",
                        options=options,
                        secret_options=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                            name="name",
                            value_from="valueFrom"
                        )]
                    ),
                    memory=123,
                    mount_points=[batch_mixins.CfnJobDefinitionPropsMixin.MountPointsProperty(
                        container_path="containerPath",
                        read_only=False,
                        source_volume="sourceVolume"
                    )],
                    network_configuration=batch_mixins.CfnJobDefinitionPropsMixin.NetworkConfigurationProperty(
                        assign_public_ip="assignPublicIp"
                    ),
                    privileged=False,
                    readonly_root_filesystem=False,
                    repository_credentials=batch_mixins.CfnJobDefinitionPropsMixin.RepositoryCredentialsProperty(
                        credentials_parameter="credentialsParameter"
                    ),
                    resource_requirements=[batch_mixins.CfnJobDefinitionPropsMixin.ResourceRequirementProperty(
                        type="type",
                        value="value"
                    )],
                    runtime_platform=batch_mixins.CfnJobDefinitionPropsMixin.RuntimePlatformProperty(
                        cpu_architecture="cpuArchitecture",
                        operating_system_family="operatingSystemFamily"
                    ),
                    secrets=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                        name="name",
                        value_from="valueFrom"
                    )],
                    ulimits=[batch_mixins.CfnJobDefinitionPropsMixin.UlimitProperty(
                        hard_limit=123,
                        name="name",
                        soft_limit=123
                    )],
                    user="user",
                    vcpus=123,
                    volumes=[batch_mixins.CfnJobDefinitionPropsMixin.VolumesProperty(
                        efs_volume_configuration=batch_mixins.CfnJobDefinitionPropsMixin.EfsVolumeConfigurationProperty(
                            authorization_config=batch_mixins.CfnJobDefinitionPropsMixin.AuthorizationConfigProperty(
                                access_point_id="accessPointId",
                                iam="iam"
                            ),
                            file_system_id="fileSystemId",
                            root_directory="rootDirectory",
                            transit_encryption="transitEncryption",
                            transit_encryption_port=123
                        ),
                        host=batch_mixins.CfnJobDefinitionPropsMixin.VolumesHostProperty(
                            source_path="sourcePath"
                        ),
                        name="name"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8123c7a975d95658fed794d63213d173f02b341be6ac3999556de746e2f06899)
                check_type(argname="argument command", value=command, expected_type=type_hints["command"])
                check_type(argname="argument enable_execute_command", value=enable_execute_command, expected_type=type_hints["enable_execute_command"])
                check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
                check_type(argname="argument ephemeral_storage", value=ephemeral_storage, expected_type=type_hints["ephemeral_storage"])
                check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
                check_type(argname="argument fargate_platform_configuration", value=fargate_platform_configuration, expected_type=type_hints["fargate_platform_configuration"])
                check_type(argname="argument image", value=image, expected_type=type_hints["image"])
                check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                check_type(argname="argument job_role_arn", value=job_role_arn, expected_type=type_hints["job_role_arn"])
                check_type(argname="argument linux_parameters", value=linux_parameters, expected_type=type_hints["linux_parameters"])
                check_type(argname="argument log_configuration", value=log_configuration, expected_type=type_hints["log_configuration"])
                check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
                check_type(argname="argument mount_points", value=mount_points, expected_type=type_hints["mount_points"])
                check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
                check_type(argname="argument privileged", value=privileged, expected_type=type_hints["privileged"])
                check_type(argname="argument readonly_root_filesystem", value=readonly_root_filesystem, expected_type=type_hints["readonly_root_filesystem"])
                check_type(argname="argument repository_credentials", value=repository_credentials, expected_type=type_hints["repository_credentials"])
                check_type(argname="argument resource_requirements", value=resource_requirements, expected_type=type_hints["resource_requirements"])
                check_type(argname="argument runtime_platform", value=runtime_platform, expected_type=type_hints["runtime_platform"])
                check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
                check_type(argname="argument ulimits", value=ulimits, expected_type=type_hints["ulimits"])
                check_type(argname="argument user", value=user, expected_type=type_hints["user"])
                check_type(argname="argument vcpus", value=vcpus, expected_type=type_hints["vcpus"])
                check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if command is not None:
                self._values["command"] = command
            if enable_execute_command is not None:
                self._values["enable_execute_command"] = enable_execute_command
            if environment is not None:
                self._values["environment"] = environment
            if ephemeral_storage is not None:
                self._values["ephemeral_storage"] = ephemeral_storage
            if execution_role_arn is not None:
                self._values["execution_role_arn"] = execution_role_arn
            if fargate_platform_configuration is not None:
                self._values["fargate_platform_configuration"] = fargate_platform_configuration
            if image is not None:
                self._values["image"] = image
            if instance_type is not None:
                self._values["instance_type"] = instance_type
            if job_role_arn is not None:
                self._values["job_role_arn"] = job_role_arn
            if linux_parameters is not None:
                self._values["linux_parameters"] = linux_parameters
            if log_configuration is not None:
                self._values["log_configuration"] = log_configuration
            if memory is not None:
                self._values["memory"] = memory
            if mount_points is not None:
                self._values["mount_points"] = mount_points
            if network_configuration is not None:
                self._values["network_configuration"] = network_configuration
            if privileged is not None:
                self._values["privileged"] = privileged
            if readonly_root_filesystem is not None:
                self._values["readonly_root_filesystem"] = readonly_root_filesystem
            if repository_credentials is not None:
                self._values["repository_credentials"] = repository_credentials
            if resource_requirements is not None:
                self._values["resource_requirements"] = resource_requirements
            if runtime_platform is not None:
                self._values["runtime_platform"] = runtime_platform
            if secrets is not None:
                self._values["secrets"] = secrets
            if ulimits is not None:
                self._values["ulimits"] = ulimits
            if user is not None:
                self._values["user"] = user
            if vcpus is not None:
                self._values["vcpus"] = vcpus
            if volumes is not None:
                self._values["volumes"] = volumes

        @builtins.property
        def command(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The command that's passed to the container.

            This parameter maps to ``Cmd`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``COMMAND`` parameter to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . For more information, see `https://docs.docker.com/engine/reference/builder/#cmd <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/builder/#cmd>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-command
            '''
            result = self._values.get("command")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def enable_execute_command(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether execute command functionality is turned on for this task.

            If ``true`` , execute command functionality is turned on all the containers in the task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-enableexecutecommand
            '''
            result = self._values.get("enable_execute_command")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def environment(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EnvironmentProperty"]]]]:
            '''The environment variables to pass to a container.

            This parameter maps to ``Env`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--env`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .
            .. epigraph::

               We don't recommend using plaintext environment variables for sensitive information, such as credential data. > Environment variables cannot start with " ``AWS_BATCH`` ". This naming convention is reserved for variables that AWS Batch sets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-environment
            '''
            result = self._values.get("environment")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EnvironmentProperty"]]]], result)

        @builtins.property
        def ephemeral_storage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EphemeralStorageProperty"]]:
            '''The amount of ephemeral storage to allocate for the task.

            This parameter is used to expand the total amount of ephemeral storage available, beyond the default amount, for tasks hosted on AWS Fargate .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-ephemeralstorage
            '''
            result = self._values.get("ephemeral_storage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EphemeralStorageProperty"]], result)

        @builtins.property
        def execution_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the execution role that AWS Batch can assume.

            For jobs that run on Fargate resources, you must provide an execution role. For more information, see `AWS Batch execution IAM role <https://docs.aws.amazon.com/batch/latest/userguide/execution-IAM-role.html>`_ in the *AWS Batch User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-executionrolearn
            '''
            result = self._values.get("execution_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def fargate_platform_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.FargatePlatformConfigurationProperty"]]:
            '''The platform configuration for jobs that are running on Fargate resources.

            Jobs that are running on Amazon EC2 resources must not specify this parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-fargateplatformconfiguration
            '''
            result = self._values.get("fargate_platform_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.FargatePlatformConfigurationProperty"]], result)

        @builtins.property
        def image(self) -> typing.Optional[builtins.str]:
            '''Required.

            The image used to start a container. This string is passed directly to the Docker daemon. Images in the Docker Hub registry are available by default. Other repositories are specified with ``*repository-url* / *image* : *tag*`` . It can be 255 characters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), underscores (_), colons (:), periods (.), forward slashes (/), and number signs (#). This parameter maps to ``Image`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``IMAGE`` parameter of `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .
            .. epigraph::

               Docker image architecture must match the processor architecture of the compute resources that they're scheduled on. For example, ARM-based Docker images can only run on ARM-based compute resources.

            - Images in Amazon ECR Public repositories use the full ``registry/repository[:tag]`` or ``registry/repository[@digest]`` naming conventions. For example, ``public.ecr.aws/ *registry_alias* / *my-web-app* : *latest*`` .
            - Images in Amazon ECR repositories use the full registry and repository URI (for example, ``123456789012.dkr.ecr.<region-name>.amazonaws.com/<repository-name>`` ).
            - Images in official repositories on Docker Hub use a single name (for example, ``ubuntu`` or ``mongo`` ).
            - Images in other repositories on Docker Hub are qualified with an organization name (for example, ``amazon/amazon-ecs-agent`` ).
            - Images in other online repositories are qualified further by a domain name (for example, ``quay.io/assemblyline/ubuntu`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-image
            '''
            result = self._values.get("image")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-instancetype
            '''
            result = self._values.get("instance_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def job_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role that the container can assume for AWS permissions.

            For more information, see `IAM roles for tasks <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-jobrolearn
            '''
            result = self._values.get("job_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def linux_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.LinuxParametersProperty"]]:
            '''Linux-specific modifications that are applied to the container, such as details for device mappings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-linuxparameters
            '''
            result = self._values.get("linux_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.LinuxParametersProperty"]], result)

        @builtins.property
        def log_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.LogConfigurationProperty"]]:
            '''The log configuration specification for the container.

            This parameter maps to ``LogConfig`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--log-driver`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . By default, containers use the same logging driver that the Docker daemon uses. However the container might use a different logging driver than the Docker daemon by specifying a log driver with this parameter in the container definition. To use a different logging driver for a container, the log system must be configured properly on the container instance (or on a different log server for remote logging options). For more information on the options for different supported log drivers, see `Configure logging drivers <https://docs.aws.amazon.com/https://docs.docker.com/engine/admin/logging/overview/>`_ in the Docker documentation.
            .. epigraph::

               AWS Batch currently supports a subset of the logging drivers available to the Docker daemon (shown in the `LogConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-logconfiguration.html>`_ data type).

            This parameter requires version 1.18 of the Docker Remote API or greater on your container instance. To check the Docker Remote API version on your container instance, log in to your container instance and run the following command: ``sudo docker version | grep "Server API version"``
            .. epigraph::

               The Amazon ECS container agent running on a container instance must register the logging drivers available on that instance with the ``ECS_AVAILABLE_LOGGING_DRIVERS`` environment variable before containers placed on that instance can use these log configuration options. For more information, see `Amazon ECS container agent configuration <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-config.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-logconfiguration
            '''
            result = self._values.get("log_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.LogConfigurationProperty"]], result)

        @builtins.property
        def memory(self) -> typing.Optional[jsii.Number]:
            '''This parameter is deprecated, use ``resourceRequirements`` to specify the memory requirements for the job definition.

            It's not supported for jobs running on Fargate resources. For jobs that run on Amazon EC2 resources, it specifies the memory hard limit (in MiB) for a container. If your container attempts to exceed the specified number, it's terminated. You must specify at least 4 MiB of memory for a job using this parameter. The memory hard limit can be specified in several places. It must be specified for each node at least once.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-memory
            '''
            result = self._values.get("memory")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def mount_points(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.MountPointsProperty"]]]]:
            '''The mount points for data volumes in your container.

            This parameter maps to ``Volumes`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--volume`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-mountpoints
            '''
            result = self._values.get("mount_points")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.MountPointsProperty"]]]], result)

        @builtins.property
        def network_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.NetworkConfigurationProperty"]]:
            '''The network configuration for jobs that are running on Fargate resources.

            Jobs that are running on Amazon EC2 resources must not specify this parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-networkconfiguration
            '''
            result = self._values.get("network_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.NetworkConfigurationProperty"]], result)

        @builtins.property
        def privileged(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When this parameter is true, the container is given elevated permissions on the host container instance (similar to the ``root`` user).

            This parameter maps to ``Privileged`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--privileged`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . The default value is false.
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources and shouldn't be provided, or specified as false.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-privileged
            '''
            result = self._values.get("privileged")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def readonly_root_filesystem(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When this parameter is true, the container is given read-only access to its root file system.

            This parameter maps to ``ReadonlyRootfs`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--read-only`` option to ``docker run`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-readonlyrootfilesystem
            '''
            result = self._values.get("readonly_root_filesystem")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def repository_credentials(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.RepositoryCredentialsProperty"]]:
            '''The private repository authentication credentials to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-repositorycredentials
            '''
            result = self._values.get("repository_credentials")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.RepositoryCredentialsProperty"]], result)

        @builtins.property
        def resource_requirements(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.ResourceRequirementProperty"]]]]:
            '''The type and amount of resources to assign to a container.

            The supported resources include ``GPU`` , ``MEMORY`` , and ``VCPU`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-resourcerequirements
            '''
            result = self._values.get("resource_requirements")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.ResourceRequirementProperty"]]]], result)

        @builtins.property
        def runtime_platform(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.RuntimePlatformProperty"]]:
            '''An object that represents the compute environment architecture for AWS Batch jobs on Fargate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-runtimeplatform
            '''
            result = self._values.get("runtime_platform")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.RuntimePlatformProperty"]], result)

        @builtins.property
        def secrets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.SecretProperty"]]]]:
            '''The secrets for the container.

            For more information, see `Specifying sensitive data <https://docs.aws.amazon.com/batch/latest/userguide/specifying-sensitive-data.html>`_ in the *AWS Batch User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-secrets
            '''
            result = self._values.get("secrets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.SecretProperty"]]]], result)

        @builtins.property
        def ulimits(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.UlimitProperty"]]]]:
            '''A list of ``ulimits`` to set in the container.

            This parameter maps to ``Ulimits`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--ulimit`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources and shouldn't be provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-ulimits
            '''
            result = self._values.get("ulimits")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.UlimitProperty"]]]], result)

        @builtins.property
        def user(self) -> typing.Optional[builtins.str]:
            '''The user name to use inside the container.

            This parameter maps to ``User`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--user`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-user
            '''
            result = self._values.get("user")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vcpus(self) -> typing.Optional[jsii.Number]:
            '''This parameter is deprecated, use ``resourceRequirements`` to specify the vCPU requirements for the job definition.

            It's not supported for jobs running on Fargate resources. For jobs running on Amazon EC2 resources, it specifies the number of vCPUs reserved for the job.

            Each vCPU is equivalent to 1,024 CPU shares. This parameter maps to ``CpuShares`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--cpu-shares`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . The number of vCPUs must be specified but can be specified in several places. You must specify it at least once for each node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-vcpus
            '''
            result = self._values.get("vcpus")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volumes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.VolumesProperty"]]]]:
            '''A list of data volumes used in a job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-volumes
            '''
            result = self._values.get("volumes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.VolumesProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContainerPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.DeviceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "container_path": "containerPath",
            "host_path": "hostPath",
            "permissions": "permissions",
        },
    )
    class DeviceProperty:
        def __init__(
            self,
            *,
            container_path: typing.Optional[builtins.str] = None,
            host_path: typing.Optional[builtins.str] = None,
            permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''An object that represents a container instance host device.

            .. epigraph::

               This object isn't applicable to jobs that are running on Fargate resources and shouldn't be provided.

            :param container_path: The path inside the container that's used to expose the host device. By default, the ``hostPath`` value is used.
            :param host_path: The path for the device on the host container instance.
            :param permissions: The explicit permissions to provide to the container for the device. By default, the container has permissions for ``read`` , ``write`` , and ``mknod`` for the device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-device.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                device_property = batch_mixins.CfnJobDefinitionPropsMixin.DeviceProperty(
                    container_path="containerPath",
                    host_path="hostPath",
                    permissions=["permissions"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db5d2d62863fa365abbc7dc6d8fe5da5ecffc2dc2dae6a7c3999db53a89e9c16)
                check_type(argname="argument container_path", value=container_path, expected_type=type_hints["container_path"])
                check_type(argname="argument host_path", value=host_path, expected_type=type_hints["host_path"])
                check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if container_path is not None:
                self._values["container_path"] = container_path
            if host_path is not None:
                self._values["host_path"] = host_path
            if permissions is not None:
                self._values["permissions"] = permissions

        @builtins.property
        def container_path(self) -> typing.Optional[builtins.str]:
            '''The path inside the container that's used to expose the host device.

            By default, the ``hostPath`` value is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-device.html#cfn-batch-jobdefinition-device-containerpath
            '''
            result = self._values.get("container_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def host_path(self) -> typing.Optional[builtins.str]:
            '''The path for the device on the host container instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-device.html#cfn-batch-jobdefinition-device-hostpath
            '''
            result = self._values.get("host_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def permissions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The explicit permissions to provide to the container for the device.

            By default, the container has permissions for ``read`` , ``write`` , and ``mknod`` for the device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-device.html#cfn-batch-jobdefinition-device-permissions
            '''
            result = self._values.get("permissions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeviceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.EcsPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"task_properties": "taskProperties"},
    )
    class EcsPropertiesProperty:
        def __init__(
            self,
            *,
            task_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.EcsTaskPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''An object that contains the properties for the Amazon ECS resources of a job.

            :param task_properties: An object that contains the properties for the Amazon ECS task definition of a job. .. epigraph:: This object is currently limited to one task element. However, the task element can run up to 10 containers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ecsproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                # options: Any
                
                ecs_properties_property = batch_mixins.CfnJobDefinitionPropsMixin.EcsPropertiesProperty(
                    task_properties=[batch_mixins.CfnJobDefinitionPropsMixin.EcsTaskPropertiesProperty(
                        containers=[batch_mixins.CfnJobDefinitionPropsMixin.TaskContainerPropertiesProperty(
                            command=["command"],
                            depends_on=[batch_mixins.CfnJobDefinitionPropsMixin.TaskContainerDependencyProperty(
                                condition="condition",
                                container_name="containerName"
                            )],
                            environment=[batch_mixins.CfnJobDefinitionPropsMixin.EnvironmentProperty(
                                name="name",
                                value="value"
                            )],
                            essential=False,
                            firelens_configuration=batch_mixins.CfnJobDefinitionPropsMixin.FirelensConfigurationProperty(
                                options={
                                    "options_key": "options"
                                },
                                type="type"
                            ),
                            image="image",
                            linux_parameters=batch_mixins.CfnJobDefinitionPropsMixin.LinuxParametersProperty(
                                devices=[batch_mixins.CfnJobDefinitionPropsMixin.DeviceProperty(
                                    container_path="containerPath",
                                    host_path="hostPath",
                                    permissions=["permissions"]
                                )],
                                init_process_enabled=False,
                                max_swap=123,
                                shared_memory_size=123,
                                swappiness=123,
                                tmpfs=[batch_mixins.CfnJobDefinitionPropsMixin.TmpfsProperty(
                                    container_path="containerPath",
                                    mount_options=["mountOptions"],
                                    size=123
                                )]
                            ),
                            log_configuration=batch_mixins.CfnJobDefinitionPropsMixin.LogConfigurationProperty(
                                log_driver="logDriver",
                                options=options,
                                secret_options=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                                    name="name",
                                    value_from="valueFrom"
                                )]
                            ),
                            mount_points=[batch_mixins.CfnJobDefinitionPropsMixin.MountPointProperty(
                                container_path="containerPath",
                                read_only=False,
                                source_volume="sourceVolume"
                            )],
                            name="name",
                            privileged=False,
                            readonly_root_filesystem=False,
                            repository_credentials=batch_mixins.CfnJobDefinitionPropsMixin.RepositoryCredentialsProperty(
                                credentials_parameter="credentialsParameter"
                            ),
                            resource_requirements=[batch_mixins.CfnJobDefinitionPropsMixin.ResourceRequirementProperty(
                                type="type",
                                value="value"
                            )],
                            secrets=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                                name="name",
                                value_from="valueFrom"
                            )],
                            ulimits=[batch_mixins.CfnJobDefinitionPropsMixin.UlimitProperty(
                                hard_limit=123,
                                name="name",
                                soft_limit=123
                            )],
                            user="user"
                        )],
                        enable_execute_command=False,
                        ephemeral_storage=batch_mixins.CfnJobDefinitionPropsMixin.EphemeralStorageProperty(
                            size_in_gi_b=123
                        ),
                        execution_role_arn="executionRoleArn",
                        ipc_mode="ipcMode",
                        network_configuration=batch_mixins.CfnJobDefinitionPropsMixin.NetworkConfigurationProperty(
                            assign_public_ip="assignPublicIp"
                        ),
                        pid_mode="pidMode",
                        platform_version="platformVersion",
                        runtime_platform=batch_mixins.CfnJobDefinitionPropsMixin.RuntimePlatformProperty(
                            cpu_architecture="cpuArchitecture",
                            operating_system_family="operatingSystemFamily"
                        ),
                        task_role_arn="taskRoleArn",
                        volumes=[batch_mixins.CfnJobDefinitionPropsMixin.VolumesProperty(
                            efs_volume_configuration=batch_mixins.CfnJobDefinitionPropsMixin.EfsVolumeConfigurationProperty(
                                authorization_config=batch_mixins.CfnJobDefinitionPropsMixin.AuthorizationConfigProperty(
                                    access_point_id="accessPointId",
                                    iam="iam"
                                ),
                                file_system_id="fileSystemId",
                                root_directory="rootDirectory",
                                transit_encryption="transitEncryption",
                                transit_encryption_port=123
                            ),
                            host=batch_mixins.CfnJobDefinitionPropsMixin.VolumesHostProperty(
                                source_path="sourcePath"
                            ),
                            name="name"
                        )]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f43527e74009146074a93c08a0be76a471666027e6f2df162e469ec0fe01866)
                check_type(argname="argument task_properties", value=task_properties, expected_type=type_hints["task_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if task_properties is not None:
                self._values["task_properties"] = task_properties

        @builtins.property
        def task_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EcsTaskPropertiesProperty"]]]]:
            '''An object that contains the properties for the Amazon ECS task definition of a job.

            .. epigraph::

               This object is currently limited to one task element. However, the task element can run up to 10 containers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ecsproperties.html#cfn-batch-jobdefinition-ecsproperties-taskproperties
            '''
            result = self._values.get("task_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EcsTaskPropertiesProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EcsPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.EcsTaskPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "containers": "containers",
            "enable_execute_command": "enableExecuteCommand",
            "ephemeral_storage": "ephemeralStorage",
            "execution_role_arn": "executionRoleArn",
            "ipc_mode": "ipcMode",
            "network_configuration": "networkConfiguration",
            "pid_mode": "pidMode",
            "platform_version": "platformVersion",
            "runtime_platform": "runtimePlatform",
            "task_role_arn": "taskRoleArn",
            "volumes": "volumes",
        },
    )
    class EcsTaskPropertiesProperty:
        def __init__(
            self,
            *,
            containers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.TaskContainerPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            enable_execute_command: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            ephemeral_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.EphemeralStorageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            execution_role_arn: typing.Optional[builtins.str] = None,
            ipc_mode: typing.Optional[builtins.str] = None,
            network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.NetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            pid_mode: typing.Optional[builtins.str] = None,
            platform_version: typing.Optional[builtins.str] = None,
            runtime_platform: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.RuntimePlatformProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            task_role_arn: typing.Optional[builtins.str] = None,
            volumes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.VolumesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The properties for a task definition that describes the container and volume definitions of an Amazon ECS task.

            You can specify which Docker images to use, the required resources, and other configurations related to launching the task definition through an Amazon ECS service or task.

            :param containers: This object is a list of containers.
            :param enable_execute_command: Determines whether execute command functionality is turned on for this task. If ``true`` , execute command functionality is turned on all the containers in the task.
            :param ephemeral_storage: The amount of ephemeral storage to allocate for the task. This parameter is used to expand the total amount of ephemeral storage available, beyond the default amount, for tasks hosted on AWS Fargate .
            :param execution_role_arn: The Amazon Resource Name (ARN) of the execution role that AWS Batch can assume. For jobs that run on Fargate resources, you must provide an execution role. For more information, see `AWS Batch execution IAM role <https://docs.aws.amazon.com/batch/latest/userguide/execution-IAM-role.html>`_ in the *AWS Batch User Guide* .
            :param ipc_mode: The IPC resource namespace to use for the containers in the task. The valid values are ``host`` , ``task`` , or ``none`` . If ``host`` is specified, all containers within the tasks that specified the ``host`` IPC mode on the same container instance share the same IPC resources with the host Amazon EC2 instance. If ``task`` is specified, all containers within the specified ``task`` share the same IPC resources. If ``none`` is specified, the IPC resources within the containers of a task are private, and are not shared with other containers in a task or on the container instance. If no value is specified, then the IPC resource namespace sharing depends on the Docker daemon setting on the container instance. For more information, see `IPC settings <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/#ipc-settings---ipc>`_ in the Docker run reference.
            :param network_configuration: The network configuration for jobs that are running on Fargate resources. Jobs that are running on Amazon EC2 resources must not specify this parameter.
            :param pid_mode: The process namespace to use for the containers in the task. The valid values are ``host`` or ``task`` . For example, monitoring sidecars might need ``pidMode`` to access information about other containers running in the same task. If ``host`` is specified, all containers within the tasks that specified the ``host`` PID mode on the same container instance share the process namespace with the host Amazon EC2 instance. If ``task`` is specified, all containers within the specified task share the same process namespace. If no value is specified, the default is a private namespace for each container. For more information, see `PID settings <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/#pid-settings---pid>`_ in the Docker run reference.
            :param platform_version: The Fargate platform version where the jobs are running. A platform version is specified only for jobs that are running on Fargate resources. If one isn't specified, the ``LATEST`` platform version is used by default. This uses a recent, approved version of the Fargate platform for compute resources. For more information, see `AWS Fargate platform versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the *Amazon Elastic Container Service Developer Guide* .
            :param runtime_platform: An object that represents the compute environment architecture for AWS Batch jobs on Fargate.
            :param task_role_arn: The Amazon Resource Name (ARN) that's associated with the Amazon ECS task. .. epigraph:: This is object is comparable to `ContainerProperties:jobRoleArn <https://docs.aws.amazon.com/batch/latest/APIReference/API_ContainerProperties.html>`_ .
            :param volumes: A list of volumes that are associated with the job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ecstaskproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                # options: Any
                
                ecs_task_properties_property = batch_mixins.CfnJobDefinitionPropsMixin.EcsTaskPropertiesProperty(
                    containers=[batch_mixins.CfnJobDefinitionPropsMixin.TaskContainerPropertiesProperty(
                        command=["command"],
                        depends_on=[batch_mixins.CfnJobDefinitionPropsMixin.TaskContainerDependencyProperty(
                            condition="condition",
                            container_name="containerName"
                        )],
                        environment=[batch_mixins.CfnJobDefinitionPropsMixin.EnvironmentProperty(
                            name="name",
                            value="value"
                        )],
                        essential=False,
                        firelens_configuration=batch_mixins.CfnJobDefinitionPropsMixin.FirelensConfigurationProperty(
                            options={
                                "options_key": "options"
                            },
                            type="type"
                        ),
                        image="image",
                        linux_parameters=batch_mixins.CfnJobDefinitionPropsMixin.LinuxParametersProperty(
                            devices=[batch_mixins.CfnJobDefinitionPropsMixin.DeviceProperty(
                                container_path="containerPath",
                                host_path="hostPath",
                                permissions=["permissions"]
                            )],
                            init_process_enabled=False,
                            max_swap=123,
                            shared_memory_size=123,
                            swappiness=123,
                            tmpfs=[batch_mixins.CfnJobDefinitionPropsMixin.TmpfsProperty(
                                container_path="containerPath",
                                mount_options=["mountOptions"],
                                size=123
                            )]
                        ),
                        log_configuration=batch_mixins.CfnJobDefinitionPropsMixin.LogConfigurationProperty(
                            log_driver="logDriver",
                            options=options,
                            secret_options=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                                name="name",
                                value_from="valueFrom"
                            )]
                        ),
                        mount_points=[batch_mixins.CfnJobDefinitionPropsMixin.MountPointProperty(
                            container_path="containerPath",
                            read_only=False,
                            source_volume="sourceVolume"
                        )],
                        name="name",
                        privileged=False,
                        readonly_root_filesystem=False,
                        repository_credentials=batch_mixins.CfnJobDefinitionPropsMixin.RepositoryCredentialsProperty(
                            credentials_parameter="credentialsParameter"
                        ),
                        resource_requirements=[batch_mixins.CfnJobDefinitionPropsMixin.ResourceRequirementProperty(
                            type="type",
                            value="value"
                        )],
                        secrets=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                            name="name",
                            value_from="valueFrom"
                        )],
                        ulimits=[batch_mixins.CfnJobDefinitionPropsMixin.UlimitProperty(
                            hard_limit=123,
                            name="name",
                            soft_limit=123
                        )],
                        user="user"
                    )],
                    enable_execute_command=False,
                    ephemeral_storage=batch_mixins.CfnJobDefinitionPropsMixin.EphemeralStorageProperty(
                        size_in_gi_b=123
                    ),
                    execution_role_arn="executionRoleArn",
                    ipc_mode="ipcMode",
                    network_configuration=batch_mixins.CfnJobDefinitionPropsMixin.NetworkConfigurationProperty(
                        assign_public_ip="assignPublicIp"
                    ),
                    pid_mode="pidMode",
                    platform_version="platformVersion",
                    runtime_platform=batch_mixins.CfnJobDefinitionPropsMixin.RuntimePlatformProperty(
                        cpu_architecture="cpuArchitecture",
                        operating_system_family="operatingSystemFamily"
                    ),
                    task_role_arn="taskRoleArn",
                    volumes=[batch_mixins.CfnJobDefinitionPropsMixin.VolumesProperty(
                        efs_volume_configuration=batch_mixins.CfnJobDefinitionPropsMixin.EfsVolumeConfigurationProperty(
                            authorization_config=batch_mixins.CfnJobDefinitionPropsMixin.AuthorizationConfigProperty(
                                access_point_id="accessPointId",
                                iam="iam"
                            ),
                            file_system_id="fileSystemId",
                            root_directory="rootDirectory",
                            transit_encryption="transitEncryption",
                            transit_encryption_port=123
                        ),
                        host=batch_mixins.CfnJobDefinitionPropsMixin.VolumesHostProperty(
                            source_path="sourcePath"
                        ),
                        name="name"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__10d48aac040b1240ed1ab74ad217f7da6599e55f40a8b0b56ee6f019f964168c)
                check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
                check_type(argname="argument enable_execute_command", value=enable_execute_command, expected_type=type_hints["enable_execute_command"])
                check_type(argname="argument ephemeral_storage", value=ephemeral_storage, expected_type=type_hints["ephemeral_storage"])
                check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
                check_type(argname="argument ipc_mode", value=ipc_mode, expected_type=type_hints["ipc_mode"])
                check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
                check_type(argname="argument pid_mode", value=pid_mode, expected_type=type_hints["pid_mode"])
                check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
                check_type(argname="argument runtime_platform", value=runtime_platform, expected_type=type_hints["runtime_platform"])
                check_type(argname="argument task_role_arn", value=task_role_arn, expected_type=type_hints["task_role_arn"])
                check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if containers is not None:
                self._values["containers"] = containers
            if enable_execute_command is not None:
                self._values["enable_execute_command"] = enable_execute_command
            if ephemeral_storage is not None:
                self._values["ephemeral_storage"] = ephemeral_storage
            if execution_role_arn is not None:
                self._values["execution_role_arn"] = execution_role_arn
            if ipc_mode is not None:
                self._values["ipc_mode"] = ipc_mode
            if network_configuration is not None:
                self._values["network_configuration"] = network_configuration
            if pid_mode is not None:
                self._values["pid_mode"] = pid_mode
            if platform_version is not None:
                self._values["platform_version"] = platform_version
            if runtime_platform is not None:
                self._values["runtime_platform"] = runtime_platform
            if task_role_arn is not None:
                self._values["task_role_arn"] = task_role_arn
            if volumes is not None:
                self._values["volumes"] = volumes

        @builtins.property
        def containers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.TaskContainerPropertiesProperty"]]]]:
            '''This object is a list of containers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ecstaskproperties.html#cfn-batch-jobdefinition-ecstaskproperties-containers
            '''
            result = self._values.get("containers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.TaskContainerPropertiesProperty"]]]], result)

        @builtins.property
        def enable_execute_command(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether execute command functionality is turned on for this task.

            If ``true`` , execute command functionality is turned on all the containers in the task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ecstaskproperties.html#cfn-batch-jobdefinition-ecstaskproperties-enableexecutecommand
            '''
            result = self._values.get("enable_execute_command")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def ephemeral_storage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EphemeralStorageProperty"]]:
            '''The amount of ephemeral storage to allocate for the task.

            This parameter is used to expand the total amount of ephemeral storage available, beyond the default amount, for tasks hosted on AWS Fargate .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ecstaskproperties.html#cfn-batch-jobdefinition-ecstaskproperties-ephemeralstorage
            '''
            result = self._values.get("ephemeral_storage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EphemeralStorageProperty"]], result)

        @builtins.property
        def execution_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the execution role that AWS Batch can assume.

            For jobs that run on Fargate resources, you must provide an execution role. For more information, see `AWS Batch execution IAM role <https://docs.aws.amazon.com/batch/latest/userguide/execution-IAM-role.html>`_ in the *AWS Batch User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ecstaskproperties.html#cfn-batch-jobdefinition-ecstaskproperties-executionrolearn
            '''
            result = self._values.get("execution_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ipc_mode(self) -> typing.Optional[builtins.str]:
            '''The IPC resource namespace to use for the containers in the task.

            The valid values are ``host`` , ``task`` , or ``none`` .

            If ``host`` is specified, all containers within the tasks that specified the ``host`` IPC mode on the same container instance share the same IPC resources with the host Amazon EC2 instance.

            If ``task`` is specified, all containers within the specified ``task`` share the same IPC resources.

            If ``none`` is specified, the IPC resources within the containers of a task are private, and are not shared with other containers in a task or on the container instance.

            If no value is specified, then the IPC resource namespace sharing depends on the Docker daemon setting on the container instance. For more information, see `IPC settings <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/#ipc-settings---ipc>`_ in the Docker run reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ecstaskproperties.html#cfn-batch-jobdefinition-ecstaskproperties-ipcmode
            '''
            result = self._values.get("ipc_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def network_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.NetworkConfigurationProperty"]]:
            '''The network configuration for jobs that are running on Fargate resources.

            Jobs that are running on Amazon EC2 resources must not specify this parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ecstaskproperties.html#cfn-batch-jobdefinition-ecstaskproperties-networkconfiguration
            '''
            result = self._values.get("network_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.NetworkConfigurationProperty"]], result)

        @builtins.property
        def pid_mode(self) -> typing.Optional[builtins.str]:
            '''The process namespace to use for the containers in the task.

            The valid values are ``host`` or ``task`` . For example, monitoring sidecars might need ``pidMode`` to access information about other containers running in the same task.

            If ``host`` is specified, all containers within the tasks that specified the ``host`` PID mode on the same container instance share the process namespace with the host Amazon EC2 instance.

            If ``task`` is specified, all containers within the specified task share the same process namespace.

            If no value is specified, the default is a private namespace for each container. For more information, see `PID settings <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/#pid-settings---pid>`_ in the Docker run reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ecstaskproperties.html#cfn-batch-jobdefinition-ecstaskproperties-pidmode
            '''
            result = self._values.get("pid_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def platform_version(self) -> typing.Optional[builtins.str]:
            '''The Fargate platform version where the jobs are running.

            A platform version is specified only for jobs that are running on Fargate resources. If one isn't specified, the ``LATEST`` platform version is used by default. This uses a recent, approved version of the Fargate platform for compute resources. For more information, see `AWS Fargate platform versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ecstaskproperties.html#cfn-batch-jobdefinition-ecstaskproperties-platformversion
            '''
            result = self._values.get("platform_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def runtime_platform(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.RuntimePlatformProperty"]]:
            '''An object that represents the compute environment architecture for AWS Batch jobs on Fargate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ecstaskproperties.html#cfn-batch-jobdefinition-ecstaskproperties-runtimeplatform
            '''
            result = self._values.get("runtime_platform")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.RuntimePlatformProperty"]], result)

        @builtins.property
        def task_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) that's associated with the Amazon ECS task.

            .. epigraph::

               This is object is comparable to `ContainerProperties:jobRoleArn <https://docs.aws.amazon.com/batch/latest/APIReference/API_ContainerProperties.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ecstaskproperties.html#cfn-batch-jobdefinition-ecstaskproperties-taskrolearn
            '''
            result = self._values.get("task_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def volumes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.VolumesProperty"]]]]:
            '''A list of volumes that are associated with the job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ecstaskproperties.html#cfn-batch-jobdefinition-ecstaskproperties-volumes
            '''
            result = self._values.get("volumes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.VolumesProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EcsTaskPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.EfsVolumeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorization_config": "authorizationConfig",
            "file_system_id": "fileSystemId",
            "root_directory": "rootDirectory",
            "transit_encryption": "transitEncryption",
            "transit_encryption_port": "transitEncryptionPort",
        },
    )
    class EfsVolumeConfigurationProperty:
        def __init__(
            self,
            *,
            authorization_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.AuthorizationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            file_system_id: typing.Optional[builtins.str] = None,
            root_directory: typing.Optional[builtins.str] = None,
            transit_encryption: typing.Optional[builtins.str] = None,
            transit_encryption_port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param authorization_config: 
            :param file_system_id: 
            :param root_directory: 
            :param transit_encryption: 
            :param transit_encryption_port: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-efsvolumeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                efs_volume_configuration_property = batch_mixins.CfnJobDefinitionPropsMixin.EfsVolumeConfigurationProperty(
                    authorization_config=batch_mixins.CfnJobDefinitionPropsMixin.AuthorizationConfigProperty(
                        access_point_id="accessPointId",
                        iam="iam"
                    ),
                    file_system_id="fileSystemId",
                    root_directory="rootDirectory",
                    transit_encryption="transitEncryption",
                    transit_encryption_port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9d746f40c72d4b2e1cf30831369ccecbcb84aad796e72c4a4f92ad034fdeb32c)
                check_type(argname="argument authorization_config", value=authorization_config, expected_type=type_hints["authorization_config"])
                check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
                check_type(argname="argument root_directory", value=root_directory, expected_type=type_hints["root_directory"])
                check_type(argname="argument transit_encryption", value=transit_encryption, expected_type=type_hints["transit_encryption"])
                check_type(argname="argument transit_encryption_port", value=transit_encryption_port, expected_type=type_hints["transit_encryption_port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authorization_config is not None:
                self._values["authorization_config"] = authorization_config
            if file_system_id is not None:
                self._values["file_system_id"] = file_system_id
            if root_directory is not None:
                self._values["root_directory"] = root_directory
            if transit_encryption is not None:
                self._values["transit_encryption"] = transit_encryption
            if transit_encryption_port is not None:
                self._values["transit_encryption_port"] = transit_encryption_port

        @builtins.property
        def authorization_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.AuthorizationConfigProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-efsvolumeconfiguration.html#cfn-batch-jobdefinition-efsvolumeconfiguration-authorizationconfig
            '''
            result = self._values.get("authorization_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.AuthorizationConfigProperty"]], result)

        @builtins.property
        def file_system_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-efsvolumeconfiguration.html#cfn-batch-jobdefinition-efsvolumeconfiguration-filesystemid
            '''
            result = self._values.get("file_system_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def root_directory(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-efsvolumeconfiguration.html#cfn-batch-jobdefinition-efsvolumeconfiguration-rootdirectory
            '''
            result = self._values.get("root_directory")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def transit_encryption(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-efsvolumeconfiguration.html#cfn-batch-jobdefinition-efsvolumeconfiguration-transitencryption
            '''
            result = self._values.get("transit_encryption")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def transit_encryption_port(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-efsvolumeconfiguration.html#cfn-batch-jobdefinition-efsvolumeconfiguration-transitencryptionport
            '''
            result = self._values.get("transit_encryption_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EfsVolumeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.EksContainerEnvironmentVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class EksContainerEnvironmentVariableProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An environment variable.

            :param name: The name of the environment variable.
            :param value: The value of the environment variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainerenvironmentvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                eks_container_environment_variable_property = batch_mixins.CfnJobDefinitionPropsMixin.EksContainerEnvironmentVariableProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__610e71856483adb0d62ca5484a1f9f7644a50b02b762e82d3d37f4b27ba155c3)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the environment variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainerenvironmentvariable.html#cfn-batch-jobdefinition-ekscontainerenvironmentvariable-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the environment variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainerenvironmentvariable.html#cfn-batch-jobdefinition-ekscontainerenvironmentvariable-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksContainerEnvironmentVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.EksContainerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "args": "args",
            "command": "command",
            "env": "env",
            "image": "image",
            "image_pull_policy": "imagePullPolicy",
            "name": "name",
            "resources": "resources",
            "security_context": "securityContext",
            "volume_mounts": "volumeMounts",
        },
    )
    class EksContainerProperty:
        def __init__(
            self,
            *,
            args: typing.Optional[typing.Sequence[builtins.str]] = None,
            command: typing.Optional[typing.Sequence[builtins.str]] = None,
            env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.EksContainerEnvironmentVariableProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            image: typing.Optional[builtins.str] = None,
            image_pull_policy: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.ResourcesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            security_context: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.SecurityContextProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            volume_mounts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.EksContainerVolumeMountProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''EKS container properties are used in job definitions for Amazon EKS based job definitions to describe the properties for a container node in the pod that's launched as part of a job.

            This can't be specified for Amazon ECS based job definitions.

            :param args: An array of arguments to the entrypoint. If this isn't specified, the ``CMD`` of the container image is used. This corresponds to the ``args`` member in the `Entrypoint <https://docs.aws.amazon.com/https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#entrypoint>`_ portion of the `Pod <https://docs.aws.amazon.com/https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/>`_ in Kubernetes. Environment variable references are expanded using the container's environment. If the referenced environment variable doesn't exist, the reference in the command isn't changed. For example, if the reference is to " ``$(NAME1)`` " and the ``NAME1`` environment variable doesn't exist, the command string will remain " ``$(NAME1)`` ." ``$$`` is replaced with ``$`` , and the resulting string isn't expanded. For example, ``$$(VAR_NAME)`` is passed as ``$(VAR_NAME)`` whether or not the ``VAR_NAME`` environment variable exists. For more information, see `Dockerfile reference: CMD <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/builder/#cmd>`_ and `Define a command and arguments for a pod <https://docs.aws.amazon.com/https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/>`_ in the *Kubernetes documentation* .
            :param command: The entrypoint for the container. This isn't run within a shell. If this isn't specified, the ``ENTRYPOINT`` of the container image is used. Environment variable references are expanded using the container's environment. If the referenced environment variable doesn't exist, the reference in the command isn't changed. For example, if the reference is to " ``$(NAME1)`` " and the ``NAME1`` environment variable doesn't exist, the command string will remain " ``$(NAME1)`` ." ``$$`` is replaced with ``$`` and the resulting string isn't expanded. For example, ``$$(VAR_NAME)`` will be passed as ``$(VAR_NAME)`` whether or not the ``VAR_NAME`` environment variable exists. The entrypoint can't be updated. For more information, see `ENTRYPOINT <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/builder/#entrypoint>`_ in the *Dockerfile reference* and `Define a command and arguments for a container <https://docs.aws.amazon.com/https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/>`_ and `Entrypoint <https://docs.aws.amazon.com/https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#entrypoint>`_ in the *Kubernetes documentation* .
            :param env: The environment variables to pass to a container. .. epigraph:: Environment variables cannot start with " ``AWS_BATCH`` ". This naming convention is reserved for variables that AWS Batch sets.
            :param image: The Docker image used to start the container.
            :param image_pull_policy: The image pull policy for the container. Supported values are ``Always`` , ``IfNotPresent`` , and ``Never`` . This parameter defaults to ``IfNotPresent`` . However, if the ``:latest`` tag is specified, it defaults to ``Always`` . For more information, see `Updating images <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/containers/images/#updating-images>`_ in the *Kubernetes documentation* .
            :param name: The name of the container. If the name isn't specified, the default name " ``Default`` " is used. Each container in a pod must have a unique name.
            :param resources: The type and amount of resources to assign to a container. The supported resources include ``memory`` , ``cpu`` , and ``nvidia.com/gpu`` . For more information, see `Resource management for pods and containers <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/>`_ in the *Kubernetes documentation* .
            :param security_context: The security context for a job. For more information, see `Configure a security context for a pod or container <https://docs.aws.amazon.com/https://kubernetes.io/docs/tasks/configure-pod-container/security-context/>`_ in the *Kubernetes documentation* .
            :param volume_mounts: The volume mounts for the container. AWS Batch supports ``emptyDir`` , ``hostPath`` , and ``secret`` volume types. For more information about volumes and volume mounts in Kubernetes, see `Volumes <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/>`_ in the *Kubernetes documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainer.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                # limits: Any
                # requests: Any
                
                eks_container_property = batch_mixins.CfnJobDefinitionPropsMixin.EksContainerProperty(
                    args=["args"],
                    command=["command"],
                    env=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerEnvironmentVariableProperty(
                        name="name",
                        value="value"
                    )],
                    image="image",
                    image_pull_policy="imagePullPolicy",
                    name="name",
                    resources=batch_mixins.CfnJobDefinitionPropsMixin.ResourcesProperty(
                        limits=limits,
                        requests=requests
                    ),
                    security_context=batch_mixins.CfnJobDefinitionPropsMixin.SecurityContextProperty(
                        allow_privilege_escalation=False,
                        privileged=False,
                        read_only_root_filesystem=False,
                        run_as_group=123,
                        run_as_non_root=False,
                        run_as_user=123
                    ),
                    volume_mounts=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerVolumeMountProperty(
                        mount_path="mountPath",
                        name="name",
                        read_only=False,
                        sub_path="subPath"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b7d1118b1ddd2e3c55b50d6427f174d05619687cc7547da022d35a498ccfc570)
                check_type(argname="argument args", value=args, expected_type=type_hints["args"])
                check_type(argname="argument command", value=command, expected_type=type_hints["command"])
                check_type(argname="argument env", value=env, expected_type=type_hints["env"])
                check_type(argname="argument image", value=image, expected_type=type_hints["image"])
                check_type(argname="argument image_pull_policy", value=image_pull_policy, expected_type=type_hints["image_pull_policy"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
                check_type(argname="argument security_context", value=security_context, expected_type=type_hints["security_context"])
                check_type(argname="argument volume_mounts", value=volume_mounts, expected_type=type_hints["volume_mounts"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if args is not None:
                self._values["args"] = args
            if command is not None:
                self._values["command"] = command
            if env is not None:
                self._values["env"] = env
            if image is not None:
                self._values["image"] = image
            if image_pull_policy is not None:
                self._values["image_pull_policy"] = image_pull_policy
            if name is not None:
                self._values["name"] = name
            if resources is not None:
                self._values["resources"] = resources
            if security_context is not None:
                self._values["security_context"] = security_context
            if volume_mounts is not None:
                self._values["volume_mounts"] = volume_mounts

        @builtins.property
        def args(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of arguments to the entrypoint.

            If this isn't specified, the ``CMD`` of the container image is used. This corresponds to the ``args`` member in the `Entrypoint <https://docs.aws.amazon.com/https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#entrypoint>`_ portion of the `Pod <https://docs.aws.amazon.com/https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/>`_ in Kubernetes. Environment variable references are expanded using the container's environment.

            If the referenced environment variable doesn't exist, the reference in the command isn't changed. For example, if the reference is to " ``$(NAME1)`` " and the ``NAME1`` environment variable doesn't exist, the command string will remain " ``$(NAME1)`` ." ``$$`` is replaced with ``$`` , and the resulting string isn't expanded. For example, ``$$(VAR_NAME)`` is passed as ``$(VAR_NAME)`` whether or not the ``VAR_NAME`` environment variable exists. For more information, see `Dockerfile reference: CMD <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/builder/#cmd>`_ and `Define a command and arguments for a pod <https://docs.aws.amazon.com/https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/>`_ in the *Kubernetes documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainer.html#cfn-batch-jobdefinition-ekscontainer-args
            '''
            result = self._values.get("args")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def command(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The entrypoint for the container.

            This isn't run within a shell. If this isn't specified, the ``ENTRYPOINT`` of the container image is used. Environment variable references are expanded using the container's environment.

            If the referenced environment variable doesn't exist, the reference in the command isn't changed. For example, if the reference is to " ``$(NAME1)`` " and the ``NAME1`` environment variable doesn't exist, the command string will remain " ``$(NAME1)`` ." ``$$`` is replaced with ``$`` and the resulting string isn't expanded. For example, ``$$(VAR_NAME)`` will be passed as ``$(VAR_NAME)`` whether or not the ``VAR_NAME`` environment variable exists. The entrypoint can't be updated. For more information, see `ENTRYPOINT <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/builder/#entrypoint>`_ in the *Dockerfile reference* and `Define a command and arguments for a container <https://docs.aws.amazon.com/https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/>`_ and `Entrypoint <https://docs.aws.amazon.com/https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#entrypoint>`_ in the *Kubernetes documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainer.html#cfn-batch-jobdefinition-ekscontainer-command
            '''
            result = self._values.get("command")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def env(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EksContainerEnvironmentVariableProperty"]]]]:
            '''The environment variables to pass to a container.

            .. epigraph::

               Environment variables cannot start with " ``AWS_BATCH`` ". This naming convention is reserved for variables that AWS Batch sets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainer.html#cfn-batch-jobdefinition-ekscontainer-env
            '''
            result = self._values.get("env")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EksContainerEnvironmentVariableProperty"]]]], result)

        @builtins.property
        def image(self) -> typing.Optional[builtins.str]:
            '''The Docker image used to start the container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainer.html#cfn-batch-jobdefinition-ekscontainer-image
            '''
            result = self._values.get("image")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_pull_policy(self) -> typing.Optional[builtins.str]:
            '''The image pull policy for the container.

            Supported values are ``Always`` , ``IfNotPresent`` , and ``Never`` . This parameter defaults to ``IfNotPresent`` . However, if the ``:latest`` tag is specified, it defaults to ``Always`` . For more information, see `Updating images <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/containers/images/#updating-images>`_ in the *Kubernetes documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainer.html#cfn-batch-jobdefinition-ekscontainer-imagepullpolicy
            '''
            result = self._values.get("image_pull_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the container.

            If the name isn't specified, the default name " ``Default`` " is used. Each container in a pod must have a unique name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainer.html#cfn-batch-jobdefinition-ekscontainer-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resources(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.ResourcesProperty"]]:
            '''The type and amount of resources to assign to a container.

            The supported resources include ``memory`` , ``cpu`` , and ``nvidia.com/gpu`` . For more information, see `Resource management for pods and containers <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/>`_ in the *Kubernetes documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainer.html#cfn-batch-jobdefinition-ekscontainer-resources
            '''
            result = self._values.get("resources")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.ResourcesProperty"]], result)

        @builtins.property
        def security_context(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.SecurityContextProperty"]]:
            '''The security context for a job.

            For more information, see `Configure a security context for a pod or container <https://docs.aws.amazon.com/https://kubernetes.io/docs/tasks/configure-pod-container/security-context/>`_ in the *Kubernetes documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainer.html#cfn-batch-jobdefinition-ekscontainer-securitycontext
            '''
            result = self._values.get("security_context")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.SecurityContextProperty"]], result)

        @builtins.property
        def volume_mounts(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EksContainerVolumeMountProperty"]]]]:
            '''The volume mounts for the container.

            AWS Batch supports ``emptyDir`` , ``hostPath`` , and ``secret`` volume types. For more information about volumes and volume mounts in Kubernetes, see `Volumes <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/>`_ in the *Kubernetes documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainer.html#cfn-batch-jobdefinition-ekscontainer-volumemounts
            '''
            result = self._values.get("volume_mounts")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EksContainerVolumeMountProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksContainerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.EksContainerVolumeMountProperty",
        jsii_struct_bases=[],
        name_mapping={
            "mount_path": "mountPath",
            "name": "name",
            "read_only": "readOnly",
            "sub_path": "subPath",
        },
    )
    class EksContainerVolumeMountProperty:
        def __init__(
            self,
            *,
            mount_path: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            sub_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The volume mounts for a container for an Amazon EKS job.

            For more information about volumes and volume mounts in Kubernetes, see `Volumes <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/>`_ in the *Kubernetes documentation* .

            :param mount_path: The path on the container where the volume is mounted.
            :param name: The name the volume mount. This must match the name of one of the volumes in the pod.
            :param read_only: If this value is ``true`` , the container has read-only access to the volume. Otherwise, the container can write to the volume. The default value is ``false`` .
            :param sub_path: A sub-path inside the referenced volume instead of its root.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainervolumemount.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                eks_container_volume_mount_property = batch_mixins.CfnJobDefinitionPropsMixin.EksContainerVolumeMountProperty(
                    mount_path="mountPath",
                    name="name",
                    read_only=False,
                    sub_path="subPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__670f1be772833ab577dafd36d83046dfee8dffbbb7ed935e2a7dc64350ff117a)
                check_type(argname="argument mount_path", value=mount_path, expected_type=type_hints["mount_path"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
                check_type(argname="argument sub_path", value=sub_path, expected_type=type_hints["sub_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mount_path is not None:
                self._values["mount_path"] = mount_path
            if name is not None:
                self._values["name"] = name
            if read_only is not None:
                self._values["read_only"] = read_only
            if sub_path is not None:
                self._values["sub_path"] = sub_path

        @builtins.property
        def mount_path(self) -> typing.Optional[builtins.str]:
            '''The path on the container where the volume is mounted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainervolumemount.html#cfn-batch-jobdefinition-ekscontainervolumemount-mountpath
            '''
            result = self._values.get("mount_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name the volume mount.

            This must match the name of one of the volumes in the pod.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainervolumemount.html#cfn-batch-jobdefinition-ekscontainervolumemount-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def read_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If this value is ``true`` , the container has read-only access to the volume.

            Otherwise, the container can write to the volume. The default value is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainervolumemount.html#cfn-batch-jobdefinition-ekscontainervolumemount-readonly
            '''
            result = self._values.get("read_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def sub_path(self) -> typing.Optional[builtins.str]:
            '''A sub-path inside the referenced volume instead of its root.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainervolumemount.html#cfn-batch-jobdefinition-ekscontainervolumemount-subpath
            '''
            result = self._values.get("sub_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksContainerVolumeMountProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.EksPersistentVolumeClaimProperty",
        jsii_struct_bases=[],
        name_mapping={"claim_name": "claimName", "read_only": "readOnly"},
    )
    class EksPersistentVolumeClaimProperty:
        def __init__(
            self,
            *,
            claim_name: typing.Optional[builtins.str] = None,
            read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''A ``persistentVolumeClaim`` volume is used to mount a `PersistentVolume <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/persistent-volumes/>`_ into a Pod. PersistentVolumeClaims are a way for users to "claim" durable storage without knowing the details of the particular cloud environment. See the information about `PersistentVolumes <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/persistent-volumes/>`_ in the *Kubernetes documentation* .

            :param claim_name: The name of the ``persistentVolumeClaim`` bounded to a ``persistentVolume`` . For more information, see `Persistent Volume Claims <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims>`_ in the *Kubernetes documentation* .
            :param read_only: An optional boolean value indicating if the mount is read only. Default is false. For more information, see `Read Only Mounts <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/#read-only-mounts>`_ in the *Kubernetes documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekspersistentvolumeclaim.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                eks_persistent_volume_claim_property = batch_mixins.CfnJobDefinitionPropsMixin.EksPersistentVolumeClaimProperty(
                    claim_name="claimName",
                    read_only=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a0751e687219b001decb2718958399b0781fcf70e6f6b78b5a00d5617993a58)
                check_type(argname="argument claim_name", value=claim_name, expected_type=type_hints["claim_name"])
                check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if claim_name is not None:
                self._values["claim_name"] = claim_name
            if read_only is not None:
                self._values["read_only"] = read_only

        @builtins.property
        def claim_name(self) -> typing.Optional[builtins.str]:
            '''The name of the ``persistentVolumeClaim`` bounded to a ``persistentVolume`` .

            For more information, see `Persistent Volume Claims <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims>`_ in the *Kubernetes documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekspersistentvolumeclaim.html#cfn-batch-jobdefinition-ekspersistentvolumeclaim-claimname
            '''
            result = self._values.get("claim_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def read_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''An optional boolean value indicating if the mount is read only.

            Default is false. For more information, see `Read Only Mounts <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/#read-only-mounts>`_ in the *Kubernetes documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekspersistentvolumeclaim.html#cfn-batch-jobdefinition-ekspersistentvolumeclaim-readonly
            '''
            result = self._values.get("read_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksPersistentVolumeClaimProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.EksPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"pod_properties": "podProperties"},
    )
    class EksPropertiesProperty:
        def __init__(
            self,
            *,
            pod_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.PodPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that contains the properties for the Kubernetes resources of a job.

            :param pod_properties: The properties for the Kubernetes pod resources of a job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-eksproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                # labels: Any
                # limits: Any
                # requests: Any
                
                eks_properties_property = batch_mixins.CfnJobDefinitionPropsMixin.EksPropertiesProperty(
                    pod_properties=batch_mixins.CfnJobDefinitionPropsMixin.PodPropertiesProperty(
                        containers=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerProperty(
                            args=["args"],
                            command=["command"],
                            env=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerEnvironmentVariableProperty(
                                name="name",
                                value="value"
                            )],
                            image="image",
                            image_pull_policy="imagePullPolicy",
                            name="name",
                            resources=batch_mixins.CfnJobDefinitionPropsMixin.ResourcesProperty(
                                limits=limits,
                                requests=requests
                            ),
                            security_context=batch_mixins.CfnJobDefinitionPropsMixin.SecurityContextProperty(
                                allow_privilege_escalation=False,
                                privileged=False,
                                read_only_root_filesystem=False,
                                run_as_group=123,
                                run_as_non_root=False,
                                run_as_user=123
                            ),
                            volume_mounts=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerVolumeMountProperty(
                                mount_path="mountPath",
                                name="name",
                                read_only=False,
                                sub_path="subPath"
                            )]
                        )],
                        dns_policy="dnsPolicy",
                        host_network=False,
                        image_pull_secrets=[batch_mixins.CfnJobDefinitionPropsMixin.ImagePullSecretProperty(
                            name="name"
                        )],
                        init_containers=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerProperty(
                            args=["args"],
                            command=["command"],
                            env=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerEnvironmentVariableProperty(
                                name="name",
                                value="value"
                            )],
                            image="image",
                            image_pull_policy="imagePullPolicy",
                            name="name",
                            resources=batch_mixins.CfnJobDefinitionPropsMixin.ResourcesProperty(
                                limits=limits,
                                requests=requests
                            ),
                            security_context=batch_mixins.CfnJobDefinitionPropsMixin.SecurityContextProperty(
                                allow_privilege_escalation=False,
                                privileged=False,
                                read_only_root_filesystem=False,
                                run_as_group=123,
                                run_as_non_root=False,
                                run_as_user=123
                            ),
                            volume_mounts=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerVolumeMountProperty(
                                mount_path="mountPath",
                                name="name",
                                read_only=False,
                                sub_path="subPath"
                            )]
                        )],
                        metadata=batch_mixins.CfnJobDefinitionPropsMixin.MetadataProperty(
                            labels=labels
                        ),
                        service_account_name="serviceAccountName",
                        share_process_namespace=False,
                        volumes=[batch_mixins.CfnJobDefinitionPropsMixin.EksVolumeProperty(
                            empty_dir=batch_mixins.CfnJobDefinitionPropsMixin.EmptyDirProperty(
                                medium="medium",
                                size_limit="sizeLimit"
                            ),
                            host_path=batch_mixins.CfnJobDefinitionPropsMixin.HostPathProperty(
                                path="path"
                            ),
                            name="name",
                            persistent_volume_claim=batch_mixins.CfnJobDefinitionPropsMixin.EksPersistentVolumeClaimProperty(
                                claim_name="claimName",
                                read_only=False
                            ),
                            secret=batch_mixins.CfnJobDefinitionPropsMixin.EksSecretProperty(
                                optional=False,
                                secret_name="secretName"
                            )
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1699fd5575882ca37d362f4225f8c5fb7977f5d1d9da25324b55cfe8b7c091c2)
                check_type(argname="argument pod_properties", value=pod_properties, expected_type=type_hints["pod_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if pod_properties is not None:
                self._values["pod_properties"] = pod_properties

        @builtins.property
        def pod_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.PodPropertiesProperty"]]:
            '''The properties for the Kubernetes pod resources of a job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-eksproperties.html#cfn-batch-jobdefinition-eksproperties-podproperties
            '''
            result = self._values.get("pod_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.PodPropertiesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.EksSecretProperty",
        jsii_struct_bases=[],
        name_mapping={"optional": "optional", "secret_name": "secretName"},
    )
    class EksSecretProperty:
        def __init__(
            self,
            *,
            optional: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            secret_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration of a Kubernetes ``secret`` volume.

            For more information, see `secret <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/#secret>`_ in the *Kubernetes documentation* .

            :param optional: Specifies whether the secret or the secret's keys must be defined.
            :param secret_name: The name of the secret. The name must be allowed as a DNS subdomain name. For more information, see `DNS subdomain names <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-subdomain-names>`_ in the *Kubernetes documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekssecret.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                eks_secret_property = batch_mixins.CfnJobDefinitionPropsMixin.EksSecretProperty(
                    optional=False,
                    secret_name="secretName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__33d0f748f7535e10c40eed1e837a480668788dbaf02f74f8de99afccf05cb650)
                check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
                check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if optional is not None:
                self._values["optional"] = optional
            if secret_name is not None:
                self._values["secret_name"] = secret_name

        @builtins.property
        def optional(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the secret or the secret's keys must be defined.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekssecret.html#cfn-batch-jobdefinition-ekssecret-optional
            '''
            result = self._values.get("optional")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def secret_name(self) -> typing.Optional[builtins.str]:
            '''The name of the secret.

            The name must be allowed as a DNS subdomain name. For more information, see `DNS subdomain names <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-subdomain-names>`_ in the *Kubernetes documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekssecret.html#cfn-batch-jobdefinition-ekssecret-secretname
            '''
            result = self._values.get("secret_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksSecretProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.EksVolumeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "empty_dir": "emptyDir",
            "host_path": "hostPath",
            "name": "name",
            "persistent_volume_claim": "persistentVolumeClaim",
            "secret": "secret",
        },
    )
    class EksVolumeProperty:
        def __init__(
            self,
            *,
            empty_dir: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.EmptyDirProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            host_path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.HostPathProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
            persistent_volume_claim: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.EksPersistentVolumeClaimProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secret: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.EksSecretProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies an Amazon EKS volume for a job definition.

            :param empty_dir: Specifies the configuration of a Kubernetes ``emptyDir`` volume. For more information, see `emptyDir <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/#emptydir>`_ in the *Kubernetes documentation* .
            :param host_path: Specifies the configuration of a Kubernetes ``hostPath`` volume. For more information, see `hostPath <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/#hostpath>`_ in the *Kubernetes documentation* .
            :param name: The name of the volume. The name must be allowed as a DNS subdomain name. For more information, see `DNS subdomain names <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-subdomain-names>`_ in the *Kubernetes documentation* .
            :param persistent_volume_claim: Specifies the configuration of a Kubernetes ``persistentVolumeClaim`` bounded to a ``persistentVolume`` . For more information, see `Persistent Volume Claims <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims>`_ in the *Kubernetes documentation* .
            :param secret: Specifies the configuration of a Kubernetes ``secret`` volume. For more information, see `secret <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/#secret>`_ in the *Kubernetes documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-eksvolume.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                eks_volume_property = batch_mixins.CfnJobDefinitionPropsMixin.EksVolumeProperty(
                    empty_dir=batch_mixins.CfnJobDefinitionPropsMixin.EmptyDirProperty(
                        medium="medium",
                        size_limit="sizeLimit"
                    ),
                    host_path=batch_mixins.CfnJobDefinitionPropsMixin.HostPathProperty(
                        path="path"
                    ),
                    name="name",
                    persistent_volume_claim=batch_mixins.CfnJobDefinitionPropsMixin.EksPersistentVolumeClaimProperty(
                        claim_name="claimName",
                        read_only=False
                    ),
                    secret=batch_mixins.CfnJobDefinitionPropsMixin.EksSecretProperty(
                        optional=False,
                        secret_name="secretName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd520e3b0ecc3777227351e91ec59155949c3f92d933526a7138062b041f5f22)
                check_type(argname="argument empty_dir", value=empty_dir, expected_type=type_hints["empty_dir"])
                check_type(argname="argument host_path", value=host_path, expected_type=type_hints["host_path"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument persistent_volume_claim", value=persistent_volume_claim, expected_type=type_hints["persistent_volume_claim"])
                check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if empty_dir is not None:
                self._values["empty_dir"] = empty_dir
            if host_path is not None:
                self._values["host_path"] = host_path
            if name is not None:
                self._values["name"] = name
            if persistent_volume_claim is not None:
                self._values["persistent_volume_claim"] = persistent_volume_claim
            if secret is not None:
                self._values["secret"] = secret

        @builtins.property
        def empty_dir(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EmptyDirProperty"]]:
            '''Specifies the configuration of a Kubernetes ``emptyDir`` volume.

            For more information, see `emptyDir <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/#emptydir>`_ in the *Kubernetes documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-eksvolume.html#cfn-batch-jobdefinition-eksvolume-emptydir
            '''
            result = self._values.get("empty_dir")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EmptyDirProperty"]], result)

        @builtins.property
        def host_path(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.HostPathProperty"]]:
            '''Specifies the configuration of a Kubernetes ``hostPath`` volume.

            For more information, see `hostPath <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/#hostpath>`_ in the *Kubernetes documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-eksvolume.html#cfn-batch-jobdefinition-eksvolume-hostpath
            '''
            result = self._values.get("host_path")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.HostPathProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the volume.

            The name must be allowed as a DNS subdomain name. For more information, see `DNS subdomain names <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-subdomain-names>`_ in the *Kubernetes documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-eksvolume.html#cfn-batch-jobdefinition-eksvolume-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def persistent_volume_claim(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EksPersistentVolumeClaimProperty"]]:
            '''Specifies the configuration of a Kubernetes ``persistentVolumeClaim`` bounded to a ``persistentVolume`` .

            For more information, see `Persistent Volume Claims <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims>`_ in the *Kubernetes documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-eksvolume.html#cfn-batch-jobdefinition-eksvolume-persistentvolumeclaim
            '''
            result = self._values.get("persistent_volume_claim")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EksPersistentVolumeClaimProperty"]], result)

        @builtins.property
        def secret(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EksSecretProperty"]]:
            '''Specifies the configuration of a Kubernetes ``secret`` volume.

            For more information, see `secret <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/#secret>`_ in the *Kubernetes documentation* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-eksvolume.html#cfn-batch-jobdefinition-eksvolume-secret
            '''
            result = self._values.get("secret")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EksSecretProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksVolumeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.EmptyDirProperty",
        jsii_struct_bases=[],
        name_mapping={"medium": "medium", "size_limit": "sizeLimit"},
    )
    class EmptyDirProperty:
        def __init__(
            self,
            *,
            medium: typing.Optional[builtins.str] = None,
            size_limit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param medium: 
            :param size_limit: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-emptydir.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                empty_dir_property = batch_mixins.CfnJobDefinitionPropsMixin.EmptyDirProperty(
                    medium="medium",
                    size_limit="sizeLimit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0b9c3903e7935a21888e1cc782db905a24604b669b5924f4107e00a0cad11903)
                check_type(argname="argument medium", value=medium, expected_type=type_hints["medium"])
                check_type(argname="argument size_limit", value=size_limit, expected_type=type_hints["size_limit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if medium is not None:
                self._values["medium"] = medium
            if size_limit is not None:
                self._values["size_limit"] = size_limit

        @builtins.property
        def medium(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-emptydir.html#cfn-batch-jobdefinition-emptydir-medium
            '''
            result = self._values.get("medium")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def size_limit(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-emptydir.html#cfn-batch-jobdefinition-emptydir-sizelimit
            '''
            result = self._values.get("size_limit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EmptyDirProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.EnvironmentProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class EnvironmentProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Environment property type specifies environment variables to use in a job definition.

            :param name: The name of the environment variable.
            :param value: The value of the environment variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-environment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                environment_property = batch_mixins.CfnJobDefinitionPropsMixin.EnvironmentProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__36b6ac57ce0cdbe7ed0745bffc7a57f8fcdfe7d7e8e986e96d6bb73ed3436a6e)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the environment variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-environment.html#cfn-batch-jobdefinition-environment-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the environment variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-environment.html#cfn-batch-jobdefinition-environment-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.EphemeralStorageProperty",
        jsii_struct_bases=[],
        name_mapping={"size_in_gib": "sizeInGiB"},
    )
    class EphemeralStorageProperty:
        def __init__(self, *, size_in_gib: typing.Optional[jsii.Number] = None) -> None:
            '''The amount of ephemeral storage to allocate for the task.

            This parameter is used to expand the total amount of ephemeral storage available, beyond the default amount, for tasks hosted on AWS Fargate .

            :param size_in_gib: The total amount, in GiB, of ephemeral storage to set for the task. The minimum supported value is ``21`` GiB and the maximum supported value is ``200`` GiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ephemeralstorage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                ephemeral_storage_property = batch_mixins.CfnJobDefinitionPropsMixin.EphemeralStorageProperty(
                    size_in_gi_b=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b6251e67d1c65a706a864fa6e924eb8a136900755eab8755d6d3e8eeb998e0d0)
                check_type(argname="argument size_in_gib", value=size_in_gib, expected_type=type_hints["size_in_gib"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if size_in_gib is not None:
                self._values["size_in_gib"] = size_in_gib

        @builtins.property
        def size_in_gib(self) -> typing.Optional[jsii.Number]:
            '''The total amount, in GiB, of ephemeral storage to set for the task.

            The minimum supported value is ``21`` GiB and the maximum supported value is ``200`` GiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ephemeralstorage.html#cfn-batch-jobdefinition-ephemeralstorage-sizeingib
            '''
            result = self._values.get("size_in_gib")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EphemeralStorageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.EvaluateOnExitProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "on_exit_code": "onExitCode",
            "on_reason": "onReason",
            "on_status_reason": "onStatusReason",
        },
    )
    class EvaluateOnExitProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            on_exit_code: typing.Optional[builtins.str] = None,
            on_reason: typing.Optional[builtins.str] = None,
            on_status_reason: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an array of up to 5 conditions to be met, and an action to take ( ``RETRY`` or ``EXIT`` ) if all conditions are met.

            If none of the ``EvaluateOnExit`` conditions in a ``RetryStrategy`` match, then the job is retried.

            :param action: Specifies the action to take if all of the specified conditions ( ``onStatusReason`` , ``onReason`` , and ``onExitCode`` ) are met. The values aren't case sensitive.
            :param on_exit_code: Contains a glob pattern to match against the decimal representation of the ``ExitCode`` returned for a job. The pattern can be up to 512 characters long. It can contain only numbers, and can end with an asterisk (*) so that only the start of the string needs to be an exact match. The string can contain up to 512 characters.
            :param on_reason: Contains a glob pattern to match against the ``Reason`` returned for a job. The pattern can contain up to 512 characters. It can contain letters, numbers, periods (.), colons (:), and white space (including spaces and tabs). It can optionally end with an asterisk (*) so that only the start of the string needs to be an exact match.
            :param on_status_reason: Contains a glob pattern to match against the ``StatusReason`` returned for a job. The pattern can contain up to 512 characters. It can contain letters, numbers, periods (.), colons (:), and white spaces (including spaces or tabs). It can optionally end with an asterisk (*) so that only the start of the string needs to be an exact match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-evaluateonexit.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                evaluate_on_exit_property = batch_mixins.CfnJobDefinitionPropsMixin.EvaluateOnExitProperty(
                    action="action",
                    on_exit_code="onExitCode",
                    on_reason="onReason",
                    on_status_reason="onStatusReason"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__180ea3fbfb4a0b9b2dac0e30999d723bf15508e980e3e0cdb6e59e9339afd2dd)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument on_exit_code", value=on_exit_code, expected_type=type_hints["on_exit_code"])
                check_type(argname="argument on_reason", value=on_reason, expected_type=type_hints["on_reason"])
                check_type(argname="argument on_status_reason", value=on_status_reason, expected_type=type_hints["on_status_reason"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if on_exit_code is not None:
                self._values["on_exit_code"] = on_exit_code
            if on_reason is not None:
                self._values["on_reason"] = on_reason
            if on_status_reason is not None:
                self._values["on_status_reason"] = on_status_reason

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''Specifies the action to take if all of the specified conditions ( ``onStatusReason`` , ``onReason`` , and ``onExitCode`` ) are met.

            The values aren't case sensitive.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-evaluateonexit.html#cfn-batch-jobdefinition-evaluateonexit-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def on_exit_code(self) -> typing.Optional[builtins.str]:
            '''Contains a glob pattern to match against the decimal representation of the ``ExitCode`` returned for a job.

            The pattern can be up to 512 characters long. It can contain only numbers, and can end with an asterisk (*) so that only the start of the string needs to be an exact match.

            The string can contain up to 512 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-evaluateonexit.html#cfn-batch-jobdefinition-evaluateonexit-onexitcode
            '''
            result = self._values.get("on_exit_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def on_reason(self) -> typing.Optional[builtins.str]:
            '''Contains a glob pattern to match against the ``Reason`` returned for a job.

            The pattern can contain up to 512 characters. It can contain letters, numbers, periods (.), colons (:), and white space (including spaces and tabs). It can optionally end with an asterisk (*) so that only the start of the string needs to be an exact match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-evaluateonexit.html#cfn-batch-jobdefinition-evaluateonexit-onreason
            '''
            result = self._values.get("on_reason")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def on_status_reason(self) -> typing.Optional[builtins.str]:
            '''Contains a glob pattern to match against the ``StatusReason`` returned for a job.

            The pattern can contain up to 512 characters. It can contain letters, numbers, periods (.), colons (:), and white spaces (including spaces or tabs). It can optionally end with an asterisk (*) so that only the start of the string needs to be an exact match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-evaluateonexit.html#cfn-batch-jobdefinition-evaluateonexit-onstatusreason
            '''
            result = self._values.get("on_status_reason")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluateOnExitProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.FargatePlatformConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"platform_version": "platformVersion"},
    )
    class FargatePlatformConfigurationProperty:
        def __init__(
            self,
            *,
            platform_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The platform configuration for jobs that are running on Fargate resources.

            Jobs that run on Amazon EC2 resources must not specify this parameter.

            :param platform_version: The AWS Fargate platform version where the jobs are running. A platform version is specified only for jobs that are running on Fargate resources. If one isn't specified, the ``LATEST`` platform version is used by default. This uses a recent, approved version of the AWS Fargate platform for compute resources. For more information, see `AWS Fargate platform versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-fargateplatformconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                fargate_platform_configuration_property = batch_mixins.CfnJobDefinitionPropsMixin.FargatePlatformConfigurationProperty(
                    platform_version="platformVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3d01259e640cadebf4b4c451149db92ac8ab6de1356a43a69e22406ae5350f50)
                check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if platform_version is not None:
                self._values["platform_version"] = platform_version

        @builtins.property
        def platform_version(self) -> typing.Optional[builtins.str]:
            '''The AWS Fargate platform version where the jobs are running.

            A platform version is specified only for jobs that are running on Fargate resources. If one isn't specified, the ``LATEST`` platform version is used by default. This uses a recent, approved version of the AWS Fargate platform for compute resources. For more information, see `AWS Fargate platform versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-fargateplatformconfiguration.html#cfn-batch-jobdefinition-fargateplatformconfiguration-platformversion
            '''
            result = self._values.get("platform_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FargatePlatformConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.FirelensConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"options": "options", "type": "type"},
    )
    class FirelensConfigurationProperty:
        def __init__(
            self,
            *,
            options: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The FireLens configuration for the container.

            This is used to specify and configure a log router for container logs. For more information, see `Custom log <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_firelens.html>`_ routing in the *Amazon Elastic Container Service Developer Guide* .

            :param options: The options to use when configuring the log router. This field is optional and can be used to specify a custom configuration file or to add additional metadata, such as the task, task definition, cluster, and container instance details to the log event. If specified, the syntax to use is ``"options":{"enable-ecs-log-metadata":"true|false","config-file-type:"s3|file","config-file-value":"arn:aws:s3:::mybucket/fluent.conf|filepath"}`` . For more information, see `Creating a task definition that uses a FireLens configuration <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_firelens.html#firelens-taskdef>`_ in the *Amazon Elastic Container Service Developer Guide* .
            :param type: The log router to use. The valid values are ``fluentd`` or ``fluentbit`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-firelensconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                firelens_configuration_property = batch_mixins.CfnJobDefinitionPropsMixin.FirelensConfigurationProperty(
                    options={
                        "options_key": "options"
                    },
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__51ce8c2dbc249874b77d6b580d43812f54abd89cbe980af6dd07921d89aa707b)
                check_type(argname="argument options", value=options, expected_type=type_hints["options"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if options is not None:
                self._values["options"] = options
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def options(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The options to use when configuring the log router.

            This field is optional and can be used to specify a custom configuration file or to add additional metadata, such as the task, task definition, cluster, and container instance details to the log event. If specified, the syntax to use is ``"options":{"enable-ecs-log-metadata":"true|false","config-file-type:"s3|file","config-file-value":"arn:aws:s3:::mybucket/fluent.conf|filepath"}`` . For more information, see `Creating a task definition that uses a FireLens configuration <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_firelens.html#firelens-taskdef>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-firelensconfiguration.html#cfn-batch-jobdefinition-firelensconfiguration-options
            '''
            result = self._values.get("options")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The log router to use.

            The valid values are ``fluentd`` or ``fluentbit`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-firelensconfiguration.html#cfn-batch-jobdefinition-firelensconfiguration-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FirelensConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.HostPathProperty",
        jsii_struct_bases=[],
        name_mapping={"path": "path"},
    )
    class HostPathProperty:
        def __init__(self, *, path: typing.Optional[builtins.str] = None) -> None:
            '''
            :param path: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-hostpath.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                host_path_property = batch_mixins.CfnJobDefinitionPropsMixin.HostPathProperty(
                    path="path"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4540d0994e62cb27e31ea48fb7bdbcf193de5b11a395b4f9ea687cf7524f19b2)
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if path is not None:
                self._values["path"] = path

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-hostpath.html#cfn-batch-jobdefinition-hostpath-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HostPathProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.ImagePullSecretProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class ImagePullSecretProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''References a Kubernetes secret resource.

            This name of the secret must start and end with an alphanumeric character, is required to be lowercase, can include periods (.) and hyphens (-), and can't contain more than 253 characters.

            :param name: Provides a unique identifier for the ``ImagePullSecret`` . This object is required when ``EksPodProperties$imagePullSecrets`` is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-imagepullsecret.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                image_pull_secret_property = batch_mixins.CfnJobDefinitionPropsMixin.ImagePullSecretProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e76f6b9abdfac95ed04151b59d888438effa81f5cce07fd6faea855f76b330af)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Provides a unique identifier for the ``ImagePullSecret`` .

            This object is required when ``EksPodProperties$imagePullSecrets`` is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-imagepullsecret.html#cfn-batch-jobdefinition-imagepullsecret-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImagePullSecretProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.JobTimeoutProperty",
        jsii_struct_bases=[],
        name_mapping={"attempt_duration_seconds": "attemptDurationSeconds"},
    )
    class JobTimeoutProperty:
        def __init__(
            self,
            *,
            attempt_duration_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that represents a job timeout configuration.

            :param attempt_duration_seconds: The job timeout time (in seconds) that's measured from the job attempt's ``startedAt`` timestamp. After this time passes, AWS Batch terminates your jobs if they aren't finished. The minimum value for the timeout is 60 seconds. For array jobs, the timeout applies to the child jobs, not to the parent array job. For multi-node parallel (MNP) jobs, the timeout applies to the whole job, not to the individual nodes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-jobtimeout.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                job_timeout_property = batch_mixins.CfnJobDefinitionPropsMixin.JobTimeoutProperty(
                    attempt_duration_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__807d7b4536f4dc63e0b69ba851801e70b5d4ae665fdb1523490e5cb69cfbe965)
                check_type(argname="argument attempt_duration_seconds", value=attempt_duration_seconds, expected_type=type_hints["attempt_duration_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attempt_duration_seconds is not None:
                self._values["attempt_duration_seconds"] = attempt_duration_seconds

        @builtins.property
        def attempt_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''The job timeout time (in seconds) that's measured from the job attempt's ``startedAt`` timestamp.

            After this time passes, AWS Batch terminates your jobs if they aren't finished. The minimum value for the timeout is 60 seconds.

            For array jobs, the timeout applies to the child jobs, not to the parent array job.

            For multi-node parallel (MNP) jobs, the timeout applies to the whole job, not to the individual nodes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-jobtimeout.html#cfn-batch-jobdefinition-jobtimeout-attemptdurationseconds
            '''
            result = self._values.get("attempt_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JobTimeoutProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.LinuxParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "devices": "devices",
            "init_process_enabled": "initProcessEnabled",
            "max_swap": "maxSwap",
            "shared_memory_size": "sharedMemorySize",
            "swappiness": "swappiness",
            "tmpfs": "tmpfs",
        },
    )
    class LinuxParametersProperty:
        def __init__(
            self,
            *,
            devices: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.DeviceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            init_process_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            max_swap: typing.Optional[jsii.Number] = None,
            shared_memory_size: typing.Optional[jsii.Number] = None,
            swappiness: typing.Optional[jsii.Number] = None,
            tmpfs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.TmpfsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Linux-specific modifications that are applied to the container, such as details for device mappings.

            :param devices: Any of the host devices to expose to the container. This parameter maps to ``Devices`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--device`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't provide it for these jobs.
            :param init_process_enabled: If true, run an ``init`` process inside the container that forwards signals and reaps processes. This parameter maps to the ``--init`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . This parameter requires version 1.25 of the Docker Remote API or greater on your container instance. To check the Docker Remote API version on your container instance, log in to your container instance and run the following command: ``sudo docker version | grep "Server API version"``
            :param max_swap: The total amount of swap memory (in MiB) a container can use. This parameter is translated to the ``--memory-swap`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ where the value is the sum of the container memory plus the ``maxSwap`` value. For more information, see ```--memory-swap`` details <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/resource_constraints/#--memory-swap-details>`_ in the Docker documentation. If a ``maxSwap`` value of ``0`` is specified, the container doesn't use swap. Accepted values are ``0`` or any positive integer. If the ``maxSwap`` parameter is omitted, the container doesn't use the swap configuration for the container instance on which it runs. A ``maxSwap`` value must be set for the ``swappiness`` parameter to be used. .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't provide it for these jobs.
            :param shared_memory_size: The value for the size (in MiB) of the ``/dev/shm`` volume. This parameter maps to the ``--shm-size`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't provide it for these jobs.
            :param swappiness: You can use this parameter to tune a container's memory swappiness behavior. A ``swappiness`` value of ``0`` causes swapping to not occur unless absolutely necessary. A ``swappiness`` value of ``100`` causes pages to be swapped aggressively. Valid values are whole numbers between ``0`` and ``100`` . If the ``swappiness`` parameter isn't specified, a default value of ``60`` is used. If a value isn't specified for ``maxSwap`` , then this parameter is ignored. If ``maxSwap`` is set to 0, the container doesn't use swap. This parameter maps to the ``--memory-swappiness`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . Consider the following when you use a per-container swap configuration. - Swap space must be enabled and allocated on the container instance for the containers to use. .. epigraph:: By default, the Amazon ECS optimized AMIs don't have swap enabled. You must enable swap on the instance to use this feature. For more information, see `Instance store swap volumes <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-store-swap-volumes.html>`_ in the *Amazon EC2 User Guide for Linux Instances* or `How do I allocate memory to work as swap space in an Amazon EC2 instance by using a swap file? <https://docs.aws.amazon.com/premiumsupport/knowledge-center/ec2-memory-swap-file/>`_ - The swap space parameters are only supported for job definitions using EC2 resources. - If the ``maxSwap`` and ``swappiness`` parameters are omitted from a job definition, each container has a default ``swappiness`` value of 60. Moreover, the total swap usage is limited to two times the memory reservation of the container. .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't provide it for these jobs.
            :param tmpfs: The container path, mount options, and size (in MiB) of the ``tmpfs`` mount. This parameter maps to the ``--tmpfs`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't provide this parameter for this resource type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-linuxparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                linux_parameters_property = batch_mixins.CfnJobDefinitionPropsMixin.LinuxParametersProperty(
                    devices=[batch_mixins.CfnJobDefinitionPropsMixin.DeviceProperty(
                        container_path="containerPath",
                        host_path="hostPath",
                        permissions=["permissions"]
                    )],
                    init_process_enabled=False,
                    max_swap=123,
                    shared_memory_size=123,
                    swappiness=123,
                    tmpfs=[batch_mixins.CfnJobDefinitionPropsMixin.TmpfsProperty(
                        container_path="containerPath",
                        mount_options=["mountOptions"],
                        size=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a8ca7df82403669c12cf396698dd4d31318baa72a3d8e2ad1135ed49c726577)
                check_type(argname="argument devices", value=devices, expected_type=type_hints["devices"])
                check_type(argname="argument init_process_enabled", value=init_process_enabled, expected_type=type_hints["init_process_enabled"])
                check_type(argname="argument max_swap", value=max_swap, expected_type=type_hints["max_swap"])
                check_type(argname="argument shared_memory_size", value=shared_memory_size, expected_type=type_hints["shared_memory_size"])
                check_type(argname="argument swappiness", value=swappiness, expected_type=type_hints["swappiness"])
                check_type(argname="argument tmpfs", value=tmpfs, expected_type=type_hints["tmpfs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if devices is not None:
                self._values["devices"] = devices
            if init_process_enabled is not None:
                self._values["init_process_enabled"] = init_process_enabled
            if max_swap is not None:
                self._values["max_swap"] = max_swap
            if shared_memory_size is not None:
                self._values["shared_memory_size"] = shared_memory_size
            if swappiness is not None:
                self._values["swappiness"] = swappiness
            if tmpfs is not None:
                self._values["tmpfs"] = tmpfs

        @builtins.property
        def devices(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.DeviceProperty"]]]]:
            '''Any of the host devices to expose to the container.

            This parameter maps to ``Devices`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--device`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't provide it for these jobs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-linuxparameters.html#cfn-batch-jobdefinition-linuxparameters-devices
            '''
            result = self._values.get("devices")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.DeviceProperty"]]]], result)

        @builtins.property
        def init_process_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If true, run an ``init`` process inside the container that forwards signals and reaps processes.

            This parameter maps to the ``--init`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . This parameter requires version 1.25 of the Docker Remote API or greater on your container instance. To check the Docker Remote API version on your container instance, log in to your container instance and run the following command: ``sudo docker version | grep "Server API version"``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-linuxparameters.html#cfn-batch-jobdefinition-linuxparameters-initprocessenabled
            '''
            result = self._values.get("init_process_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def max_swap(self) -> typing.Optional[jsii.Number]:
            '''The total amount of swap memory (in MiB) a container can use.

            This parameter is translated to the ``--memory-swap`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ where the value is the sum of the container memory plus the ``maxSwap`` value. For more information, see ```--memory-swap`` details <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/resource_constraints/#--memory-swap-details>`_ in the Docker documentation.

            If a ``maxSwap`` value of ``0`` is specified, the container doesn't use swap. Accepted values are ``0`` or any positive integer. If the ``maxSwap`` parameter is omitted, the container doesn't use the swap configuration for the container instance on which it runs. A ``maxSwap`` value must be set for the ``swappiness`` parameter to be used.
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't provide it for these jobs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-linuxparameters.html#cfn-batch-jobdefinition-linuxparameters-maxswap
            '''
            result = self._values.get("max_swap")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def shared_memory_size(self) -> typing.Optional[jsii.Number]:
            '''The value for the size (in MiB) of the ``/dev/shm`` volume.

            This parameter maps to the ``--shm-size`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't provide it for these jobs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-linuxparameters.html#cfn-batch-jobdefinition-linuxparameters-sharedmemorysize
            '''
            result = self._values.get("shared_memory_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def swappiness(self) -> typing.Optional[jsii.Number]:
            '''You can use this parameter to tune a container's memory swappiness behavior.

            A ``swappiness`` value of ``0`` causes swapping to not occur unless absolutely necessary. A ``swappiness`` value of ``100`` causes pages to be swapped aggressively. Valid values are whole numbers between ``0`` and ``100`` . If the ``swappiness`` parameter isn't specified, a default value of ``60`` is used. If a value isn't specified for ``maxSwap`` , then this parameter is ignored. If ``maxSwap`` is set to 0, the container doesn't use swap. This parameter maps to the ``--memory-swappiness`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .

            Consider the following when you use a per-container swap configuration.

            - Swap space must be enabled and allocated on the container instance for the containers to use.

            .. epigraph::

               By default, the Amazon ECS optimized AMIs don't have swap enabled. You must enable swap on the instance to use this feature. For more information, see `Instance store swap volumes <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-store-swap-volumes.html>`_ in the *Amazon EC2 User Guide for Linux Instances* or `How do I allocate memory to work as swap space in an Amazon EC2 instance by using a swap file? <https://docs.aws.amazon.com/premiumsupport/knowledge-center/ec2-memory-swap-file/>`_

            - The swap space parameters are only supported for job definitions using EC2 resources.
            - If the ``maxSwap`` and ``swappiness`` parameters are omitted from a job definition, each container has a default ``swappiness`` value of 60. Moreover, the total swap usage is limited to two times the memory reservation of the container.

            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't provide it for these jobs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-linuxparameters.html#cfn-batch-jobdefinition-linuxparameters-swappiness
            '''
            result = self._values.get("swappiness")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def tmpfs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.TmpfsProperty"]]]]:
            '''The container path, mount options, and size (in MiB) of the ``tmpfs`` mount.

            This parameter maps to the ``--tmpfs`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't provide this parameter for this resource type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-linuxparameters.html#cfn-batch-jobdefinition-linuxparameters-tmpfs
            '''
            result = self._values.get("tmpfs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.TmpfsProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LinuxParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.LogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "log_driver": "logDriver",
            "options": "options",
            "secret_options": "secretOptions",
        },
    )
    class LogConfigurationProperty:
        def __init__(
            self,
            *,
            log_driver: typing.Optional[builtins.str] = None,
            options: typing.Any = None,
            secret_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.SecretProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Log configuration options to send to a custom log driver for the container.

            :param log_driver: The log driver to use for the container. The valid values that are listed for this parameter are log drivers that the Amazon ECS container agent can communicate with by default. The supported log drivers are ``awsfirelens`` , ``awslogs`` , ``fluentd`` , ``gelf`` , ``json-file`` , ``journald`` , ``logentries`` , ``syslog`` , and ``splunk`` . .. epigraph:: Jobs that are running on Fargate resources are restricted to the ``awslogs`` and ``splunk`` log drivers. - **awsfirelens** - Specifies the firelens logging driver. For more information on configuring Firelens, see `Send Amazon ECS logs to an AWS service or AWS Partner <https://docs.aws.amazon.com//AmazonECS/latest/developerguide/using_firelens.html>`_ in the *Amazon Elastic Container Service Developer Guide* . - **awslogs** - Specifies the Amazon CloudWatch Logs logging driver. For more information, see `Using the awslogs log driver <https://docs.aws.amazon.com/batch/latest/userguide/using_awslogs.html>`_ in the *AWS Batch User Guide* and `Amazon CloudWatch Logs logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/awslogs/>`_ in the Docker documentation. - **fluentd** - Specifies the Fluentd logging driver. For more information including usage and options, see `Fluentd logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/fluentd/>`_ in the *Docker documentation* . - **gelf** - Specifies the Graylog Extended Format (GELF) logging driver. For more information including usage and options, see `Graylog Extended Format logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/gelf/>`_ in the *Docker documentation* . - **journald** - Specifies the journald logging driver. For more information including usage and options, see `Journald logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/journald/>`_ in the *Docker documentation* . - **json-file** - Specifies the JSON file logging driver. For more information including usage and options, see `JSON File logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/json-file/>`_ in the *Docker documentation* . - **splunk** - Specifies the Splunk logging driver. For more information including usage and options, see `Splunk logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/splunk/>`_ in the *Docker documentation* . - **syslog** - Specifies the syslog logging driver. For more information including usage and options, see `Syslog logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/syslog/>`_ in the *Docker documentation* . .. epigraph:: If you have a custom driver that's not listed earlier that you want to work with the Amazon ECS container agent, you can fork the Amazon ECS container agent project that's `available on GitHub <https://docs.aws.amazon.com/https://github.com/aws/amazon-ecs-agent>`_ and customize it to work with that driver. We encourage you to submit pull requests for changes that you want to have included. However, Amazon Web Services doesn't currently support running modified copies of this software. This parameter requires version 1.18 of the Docker Remote API or greater on your container instance. To check the Docker Remote API version on your container instance, log in to your container instance and run the following command: ``sudo docker version | grep "Server API version"``
            :param options: The configuration options to send to the log driver. This parameter requires version 1.19 of the Docker Remote API or greater on your container instance. To check the Docker Remote API version on your container instance, log in to your container instance and run the following command: ``sudo docker version | grep "Server API version"``
            :param secret_options: The secrets to pass to the log configuration. For more information, see `Specifying sensitive data <https://docs.aws.amazon.com/batch/latest/userguide/specifying-sensitive-data.html>`_ in the *AWS Batch User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-logconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                # options: Any
                
                log_configuration_property = batch_mixins.CfnJobDefinitionPropsMixin.LogConfigurationProperty(
                    log_driver="logDriver",
                    options=options,
                    secret_options=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                        name="name",
                        value_from="valueFrom"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bcbc658088bd56e9e53fc9c5536e1d4150231ba5f4e7175dcdedc83b0941c430)
                check_type(argname="argument log_driver", value=log_driver, expected_type=type_hints["log_driver"])
                check_type(argname="argument options", value=options, expected_type=type_hints["options"])
                check_type(argname="argument secret_options", value=secret_options, expected_type=type_hints["secret_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_driver is not None:
                self._values["log_driver"] = log_driver
            if options is not None:
                self._values["options"] = options
            if secret_options is not None:
                self._values["secret_options"] = secret_options

        @builtins.property
        def log_driver(self) -> typing.Optional[builtins.str]:
            '''The log driver to use for the container.

            The valid values that are listed for this parameter are log drivers that the Amazon ECS container agent can communicate with by default.

            The supported log drivers are ``awsfirelens`` , ``awslogs`` , ``fluentd`` , ``gelf`` , ``json-file`` , ``journald`` , ``logentries`` , ``syslog`` , and ``splunk`` .
            .. epigraph::

               Jobs that are running on Fargate resources are restricted to the ``awslogs`` and ``splunk`` log drivers.

            - **awsfirelens** - Specifies the firelens logging driver. For more information on configuring Firelens, see `Send Amazon ECS logs to an AWS service or AWS Partner <https://docs.aws.amazon.com//AmazonECS/latest/developerguide/using_firelens.html>`_ in the *Amazon Elastic Container Service Developer Guide* .
            - **awslogs** - Specifies the Amazon CloudWatch Logs logging driver. For more information, see `Using the awslogs log driver <https://docs.aws.amazon.com/batch/latest/userguide/using_awslogs.html>`_ in the *AWS Batch User Guide* and `Amazon CloudWatch Logs logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/awslogs/>`_ in the Docker documentation.
            - **fluentd** - Specifies the Fluentd logging driver. For more information including usage and options, see `Fluentd logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/fluentd/>`_ in the *Docker documentation* .
            - **gelf** - Specifies the Graylog Extended Format (GELF) logging driver. For more information including usage and options, see `Graylog Extended Format logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/gelf/>`_ in the *Docker documentation* .
            - **journald** - Specifies the journald logging driver. For more information including usage and options, see `Journald logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/journald/>`_ in the *Docker documentation* .
            - **json-file** - Specifies the JSON file logging driver. For more information including usage and options, see `JSON File logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/json-file/>`_ in the *Docker documentation* .
            - **splunk** - Specifies the Splunk logging driver. For more information including usage and options, see `Splunk logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/splunk/>`_ in the *Docker documentation* .
            - **syslog** - Specifies the syslog logging driver. For more information including usage and options, see `Syslog logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/syslog/>`_ in the *Docker documentation* .

            .. epigraph::

               If you have a custom driver that's not listed earlier that you want to work with the Amazon ECS container agent, you can fork the Amazon ECS container agent project that's `available on GitHub <https://docs.aws.amazon.com/https://github.com/aws/amazon-ecs-agent>`_ and customize it to work with that driver. We encourage you to submit pull requests for changes that you want to have included. However, Amazon Web Services doesn't currently support running modified copies of this software.

            This parameter requires version 1.18 of the Docker Remote API or greater on your container instance. To check the Docker Remote API version on your container instance, log in to your container instance and run the following command: ``sudo docker version | grep "Server API version"``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-logconfiguration.html#cfn-batch-jobdefinition-logconfiguration-logdriver
            '''
            result = self._values.get("log_driver")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def options(self) -> typing.Any:
            '''The configuration options to send to the log driver.

            This parameter requires version 1.19 of the Docker Remote API or greater on your container instance. To check the Docker Remote API version on your container instance, log in to your container instance and run the following command: ``sudo docker version | grep "Server API version"``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-logconfiguration.html#cfn-batch-jobdefinition-logconfiguration-options
            '''
            result = self._values.get("options")
            return typing.cast(typing.Any, result)

        @builtins.property
        def secret_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.SecretProperty"]]]]:
            '''The secrets to pass to the log configuration.

            For more information, see `Specifying sensitive data <https://docs.aws.amazon.com/batch/latest/userguide/specifying-sensitive-data.html>`_ in the *AWS Batch User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-logconfiguration.html#cfn-batch-jobdefinition-logconfiguration-secretoptions
            '''
            result = self._values.get("secret_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.SecretProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.MetadataProperty",
        jsii_struct_bases=[],
        name_mapping={"labels": "labels"},
    )
    class MetadataProperty:
        def __init__(self, *, labels: typing.Any = None) -> None:
            '''
            :param labels: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-metadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                # labels: Any
                
                metadata_property = batch_mixins.CfnJobDefinitionPropsMixin.MetadataProperty(
                    labels=labels
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4852fa6a00e41662c659e430b8dfe1e2f0c25f72cf8739c1ed6e342d8df46191)
                check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if labels is not None:
                self._values["labels"] = labels

        @builtins.property
        def labels(self) -> typing.Any:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-metadata.html#cfn-batch-jobdefinition-metadata-labels
            '''
            result = self._values.get("labels")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.MountPointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "container_path": "containerPath",
            "read_only": "readOnly",
            "source_volume": "sourceVolume",
        },
    )
    class MountPointProperty:
        def __init__(
            self,
            *,
            container_path: typing.Optional[builtins.str] = None,
            read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            source_volume: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Details for a Docker volume mount point that's used in a job's container properties.

            This parameter maps to ``Volumes`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.43/#tag/Container/operation/ContainerCreate>`_ section of the *Docker Remote API* and the ``--volume`` option to docker run.

            :param container_path: The path on the container where the host volume is mounted.
            :param read_only: If this value is ``true`` , the container has read-only access to the volume. Otherwise, the container can write to the volume. The default value is ``false`` .
            :param source_volume: The name of the volume to mount.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-mountpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                mount_point_property = batch_mixins.CfnJobDefinitionPropsMixin.MountPointProperty(
                    container_path="containerPath",
                    read_only=False,
                    source_volume="sourceVolume"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8f9b359a15f63a066ad1e7d5fde3c616cce63d4cab9ecd6371a09c3b5f714991)
                check_type(argname="argument container_path", value=container_path, expected_type=type_hints["container_path"])
                check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
                check_type(argname="argument source_volume", value=source_volume, expected_type=type_hints["source_volume"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if container_path is not None:
                self._values["container_path"] = container_path
            if read_only is not None:
                self._values["read_only"] = read_only
            if source_volume is not None:
                self._values["source_volume"] = source_volume

        @builtins.property
        def container_path(self) -> typing.Optional[builtins.str]:
            '''The path on the container where the host volume is mounted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-mountpoint.html#cfn-batch-jobdefinition-mountpoint-containerpath
            '''
            result = self._values.get("container_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def read_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If this value is ``true`` , the container has read-only access to the volume.

            Otherwise, the container can write to the volume. The default value is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-mountpoint.html#cfn-batch-jobdefinition-mountpoint-readonly
            '''
            result = self._values.get("read_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def source_volume(self) -> typing.Optional[builtins.str]:
            '''The name of the volume to mount.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-mountpoint.html#cfn-batch-jobdefinition-mountpoint-sourcevolume
            '''
            result = self._values.get("source_volume")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MountPointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.MountPointsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "container_path": "containerPath",
            "read_only": "readOnly",
            "source_volume": "sourceVolume",
        },
    )
    class MountPointsProperty:
        def __init__(
            self,
            *,
            container_path: typing.Optional[builtins.str] = None,
            read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            source_volume: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param container_path: 
            :param read_only: 
            :param source_volume: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-mountpoints.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                mount_points_property = batch_mixins.CfnJobDefinitionPropsMixin.MountPointsProperty(
                    container_path="containerPath",
                    read_only=False,
                    source_volume="sourceVolume"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2f233857cc8a563bd7bedc5306a2d26c8cf217bca9bb0a69faf227d5a888748a)
                check_type(argname="argument container_path", value=container_path, expected_type=type_hints["container_path"])
                check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
                check_type(argname="argument source_volume", value=source_volume, expected_type=type_hints["source_volume"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if container_path is not None:
                self._values["container_path"] = container_path
            if read_only is not None:
                self._values["read_only"] = read_only
            if source_volume is not None:
                self._values["source_volume"] = source_volume

        @builtins.property
        def container_path(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-mountpoints.html#cfn-batch-jobdefinition-mountpoints-containerpath
            '''
            result = self._values.get("container_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def read_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-mountpoints.html#cfn-batch-jobdefinition-mountpoints-readonly
            '''
            result = self._values.get("read_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def source_volume(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-mountpoints.html#cfn-batch-jobdefinition-mountpoints-sourcevolume
            '''
            result = self._values.get("source_volume")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MountPointsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.MultiNodeEcsPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"task_properties": "taskProperties"},
    )
    class MultiNodeEcsPropertiesProperty:
        def __init__(
            self,
            *,
            task_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.MultiNodeEcsTaskPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''An object that contains the properties for the Amazon ECS resources of a job.

            :param task_properties: An object that contains the properties for the Amazon ECS task definition of a job. .. epigraph:: This object is currently limited to one task element. However, the task element can run up to 10 containers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-multinodeecsproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                # options: Any
                
                multi_node_ecs_properties_property = batch_mixins.CfnJobDefinitionPropsMixin.MultiNodeEcsPropertiesProperty(
                    task_properties=[batch_mixins.CfnJobDefinitionPropsMixin.MultiNodeEcsTaskPropertiesProperty(
                        containers=[batch_mixins.CfnJobDefinitionPropsMixin.TaskContainerPropertiesProperty(
                            command=["command"],
                            depends_on=[batch_mixins.CfnJobDefinitionPropsMixin.TaskContainerDependencyProperty(
                                condition="condition",
                                container_name="containerName"
                            )],
                            environment=[batch_mixins.CfnJobDefinitionPropsMixin.EnvironmentProperty(
                                name="name",
                                value="value"
                            )],
                            essential=False,
                            firelens_configuration=batch_mixins.CfnJobDefinitionPropsMixin.FirelensConfigurationProperty(
                                options={
                                    "options_key": "options"
                                },
                                type="type"
                            ),
                            image="image",
                            linux_parameters=batch_mixins.CfnJobDefinitionPropsMixin.LinuxParametersProperty(
                                devices=[batch_mixins.CfnJobDefinitionPropsMixin.DeviceProperty(
                                    container_path="containerPath",
                                    host_path="hostPath",
                                    permissions=["permissions"]
                                )],
                                init_process_enabled=False,
                                max_swap=123,
                                shared_memory_size=123,
                                swappiness=123,
                                tmpfs=[batch_mixins.CfnJobDefinitionPropsMixin.TmpfsProperty(
                                    container_path="containerPath",
                                    mount_options=["mountOptions"],
                                    size=123
                                )]
                            ),
                            log_configuration=batch_mixins.CfnJobDefinitionPropsMixin.LogConfigurationProperty(
                                log_driver="logDriver",
                                options=options,
                                secret_options=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                                    name="name",
                                    value_from="valueFrom"
                                )]
                            ),
                            mount_points=[batch_mixins.CfnJobDefinitionPropsMixin.MountPointProperty(
                                container_path="containerPath",
                                read_only=False,
                                source_volume="sourceVolume"
                            )],
                            name="name",
                            privileged=False,
                            readonly_root_filesystem=False,
                            repository_credentials=batch_mixins.CfnJobDefinitionPropsMixin.RepositoryCredentialsProperty(
                                credentials_parameter="credentialsParameter"
                            ),
                            resource_requirements=[batch_mixins.CfnJobDefinitionPropsMixin.ResourceRequirementProperty(
                                type="type",
                                value="value"
                            )],
                            secrets=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                                name="name",
                                value_from="valueFrom"
                            )],
                            ulimits=[batch_mixins.CfnJobDefinitionPropsMixin.UlimitProperty(
                                hard_limit=123,
                                name="name",
                                soft_limit=123
                            )],
                            user="user"
                        )],
                        enable_execute_command=False,
                        execution_role_arn="executionRoleArn",
                        ipc_mode="ipcMode",
                        pid_mode="pidMode",
                        task_role_arn="taskRoleArn",
                        volumes=[batch_mixins.CfnJobDefinitionPropsMixin.VolumesProperty(
                            efs_volume_configuration=batch_mixins.CfnJobDefinitionPropsMixin.EfsVolumeConfigurationProperty(
                                authorization_config=batch_mixins.CfnJobDefinitionPropsMixin.AuthorizationConfigProperty(
                                    access_point_id="accessPointId",
                                    iam="iam"
                                ),
                                file_system_id="fileSystemId",
                                root_directory="rootDirectory",
                                transit_encryption="transitEncryption",
                                transit_encryption_port=123
                            ),
                            host=batch_mixins.CfnJobDefinitionPropsMixin.VolumesHostProperty(
                                source_path="sourcePath"
                            ),
                            name="name"
                        )]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7e40ff6e1baf2ea84e2508656704eaafa0e9f67109fc3265b3268195d7886e00)
                check_type(argname="argument task_properties", value=task_properties, expected_type=type_hints["task_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if task_properties is not None:
                self._values["task_properties"] = task_properties

        @builtins.property
        def task_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.MultiNodeEcsTaskPropertiesProperty"]]]]:
            '''An object that contains the properties for the Amazon ECS task definition of a job.

            .. epigraph::

               This object is currently limited to one task element. However, the task element can run up to 10 containers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-multinodeecsproperties.html#cfn-batch-jobdefinition-multinodeecsproperties-taskproperties
            '''
            result = self._values.get("task_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.MultiNodeEcsTaskPropertiesProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MultiNodeEcsPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.MultiNodeEcsTaskPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "containers": "containers",
            "enable_execute_command": "enableExecuteCommand",
            "execution_role_arn": "executionRoleArn",
            "ipc_mode": "ipcMode",
            "pid_mode": "pidMode",
            "task_role_arn": "taskRoleArn",
            "volumes": "volumes",
        },
    )
    class MultiNodeEcsTaskPropertiesProperty:
        def __init__(
            self,
            *,
            containers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.TaskContainerPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            enable_execute_command: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            execution_role_arn: typing.Optional[builtins.str] = None,
            ipc_mode: typing.Optional[builtins.str] = None,
            pid_mode: typing.Optional[builtins.str] = None,
            task_role_arn: typing.Optional[builtins.str] = None,
            volumes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.VolumesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The properties for a task definition that describes the container and volume definitions of an Amazon ECS task.

            You can specify which Docker images to use, the required resources, and other configurations related to launching the task definition through an Amazon ECS service or task.

            :param containers: This object is a list of containers.
            :param enable_execute_command: Determines whether execute command functionality is turned on for this task. If ``true`` , execute command functionality is turned on all the containers in the task.
            :param execution_role_arn: The Amazon Resource Name (ARN) of the execution role that AWS Batch can assume. For jobs that run on Fargate resources, you must provide an execution role. For more information, see `AWS Batch execution IAM role <https://docs.aws.amazon.com/batch/latest/userguide/execution-IAM-role.html>`_ in the *AWS Batch User Guide* .
            :param ipc_mode: The IPC resource namespace to use for the containers in the task. The valid values are ``host`` , ``task`` , or ``none`` . If ``host`` is specified, all containers within the tasks that specified the ``host`` IPC mode on the same container instance share the same IPC resources with the host Amazon EC2 instance. If ``task`` is specified, all containers within the specified ``task`` share the same IPC resources. If ``none`` is specified, the IPC resources within the containers of a task are private, and are not shared with other containers in a task or on the container instance. If no value is specified, then the IPC resource namespace sharing depends on the Docker daemon setting on the container instance. For more information, see `IPC settings <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/#ipc-settings---ipc>`_ in the Docker run reference.
            :param pid_mode: The process namespace to use for the containers in the task. The valid values are ``host`` or ``task`` . For example, monitoring sidecars might need ``pidMode`` to access information about other containers running in the same task. If ``host`` is specified, all containers within the tasks that specified the ``host`` PID mode on the same container instance share the process namespace with the host Amazon EC2 instance. If ``task`` is specified, all containers within the specified task share the same process namespace. If no value is specified, the default is a private namespace for each container. For more information, see `PID settings <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/#pid-settings---pid>`_ in the Docker run reference.
            :param task_role_arn: The Amazon Resource Name (ARN) that's associated with the Amazon ECS task. .. epigraph:: This is object is comparable to `ContainerProperties:jobRoleArn <https://docs.aws.amazon.com/batch/latest/APIReference/API_ContainerProperties.html>`_ .
            :param volumes: A list of volumes that are associated with the job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-multinodeecstaskproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                # options: Any
                
                multi_node_ecs_task_properties_property = batch_mixins.CfnJobDefinitionPropsMixin.MultiNodeEcsTaskPropertiesProperty(
                    containers=[batch_mixins.CfnJobDefinitionPropsMixin.TaskContainerPropertiesProperty(
                        command=["command"],
                        depends_on=[batch_mixins.CfnJobDefinitionPropsMixin.TaskContainerDependencyProperty(
                            condition="condition",
                            container_name="containerName"
                        )],
                        environment=[batch_mixins.CfnJobDefinitionPropsMixin.EnvironmentProperty(
                            name="name",
                            value="value"
                        )],
                        essential=False,
                        firelens_configuration=batch_mixins.CfnJobDefinitionPropsMixin.FirelensConfigurationProperty(
                            options={
                                "options_key": "options"
                            },
                            type="type"
                        ),
                        image="image",
                        linux_parameters=batch_mixins.CfnJobDefinitionPropsMixin.LinuxParametersProperty(
                            devices=[batch_mixins.CfnJobDefinitionPropsMixin.DeviceProperty(
                                container_path="containerPath",
                                host_path="hostPath",
                                permissions=["permissions"]
                            )],
                            init_process_enabled=False,
                            max_swap=123,
                            shared_memory_size=123,
                            swappiness=123,
                            tmpfs=[batch_mixins.CfnJobDefinitionPropsMixin.TmpfsProperty(
                                container_path="containerPath",
                                mount_options=["mountOptions"],
                                size=123
                            )]
                        ),
                        log_configuration=batch_mixins.CfnJobDefinitionPropsMixin.LogConfigurationProperty(
                            log_driver="logDriver",
                            options=options,
                            secret_options=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                                name="name",
                                value_from="valueFrom"
                            )]
                        ),
                        mount_points=[batch_mixins.CfnJobDefinitionPropsMixin.MountPointProperty(
                            container_path="containerPath",
                            read_only=False,
                            source_volume="sourceVolume"
                        )],
                        name="name",
                        privileged=False,
                        readonly_root_filesystem=False,
                        repository_credentials=batch_mixins.CfnJobDefinitionPropsMixin.RepositoryCredentialsProperty(
                            credentials_parameter="credentialsParameter"
                        ),
                        resource_requirements=[batch_mixins.CfnJobDefinitionPropsMixin.ResourceRequirementProperty(
                            type="type",
                            value="value"
                        )],
                        secrets=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                            name="name",
                            value_from="valueFrom"
                        )],
                        ulimits=[batch_mixins.CfnJobDefinitionPropsMixin.UlimitProperty(
                            hard_limit=123,
                            name="name",
                            soft_limit=123
                        )],
                        user="user"
                    )],
                    enable_execute_command=False,
                    execution_role_arn="executionRoleArn",
                    ipc_mode="ipcMode",
                    pid_mode="pidMode",
                    task_role_arn="taskRoleArn",
                    volumes=[batch_mixins.CfnJobDefinitionPropsMixin.VolumesProperty(
                        efs_volume_configuration=batch_mixins.CfnJobDefinitionPropsMixin.EfsVolumeConfigurationProperty(
                            authorization_config=batch_mixins.CfnJobDefinitionPropsMixin.AuthorizationConfigProperty(
                                access_point_id="accessPointId",
                                iam="iam"
                            ),
                            file_system_id="fileSystemId",
                            root_directory="rootDirectory",
                            transit_encryption="transitEncryption",
                            transit_encryption_port=123
                        ),
                        host=batch_mixins.CfnJobDefinitionPropsMixin.VolumesHostProperty(
                            source_path="sourcePath"
                        ),
                        name="name"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__75bc1ce239180115070372f1fc9f0ab27916fcfecc19549715b129942887dd86)
                check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
                check_type(argname="argument enable_execute_command", value=enable_execute_command, expected_type=type_hints["enable_execute_command"])
                check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
                check_type(argname="argument ipc_mode", value=ipc_mode, expected_type=type_hints["ipc_mode"])
                check_type(argname="argument pid_mode", value=pid_mode, expected_type=type_hints["pid_mode"])
                check_type(argname="argument task_role_arn", value=task_role_arn, expected_type=type_hints["task_role_arn"])
                check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if containers is not None:
                self._values["containers"] = containers
            if enable_execute_command is not None:
                self._values["enable_execute_command"] = enable_execute_command
            if execution_role_arn is not None:
                self._values["execution_role_arn"] = execution_role_arn
            if ipc_mode is not None:
                self._values["ipc_mode"] = ipc_mode
            if pid_mode is not None:
                self._values["pid_mode"] = pid_mode
            if task_role_arn is not None:
                self._values["task_role_arn"] = task_role_arn
            if volumes is not None:
                self._values["volumes"] = volumes

        @builtins.property
        def containers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.TaskContainerPropertiesProperty"]]]]:
            '''This object is a list of containers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-multinodeecstaskproperties.html#cfn-batch-jobdefinition-multinodeecstaskproperties-containers
            '''
            result = self._values.get("containers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.TaskContainerPropertiesProperty"]]]], result)

        @builtins.property
        def enable_execute_command(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether execute command functionality is turned on for this task.

            If ``true`` , execute command functionality is turned on all the containers in the task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-multinodeecstaskproperties.html#cfn-batch-jobdefinition-multinodeecstaskproperties-enableexecutecommand
            '''
            result = self._values.get("enable_execute_command")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def execution_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the execution role that AWS Batch can assume.

            For jobs that run on Fargate resources, you must provide an execution role. For more information, see `AWS Batch execution IAM role <https://docs.aws.amazon.com/batch/latest/userguide/execution-IAM-role.html>`_ in the *AWS Batch User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-multinodeecstaskproperties.html#cfn-batch-jobdefinition-multinodeecstaskproperties-executionrolearn
            '''
            result = self._values.get("execution_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ipc_mode(self) -> typing.Optional[builtins.str]:
            '''The IPC resource namespace to use for the containers in the task.

            The valid values are ``host`` , ``task`` , or ``none`` .

            If ``host`` is specified, all containers within the tasks that specified the ``host`` IPC mode on the same container instance share the same IPC resources with the host Amazon EC2 instance.

            If ``task`` is specified, all containers within the specified ``task`` share the same IPC resources.

            If ``none`` is specified, the IPC resources within the containers of a task are private, and are not shared with other containers in a task or on the container instance.

            If no value is specified, then the IPC resource namespace sharing depends on the Docker daemon setting on the container instance. For more information, see `IPC settings <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/#ipc-settings---ipc>`_ in the Docker run reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-multinodeecstaskproperties.html#cfn-batch-jobdefinition-multinodeecstaskproperties-ipcmode
            '''
            result = self._values.get("ipc_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pid_mode(self) -> typing.Optional[builtins.str]:
            '''The process namespace to use for the containers in the task.

            The valid values are ``host`` or ``task`` . For example, monitoring sidecars might need ``pidMode`` to access information about other containers running in the same task.

            If ``host`` is specified, all containers within the tasks that specified the ``host`` PID mode on the same container instance share the process namespace with the host Amazon EC2 instance.

            If ``task`` is specified, all containers within the specified task share the same process namespace.

            If no value is specified, the default is a private namespace for each container. For more information, see `PID settings <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/#pid-settings---pid>`_ in the Docker run reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-multinodeecstaskproperties.html#cfn-batch-jobdefinition-multinodeecstaskproperties-pidmode
            '''
            result = self._values.get("pid_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def task_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) that's associated with the Amazon ECS task.

            .. epigraph::

               This is object is comparable to `ContainerProperties:jobRoleArn <https://docs.aws.amazon.com/batch/latest/APIReference/API_ContainerProperties.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-multinodeecstaskproperties.html#cfn-batch-jobdefinition-multinodeecstaskproperties-taskrolearn
            '''
            result = self._values.get("task_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def volumes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.VolumesProperty"]]]]:
            '''A list of volumes that are associated with the job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-multinodeecstaskproperties.html#cfn-batch-jobdefinition-multinodeecstaskproperties-volumes
            '''
            result = self._values.get("volumes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.VolumesProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MultiNodeEcsTaskPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.NetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"assign_public_ip": "assignPublicIp"},
    )
    class NetworkConfigurationProperty:
        def __init__(
            self,
            *,
            assign_public_ip: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The network configuration for jobs that are running on Fargate resources.

            Jobs that are running on Amazon EC2 resources must not specify this parameter.

            :param assign_public_ip: Indicates whether the job has a public IP address. For a job that's running on Fargate resources in a private subnet to send outbound traffic to the internet (for example, to pull container images), the private subnet requires a NAT gateway be attached to route requests to the internet. For more information, see `Amazon ECS task networking <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-networking.html>`_ in the *Amazon Elastic Container Service Developer Guide* . The default value is " ``DISABLED`` ".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-networkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                network_configuration_property = batch_mixins.CfnJobDefinitionPropsMixin.NetworkConfigurationProperty(
                    assign_public_ip="assignPublicIp"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a4cca6e41aaf81cfe601c5b66371ac220e000c0a5fb2887a06964c2235a56c18)
                check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if assign_public_ip is not None:
                self._values["assign_public_ip"] = assign_public_ip

        @builtins.property
        def assign_public_ip(self) -> typing.Optional[builtins.str]:
            '''Indicates whether the job has a public IP address.

            For a job that's running on Fargate resources in a private subnet to send outbound traffic to the internet (for example, to pull container images), the private subnet requires a NAT gateway be attached to route requests to the internet. For more information, see `Amazon ECS task networking <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-networking.html>`_ in the *Amazon Elastic Container Service Developer Guide* . The default value is " ``DISABLED`` ".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-networkconfiguration.html#cfn-batch-jobdefinition-networkconfiguration-assignpublicip
            '''
            result = self._values.get("assign_public_ip")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.NodePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "main_node": "mainNode",
            "node_range_properties": "nodeRangeProperties",
            "num_nodes": "numNodes",
        },
    )
    class NodePropertiesProperty:
        def __init__(
            self,
            *,
            main_node: typing.Optional[jsii.Number] = None,
            node_range_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.NodeRangePropertyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            num_nodes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that represents the node properties of a multi-node parallel job.

            .. epigraph::

               Node properties can't be specified for Amazon EKS based job definitions.

            :param main_node: Specifies the node index for the main node of a multi-node parallel job. This node index value must be fewer than the number of nodes.
            :param node_range_properties: A list of node ranges and their properties that are associated with a multi-node parallel job.
            :param num_nodes: The number of nodes that are associated with a multi-node parallel job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-nodeproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                # labels: Any
                # limits: Any
                # options: Any
                # requests: Any
                
                node_properties_property = batch_mixins.CfnJobDefinitionPropsMixin.NodePropertiesProperty(
                    main_node=123,
                    node_range_properties=[batch_mixins.CfnJobDefinitionPropsMixin.NodeRangePropertyProperty(
                        consumable_resource_properties=batch_mixins.CfnJobDefinitionPropsMixin.ConsumableResourcePropertiesProperty(
                            consumable_resource_list=[batch_mixins.CfnJobDefinitionPropsMixin.ConsumableResourceRequirementProperty(
                                consumable_resource="consumableResource",
                                quantity=123
                            )]
                        ),
                        container=batch_mixins.CfnJobDefinitionPropsMixin.ContainerPropertiesProperty(
                            command=["command"],
                            enable_execute_command=False,
                            environment=[batch_mixins.CfnJobDefinitionPropsMixin.EnvironmentProperty(
                                name="name",
                                value="value"
                            )],
                            ephemeral_storage=batch_mixins.CfnJobDefinitionPropsMixin.EphemeralStorageProperty(
                                size_in_gi_b=123
                            ),
                            execution_role_arn="executionRoleArn",
                            fargate_platform_configuration=batch_mixins.CfnJobDefinitionPropsMixin.FargatePlatformConfigurationProperty(
                                platform_version="platformVersion"
                            ),
                            image="image",
                            instance_type="instanceType",
                            job_role_arn="jobRoleArn",
                            linux_parameters=batch_mixins.CfnJobDefinitionPropsMixin.LinuxParametersProperty(
                                devices=[batch_mixins.CfnJobDefinitionPropsMixin.DeviceProperty(
                                    container_path="containerPath",
                                    host_path="hostPath",
                                    permissions=["permissions"]
                                )],
                                init_process_enabled=False,
                                max_swap=123,
                                shared_memory_size=123,
                                swappiness=123,
                                tmpfs=[batch_mixins.CfnJobDefinitionPropsMixin.TmpfsProperty(
                                    container_path="containerPath",
                                    mount_options=["mountOptions"],
                                    size=123
                                )]
                            ),
                            log_configuration=batch_mixins.CfnJobDefinitionPropsMixin.LogConfigurationProperty(
                                log_driver="logDriver",
                                options=options,
                                secret_options=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                                    name="name",
                                    value_from="valueFrom"
                                )]
                            ),
                            memory=123,
                            mount_points=[batch_mixins.CfnJobDefinitionPropsMixin.MountPointsProperty(
                                container_path="containerPath",
                                read_only=False,
                                source_volume="sourceVolume"
                            )],
                            network_configuration=batch_mixins.CfnJobDefinitionPropsMixin.NetworkConfigurationProperty(
                                assign_public_ip="assignPublicIp"
                            ),
                            privileged=False,
                            readonly_root_filesystem=False,
                            repository_credentials=batch_mixins.CfnJobDefinitionPropsMixin.RepositoryCredentialsProperty(
                                credentials_parameter="credentialsParameter"
                            ),
                            resource_requirements=[batch_mixins.CfnJobDefinitionPropsMixin.ResourceRequirementProperty(
                                type="type",
                                value="value"
                            )],
                            runtime_platform=batch_mixins.CfnJobDefinitionPropsMixin.RuntimePlatformProperty(
                                cpu_architecture="cpuArchitecture",
                                operating_system_family="operatingSystemFamily"
                            ),
                            secrets=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                                name="name",
                                value_from="valueFrom"
                            )],
                            ulimits=[batch_mixins.CfnJobDefinitionPropsMixin.UlimitProperty(
                                hard_limit=123,
                                name="name",
                                soft_limit=123
                            )],
                            user="user",
                            vcpus=123,
                            volumes=[batch_mixins.CfnJobDefinitionPropsMixin.VolumesProperty(
                                efs_volume_configuration=batch_mixins.CfnJobDefinitionPropsMixin.EfsVolumeConfigurationProperty(
                                    authorization_config=batch_mixins.CfnJobDefinitionPropsMixin.AuthorizationConfigProperty(
                                        access_point_id="accessPointId",
                                        iam="iam"
                                    ),
                                    file_system_id="fileSystemId",
                                    root_directory="rootDirectory",
                                    transit_encryption="transitEncryption",
                                    transit_encryption_port=123
                                ),
                                host=batch_mixins.CfnJobDefinitionPropsMixin.VolumesHostProperty(
                                    source_path="sourcePath"
                                ),
                                name="name"
                            )]
                        ),
                        ecs_properties=batch_mixins.CfnJobDefinitionPropsMixin.MultiNodeEcsPropertiesProperty(
                            task_properties=[batch_mixins.CfnJobDefinitionPropsMixin.MultiNodeEcsTaskPropertiesProperty(
                                containers=[batch_mixins.CfnJobDefinitionPropsMixin.TaskContainerPropertiesProperty(
                                    command=["command"],
                                    depends_on=[batch_mixins.CfnJobDefinitionPropsMixin.TaskContainerDependencyProperty(
                                        condition="condition",
                                        container_name="containerName"
                                    )],
                                    environment=[batch_mixins.CfnJobDefinitionPropsMixin.EnvironmentProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    essential=False,
                                    firelens_configuration=batch_mixins.CfnJobDefinitionPropsMixin.FirelensConfigurationProperty(
                                        options={
                                            "options_key": "options"
                                        },
                                        type="type"
                                    ),
                                    image="image",
                                    linux_parameters=batch_mixins.CfnJobDefinitionPropsMixin.LinuxParametersProperty(
                                        devices=[batch_mixins.CfnJobDefinitionPropsMixin.DeviceProperty(
                                            container_path="containerPath",
                                            host_path="hostPath",
                                            permissions=["permissions"]
                                        )],
                                        init_process_enabled=False,
                                        max_swap=123,
                                        shared_memory_size=123,
                                        swappiness=123,
                                        tmpfs=[batch_mixins.CfnJobDefinitionPropsMixin.TmpfsProperty(
                                            container_path="containerPath",
                                            mount_options=["mountOptions"],
                                            size=123
                                        )]
                                    ),
                                    log_configuration=batch_mixins.CfnJobDefinitionPropsMixin.LogConfigurationProperty(
                                        log_driver="logDriver",
                                        options=options,
                                        secret_options=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                                            name="name",
                                            value_from="valueFrom"
                                        )]
                                    ),
                                    mount_points=[batch_mixins.CfnJobDefinitionPropsMixin.MountPointProperty(
                                        container_path="containerPath",
                                        read_only=False,
                                        source_volume="sourceVolume"
                                    )],
                                    name="name",
                                    privileged=False,
                                    readonly_root_filesystem=False,
                                    repository_credentials=batch_mixins.CfnJobDefinitionPropsMixin.RepositoryCredentialsProperty(
                                        credentials_parameter="credentialsParameter"
                                    ),
                                    resource_requirements=[batch_mixins.CfnJobDefinitionPropsMixin.ResourceRequirementProperty(
                                        type="type",
                                        value="value"
                                    )],
                                    secrets=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                                        name="name",
                                        value_from="valueFrom"
                                    )],
                                    ulimits=[batch_mixins.CfnJobDefinitionPropsMixin.UlimitProperty(
                                        hard_limit=123,
                                        name="name",
                                        soft_limit=123
                                    )],
                                    user="user"
                                )],
                                enable_execute_command=False,
                                execution_role_arn="executionRoleArn",
                                ipc_mode="ipcMode",
                                pid_mode="pidMode",
                                task_role_arn="taskRoleArn",
                                volumes=[batch_mixins.CfnJobDefinitionPropsMixin.VolumesProperty(
                                    efs_volume_configuration=batch_mixins.CfnJobDefinitionPropsMixin.EfsVolumeConfigurationProperty(
                                        authorization_config=batch_mixins.CfnJobDefinitionPropsMixin.AuthorizationConfigProperty(
                                            access_point_id="accessPointId",
                                            iam="iam"
                                        ),
                                        file_system_id="fileSystemId",
                                        root_directory="rootDirectory",
                                        transit_encryption="transitEncryption",
                                        transit_encryption_port=123
                                    ),
                                    host=batch_mixins.CfnJobDefinitionPropsMixin.VolumesHostProperty(
                                        source_path="sourcePath"
                                    ),
                                    name="name"
                                )]
                            )]
                        ),
                        eks_properties=batch_mixins.CfnJobDefinitionPropsMixin.EksPropertiesProperty(
                            pod_properties=batch_mixins.CfnJobDefinitionPropsMixin.PodPropertiesProperty(
                                containers=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerProperty(
                                    args=["args"],
                                    command=["command"],
                                    env=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerEnvironmentVariableProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    image="image",
                                    image_pull_policy="imagePullPolicy",
                                    name="name",
                                    resources=batch_mixins.CfnJobDefinitionPropsMixin.ResourcesProperty(
                                        limits=limits,
                                        requests=requests
                                    ),
                                    security_context=batch_mixins.CfnJobDefinitionPropsMixin.SecurityContextProperty(
                                        allow_privilege_escalation=False,
                                        privileged=False,
                                        read_only_root_filesystem=False,
                                        run_as_group=123,
                                        run_as_non_root=False,
                                        run_as_user=123
                                    ),
                                    volume_mounts=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerVolumeMountProperty(
                                        mount_path="mountPath",
                                        name="name",
                                        read_only=False,
                                        sub_path="subPath"
                                    )]
                                )],
                                dns_policy="dnsPolicy",
                                host_network=False,
                                image_pull_secrets=[batch_mixins.CfnJobDefinitionPropsMixin.ImagePullSecretProperty(
                                    name="name"
                                )],
                                init_containers=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerProperty(
                                    args=["args"],
                                    command=["command"],
                                    env=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerEnvironmentVariableProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    image="image",
                                    image_pull_policy="imagePullPolicy",
                                    name="name",
                                    resources=batch_mixins.CfnJobDefinitionPropsMixin.ResourcesProperty(
                                        limits=limits,
                                        requests=requests
                                    ),
                                    security_context=batch_mixins.CfnJobDefinitionPropsMixin.SecurityContextProperty(
                                        allow_privilege_escalation=False,
                                        privileged=False,
                                        read_only_root_filesystem=False,
                                        run_as_group=123,
                                        run_as_non_root=False,
                                        run_as_user=123
                                    ),
                                    volume_mounts=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerVolumeMountProperty(
                                        mount_path="mountPath",
                                        name="name",
                                        read_only=False,
                                        sub_path="subPath"
                                    )]
                                )],
                                metadata=batch_mixins.CfnJobDefinitionPropsMixin.MetadataProperty(
                                    labels=labels
                                ),
                                service_account_name="serviceAccountName",
                                share_process_namespace=False,
                                volumes=[batch_mixins.CfnJobDefinitionPropsMixin.EksVolumeProperty(
                                    empty_dir=batch_mixins.CfnJobDefinitionPropsMixin.EmptyDirProperty(
                                        medium="medium",
                                        size_limit="sizeLimit"
                                    ),
                                    host_path=batch_mixins.CfnJobDefinitionPropsMixin.HostPathProperty(
                                        path="path"
                                    ),
                                    name="name",
                                    persistent_volume_claim=batch_mixins.CfnJobDefinitionPropsMixin.EksPersistentVolumeClaimProperty(
                                        claim_name="claimName",
                                        read_only=False
                                    ),
                                    secret=batch_mixins.CfnJobDefinitionPropsMixin.EksSecretProperty(
                                        optional=False,
                                        secret_name="secretName"
                                    )
                                )]
                            )
                        ),
                        instance_types=["instanceTypes"],
                        target_nodes="targetNodes"
                    )],
                    num_nodes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e7a7b9392a47c632922643c51b6a15680e27abc8cbf41d92167891a151e9815c)
                check_type(argname="argument main_node", value=main_node, expected_type=type_hints["main_node"])
                check_type(argname="argument node_range_properties", value=node_range_properties, expected_type=type_hints["node_range_properties"])
                check_type(argname="argument num_nodes", value=num_nodes, expected_type=type_hints["num_nodes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if main_node is not None:
                self._values["main_node"] = main_node
            if node_range_properties is not None:
                self._values["node_range_properties"] = node_range_properties
            if num_nodes is not None:
                self._values["num_nodes"] = num_nodes

        @builtins.property
        def main_node(self) -> typing.Optional[jsii.Number]:
            '''Specifies the node index for the main node of a multi-node parallel job.

            This node index value must be fewer than the number of nodes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-nodeproperties.html#cfn-batch-jobdefinition-nodeproperties-mainnode
            '''
            result = self._values.get("main_node")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def node_range_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.NodeRangePropertyProperty"]]]]:
            '''A list of node ranges and their properties that are associated with a multi-node parallel job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-nodeproperties.html#cfn-batch-jobdefinition-nodeproperties-noderangeproperties
            '''
            result = self._values.get("node_range_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.NodeRangePropertyProperty"]]]], result)

        @builtins.property
        def num_nodes(self) -> typing.Optional[jsii.Number]:
            '''The number of nodes that are associated with a multi-node parallel job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-nodeproperties.html#cfn-batch-jobdefinition-nodeproperties-numnodes
            '''
            result = self._values.get("num_nodes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.NodeRangePropertyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "consumable_resource_properties": "consumableResourceProperties",
            "container": "container",
            "ecs_properties": "ecsProperties",
            "eks_properties": "eksProperties",
            "instance_types": "instanceTypes",
            "target_nodes": "targetNodes",
        },
    )
    class NodeRangePropertyProperty:
        def __init__(
            self,
            *,
            consumable_resource_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.ConsumableResourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            container: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.ContainerPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ecs_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.MultiNodeEcsPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            eks_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.EksPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            target_nodes: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This is an object that represents the properties of the node range for a multi-node parallel job.

            :param consumable_resource_properties: Contains a list of consumable resources required by a job.
            :param container: The container details for the node range.
            :param ecs_properties: This is an object that represents the properties of the node range for a multi-node parallel job.
            :param eks_properties: This is an object that represents the properties of the node range for a multi-node parallel job.
            :param instance_types: The instance types of the underlying host infrastructure of a multi-node parallel job. .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. In addition, this list object is currently limited to one element.
            :param target_nodes: The range of nodes, using node index values. A range of ``0:3`` indicates nodes with index values of ``0`` through ``3`` . If the starting range value is omitted ( ``:n`` ), then ``0`` is used to start the range. If the ending range value is omitted ( ``n:`` ), then the highest possible node index is used to end the range. Your accumulative node ranges must account for all nodes ( ``0:n`` ). You can nest node ranges (for example, ``0:10`` and ``4:5`` ). In this case, the ``4:5`` range properties override the ``0:10`` properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-noderangeproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                # labels: Any
                # limits: Any
                # options: Any
                # requests: Any
                
                node_range_property_property = batch_mixins.CfnJobDefinitionPropsMixin.NodeRangePropertyProperty(
                    consumable_resource_properties=batch_mixins.CfnJobDefinitionPropsMixin.ConsumableResourcePropertiesProperty(
                        consumable_resource_list=[batch_mixins.CfnJobDefinitionPropsMixin.ConsumableResourceRequirementProperty(
                            consumable_resource="consumableResource",
                            quantity=123
                        )]
                    ),
                    container=batch_mixins.CfnJobDefinitionPropsMixin.ContainerPropertiesProperty(
                        command=["command"],
                        enable_execute_command=False,
                        environment=[batch_mixins.CfnJobDefinitionPropsMixin.EnvironmentProperty(
                            name="name",
                            value="value"
                        )],
                        ephemeral_storage=batch_mixins.CfnJobDefinitionPropsMixin.EphemeralStorageProperty(
                            size_in_gi_b=123
                        ),
                        execution_role_arn="executionRoleArn",
                        fargate_platform_configuration=batch_mixins.CfnJobDefinitionPropsMixin.FargatePlatformConfigurationProperty(
                            platform_version="platformVersion"
                        ),
                        image="image",
                        instance_type="instanceType",
                        job_role_arn="jobRoleArn",
                        linux_parameters=batch_mixins.CfnJobDefinitionPropsMixin.LinuxParametersProperty(
                            devices=[batch_mixins.CfnJobDefinitionPropsMixin.DeviceProperty(
                                container_path="containerPath",
                                host_path="hostPath",
                                permissions=["permissions"]
                            )],
                            init_process_enabled=False,
                            max_swap=123,
                            shared_memory_size=123,
                            swappiness=123,
                            tmpfs=[batch_mixins.CfnJobDefinitionPropsMixin.TmpfsProperty(
                                container_path="containerPath",
                                mount_options=["mountOptions"],
                                size=123
                            )]
                        ),
                        log_configuration=batch_mixins.CfnJobDefinitionPropsMixin.LogConfigurationProperty(
                            log_driver="logDriver",
                            options=options,
                            secret_options=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                                name="name",
                                value_from="valueFrom"
                            )]
                        ),
                        memory=123,
                        mount_points=[batch_mixins.CfnJobDefinitionPropsMixin.MountPointsProperty(
                            container_path="containerPath",
                            read_only=False,
                            source_volume="sourceVolume"
                        )],
                        network_configuration=batch_mixins.CfnJobDefinitionPropsMixin.NetworkConfigurationProperty(
                            assign_public_ip="assignPublicIp"
                        ),
                        privileged=False,
                        readonly_root_filesystem=False,
                        repository_credentials=batch_mixins.CfnJobDefinitionPropsMixin.RepositoryCredentialsProperty(
                            credentials_parameter="credentialsParameter"
                        ),
                        resource_requirements=[batch_mixins.CfnJobDefinitionPropsMixin.ResourceRequirementProperty(
                            type="type",
                            value="value"
                        )],
                        runtime_platform=batch_mixins.CfnJobDefinitionPropsMixin.RuntimePlatformProperty(
                            cpu_architecture="cpuArchitecture",
                            operating_system_family="operatingSystemFamily"
                        ),
                        secrets=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                            name="name",
                            value_from="valueFrom"
                        )],
                        ulimits=[batch_mixins.CfnJobDefinitionPropsMixin.UlimitProperty(
                            hard_limit=123,
                            name="name",
                            soft_limit=123
                        )],
                        user="user",
                        vcpus=123,
                        volumes=[batch_mixins.CfnJobDefinitionPropsMixin.VolumesProperty(
                            efs_volume_configuration=batch_mixins.CfnJobDefinitionPropsMixin.EfsVolumeConfigurationProperty(
                                authorization_config=batch_mixins.CfnJobDefinitionPropsMixin.AuthorizationConfigProperty(
                                    access_point_id="accessPointId",
                                    iam="iam"
                                ),
                                file_system_id="fileSystemId",
                                root_directory="rootDirectory",
                                transit_encryption="transitEncryption",
                                transit_encryption_port=123
                            ),
                            host=batch_mixins.CfnJobDefinitionPropsMixin.VolumesHostProperty(
                                source_path="sourcePath"
                            ),
                            name="name"
                        )]
                    ),
                    ecs_properties=batch_mixins.CfnJobDefinitionPropsMixin.MultiNodeEcsPropertiesProperty(
                        task_properties=[batch_mixins.CfnJobDefinitionPropsMixin.MultiNodeEcsTaskPropertiesProperty(
                            containers=[batch_mixins.CfnJobDefinitionPropsMixin.TaskContainerPropertiesProperty(
                                command=["command"],
                                depends_on=[batch_mixins.CfnJobDefinitionPropsMixin.TaskContainerDependencyProperty(
                                    condition="condition",
                                    container_name="containerName"
                                )],
                                environment=[batch_mixins.CfnJobDefinitionPropsMixin.EnvironmentProperty(
                                    name="name",
                                    value="value"
                                )],
                                essential=False,
                                firelens_configuration=batch_mixins.CfnJobDefinitionPropsMixin.FirelensConfigurationProperty(
                                    options={
                                        "options_key": "options"
                                    },
                                    type="type"
                                ),
                                image="image",
                                linux_parameters=batch_mixins.CfnJobDefinitionPropsMixin.LinuxParametersProperty(
                                    devices=[batch_mixins.CfnJobDefinitionPropsMixin.DeviceProperty(
                                        container_path="containerPath",
                                        host_path="hostPath",
                                        permissions=["permissions"]
                                    )],
                                    init_process_enabled=False,
                                    max_swap=123,
                                    shared_memory_size=123,
                                    swappiness=123,
                                    tmpfs=[batch_mixins.CfnJobDefinitionPropsMixin.TmpfsProperty(
                                        container_path="containerPath",
                                        mount_options=["mountOptions"],
                                        size=123
                                    )]
                                ),
                                log_configuration=batch_mixins.CfnJobDefinitionPropsMixin.LogConfigurationProperty(
                                    log_driver="logDriver",
                                    options=options,
                                    secret_options=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                                        name="name",
                                        value_from="valueFrom"
                                    )]
                                ),
                                mount_points=[batch_mixins.CfnJobDefinitionPropsMixin.MountPointProperty(
                                    container_path="containerPath",
                                    read_only=False,
                                    source_volume="sourceVolume"
                                )],
                                name="name",
                                privileged=False,
                                readonly_root_filesystem=False,
                                repository_credentials=batch_mixins.CfnJobDefinitionPropsMixin.RepositoryCredentialsProperty(
                                    credentials_parameter="credentialsParameter"
                                ),
                                resource_requirements=[batch_mixins.CfnJobDefinitionPropsMixin.ResourceRequirementProperty(
                                    type="type",
                                    value="value"
                                )],
                                secrets=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                                    name="name",
                                    value_from="valueFrom"
                                )],
                                ulimits=[batch_mixins.CfnJobDefinitionPropsMixin.UlimitProperty(
                                    hard_limit=123,
                                    name="name",
                                    soft_limit=123
                                )],
                                user="user"
                            )],
                            enable_execute_command=False,
                            execution_role_arn="executionRoleArn",
                            ipc_mode="ipcMode",
                            pid_mode="pidMode",
                            task_role_arn="taskRoleArn",
                            volumes=[batch_mixins.CfnJobDefinitionPropsMixin.VolumesProperty(
                                efs_volume_configuration=batch_mixins.CfnJobDefinitionPropsMixin.EfsVolumeConfigurationProperty(
                                    authorization_config=batch_mixins.CfnJobDefinitionPropsMixin.AuthorizationConfigProperty(
                                        access_point_id="accessPointId",
                                        iam="iam"
                                    ),
                                    file_system_id="fileSystemId",
                                    root_directory="rootDirectory",
                                    transit_encryption="transitEncryption",
                                    transit_encryption_port=123
                                ),
                                host=batch_mixins.CfnJobDefinitionPropsMixin.VolumesHostProperty(
                                    source_path="sourcePath"
                                ),
                                name="name"
                            )]
                        )]
                    ),
                    eks_properties=batch_mixins.CfnJobDefinitionPropsMixin.EksPropertiesProperty(
                        pod_properties=batch_mixins.CfnJobDefinitionPropsMixin.PodPropertiesProperty(
                            containers=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerProperty(
                                args=["args"],
                                command=["command"],
                                env=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerEnvironmentVariableProperty(
                                    name="name",
                                    value="value"
                                )],
                                image="image",
                                image_pull_policy="imagePullPolicy",
                                name="name",
                                resources=batch_mixins.CfnJobDefinitionPropsMixin.ResourcesProperty(
                                    limits=limits,
                                    requests=requests
                                ),
                                security_context=batch_mixins.CfnJobDefinitionPropsMixin.SecurityContextProperty(
                                    allow_privilege_escalation=False,
                                    privileged=False,
                                    read_only_root_filesystem=False,
                                    run_as_group=123,
                                    run_as_non_root=False,
                                    run_as_user=123
                                ),
                                volume_mounts=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerVolumeMountProperty(
                                    mount_path="mountPath",
                                    name="name",
                                    read_only=False,
                                    sub_path="subPath"
                                )]
                            )],
                            dns_policy="dnsPolicy",
                            host_network=False,
                            image_pull_secrets=[batch_mixins.CfnJobDefinitionPropsMixin.ImagePullSecretProperty(
                                name="name"
                            )],
                            init_containers=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerProperty(
                                args=["args"],
                                command=["command"],
                                env=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerEnvironmentVariableProperty(
                                    name="name",
                                    value="value"
                                )],
                                image="image",
                                image_pull_policy="imagePullPolicy",
                                name="name",
                                resources=batch_mixins.CfnJobDefinitionPropsMixin.ResourcesProperty(
                                    limits=limits,
                                    requests=requests
                                ),
                                security_context=batch_mixins.CfnJobDefinitionPropsMixin.SecurityContextProperty(
                                    allow_privilege_escalation=False,
                                    privileged=False,
                                    read_only_root_filesystem=False,
                                    run_as_group=123,
                                    run_as_non_root=False,
                                    run_as_user=123
                                ),
                                volume_mounts=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerVolumeMountProperty(
                                    mount_path="mountPath",
                                    name="name",
                                    read_only=False,
                                    sub_path="subPath"
                                )]
                            )],
                            metadata=batch_mixins.CfnJobDefinitionPropsMixin.MetadataProperty(
                                labels=labels
                            ),
                            service_account_name="serviceAccountName",
                            share_process_namespace=False,
                            volumes=[batch_mixins.CfnJobDefinitionPropsMixin.EksVolumeProperty(
                                empty_dir=batch_mixins.CfnJobDefinitionPropsMixin.EmptyDirProperty(
                                    medium="medium",
                                    size_limit="sizeLimit"
                                ),
                                host_path=batch_mixins.CfnJobDefinitionPropsMixin.HostPathProperty(
                                    path="path"
                                ),
                                name="name",
                                persistent_volume_claim=batch_mixins.CfnJobDefinitionPropsMixin.EksPersistentVolumeClaimProperty(
                                    claim_name="claimName",
                                    read_only=False
                                ),
                                secret=batch_mixins.CfnJobDefinitionPropsMixin.EksSecretProperty(
                                    optional=False,
                                    secret_name="secretName"
                                )
                            )]
                        )
                    ),
                    instance_types=["instanceTypes"],
                    target_nodes="targetNodes"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a33a59520854daf4f026d2061801fb7cdb25cac070e0151beff4bc1c97bc4271)
                check_type(argname="argument consumable_resource_properties", value=consumable_resource_properties, expected_type=type_hints["consumable_resource_properties"])
                check_type(argname="argument container", value=container, expected_type=type_hints["container"])
                check_type(argname="argument ecs_properties", value=ecs_properties, expected_type=type_hints["ecs_properties"])
                check_type(argname="argument eks_properties", value=eks_properties, expected_type=type_hints["eks_properties"])
                check_type(argname="argument instance_types", value=instance_types, expected_type=type_hints["instance_types"])
                check_type(argname="argument target_nodes", value=target_nodes, expected_type=type_hints["target_nodes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if consumable_resource_properties is not None:
                self._values["consumable_resource_properties"] = consumable_resource_properties
            if container is not None:
                self._values["container"] = container
            if ecs_properties is not None:
                self._values["ecs_properties"] = ecs_properties
            if eks_properties is not None:
                self._values["eks_properties"] = eks_properties
            if instance_types is not None:
                self._values["instance_types"] = instance_types
            if target_nodes is not None:
                self._values["target_nodes"] = target_nodes

        @builtins.property
        def consumable_resource_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.ConsumableResourcePropertiesProperty"]]:
            '''Contains a list of consumable resources required by a job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-noderangeproperty.html#cfn-batch-jobdefinition-noderangeproperty-consumableresourceproperties
            '''
            result = self._values.get("consumable_resource_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.ConsumableResourcePropertiesProperty"]], result)

        @builtins.property
        def container(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.ContainerPropertiesProperty"]]:
            '''The container details for the node range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-noderangeproperty.html#cfn-batch-jobdefinition-noderangeproperty-container
            '''
            result = self._values.get("container")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.ContainerPropertiesProperty"]], result)

        @builtins.property
        def ecs_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.MultiNodeEcsPropertiesProperty"]]:
            '''This is an object that represents the properties of the node range for a multi-node parallel job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-noderangeproperty.html#cfn-batch-jobdefinition-noderangeproperty-ecsproperties
            '''
            result = self._values.get("ecs_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.MultiNodeEcsPropertiesProperty"]], result)

        @builtins.property
        def eks_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EksPropertiesProperty"]]:
            '''This is an object that represents the properties of the node range for a multi-node parallel job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-noderangeproperty.html#cfn-batch-jobdefinition-noderangeproperty-eksproperties
            '''
            result = self._values.get("eks_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EksPropertiesProperty"]], result)

        @builtins.property
        def instance_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The instance types of the underlying host infrastructure of a multi-node parallel job.

            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources.

               In addition, this list object is currently limited to one element.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-noderangeproperty.html#cfn-batch-jobdefinition-noderangeproperty-instancetypes
            '''
            result = self._values.get("instance_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def target_nodes(self) -> typing.Optional[builtins.str]:
            '''The range of nodes, using node index values.

            A range of ``0:3`` indicates nodes with index values of ``0`` through ``3`` . If the starting range value is omitted ( ``:n`` ), then ``0`` is used to start the range. If the ending range value is omitted ( ``n:`` ), then the highest possible node index is used to end the range. Your accumulative node ranges must account for all nodes ( ``0:n`` ). You can nest node ranges (for example, ``0:10`` and ``4:5`` ). In this case, the ``4:5`` range properties override the ``0:10`` properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-noderangeproperty.html#cfn-batch-jobdefinition-noderangeproperty-targetnodes
            '''
            result = self._values.get("target_nodes")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeRangePropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.PodPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "containers": "containers",
            "dns_policy": "dnsPolicy",
            "host_network": "hostNetwork",
            "image_pull_secrets": "imagePullSecrets",
            "init_containers": "initContainers",
            "metadata": "metadata",
            "service_account_name": "serviceAccountName",
            "share_process_namespace": "shareProcessNamespace",
            "volumes": "volumes",
        },
    )
    class PodPropertiesProperty:
        def __init__(
            self,
            *,
            containers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.EksContainerProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            dns_policy: typing.Optional[builtins.str] = None,
            host_network: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            image_pull_secrets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.ImagePullSecretProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            init_containers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.EksContainerProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.MetadataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_account_name: typing.Optional[builtins.str] = None,
            share_process_namespace: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            volumes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.EksVolumeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''
            :param containers: 
            :param dns_policy: 
            :param host_network: 
            :param image_pull_secrets: 
            :param init_containers: 
            :param metadata: 
            :param service_account_name: 
            :param share_process_namespace: 
            :param volumes: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-podproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                # labels: Any
                # limits: Any
                # requests: Any
                
                pod_properties_property = batch_mixins.CfnJobDefinitionPropsMixin.PodPropertiesProperty(
                    containers=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerProperty(
                        args=["args"],
                        command=["command"],
                        env=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerEnvironmentVariableProperty(
                            name="name",
                            value="value"
                        )],
                        image="image",
                        image_pull_policy="imagePullPolicy",
                        name="name",
                        resources=batch_mixins.CfnJobDefinitionPropsMixin.ResourcesProperty(
                            limits=limits,
                            requests=requests
                        ),
                        security_context=batch_mixins.CfnJobDefinitionPropsMixin.SecurityContextProperty(
                            allow_privilege_escalation=False,
                            privileged=False,
                            read_only_root_filesystem=False,
                            run_as_group=123,
                            run_as_non_root=False,
                            run_as_user=123
                        ),
                        volume_mounts=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerVolumeMountProperty(
                            mount_path="mountPath",
                            name="name",
                            read_only=False,
                            sub_path="subPath"
                        )]
                    )],
                    dns_policy="dnsPolicy",
                    host_network=False,
                    image_pull_secrets=[batch_mixins.CfnJobDefinitionPropsMixin.ImagePullSecretProperty(
                        name="name"
                    )],
                    init_containers=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerProperty(
                        args=["args"],
                        command=["command"],
                        env=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerEnvironmentVariableProperty(
                            name="name",
                            value="value"
                        )],
                        image="image",
                        image_pull_policy="imagePullPolicy",
                        name="name",
                        resources=batch_mixins.CfnJobDefinitionPropsMixin.ResourcesProperty(
                            limits=limits,
                            requests=requests
                        ),
                        security_context=batch_mixins.CfnJobDefinitionPropsMixin.SecurityContextProperty(
                            allow_privilege_escalation=False,
                            privileged=False,
                            read_only_root_filesystem=False,
                            run_as_group=123,
                            run_as_non_root=False,
                            run_as_user=123
                        ),
                        volume_mounts=[batch_mixins.CfnJobDefinitionPropsMixin.EksContainerVolumeMountProperty(
                            mount_path="mountPath",
                            name="name",
                            read_only=False,
                            sub_path="subPath"
                        )]
                    )],
                    metadata=batch_mixins.CfnJobDefinitionPropsMixin.MetadataProperty(
                        labels=labels
                    ),
                    service_account_name="serviceAccountName",
                    share_process_namespace=False,
                    volumes=[batch_mixins.CfnJobDefinitionPropsMixin.EksVolumeProperty(
                        empty_dir=batch_mixins.CfnJobDefinitionPropsMixin.EmptyDirProperty(
                            medium="medium",
                            size_limit="sizeLimit"
                        ),
                        host_path=batch_mixins.CfnJobDefinitionPropsMixin.HostPathProperty(
                            path="path"
                        ),
                        name="name",
                        persistent_volume_claim=batch_mixins.CfnJobDefinitionPropsMixin.EksPersistentVolumeClaimProperty(
                            claim_name="claimName",
                            read_only=False
                        ),
                        secret=batch_mixins.CfnJobDefinitionPropsMixin.EksSecretProperty(
                            optional=False,
                            secret_name="secretName"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__de8c684be247f5ba54742ec8dea491caf11912a15415f2a76a90e85b591239d3)
                check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
                check_type(argname="argument dns_policy", value=dns_policy, expected_type=type_hints["dns_policy"])
                check_type(argname="argument host_network", value=host_network, expected_type=type_hints["host_network"])
                check_type(argname="argument image_pull_secrets", value=image_pull_secrets, expected_type=type_hints["image_pull_secrets"])
                check_type(argname="argument init_containers", value=init_containers, expected_type=type_hints["init_containers"])
                check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
                check_type(argname="argument service_account_name", value=service_account_name, expected_type=type_hints["service_account_name"])
                check_type(argname="argument share_process_namespace", value=share_process_namespace, expected_type=type_hints["share_process_namespace"])
                check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if containers is not None:
                self._values["containers"] = containers
            if dns_policy is not None:
                self._values["dns_policy"] = dns_policy
            if host_network is not None:
                self._values["host_network"] = host_network
            if image_pull_secrets is not None:
                self._values["image_pull_secrets"] = image_pull_secrets
            if init_containers is not None:
                self._values["init_containers"] = init_containers
            if metadata is not None:
                self._values["metadata"] = metadata
            if service_account_name is not None:
                self._values["service_account_name"] = service_account_name
            if share_process_namespace is not None:
                self._values["share_process_namespace"] = share_process_namespace
            if volumes is not None:
                self._values["volumes"] = volumes

        @builtins.property
        def containers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EksContainerProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-podproperties.html#cfn-batch-jobdefinition-podproperties-containers
            '''
            result = self._values.get("containers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EksContainerProperty"]]]], result)

        @builtins.property
        def dns_policy(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-podproperties.html#cfn-batch-jobdefinition-podproperties-dnspolicy
            '''
            result = self._values.get("dns_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def host_network(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-podproperties.html#cfn-batch-jobdefinition-podproperties-hostnetwork
            '''
            result = self._values.get("host_network")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def image_pull_secrets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.ImagePullSecretProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-podproperties.html#cfn-batch-jobdefinition-podproperties-imagepullsecrets
            '''
            result = self._values.get("image_pull_secrets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.ImagePullSecretProperty"]]]], result)

        @builtins.property
        def init_containers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EksContainerProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-podproperties.html#cfn-batch-jobdefinition-podproperties-initcontainers
            '''
            result = self._values.get("init_containers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EksContainerProperty"]]]], result)

        @builtins.property
        def metadata(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.MetadataProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-podproperties.html#cfn-batch-jobdefinition-podproperties-metadata
            '''
            result = self._values.get("metadata")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.MetadataProperty"]], result)

        @builtins.property
        def service_account_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-podproperties.html#cfn-batch-jobdefinition-podproperties-serviceaccountname
            '''
            result = self._values.get("service_account_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def share_process_namespace(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-podproperties.html#cfn-batch-jobdefinition-podproperties-shareprocessnamespace
            '''
            result = self._values.get("share_process_namespace")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def volumes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EksVolumeProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-podproperties.html#cfn-batch-jobdefinition-podproperties-volumes
            '''
            result = self._values.get("volumes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EksVolumeProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PodPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.RepositoryCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"credentials_parameter": "credentialsParameter"},
    )
    class RepositoryCredentialsProperty:
        def __init__(
            self,
            *,
            credentials_parameter: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The repository credentials for private registry authentication.

            :param credentials_parameter: The Amazon Resource Name (ARN) of the secret containing the private repository credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-repositorycredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                repository_credentials_property = batch_mixins.CfnJobDefinitionPropsMixin.RepositoryCredentialsProperty(
                    credentials_parameter="credentialsParameter"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__47d045ffdcd9d63fbc199d26009df6040bb36b1676bd5de1af71d140b6efadd1)
                check_type(argname="argument credentials_parameter", value=credentials_parameter, expected_type=type_hints["credentials_parameter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if credentials_parameter is not None:
                self._values["credentials_parameter"] = credentials_parameter

        @builtins.property
        def credentials_parameter(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the secret containing the private repository credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-repositorycredentials.html#cfn-batch-jobdefinition-repositorycredentials-credentialsparameter
            '''
            result = self._values.get("credentials_parameter")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RepositoryCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.ResourceRequirementProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class ResourceRequirementProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The type and amount of a resource to assign to a container.

            The supported resources include ``GPU`` , ``MEMORY`` , and ``VCPU`` .

            :param type: The type of resource to assign to a container. The supported resources include ``GPU`` , ``MEMORY`` , and ``VCPU`` .
            :param value: The quantity of the specified resource to reserve for the container. The values vary based on the ``type`` specified. - **type="GPU"** - The number of physical GPUs to reserve for the container. Make sure that the number of GPUs reserved for all containers in a job doesn't exceed the number of available GPUs on the compute resource that the job is launched on. .. epigraph:: GPUs aren't available for jobs that are running on Fargate resources. - **type="MEMORY"** - The memory hard limit (in MiB) present to the container. This parameter is supported for jobs that are running on Amazon EC2 resources. If your container attempts to exceed the memory specified, the container is terminated. This parameter maps to ``Memory`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--memory`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . You must specify at least 4 MiB of memory for a job. This is required but can be specified in several places for multi-node parallel (MNP) jobs. It must be specified for each node at least once. This parameter maps to ``Memory`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--memory`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . .. epigraph:: If you're trying to maximize your resource utilization by providing your jobs as much memory as possible for a particular instance type, see `Memory management <https://docs.aws.amazon.com/batch/latest/userguide/memory-management.html>`_ in the *AWS Batch User Guide* . For jobs that are running on Fargate resources, then ``value`` is the hard limit (in MiB), and must match one of the supported values and the ``VCPU`` values must be one of the values supported for that memory value. - **value = 512** - ``VCPU`` = 0.25 - **value = 1024** - ``VCPU`` = 0.25 or 0.5 - **value = 2048** - ``VCPU`` = 0.25, 0.5, or 1 - **value = 3072** - ``VCPU`` = 0.5, or 1 - **value = 4096** - ``VCPU`` = 0.5, 1, or 2 - **value = 5120, 6144, or 7168** - ``VCPU`` = 1 or 2 - **value = 8192** - ``VCPU`` = 1, 2, or 4 - **value = 9216, 10240, 11264, 12288, 13312, 14336, or 15360** - ``VCPU`` = 2 or 4 - **value = 16384** - ``VCPU`` = 2, 4, or 8 - **value = 17408, 18432, 19456, 21504, 22528, 23552, 25600, 26624, 27648, 29696, or 30720** - ``VCPU`` = 4 - **value = 20480, 24576, or 28672** - ``VCPU`` = 4 or 8 - **value = 36864, 45056, 53248, or 61440** - ``VCPU`` = 8 - **value = 32768, 40960, 49152, or 57344** - ``VCPU`` = 8 or 16 - **value = 65536, 73728, 81920, 90112, 98304, 106496, 114688, or 122880** - ``VCPU`` = 16 - **type="VCPU"** - The number of vCPUs reserved for the container. This parameter maps to ``CpuShares`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--cpu-shares`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . Each vCPU is equivalent to 1,024 CPU shares. For Amazon EC2 resources, you must specify at least one vCPU. This is required but can be specified in several places; it must be specified for each node at least once. The default for the Fargate On-Demand vCPU resource count quota is 6 vCPUs. For more information about Fargate quotas, see `AWS Fargate quotas <https://docs.aws.amazon.com/general/latest/gr/ecs-service.html#service-quotas-fargate>`_ in the *AWS General Reference* . For jobs that are running on Fargate resources, then ``value`` must match one of the supported values and the ``MEMORY`` values must be one of the values supported for that ``VCPU`` value. The supported values are 0.25, 0.5, 1, 2, 4, 8, and 16 - **value = 0.25** - ``MEMORY`` = 512, 1024, or 2048 - **value = 0.5** - ``MEMORY`` = 1024, 2048, 3072, or 4096 - **value = 1** - ``MEMORY`` = 2048, 3072, 4096, 5120, 6144, 7168, or 8192 - **value = 2** - ``MEMORY`` = 4096, 5120, 6144, 7168, 8192, 9216, 10240, 11264, 12288, 13312, 14336, 15360, or 16384 - **value = 4** - ``MEMORY`` = 8192, 9216, 10240, 11264, 12288, 13312, 14336, 15360, 16384, 17408, 18432, 19456, 20480, 21504, 22528, 23552, 24576, 25600, 26624, 27648, 28672, 29696, or 30720 - **value = 8** - ``MEMORY`` = 16384, 20480, 24576, 28672, 32768, 36864, 40960, 45056, 49152, 53248, 57344, or 61440 - **value = 16** - ``MEMORY`` = 32768, 40960, 49152, 57344, 65536, 73728, 81920, 90112, 98304, 106496, 114688, or 122880

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-resourcerequirement.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                resource_requirement_property = batch_mixins.CfnJobDefinitionPropsMixin.ResourceRequirementProperty(
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3945172c4385b4c0e69592db554109ed784e14468acdc15006c5067e539791a2)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of resource to assign to a container.

            The supported resources include ``GPU`` , ``MEMORY`` , and ``VCPU`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-resourcerequirement.html#cfn-batch-jobdefinition-resourcerequirement-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The quantity of the specified resource to reserve for the container. The values vary based on the ``type`` specified.

            - **type="GPU"** - The number of physical GPUs to reserve for the container. Make sure that the number of GPUs reserved for all containers in a job doesn't exceed the number of available GPUs on the compute resource that the job is launched on.

            .. epigraph::

               GPUs aren't available for jobs that are running on Fargate resources.

            - **type="MEMORY"** - The memory hard limit (in MiB) present to the container. This parameter is supported for jobs that are running on Amazon EC2 resources. If your container attempts to exceed the memory specified, the container is terminated. This parameter maps to ``Memory`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--memory`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . You must specify at least 4 MiB of memory for a job. This is required but can be specified in several places for multi-node parallel (MNP) jobs. It must be specified for each node at least once. This parameter maps to ``Memory`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--memory`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .

            .. epigraph::

               If you're trying to maximize your resource utilization by providing your jobs as much memory as possible for a particular instance type, see `Memory management <https://docs.aws.amazon.com/batch/latest/userguide/memory-management.html>`_ in the *AWS Batch User Guide* .

            For jobs that are running on Fargate resources, then ``value`` is the hard limit (in MiB), and must match one of the supported values and the ``VCPU`` values must be one of the values supported for that memory value.

            - **value = 512** - ``VCPU`` = 0.25
            - **value = 1024** - ``VCPU`` = 0.25 or 0.5
            - **value = 2048** - ``VCPU`` = 0.25, 0.5, or 1
            - **value = 3072** - ``VCPU`` = 0.5, or 1
            - **value = 4096** - ``VCPU`` = 0.5, 1, or 2
            - **value = 5120, 6144, or 7168** - ``VCPU`` = 1 or 2
            - **value = 8192** - ``VCPU`` = 1, 2, or 4
            - **value = 9216, 10240, 11264, 12288, 13312, 14336, or 15360** - ``VCPU`` = 2 or 4
            - **value = 16384** - ``VCPU`` = 2, 4, or 8
            - **value = 17408, 18432, 19456, 21504, 22528, 23552, 25600, 26624, 27648, 29696, or 30720** - ``VCPU`` = 4
            - **value = 20480, 24576, or 28672** - ``VCPU`` = 4 or 8
            - **value = 36864, 45056, 53248, or 61440** - ``VCPU`` = 8
            - **value = 32768, 40960, 49152, or 57344** - ``VCPU`` = 8 or 16
            - **value = 65536, 73728, 81920, 90112, 98304, 106496, 114688, or 122880** - ``VCPU`` = 16
            - **type="VCPU"** - The number of vCPUs reserved for the container. This parameter maps to ``CpuShares`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--cpu-shares`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . Each vCPU is equivalent to 1,024 CPU shares. For Amazon EC2 resources, you must specify at least one vCPU. This is required but can be specified in several places; it must be specified for each node at least once.

            The default for the Fargate On-Demand vCPU resource count quota is 6 vCPUs. For more information about Fargate quotas, see `AWS Fargate quotas <https://docs.aws.amazon.com/general/latest/gr/ecs-service.html#service-quotas-fargate>`_ in the *AWS General Reference* .

            For jobs that are running on Fargate resources, then ``value`` must match one of the supported values and the ``MEMORY`` values must be one of the values supported for that ``VCPU`` value. The supported values are 0.25, 0.5, 1, 2, 4, 8, and 16

            - **value = 0.25** - ``MEMORY`` = 512, 1024, or 2048
            - **value = 0.5** - ``MEMORY`` = 1024, 2048, 3072, or 4096
            - **value = 1** - ``MEMORY`` = 2048, 3072, 4096, 5120, 6144, 7168, or 8192
            - **value = 2** - ``MEMORY`` = 4096, 5120, 6144, 7168, 8192, 9216, 10240, 11264, 12288, 13312, 14336, 15360, or 16384
            - **value = 4** - ``MEMORY`` = 8192, 9216, 10240, 11264, 12288, 13312, 14336, 15360, 16384, 17408, 18432, 19456, 20480, 21504, 22528, 23552, 24576, 25600, 26624, 27648, 28672, 29696, or 30720
            - **value = 8** - ``MEMORY`` = 16384, 20480, 24576, 28672, 32768, 36864, 40960, 45056, 49152, 53248, 57344, or 61440
            - **value = 16** - ``MEMORY`` = 32768, 40960, 49152, 57344, 65536, 73728, 81920, 90112, 98304, 106496, 114688, or 122880

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-resourcerequirement.html#cfn-batch-jobdefinition-resourcerequirement-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceRequirementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.ResourceRetentionPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"skip_deregister_on_update": "skipDeregisterOnUpdate"},
    )
    class ResourceRetentionPolicyProperty:
        def __init__(
            self,
            *,
            skip_deregister_on_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Specifies the resource retention policy settings for a job definition.

            :param skip_deregister_on_update: Specifies whether the previous revision of the job definition is retained in an active status after UPDATE events for the resource. The default value is ``false`` . When the property is set to ``false`` , the previous revision of the job definition is de-registered after a new revision is created. When the property is set to ``true`` , the previous revision of the job definition is not de-registered. Default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-resourceretentionpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                resource_retention_policy_property = batch_mixins.CfnJobDefinitionPropsMixin.ResourceRetentionPolicyProperty(
                    skip_deregister_on_update=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__83cedf64bcbf85b1d7ff57df48c464ea08697dd6cd85ca6cc3699ef02622ddbf)
                check_type(argname="argument skip_deregister_on_update", value=skip_deregister_on_update, expected_type=type_hints["skip_deregister_on_update"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if skip_deregister_on_update is not None:
                self._values["skip_deregister_on_update"] = skip_deregister_on_update

        @builtins.property
        def skip_deregister_on_update(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the previous revision of the job definition is retained in an active status after UPDATE events for the resource.

            The default value is ``false`` . When the property is set to ``false`` , the previous revision of the job definition is de-registered after a new revision is created. When the property is set to ``true`` , the previous revision of the job definition is not de-registered.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-resourceretentionpolicy.html#cfn-batch-jobdefinition-resourceretentionpolicy-skipderegisteronupdate
            '''
            result = self._values.get("skip_deregister_on_update")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceRetentionPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.ResourcesProperty",
        jsii_struct_bases=[],
        name_mapping={"limits": "limits", "requests": "requests"},
    )
    class ResourcesProperty:
        def __init__(
            self,
            *,
            limits: typing.Any = None,
            requests: typing.Any = None,
        ) -> None:
            '''
            :param limits: 
            :param requests: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-resources.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                # limits: Any
                # requests: Any
                
                resources_property = batch_mixins.CfnJobDefinitionPropsMixin.ResourcesProperty(
                    limits=limits,
                    requests=requests
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3f45306336ff67b2bce51d0a63f161b784c9e00b4dfca83bbc69c98a2f4c368b)
                check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
                check_type(argname="argument requests", value=requests, expected_type=type_hints["requests"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if limits is not None:
                self._values["limits"] = limits
            if requests is not None:
                self._values["requests"] = requests

        @builtins.property
        def limits(self) -> typing.Any:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-resources.html#cfn-batch-jobdefinition-resources-limits
            '''
            result = self._values.get("limits")
            return typing.cast(typing.Any, result)

        @builtins.property
        def requests(self) -> typing.Any:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-resources.html#cfn-batch-jobdefinition-resources-requests
            '''
            result = self._values.get("requests")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourcesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.RetryStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={"attempts": "attempts", "evaluate_on_exit": "evaluateOnExit"},
    )
    class RetryStrategyProperty:
        def __init__(
            self,
            *,
            attempts: typing.Optional[jsii.Number] = None,
            evaluate_on_exit: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.EvaluateOnExitProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The retry strategy that's associated with a job.

            For more information, see `Automated job retries <https://docs.aws.amazon.com/batch/latest/userguide/job_retries.html>`_ in the *AWS Batch User Guide* .

            :param attempts: The number of times to move a job to the ``RUNNABLE`` status. You can specify between 1 and 10 attempts. If the value of ``attempts`` is greater than one, the job is retried on failure the same number of attempts as the value.
            :param evaluate_on_exit: Array of up to 5 objects that specify the conditions where jobs are retried or failed. If this parameter is specified, then the ``attempts`` parameter must also be specified. If none of the listed conditions match, then the job is retried.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-retrystrategy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                retry_strategy_property = batch_mixins.CfnJobDefinitionPropsMixin.RetryStrategyProperty(
                    attempts=123,
                    evaluate_on_exit=[batch_mixins.CfnJobDefinitionPropsMixin.EvaluateOnExitProperty(
                        action="action",
                        on_exit_code="onExitCode",
                        on_reason="onReason",
                        on_status_reason="onStatusReason"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__39ee6407c07cd343365710b06db5f74f78424c2464899dc11c859a661de3b071)
                check_type(argname="argument attempts", value=attempts, expected_type=type_hints["attempts"])
                check_type(argname="argument evaluate_on_exit", value=evaluate_on_exit, expected_type=type_hints["evaluate_on_exit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attempts is not None:
                self._values["attempts"] = attempts
            if evaluate_on_exit is not None:
                self._values["evaluate_on_exit"] = evaluate_on_exit

        @builtins.property
        def attempts(self) -> typing.Optional[jsii.Number]:
            '''The number of times to move a job to the ``RUNNABLE`` status.

            You can specify between 1 and 10 attempts. If the value of ``attempts`` is greater than one, the job is retried on failure the same number of attempts as the value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-retrystrategy.html#cfn-batch-jobdefinition-retrystrategy-attempts
            '''
            result = self._values.get("attempts")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def evaluate_on_exit(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EvaluateOnExitProperty"]]]]:
            '''Array of up to 5 objects that specify the conditions where jobs are retried or failed.

            If this parameter is specified, then the ``attempts`` parameter must also be specified. If none of the listed conditions match, then the job is retried.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-retrystrategy.html#cfn-batch-jobdefinition-retrystrategy-evaluateonexit
            '''
            result = self._values.get("evaluate_on_exit")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EvaluateOnExitProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetryStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.RuntimePlatformProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cpu_architecture": "cpuArchitecture",
            "operating_system_family": "operatingSystemFamily",
        },
    )
    class RuntimePlatformProperty:
        def __init__(
            self,
            *,
            cpu_architecture: typing.Optional[builtins.str] = None,
            operating_system_family: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the compute environment architecture for AWS Batch jobs on Fargate.

            :param cpu_architecture: The vCPU architecture. The default value is ``X86_64`` . Valid values are ``X86_64`` and ``ARM64`` . .. epigraph:: This parameter must be set to ``X86_64`` for Windows containers. > Fargate Spot is not supported on Windows-based containers on Fargate. A job queue will be blocked if a Windows job is submitted to a job queue with only Fargate Spot compute environments. However, you can attach both ``FARGATE`` and ``FARGATE_SPOT`` compute environments to the same job queue.
            :param operating_system_family: The operating system for the compute environment. Valid values are: ``LINUX`` (default), ``WINDOWS_SERVER_2019_CORE`` , ``WINDOWS_SERVER_2019_FULL`` , ``WINDOWS_SERVER_2022_CORE`` , and ``WINDOWS_SERVER_2022_FULL`` . .. epigraph:: The following parameters can’t be set for Windows containers: ``linuxParameters`` , ``privileged`` , ``user`` , ``ulimits`` , ``readonlyRootFilesystem`` , and ``efsVolumeConfiguration`` . > The AWS Batch Scheduler checks the compute environments that are attached to the job queue before registering a task definition with Fargate. In this scenario, the job queue is where the job is submitted. If the job requires a Windows container and the first compute environment is ``LINUX`` , the compute environment is skipped and the next compute environment is checked until a Windows-based compute environment is found. > Fargate Spot is not supported on Windows-based containers on Fargate. A job queue will be blocked if a Windows job is submitted to a job queue with only Fargate Spot compute environments. However, you can attach both ``FARGATE`` and ``FARGATE_SPOT`` compute environments to the same job queue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-runtimeplatform.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                runtime_platform_property = batch_mixins.CfnJobDefinitionPropsMixin.RuntimePlatformProperty(
                    cpu_architecture="cpuArchitecture",
                    operating_system_family="operatingSystemFamily"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9cb5f73fc44ae2f8b47a42723be41230dc78ef9f37e2023bd64ec95410b6bece)
                check_type(argname="argument cpu_architecture", value=cpu_architecture, expected_type=type_hints["cpu_architecture"])
                check_type(argname="argument operating_system_family", value=operating_system_family, expected_type=type_hints["operating_system_family"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cpu_architecture is not None:
                self._values["cpu_architecture"] = cpu_architecture
            if operating_system_family is not None:
                self._values["operating_system_family"] = operating_system_family

        @builtins.property
        def cpu_architecture(self) -> typing.Optional[builtins.str]:
            '''The vCPU architecture. The default value is ``X86_64`` . Valid values are ``X86_64`` and ``ARM64`` .

            .. epigraph::

               This parameter must be set to ``X86_64`` for Windows containers. > Fargate Spot is not supported on Windows-based containers on Fargate. A job queue will be blocked if a Windows job is submitted to a job queue with only Fargate Spot compute environments. However, you can attach both ``FARGATE`` and ``FARGATE_SPOT`` compute environments to the same job queue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-runtimeplatform.html#cfn-batch-jobdefinition-runtimeplatform-cpuarchitecture
            '''
            result = self._values.get("cpu_architecture")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operating_system_family(self) -> typing.Optional[builtins.str]:
            '''The operating system for the compute environment.

            Valid values are: ``LINUX`` (default), ``WINDOWS_SERVER_2019_CORE`` , ``WINDOWS_SERVER_2019_FULL`` , ``WINDOWS_SERVER_2022_CORE`` , and ``WINDOWS_SERVER_2022_FULL`` .
            .. epigraph::

               The following parameters can’t be set for Windows containers: ``linuxParameters`` , ``privileged`` , ``user`` , ``ulimits`` , ``readonlyRootFilesystem`` , and ``efsVolumeConfiguration`` . > The AWS Batch Scheduler checks the compute environments that are attached to the job queue before registering a task definition with Fargate. In this scenario, the job queue is where the job is submitted. If the job requires a Windows container and the first compute environment is ``LINUX`` , the compute environment is skipped and the next compute environment is checked until a Windows-based compute environment is found. > Fargate Spot is not supported on Windows-based containers on Fargate. A job queue will be blocked if a Windows job is submitted to a job queue with only Fargate Spot compute environments. However, you can attach both ``FARGATE`` and ``FARGATE_SPOT`` compute environments to the same job queue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-runtimeplatform.html#cfn-batch-jobdefinition-runtimeplatform-operatingsystemfamily
            '''
            result = self._values.get("operating_system_family")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuntimePlatformProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.SecretProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value_from": "valueFrom"},
    )
    class SecretProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value_from: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents the secret to expose to your container.

            Secrets can be exposed to a container in the following ways:

            - To inject sensitive data into your containers as environment variables, use the ``secrets`` container definition parameter.
            - To reference sensitive information in the log configuration of a container, use the ``secretOptions`` container definition parameter.

            For more information, see `Specifying sensitive data <https://docs.aws.amazon.com/batch/latest/userguide/specifying-sensitive-data.html>`_ in the *AWS Batch User Guide* .

            :param name: The name of the secret.
            :param value_from: The secret to expose to the container. The supported values are either the full Amazon Resource Name (ARN) of the AWS Secrets Manager secret or the full ARN of the parameter in the AWS Systems Manager Parameter Store. .. epigraph:: If the AWS Systems Manager Parameter Store parameter exists in the same Region as the job you're launching, then you can use either the full Amazon Resource Name (ARN) or name of the parameter. If the parameter exists in a different Region, then the full ARN must be specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-secret.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                secret_property = batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                    name="name",
                    value_from="valueFrom"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2652d6c60261cb148fbc6b388cc91d678c293dac6d990f01439c011163a2ef16)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value_from", value=value_from, expected_type=type_hints["value_from"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value_from is not None:
                self._values["value_from"] = value_from

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-secret.html#cfn-batch-jobdefinition-secret-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value_from(self) -> typing.Optional[builtins.str]:
            '''The secret to expose to the container.

            The supported values are either the full Amazon Resource Name (ARN) of the AWS Secrets Manager secret or the full ARN of the parameter in the AWS Systems Manager Parameter Store.
            .. epigraph::

               If the AWS Systems Manager Parameter Store parameter exists in the same Region as the job you're launching, then you can use either the full Amazon Resource Name (ARN) or name of the parameter. If the parameter exists in a different Region, then the full ARN must be specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-secret.html#cfn-batch-jobdefinition-secret-valuefrom
            '''
            result = self._values.get("value_from")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecretProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.SecurityContextProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_privilege_escalation": "allowPrivilegeEscalation",
            "privileged": "privileged",
            "read_only_root_filesystem": "readOnlyRootFilesystem",
            "run_as_group": "runAsGroup",
            "run_as_non_root": "runAsNonRoot",
            "run_as_user": "runAsUser",
        },
    )
    class SecurityContextProperty:
        def __init__(
            self,
            *,
            allow_privilege_escalation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            privileged: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            read_only_root_filesystem: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            run_as_group: typing.Optional[jsii.Number] = None,
            run_as_non_root: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            run_as_user: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param allow_privilege_escalation: 
            :param privileged: 
            :param read_only_root_filesystem: 
            :param run_as_group: 
            :param run_as_non_root: 
            :param run_as_user: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-securitycontext.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                security_context_property = batch_mixins.CfnJobDefinitionPropsMixin.SecurityContextProperty(
                    allow_privilege_escalation=False,
                    privileged=False,
                    read_only_root_filesystem=False,
                    run_as_group=123,
                    run_as_non_root=False,
                    run_as_user=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__440b15373aae3a2eeac026055d7ec32a15b5b7b9a05220647f0c0398dcf77b11)
                check_type(argname="argument allow_privilege_escalation", value=allow_privilege_escalation, expected_type=type_hints["allow_privilege_escalation"])
                check_type(argname="argument privileged", value=privileged, expected_type=type_hints["privileged"])
                check_type(argname="argument read_only_root_filesystem", value=read_only_root_filesystem, expected_type=type_hints["read_only_root_filesystem"])
                check_type(argname="argument run_as_group", value=run_as_group, expected_type=type_hints["run_as_group"])
                check_type(argname="argument run_as_non_root", value=run_as_non_root, expected_type=type_hints["run_as_non_root"])
                check_type(argname="argument run_as_user", value=run_as_user, expected_type=type_hints["run_as_user"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_privilege_escalation is not None:
                self._values["allow_privilege_escalation"] = allow_privilege_escalation
            if privileged is not None:
                self._values["privileged"] = privileged
            if read_only_root_filesystem is not None:
                self._values["read_only_root_filesystem"] = read_only_root_filesystem
            if run_as_group is not None:
                self._values["run_as_group"] = run_as_group
            if run_as_non_root is not None:
                self._values["run_as_non_root"] = run_as_non_root
            if run_as_user is not None:
                self._values["run_as_user"] = run_as_user

        @builtins.property
        def allow_privilege_escalation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-securitycontext.html#cfn-batch-jobdefinition-securitycontext-allowprivilegeescalation
            '''
            result = self._values.get("allow_privilege_escalation")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def privileged(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-securitycontext.html#cfn-batch-jobdefinition-securitycontext-privileged
            '''
            result = self._values.get("privileged")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def read_only_root_filesystem(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-securitycontext.html#cfn-batch-jobdefinition-securitycontext-readonlyrootfilesystem
            '''
            result = self._values.get("read_only_root_filesystem")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def run_as_group(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-securitycontext.html#cfn-batch-jobdefinition-securitycontext-runasgroup
            '''
            result = self._values.get("run_as_group")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def run_as_non_root(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-securitycontext.html#cfn-batch-jobdefinition-securitycontext-runasnonroot
            '''
            result = self._values.get("run_as_non_root")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def run_as_user(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-securitycontext.html#cfn-batch-jobdefinition-securitycontext-runasuser
            '''
            result = self._values.get("run_as_user")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecurityContextProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.TaskContainerDependencyProperty",
        jsii_struct_bases=[],
        name_mapping={"condition": "condition", "container_name": "containerName"},
    )
    class TaskContainerDependencyProperty:
        def __init__(
            self,
            *,
            condition: typing.Optional[builtins.str] = None,
            container_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A list of containers that this task depends on.

            :param condition: The dependency condition of the container. The following are the available conditions and their behavior:. - ``START`` - This condition emulates the behavior of links and volumes today. It validates that a dependent container is started before permitting other containers to start. - ``COMPLETE`` - This condition validates that a dependent container runs to completion (exits) before permitting other containers to start. This can be useful for nonessential containers that run a script and then exit. This condition can't be set on an essential container. - ``SUCCESS`` - This condition is the same as ``COMPLETE`` , but it also requires that the container exits with a zero status. This condition can't be set on an essential container.
            :param container_name: A unique identifier for the container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerdependency.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                task_container_dependency_property = batch_mixins.CfnJobDefinitionPropsMixin.TaskContainerDependencyProperty(
                    condition="condition",
                    container_name="containerName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__93bc1da4709753158a71b2b89d48018a9867fa8fb7517608b34864e601d2d613)
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
                check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if condition is not None:
                self._values["condition"] = condition
            if container_name is not None:
                self._values["container_name"] = container_name

        @builtins.property
        def condition(self) -> typing.Optional[builtins.str]:
            '''The dependency condition of the container. The following are the available conditions and their behavior:.

            - ``START`` - This condition emulates the behavior of links and volumes today. It validates that a dependent container is started before permitting other containers to start.
            - ``COMPLETE`` - This condition validates that a dependent container runs to completion (exits) before permitting other containers to start. This can be useful for nonessential containers that run a script and then exit. This condition can't be set on an essential container.
            - ``SUCCESS`` - This condition is the same as ``COMPLETE`` , but it also requires that the container exits with a zero status. This condition can't be set on an essential container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerdependency.html#cfn-batch-jobdefinition-taskcontainerdependency-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def container_name(self) -> typing.Optional[builtins.str]:
            '''A unique identifier for the container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerdependency.html#cfn-batch-jobdefinition-taskcontainerdependency-containername
            '''
            result = self._values.get("container_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskContainerDependencyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.TaskContainerPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "command": "command",
            "depends_on": "dependsOn",
            "environment": "environment",
            "essential": "essential",
            "firelens_configuration": "firelensConfiguration",
            "image": "image",
            "linux_parameters": "linuxParameters",
            "log_configuration": "logConfiguration",
            "mount_points": "mountPoints",
            "name": "name",
            "privileged": "privileged",
            "readonly_root_filesystem": "readonlyRootFilesystem",
            "repository_credentials": "repositoryCredentials",
            "resource_requirements": "resourceRequirements",
            "secrets": "secrets",
            "ulimits": "ulimits",
            "user": "user",
        },
    )
    class TaskContainerPropertiesProperty:
        def __init__(
            self,
            *,
            command: typing.Optional[typing.Sequence[builtins.str]] = None,
            depends_on: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.TaskContainerDependencyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.EnvironmentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            essential: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            firelens_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.FirelensConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            image: typing.Optional[builtins.str] = None,
            linux_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.LinuxParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            log_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.LogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            mount_points: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.MountPointProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            name: typing.Optional[builtins.str] = None,
            privileged: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            readonly_root_filesystem: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            repository_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.RepositoryCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resource_requirements: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.ResourceRequirementProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            secrets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.SecretProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ulimits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.UlimitProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            user: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Container properties are used for Amazon ECS-based job definitions.

            These properties to describe the container that's launched as part of a job.

            :param command: The command that's passed to the container. This parameter maps to ``Cmd`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``COMMAND`` parameter to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . For more information, see `Dockerfile reference: CMD <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/builder/#cmd>`_ .
            :param depends_on: A list of containers that this container depends on.
            :param environment: The environment variables to pass to a container. This parameter maps to Env in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--env`` parameter to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . .. epigraph:: We don't recommend using plaintext environment variables for sensitive information, such as credential data. > Environment variables cannot start with ``AWS_BATCH`` . This naming convention is reserved for variables that AWS Batch sets.
            :param essential: If the essential parameter of a container is marked as ``true`` , and that container fails or stops for any reason, all other containers that are part of the task are stopped. If the ``essential`` parameter of a container is marked as false, its failure doesn't affect the rest of the containers in a task. If this parameter is omitted, a container is assumed to be essential. All jobs must have at least one essential container. If you have an application that's composed of multiple containers, group containers that are used for a common purpose into components, and separate the different components into multiple task definitions. For more information, see `Application Architecture <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/application_architecture.html>`_ in the *Amazon Elastic Container Service Developer Guide* .
            :param firelens_configuration: The FireLens configuration for the container. This is used to specify and configure a log router for container logs. For more information, see `Custom log <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_firelens.html>`_ routing in the *Amazon Elastic Container Service Developer Guide* .
            :param image: The image used to start a container. This string is passed directly to the Docker daemon. By default, images in the Docker Hub registry are available. Other repositories are specified with either ``repository-url/image:tag`` or ``repository-url/image@digest`` . Up to 255 letters (uppercase and lowercase), numbers, hyphens, underscores, colons, periods, forward slashes, and number signs are allowed. This parameter maps to ``Image`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/#operation/ContainerCreate>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/>`_ and the ``IMAGE`` parameter of the `*docker run* <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/#security-configuration>`_ .
            :param linux_parameters: Linux-specific modifications that are applied to the container, such as Linux kernel capabilities. For more information, see `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`_ .
            :param log_configuration: The log configuration specification for the container. This parameter maps to ``LogConfig`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/#operation/ContainerCreate>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/>`_ and the ``--log-driver`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/#security-configuration>`_ . By default, containers use the same logging driver that the Docker daemon uses. However the container can use a different logging driver than the Docker daemon by specifying a log driver with this parameter in the container definition. To use a different logging driver for a container, the log system must be configured properly on the container instance (or on a different log server for remote logging options). For more information about the options for different supported log drivers, see `Configure logging drivers <https://docs.aws.amazon.com/https://docs.docker.com/engine/admin/logging/overview/>`_ in the *Docker documentation* . .. epigraph:: Amazon ECS currently supports a subset of the logging drivers available to the Docker daemon (shown in the ``LogConfiguration`` data type). Additional log drivers may be available in future releases of the Amazon ECS container agent. This parameter requires version 1.18 of the Docker Remote API or greater on your container instance. To check the Docker Remote API version on your container instance, log in to your container instance and run the following command: sudo docker version ``--format '{{.Server.APIVersion}}'`` .. epigraph:: The Amazon ECS container agent running on a container instance must register the logging drivers available on that instance with the ``ECS_AVAILABLE_LOGGING_DRIVERS`` environment variable before containers placed on that instance can use these log configuration options. For more information, see `Amazon ECS container agent configuration <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-config.html>`_ in the *Amazon Elastic Container Service Developer Guide* .
            :param mount_points: The mount points for data volumes in your container. This parameter maps to ``Volumes`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/#operation/ContainerCreate>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/>`_ and the `--volume <https://docs.aws.amazon.com/>`_ option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/#security-configuration>`_ . Windows containers can mount whole directories on the same drive as ``$env:ProgramData`` . Windows containers can't mount directories on a different drive, and mount point can't be across drives.
            :param name: The name of a container. The name can be used as a unique identifier to target your ``dependsOn`` and ``Overrides`` objects.
            :param privileged: When this parameter is ``true`` , the container is given elevated privileges on the host container instance (similar to the ``root`` user). This parameter maps to ``Privileged`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/#operation/ContainerCreate>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/>`_ and the ``--privileged`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/#security-configuration>`_ . .. epigraph:: This parameter is not supported for Windows containers or tasks run on Fargate.
            :param readonly_root_filesystem: When this parameter is true, the container is given read-only access to its root file system. This parameter maps to ``ReadonlyRootfs`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/#operation/ContainerCreate>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/>`_ and the ``--read-only`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/#security-configuration>`_ . .. epigraph:: This parameter is not supported for Windows containers.
            :param repository_credentials: The private repository authentication credentials to use.
            :param resource_requirements: The type and amount of a resource to assign to a container. The only supported resource is a GPU.
            :param secrets: The secrets to pass to the container. For more information, see `Specifying Sensitive Data <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/specifying-sensitive-data.html>`_ in the Amazon Elastic Container Service Developer Guide.
            :param ulimits: A list of ``ulimits`` to set in the container. If a ``ulimit`` value is specified in a task definition, it overrides the default values set by Docker. This parameter maps to ``Ulimits`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/#operation/ContainerCreate>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/>`_ and the ``--ulimit`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/#security-configuration>`_ . Amazon ECS tasks hosted on Fargate use the default resource limit values set by the operating system with the exception of the nofile resource limit parameter which Fargate overrides. The ``nofile`` resource limit sets a restriction on the number of open files that a container can use. The default ``nofile`` soft limit is ``1024`` and the default hard limit is ``65535`` . This parameter requires version 1.18 of the Docker Remote API or greater on your container instance. To check the Docker Remote API version on your container instance, log in to your container instance and run the following command: sudo docker version ``--format '{{.Server.APIVersion}}'`` .. epigraph:: This parameter is not supported for Windows containers.
            :param user: The user to use inside the container. This parameter maps to User in the Create a container section of the Docker Remote API and the --user option to docker run. .. epigraph:: When running tasks using the ``host`` network mode, don't run containers using the ``root user (UID 0)`` . We recommend using a non-root user for better security. You can specify the ``user`` using the following formats. If specifying a UID or GID, you must specify it as a positive integer. - ``user`` - ``user:group`` - ``uid`` - ``uid:gid`` - ``user:gi`` - ``uid:group`` .. epigraph:: This parameter is not supported for Windows containers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                # options: Any
                
                task_container_properties_property = batch_mixins.CfnJobDefinitionPropsMixin.TaskContainerPropertiesProperty(
                    command=["command"],
                    depends_on=[batch_mixins.CfnJobDefinitionPropsMixin.TaskContainerDependencyProperty(
                        condition="condition",
                        container_name="containerName"
                    )],
                    environment=[batch_mixins.CfnJobDefinitionPropsMixin.EnvironmentProperty(
                        name="name",
                        value="value"
                    )],
                    essential=False,
                    firelens_configuration=batch_mixins.CfnJobDefinitionPropsMixin.FirelensConfigurationProperty(
                        options={
                            "options_key": "options"
                        },
                        type="type"
                    ),
                    image="image",
                    linux_parameters=batch_mixins.CfnJobDefinitionPropsMixin.LinuxParametersProperty(
                        devices=[batch_mixins.CfnJobDefinitionPropsMixin.DeviceProperty(
                            container_path="containerPath",
                            host_path="hostPath",
                            permissions=["permissions"]
                        )],
                        init_process_enabled=False,
                        max_swap=123,
                        shared_memory_size=123,
                        swappiness=123,
                        tmpfs=[batch_mixins.CfnJobDefinitionPropsMixin.TmpfsProperty(
                            container_path="containerPath",
                            mount_options=["mountOptions"],
                            size=123
                        )]
                    ),
                    log_configuration=batch_mixins.CfnJobDefinitionPropsMixin.LogConfigurationProperty(
                        log_driver="logDriver",
                        options=options,
                        secret_options=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                            name="name",
                            value_from="valueFrom"
                        )]
                    ),
                    mount_points=[batch_mixins.CfnJobDefinitionPropsMixin.MountPointProperty(
                        container_path="containerPath",
                        read_only=False,
                        source_volume="sourceVolume"
                    )],
                    name="name",
                    privileged=False,
                    readonly_root_filesystem=False,
                    repository_credentials=batch_mixins.CfnJobDefinitionPropsMixin.RepositoryCredentialsProperty(
                        credentials_parameter="credentialsParameter"
                    ),
                    resource_requirements=[batch_mixins.CfnJobDefinitionPropsMixin.ResourceRequirementProperty(
                        type="type",
                        value="value"
                    )],
                    secrets=[batch_mixins.CfnJobDefinitionPropsMixin.SecretProperty(
                        name="name",
                        value_from="valueFrom"
                    )],
                    ulimits=[batch_mixins.CfnJobDefinitionPropsMixin.UlimitProperty(
                        hard_limit=123,
                        name="name",
                        soft_limit=123
                    )],
                    user="user"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__871ff1f8637d018c37cf9ddd4858e5988a0dd510d6c910b837dc04545a04c902)
                check_type(argname="argument command", value=command, expected_type=type_hints["command"])
                check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
                check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
                check_type(argname="argument essential", value=essential, expected_type=type_hints["essential"])
                check_type(argname="argument firelens_configuration", value=firelens_configuration, expected_type=type_hints["firelens_configuration"])
                check_type(argname="argument image", value=image, expected_type=type_hints["image"])
                check_type(argname="argument linux_parameters", value=linux_parameters, expected_type=type_hints["linux_parameters"])
                check_type(argname="argument log_configuration", value=log_configuration, expected_type=type_hints["log_configuration"])
                check_type(argname="argument mount_points", value=mount_points, expected_type=type_hints["mount_points"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument privileged", value=privileged, expected_type=type_hints["privileged"])
                check_type(argname="argument readonly_root_filesystem", value=readonly_root_filesystem, expected_type=type_hints["readonly_root_filesystem"])
                check_type(argname="argument repository_credentials", value=repository_credentials, expected_type=type_hints["repository_credentials"])
                check_type(argname="argument resource_requirements", value=resource_requirements, expected_type=type_hints["resource_requirements"])
                check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
                check_type(argname="argument ulimits", value=ulimits, expected_type=type_hints["ulimits"])
                check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if command is not None:
                self._values["command"] = command
            if depends_on is not None:
                self._values["depends_on"] = depends_on
            if environment is not None:
                self._values["environment"] = environment
            if essential is not None:
                self._values["essential"] = essential
            if firelens_configuration is not None:
                self._values["firelens_configuration"] = firelens_configuration
            if image is not None:
                self._values["image"] = image
            if linux_parameters is not None:
                self._values["linux_parameters"] = linux_parameters
            if log_configuration is not None:
                self._values["log_configuration"] = log_configuration
            if mount_points is not None:
                self._values["mount_points"] = mount_points
            if name is not None:
                self._values["name"] = name
            if privileged is not None:
                self._values["privileged"] = privileged
            if readonly_root_filesystem is not None:
                self._values["readonly_root_filesystem"] = readonly_root_filesystem
            if repository_credentials is not None:
                self._values["repository_credentials"] = repository_credentials
            if resource_requirements is not None:
                self._values["resource_requirements"] = resource_requirements
            if secrets is not None:
                self._values["secrets"] = secrets
            if ulimits is not None:
                self._values["ulimits"] = ulimits
            if user is not None:
                self._values["user"] = user

        @builtins.property
        def command(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The command that's passed to the container.

            This parameter maps to ``Cmd`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``COMMAND`` parameter to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . For more information, see `Dockerfile reference: CMD <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/builder/#cmd>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerproperties.html#cfn-batch-jobdefinition-taskcontainerproperties-command
            '''
            result = self._values.get("command")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def depends_on(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.TaskContainerDependencyProperty"]]]]:
            '''A list of containers that this container depends on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerproperties.html#cfn-batch-jobdefinition-taskcontainerproperties-dependson
            '''
            result = self._values.get("depends_on")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.TaskContainerDependencyProperty"]]]], result)

        @builtins.property
        def environment(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EnvironmentProperty"]]]]:
            '''The environment variables to pass to a container.

            This parameter maps to Env in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--env`` parameter to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .
            .. epigraph::

               We don't recommend using plaintext environment variables for sensitive information, such as credential data. > Environment variables cannot start with ``AWS_BATCH`` . This naming convention is reserved for variables that AWS Batch sets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerproperties.html#cfn-batch-jobdefinition-taskcontainerproperties-environment
            '''
            result = self._values.get("environment")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EnvironmentProperty"]]]], result)

        @builtins.property
        def essential(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If the essential parameter of a container is marked as ``true`` , and that container fails or stops for any reason, all other containers that are part of the task are stopped.

            If the ``essential`` parameter of a container is marked as false, its failure doesn't affect the rest of the containers in a task. If this parameter is omitted, a container is assumed to be essential.

            All jobs must have at least one essential container. If you have an application that's composed of multiple containers, group containers that are used for a common purpose into components, and separate the different components into multiple task definitions. For more information, see `Application Architecture <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/application_architecture.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerproperties.html#cfn-batch-jobdefinition-taskcontainerproperties-essential
            '''
            result = self._values.get("essential")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def firelens_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.FirelensConfigurationProperty"]]:
            '''The FireLens configuration for the container.

            This is used to specify and configure a log router for container logs. For more information, see `Custom log <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_firelens.html>`_ routing in the *Amazon Elastic Container Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerproperties.html#cfn-batch-jobdefinition-taskcontainerproperties-firelensconfiguration
            '''
            result = self._values.get("firelens_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.FirelensConfigurationProperty"]], result)

        @builtins.property
        def image(self) -> typing.Optional[builtins.str]:
            '''The image used to start a container.

            This string is passed directly to the Docker daemon. By default, images in the Docker Hub registry are available. Other repositories are specified with either ``repository-url/image:tag`` or ``repository-url/image@digest`` . Up to 255 letters (uppercase and lowercase), numbers, hyphens, underscores, colons, periods, forward slashes, and number signs are allowed. This parameter maps to ``Image`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/#operation/ContainerCreate>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/>`_ and the ``IMAGE`` parameter of the `*docker run* <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/#security-configuration>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerproperties.html#cfn-batch-jobdefinition-taskcontainerproperties-image
            '''
            result = self._values.get("image")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def linux_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.LinuxParametersProperty"]]:
            '''Linux-specific modifications that are applied to the container, such as Linux kernel capabilities.

            For more information, see `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerproperties.html#cfn-batch-jobdefinition-taskcontainerproperties-linuxparameters
            '''
            result = self._values.get("linux_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.LinuxParametersProperty"]], result)

        @builtins.property
        def log_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.LogConfigurationProperty"]]:
            '''The log configuration specification for the container.

            This parameter maps to ``LogConfig`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/#operation/ContainerCreate>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/>`_ and the ``--log-driver`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/#security-configuration>`_ .

            By default, containers use the same logging driver that the Docker daemon uses. However the container can use a different logging driver than the Docker daemon by specifying a log driver with this parameter in the container definition. To use a different logging driver for a container, the log system must be configured properly on the container instance (or on a different log server for remote logging options). For more information about the options for different supported log drivers, see `Configure logging drivers <https://docs.aws.amazon.com/https://docs.docker.com/engine/admin/logging/overview/>`_ in the *Docker documentation* .
            .. epigraph::

               Amazon ECS currently supports a subset of the logging drivers available to the Docker daemon (shown in the ``LogConfiguration`` data type). Additional log drivers may be available in future releases of the Amazon ECS container agent.

            This parameter requires version 1.18 of the Docker Remote API or greater on your container instance. To check the Docker Remote API version on your container instance, log in to your container instance and run the following command: sudo docker version ``--format '{{.Server.APIVersion}}'``
            .. epigraph::

               The Amazon ECS container agent running on a container instance must register the logging drivers available on that instance with the ``ECS_AVAILABLE_LOGGING_DRIVERS`` environment variable before containers placed on that instance can use these log configuration options. For more information, see `Amazon ECS container agent configuration <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-config.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerproperties.html#cfn-batch-jobdefinition-taskcontainerproperties-logconfiguration
            '''
            result = self._values.get("log_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.LogConfigurationProperty"]], result)

        @builtins.property
        def mount_points(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.MountPointProperty"]]]]:
            '''The mount points for data volumes in your container.

            This parameter maps to ``Volumes`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/#operation/ContainerCreate>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/>`_ and the `--volume <https://docs.aws.amazon.com/>`_ option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/#security-configuration>`_ .

            Windows containers can mount whole directories on the same drive as ``$env:ProgramData`` . Windows containers can't mount directories on a different drive, and mount point can't be across drives.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerproperties.html#cfn-batch-jobdefinition-taskcontainerproperties-mountpoints
            '''
            result = self._values.get("mount_points")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.MountPointProperty"]]]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of a container.

            The name can be used as a unique identifier to target your ``dependsOn`` and ``Overrides`` objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerproperties.html#cfn-batch-jobdefinition-taskcontainerproperties-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def privileged(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When this parameter is ``true`` , the container is given elevated privileges on the host container instance (similar to the ``root`` user).

            This parameter maps to ``Privileged`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/#operation/ContainerCreate>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/>`_ and the ``--privileged`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/#security-configuration>`_ .
            .. epigraph::

               This parameter is not supported for Windows containers or tasks run on Fargate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerproperties.html#cfn-batch-jobdefinition-taskcontainerproperties-privileged
            '''
            result = self._values.get("privileged")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def readonly_root_filesystem(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When this parameter is true, the container is given read-only access to its root file system.

            This parameter maps to ``ReadonlyRootfs`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/#operation/ContainerCreate>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/>`_ and the ``--read-only`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/#security-configuration>`_ .
            .. epigraph::

               This parameter is not supported for Windows containers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerproperties.html#cfn-batch-jobdefinition-taskcontainerproperties-readonlyrootfilesystem
            '''
            result = self._values.get("readonly_root_filesystem")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def repository_credentials(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.RepositoryCredentialsProperty"]]:
            '''The private repository authentication credentials to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerproperties.html#cfn-batch-jobdefinition-taskcontainerproperties-repositorycredentials
            '''
            result = self._values.get("repository_credentials")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.RepositoryCredentialsProperty"]], result)

        @builtins.property
        def resource_requirements(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.ResourceRequirementProperty"]]]]:
            '''The type and amount of a resource to assign to a container.

            The only supported resource is a GPU.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerproperties.html#cfn-batch-jobdefinition-taskcontainerproperties-resourcerequirements
            '''
            result = self._values.get("resource_requirements")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.ResourceRequirementProperty"]]]], result)

        @builtins.property
        def secrets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.SecretProperty"]]]]:
            '''The secrets to pass to the container.

            For more information, see `Specifying Sensitive Data <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/specifying-sensitive-data.html>`_ in the Amazon Elastic Container Service Developer Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerproperties.html#cfn-batch-jobdefinition-taskcontainerproperties-secrets
            '''
            result = self._values.get("secrets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.SecretProperty"]]]], result)

        @builtins.property
        def ulimits(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.UlimitProperty"]]]]:
            '''A list of ``ulimits`` to set in the container.

            If a ``ulimit`` value is specified in a task definition, it overrides the default values set by Docker. This parameter maps to ``Ulimits`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/#operation/ContainerCreate>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.35/>`_ and the ``--ulimit`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/#security-configuration>`_ .

            Amazon ECS tasks hosted on Fargate use the default resource limit values set by the operating system with the exception of the nofile resource limit parameter which Fargate overrides. The ``nofile`` resource limit sets a restriction on the number of open files that a container can use. The default ``nofile`` soft limit is ``1024`` and the default hard limit is ``65535`` .

            This parameter requires version 1.18 of the Docker Remote API or greater on your container instance. To check the Docker Remote API version on your container instance, log in to your container instance and run the following command: sudo docker version ``--format '{{.Server.APIVersion}}'``
            .. epigraph::

               This parameter is not supported for Windows containers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerproperties.html#cfn-batch-jobdefinition-taskcontainerproperties-ulimits
            '''
            result = self._values.get("ulimits")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.UlimitProperty"]]]], result)

        @builtins.property
        def user(self) -> typing.Optional[builtins.str]:
            '''The user to use inside the container.

            This parameter maps to User in the Create a container section of the Docker Remote API and the --user option to docker run.
            .. epigraph::

               When running tasks using the ``host`` network mode, don't run containers using the ``root user (UID 0)`` . We recommend using a non-root user for better security.

            You can specify the ``user`` using the following formats. If specifying a UID or GID, you must specify it as a positive integer.

            - ``user``
            - ``user:group``
            - ``uid``
            - ``uid:gid``
            - ``user:gi``
            - ``uid:group``

            .. epigraph::

               This parameter is not supported for Windows containers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-taskcontainerproperties.html#cfn-batch-jobdefinition-taskcontainerproperties-user
            '''
            result = self._values.get("user")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskContainerPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.TimeoutProperty",
        jsii_struct_bases=[],
        name_mapping={"attempt_duration_seconds": "attemptDurationSeconds"},
    )
    class TimeoutProperty:
        def __init__(
            self,
            *,
            attempt_duration_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param attempt_duration_seconds: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-timeout.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                timeout_property = batch_mixins.CfnJobDefinitionPropsMixin.TimeoutProperty(
                    attempt_duration_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3e8a72f0c7f821c60934e108c04d4da77e24b93a2eb90ee2dfd23197642d3466)
                check_type(argname="argument attempt_duration_seconds", value=attempt_duration_seconds, expected_type=type_hints["attempt_duration_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attempt_duration_seconds is not None:
                self._values["attempt_duration_seconds"] = attempt_duration_seconds

        @builtins.property
        def attempt_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-timeout.html#cfn-batch-jobdefinition-timeout-attemptdurationseconds
            '''
            result = self._values.get("attempt_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeoutProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.TmpfsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "container_path": "containerPath",
            "mount_options": "mountOptions",
            "size": "size",
        },
    )
    class TmpfsProperty:
        def __init__(
            self,
            *,
            container_path: typing.Optional[builtins.str] = None,
            mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
            size: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The container path, mount options, and size of the ``tmpfs`` mount.

            .. epigraph::

               This object isn't applicable to jobs that are running on Fargate resources.

            :param container_path: The absolute file path in the container where the ``tmpfs`` volume is mounted.
            :param mount_options: The list of ``tmpfs`` volume mount options. Valid values: " ``defaults`` " | " ``ro`` " | " ``rw`` " | " ``suid`` " | " ``nosuid`` " | " ``dev`` " | " ``nodev`` " | " ``exec`` " | " ``noexec`` " | " ``sync`` " | " ``async`` " | " ``dirsync`` " | " ``remount`` " | " ``mand`` " | " ``nomand`` " | " ``atime`` " | " ``noatime`` " | " ``diratime`` " | " ``nodiratime`` " | " ``bind`` " | " ``rbind" | "unbindable" | "runbindable" | "private" | "rprivate" | "shared" | "rshared" | "slave" | "rslave" | "relatime`` " | " ``norelatime`` " | " ``strictatime`` " | " ``nostrictatime`` " | " ``mode`` " | " ``uid`` " | " ``gid`` " | " ``nr_inodes`` " | " ``nr_blocks`` " | " ``mpol`` "
            :param size: The size (in MiB) of the ``tmpfs`` volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-tmpfs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                tmpfs_property = batch_mixins.CfnJobDefinitionPropsMixin.TmpfsProperty(
                    container_path="containerPath",
                    mount_options=["mountOptions"],
                    size=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bf64c3f8e3b4b5c2435f9d8191b9657d7f20e6b122222a2e3302bf3a964103c4)
                check_type(argname="argument container_path", value=container_path, expected_type=type_hints["container_path"])
                check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
                check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if container_path is not None:
                self._values["container_path"] = container_path
            if mount_options is not None:
                self._values["mount_options"] = mount_options
            if size is not None:
                self._values["size"] = size

        @builtins.property
        def container_path(self) -> typing.Optional[builtins.str]:
            '''The absolute file path in the container where the ``tmpfs`` volume is mounted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-tmpfs.html#cfn-batch-jobdefinition-tmpfs-containerpath
            '''
            result = self._values.get("container_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mount_options(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of ``tmpfs`` volume mount options.

            Valid values: " ``defaults`` " | " ``ro`` " | " ``rw`` " | " ``suid`` " | " ``nosuid`` " | " ``dev`` " | " ``nodev`` " | " ``exec`` " | " ``noexec`` " | " ``sync`` " | " ``async`` " | " ``dirsync`` " | " ``remount`` " | " ``mand`` " | " ``nomand`` " | " ``atime`` " | " ``noatime`` " | " ``diratime`` " | " ``nodiratime`` " | " ``bind`` " | " ``rbind" | "unbindable" | "runbindable" | "private" | "rprivate" | "shared" | "rshared" | "slave" | "rslave" | "relatime`` " | " ``norelatime`` " | " ``strictatime`` " | " ``nostrictatime`` " | " ``mode`` " | " ``uid`` " | " ``gid`` " | " ``nr_inodes`` " | " ``nr_blocks`` " | " ``mpol`` "

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-tmpfs.html#cfn-batch-jobdefinition-tmpfs-mountoptions
            '''
            result = self._values.get("mount_options")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def size(self) -> typing.Optional[jsii.Number]:
            '''The size (in MiB) of the ``tmpfs`` volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-tmpfs.html#cfn-batch-jobdefinition-tmpfs-size
            '''
            result = self._values.get("size")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TmpfsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.UlimitProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hard_limit": "hardLimit",
            "name": "name",
            "soft_limit": "softLimit",
        },
    )
    class UlimitProperty:
        def __init__(
            self,
            *,
            hard_limit: typing.Optional[jsii.Number] = None,
            name: typing.Optional[builtins.str] = None,
            soft_limit: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The ``ulimit`` settings to pass to the container. For more information, see `Ulimit <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_Ulimit.html>`_ .

            .. epigraph::

               This object isn't applicable to jobs that are running on Fargate resources.

            :param hard_limit: The hard limit for the ``ulimit`` type.
            :param name: The ``type`` of the ``ulimit`` . Valid values are: ``core`` | ``cpu`` | ``data`` | ``fsize`` | ``locks`` | ``memlock`` | ``msgqueue`` | ``nice`` | ``nofile`` | ``nproc`` | ``rss`` | ``rtprio`` | ``rttime`` | ``sigpending`` | ``stack`` .
            :param soft_limit: The soft limit for the ``ulimit`` type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ulimit.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                ulimit_property = batch_mixins.CfnJobDefinitionPropsMixin.UlimitProperty(
                    hard_limit=123,
                    name="name",
                    soft_limit=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cb6820461a55e970afdf8747c17246f0a307f716a0f871aeda35ee14612765d3)
                check_type(argname="argument hard_limit", value=hard_limit, expected_type=type_hints["hard_limit"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument soft_limit", value=soft_limit, expected_type=type_hints["soft_limit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hard_limit is not None:
                self._values["hard_limit"] = hard_limit
            if name is not None:
                self._values["name"] = name
            if soft_limit is not None:
                self._values["soft_limit"] = soft_limit

        @builtins.property
        def hard_limit(self) -> typing.Optional[jsii.Number]:
            '''The hard limit for the ``ulimit`` type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ulimit.html#cfn-batch-jobdefinition-ulimit-hardlimit
            '''
            result = self._values.get("hard_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The ``type`` of the ``ulimit`` .

            Valid values are: ``core`` | ``cpu`` | ``data`` | ``fsize`` | ``locks`` | ``memlock`` | ``msgqueue`` | ``nice`` | ``nofile`` | ``nproc`` | ``rss`` | ``rtprio`` | ``rttime`` | ``sigpending`` | ``stack`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ulimit.html#cfn-batch-jobdefinition-ulimit-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def soft_limit(self) -> typing.Optional[jsii.Number]:
            '''The soft limit for the ``ulimit`` type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ulimit.html#cfn-batch-jobdefinition-ulimit-softlimit
            '''
            result = self._values.get("soft_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UlimitProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.VolumesHostProperty",
        jsii_struct_bases=[],
        name_mapping={"source_path": "sourcePath"},
    )
    class VolumesHostProperty:
        def __init__(
            self,
            *,
            source_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param source_path: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumeshost.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                volumes_host_property = batch_mixins.CfnJobDefinitionPropsMixin.VolumesHostProperty(
                    source_path="sourcePath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e50a5e660ff7a2db2d48b265496dda126e4e9f841e5c3ba42d791256dfc4e61d)
                check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source_path is not None:
                self._values["source_path"] = source_path

        @builtins.property
        def source_path(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumeshost.html#cfn-batch-jobdefinition-volumeshost-sourcepath
            '''
            result = self._values.get("source_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VolumesHostProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobDefinitionPropsMixin.VolumesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "efs_volume_configuration": "efsVolumeConfiguration",
            "host": "host",
            "name": "name",
        },
    )
    class VolumesProperty:
        def __init__(
            self,
            *,
            efs_volume_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.EfsVolumeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            host: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobDefinitionPropsMixin.VolumesHostProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param efs_volume_configuration: 
            :param host: 
            :param name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                volumes_property = batch_mixins.CfnJobDefinitionPropsMixin.VolumesProperty(
                    efs_volume_configuration=batch_mixins.CfnJobDefinitionPropsMixin.EfsVolumeConfigurationProperty(
                        authorization_config=batch_mixins.CfnJobDefinitionPropsMixin.AuthorizationConfigProperty(
                            access_point_id="accessPointId",
                            iam="iam"
                        ),
                        file_system_id="fileSystemId",
                        root_directory="rootDirectory",
                        transit_encryption="transitEncryption",
                        transit_encryption_port=123
                    ),
                    host=batch_mixins.CfnJobDefinitionPropsMixin.VolumesHostProperty(
                        source_path="sourcePath"
                    ),
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1312b6393d87d551f43f65671f23eac8d0abc996e6e98e677c24ec7af387442e)
                check_type(argname="argument efs_volume_configuration", value=efs_volume_configuration, expected_type=type_hints["efs_volume_configuration"])
                check_type(argname="argument host", value=host, expected_type=type_hints["host"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if efs_volume_configuration is not None:
                self._values["efs_volume_configuration"] = efs_volume_configuration
            if host is not None:
                self._values["host"] = host
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def efs_volume_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EfsVolumeConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumes.html#cfn-batch-jobdefinition-volumes-efsvolumeconfiguration
            '''
            result = self._values.get("efs_volume_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.EfsVolumeConfigurationProperty"]], result)

        @builtins.property
        def host(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.VolumesHostProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumes.html#cfn-batch-jobdefinition-volumes-host
            '''
            result = self._values.get("host")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobDefinitionPropsMixin.VolumesHostProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumes.html#cfn-batch-jobdefinition-volumes-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VolumesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobQueueMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_environment_order": "computeEnvironmentOrder",
        "job_queue_name": "jobQueueName",
        "job_queue_type": "jobQueueType",
        "job_state_time_limit_actions": "jobStateTimeLimitActions",
        "priority": "priority",
        "scheduling_policy_arn": "schedulingPolicyArn",
        "service_environment_order": "serviceEnvironmentOrder",
        "state": "state",
        "tags": "tags",
    },
)
class CfnJobQueueMixinProps:
    def __init__(
        self,
        *,
        compute_environment_order: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobQueuePropsMixin.ComputeEnvironmentOrderProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        job_queue_name: typing.Optional[builtins.str] = None,
        job_queue_type: typing.Optional[builtins.str] = None,
        job_state_time_limit_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobQueuePropsMixin.JobStateTimeLimitActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        priority: typing.Optional[jsii.Number] = None,
        scheduling_policy_arn: typing.Optional[builtins.str] = None,
        service_environment_order: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobQueuePropsMixin.ServiceEnvironmentOrderProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnJobQueuePropsMixin.

        :param compute_environment_order: The set of compute environments mapped to a job queue and their order relative to each other. The job scheduler uses this parameter to determine which compute environment runs a specific job. Compute environments must be in the ``VALID`` state before you can associate them with a job queue. You can associate up to three compute environments with a job queue. All of the compute environments must be either EC2 ( ``EC2`` or ``SPOT`` ) or Fargate ( ``FARGATE`` or ``FARGATE_SPOT`` ); EC2 and Fargate compute environments can't be mixed. .. epigraph:: All compute environments that are associated with a job queue must share the same architecture. AWS Batch doesn't support mixing compute environment architecture types in a single job queue.
        :param job_queue_name: The name of the job queue. It can be up to 128 letters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_).
        :param job_queue_type: The type of job queue. For service jobs that run on SageMaker AI , this value is ``SAGEMAKER_TRAINING`` . For regular container jobs, this value is ``EKS`` , ``ECS`` , or ``ECS_FARGATE`` depending on the compute environment.
        :param job_state_time_limit_actions: The set of actions that AWS Batch perform on jobs that remain at the head of the job queue in the specified state longer than specified times. AWS Batch will perform each action after ``maxTimeSeconds`` has passed.
        :param priority: The priority of the job queue. Job queues with a higher priority (or a higher integer value for the ``priority`` parameter) are evaluated first when associated with the same compute environment. Priority is determined in descending order. For example, a job queue with a priority value of ``10`` is given scheduling preference over a job queue with a priority value of ``1`` . All of the compute environments must be either EC2 ( ``EC2`` or ``SPOT`` ) or Fargate ( ``FARGATE`` or ``FARGATE_SPOT`` ); EC2 and Fargate compute environments can't be mixed.
        :param scheduling_policy_arn: The Amazon Resource Name (ARN) of the scheduling policy. The format is ``aws: *Partition* :batch: *Region* : *Account* :scheduling-policy/ *Name*`` . For example, ``aws:aws:batch:us-west-2:123456789012:scheduling-policy/MySchedulingPolicy`` .
        :param service_environment_order: The order of the service environment associated with the job queue. Job queues with a higher priority are evaluated first when associated with the same service environment.
        :param state: The state of the job queue. If the job queue state is ``ENABLED`` , it is able to accept jobs. If the job queue state is ``DISABLED`` , new jobs can't be added to the queue, but jobs already in the queue can finish.
        :param tags: The tags that are applied to the job queue. For more information, see `Tagging your AWS Batch resources <https://docs.aws.amazon.com/batch/latest/userguide/using-tags.html>`_ in *AWS Batch User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
            
            cfn_job_queue_mixin_props = batch_mixins.CfnJobQueueMixinProps(
                compute_environment_order=[batch_mixins.CfnJobQueuePropsMixin.ComputeEnvironmentOrderProperty(
                    compute_environment="computeEnvironment",
                    order=123
                )],
                job_queue_name="jobQueueName",
                job_queue_type="jobQueueType",
                job_state_time_limit_actions=[batch_mixins.CfnJobQueuePropsMixin.JobStateTimeLimitActionProperty(
                    action="action",
                    max_time_seconds=123,
                    reason="reason",
                    state="state"
                )],
                priority=123,
                scheduling_policy_arn="schedulingPolicyArn",
                service_environment_order=[batch_mixins.CfnJobQueuePropsMixin.ServiceEnvironmentOrderProperty(
                    order=123,
                    service_environment="serviceEnvironment"
                )],
                state="state",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fdc49293e384619d9764cb0337780eaa82c560d0031c3e934ba03a11185109c)
            check_type(argname="argument compute_environment_order", value=compute_environment_order, expected_type=type_hints["compute_environment_order"])
            check_type(argname="argument job_queue_name", value=job_queue_name, expected_type=type_hints["job_queue_name"])
            check_type(argname="argument job_queue_type", value=job_queue_type, expected_type=type_hints["job_queue_type"])
            check_type(argname="argument job_state_time_limit_actions", value=job_state_time_limit_actions, expected_type=type_hints["job_state_time_limit_actions"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument scheduling_policy_arn", value=scheduling_policy_arn, expected_type=type_hints["scheduling_policy_arn"])
            check_type(argname="argument service_environment_order", value=service_environment_order, expected_type=type_hints["service_environment_order"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compute_environment_order is not None:
            self._values["compute_environment_order"] = compute_environment_order
        if job_queue_name is not None:
            self._values["job_queue_name"] = job_queue_name
        if job_queue_type is not None:
            self._values["job_queue_type"] = job_queue_type
        if job_state_time_limit_actions is not None:
            self._values["job_state_time_limit_actions"] = job_state_time_limit_actions
        if priority is not None:
            self._values["priority"] = priority
        if scheduling_policy_arn is not None:
            self._values["scheduling_policy_arn"] = scheduling_policy_arn
        if service_environment_order is not None:
            self._values["service_environment_order"] = service_environment_order
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def compute_environment_order(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobQueuePropsMixin.ComputeEnvironmentOrderProperty"]]]]:
        '''The set of compute environments mapped to a job queue and their order relative to each other.

        The job scheduler uses this parameter to determine which compute environment runs a specific job. Compute environments must be in the ``VALID`` state before you can associate them with a job queue. You can associate up to three compute environments with a job queue. All of the compute environments must be either EC2 ( ``EC2`` or ``SPOT`` ) or Fargate ( ``FARGATE`` or ``FARGATE_SPOT`` ); EC2 and Fargate compute environments can't be mixed.
        .. epigraph::

           All compute environments that are associated with a job queue must share the same architecture. AWS Batch doesn't support mixing compute environment architecture types in a single job queue.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-computeenvironmentorder
        '''
        result = self._values.get("compute_environment_order")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobQueuePropsMixin.ComputeEnvironmentOrderProperty"]]]], result)

    @builtins.property
    def job_queue_name(self) -> typing.Optional[builtins.str]:
        '''The name of the job queue.

        It can be up to 128 letters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-jobqueuename
        '''
        result = self._values.get("job_queue_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_queue_type(self) -> typing.Optional[builtins.str]:
        '''The type of job queue.

        For service jobs that run on SageMaker AI , this value is ``SAGEMAKER_TRAINING`` . For regular container jobs, this value is ``EKS`` , ``ECS`` , or ``ECS_FARGATE`` depending on the compute environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-jobqueuetype
        '''
        result = self._values.get("job_queue_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_state_time_limit_actions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobQueuePropsMixin.JobStateTimeLimitActionProperty"]]]]:
        '''The set of actions that AWS Batch perform on jobs that remain at the head of the job queue in the specified state longer than specified times.

        AWS Batch will perform each action after ``maxTimeSeconds`` has passed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-jobstatetimelimitactions
        '''
        result = self._values.get("job_state_time_limit_actions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobQueuePropsMixin.JobStateTimeLimitActionProperty"]]]], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''The priority of the job queue.

        Job queues with a higher priority (or a higher integer value for the ``priority`` parameter) are evaluated first when associated with the same compute environment. Priority is determined in descending order. For example, a job queue with a priority value of ``10`` is given scheduling preference over a job queue with a priority value of ``1`` . All of the compute environments must be either EC2 ( ``EC2`` or ``SPOT`` ) or Fargate ( ``FARGATE`` or ``FARGATE_SPOT`` ); EC2 and Fargate compute environments can't be mixed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-priority
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scheduling_policy_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the scheduling policy.

        The format is ``aws: *Partition* :batch: *Region* : *Account* :scheduling-policy/ *Name*`` . For example, ``aws:aws:batch:us-west-2:123456789012:scheduling-policy/MySchedulingPolicy`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-schedulingpolicyarn
        '''
        result = self._values.get("scheduling_policy_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_environment_order(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobQueuePropsMixin.ServiceEnvironmentOrderProperty"]]]]:
        '''The order of the service environment associated with the job queue.

        Job queues with a higher priority are evaluated first when associated with the same service environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-serviceenvironmentorder
        '''
        result = self._values.get("service_environment_order")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobQueuePropsMixin.ServiceEnvironmentOrderProperty"]]]], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the job queue.

        If the job queue state is ``ENABLED`` , it is able to accept jobs. If the job queue state is ``DISABLED`` , new jobs can't be added to the queue, but jobs already in the queue can finish.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags that are applied to the job queue.

        For more information, see `Tagging your AWS Batch resources <https://docs.aws.amazon.com/batch/latest/userguide/using-tags.html>`_ in *AWS Batch User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnJobQueueMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnJobQueuePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobQueuePropsMixin",
):
    '''The ``AWS::Batch::JobQueue`` resource specifies the parameters for an AWS Batch job queue definition.

    For more information, see `Job Queues <https://docs.aws.amazon.com/batch/latest/userguide/job_queues.html>`_ in the ** .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html
    :cloudformationResource: AWS::Batch::JobQueue
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
        
        cfn_job_queue_props_mixin = batch_mixins.CfnJobQueuePropsMixin(batch_mixins.CfnJobQueueMixinProps(
            compute_environment_order=[batch_mixins.CfnJobQueuePropsMixin.ComputeEnvironmentOrderProperty(
                compute_environment="computeEnvironment",
                order=123
            )],
            job_queue_name="jobQueueName",
            job_queue_type="jobQueueType",
            job_state_time_limit_actions=[batch_mixins.CfnJobQueuePropsMixin.JobStateTimeLimitActionProperty(
                action="action",
                max_time_seconds=123,
                reason="reason",
                state="state"
            )],
            priority=123,
            scheduling_policy_arn="schedulingPolicyArn",
            service_environment_order=[batch_mixins.CfnJobQueuePropsMixin.ServiceEnvironmentOrderProperty(
                order=123,
                service_environment="serviceEnvironment"
            )],
            state="state",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnJobQueueMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Batch::JobQueue``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75e04112a89c65c353ede7579d62d11ca8f34b1aa2257c6ae4c7f22437b8c6f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1869c5490c0d52d4fd596c94ee47ac425afaccb4e6b6d3193d162fb7ee39116)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8234d04bc6fcbf3a051114e103e8b587b47ab57ee5b9fd9cae986084f2512c0f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnJobQueueMixinProps:
        return typing.cast(CfnJobQueueMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobQueuePropsMixin.ComputeEnvironmentOrderProperty",
        jsii_struct_bases=[],
        name_mapping={"compute_environment": "computeEnvironment", "order": "order"},
    )
    class ComputeEnvironmentOrderProperty:
        def __init__(
            self,
            *,
            compute_environment: typing.Optional[builtins.str] = None,
            order: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The order that compute environments are tried in for job placement within a queue.

            Compute environments are tried in ascending order. For example, if two compute environments are associated with a job queue, the compute environment with a lower order integer value is tried for job placement first. Compute environments must be in the ``VALID`` state before you can associate them with a job queue. All of the compute environments must be either EC2 ( ``EC2`` or ``SPOT`` ) or Fargate ( ``FARGATE`` or ``FARGATE_SPOT`` ); Amazon EC2 and Fargate compute environments can't be mixed.
            .. epigraph::

               All compute environments that are associated with a job queue must share the same architecture. AWS Batch doesn't support mixing compute environment architecture types in a single job queue.

            :param compute_environment: The Amazon Resource Name (ARN) of the compute environment.
            :param order: The order of the compute environment. Compute environments are tried in ascending order. For example, if two compute environments are associated with a job queue, the compute environment with a lower ``order`` integer value is tried for job placement first.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobqueue-computeenvironmentorder.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                compute_environment_order_property = batch_mixins.CfnJobQueuePropsMixin.ComputeEnvironmentOrderProperty(
                    compute_environment="computeEnvironment",
                    order=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2895898b1aa1f556237346f63b993a6714e510e0bf62c02412d0a5ca814aef9e)
                check_type(argname="argument compute_environment", value=compute_environment, expected_type=type_hints["compute_environment"])
                check_type(argname="argument order", value=order, expected_type=type_hints["order"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if compute_environment is not None:
                self._values["compute_environment"] = compute_environment
            if order is not None:
                self._values["order"] = order

        @builtins.property
        def compute_environment(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the compute environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobqueue-computeenvironmentorder.html#cfn-batch-jobqueue-computeenvironmentorder-computeenvironment
            '''
            result = self._values.get("compute_environment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def order(self) -> typing.Optional[jsii.Number]:
            '''The order of the compute environment.

            Compute environments are tried in ascending order. For example, if two compute environments are associated with a job queue, the compute environment with a lower ``order`` integer value is tried for job placement first.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobqueue-computeenvironmentorder.html#cfn-batch-jobqueue-computeenvironmentorder-order
            '''
            result = self._values.get("order")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComputeEnvironmentOrderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobQueuePropsMixin.JobStateTimeLimitActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "max_time_seconds": "maxTimeSeconds",
            "reason": "reason",
            "state": "state",
        },
    )
    class JobStateTimeLimitActionProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            max_time_seconds: typing.Optional[jsii.Number] = None,
            reason: typing.Optional[builtins.str] = None,
            state: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an action that AWS Batch will take after the job has remained at the head of the queue in the specified state for longer than the specified time.

            :param action: The action to take when a job is at the head of the job queue in the specified state for the specified period of time. The only supported value is ``CANCEL`` , which will cancel the job.
            :param max_time_seconds: The approximate amount of time, in seconds, that must pass with the job in the specified state before the action is taken. The minimum value is 600 (10 minutes) and the maximum value is 86,400 (24 hours).
            :param reason: The reason to log for the action being taken.
            :param state: The state of the job needed to trigger the action. The only supported value is ``RUNNABLE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobqueue-jobstatetimelimitaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                job_state_time_limit_action_property = batch_mixins.CfnJobQueuePropsMixin.JobStateTimeLimitActionProperty(
                    action="action",
                    max_time_seconds=123,
                    reason="reason",
                    state="state"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bdf6408373e1acdcf46d04c2447e07c5cf3da478b3695e74a19d76c90fbe8d63)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument max_time_seconds", value=max_time_seconds, expected_type=type_hints["max_time_seconds"])
                check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if max_time_seconds is not None:
                self._values["max_time_seconds"] = max_time_seconds
            if reason is not None:
                self._values["reason"] = reason
            if state is not None:
                self._values["state"] = state

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to take when a job is at the head of the job queue in the specified state for the specified period of time.

            The only supported value is ``CANCEL`` , which will cancel the job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobqueue-jobstatetimelimitaction.html#cfn-batch-jobqueue-jobstatetimelimitaction-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_time_seconds(self) -> typing.Optional[jsii.Number]:
            '''The approximate amount of time, in seconds, that must pass with the job in the specified state before the action is taken.

            The minimum value is 600 (10 minutes) and the maximum value is 86,400 (24 hours).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobqueue-jobstatetimelimitaction.html#cfn-batch-jobqueue-jobstatetimelimitaction-maxtimeseconds
            '''
            result = self._values.get("max_time_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def reason(self) -> typing.Optional[builtins.str]:
            '''The reason to log for the action being taken.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobqueue-jobstatetimelimitaction.html#cfn-batch-jobqueue-jobstatetimelimitaction-reason
            '''
            result = self._values.get("reason")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            '''The state of the job needed to trigger the action.

            The only supported value is ``RUNNABLE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobqueue-jobstatetimelimitaction.html#cfn-batch-jobqueue-jobstatetimelimitaction-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JobStateTimeLimitActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnJobQueuePropsMixin.ServiceEnvironmentOrderProperty",
        jsii_struct_bases=[],
        name_mapping={"order": "order", "service_environment": "serviceEnvironment"},
    )
    class ServiceEnvironmentOrderProperty:
        def __init__(
            self,
            *,
            order: typing.Optional[jsii.Number] = None,
            service_environment: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the order of a service environment for a job queue.

            This determines the priority order when multiple service environments are associated with the same job queue.

            :param order: The order of the service environment. Job queues with a higher priority are evaluated first when associated with the same service environment.
            :param service_environment: The name or ARN of the service environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobqueue-serviceenvironmentorder.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                service_environment_order_property = batch_mixins.CfnJobQueuePropsMixin.ServiceEnvironmentOrderProperty(
                    order=123,
                    service_environment="serviceEnvironment"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8805e81dbcb878f4442d945319b634e6d87a3684afe255251c6dc4de3ee4fa0e)
                check_type(argname="argument order", value=order, expected_type=type_hints["order"])
                check_type(argname="argument service_environment", value=service_environment, expected_type=type_hints["service_environment"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if order is not None:
                self._values["order"] = order
            if service_environment is not None:
                self._values["service_environment"] = service_environment

        @builtins.property
        def order(self) -> typing.Optional[jsii.Number]:
            '''The order of the service environment.

            Job queues with a higher priority are evaluated first when associated with the same service environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobqueue-serviceenvironmentorder.html#cfn-batch-jobqueue-serviceenvironmentorder-order
            '''
            result = self._values.get("order")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def service_environment(self) -> typing.Optional[builtins.str]:
            '''The name or ARN of the service environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobqueue-serviceenvironmentorder.html#cfn-batch-jobqueue-serviceenvironmentorder-serviceenvironment
            '''
            result = self._values.get("service_environment")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceEnvironmentOrderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnSchedulingPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "fairshare_policy": "fairsharePolicy",
        "name": "name",
        "tags": "tags",
    },
)
class CfnSchedulingPolicyMixinProps:
    def __init__(
        self,
        *,
        fairshare_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchedulingPolicyPropsMixin.FairsharePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnSchedulingPolicyPropsMixin.

        :param fairshare_policy: The fair-share scheduling policy details.
        :param name: The name of the fair-share scheduling policy. It can be up to 128 letters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_).
        :param tags: The tags that you apply to the scheduling policy to help you categorize and organize your resources. Each tag consists of a key and an optional value. For more information, see `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in *AWS General Reference* . These tags can be updated or removed using the `TagResource <https://docs.aws.amazon.com/batch/latest/APIReference/API_TagResource.html>`_ and `UntagResource <https://docs.aws.amazon.com/batch/latest/APIReference/API_UntagResource.html>`_ API operations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-schedulingpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
            
            cfn_scheduling_policy_mixin_props = batch_mixins.CfnSchedulingPolicyMixinProps(
                fairshare_policy=batch_mixins.CfnSchedulingPolicyPropsMixin.FairsharePolicyProperty(
                    compute_reservation=123,
                    share_decay_seconds=123,
                    share_distribution=[batch_mixins.CfnSchedulingPolicyPropsMixin.ShareAttributesProperty(
                        share_identifier="shareIdentifier",
                        weight_factor=123
                    )]
                ),
                name="name",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c876a840b18b9e0d4124a105913cb3ba1713d47465d99a67b1a7c0501a9c919)
            check_type(argname="argument fairshare_policy", value=fairshare_policy, expected_type=type_hints["fairshare_policy"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fairshare_policy is not None:
            self._values["fairshare_policy"] = fairshare_policy
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def fairshare_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulingPolicyPropsMixin.FairsharePolicyProperty"]]:
        '''The fair-share scheduling policy details.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-schedulingpolicy.html#cfn-batch-schedulingpolicy-fairsharepolicy
        '''
        result = self._values.get("fairshare_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulingPolicyPropsMixin.FairsharePolicyProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the fair-share scheduling policy.

        It can be up to 128 letters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-schedulingpolicy.html#cfn-batch-schedulingpolicy-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags that you apply to the scheduling policy to help you categorize and organize your resources.

        Each tag consists of a key and an optional value. For more information, see `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in *AWS General Reference* .

        These tags can be updated or removed using the `TagResource <https://docs.aws.amazon.com/batch/latest/APIReference/API_TagResource.html>`_ and `UntagResource <https://docs.aws.amazon.com/batch/latest/APIReference/API_UntagResource.html>`_ API operations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-schedulingpolicy.html#cfn-batch-schedulingpolicy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSchedulingPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSchedulingPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnSchedulingPolicyPropsMixin",
):
    '''The ``AWS::Batch::SchedulingPolicy`` resource specifies the parameters for an AWS Batch scheduling policy.

    For more information, see `Scheduling Policies <https://docs.aws.amazon.com/batch/latest/userguide/scheduling_policies.html>`_ in the ** .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-schedulingpolicy.html
    :cloudformationResource: AWS::Batch::SchedulingPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
        
        cfn_scheduling_policy_props_mixin = batch_mixins.CfnSchedulingPolicyPropsMixin(batch_mixins.CfnSchedulingPolicyMixinProps(
            fairshare_policy=batch_mixins.CfnSchedulingPolicyPropsMixin.FairsharePolicyProperty(
                compute_reservation=123,
                share_decay_seconds=123,
                share_distribution=[batch_mixins.CfnSchedulingPolicyPropsMixin.ShareAttributesProperty(
                    share_identifier="shareIdentifier",
                    weight_factor=123
                )]
            ),
            name="name",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSchedulingPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Batch::SchedulingPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9e87eac09e87dc387872e470daafb3941ec1cec2e0458be5fa54f0b36445d79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__679cff01d7da346ac49724cd123f49affc50192f5c6ee2c6b6313a3bc8046de4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa15fc1e36f4e3ed981abef349c724d389a891d20452dbb5754fb9d0bbddc825)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSchedulingPolicyMixinProps:
        return typing.cast(CfnSchedulingPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnSchedulingPolicyPropsMixin.FairsharePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "compute_reservation": "computeReservation",
            "share_decay_seconds": "shareDecaySeconds",
            "share_distribution": "shareDistribution",
        },
    )
    class FairsharePolicyProperty:
        def __init__(
            self,
            *,
            compute_reservation: typing.Optional[jsii.Number] = None,
            share_decay_seconds: typing.Optional[jsii.Number] = None,
            share_distribution: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchedulingPolicyPropsMixin.ShareAttributesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The fair-share scheduling policy details.

            :param compute_reservation: A value used to reserve some of the available maximum vCPU for share identifiers that aren't already used. The reserved ratio is ``( *computeReservation* /100)^ *ActiveFairShares*`` where ``*ActiveFairShares*`` is the number of active share identifiers. For example, a ``computeReservation`` value of 50 indicates that AWS Batch reserves 50% of the maximum available vCPU if there's only one share identifier. It reserves 25% if there are two share identifiers. It reserves 12.5% if there are three share identifiers. A ``computeReservation`` value of 25 indicates that AWS Batch should reserve 25% of the maximum available vCPU if there's only one share identifier, 6.25% if there are two fair share identifiers, and 1.56% if there are three share identifiers. The minimum value is 0 and the maximum value is 99.
            :param share_decay_seconds: The amount of time (in seconds) to use to calculate a fair-share percentage for each share identifier in use. A value of zero (0) indicates the default minimum time window (600 seconds). The maximum supported value is 604800 (1 week). The decay allows for more recently run jobs to have more weight than jobs that ran earlier. Consider adjusting this number if you have jobs that (on average) run longer than ten minutes, or a large difference in job count or job run times between share identifiers, and the allocation of resources doesn't meet your needs.
            :param share_distribution: An array of ``SharedIdentifier`` objects that contain the weights for the share identifiers for the fair-share policy. Share identifiers that aren't included have a default weight of ``1.0`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-schedulingpolicy-fairsharepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                fairshare_policy_property = batch_mixins.CfnSchedulingPolicyPropsMixin.FairsharePolicyProperty(
                    compute_reservation=123,
                    share_decay_seconds=123,
                    share_distribution=[batch_mixins.CfnSchedulingPolicyPropsMixin.ShareAttributesProperty(
                        share_identifier="shareIdentifier",
                        weight_factor=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8b10c5318e829357912fe9014ea934b7b3815690d45df4ab957f9a01c16466fe)
                check_type(argname="argument compute_reservation", value=compute_reservation, expected_type=type_hints["compute_reservation"])
                check_type(argname="argument share_decay_seconds", value=share_decay_seconds, expected_type=type_hints["share_decay_seconds"])
                check_type(argname="argument share_distribution", value=share_distribution, expected_type=type_hints["share_distribution"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if compute_reservation is not None:
                self._values["compute_reservation"] = compute_reservation
            if share_decay_seconds is not None:
                self._values["share_decay_seconds"] = share_decay_seconds
            if share_distribution is not None:
                self._values["share_distribution"] = share_distribution

        @builtins.property
        def compute_reservation(self) -> typing.Optional[jsii.Number]:
            '''A value used to reserve some of the available maximum vCPU for share identifiers that aren't already used.

            The reserved ratio is ``( *computeReservation* /100)^ *ActiveFairShares*`` where ``*ActiveFairShares*`` is the number of active share identifiers.

            For example, a ``computeReservation`` value of 50 indicates that AWS Batch reserves 50% of the maximum available vCPU if there's only one share identifier. It reserves 25% if there are two share identifiers. It reserves 12.5% if there are three share identifiers. A ``computeReservation`` value of 25 indicates that AWS Batch should reserve 25% of the maximum available vCPU if there's only one share identifier, 6.25% if there are two fair share identifiers, and 1.56% if there are three share identifiers.

            The minimum value is 0 and the maximum value is 99.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-schedulingpolicy-fairsharepolicy.html#cfn-batch-schedulingpolicy-fairsharepolicy-computereservation
            '''
            result = self._values.get("compute_reservation")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def share_decay_seconds(self) -> typing.Optional[jsii.Number]:
            '''The amount of time (in seconds) to use to calculate a fair-share percentage for each share identifier in use.

            A value of zero (0) indicates the default minimum time window (600 seconds). The maximum supported value is 604800 (1 week).

            The decay allows for more recently run jobs to have more weight than jobs that ran earlier. Consider adjusting this number if you have jobs that (on average) run longer than ten minutes, or a large difference in job count or job run times between share identifiers, and the allocation of resources doesn't meet your needs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-schedulingpolicy-fairsharepolicy.html#cfn-batch-schedulingpolicy-fairsharepolicy-sharedecayseconds
            '''
            result = self._values.get("share_decay_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def share_distribution(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulingPolicyPropsMixin.ShareAttributesProperty"]]]]:
            '''An array of ``SharedIdentifier`` objects that contain the weights for the share identifiers for the fair-share policy.

            Share identifiers that aren't included have a default weight of ``1.0`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-schedulingpolicy-fairsharepolicy.html#cfn-batch-schedulingpolicy-fairsharepolicy-sharedistribution
            '''
            result = self._values.get("share_distribution")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulingPolicyPropsMixin.ShareAttributesProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FairsharePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnSchedulingPolicyPropsMixin.ShareAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "share_identifier": "shareIdentifier",
            "weight_factor": "weightFactor",
        },
    )
    class ShareAttributesProperty:
        def __init__(
            self,
            *,
            share_identifier: typing.Optional[builtins.str] = None,
            weight_factor: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the weights for the share identifiers for the fair-share policy.

            Share identifiers that aren't included have a default weight of ``1.0`` .

            :param share_identifier: A share identifier or share identifier prefix. If the string ends with an asterisk (*), this entry specifies the weight factor to use for share identifiers that start with that prefix. The list of share identifiers in a fair-share policy can't overlap. For example, you can't have one that specifies a ``shareIdentifier`` of ``UserA*`` and another that specifies a ``shareIdentifier`` of ``UserA1`` . There can be no more than 500 share identifiers active in a job queue. The string is limited to 255 alphanumeric characters, and can be followed by an asterisk (*).
            :param weight_factor: The weight factor for the share identifier. The default value is 1.0. A lower value has a higher priority for compute resources. For example, jobs that use a share identifier with a weight factor of 0.125 (1/8) get 8 times the compute resources of jobs that use a share identifier with a weight factor of 1. The smallest supported value is 0.0001, and the largest supported value is 999.9999.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-schedulingpolicy-shareattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                share_attributes_property = batch_mixins.CfnSchedulingPolicyPropsMixin.ShareAttributesProperty(
                    share_identifier="shareIdentifier",
                    weight_factor=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0dc9b42832284ec4c052cafa3498a1440562a707c47438a6f14f49bd0e823c49)
                check_type(argname="argument share_identifier", value=share_identifier, expected_type=type_hints["share_identifier"])
                check_type(argname="argument weight_factor", value=weight_factor, expected_type=type_hints["weight_factor"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if share_identifier is not None:
                self._values["share_identifier"] = share_identifier
            if weight_factor is not None:
                self._values["weight_factor"] = weight_factor

        @builtins.property
        def share_identifier(self) -> typing.Optional[builtins.str]:
            '''A share identifier or share identifier prefix.

            If the string ends with an asterisk (*), this entry specifies the weight factor to use for share identifiers that start with that prefix. The list of share identifiers in a fair-share policy can't overlap. For example, you can't have one that specifies a ``shareIdentifier`` of ``UserA*`` and another that specifies a ``shareIdentifier`` of ``UserA1`` .

            There can be no more than 500 share identifiers active in a job queue.

            The string is limited to 255 alphanumeric characters, and can be followed by an asterisk (*).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-schedulingpolicy-shareattributes.html#cfn-batch-schedulingpolicy-shareattributes-shareidentifier
            '''
            result = self._values.get("share_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weight_factor(self) -> typing.Optional[jsii.Number]:
            '''The weight factor for the share identifier.

            The default value is 1.0. A lower value has a higher priority for compute resources. For example, jobs that use a share identifier with a weight factor of 0.125 (1/8) get 8 times the compute resources of jobs that use a share identifier with a weight factor of 1.

            The smallest supported value is 0.0001, and the largest supported value is 999.9999.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-schedulingpolicy-shareattributes.html#cfn-batch-schedulingpolicy-shareattributes-weightfactor
            '''
            result = self._values.get("weight_factor")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ShareAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnServiceEnvironmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "capacity_limits": "capacityLimits",
        "service_environment_name": "serviceEnvironmentName",
        "service_environment_type": "serviceEnvironmentType",
        "state": "state",
        "tags": "tags",
    },
)
class CfnServiceEnvironmentMixinProps:
    def __init__(
        self,
        *,
        capacity_limits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceEnvironmentPropsMixin.CapacityLimitProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        service_environment_name: typing.Optional[builtins.str] = None,
        service_environment_type: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnServiceEnvironmentPropsMixin.

        :param capacity_limits: The capacity limits for the service environment. This defines the maximum resources that can be used by service jobs in this environment.
        :param service_environment_name: The name of the service environment.
        :param service_environment_type: The type of service environment. For SageMaker Training jobs, this value is ``SAGEMAKER_TRAINING`` .
        :param state: The state of the service environment. Valid values are ``ENABLED`` and ``DISABLED`` .
        :param tags: The tags associated with the service environment. Each tag consists of a key and an optional value. For more information, see `Tagging your AWS Batch resources <https://docs.aws.amazon.com/batch/latest/userguide/using-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-serviceenvironment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
            
            cfn_service_environment_mixin_props = batch_mixins.CfnServiceEnvironmentMixinProps(
                capacity_limits=[batch_mixins.CfnServiceEnvironmentPropsMixin.CapacityLimitProperty(
                    capacity_unit="capacityUnit",
                    max_capacity=123
                )],
                service_environment_name="serviceEnvironmentName",
                service_environment_type="serviceEnvironmentType",
                state="state",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a49cbd984bd0e164047ced343c4045d887d9893618214d4a1ea9fec2f0618a)
            check_type(argname="argument capacity_limits", value=capacity_limits, expected_type=type_hints["capacity_limits"])
            check_type(argname="argument service_environment_name", value=service_environment_name, expected_type=type_hints["service_environment_name"])
            check_type(argname="argument service_environment_type", value=service_environment_type, expected_type=type_hints["service_environment_type"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if capacity_limits is not None:
            self._values["capacity_limits"] = capacity_limits
        if service_environment_name is not None:
            self._values["service_environment_name"] = service_environment_name
        if service_environment_type is not None:
            self._values["service_environment_type"] = service_environment_type
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def capacity_limits(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceEnvironmentPropsMixin.CapacityLimitProperty"]]]]:
        '''The capacity limits for the service environment.

        This defines the maximum resources that can be used by service jobs in this environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-serviceenvironment.html#cfn-batch-serviceenvironment-capacitylimits
        '''
        result = self._values.get("capacity_limits")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceEnvironmentPropsMixin.CapacityLimitProperty"]]]], result)

    @builtins.property
    def service_environment_name(self) -> typing.Optional[builtins.str]:
        '''The name of the service environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-serviceenvironment.html#cfn-batch-serviceenvironment-serviceenvironmentname
        '''
        result = self._values.get("service_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_environment_type(self) -> typing.Optional[builtins.str]:
        '''The type of service environment.

        For SageMaker Training jobs, this value is ``SAGEMAKER_TRAINING`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-serviceenvironment.html#cfn-batch-serviceenvironment-serviceenvironmenttype
        '''
        result = self._values.get("service_environment_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the service environment.

        Valid values are ``ENABLED`` and ``DISABLED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-serviceenvironment.html#cfn-batch-serviceenvironment-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags associated with the service environment.

        Each tag consists of a key and an optional value. For more information, see `Tagging your AWS Batch resources <https://docs.aws.amazon.com/batch/latest/userguide/using-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-serviceenvironment.html#cfn-batch-serviceenvironment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceEnvironmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnServiceEnvironmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnServiceEnvironmentPropsMixin",
):
    '''Creates a service environment for running service jobs.

    Service environments define capacity limits for specific service types such as SageMaker Training jobs.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-serviceenvironment.html
    :cloudformationResource: AWS::Batch::ServiceEnvironment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
        
        cfn_service_environment_props_mixin = batch_mixins.CfnServiceEnvironmentPropsMixin(batch_mixins.CfnServiceEnvironmentMixinProps(
            capacity_limits=[batch_mixins.CfnServiceEnvironmentPropsMixin.CapacityLimitProperty(
                capacity_unit="capacityUnit",
                max_capacity=123
            )],
            service_environment_name="serviceEnvironmentName",
            service_environment_type="serviceEnvironmentType",
            state="state",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnServiceEnvironmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Batch::ServiceEnvironment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__769275946851bede4c055cb074ca4ff346a6e32d46a2af3e805e91a2b5802e30)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4492f568b83877aabfdbe6a158f67c1c442432196bfc2215c047732d7e07bfd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b6ea447e8ab757ea4764889d9f7dee2167cd85a8fca36e92782aac3baea6a59)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnServiceEnvironmentMixinProps:
        return typing.cast(CfnServiceEnvironmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_batch.mixins.CfnServiceEnvironmentPropsMixin.CapacityLimitProperty",
        jsii_struct_bases=[],
        name_mapping={"capacity_unit": "capacityUnit", "max_capacity": "maxCapacity"},
    )
    class CapacityLimitProperty:
        def __init__(
            self,
            *,
            capacity_unit: typing.Optional[builtins.str] = None,
            max_capacity: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines the capacity limit for a service environment.

            This structure specifies the maximum amount of resources that can be used by service jobs in the environment.

            :param capacity_unit: The unit of measure for the capacity limit. This defines how the maxCapacity value should be interpreted. For ``SAGEMAKER_TRAINING`` jobs, use ``NUM_INSTANCES`` .
            :param max_capacity: The maximum capacity available for the service environment. This value represents the maximum amount resources that can be allocated to service jobs. For example, ``maxCapacity=50`` , ``capacityUnit=NUM_INSTANCES`` . This indicates that the maximum number of instances that can be run on this service environment is 50. You could then run 5 SageMaker Training jobs that each use 10 instances. However, if you submit another job that requires 10 instances, it will wait in the queue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-serviceenvironment-capacitylimit.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_batch import mixins as batch_mixins
                
                capacity_limit_property = batch_mixins.CfnServiceEnvironmentPropsMixin.CapacityLimitProperty(
                    capacity_unit="capacityUnit",
                    max_capacity=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e7d3bdd7187db7f26ca11c2ff0a14a65981d005818c5b18b910ea9d7dd1b6e73)
                check_type(argname="argument capacity_unit", value=capacity_unit, expected_type=type_hints["capacity_unit"])
                check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capacity_unit is not None:
                self._values["capacity_unit"] = capacity_unit
            if max_capacity is not None:
                self._values["max_capacity"] = max_capacity

        @builtins.property
        def capacity_unit(self) -> typing.Optional[builtins.str]:
            '''The unit of measure for the capacity limit.

            This defines how the maxCapacity value should be interpreted. For ``SAGEMAKER_TRAINING`` jobs, use ``NUM_INSTANCES`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-serviceenvironment-capacitylimit.html#cfn-batch-serviceenvironment-capacitylimit-capacityunit
            '''
            result = self._values.get("capacity_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_capacity(self) -> typing.Optional[jsii.Number]:
            '''The maximum capacity available for the service environment.

            This value represents the maximum amount resources that can be allocated to service jobs.

            For example, ``maxCapacity=50`` , ``capacityUnit=NUM_INSTANCES`` . This indicates that the maximum number of instances that can be run on this service environment is 50. You could then run 5 SageMaker Training jobs that each use 10 instances. However, if you submit another job that requires 10 instances, it will wait in the queue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-serviceenvironment-capacitylimit.html#cfn-batch-serviceenvironment-capacitylimit-maxcapacity
            '''
            result = self._values.get("max_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityLimitProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnComputeEnvironmentMixinProps",
    "CfnComputeEnvironmentPropsMixin",
    "CfnConsumableResourceMixinProps",
    "CfnConsumableResourcePropsMixin",
    "CfnJobDefinitionMixinProps",
    "CfnJobDefinitionPropsMixin",
    "CfnJobQueueMixinProps",
    "CfnJobQueuePropsMixin",
    "CfnSchedulingPolicyMixinProps",
    "CfnSchedulingPolicyPropsMixin",
    "CfnServiceEnvironmentMixinProps",
    "CfnServiceEnvironmentPropsMixin",
]

publication.publish()

def _typecheckingstub__3eca7e9bb48dc8c53779233c34c1b3b48f3f81bb63409ee78547b5426f4a0abe(
    *,
    compute_environment_name: typing.Optional[builtins.str] = None,
    compute_resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComputeEnvironmentPropsMixin.ComputeResourcesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    context: typing.Optional[builtins.str] = None,
    eks_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComputeEnvironmentPropsMixin.EksConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    replace_compute_environment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    service_role: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
    unmanagedv_cpus: typing.Optional[jsii.Number] = None,
    update_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComputeEnvironmentPropsMixin.UpdatePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88f5a15200eb018b614f82e670428401d704579f42ebf5c43cbb03513967c248(
    props: typing.Union[CfnComputeEnvironmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26728de17ad0822af3ddd19021f263835ac6e85e611335e832b007e0eaf024b1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daadb6113f0a1945dc1e65345283e4250bc7f3fd0e119cd0978f2e308d23a739(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d66f10fa1b3e88b935bc597bc33872c12fbbc3eafb16866ae2d40e801c98a64(
    *,
    allocation_strategy: typing.Optional[builtins.str] = None,
    bid_percentage: typing.Optional[jsii.Number] = None,
    desiredv_cpus: typing.Optional[jsii.Number] = None,
    ec2_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComputeEnvironmentPropsMixin.Ec2ConfigurationObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ec2_key_pair: typing.Optional[builtins.str] = None,
    image_id: typing.Optional[builtins.str] = None,
    instance_role: typing.Optional[builtins.str] = None,
    instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    launch_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComputeEnvironmentPropsMixin.LaunchTemplateSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maxv_cpus: typing.Optional[jsii.Number] = None,
    minv_cpus: typing.Optional[jsii.Number] = None,
    placement_group: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    spot_iam_fleet_role: typing.Optional[builtins.str] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
    update_to_latest_image_version: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00023ed80a08e816151f9b1563df188d68d5a889926e8e3c4085b54c3ad37c7b(
    *,
    image_id_override: typing.Optional[builtins.str] = None,
    image_kubernetes_version: typing.Optional[builtins.str] = None,
    image_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b8d407ca69cf2ff1009c4f05a24470c07dbeb2a4979c43bb859742ebd24c00b(
    *,
    eks_cluster_arn: typing.Optional[builtins.str] = None,
    kubernetes_namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83068de22d881a95f456528ce0e40a31cf96232d6ffbfd9972cca6ca8117eab3(
    *,
    launch_template_id: typing.Optional[builtins.str] = None,
    launch_template_name: typing.Optional[builtins.str] = None,
    target_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    userdata_type: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b340d5a80f630c040ca1d13f63a7423fd51f51dde53cf391c5a002e89eb59b6b(
    *,
    launch_template_id: typing.Optional[builtins.str] = None,
    launch_template_name: typing.Optional[builtins.str] = None,
    overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComputeEnvironmentPropsMixin.LaunchTemplateSpecificationOverrideProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    userdata_type: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73efe81a7ee75c6cc3527b46b16e6b3dc00282503701ea44a66d7873535a434(
    *,
    job_execution_timeout_minutes: typing.Optional[jsii.Number] = None,
    terminate_jobs_on_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21179910b253b4a582cb266d454cec991cd5e54fa3074696b95ca84774ca2d16(
    *,
    consumable_resource_name: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    total_quantity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b366079b0bc8b5d7d242a928465c0e3fbfcc5aec27504186b02cc5fc84b4a95d(
    props: typing.Union[CfnConsumableResourceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5318b54fa86b435e3b22cfe586581f60aac0fbf439ded168ad9897198f88f4b3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f42a786dc8973a572c356eb280104e2c9e605f11685288a7dbd6152ce879bc2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8dbe65ec91d17ee6b06ec4341b531c757a3e0222e2e238001f2d50cba11d245(
    *,
    consumable_resource_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.ConsumableResourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    container_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.ContainerPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ecs_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.EcsPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    eks_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.EksPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    job_definition_name: typing.Optional[builtins.str] = None,
    node_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.NodePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parameters: typing.Any = None,
    platform_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
    propagate_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    resource_retention_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.ResourceRetentionPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    retry_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.RetryStrategyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scheduling_priority: typing.Optional[jsii.Number] = None,
    tags: typing.Any = None,
    timeout: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.TimeoutProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87abfbcd1852552990b06a57c912fd73ccc3116bbd9eef194078801f24666bc(
    props: typing.Union[CfnJobDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8337b26b1f946e02bd1a11c59396c3d67594216d66b0b2f807fddad35dd940b4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d2d34aca74bf95fffa06e556b45bc8f4fb593d8537ed3505bd29f9f95ad120e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c808feda9afa8f364208a37522654fc65160163e1ece1ac2e2b8c07b10aa4452(
    *,
    access_point_id: typing.Optional[builtins.str] = None,
    iam: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__188f31c82213bad51eaa19f67e62c4062b1dac049edcce7e4b8583e28248c6f2(
    *,
    consumable_resource_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.ConsumableResourceRequirementProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2283572e826c7e3cced44564e73ffffb3021d9e0011f613f5def44ca8fcb3587(
    *,
    consumable_resource: typing.Optional[builtins.str] = None,
    quantity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8123c7a975d95658fed794d63213d173f02b341be6ac3999556de746e2f06899(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_execute_command: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.EnvironmentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ephemeral_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.EphemeralStorageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    fargate_platform_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.FargatePlatformConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[builtins.str] = None,
    job_role_arn: typing.Optional[builtins.str] = None,
    linux_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.LinuxParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    log_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.LogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    memory: typing.Optional[jsii.Number] = None,
    mount_points: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.MountPointsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    privileged: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    readonly_root_filesystem: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    repository_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.RepositoryCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_requirements: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.ResourceRequirementProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    runtime_platform: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.RuntimePlatformProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secrets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.SecretProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ulimits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.UlimitProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    user: typing.Optional[builtins.str] = None,
    vcpus: typing.Optional[jsii.Number] = None,
    volumes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.VolumesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db5d2d62863fa365abbc7dc6d8fe5da5ecffc2dc2dae6a7c3999db53a89e9c16(
    *,
    container_path: typing.Optional[builtins.str] = None,
    host_path: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f43527e74009146074a93c08a0be76a471666027e6f2df162e469ec0fe01866(
    *,
    task_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.EcsTaskPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d48aac040b1240ed1ab74ad217f7da6599e55f40a8b0b56ee6f019f964168c(
    *,
    containers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.TaskContainerPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    enable_execute_command: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ephemeral_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.EphemeralStorageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    ipc_mode: typing.Optional[builtins.str] = None,
    network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    pid_mode: typing.Optional[builtins.str] = None,
    platform_version: typing.Optional[builtins.str] = None,
    runtime_platform: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.RuntimePlatformProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_role_arn: typing.Optional[builtins.str] = None,
    volumes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.VolumesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d746f40c72d4b2e1cf30831369ccecbcb84aad796e72c4a4f92ad034fdeb32c(
    *,
    authorization_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.AuthorizationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    file_system_id: typing.Optional[builtins.str] = None,
    root_directory: typing.Optional[builtins.str] = None,
    transit_encryption: typing.Optional[builtins.str] = None,
    transit_encryption_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610e71856483adb0d62ca5484a1f9f7644a50b02b762e82d3d37f4b27ba155c3(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d1118b1ddd2e3c55b50d6427f174d05619687cc7547da022d35a498ccfc570(
    *,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.EksContainerEnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    image: typing.Optional[builtins.str] = None,
    image_pull_policy: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.ResourcesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    security_context: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.SecurityContextProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    volume_mounts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.EksContainerVolumeMountProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670f1be772833ab577dafd36d83046dfee8dffbbb7ed935e2a7dc64350ff117a(
    *,
    mount_path: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    sub_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a0751e687219b001decb2718958399b0781fcf70e6f6b78b5a00d5617993a58(
    *,
    claim_name: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1699fd5575882ca37d362f4225f8c5fb7977f5d1d9da25324b55cfe8b7c091c2(
    *,
    pod_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.PodPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d0f748f7535e10c40eed1e837a480668788dbaf02f74f8de99afccf05cb650(
    *,
    optional: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    secret_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd520e3b0ecc3777227351e91ec59155949c3f92d933526a7138062b041f5f22(
    *,
    empty_dir: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.EmptyDirProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    host_path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.HostPathProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    persistent_volume_claim: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.EksPersistentVolumeClaimProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secret: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.EksSecretProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9c3903e7935a21888e1cc782db905a24604b669b5924f4107e00a0cad11903(
    *,
    medium: typing.Optional[builtins.str] = None,
    size_limit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b6ac57ce0cdbe7ed0745bffc7a57f8fcdfe7d7e8e986e96d6bb73ed3436a6e(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6251e67d1c65a706a864fa6e924eb8a136900755eab8755d6d3e8eeb998e0d0(
    *,
    size_in_gib: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180ea3fbfb4a0b9b2dac0e30999d723bf15508e980e3e0cdb6e59e9339afd2dd(
    *,
    action: typing.Optional[builtins.str] = None,
    on_exit_code: typing.Optional[builtins.str] = None,
    on_reason: typing.Optional[builtins.str] = None,
    on_status_reason: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d01259e640cadebf4b4c451149db92ac8ab6de1356a43a69e22406ae5350f50(
    *,
    platform_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51ce8c2dbc249874b77d6b580d43812f54abd89cbe980af6dd07921d89aa707b(
    *,
    options: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4540d0994e62cb27e31ea48fb7bdbcf193de5b11a395b4f9ea687cf7524f19b2(
    *,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e76f6b9abdfac95ed04151b59d888438effa81f5cce07fd6faea855f76b330af(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__807d7b4536f4dc63e0b69ba851801e70b5d4ae665fdb1523490e5cb69cfbe965(
    *,
    attempt_duration_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8ca7df82403669c12cf396698dd4d31318baa72a3d8e2ad1135ed49c726577(
    *,
    devices: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.DeviceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    init_process_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    max_swap: typing.Optional[jsii.Number] = None,
    shared_memory_size: typing.Optional[jsii.Number] = None,
    swappiness: typing.Optional[jsii.Number] = None,
    tmpfs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.TmpfsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcbc658088bd56e9e53fc9c5536e1d4150231ba5f4e7175dcdedc83b0941c430(
    *,
    log_driver: typing.Optional[builtins.str] = None,
    options: typing.Any = None,
    secret_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.SecretProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4852fa6a00e41662c659e430b8dfe1e2f0c25f72cf8739c1ed6e342d8df46191(
    *,
    labels: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f9b359a15f63a066ad1e7d5fde3c616cce63d4cab9ecd6371a09c3b5f714991(
    *,
    container_path: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    source_volume: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f233857cc8a563bd7bedc5306a2d26c8cf217bca9bb0a69faf227d5a888748a(
    *,
    container_path: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    source_volume: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e40ff6e1baf2ea84e2508656704eaafa0e9f67109fc3265b3268195d7886e00(
    *,
    task_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.MultiNodeEcsTaskPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75bc1ce239180115070372f1fc9f0ab27916fcfecc19549715b129942887dd86(
    *,
    containers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.TaskContainerPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    enable_execute_command: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    ipc_mode: typing.Optional[builtins.str] = None,
    pid_mode: typing.Optional[builtins.str] = None,
    task_role_arn: typing.Optional[builtins.str] = None,
    volumes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.VolumesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4cca6e41aaf81cfe601c5b66371ac220e000c0a5fb2887a06964c2235a56c18(
    *,
    assign_public_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a7b9392a47c632922643c51b6a15680e27abc8cbf41d92167891a151e9815c(
    *,
    main_node: typing.Optional[jsii.Number] = None,
    node_range_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.NodeRangePropertyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    num_nodes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a33a59520854daf4f026d2061801fb7cdb25cac070e0151beff4bc1c97bc4271(
    *,
    consumable_resource_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.ConsumableResourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    container: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.ContainerPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ecs_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.MultiNodeEcsPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    eks_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.EksPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_nodes: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8c684be247f5ba54742ec8dea491caf11912a15415f2a76a90e85b591239d3(
    *,
    containers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.EksContainerProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    dns_policy: typing.Optional[builtins.str] = None,
    host_network: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    image_pull_secrets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.ImagePullSecretProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    init_containers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.EksContainerProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.MetadataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_account_name: typing.Optional[builtins.str] = None,
    share_process_namespace: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    volumes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.EksVolumeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47d045ffdcd9d63fbc199d26009df6040bb36b1676bd5de1af71d140b6efadd1(
    *,
    credentials_parameter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3945172c4385b4c0e69592db554109ed784e14468acdc15006c5067e539791a2(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83cedf64bcbf85b1d7ff57df48c464ea08697dd6cd85ca6cc3699ef02622ddbf(
    *,
    skip_deregister_on_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f45306336ff67b2bce51d0a63f161b784c9e00b4dfca83bbc69c98a2f4c368b(
    *,
    limits: typing.Any = None,
    requests: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39ee6407c07cd343365710b06db5f74f78424c2464899dc11c859a661de3b071(
    *,
    attempts: typing.Optional[jsii.Number] = None,
    evaluate_on_exit: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.EvaluateOnExitProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb5f73fc44ae2f8b47a42723be41230dc78ef9f37e2023bd64ec95410b6bece(
    *,
    cpu_architecture: typing.Optional[builtins.str] = None,
    operating_system_family: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2652d6c60261cb148fbc6b388cc91d678c293dac6d990f01439c011163a2ef16(
    *,
    name: typing.Optional[builtins.str] = None,
    value_from: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__440b15373aae3a2eeac026055d7ec32a15b5b7b9a05220647f0c0398dcf77b11(
    *,
    allow_privilege_escalation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    privileged: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    read_only_root_filesystem: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    run_as_group: typing.Optional[jsii.Number] = None,
    run_as_non_root: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    run_as_user: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93bc1da4709753158a71b2b89d48018a9867fa8fb7517608b34864e601d2d613(
    *,
    condition: typing.Optional[builtins.str] = None,
    container_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__871ff1f8637d018c37cf9ddd4858e5988a0dd510d6c910b837dc04545a04c902(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    depends_on: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.TaskContainerDependencyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.EnvironmentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    essential: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    firelens_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.FirelensConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image: typing.Optional[builtins.str] = None,
    linux_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.LinuxParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    log_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.LogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mount_points: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.MountPointProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    privileged: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    readonly_root_filesystem: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    repository_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.RepositoryCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_requirements: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.ResourceRequirementProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    secrets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.SecretProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ulimits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.UlimitProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8a72f0c7f821c60934e108c04d4da77e24b93a2eb90ee2dfd23197642d3466(
    *,
    attempt_duration_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf64c3f8e3b4b5c2435f9d8191b9657d7f20e6b122222a2e3302bf3a964103c4(
    *,
    container_path: typing.Optional[builtins.str] = None,
    mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb6820461a55e970afdf8747c17246f0a307f716a0f871aeda35ee14612765d3(
    *,
    hard_limit: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    soft_limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e50a5e660ff7a2db2d48b265496dda126e4e9f841e5c3ba42d791256dfc4e61d(
    *,
    source_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1312b6393d87d551f43f65671f23eac8d0abc996e6e98e677c24ec7af387442e(
    *,
    efs_volume_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.EfsVolumeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    host: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobDefinitionPropsMixin.VolumesHostProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fdc49293e384619d9764cb0337780eaa82c560d0031c3e934ba03a11185109c(
    *,
    compute_environment_order: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobQueuePropsMixin.ComputeEnvironmentOrderProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    job_queue_name: typing.Optional[builtins.str] = None,
    job_queue_type: typing.Optional[builtins.str] = None,
    job_state_time_limit_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobQueuePropsMixin.JobStateTimeLimitActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    priority: typing.Optional[jsii.Number] = None,
    scheduling_policy_arn: typing.Optional[builtins.str] = None,
    service_environment_order: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobQueuePropsMixin.ServiceEnvironmentOrderProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e04112a89c65c353ede7579d62d11ca8f34b1aa2257c6ae4c7f22437b8c6f4(
    props: typing.Union[CfnJobQueueMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1869c5490c0d52d4fd596c94ee47ac425afaccb4e6b6d3193d162fb7ee39116(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8234d04bc6fcbf3a051114e103e8b587b47ab57ee5b9fd9cae986084f2512c0f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2895898b1aa1f556237346f63b993a6714e510e0bf62c02412d0a5ca814aef9e(
    *,
    compute_environment: typing.Optional[builtins.str] = None,
    order: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf6408373e1acdcf46d04c2447e07c5cf3da478b3695e74a19d76c90fbe8d63(
    *,
    action: typing.Optional[builtins.str] = None,
    max_time_seconds: typing.Optional[jsii.Number] = None,
    reason: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8805e81dbcb878f4442d945319b634e6d87a3684afe255251c6dc4de3ee4fa0e(
    *,
    order: typing.Optional[jsii.Number] = None,
    service_environment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c876a840b18b9e0d4124a105913cb3ba1713d47465d99a67b1a7c0501a9c919(
    *,
    fairshare_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchedulingPolicyPropsMixin.FairsharePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e87eac09e87dc387872e470daafb3941ec1cec2e0458be5fa54f0b36445d79(
    props: typing.Union[CfnSchedulingPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__679cff01d7da346ac49724cd123f49affc50192f5c6ee2c6b6313a3bc8046de4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa15fc1e36f4e3ed981abef349c724d389a891d20452dbb5754fb9d0bbddc825(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b10c5318e829357912fe9014ea934b7b3815690d45df4ab957f9a01c16466fe(
    *,
    compute_reservation: typing.Optional[jsii.Number] = None,
    share_decay_seconds: typing.Optional[jsii.Number] = None,
    share_distribution: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchedulingPolicyPropsMixin.ShareAttributesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc9b42832284ec4c052cafa3498a1440562a707c47438a6f14f49bd0e823c49(
    *,
    share_identifier: typing.Optional[builtins.str] = None,
    weight_factor: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a49cbd984bd0e164047ced343c4045d887d9893618214d4a1ea9fec2f0618a(
    *,
    capacity_limits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceEnvironmentPropsMixin.CapacityLimitProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    service_environment_name: typing.Optional[builtins.str] = None,
    service_environment_type: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__769275946851bede4c055cb074ca4ff346a6e32d46a2af3e805e91a2b5802e30(
    props: typing.Union[CfnServiceEnvironmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4492f568b83877aabfdbe6a158f67c1c442432196bfc2215c047732d7e07bfd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6ea447e8ab757ea4764889d9f7dee2167cd85a8fca36e92782aac3baea6a59(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d3bdd7187db7f26ca11c2ff0a14a65981d005818c5b18b910ea9d7dd1b6e73(
    *,
    capacity_unit: typing.Optional[builtins.str] = None,
    max_capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
