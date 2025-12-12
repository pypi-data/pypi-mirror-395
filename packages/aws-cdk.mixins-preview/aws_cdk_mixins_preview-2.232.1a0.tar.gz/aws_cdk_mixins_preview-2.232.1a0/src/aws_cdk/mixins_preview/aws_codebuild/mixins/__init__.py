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
    jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnFleetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "base_capacity": "baseCapacity",
        "compute_configuration": "computeConfiguration",
        "compute_type": "computeType",
        "environment_type": "environmentType",
        "fleet_proxy_configuration": "fleetProxyConfiguration",
        "fleet_service_role": "fleetServiceRole",
        "fleet_vpc_config": "fleetVpcConfig",
        "image_id": "imageId",
        "name": "name",
        "overflow_behavior": "overflowBehavior",
        "scaling_configuration": "scalingConfiguration",
        "tags": "tags",
    },
)
class CfnFleetMixinProps:
    def __init__(
        self,
        *,
        base_capacity: typing.Optional[jsii.Number] = None,
        compute_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.ComputeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        compute_type: typing.Optional[builtins.str] = None,
        environment_type: typing.Optional[builtins.str] = None,
        fleet_proxy_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.ProxyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        fleet_service_role: typing.Optional[builtins.str] = None,
        fleet_vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        image_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        overflow_behavior: typing.Optional[builtins.str] = None,
        scaling_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.ScalingConfigurationInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFleetPropsMixin.

        :param base_capacity: The initial number of machines allocated to the compute ﬂeet, which deﬁnes the number of builds that can run in parallel.
        :param compute_configuration: The compute configuration of the compute fleet. This is only required if ``computeType`` is set to ``ATTRIBUTE_BASED_COMPUTE`` or ``CUSTOM_INSTANCE_TYPE`` .
        :param compute_type: Information about the compute resources the compute fleet uses. Available values include:. - ``ATTRIBUTE_BASED_COMPUTE`` : Specify the amount of vCPUs, memory, disk space, and the type of machine. .. epigraph:: If you use ``ATTRIBUTE_BASED_COMPUTE`` , you must define your attributes by using ``computeConfiguration`` . AWS CodeBuild will select the cheapest instance that satisfies your specified attributes. For more information, see `Reserved capacity environment types <https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-compute-types.html#environment-reserved-capacity.types>`_ in the *AWS CodeBuild User Guide* . - ``BUILD_GENERAL1_SMALL`` : Use up to 4 GiB memory and 2 vCPUs for builds. - ``BUILD_GENERAL1_MEDIUM`` : Use up to 8 GiB memory and 4 vCPUs for builds. - ``BUILD_GENERAL1_LARGE`` : Use up to 16 GiB memory and 8 vCPUs for builds, depending on your environment type. - ``BUILD_GENERAL1_XLARGE`` : Use up to 72 GiB memory and 36 vCPUs for builds, depending on your environment type. - ``BUILD_GENERAL1_2XLARGE`` : Use up to 144 GiB memory, 72 vCPUs, and 824 GB of SSD storage for builds. This compute type supports Docker images up to 100 GB uncompressed. - ``BUILD_LAMBDA_1GB`` : Use up to 1 GiB memory for builds. Only available for environment type ``LINUX_LAMBDA_CONTAINER`` and ``ARM_LAMBDA_CONTAINER`` . - ``BUILD_LAMBDA_2GB`` : Use up to 2 GiB memory for builds. Only available for environment type ``LINUX_LAMBDA_CONTAINER`` and ``ARM_LAMBDA_CONTAINER`` . - ``BUILD_LAMBDA_4GB`` : Use up to 4 GiB memory for builds. Only available for environment type ``LINUX_LAMBDA_CONTAINER`` and ``ARM_LAMBDA_CONTAINER`` . - ``BUILD_LAMBDA_8GB`` : Use up to 8 GiB memory for builds. Only available for environment type ``LINUX_LAMBDA_CONTAINER`` and ``ARM_LAMBDA_CONTAINER`` . - ``BUILD_LAMBDA_10GB`` : Use up to 10 GiB memory for builds. Only available for environment type ``LINUX_LAMBDA_CONTAINER`` and ``ARM_LAMBDA_CONTAINER`` . If you use ``BUILD_GENERAL1_SMALL`` : - For environment type ``LINUX_CONTAINER`` , you can use up to 4 GiB memory and 2 vCPUs for builds. - For environment type ``LINUX_GPU_CONTAINER`` , you can use up to 16 GiB memory, 4 vCPUs, and 1 NVIDIA A10G Tensor Core GPU for builds. - For environment type ``ARM_CONTAINER`` , you can use up to 4 GiB memory and 2 vCPUs on ARM-based processors for builds. If you use ``BUILD_GENERAL1_LARGE`` : - For environment type ``LINUX_CONTAINER`` , you can use up to 16 GiB memory and 8 vCPUs for builds. - For environment type ``LINUX_GPU_CONTAINER`` , you can use up to 255 GiB memory, 32 vCPUs, and 4 NVIDIA Tesla V100 GPUs for builds. - For environment type ``ARM_CONTAINER`` , you can use up to 16 GiB memory and 8 vCPUs on ARM-based processors for builds. For more information, see `On-demand environment types <https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-compute-types.html#environment.types>`_ in the *AWS CodeBuild User Guide.*
        :param environment_type: The environment type of the compute fleet. - The environment type ``ARM_CONTAINER`` is available only in regions US East (N. Virginia), US East (Ohio), US West (Oregon), EU (Ireland), Asia Pacific (Mumbai), Asia Pacific (Tokyo), Asia Pacific (Singapore), Asia Pacific (Sydney), EU (Frankfurt), and South America (São Paulo). - The environment type ``ARM_EC2`` is available only in regions US East (N. Virginia), US East (Ohio), US West (Oregon), EU (Ireland), EU (Frankfurt), Asia Pacific (Tokyo), Asia Pacific (Singapore), Asia Pacific (Sydney), South America (São Paulo), and Asia Pacific (Mumbai). - The environment type ``LINUX_CONTAINER`` is available only in regions US East (N. Virginia), US East (Ohio), US West (Oregon), EU (Ireland), EU (Frankfurt), Asia Pacific (Tokyo), Asia Pacific (Singapore), Asia Pacific (Sydney), South America (São Paulo), and Asia Pacific (Mumbai). - The environment type ``LINUX_EC2`` is available only in regions US East (N. Virginia), US East (Ohio), US West (Oregon), EU (Ireland), EU (Frankfurt), Asia Pacific (Tokyo), Asia Pacific (Singapore), Asia Pacific (Sydney), South America (São Paulo), and Asia Pacific (Mumbai). - The environment type ``LINUX_GPU_CONTAINER`` is available only in regions US East (N. Virginia), US East (Ohio), US West (Oregon), EU (Ireland), EU (Frankfurt), Asia Pacific (Tokyo), and Asia Pacific (Sydney). - The environment type ``MAC_ARM`` is available only in regions US East (Ohio), US East (N. Virginia), US West (Oregon), Europe (Frankfurt), and Asia Pacific (Sydney). - The environment type ``WINDOWS_EC2`` is available only in regions US East (N. Virginia), US East (Ohio), US West (Oregon), EU (Ireland), EU (Frankfurt), Asia Pacific (Tokyo), Asia Pacific (Singapore), Asia Pacific (Sydney), South America (São Paulo), and Asia Pacific (Mumbai). - The environment type ``WINDOWS_SERVER_2019_CONTAINER`` is available only in regions US East (N. Virginia), US East (Ohio), US West (Oregon), Asia Pacific (Sydney), Asia Pacific (Tokyo), Asia Pacific (Mumbai) and EU (Ireland). - The environment type ``WINDOWS_SERVER_2022_CONTAINER`` is available only in regions US East (N. Virginia), US East (Ohio), US West (Oregon), EU (Ireland), EU (Frankfurt), Asia Pacific (Sydney), Asia Pacific (Singapore), Asia Pacific (Tokyo), South America (São Paulo) and Asia Pacific (Mumbai). For more information, see `Build environment compute types <https://docs.aws.amazon.com//codebuild/latest/userguide/build-env-ref-compute-types.html>`_ in the *AWS CodeBuild user guide* .
        :param fleet_proxy_configuration: Information about the proxy configurations that apply network access control to your reserved capacity instances.
        :param fleet_service_role: The service role associated with the compute fleet. For more information, see `Allow a user to add a permission policy for a fleet service role <https://docs.aws.amazon.com/codebuild/latest/userguide/auth-and-access-control-iam-identity-based-access-control.html#customer-managed-policies-example-permission-policy-fleet-service-role.html>`_ in the *AWS CodeBuild User Guide* .
        :param fleet_vpc_config: Information about the VPC configuration that AWS CodeBuild accesses.
        :param image_id: The Amazon Machine Image (AMI) of the compute fleet.
        :param name: The name of the compute fleet.
        :param overflow_behavior: The compute fleet overflow behavior. - For overflow behavior ``QUEUE`` , your overflow builds need to wait on the existing fleet instance to become available. - For overflow behavior ``ON_DEMAND`` , your overflow builds run on CodeBuild on-demand. .. epigraph:: If you choose to set your overflow behavior to on-demand while creating a VPC-connected fleet, make sure that you add the required VPC permissions to your project service role. For more information, see `Example policy statement to allow CodeBuild access to AWS services required to create a VPC network interface <https://docs.aws.amazon.com/codebuild/latest/userguide/auth-and-access-control-iam-identity-based-access-control.html#customer-managed-policies-example-create-vpc-network-interface>`_ .
        :param scaling_configuration: The scaling configuration of the compute fleet.
        :param tags: A list of tag key and value pairs associated with this compute fleet. These tags are available for use by AWS services that support AWS CodeBuild compute fleet tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-fleet.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
            
            cfn_fleet_mixin_props = codebuild_mixins.CfnFleetMixinProps(
                base_capacity=123,
                compute_configuration=codebuild_mixins.CfnFleetPropsMixin.ComputeConfigurationProperty(
                    disk=123,
                    instance_type="instanceType",
                    machine_type="machineType",
                    memory=123,
                    v_cpu=123
                ),
                compute_type="computeType",
                environment_type="environmentType",
                fleet_proxy_configuration=codebuild_mixins.CfnFleetPropsMixin.ProxyConfigurationProperty(
                    default_behavior="defaultBehavior",
                    ordered_proxy_rules=[codebuild_mixins.CfnFleetPropsMixin.FleetProxyRuleProperty(
                        effect="effect",
                        entities=["entities"],
                        type="type"
                    )]
                ),
                fleet_service_role="fleetServiceRole",
                fleet_vpc_config=codebuild_mixins.CfnFleetPropsMixin.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnets=["subnets"],
                    vpc_id="vpcId"
                ),
                image_id="imageId",
                name="name",
                overflow_behavior="overflowBehavior",
                scaling_configuration=codebuild_mixins.CfnFleetPropsMixin.ScalingConfigurationInputProperty(
                    max_capacity=123,
                    scaling_type="scalingType",
                    target_tracking_scaling_configs=[codebuild_mixins.CfnFleetPropsMixin.TargetTrackingScalingConfigurationProperty(
                        metric_type="metricType",
                        target_value=123
                    )]
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6678bade3381671cdb1bbd3e6a97e3ce64fda51990f47ab419711fe21bf8d8d3)
            check_type(argname="argument base_capacity", value=base_capacity, expected_type=type_hints["base_capacity"])
            check_type(argname="argument compute_configuration", value=compute_configuration, expected_type=type_hints["compute_configuration"])
            check_type(argname="argument compute_type", value=compute_type, expected_type=type_hints["compute_type"])
            check_type(argname="argument environment_type", value=environment_type, expected_type=type_hints["environment_type"])
            check_type(argname="argument fleet_proxy_configuration", value=fleet_proxy_configuration, expected_type=type_hints["fleet_proxy_configuration"])
            check_type(argname="argument fleet_service_role", value=fleet_service_role, expected_type=type_hints["fleet_service_role"])
            check_type(argname="argument fleet_vpc_config", value=fleet_vpc_config, expected_type=type_hints["fleet_vpc_config"])
            check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument overflow_behavior", value=overflow_behavior, expected_type=type_hints["overflow_behavior"])
            check_type(argname="argument scaling_configuration", value=scaling_configuration, expected_type=type_hints["scaling_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if base_capacity is not None:
            self._values["base_capacity"] = base_capacity
        if compute_configuration is not None:
            self._values["compute_configuration"] = compute_configuration
        if compute_type is not None:
            self._values["compute_type"] = compute_type
        if environment_type is not None:
            self._values["environment_type"] = environment_type
        if fleet_proxy_configuration is not None:
            self._values["fleet_proxy_configuration"] = fleet_proxy_configuration
        if fleet_service_role is not None:
            self._values["fleet_service_role"] = fleet_service_role
        if fleet_vpc_config is not None:
            self._values["fleet_vpc_config"] = fleet_vpc_config
        if image_id is not None:
            self._values["image_id"] = image_id
        if name is not None:
            self._values["name"] = name
        if overflow_behavior is not None:
            self._values["overflow_behavior"] = overflow_behavior
        if scaling_configuration is not None:
            self._values["scaling_configuration"] = scaling_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def base_capacity(self) -> typing.Optional[jsii.Number]:
        '''The initial number of machines allocated to the compute ﬂeet, which deﬁnes the number of builds that can run in parallel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-fleet.html#cfn-codebuild-fleet-basecapacity
        '''
        result = self._values.get("base_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def compute_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.ComputeConfigurationProperty"]]:
        '''The compute configuration of the compute fleet.

        This is only required if ``computeType`` is set to ``ATTRIBUTE_BASED_COMPUTE`` or ``CUSTOM_INSTANCE_TYPE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-fleet.html#cfn-codebuild-fleet-computeconfiguration
        '''
        result = self._values.get("compute_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.ComputeConfigurationProperty"]], result)

    @builtins.property
    def compute_type(self) -> typing.Optional[builtins.str]:
        '''Information about the compute resources the compute fleet uses. Available values include:.

        - ``ATTRIBUTE_BASED_COMPUTE`` : Specify the amount of vCPUs, memory, disk space, and the type of machine.

        .. epigraph::

           If you use ``ATTRIBUTE_BASED_COMPUTE`` , you must define your attributes by using ``computeConfiguration`` . AWS CodeBuild will select the cheapest instance that satisfies your specified attributes. For more information, see `Reserved capacity environment types <https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-compute-types.html#environment-reserved-capacity.types>`_ in the *AWS CodeBuild User Guide* .

        - ``BUILD_GENERAL1_SMALL`` : Use up to 4 GiB memory and 2 vCPUs for builds.
        - ``BUILD_GENERAL1_MEDIUM`` : Use up to 8 GiB memory and 4 vCPUs for builds.
        - ``BUILD_GENERAL1_LARGE`` : Use up to 16 GiB memory and 8 vCPUs for builds, depending on your environment type.
        - ``BUILD_GENERAL1_XLARGE`` : Use up to 72 GiB memory and 36 vCPUs for builds, depending on your environment type.
        - ``BUILD_GENERAL1_2XLARGE`` : Use up to 144 GiB memory, 72 vCPUs, and 824 GB of SSD storage for builds. This compute type supports Docker images up to 100 GB uncompressed.
        - ``BUILD_LAMBDA_1GB`` : Use up to 1 GiB memory for builds. Only available for environment type ``LINUX_LAMBDA_CONTAINER`` and ``ARM_LAMBDA_CONTAINER`` .
        - ``BUILD_LAMBDA_2GB`` : Use up to 2 GiB memory for builds. Only available for environment type ``LINUX_LAMBDA_CONTAINER`` and ``ARM_LAMBDA_CONTAINER`` .
        - ``BUILD_LAMBDA_4GB`` : Use up to 4 GiB memory for builds. Only available for environment type ``LINUX_LAMBDA_CONTAINER`` and ``ARM_LAMBDA_CONTAINER`` .
        - ``BUILD_LAMBDA_8GB`` : Use up to 8 GiB memory for builds. Only available for environment type ``LINUX_LAMBDA_CONTAINER`` and ``ARM_LAMBDA_CONTAINER`` .
        - ``BUILD_LAMBDA_10GB`` : Use up to 10 GiB memory for builds. Only available for environment type ``LINUX_LAMBDA_CONTAINER`` and ``ARM_LAMBDA_CONTAINER`` .

        If you use ``BUILD_GENERAL1_SMALL`` :

        - For environment type ``LINUX_CONTAINER`` , you can use up to 4 GiB memory and 2 vCPUs for builds.
        - For environment type ``LINUX_GPU_CONTAINER`` , you can use up to 16 GiB memory, 4 vCPUs, and 1 NVIDIA A10G Tensor Core GPU for builds.
        - For environment type ``ARM_CONTAINER`` , you can use up to 4 GiB memory and 2 vCPUs on ARM-based processors for builds.

        If you use ``BUILD_GENERAL1_LARGE`` :

        - For environment type ``LINUX_CONTAINER`` , you can use up to 16 GiB memory and 8 vCPUs for builds.
        - For environment type ``LINUX_GPU_CONTAINER`` , you can use up to 255 GiB memory, 32 vCPUs, and 4 NVIDIA Tesla V100 GPUs for builds.
        - For environment type ``ARM_CONTAINER`` , you can use up to 16 GiB memory and 8 vCPUs on ARM-based processors for builds.

        For more information, see `On-demand environment types <https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-compute-types.html#environment.types>`_ in the *AWS CodeBuild User Guide.*

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-fleet.html#cfn-codebuild-fleet-computetype
        '''
        result = self._values.get("compute_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_type(self) -> typing.Optional[builtins.str]:
        '''The environment type of the compute fleet.

        - The environment type ``ARM_CONTAINER`` is available only in regions US East (N. Virginia), US East (Ohio), US West (Oregon), EU (Ireland), Asia Pacific (Mumbai), Asia Pacific (Tokyo), Asia Pacific (Singapore), Asia Pacific (Sydney), EU (Frankfurt), and South America (São Paulo).
        - The environment type ``ARM_EC2`` is available only in regions US East (N. Virginia), US East (Ohio), US West (Oregon), EU (Ireland), EU (Frankfurt), Asia Pacific (Tokyo), Asia Pacific (Singapore), Asia Pacific (Sydney), South America (São Paulo), and Asia Pacific (Mumbai).
        - The environment type ``LINUX_CONTAINER`` is available only in regions US East (N. Virginia), US East (Ohio), US West (Oregon), EU (Ireland), EU (Frankfurt), Asia Pacific (Tokyo), Asia Pacific (Singapore), Asia Pacific (Sydney), South America (São Paulo), and Asia Pacific (Mumbai).
        - The environment type ``LINUX_EC2`` is available only in regions US East (N. Virginia), US East (Ohio), US West (Oregon), EU (Ireland), EU (Frankfurt), Asia Pacific (Tokyo), Asia Pacific (Singapore), Asia Pacific (Sydney), South America (São Paulo), and Asia Pacific (Mumbai).
        - The environment type ``LINUX_GPU_CONTAINER`` is available only in regions US East (N. Virginia), US East (Ohio), US West (Oregon), EU (Ireland), EU (Frankfurt), Asia Pacific (Tokyo), and Asia Pacific (Sydney).
        - The environment type ``MAC_ARM`` is available only in regions US East (Ohio), US East (N. Virginia), US West (Oregon), Europe (Frankfurt), and Asia Pacific (Sydney).
        - The environment type ``WINDOWS_EC2`` is available only in regions US East (N. Virginia), US East (Ohio), US West (Oregon), EU (Ireland), EU (Frankfurt), Asia Pacific (Tokyo), Asia Pacific (Singapore), Asia Pacific (Sydney), South America (São Paulo), and Asia Pacific (Mumbai).
        - The environment type ``WINDOWS_SERVER_2019_CONTAINER`` is available only in regions US East (N. Virginia), US East (Ohio), US West (Oregon), Asia Pacific (Sydney), Asia Pacific (Tokyo), Asia Pacific (Mumbai) and EU (Ireland).
        - The environment type ``WINDOWS_SERVER_2022_CONTAINER`` is available only in regions US East (N. Virginia), US East (Ohio), US West (Oregon), EU (Ireland), EU (Frankfurt), Asia Pacific (Sydney), Asia Pacific (Singapore), Asia Pacific (Tokyo), South America (São Paulo) and Asia Pacific (Mumbai).

        For more information, see `Build environment compute types <https://docs.aws.amazon.com//codebuild/latest/userguide/build-env-ref-compute-types.html>`_ in the *AWS CodeBuild user guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-fleet.html#cfn-codebuild-fleet-environmenttype
        '''
        result = self._values.get("environment_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fleet_proxy_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.ProxyConfigurationProperty"]]:
        '''Information about the proxy configurations that apply network access control to your reserved capacity instances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-fleet.html#cfn-codebuild-fleet-fleetproxyconfiguration
        '''
        result = self._values.get("fleet_proxy_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.ProxyConfigurationProperty"]], result)

    @builtins.property
    def fleet_service_role(self) -> typing.Optional[builtins.str]:
        '''The service role associated with the compute fleet.

        For more information, see `Allow a user to add a permission policy for a fleet service role <https://docs.aws.amazon.com/codebuild/latest/userguide/auth-and-access-control-iam-identity-based-access-control.html#customer-managed-policies-example-permission-policy-fleet-service-role.html>`_ in the *AWS CodeBuild User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-fleet.html#cfn-codebuild-fleet-fleetservicerole
        '''
        result = self._values.get("fleet_service_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fleet_vpc_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.VpcConfigProperty"]]:
        '''Information about the VPC configuration that AWS CodeBuild accesses.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-fleet.html#cfn-codebuild-fleet-fleetvpcconfig
        '''
        result = self._values.get("fleet_vpc_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.VpcConfigProperty"]], result)

    @builtins.property
    def image_id(self) -> typing.Optional[builtins.str]:
        '''The Amazon Machine Image (AMI) of the compute fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-fleet.html#cfn-codebuild-fleet-imageid
        '''
        result = self._values.get("image_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the compute fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-fleet.html#cfn-codebuild-fleet-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def overflow_behavior(self) -> typing.Optional[builtins.str]:
        '''The compute fleet overflow behavior.

        - For overflow behavior ``QUEUE`` , your overflow builds need to wait on the existing fleet instance to become available.
        - For overflow behavior ``ON_DEMAND`` , your overflow builds run on CodeBuild on-demand.

        .. epigraph::

           If you choose to set your overflow behavior to on-demand while creating a VPC-connected fleet, make sure that you add the required VPC permissions to your project service role. For more information, see `Example policy statement to allow CodeBuild access to AWS services required to create a VPC network interface <https://docs.aws.amazon.com/codebuild/latest/userguide/auth-and-access-control-iam-identity-based-access-control.html#customer-managed-policies-example-create-vpc-network-interface>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-fleet.html#cfn-codebuild-fleet-overflowbehavior
        '''
        result = self._values.get("overflow_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.ScalingConfigurationInputProperty"]]:
        '''The scaling configuration of the compute fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-fleet.html#cfn-codebuild-fleet-scalingconfiguration
        '''
        result = self._values.get("scaling_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.ScalingConfigurationInputProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tag key and value pairs associated with this compute fleet.

        These tags are available for use by AWS services that support AWS CodeBuild compute fleet tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-fleet.html#cfn-codebuild-fleet-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFleetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFleetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnFleetPropsMixin",
):
    '''The ``AWS::CodeBuild::Fleet`` resource configures a compute fleet, a set of dedicated instances for your build environment.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-fleet.html
    :cloudformationResource: AWS::CodeBuild::Fleet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
        
        cfn_fleet_props_mixin = codebuild_mixins.CfnFleetPropsMixin(codebuild_mixins.CfnFleetMixinProps(
            base_capacity=123,
            compute_configuration=codebuild_mixins.CfnFleetPropsMixin.ComputeConfigurationProperty(
                disk=123,
                instance_type="instanceType",
                machine_type="machineType",
                memory=123,
                v_cpu=123
            ),
            compute_type="computeType",
            environment_type="environmentType",
            fleet_proxy_configuration=codebuild_mixins.CfnFleetPropsMixin.ProxyConfigurationProperty(
                default_behavior="defaultBehavior",
                ordered_proxy_rules=[codebuild_mixins.CfnFleetPropsMixin.FleetProxyRuleProperty(
                    effect="effect",
                    entities=["entities"],
                    type="type"
                )]
            ),
            fleet_service_role="fleetServiceRole",
            fleet_vpc_config=codebuild_mixins.CfnFleetPropsMixin.VpcConfigProperty(
                security_group_ids=["securityGroupIds"],
                subnets=["subnets"],
                vpc_id="vpcId"
            ),
            image_id="imageId",
            name="name",
            overflow_behavior="overflowBehavior",
            scaling_configuration=codebuild_mixins.CfnFleetPropsMixin.ScalingConfigurationInputProperty(
                max_capacity=123,
                scaling_type="scalingType",
                target_tracking_scaling_configs=[codebuild_mixins.CfnFleetPropsMixin.TargetTrackingScalingConfigurationProperty(
                    metric_type="metricType",
                    target_value=123
                )]
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFleetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CodeBuild::Fleet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__718c89f510f8f36254066217c006415cf2775f8e4294a7fd3b5d07237b730f99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fe16a895a96c60080d533e506ce9f66058e7a5085eeba733b5d3262f0793b54)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35073713375292328621156a58409c2cc65795d1292fa03c868de27c6da6f24a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFleetMixinProps:
        return typing.cast(CfnFleetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnFleetPropsMixin.ComputeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "disk": "disk",
            "instance_type": "instanceType",
            "machine_type": "machineType",
            "memory": "memory",
            "v_cpu": "vCpu",
        },
    )
    class ComputeConfigurationProperty:
        def __init__(
            self,
            *,
            disk: typing.Optional[jsii.Number] = None,
            instance_type: typing.Optional[builtins.str] = None,
            machine_type: typing.Optional[builtins.str] = None,
            memory: typing.Optional[jsii.Number] = None,
            v_cpu: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains compute attributes.

            These attributes only need be specified when your project's or fleet's ``computeType`` is set to ``ATTRIBUTE_BASED_COMPUTE`` or ``CUSTOM_INSTANCE_TYPE`` .

            :param disk: The amount of disk space of the instance type included in your fleet.
            :param instance_type: The EC2 instance type to be launched in your fleet.
            :param machine_type: The machine type of the instance type included in your fleet.
            :param memory: The amount of memory of the instance type included in your fleet.
            :param v_cpu: The number of vCPUs of the instance type included in your fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-computeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                compute_configuration_property = codebuild_mixins.CfnFleetPropsMixin.ComputeConfigurationProperty(
                    disk=123,
                    instance_type="instanceType",
                    machine_type="machineType",
                    memory=123,
                    v_cpu=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__36496bf890fb5555997aaa5bcb4f405a0df84fce23768fa8d1796ad346e6c347)
                check_type(argname="argument disk", value=disk, expected_type=type_hints["disk"])
                check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
                check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
                check_type(argname="argument v_cpu", value=v_cpu, expected_type=type_hints["v_cpu"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if disk is not None:
                self._values["disk"] = disk
            if instance_type is not None:
                self._values["instance_type"] = instance_type
            if machine_type is not None:
                self._values["machine_type"] = machine_type
            if memory is not None:
                self._values["memory"] = memory
            if v_cpu is not None:
                self._values["v_cpu"] = v_cpu

        @builtins.property
        def disk(self) -> typing.Optional[jsii.Number]:
            '''The amount of disk space of the instance type included in your fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-computeconfiguration.html#cfn-codebuild-fleet-computeconfiguration-disk
            '''
            result = self._values.get("disk")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            '''The EC2 instance type to be launched in your fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-computeconfiguration.html#cfn-codebuild-fleet-computeconfiguration-instancetype
            '''
            result = self._values.get("instance_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def machine_type(self) -> typing.Optional[builtins.str]:
            '''The machine type of the instance type included in your fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-computeconfiguration.html#cfn-codebuild-fleet-computeconfiguration-machinetype
            '''
            result = self._values.get("machine_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def memory(self) -> typing.Optional[jsii.Number]:
            '''The amount of memory of the instance type included in your fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-computeconfiguration.html#cfn-codebuild-fleet-computeconfiguration-memory
            '''
            result = self._values.get("memory")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def v_cpu(self) -> typing.Optional[jsii.Number]:
            '''The number of vCPUs of the instance type included in your fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-computeconfiguration.html#cfn-codebuild-fleet-computeconfiguration-vcpu
            '''
            result = self._values.get("v_cpu")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComputeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnFleetPropsMixin.FleetProxyRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"effect": "effect", "entities": "entities", "type": "type"},
    )
    class FleetProxyRuleProperty:
        def __init__(
            self,
            *,
            effect: typing.Optional[builtins.str] = None,
            entities: typing.Optional[typing.Sequence[builtins.str]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the proxy rule for your reserved capacity instances.

            :param effect: The behavior of the proxy rule.
            :param entities: The destination of the proxy rule.
            :param type: The type of proxy rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-fleetproxyrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                fleet_proxy_rule_property = codebuild_mixins.CfnFleetPropsMixin.FleetProxyRuleProperty(
                    effect="effect",
                    entities=["entities"],
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7f21ac34db3816fd5c46ec904caf734d78caa5eb0899fc7c3a07b09ff4164b6e)
                check_type(argname="argument effect", value=effect, expected_type=type_hints["effect"])
                check_type(argname="argument entities", value=entities, expected_type=type_hints["entities"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if effect is not None:
                self._values["effect"] = effect
            if entities is not None:
                self._values["entities"] = entities
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def effect(self) -> typing.Optional[builtins.str]:
            '''The behavior of the proxy rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-fleetproxyrule.html#cfn-codebuild-fleet-fleetproxyrule-effect
            '''
            result = self._values.get("effect")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def entities(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The destination of the proxy rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-fleetproxyrule.html#cfn-codebuild-fleet-fleetproxyrule-entities
            '''
            result = self._values.get("entities")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of proxy rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-fleetproxyrule.html#cfn-codebuild-fleet-fleetproxyrule-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FleetProxyRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnFleetPropsMixin.ProxyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_behavior": "defaultBehavior",
            "ordered_proxy_rules": "orderedProxyRules",
        },
    )
    class ProxyConfigurationProperty:
        def __init__(
            self,
            *,
            default_behavior: typing.Optional[builtins.str] = None,
            ordered_proxy_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.FleetProxyRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Information about the proxy configurations that apply network access control to your reserved capacity instances.

            :param default_behavior: The default behavior of outgoing traffic.
            :param ordered_proxy_rules: An array of ``FleetProxyRule`` objects that represent the specified destination domains or IPs to allow or deny network access control to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-proxyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                proxy_configuration_property = codebuild_mixins.CfnFleetPropsMixin.ProxyConfigurationProperty(
                    default_behavior="defaultBehavior",
                    ordered_proxy_rules=[codebuild_mixins.CfnFleetPropsMixin.FleetProxyRuleProperty(
                        effect="effect",
                        entities=["entities"],
                        type="type"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8fff32fccca2ecaa6f3ab0abb011879cbb4f3c5861cf2b3237eac252e387e4da)
                check_type(argname="argument default_behavior", value=default_behavior, expected_type=type_hints["default_behavior"])
                check_type(argname="argument ordered_proxy_rules", value=ordered_proxy_rules, expected_type=type_hints["ordered_proxy_rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_behavior is not None:
                self._values["default_behavior"] = default_behavior
            if ordered_proxy_rules is not None:
                self._values["ordered_proxy_rules"] = ordered_proxy_rules

        @builtins.property
        def default_behavior(self) -> typing.Optional[builtins.str]:
            '''The default behavior of outgoing traffic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-proxyconfiguration.html#cfn-codebuild-fleet-proxyconfiguration-defaultbehavior
            '''
            result = self._values.get("default_behavior")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ordered_proxy_rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.FleetProxyRuleProperty"]]]]:
            '''An array of ``FleetProxyRule`` objects that represent the specified destination domains or IPs to allow or deny network access control to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-proxyconfiguration.html#cfn-codebuild-fleet-proxyconfiguration-orderedproxyrules
            '''
            result = self._values.get("ordered_proxy_rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.FleetProxyRuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProxyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnFleetPropsMixin.ScalingConfigurationInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_capacity": "maxCapacity",
            "scaling_type": "scalingType",
            "target_tracking_scaling_configs": "targetTrackingScalingConfigs",
        },
    )
    class ScalingConfigurationInputProperty:
        def __init__(
            self,
            *,
            max_capacity: typing.Optional[jsii.Number] = None,
            scaling_type: typing.Optional[builtins.str] = None,
            target_tracking_scaling_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.TargetTrackingScalingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The scaling configuration input of a compute fleet.

            :param max_capacity: The maximum number of instances in the ﬂeet when auto-scaling.
            :param scaling_type: The scaling type for a compute fleet.
            :param target_tracking_scaling_configs: A list of ``TargetTrackingScalingConfiguration`` objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-scalingconfigurationinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                scaling_configuration_input_property = codebuild_mixins.CfnFleetPropsMixin.ScalingConfigurationInputProperty(
                    max_capacity=123,
                    scaling_type="scalingType",
                    target_tracking_scaling_configs=[codebuild_mixins.CfnFleetPropsMixin.TargetTrackingScalingConfigurationProperty(
                        metric_type="metricType",
                        target_value=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__be2b2ed8505f87c03005008bc0d1f19baba425d999a32dc6e29e02596cedc477)
                check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
                check_type(argname="argument scaling_type", value=scaling_type, expected_type=type_hints["scaling_type"])
                check_type(argname="argument target_tracking_scaling_configs", value=target_tracking_scaling_configs, expected_type=type_hints["target_tracking_scaling_configs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_capacity is not None:
                self._values["max_capacity"] = max_capacity
            if scaling_type is not None:
                self._values["scaling_type"] = scaling_type
            if target_tracking_scaling_configs is not None:
                self._values["target_tracking_scaling_configs"] = target_tracking_scaling_configs

        @builtins.property
        def max_capacity(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of instances in the ﬂeet when auto-scaling.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-scalingconfigurationinput.html#cfn-codebuild-fleet-scalingconfigurationinput-maxcapacity
            '''
            result = self._values.get("max_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def scaling_type(self) -> typing.Optional[builtins.str]:
            '''The scaling type for a compute fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-scalingconfigurationinput.html#cfn-codebuild-fleet-scalingconfigurationinput-scalingtype
            '''
            result = self._values.get("scaling_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_tracking_scaling_configs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.TargetTrackingScalingConfigurationProperty"]]]]:
            '''A list of ``TargetTrackingScalingConfiguration`` objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-scalingconfigurationinput.html#cfn-codebuild-fleet-scalingconfigurationinput-targettrackingscalingconfigs
            '''
            result = self._values.get("target_tracking_scaling_configs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.TargetTrackingScalingConfigurationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingConfigurationInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnFleetPropsMixin.TargetTrackingScalingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"metric_type": "metricType", "target_value": "targetValue"},
    )
    class TargetTrackingScalingConfigurationProperty:
        def __init__(
            self,
            *,
            metric_type: typing.Optional[builtins.str] = None,
            target_value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines when a new instance is auto-scaled into the compute fleet.

            :param metric_type: The metric type to determine auto-scaling.
            :param target_value: The value of ``metricType`` when to start scaling.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-targettrackingscalingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                target_tracking_scaling_configuration_property = codebuild_mixins.CfnFleetPropsMixin.TargetTrackingScalingConfigurationProperty(
                    metric_type="metricType",
                    target_value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ce9bd1dbca62fae1e55c2e132857619e77e611696c879d74538dab037676de48)
                check_type(argname="argument metric_type", value=metric_type, expected_type=type_hints["metric_type"])
                check_type(argname="argument target_value", value=target_value, expected_type=type_hints["target_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric_type is not None:
                self._values["metric_type"] = metric_type
            if target_value is not None:
                self._values["target_value"] = target_value

        @builtins.property
        def metric_type(self) -> typing.Optional[builtins.str]:
            '''The metric type to determine auto-scaling.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-targettrackingscalingconfiguration.html#cfn-codebuild-fleet-targettrackingscalingconfiguration-metrictype
            '''
            result = self._values.get("metric_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_value(self) -> typing.Optional[jsii.Number]:
            '''The value of ``metricType`` when to start scaling.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-targettrackingscalingconfiguration.html#cfn-codebuild-fleet-targettrackingscalingconfiguration-targetvalue
            '''
            result = self._values.get("target_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetTrackingScalingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnFleetPropsMixin.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnets": "subnets",
            "vpc_id": "vpcId",
        },
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
            vpc_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the VPC configuration that AWS CodeBuild accesses.

            :param security_group_ids: A list of one or more security groups IDs in your Amazon VPC.
            :param subnets: A list of one or more subnet IDs in your Amazon VPC.
            :param vpc_id: The ID of the Amazon VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                vpc_config_property = codebuild_mixins.CfnFleetPropsMixin.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnets=["subnets"],
                    vpc_id="vpcId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4ecb007eb53ddbd27387fb5bebdc46bd5df61d257791aa98e32b84078e1bea6b)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnets is not None:
                self._values["subnets"] = subnets
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of one or more security groups IDs in your Amazon VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-vpcconfig.html#cfn-codebuild-fleet-vpcconfig-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of one or more subnet IDs in your Amazon VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-vpcconfig.html#cfn-codebuild-fleet-vpcconfig-subnets
            '''
            result = self._values.get("subnets")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the Amazon VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-fleet-vpcconfig.html#cfn-codebuild-fleet-vpcconfig-vpcid
            '''
            result = self._values.get("vpc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "artifacts": "artifacts",
        "auto_retry_limit": "autoRetryLimit",
        "badge_enabled": "badgeEnabled",
        "build_batch_config": "buildBatchConfig",
        "cache": "cache",
        "concurrent_build_limit": "concurrentBuildLimit",
        "description": "description",
        "encryption_key": "encryptionKey",
        "environment": "environment",
        "file_system_locations": "fileSystemLocations",
        "logs_config": "logsConfig",
        "name": "name",
        "queued_timeout_in_minutes": "queuedTimeoutInMinutes",
        "resource_access_role": "resourceAccessRole",
        "secondary_artifacts": "secondaryArtifacts",
        "secondary_sources": "secondarySources",
        "secondary_source_versions": "secondarySourceVersions",
        "service_role": "serviceRole",
        "source": "source",
        "source_version": "sourceVersion",
        "tags": "tags",
        "timeout_in_minutes": "timeoutInMinutes",
        "triggers": "triggers",
        "visibility": "visibility",
        "vpc_config": "vpcConfig",
    },
)
class CfnProjectMixinProps:
    def __init__(
        self,
        *,
        artifacts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.ArtifactsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        auto_retry_limit: typing.Optional[jsii.Number] = None,
        badge_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        build_batch_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.ProjectBuildBatchConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        cache: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.ProjectCacheProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        concurrent_build_limit: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.EnvironmentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        file_system_locations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.ProjectFileSystemLocationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        logs_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.LogsConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        queued_timeout_in_minutes: typing.Optional[jsii.Number] = None,
        resource_access_role: typing.Optional[builtins.str] = None,
        secondary_artifacts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.ArtifactsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        secondary_sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.SourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        secondary_source_versions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.ProjectSourceVersionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        service_role: typing.Optional[builtins.str] = None,
        source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.SourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        source_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
        triggers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.ProjectTriggersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        visibility: typing.Optional[builtins.str] = None,
        vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnProjectPropsMixin.

        :param artifacts: ``Artifacts`` is a property of the `AWS::CodeBuild::Project <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html>`_ resource that specifies output settings for artifacts generated by an AWS CodeBuild build.
        :param auto_retry_limit: 
        :param badge_enabled: Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge. For more information, see `Build Badges Sample <https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-badges.html>`_ in the *AWS CodeBuild User Guide* . .. epigraph:: Including build badges with your project is currently not supported if the source type is CodePipeline. If you specify ``CODEPIPELINE`` for the ``Source`` property, do not specify the ``BadgeEnabled`` property.
        :param build_batch_config: A ``ProjectBuildBatchConfig`` object that defines the batch build options for the project.
        :param cache: Settings that AWS CodeBuild uses to store and reuse build dependencies.
        :param concurrent_build_limit: The maximum number of concurrent builds that are allowed for this project. New builds are only started if the current number of builds is less than or equal to this limit. If the current build count meets this limit, new builds are throttled and are not run.
        :param description: A description that makes the build project easy to identify.
        :param encryption_key: The AWS Key Management Service customer master key (CMK) to be used for encrypting the build output artifacts. .. epigraph:: You can use a cross-account KMS key to encrypt the build output artifacts if your service role has permission to that key. You can specify either the Amazon Resource Name (ARN) of the CMK or, if available, the CMK's alias (using the format ``alias/<alias-name>`` ). If you don't specify a value, CodeBuild uses the managed CMK for Amazon Simple Storage Service (Amazon S3).
        :param environment: The build environment settings for the project, such as the environment type or the environment variables to use for the build environment.
        :param file_system_locations: An array of ``ProjectFileSystemLocation`` objects for a CodeBuild build project. A ``ProjectFileSystemLocation`` object specifies the ``identifier`` , ``location`` , ``mountOptions`` , ``mountPoint`` , and ``type`` of a file system created using Amazon Elastic File System.
        :param logs_config: Information about logs for the build project. A project can create logs in CloudWatch Logs, an S3 bucket, or both.
        :param name: The name of the build project. The name must be unique across all of the projects in your AWS account .
        :param queued_timeout_in_minutes: The number of minutes a build is allowed to be queued before it times out.
        :param resource_access_role: The ARN of the IAM role that enables CodeBuild to access the CloudWatch Logs and Amazon S3 artifacts for the project's builds.
        :param secondary_artifacts: A list of ``Artifacts`` objects. Each artifacts object specifies output settings that the project generates during a build.
        :param secondary_sources: An array of ``ProjectSource`` objects.
        :param secondary_source_versions: An array of ``ProjectSourceVersion`` objects. If ``secondarySourceVersions`` is specified at the build level, then they take over these ``secondarySourceVersions`` (at the project level).
        :param service_role: The ARN of the IAM role that enables AWS CodeBuild to interact with dependent AWS services on behalf of the AWS account.
        :param source: The source code settings for the project, such as the source code's repository type and location.
        :param source_version: A version of the build input to be built for this project. If not specified, the latest version is used. If specified, it must be one of: - For CodeCommit: the commit ID, branch, or Git tag to use. - For GitHub: the commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build. If a pull request ID is specified, it must use the format ``pr/pull-request-ID`` (for example ``pr/25`` ). If a branch name is specified, the branch's HEAD commit ID is used. If not specified, the default branch's HEAD commit ID is used. - For GitLab: the commit ID, branch, or Git tag to use. - For Bitbucket: the commit ID, branch name, or tag name that corresponds to the version of the source code you want to build. If a branch name is specified, the branch's HEAD commit ID is used. If not specified, the default branch's HEAD commit ID is used. - For Amazon S3: the version ID of the object that represents the build input ZIP file to use. If ``sourceVersion`` is specified at the build level, then that version takes precedence over this ``sourceVersion`` (at the project level). For more information, see `Source Version Sample with CodeBuild <https://docs.aws.amazon.com/codebuild/latest/userguide/sample-source-version.html>`_ in the *AWS CodeBuild User Guide* .
        :param tags: An arbitrary set of tags (key-value pairs) for the AWS CodeBuild project. These tags are available for use by AWS services that support AWS CodeBuild build project tags.
        :param timeout_in_minutes: How long, in minutes, from 5 to 2160 (36 hours), for AWS CodeBuild to wait before timing out any related build that did not get marked as completed. The default is 60 minutes.
        :param triggers: For an existing AWS CodeBuild build project that has its source code stored in a GitHub repository, enables AWS CodeBuild to begin automatically rebuilding the source code every time a code change is pushed to the repository.
        :param visibility: Specifies the visibility of the project's builds. Possible values are:. - **PUBLIC_READ** - The project builds are visible to the public. - **PRIVATE** - The project builds are not visible to the public.
        :param vpc_config: ``VpcConfig`` specifies settings that enable AWS CodeBuild to access resources in an Amazon VPC. For more information, see `Use AWS CodeBuild with Amazon Virtual Private Cloud <https://docs.aws.amazon.com/codebuild/latest/userguide/vpc-support.html>`_ in the *AWS CodeBuild User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
            
            cfn_project_mixin_props = codebuild_mixins.CfnProjectMixinProps(
                artifacts=codebuild_mixins.CfnProjectPropsMixin.ArtifactsProperty(
                    artifact_identifier="artifactIdentifier",
                    encryption_disabled=False,
                    location="location",
                    name="name",
                    namespace_type="namespaceType",
                    override_artifact_name=False,
                    packaging="packaging",
                    path="path",
                    type="type"
                ),
                auto_retry_limit=123,
                badge_enabled=False,
                build_batch_config=codebuild_mixins.CfnProjectPropsMixin.ProjectBuildBatchConfigProperty(
                    batch_report_mode="batchReportMode",
                    combine_artifacts=False,
                    restrictions=codebuild_mixins.CfnProjectPropsMixin.BatchRestrictionsProperty(
                        compute_types_allowed=["computeTypesAllowed"],
                        maximum_builds_allowed=123
                    ),
                    service_role="serviceRole",
                    timeout_in_mins=123
                ),
                cache=codebuild_mixins.CfnProjectPropsMixin.ProjectCacheProperty(
                    cache_namespace="cacheNamespace",
                    location="location",
                    modes=["modes"],
                    type="type"
                ),
                concurrent_build_limit=123,
                description="description",
                encryption_key="encryptionKey",
                environment=codebuild_mixins.CfnProjectPropsMixin.EnvironmentProperty(
                    certificate="certificate",
                    compute_type="computeType",
                    docker_server=codebuild_mixins.CfnProjectPropsMixin.DockerServerProperty(
                        compute_type="computeType",
                        security_group_ids=["securityGroupIds"]
                    ),
                    environment_variables=[codebuild_mixins.CfnProjectPropsMixin.EnvironmentVariableProperty(
                        name="name",
                        type="type",
                        value="value"
                    )],
                    fleet=codebuild_mixins.CfnProjectPropsMixin.ProjectFleetProperty(
                        fleet_arn="fleetArn"
                    ),
                    image="image",
                    image_pull_credentials_type="imagePullCredentialsType",
                    privileged_mode=False,
                    registry_credential=codebuild_mixins.CfnProjectPropsMixin.RegistryCredentialProperty(
                        credential="credential",
                        credential_provider="credentialProvider"
                    ),
                    type="type"
                ),
                file_system_locations=[codebuild_mixins.CfnProjectPropsMixin.ProjectFileSystemLocationProperty(
                    identifier="identifier",
                    location="location",
                    mount_options="mountOptions",
                    mount_point="mountPoint",
                    type="type"
                )],
                logs_config=codebuild_mixins.CfnProjectPropsMixin.LogsConfigProperty(
                    cloud_watch_logs=codebuild_mixins.CfnProjectPropsMixin.CloudWatchLogsConfigProperty(
                        group_name="groupName",
                        status="status",
                        stream_name="streamName"
                    ),
                    s3_logs=codebuild_mixins.CfnProjectPropsMixin.S3LogsConfigProperty(
                        encryption_disabled=False,
                        location="location",
                        status="status"
                    )
                ),
                name="name",
                queued_timeout_in_minutes=123,
                resource_access_role="resourceAccessRole",
                secondary_artifacts=[codebuild_mixins.CfnProjectPropsMixin.ArtifactsProperty(
                    artifact_identifier="artifactIdentifier",
                    encryption_disabled=False,
                    location="location",
                    name="name",
                    namespace_type="namespaceType",
                    override_artifact_name=False,
                    packaging="packaging",
                    path="path",
                    type="type"
                )],
                secondary_sources=[codebuild_mixins.CfnProjectPropsMixin.SourceProperty(
                    auth=codebuild_mixins.CfnProjectPropsMixin.SourceAuthProperty(
                        resource="resource",
                        type="type"
                    ),
                    build_spec="buildSpec",
                    build_status_config=codebuild_mixins.CfnProjectPropsMixin.BuildStatusConfigProperty(
                        context="context",
                        target_url="targetUrl"
                    ),
                    git_clone_depth=123,
                    git_submodules_config=codebuild_mixins.CfnProjectPropsMixin.GitSubmodulesConfigProperty(
                        fetch_submodules=False
                    ),
                    insecure_ssl=False,
                    location="location",
                    report_build_status=False,
                    source_identifier="sourceIdentifier",
                    type="type"
                )],
                secondary_source_versions=[codebuild_mixins.CfnProjectPropsMixin.ProjectSourceVersionProperty(
                    source_identifier="sourceIdentifier",
                    source_version="sourceVersion"
                )],
                service_role="serviceRole",
                source=codebuild_mixins.CfnProjectPropsMixin.SourceProperty(
                    auth=codebuild_mixins.CfnProjectPropsMixin.SourceAuthProperty(
                        resource="resource",
                        type="type"
                    ),
                    build_spec="buildSpec",
                    build_status_config=codebuild_mixins.CfnProjectPropsMixin.BuildStatusConfigProperty(
                        context="context",
                        target_url="targetUrl"
                    ),
                    git_clone_depth=123,
                    git_submodules_config=codebuild_mixins.CfnProjectPropsMixin.GitSubmodulesConfigProperty(
                        fetch_submodules=False
                    ),
                    insecure_ssl=False,
                    location="location",
                    report_build_status=False,
                    source_identifier="sourceIdentifier",
                    type="type"
                ),
                source_version="sourceVersion",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                timeout_in_minutes=123,
                triggers=codebuild_mixins.CfnProjectPropsMixin.ProjectTriggersProperty(
                    build_type="buildType",
                    filter_groups=[[codebuild_mixins.CfnProjectPropsMixin.WebhookFilterProperty(
                        exclude_matched_pattern=False,
                        pattern="pattern",
                        type="type"
                    )]],
                    pull_request_build_policy=codebuild_mixins.CfnProjectPropsMixin.PullRequestBuildPolicyProperty(
                        approver_roles=["approverRoles"],
                        requires_comment_approval="requiresCommentApproval"
                    ),
                    scope_configuration=codebuild_mixins.CfnProjectPropsMixin.ScopeConfigurationProperty(
                        domain="domain",
                        name="name",
                        scope="scope"
                    ),
                    webhook=False
                ),
                visibility="visibility",
                vpc_config=codebuild_mixins.CfnProjectPropsMixin.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnets=["subnets"],
                    vpc_id="vpcId"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03dcb5ea218ae77f7f0a499b9b551c15ff81dab0a63c28f507fb7d04dfe6be04)
            check_type(argname="argument artifacts", value=artifacts, expected_type=type_hints["artifacts"])
            check_type(argname="argument auto_retry_limit", value=auto_retry_limit, expected_type=type_hints["auto_retry_limit"])
            check_type(argname="argument badge_enabled", value=badge_enabled, expected_type=type_hints["badge_enabled"])
            check_type(argname="argument build_batch_config", value=build_batch_config, expected_type=type_hints["build_batch_config"])
            check_type(argname="argument cache", value=cache, expected_type=type_hints["cache"])
            check_type(argname="argument concurrent_build_limit", value=concurrent_build_limit, expected_type=type_hints["concurrent_build_limit"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument file_system_locations", value=file_system_locations, expected_type=type_hints["file_system_locations"])
            check_type(argname="argument logs_config", value=logs_config, expected_type=type_hints["logs_config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument queued_timeout_in_minutes", value=queued_timeout_in_minutes, expected_type=type_hints["queued_timeout_in_minutes"])
            check_type(argname="argument resource_access_role", value=resource_access_role, expected_type=type_hints["resource_access_role"])
            check_type(argname="argument secondary_artifacts", value=secondary_artifacts, expected_type=type_hints["secondary_artifacts"])
            check_type(argname="argument secondary_sources", value=secondary_sources, expected_type=type_hints["secondary_sources"])
            check_type(argname="argument secondary_source_versions", value=secondary_source_versions, expected_type=type_hints["secondary_source_versions"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument source_version", value=source_version, expected_type=type_hints["source_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout_in_minutes", value=timeout_in_minutes, expected_type=type_hints["timeout_in_minutes"])
            check_type(argname="argument triggers", value=triggers, expected_type=type_hints["triggers"])
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if artifacts is not None:
            self._values["artifacts"] = artifacts
        if auto_retry_limit is not None:
            self._values["auto_retry_limit"] = auto_retry_limit
        if badge_enabled is not None:
            self._values["badge_enabled"] = badge_enabled
        if build_batch_config is not None:
            self._values["build_batch_config"] = build_batch_config
        if cache is not None:
            self._values["cache"] = cache
        if concurrent_build_limit is not None:
            self._values["concurrent_build_limit"] = concurrent_build_limit
        if description is not None:
            self._values["description"] = description
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if environment is not None:
            self._values["environment"] = environment
        if file_system_locations is not None:
            self._values["file_system_locations"] = file_system_locations
        if logs_config is not None:
            self._values["logs_config"] = logs_config
        if name is not None:
            self._values["name"] = name
        if queued_timeout_in_minutes is not None:
            self._values["queued_timeout_in_minutes"] = queued_timeout_in_minutes
        if resource_access_role is not None:
            self._values["resource_access_role"] = resource_access_role
        if secondary_artifacts is not None:
            self._values["secondary_artifacts"] = secondary_artifacts
        if secondary_sources is not None:
            self._values["secondary_sources"] = secondary_sources
        if secondary_source_versions is not None:
            self._values["secondary_source_versions"] = secondary_source_versions
        if service_role is not None:
            self._values["service_role"] = service_role
        if source is not None:
            self._values["source"] = source
        if source_version is not None:
            self._values["source_version"] = source_version
        if tags is not None:
            self._values["tags"] = tags
        if timeout_in_minutes is not None:
            self._values["timeout_in_minutes"] = timeout_in_minutes
        if triggers is not None:
            self._values["triggers"] = triggers
        if visibility is not None:
            self._values["visibility"] = visibility
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def artifacts(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.ArtifactsProperty"]]:
        '''``Artifacts`` is a property of the `AWS::CodeBuild::Project <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html>`_ resource that specifies output settings for artifacts generated by an AWS CodeBuild build.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-artifacts
        '''
        result = self._values.get("artifacts")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.ArtifactsProperty"]], result)

    @builtins.property
    def auto_retry_limit(self) -> typing.Optional[jsii.Number]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-autoretrylimit
        '''
        result = self._values.get("auto_retry_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def badge_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge.

        For more information, see `Build Badges Sample <https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-badges.html>`_ in the *AWS CodeBuild User Guide* .
        .. epigraph::

           Including build badges with your project is currently not supported if the source type is CodePipeline. If you specify ``CODEPIPELINE`` for the ``Source`` property, do not specify the ``BadgeEnabled`` property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-badgeenabled
        '''
        result = self._values.get("badge_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def build_batch_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.ProjectBuildBatchConfigProperty"]]:
        '''A ``ProjectBuildBatchConfig`` object that defines the batch build options for the project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-buildbatchconfig
        '''
        result = self._values.get("build_batch_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.ProjectBuildBatchConfigProperty"]], result)

    @builtins.property
    def cache(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.ProjectCacheProperty"]]:
        '''Settings that AWS CodeBuild uses to store and reuse build dependencies.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-cache
        '''
        result = self._values.get("cache")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.ProjectCacheProperty"]], result)

    @builtins.property
    def concurrent_build_limit(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of concurrent builds that are allowed for this project.

        New builds are only started if the current number of builds is less than or equal to this limit. If the current build count meets this limit, new builds are throttled and are not run.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-concurrentbuildlimit
        '''
        result = self._values.get("concurrent_build_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description that makes the build project easy to identify.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[builtins.str]:
        '''The AWS Key Management Service customer master key (CMK) to be used for encrypting the build output artifacts.

        .. epigraph::

           You can use a cross-account KMS key to encrypt the build output artifacts if your service role has permission to that key.

        You can specify either the Amazon Resource Name (ARN) of the CMK or, if available, the CMK's alias (using the format ``alias/<alias-name>`` ). If you don't specify a value, CodeBuild uses the managed CMK for Amazon Simple Storage Service (Amazon S3).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-encryptionkey
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.EnvironmentProperty"]]:
        '''The build environment settings for the project, such as the environment type or the environment variables to use for the build environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-environment
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.EnvironmentProperty"]], result)

    @builtins.property
    def file_system_locations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.ProjectFileSystemLocationProperty"]]]]:
        '''An array of ``ProjectFileSystemLocation`` objects for a CodeBuild build project.

        A ``ProjectFileSystemLocation`` object specifies the ``identifier`` , ``location`` , ``mountOptions`` , ``mountPoint`` , and ``type`` of a file system created using Amazon Elastic File System.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-filesystemlocations
        '''
        result = self._values.get("file_system_locations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.ProjectFileSystemLocationProperty"]]]], result)

    @builtins.property
    def logs_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.LogsConfigProperty"]]:
        '''Information about logs for the build project.

        A project can create logs in CloudWatch Logs, an S3 bucket, or both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-logsconfig
        '''
        result = self._values.get("logs_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.LogsConfigProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the build project.

        The name must be unique across all of the projects in your AWS account .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def queued_timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''The number of minutes a build is allowed to be queued before it times out.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-queuedtimeoutinminutes
        '''
        result = self._values.get("queued_timeout_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_access_role(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role that enables CodeBuild to access the CloudWatch Logs and Amazon S3 artifacts for the project's builds.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-resourceaccessrole
        '''
        result = self._values.get("resource_access_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_artifacts(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.ArtifactsProperty"]]]]:
        '''A list of ``Artifacts`` objects.

        Each artifacts object specifies output settings that the project generates during a build.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondaryartifacts
        '''
        result = self._values.get("secondary_artifacts")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.ArtifactsProperty"]]]], result)

    @builtins.property
    def secondary_sources(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.SourceProperty"]]]]:
        '''An array of ``ProjectSource`` objects.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondarysources
        '''
        result = self._values.get("secondary_sources")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.SourceProperty"]]]], result)

    @builtins.property
    def secondary_source_versions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.ProjectSourceVersionProperty"]]]]:
        '''An array of ``ProjectSourceVersion`` objects.

        If ``secondarySourceVersions`` is specified at the build level, then they take over these ``secondarySourceVersions`` (at the project level).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondarysourceversions
        '''
        result = self._values.get("secondary_source_versions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.ProjectSourceVersionProperty"]]]], result)

    @builtins.property
    def service_role(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role that enables AWS CodeBuild to interact with dependent AWS services on behalf of the AWS account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-servicerole
        '''
        result = self._values.get("service_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.SourceProperty"]]:
        '''The source code settings for the project, such as the source code's repository type and location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-source
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.SourceProperty"]], result)

    @builtins.property
    def source_version(self) -> typing.Optional[builtins.str]:
        '''A version of the build input to be built for this project.

        If not specified, the latest version is used. If specified, it must be one of:

        - For CodeCommit: the commit ID, branch, or Git tag to use.
        - For GitHub: the commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build. If a pull request ID is specified, it must use the format ``pr/pull-request-ID`` (for example ``pr/25`` ). If a branch name is specified, the branch's HEAD commit ID is used. If not specified, the default branch's HEAD commit ID is used.
        - For GitLab: the commit ID, branch, or Git tag to use.
        - For Bitbucket: the commit ID, branch name, or tag name that corresponds to the version of the source code you want to build. If a branch name is specified, the branch's HEAD commit ID is used. If not specified, the default branch's HEAD commit ID is used.
        - For Amazon S3: the version ID of the object that represents the build input ZIP file to use.

        If ``sourceVersion`` is specified at the build level, then that version takes precedence over this ``sourceVersion`` (at the project level).

        For more information, see `Source Version Sample with CodeBuild <https://docs.aws.amazon.com/codebuild/latest/userguide/sample-source-version.html>`_ in the *AWS CodeBuild User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-sourceversion
        '''
        result = self._values.get("source_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An arbitrary set of tags (key-value pairs) for the AWS CodeBuild project.

        These tags are available for use by AWS services that support AWS CodeBuild build project tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''How long, in minutes, from 5 to 2160 (36 hours), for AWS CodeBuild to wait before timing out any related build that did not get marked as completed.

        The default is 60 minutes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-timeoutinminutes
        '''
        result = self._values.get("timeout_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def triggers(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.ProjectTriggersProperty"]]:
        '''For an existing AWS CodeBuild build project that has its source code stored in a GitHub repository, enables AWS CodeBuild to begin automatically rebuilding the source code every time a code change is pushed to the repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-triggers
        '''
        result = self._values.get("triggers")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.ProjectTriggersProperty"]], result)

    @builtins.property
    def visibility(self) -> typing.Optional[builtins.str]:
        '''Specifies the visibility of the project's builds. Possible values are:.

        - **PUBLIC_READ** - The project builds are visible to the public.
        - **PRIVATE** - The project builds are not visible to the public.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-visibility
        '''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.VpcConfigProperty"]]:
        '''``VpcConfig`` specifies settings that enable AWS CodeBuild to access resources in an Amazon VPC.

        For more information, see `Use AWS CodeBuild with Amazon Virtual Private Cloud <https://docs.aws.amazon.com/codebuild/latest/userguide/vpc-support.html>`_ in the *AWS CodeBuild User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-vpcconfig
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.VpcConfigProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProjectMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnProjectPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin",
):
    '''The ``AWS::CodeBuild::Project`` resource configures how AWS CodeBuild builds your source code.

    For example, it tells CodeBuild where to get the source code and which build environment to use.
    .. epigraph::

       To unset or remove a project value via CFN, explicitly provide the attribute with value as empty input.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html
    :cloudformationResource: AWS::CodeBuild::Project
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
        
        cfn_project_props_mixin = codebuild_mixins.CfnProjectPropsMixin(codebuild_mixins.CfnProjectMixinProps(
            artifacts=codebuild_mixins.CfnProjectPropsMixin.ArtifactsProperty(
                artifact_identifier="artifactIdentifier",
                encryption_disabled=False,
                location="location",
                name="name",
                namespace_type="namespaceType",
                override_artifact_name=False,
                packaging="packaging",
                path="path",
                type="type"
            ),
            auto_retry_limit=123,
            badge_enabled=False,
            build_batch_config=codebuild_mixins.CfnProjectPropsMixin.ProjectBuildBatchConfigProperty(
                batch_report_mode="batchReportMode",
                combine_artifacts=False,
                restrictions=codebuild_mixins.CfnProjectPropsMixin.BatchRestrictionsProperty(
                    compute_types_allowed=["computeTypesAllowed"],
                    maximum_builds_allowed=123
                ),
                service_role="serviceRole",
                timeout_in_mins=123
            ),
            cache=codebuild_mixins.CfnProjectPropsMixin.ProjectCacheProperty(
                cache_namespace="cacheNamespace",
                location="location",
                modes=["modes"],
                type="type"
            ),
            concurrent_build_limit=123,
            description="description",
            encryption_key="encryptionKey",
            environment=codebuild_mixins.CfnProjectPropsMixin.EnvironmentProperty(
                certificate="certificate",
                compute_type="computeType",
                docker_server=codebuild_mixins.CfnProjectPropsMixin.DockerServerProperty(
                    compute_type="computeType",
                    security_group_ids=["securityGroupIds"]
                ),
                environment_variables=[codebuild_mixins.CfnProjectPropsMixin.EnvironmentVariableProperty(
                    name="name",
                    type="type",
                    value="value"
                )],
                fleet=codebuild_mixins.CfnProjectPropsMixin.ProjectFleetProperty(
                    fleet_arn="fleetArn"
                ),
                image="image",
                image_pull_credentials_type="imagePullCredentialsType",
                privileged_mode=False,
                registry_credential=codebuild_mixins.CfnProjectPropsMixin.RegistryCredentialProperty(
                    credential="credential",
                    credential_provider="credentialProvider"
                ),
                type="type"
            ),
            file_system_locations=[codebuild_mixins.CfnProjectPropsMixin.ProjectFileSystemLocationProperty(
                identifier="identifier",
                location="location",
                mount_options="mountOptions",
                mount_point="mountPoint",
                type="type"
            )],
            logs_config=codebuild_mixins.CfnProjectPropsMixin.LogsConfigProperty(
                cloud_watch_logs=codebuild_mixins.CfnProjectPropsMixin.CloudWatchLogsConfigProperty(
                    group_name="groupName",
                    status="status",
                    stream_name="streamName"
                ),
                s3_logs=codebuild_mixins.CfnProjectPropsMixin.S3LogsConfigProperty(
                    encryption_disabled=False,
                    location="location",
                    status="status"
                )
            ),
            name="name",
            queued_timeout_in_minutes=123,
            resource_access_role="resourceAccessRole",
            secondary_artifacts=[codebuild_mixins.CfnProjectPropsMixin.ArtifactsProperty(
                artifact_identifier="artifactIdentifier",
                encryption_disabled=False,
                location="location",
                name="name",
                namespace_type="namespaceType",
                override_artifact_name=False,
                packaging="packaging",
                path="path",
                type="type"
            )],
            secondary_sources=[codebuild_mixins.CfnProjectPropsMixin.SourceProperty(
                auth=codebuild_mixins.CfnProjectPropsMixin.SourceAuthProperty(
                    resource="resource",
                    type="type"
                ),
                build_spec="buildSpec",
                build_status_config=codebuild_mixins.CfnProjectPropsMixin.BuildStatusConfigProperty(
                    context="context",
                    target_url="targetUrl"
                ),
                git_clone_depth=123,
                git_submodules_config=codebuild_mixins.CfnProjectPropsMixin.GitSubmodulesConfigProperty(
                    fetch_submodules=False
                ),
                insecure_ssl=False,
                location="location",
                report_build_status=False,
                source_identifier="sourceIdentifier",
                type="type"
            )],
            secondary_source_versions=[codebuild_mixins.CfnProjectPropsMixin.ProjectSourceVersionProperty(
                source_identifier="sourceIdentifier",
                source_version="sourceVersion"
            )],
            service_role="serviceRole",
            source=codebuild_mixins.CfnProjectPropsMixin.SourceProperty(
                auth=codebuild_mixins.CfnProjectPropsMixin.SourceAuthProperty(
                    resource="resource",
                    type="type"
                ),
                build_spec="buildSpec",
                build_status_config=codebuild_mixins.CfnProjectPropsMixin.BuildStatusConfigProperty(
                    context="context",
                    target_url="targetUrl"
                ),
                git_clone_depth=123,
                git_submodules_config=codebuild_mixins.CfnProjectPropsMixin.GitSubmodulesConfigProperty(
                    fetch_submodules=False
                ),
                insecure_ssl=False,
                location="location",
                report_build_status=False,
                source_identifier="sourceIdentifier",
                type="type"
            ),
            source_version="sourceVersion",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            timeout_in_minutes=123,
            triggers=codebuild_mixins.CfnProjectPropsMixin.ProjectTriggersProperty(
                build_type="buildType",
                filter_groups=[[codebuild_mixins.CfnProjectPropsMixin.WebhookFilterProperty(
                    exclude_matched_pattern=False,
                    pattern="pattern",
                    type="type"
                )]],
                pull_request_build_policy=codebuild_mixins.CfnProjectPropsMixin.PullRequestBuildPolicyProperty(
                    approver_roles=["approverRoles"],
                    requires_comment_approval="requiresCommentApproval"
                ),
                scope_configuration=codebuild_mixins.CfnProjectPropsMixin.ScopeConfigurationProperty(
                    domain="domain",
                    name="name",
                    scope="scope"
                ),
                webhook=False
            ),
            visibility="visibility",
            vpc_config=codebuild_mixins.CfnProjectPropsMixin.VpcConfigProperty(
                security_group_ids=["securityGroupIds"],
                subnets=["subnets"],
                vpc_id="vpcId"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnProjectMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CodeBuild::Project``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e820c4fb87defc15f1f7369a60d940aa0fc3198cfa29f64cdc7de5970d49aa03)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47a2e7bf795968abbaf9854d277d64c7af1ea3c08e9aa6a134af6129dc1acae2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__735c5733d23b5f48be52c275e4628ede948c6c00a05fb658e9b02ef875176f16)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnProjectMixinProps:
        return typing.cast(CfnProjectMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.ArtifactsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "artifact_identifier": "artifactIdentifier",
            "encryption_disabled": "encryptionDisabled",
            "location": "location",
            "name": "name",
            "namespace_type": "namespaceType",
            "override_artifact_name": "overrideArtifactName",
            "packaging": "packaging",
            "path": "path",
            "type": "type",
        },
    )
    class ArtifactsProperty:
        def __init__(
            self,
            *,
            artifact_identifier: typing.Optional[builtins.str] = None,
            encryption_disabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            location: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            namespace_type: typing.Optional[builtins.str] = None,
            override_artifact_name: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            packaging: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``Artifacts`` is a property of the `AWS::CodeBuild::Project <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html>`_ resource that specifies output settings for artifacts generated by an AWS CodeBuild build.

            :param artifact_identifier: An identifier for this artifact definition.
            :param encryption_disabled: Set to true if you do not want your output artifacts encrypted. This option is valid only if your artifacts type is Amazon Simple Storage Service (Amazon S3). If this is set with another artifacts type, an ``invalidInputException`` is thrown.
            :param location: Information about the build output artifact location:. - If ``type`` is set to ``CODEPIPELINE`` , AWS CodePipeline ignores this value if specified. This is because CodePipeline manages its build output locations instead of CodeBuild . - If ``type`` is set to ``NO_ARTIFACTS`` , this value is ignored if specified, because no build output is produced. - If ``type`` is set to ``S3`` , this is the name of the output bucket. If you specify ``CODEPIPELINE`` or ``NO_ARTIFACTS`` for the ``Type`` property, don't specify this property. For all of the other types, you must specify this property.
            :param name: Along with ``path`` and ``namespaceType`` , the pattern that AWS CodeBuild uses to name and store the output artifact:. - If ``type`` is set to ``CODEPIPELINE`` , AWS CodePipeline ignores this value if specified. This is because CodePipeline manages its build output names instead of AWS CodeBuild . - If ``type`` is set to ``NO_ARTIFACTS`` , this value is ignored if specified, because no build output is produced. - If ``type`` is set to ``S3`` , this is the name of the output artifact object. If you set the name to be a forward slash ("/"), the artifact is stored in the root of the output bucket. For example: - If ``path`` is set to ``MyArtifacts`` , ``namespaceType`` is set to ``BUILD_ID`` , and ``name`` is set to ``MyArtifact.zip`` , then the output artifact is stored in ``MyArtifacts/ *build-ID* /MyArtifact.zip`` . - If ``path`` is empty, ``namespaceType`` is set to ``NONE`` , and ``name`` is set to " ``/`` ", the output artifact is stored in the root of the output bucket. - If ``path`` is set to ``MyArtifacts`` , ``namespaceType`` is set to ``BUILD_ID`` , and ``name`` is set to " ``/`` ", the output artifact is stored in ``MyArtifacts/ *build-ID*`` . If you specify ``CODEPIPELINE`` or ``NO_ARTIFACTS`` for the ``Type`` property, don't specify this property. For all of the other types, you must specify this property.
            :param namespace_type: Along with ``path`` and ``name`` , the pattern that AWS CodeBuild uses to determine the name and location to store the output artifact: - If ``type`` is set to ``CODEPIPELINE`` , CodePipeline ignores this value if specified. This is because CodePipeline manages its build output names instead of AWS CodeBuild . - If ``type`` is set to ``NO_ARTIFACTS`` , this value is ignored if specified, because no build output is produced. - If ``type`` is set to ``S3`` , valid values include: - ``BUILD_ID`` : Include the build ID in the location of the build output artifact. - ``NONE`` : Do not include the build ID. This is the default if ``namespaceType`` is not specified. For example, if ``path`` is set to ``MyArtifacts`` , ``namespaceType`` is set to ``BUILD_ID`` , and ``name`` is set to ``MyArtifact.zip`` , the output artifact is stored in ``MyArtifacts/<build-ID>/MyArtifact.zip`` .
            :param override_artifact_name: If set to true a name specified in the buildspec file overrides the artifact name. The name specified in a buildspec file is calculated at build time and uses the Shell command language. For example, you can append a date and time to your artifact name so that it is always unique.
            :param packaging: The type of build output artifact to create:. - If ``type`` is set to ``CODEPIPELINE`` , CodePipeline ignores this value if specified. This is because CodePipeline manages its build output artifacts instead of AWS CodeBuild . - If ``type`` is set to ``NO_ARTIFACTS`` , this value is ignored if specified, because no build output is produced. - If ``type`` is set to ``S3`` , valid values include: - ``NONE`` : AWS CodeBuild creates in the output bucket a folder that contains the build output. This is the default if ``packaging`` is not specified. - ``ZIP`` : AWS CodeBuild creates in the output bucket a ZIP file that contains the build output.
            :param path: Along with ``namespaceType`` and ``name`` , the pattern that AWS CodeBuild uses to name and store the output artifact:. - If ``type`` is set to ``CODEPIPELINE`` , CodePipeline ignores this value if specified. This is because CodePipeline manages its build output names instead of AWS CodeBuild . - If ``type`` is set to ``NO_ARTIFACTS`` , this value is ignored if specified, because no build output is produced. - If ``type`` is set to ``S3`` , this is the path to the output artifact. If ``path`` is not specified, ``path`` is not used. For example, if ``path`` is set to ``MyArtifacts`` , ``namespaceType`` is set to ``NONE`` , and ``name`` is set to ``MyArtifact.zip`` , the output artifact is stored in the output bucket at ``MyArtifacts/MyArtifact.zip`` .
            :param type: The type of build output artifact. Valid values include:. - ``CODEPIPELINE`` : The build project has build output generated through CodePipeline. .. epigraph:: The ``CODEPIPELINE`` type is not supported for ``secondaryArtifacts`` . - ``NO_ARTIFACTS`` : The build project does not produce any build output. - ``S3`` : The build project stores build output in Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                artifacts_property = codebuild_mixins.CfnProjectPropsMixin.ArtifactsProperty(
                    artifact_identifier="artifactIdentifier",
                    encryption_disabled=False,
                    location="location",
                    name="name",
                    namespace_type="namespaceType",
                    override_artifact_name=False,
                    packaging="packaging",
                    path="path",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a135ac3b59f3895642ca7505b1aed677a00babe61adbc6e58dea0d55f3837e32)
                check_type(argname="argument artifact_identifier", value=artifact_identifier, expected_type=type_hints["artifact_identifier"])
                check_type(argname="argument encryption_disabled", value=encryption_disabled, expected_type=type_hints["encryption_disabled"])
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument namespace_type", value=namespace_type, expected_type=type_hints["namespace_type"])
                check_type(argname="argument override_artifact_name", value=override_artifact_name, expected_type=type_hints["override_artifact_name"])
                check_type(argname="argument packaging", value=packaging, expected_type=type_hints["packaging"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if artifact_identifier is not None:
                self._values["artifact_identifier"] = artifact_identifier
            if encryption_disabled is not None:
                self._values["encryption_disabled"] = encryption_disabled
            if location is not None:
                self._values["location"] = location
            if name is not None:
                self._values["name"] = name
            if namespace_type is not None:
                self._values["namespace_type"] = namespace_type
            if override_artifact_name is not None:
                self._values["override_artifact_name"] = override_artifact_name
            if packaging is not None:
                self._values["packaging"] = packaging
            if path is not None:
                self._values["path"] = path
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def artifact_identifier(self) -> typing.Optional[builtins.str]:
            '''An identifier for this artifact definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-artifactidentifier
            '''
            result = self._values.get("artifact_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_disabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set to true if you do not want your output artifacts encrypted.

            This option is valid only if your artifacts type is Amazon Simple Storage Service (Amazon S3). If this is set with another artifacts type, an ``invalidInputException`` is thrown.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-encryptiondisabled
            '''
            result = self._values.get("encryption_disabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def location(self) -> typing.Optional[builtins.str]:
            '''Information about the build output artifact location:.

            - If ``type`` is set to ``CODEPIPELINE`` , AWS CodePipeline ignores this value if specified. This is because CodePipeline manages its build output locations instead of CodeBuild .
            - If ``type`` is set to ``NO_ARTIFACTS`` , this value is ignored if specified, because no build output is produced.
            - If ``type`` is set to ``S3`` , this is the name of the output bucket.

            If you specify ``CODEPIPELINE`` or ``NO_ARTIFACTS`` for the ``Type`` property, don't specify this property. For all of the other types, you must specify this property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Along with ``path`` and ``namespaceType`` , the pattern that AWS CodeBuild uses to name and store the output artifact:.

            - If ``type`` is set to ``CODEPIPELINE`` , AWS CodePipeline ignores this value if specified. This is because CodePipeline manages its build output names instead of AWS CodeBuild .
            - If ``type`` is set to ``NO_ARTIFACTS`` , this value is ignored if specified, because no build output is produced.
            - If ``type`` is set to ``S3`` , this is the name of the output artifact object. If you set the name to be a forward slash ("/"), the artifact is stored in the root of the output bucket.

            For example:

            - If ``path`` is set to ``MyArtifacts`` , ``namespaceType`` is set to ``BUILD_ID`` , and ``name`` is set to ``MyArtifact.zip`` , then the output artifact is stored in ``MyArtifacts/ *build-ID* /MyArtifact.zip`` .
            - If ``path`` is empty, ``namespaceType`` is set to ``NONE`` , and ``name`` is set to " ``/`` ", the output artifact is stored in the root of the output bucket.
            - If ``path`` is set to ``MyArtifacts`` , ``namespaceType`` is set to ``BUILD_ID`` , and ``name`` is set to " ``/`` ", the output artifact is stored in ``MyArtifacts/ *build-ID*`` .

            If you specify ``CODEPIPELINE`` or ``NO_ARTIFACTS`` for the ``Type`` property, don't specify this property. For all of the other types, you must specify this property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace_type(self) -> typing.Optional[builtins.str]:
            '''Along with ``path`` and ``name`` , the pattern that AWS CodeBuild uses to determine the name and location to store the output artifact:  - If ``type`` is set to ``CODEPIPELINE`` , CodePipeline ignores this value if specified.

            This is because CodePipeline manages its build output names instead of AWS CodeBuild .

            - If ``type`` is set to ``NO_ARTIFACTS`` , this value is ignored if specified, because no build output is produced.
            - If ``type`` is set to ``S3`` , valid values include:
            - ``BUILD_ID`` : Include the build ID in the location of the build output artifact.
            - ``NONE`` : Do not include the build ID. This is the default if ``namespaceType`` is not specified.

            For example, if ``path`` is set to ``MyArtifacts`` , ``namespaceType`` is set to ``BUILD_ID`` , and ``name`` is set to ``MyArtifact.zip`` , the output artifact is stored in ``MyArtifacts/<build-ID>/MyArtifact.zip`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-namespacetype
            '''
            result = self._values.get("namespace_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def override_artifact_name(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If set to true a name specified in the buildspec file overrides the artifact name.

            The name specified in a buildspec file is calculated at build time and uses the Shell command language. For example, you can append a date and time to your artifact name so that it is always unique.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-overrideartifactname
            '''
            result = self._values.get("override_artifact_name")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def packaging(self) -> typing.Optional[builtins.str]:
            '''The type of build output artifact to create:.

            - If ``type`` is set to ``CODEPIPELINE`` , CodePipeline ignores this value if specified. This is because CodePipeline manages its build output artifacts instead of AWS CodeBuild .
            - If ``type`` is set to ``NO_ARTIFACTS`` , this value is ignored if specified, because no build output is produced.
            - If ``type`` is set to ``S3`` , valid values include:
            - ``NONE`` : AWS CodeBuild creates in the output bucket a folder that contains the build output. This is the default if ``packaging`` is not specified.
            - ``ZIP`` : AWS CodeBuild creates in the output bucket a ZIP file that contains the build output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-packaging
            '''
            result = self._values.get("packaging")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''Along with ``namespaceType`` and ``name`` , the pattern that AWS CodeBuild uses to name and store the output artifact:.

            - If ``type`` is set to ``CODEPIPELINE`` , CodePipeline ignores this value if specified. This is because CodePipeline manages its build output names instead of AWS CodeBuild .
            - If ``type`` is set to ``NO_ARTIFACTS`` , this value is ignored if specified, because no build output is produced.
            - If ``type`` is set to ``S3`` , this is the path to the output artifact. If ``path`` is not specified, ``path`` is not used.

            For example, if ``path`` is set to ``MyArtifacts`` , ``namespaceType`` is set to ``NONE`` , and ``name`` is set to ``MyArtifact.zip`` , the output artifact is stored in the output bucket at ``MyArtifacts/MyArtifact.zip`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of build output artifact. Valid values include:.

            - ``CODEPIPELINE`` : The build project has build output generated through CodePipeline.

            .. epigraph::

               The ``CODEPIPELINE`` type is not supported for ``secondaryArtifacts`` .

            - ``NO_ARTIFACTS`` : The build project does not produce any build output.
            - ``S3`` : The build project stores build output in Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArtifactsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.BatchRestrictionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "compute_types_allowed": "computeTypesAllowed",
            "maximum_builds_allowed": "maximumBuildsAllowed",
        },
    )
    class BatchRestrictionsProperty:
        def __init__(
            self,
            *,
            compute_types_allowed: typing.Optional[typing.Sequence[builtins.str]] = None,
            maximum_builds_allowed: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies restrictions for the batch build.

            :param compute_types_allowed: An array of strings that specify the compute types that are allowed for the batch build. See `Build environment compute types <https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-compute-types.html>`_ in the *AWS CodeBuild User Guide* for these values.
            :param maximum_builds_allowed: Specifies the maximum number of builds allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-batchrestrictions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                batch_restrictions_property = codebuild_mixins.CfnProjectPropsMixin.BatchRestrictionsProperty(
                    compute_types_allowed=["computeTypesAllowed"],
                    maximum_builds_allowed=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0b0dff32ec4b3300b2453ab7d0a0b6f1acdf28514b93708adc9006268a106fe7)
                check_type(argname="argument compute_types_allowed", value=compute_types_allowed, expected_type=type_hints["compute_types_allowed"])
                check_type(argname="argument maximum_builds_allowed", value=maximum_builds_allowed, expected_type=type_hints["maximum_builds_allowed"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if compute_types_allowed is not None:
                self._values["compute_types_allowed"] = compute_types_allowed
            if maximum_builds_allowed is not None:
                self._values["maximum_builds_allowed"] = maximum_builds_allowed

        @builtins.property
        def compute_types_allowed(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of strings that specify the compute types that are allowed for the batch build.

            See `Build environment compute types <https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-compute-types.html>`_ in the *AWS CodeBuild User Guide* for these values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-batchrestrictions.html#cfn-codebuild-project-batchrestrictions-computetypesallowed
            '''
            result = self._values.get("compute_types_allowed")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def maximum_builds_allowed(self) -> typing.Optional[jsii.Number]:
            '''Specifies the maximum number of builds allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-batchrestrictions.html#cfn-codebuild-project-batchrestrictions-maximumbuildsallowed
            '''
            result = self._values.get("maximum_builds_allowed")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BatchRestrictionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.BuildStatusConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"context": "context", "target_url": "targetUrl"},
    )
    class BuildStatusConfigProperty:
        def __init__(
            self,
            *,
            context: typing.Optional[builtins.str] = None,
            target_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information that defines how the AWS CodeBuild build project reports the build status to the source provider.

            :param context: Specifies the context of the build status CodeBuild sends to the source provider. The usage of this parameter depends on the source provider. - **Bitbucket** - This parameter is used for the ``name`` parameter in the Bitbucket commit status. For more information, see `build <https://docs.aws.amazon.com/https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/commit/%7Bnode%7D/statuses/build>`_ in the Bitbucket API documentation. - **GitHub/GitHub Enterprise Server** - This parameter is used for the ``context`` parameter in the GitHub commit status. For more information, see `Create a commit status <https://docs.aws.amazon.com/https://developer.github.com/v3/repos/statuses/#create-a-commit-status>`_ in the GitHub developer guide.
            :param target_url: Specifies the target url of the build status CodeBuild sends to the source provider. The usage of this parameter depends on the source provider. - **Bitbucket** - This parameter is used for the ``url`` parameter in the Bitbucket commit status. For more information, see `build <https://docs.aws.amazon.com/https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/commit/%7Bnode%7D/statuses/build>`_ in the Bitbucket API documentation. - **GitHub/GitHub Enterprise Server** - This parameter is used for the ``target_url`` parameter in the GitHub commit status. For more information, see `Create a commit status <https://docs.aws.amazon.com/https://developer.github.com/v3/repos/statuses/#create-a-commit-status>`_ in the GitHub developer guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-buildstatusconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                build_status_config_property = codebuild_mixins.CfnProjectPropsMixin.BuildStatusConfigProperty(
                    context="context",
                    target_url="targetUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c8a98f56da1090ea1e89b6e2a7fb26d0e5de501644a344fbf365fb81c8debe90)
                check_type(argname="argument context", value=context, expected_type=type_hints["context"])
                check_type(argname="argument target_url", value=target_url, expected_type=type_hints["target_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if context is not None:
                self._values["context"] = context
            if target_url is not None:
                self._values["target_url"] = target_url

        @builtins.property
        def context(self) -> typing.Optional[builtins.str]:
            '''Specifies the context of the build status CodeBuild sends to the source provider.

            The usage of this parameter depends on the source provider.

            - **Bitbucket** - This parameter is used for the ``name`` parameter in the Bitbucket commit status. For more information, see `build <https://docs.aws.amazon.com/https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/commit/%7Bnode%7D/statuses/build>`_ in the Bitbucket API documentation.
            - **GitHub/GitHub Enterprise Server** - This parameter is used for the ``context`` parameter in the GitHub commit status. For more information, see `Create a commit status <https://docs.aws.amazon.com/https://developer.github.com/v3/repos/statuses/#create-a-commit-status>`_ in the GitHub developer guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-buildstatusconfig.html#cfn-codebuild-project-buildstatusconfig-context
            '''
            result = self._values.get("context")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_url(self) -> typing.Optional[builtins.str]:
            '''Specifies the target url of the build status CodeBuild sends to the source provider.

            The usage of this parameter depends on the source provider.

            - **Bitbucket** - This parameter is used for the ``url`` parameter in the Bitbucket commit status. For more information, see `build <https://docs.aws.amazon.com/https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/commit/%7Bnode%7D/statuses/build>`_ in the Bitbucket API documentation.
            - **GitHub/GitHub Enterprise Server** - This parameter is used for the ``target_url`` parameter in the GitHub commit status. For more information, see `Create a commit status <https://docs.aws.amazon.com/https://developer.github.com/v3/repos/statuses/#create-a-commit-status>`_ in the GitHub developer guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-buildstatusconfig.html#cfn-codebuild-project-buildstatusconfig-targeturl
            '''
            result = self._values.get("target_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BuildStatusConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.CloudWatchLogsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "group_name": "groupName",
            "status": "status",
            "stream_name": "streamName",
        },
    )
    class CloudWatchLogsConfigProperty:
        def __init__(
            self,
            *,
            group_name: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
            stream_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``CloudWatchLogs`` is a property of the `AWS CodeBuild Project LogsConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-logsconfig.html>`_ property type that specifies settings for CloudWatch logs generated by an AWS CodeBuild build.

            :param group_name: The group name of the logs in CloudWatch Logs. For more information, see `Working with Log Groups and Log Streams <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html>`_ .
            :param status: The current status of the logs in CloudWatch Logs for a build project. Valid values are:. - ``ENABLED`` : CloudWatch Logs are enabled for this build project. - ``DISABLED`` : CloudWatch Logs are not enabled for this build project.
            :param stream_name: The prefix of the stream name of the CloudWatch Logs. For more information, see `Working with Log Groups and Log Streams <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-cloudwatchlogsconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                cloud_watch_logs_config_property = codebuild_mixins.CfnProjectPropsMixin.CloudWatchLogsConfigProperty(
                    group_name="groupName",
                    status="status",
                    stream_name="streamName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__abd4bb2c4f79828358477c1c05f129f9d97a4b42e85af0c1e3bf5b7a1f2e1b4f)
                check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_name is not None:
                self._values["group_name"] = group_name
            if status is not None:
                self._values["status"] = status
            if stream_name is not None:
                self._values["stream_name"] = stream_name

        @builtins.property
        def group_name(self) -> typing.Optional[builtins.str]:
            '''The group name of the logs in CloudWatch Logs.

            For more information, see `Working with Log Groups and Log Streams <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-cloudwatchlogsconfig.html#cfn-codebuild-project-cloudwatchlogsconfig-groupname
            '''
            result = self._values.get("group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The current status of the logs in CloudWatch Logs for a build project. Valid values are:.

            - ``ENABLED`` : CloudWatch Logs are enabled for this build project.
            - ``DISABLED`` : CloudWatch Logs are not enabled for this build project.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-cloudwatchlogsconfig.html#cfn-codebuild-project-cloudwatchlogsconfig-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stream_name(self) -> typing.Optional[builtins.str]:
            '''The prefix of the stream name of the CloudWatch Logs.

            For more information, see `Working with Log Groups and Log Streams <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-cloudwatchlogsconfig.html#cfn-codebuild-project-cloudwatchlogsconfig-streamname
            '''
            result = self._values.get("stream_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.DockerServerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "compute_type": "computeType",
            "security_group_ids": "securityGroupIds",
        },
    )
    class DockerServerProperty:
        def __init__(
            self,
            *,
            compute_type: typing.Optional[builtins.str] = None,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param compute_type: 
            :param security_group_ids: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-dockerserver.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                docker_server_property = codebuild_mixins.CfnProjectPropsMixin.DockerServerProperty(
                    compute_type="computeType",
                    security_group_ids=["securityGroupIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__535488f59b2f039eb8b90a0bca679bb769a6faab1c65ef3fbd5d1013c992c2e5)
                check_type(argname="argument compute_type", value=compute_type, expected_type=type_hints["compute_type"])
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if compute_type is not None:
                self._values["compute_type"] = compute_type
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids

        @builtins.property
        def compute_type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-dockerserver.html#cfn-codebuild-project-dockerserver-computetype
            '''
            result = self._values.get("compute_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-dockerserver.html#cfn-codebuild-project-dockerserver-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DockerServerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.EnvironmentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate": "certificate",
            "compute_type": "computeType",
            "docker_server": "dockerServer",
            "environment_variables": "environmentVariables",
            "fleet": "fleet",
            "image": "image",
            "image_pull_credentials_type": "imagePullCredentialsType",
            "privileged_mode": "privilegedMode",
            "registry_credential": "registryCredential",
            "type": "type",
        },
    )
    class EnvironmentProperty:
        def __init__(
            self,
            *,
            certificate: typing.Optional[builtins.str] = None,
            compute_type: typing.Optional[builtins.str] = None,
            docker_server: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.DockerServerProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            environment_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.EnvironmentVariableProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            fleet: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.ProjectFleetProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            image: typing.Optional[builtins.str] = None,
            image_pull_credentials_type: typing.Optional[builtins.str] = None,
            privileged_mode: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            registry_credential: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.RegistryCredentialProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``Environment`` is a property of the `AWS::CodeBuild::Project <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html>`_ resource that specifies the environment for an AWS CodeBuild project.

            :param certificate: The ARN of the Amazon S3 bucket, path prefix, and object key that contains the PEM-encoded certificate for the build project. For more information, see `certificate <https://docs.aws.amazon.com/codebuild/latest/userguide/create-project-cli.html#cli.environment.certificate>`_ in the *AWS CodeBuild User Guide* .
            :param compute_type: The type of compute environment. This determines the number of CPU cores and memory the build environment uses. Available values include: - ``ATTRIBUTE_BASED_COMPUTE`` : Specify the amount of vCPUs, memory, disk space, and the type of machine. .. epigraph:: If you use ``ATTRIBUTE_BASED_COMPUTE`` , you must define your attributes by using ``computeConfiguration`` . AWS CodeBuild will select the cheapest instance that satisfies your specified attributes. For more information, see `Reserved capacity environment types <https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-compute-types.html#environment-reserved-capacity.types>`_ in the *AWS CodeBuild User Guide* . - ``BUILD_GENERAL1_SMALL`` : Use up to 4 GiB memory and 2 vCPUs for builds. - ``BUILD_GENERAL1_MEDIUM`` : Use up to 8 GiB memory and 4 vCPUs for builds. - ``BUILD_GENERAL1_LARGE`` : Use up to 16 GiB memory and 8 vCPUs for builds, depending on your environment type. - ``BUILD_GENERAL1_XLARGE`` : Use up to 72 GiB memory and 36 vCPUs for builds, depending on your environment type. - ``BUILD_GENERAL1_2XLARGE`` : Use up to 144 GiB memory, 72 vCPUs, and 824 GB of SSD storage for builds. This compute type supports Docker images up to 100 GB uncompressed. - ``BUILD_LAMBDA_1GB`` : Use up to 1 GiB memory for builds. Only available for environment type ``LINUX_LAMBDA_CONTAINER`` and ``ARM_LAMBDA_CONTAINER`` . - ``BUILD_LAMBDA_2GB`` : Use up to 2 GiB memory for builds. Only available for environment type ``LINUX_LAMBDA_CONTAINER`` and ``ARM_LAMBDA_CONTAINER`` . - ``BUILD_LAMBDA_4GB`` : Use up to 4 GiB memory for builds. Only available for environment type ``LINUX_LAMBDA_CONTAINER`` and ``ARM_LAMBDA_CONTAINER`` . - ``BUILD_LAMBDA_8GB`` : Use up to 8 GiB memory for builds. Only available for environment type ``LINUX_LAMBDA_CONTAINER`` and ``ARM_LAMBDA_CONTAINER`` . - ``BUILD_LAMBDA_10GB`` : Use up to 10 GiB memory for builds. Only available for environment type ``LINUX_LAMBDA_CONTAINER`` and ``ARM_LAMBDA_CONTAINER`` . If you use ``BUILD_GENERAL1_SMALL`` : - For environment type ``LINUX_CONTAINER`` , you can use up to 4 GiB memory and 2 vCPUs for builds. - For environment type ``LINUX_GPU_CONTAINER`` , you can use up to 16 GiB memory, 4 vCPUs, and 1 NVIDIA A10G Tensor Core GPU for builds. - For environment type ``ARM_CONTAINER`` , you can use up to 4 GiB memory and 2 vCPUs on ARM-based processors for builds. If you use ``BUILD_GENERAL1_LARGE`` : - For environment type ``LINUX_CONTAINER`` , you can use up to 16 GiB memory and 8 vCPUs for builds. - For environment type ``LINUX_GPU_CONTAINER`` , you can use up to 255 GiB memory, 32 vCPUs, and 4 NVIDIA Tesla V100 GPUs for builds. - For environment type ``ARM_CONTAINER`` , you can use up to 16 GiB memory and 8 vCPUs on ARM-based processors for builds. For more information, see `On-demand environment types <https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-compute-types.html#environment.types>`_ in the *AWS CodeBuild User Guide.*
            :param docker_server: 
            :param environment_variables: A set of environment variables to make available to builds for this build project.
            :param fleet: 
            :param image: The image tag or image digest that identifies the Docker image to use for this build project. Use the following formats: - For an image tag: ``<registry>/<repository>:<tag>`` . For example, in the Docker repository that CodeBuild uses to manage its Docker images, this would be ``aws/codebuild/standard:4.0`` . - For an image digest: ``<registry>/<repository>@<digest>`` . For example, to specify an image with the digest "sha256:cbbf2f9a99b47fc460d422812b6a5adff7dfee951d8fa2e4a98caa0382cfbdbf," use ``<registry>/<repository>@sha256:cbbf2f9a99b47fc460d422812b6a5adff7dfee951d8fa2e4a98caa0382cfbdbf`` . For more information, see `Docker images provided by CodeBuild <https://docs.aws.amazon.com//codebuild/latest/userguide/build-env-ref-available.html>`_ in the *AWS CodeBuild user guide* .
            :param image_pull_credentials_type: The type of credentials AWS CodeBuild uses to pull images in your build. There are two valid values:. - ``CODEBUILD`` specifies that AWS CodeBuild uses its own credentials. This requires that you modify your ECR repository policy to trust AWS CodeBuild service principal. - ``SERVICE_ROLE`` specifies that AWS CodeBuild uses your build project's service role. When you use a cross-account or private registry image, you must use SERVICE_ROLE credentials. When you use an AWS CodeBuild curated image, you must use CODEBUILD credentials.
            :param privileged_mode: Enables running the Docker daemon inside a Docker container. Set to true only if the build project is used to build Docker images. Otherwise, a build that attempts to interact with the Docker daemon fails. The default setting is ``false`` . You can initialize the Docker daemon during the install phase of your build by adding one of the following sets of commands to the install phase of your buildspec file: If the operating system's base image is Ubuntu Linux: ``- nohup /usr/local/bin/dockerd --host=unix:///var/run/docker.sock --host=tcp://0.0.0.0:2375 --storage-driver=overlay&`` ``- timeout 15 sh -c "until docker info; do echo .; sleep 1; done"`` If the operating system's base image is Alpine Linux and the previous command does not work, add the ``-t`` argument to ``timeout`` : ``- nohup /usr/local/bin/dockerd --host=unix:///var/run/docker.sock --host=tcp://0.0.0.0:2375 --storage-driver=overlay&`` ``- timeout -t 15 sh -c "until docker info; do echo .; sleep 1; done"``
            :param registry_credential: ``RegistryCredential`` is a property of the `AWS::CodeBuild::Project Environment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-environment>`_ property that specifies information about credentials that provide access to a private Docker registry. When this is set:. - ``imagePullCredentialsType`` must be set to ``SERVICE_ROLE`` . - images cannot be curated or an Amazon ECR image.
            :param type: The type of build environment to use for related builds. .. epigraph:: If you're using compute fleets during project creation, ``type`` will be ignored. For more information, see `Build environment compute types <https://docs.aws.amazon.com//codebuild/latest/userguide/build-env-ref-compute-types.html>`_ in the *AWS CodeBuild user guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                environment_property = codebuild_mixins.CfnProjectPropsMixin.EnvironmentProperty(
                    certificate="certificate",
                    compute_type="computeType",
                    docker_server=codebuild_mixins.CfnProjectPropsMixin.DockerServerProperty(
                        compute_type="computeType",
                        security_group_ids=["securityGroupIds"]
                    ),
                    environment_variables=[codebuild_mixins.CfnProjectPropsMixin.EnvironmentVariableProperty(
                        name="name",
                        type="type",
                        value="value"
                    )],
                    fleet=codebuild_mixins.CfnProjectPropsMixin.ProjectFleetProperty(
                        fleet_arn="fleetArn"
                    ),
                    image="image",
                    image_pull_credentials_type="imagePullCredentialsType",
                    privileged_mode=False,
                    registry_credential=codebuild_mixins.CfnProjectPropsMixin.RegistryCredentialProperty(
                        credential="credential",
                        credential_provider="credentialProvider"
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4bab9cd2b7c7243228a80d9f1258671a08a6841c0ddc864cf30b42c835cd9c93)
                check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
                check_type(argname="argument compute_type", value=compute_type, expected_type=type_hints["compute_type"])
                check_type(argname="argument docker_server", value=docker_server, expected_type=type_hints["docker_server"])
                check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
                check_type(argname="argument fleet", value=fleet, expected_type=type_hints["fleet"])
                check_type(argname="argument image", value=image, expected_type=type_hints["image"])
                check_type(argname="argument image_pull_credentials_type", value=image_pull_credentials_type, expected_type=type_hints["image_pull_credentials_type"])
                check_type(argname="argument privileged_mode", value=privileged_mode, expected_type=type_hints["privileged_mode"])
                check_type(argname="argument registry_credential", value=registry_credential, expected_type=type_hints["registry_credential"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate is not None:
                self._values["certificate"] = certificate
            if compute_type is not None:
                self._values["compute_type"] = compute_type
            if docker_server is not None:
                self._values["docker_server"] = docker_server
            if environment_variables is not None:
                self._values["environment_variables"] = environment_variables
            if fleet is not None:
                self._values["fleet"] = fleet
            if image is not None:
                self._values["image"] = image
            if image_pull_credentials_type is not None:
                self._values["image_pull_credentials_type"] = image_pull_credentials_type
            if privileged_mode is not None:
                self._values["privileged_mode"] = privileged_mode
            if registry_credential is not None:
                self._values["registry_credential"] = registry_credential
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def certificate(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Amazon S3 bucket, path prefix, and object key that contains the PEM-encoded certificate for the build project.

            For more information, see `certificate <https://docs.aws.amazon.com/codebuild/latest/userguide/create-project-cli.html#cli.environment.certificate>`_ in the *AWS CodeBuild User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-certificate
            '''
            result = self._values.get("certificate")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def compute_type(self) -> typing.Optional[builtins.str]:
            '''The type of compute environment.

            This determines the number of CPU cores and memory the build environment uses. Available values include:

            - ``ATTRIBUTE_BASED_COMPUTE`` : Specify the amount of vCPUs, memory, disk space, and the type of machine.

            .. epigraph::

               If you use ``ATTRIBUTE_BASED_COMPUTE`` , you must define your attributes by using ``computeConfiguration`` . AWS CodeBuild will select the cheapest instance that satisfies your specified attributes. For more information, see `Reserved capacity environment types <https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-compute-types.html#environment-reserved-capacity.types>`_ in the *AWS CodeBuild User Guide* .

            - ``BUILD_GENERAL1_SMALL`` : Use up to 4 GiB memory and 2 vCPUs for builds.
            - ``BUILD_GENERAL1_MEDIUM`` : Use up to 8 GiB memory and 4 vCPUs for builds.
            - ``BUILD_GENERAL1_LARGE`` : Use up to 16 GiB memory and 8 vCPUs for builds, depending on your environment type.
            - ``BUILD_GENERAL1_XLARGE`` : Use up to 72 GiB memory and 36 vCPUs for builds, depending on your environment type.
            - ``BUILD_GENERAL1_2XLARGE`` : Use up to 144 GiB memory, 72 vCPUs, and 824 GB of SSD storage for builds. This compute type supports Docker images up to 100 GB uncompressed.
            - ``BUILD_LAMBDA_1GB`` : Use up to 1 GiB memory for builds. Only available for environment type ``LINUX_LAMBDA_CONTAINER`` and ``ARM_LAMBDA_CONTAINER`` .
            - ``BUILD_LAMBDA_2GB`` : Use up to 2 GiB memory for builds. Only available for environment type ``LINUX_LAMBDA_CONTAINER`` and ``ARM_LAMBDA_CONTAINER`` .
            - ``BUILD_LAMBDA_4GB`` : Use up to 4 GiB memory for builds. Only available for environment type ``LINUX_LAMBDA_CONTAINER`` and ``ARM_LAMBDA_CONTAINER`` .
            - ``BUILD_LAMBDA_8GB`` : Use up to 8 GiB memory for builds. Only available for environment type ``LINUX_LAMBDA_CONTAINER`` and ``ARM_LAMBDA_CONTAINER`` .
            - ``BUILD_LAMBDA_10GB`` : Use up to 10 GiB memory for builds. Only available for environment type ``LINUX_LAMBDA_CONTAINER`` and ``ARM_LAMBDA_CONTAINER`` .

            If you use ``BUILD_GENERAL1_SMALL`` :

            - For environment type ``LINUX_CONTAINER`` , you can use up to 4 GiB memory and 2 vCPUs for builds.
            - For environment type ``LINUX_GPU_CONTAINER`` , you can use up to 16 GiB memory, 4 vCPUs, and 1 NVIDIA A10G Tensor Core GPU for builds.
            - For environment type ``ARM_CONTAINER`` , you can use up to 4 GiB memory and 2 vCPUs on ARM-based processors for builds.

            If you use ``BUILD_GENERAL1_LARGE`` :

            - For environment type ``LINUX_CONTAINER`` , you can use up to 16 GiB memory and 8 vCPUs for builds.
            - For environment type ``LINUX_GPU_CONTAINER`` , you can use up to 255 GiB memory, 32 vCPUs, and 4 NVIDIA Tesla V100 GPUs for builds.
            - For environment type ``ARM_CONTAINER`` , you can use up to 16 GiB memory and 8 vCPUs on ARM-based processors for builds.

            For more information, see `On-demand environment types <https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-compute-types.html#environment.types>`_ in the *AWS CodeBuild User Guide.*

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-computetype
            '''
            result = self._values.get("compute_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def docker_server(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.DockerServerProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-dockerserver
            '''
            result = self._values.get("docker_server")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.DockerServerProperty"]], result)

        @builtins.property
        def environment_variables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.EnvironmentVariableProperty"]]]]:
            '''A set of environment variables to make available to builds for this build project.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-environmentvariables
            '''
            result = self._values.get("environment_variables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.EnvironmentVariableProperty"]]]], result)

        @builtins.property
        def fleet(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.ProjectFleetProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-fleet
            '''
            result = self._values.get("fleet")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.ProjectFleetProperty"]], result)

        @builtins.property
        def image(self) -> typing.Optional[builtins.str]:
            '''The image tag or image digest that identifies the Docker image to use for this build project.

            Use the following formats:

            - For an image tag: ``<registry>/<repository>:<tag>`` . For example, in the Docker repository that CodeBuild uses to manage its Docker images, this would be ``aws/codebuild/standard:4.0`` .
            - For an image digest: ``<registry>/<repository>@<digest>`` . For example, to specify an image with the digest "sha256:cbbf2f9a99b47fc460d422812b6a5adff7dfee951d8fa2e4a98caa0382cfbdbf," use ``<registry>/<repository>@sha256:cbbf2f9a99b47fc460d422812b6a5adff7dfee951d8fa2e4a98caa0382cfbdbf`` .

            For more information, see `Docker images provided by CodeBuild <https://docs.aws.amazon.com//codebuild/latest/userguide/build-env-ref-available.html>`_ in the *AWS CodeBuild user guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-image
            '''
            result = self._values.get("image")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_pull_credentials_type(self) -> typing.Optional[builtins.str]:
            '''The type of credentials AWS CodeBuild uses to pull images in your build. There are two valid values:.

            - ``CODEBUILD`` specifies that AWS CodeBuild uses its own credentials. This requires that you modify your ECR repository policy to trust AWS CodeBuild service principal.
            - ``SERVICE_ROLE`` specifies that AWS CodeBuild uses your build project's service role.

            When you use a cross-account or private registry image, you must use SERVICE_ROLE credentials. When you use an AWS CodeBuild curated image, you must use CODEBUILD credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-imagepullcredentialstype
            '''
            result = self._values.get("image_pull_credentials_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def privileged_mode(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables running the Docker daemon inside a Docker container.

            Set to true only if the build project is used to build Docker images. Otherwise, a build that attempts to interact with the Docker daemon fails. The default setting is ``false`` .

            You can initialize the Docker daemon during the install phase of your build by adding one of the following sets of commands to the install phase of your buildspec file:

            If the operating system's base image is Ubuntu Linux:

            ``- nohup /usr/local/bin/dockerd --host=unix:///var/run/docker.sock --host=tcp://0.0.0.0:2375 --storage-driver=overlay&``

            ``- timeout 15 sh -c "until docker info; do echo .; sleep 1; done"``

            If the operating system's base image is Alpine Linux and the previous command does not work, add the ``-t`` argument to ``timeout`` :

            ``- nohup /usr/local/bin/dockerd --host=unix:///var/run/docker.sock --host=tcp://0.0.0.0:2375 --storage-driver=overlay&``

            ``- timeout -t 15 sh -c "until docker info; do echo .; sleep 1; done"``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-privilegedmode
            '''
            result = self._values.get("privileged_mode")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def registry_credential(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.RegistryCredentialProperty"]]:
            '''``RegistryCredential`` is a property of the `AWS::CodeBuild::Project Environment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-environment>`_ property that specifies information about credentials that provide access to a private Docker registry. When this is set:.

            - ``imagePullCredentialsType`` must be set to ``SERVICE_ROLE`` .
            - images cannot be curated or an Amazon ECR image.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-registrycredential
            '''
            result = self._values.get("registry_credential")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.RegistryCredentialProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of build environment to use for related builds.

            .. epigraph::

               If you're using compute fleets during project creation, ``type`` will be ignored.

            For more information, see `Build environment compute types <https://docs.aws.amazon.com//codebuild/latest/userguide/build-env-ref-compute-types.html>`_ in the *AWS CodeBuild user guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-type
            '''
            result = self._values.get("type")
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
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.EnvironmentVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "type": "type", "value": "value"},
    )
    class EnvironmentVariableProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``EnvironmentVariable`` is a property of the `AWS CodeBuild Project Environment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html>`_ property type that specifies the name and value of an environment variable for an AWS CodeBuild project environment. When you use the environment to run a build, these variables are available for your builds to use. ``EnvironmentVariable`` contains a list of ``EnvironmentVariable`` property types.

            :param name: The name or key of the environment variable.
            :param type: The type of environment variable. Valid values include:. - ``PARAMETER_STORE`` : An environment variable stored in Systems Manager Parameter Store. For environment variables of this type, specify the name of the parameter as the ``value`` of the EnvironmentVariable. The parameter value will be substituted for the name at runtime. You can also define Parameter Store environment variables in the buildspec. To learn how to do so, see `env/parameter-store <https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec.env.parameter-store>`_ in the *AWS CodeBuild User Guide* . - ``PLAINTEXT`` : An environment variable in plain text format. This is the default value. - ``SECRETS_MANAGER`` : An environment variable stored in AWS Secrets Manager . For environment variables of this type, specify the name of the secret as the ``value`` of the EnvironmentVariable. The secret value will be substituted for the name at runtime. You can also define AWS Secrets Manager environment variables in the buildspec. To learn how to do so, see `env/secrets-manager <https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec.env.secrets-manager>`_ in the *AWS CodeBuild User Guide* .
            :param value: The value of the environment variable. .. epigraph:: We strongly discourage the use of ``PLAINTEXT`` environment variables to store sensitive values, especially AWS secret key IDs. ``PLAINTEXT`` environment variables can be displayed in plain text using the AWS CodeBuild console and the AWS CLI . For sensitive values, we recommend you use an environment variable of type ``PARAMETER_STORE`` or ``SECRETS_MANAGER`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environmentvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                environment_variable_property = codebuild_mixins.CfnProjectPropsMixin.EnvironmentVariableProperty(
                    name="name",
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8bb7394aeaeea10758c1328f55277665c3c00485e04a53c996701ac999e8f951)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name or key of the environment variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environmentvariable.html#cfn-codebuild-project-environmentvariable-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of environment variable. Valid values include:.

            - ``PARAMETER_STORE`` : An environment variable stored in Systems Manager Parameter Store. For environment variables of this type, specify the name of the parameter as the ``value`` of the EnvironmentVariable. The parameter value will be substituted for the name at runtime. You can also define Parameter Store environment variables in the buildspec. To learn how to do so, see `env/parameter-store <https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec.env.parameter-store>`_ in the *AWS CodeBuild User Guide* .
            - ``PLAINTEXT`` : An environment variable in plain text format. This is the default value.
            - ``SECRETS_MANAGER`` : An environment variable stored in AWS Secrets Manager . For environment variables of this type, specify the name of the secret as the ``value`` of the EnvironmentVariable. The secret value will be substituted for the name at runtime. You can also define AWS Secrets Manager environment variables in the buildspec. To learn how to do so, see `env/secrets-manager <https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec.env.secrets-manager>`_ in the *AWS CodeBuild User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environmentvariable.html#cfn-codebuild-project-environmentvariable-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the environment variable.

            .. epigraph::

               We strongly discourage the use of ``PLAINTEXT`` environment variables to store sensitive values, especially AWS secret key IDs. ``PLAINTEXT`` environment variables can be displayed in plain text using the AWS CodeBuild console and the AWS CLI . For sensitive values, we recommend you use an environment variable of type ``PARAMETER_STORE`` or ``SECRETS_MANAGER`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environmentvariable.html#cfn-codebuild-project-environmentvariable-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.GitSubmodulesConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"fetch_submodules": "fetchSubmodules"},
    )
    class GitSubmodulesConfigProperty:
        def __init__(
            self,
            *,
            fetch_submodules: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''``GitSubmodulesConfig`` is a property of the `AWS CodeBuild Project Source <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html>`_ property type that specifies information about the Git submodules configuration for the build project.

            :param fetch_submodules: Set to true to fetch Git submodules for your AWS CodeBuild build project.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-gitsubmodulesconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                git_submodules_config_property = codebuild_mixins.CfnProjectPropsMixin.GitSubmodulesConfigProperty(
                    fetch_submodules=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ac370c31aa6c99135c2627e8f720c15c0f8d4038972e3ec23345a0426a6c6638)
                check_type(argname="argument fetch_submodules", value=fetch_submodules, expected_type=type_hints["fetch_submodules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if fetch_submodules is not None:
                self._values["fetch_submodules"] = fetch_submodules

        @builtins.property
        def fetch_submodules(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set to true to fetch Git submodules for your AWS CodeBuild build project.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-gitsubmodulesconfig.html#cfn-codebuild-project-gitsubmodulesconfig-fetchsubmodules
            '''
            result = self._values.get("fetch_submodules")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GitSubmodulesConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.LogsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_watch_logs": "cloudWatchLogs", "s3_logs": "s3Logs"},
    )
    class LogsConfigProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.CloudWatchLogsConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.S3LogsConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''``LogsConfig`` is a property of the `AWS CodeBuild Project <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html>`_ resource that specifies information about logs for a build project. These can be logs in Amazon CloudWatch Logs, built in a specified S3 bucket, or both.

            :param cloud_watch_logs: Information about CloudWatch Logs for a build project. CloudWatch Logs are enabled by default.
            :param s3_logs: Information about logs built to an S3 bucket for a build project. S3 logs are not enabled by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-logsconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                logs_config_property = codebuild_mixins.CfnProjectPropsMixin.LogsConfigProperty(
                    cloud_watch_logs=codebuild_mixins.CfnProjectPropsMixin.CloudWatchLogsConfigProperty(
                        group_name="groupName",
                        status="status",
                        stream_name="streamName"
                    ),
                    s3_logs=codebuild_mixins.CfnProjectPropsMixin.S3LogsConfigProperty(
                        encryption_disabled=False,
                        location="location",
                        status="status"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__942868f8f1c4666aaca036001345c8a55b4485bda695304913fa1306720c926d)
                check_type(argname="argument cloud_watch_logs", value=cloud_watch_logs, expected_type=type_hints["cloud_watch_logs"])
                check_type(argname="argument s3_logs", value=s3_logs, expected_type=type_hints["s3_logs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs is not None:
                self._values["cloud_watch_logs"] = cloud_watch_logs
            if s3_logs is not None:
                self._values["s3_logs"] = s3_logs

        @builtins.property
        def cloud_watch_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.CloudWatchLogsConfigProperty"]]:
            '''Information about CloudWatch Logs for a build project.

            CloudWatch Logs are enabled by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-logsconfig.html#cfn-codebuild-project-logsconfig-cloudwatchlogs
            '''
            result = self._values.get("cloud_watch_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.CloudWatchLogsConfigProperty"]], result)

        @builtins.property
        def s3_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.S3LogsConfigProperty"]]:
            '''Information about logs built to an S3 bucket for a build project.

            S3 logs are not enabled by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-logsconfig.html#cfn-codebuild-project-logsconfig-s3logs
            '''
            result = self._values.get("s3_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.S3LogsConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.ProjectBuildBatchConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "batch_report_mode": "batchReportMode",
            "combine_artifacts": "combineArtifacts",
            "restrictions": "restrictions",
            "service_role": "serviceRole",
            "timeout_in_mins": "timeoutInMins",
        },
    )
    class ProjectBuildBatchConfigProperty:
        def __init__(
            self,
            *,
            batch_report_mode: typing.Optional[builtins.str] = None,
            combine_artifacts: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            restrictions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.BatchRestrictionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_role: typing.Optional[builtins.str] = None,
            timeout_in_mins: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains configuration information about a batch build project.

            :param batch_report_mode: Specifies how build status reports are sent to the source provider for the batch build. This property is only used when the source provider for your project is Bitbucket, GitHub, or GitHub Enterprise, and your project is configured to report build statuses to the source provider. - **REPORT_AGGREGATED_BATCH** - (Default) Aggregate all of the build statuses into a single status report. - **REPORT_INDIVIDUAL_BUILDS** - Send a separate status report for each individual build.
            :param combine_artifacts: Specifies if the build artifacts for the batch build should be combined into a single artifact location.
            :param restrictions: A ``BatchRestrictions`` object that specifies the restrictions for the batch build.
            :param service_role: Specifies the service role ARN for the batch build project.
            :param timeout_in_mins: Specifies the maximum amount of time, in minutes, that the batch build must be completed in.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectbuildbatchconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                project_build_batch_config_property = codebuild_mixins.CfnProjectPropsMixin.ProjectBuildBatchConfigProperty(
                    batch_report_mode="batchReportMode",
                    combine_artifacts=False,
                    restrictions=codebuild_mixins.CfnProjectPropsMixin.BatchRestrictionsProperty(
                        compute_types_allowed=["computeTypesAllowed"],
                        maximum_builds_allowed=123
                    ),
                    service_role="serviceRole",
                    timeout_in_mins=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__45b1fa0e682d0af5e6fa077c0bc6893e22db272022ee3a72e167e6ed575ce779)
                check_type(argname="argument batch_report_mode", value=batch_report_mode, expected_type=type_hints["batch_report_mode"])
                check_type(argname="argument combine_artifacts", value=combine_artifacts, expected_type=type_hints["combine_artifacts"])
                check_type(argname="argument restrictions", value=restrictions, expected_type=type_hints["restrictions"])
                check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
                check_type(argname="argument timeout_in_mins", value=timeout_in_mins, expected_type=type_hints["timeout_in_mins"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if batch_report_mode is not None:
                self._values["batch_report_mode"] = batch_report_mode
            if combine_artifacts is not None:
                self._values["combine_artifacts"] = combine_artifacts
            if restrictions is not None:
                self._values["restrictions"] = restrictions
            if service_role is not None:
                self._values["service_role"] = service_role
            if timeout_in_mins is not None:
                self._values["timeout_in_mins"] = timeout_in_mins

        @builtins.property
        def batch_report_mode(self) -> typing.Optional[builtins.str]:
            '''Specifies how build status reports are sent to the source provider for the batch build.

            This property is only used when the source provider for your project is Bitbucket, GitHub, or GitHub Enterprise, and your project is configured to report build statuses to the source provider.

            - **REPORT_AGGREGATED_BATCH** - (Default) Aggregate all of the build statuses into a single status report.
            - **REPORT_INDIVIDUAL_BUILDS** - Send a separate status report for each individual build.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectbuildbatchconfig.html#cfn-codebuild-project-projectbuildbatchconfig-batchreportmode
            '''
            result = self._values.get("batch_report_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def combine_artifacts(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies if the build artifacts for the batch build should be combined into a single artifact location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectbuildbatchconfig.html#cfn-codebuild-project-projectbuildbatchconfig-combineartifacts
            '''
            result = self._values.get("combine_artifacts")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def restrictions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.BatchRestrictionsProperty"]]:
            '''A ``BatchRestrictions`` object that specifies the restrictions for the batch build.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectbuildbatchconfig.html#cfn-codebuild-project-projectbuildbatchconfig-restrictions
            '''
            result = self._values.get("restrictions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.BatchRestrictionsProperty"]], result)

        @builtins.property
        def service_role(self) -> typing.Optional[builtins.str]:
            '''Specifies the service role ARN for the batch build project.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectbuildbatchconfig.html#cfn-codebuild-project-projectbuildbatchconfig-servicerole
            '''
            result = self._values.get("service_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timeout_in_mins(self) -> typing.Optional[jsii.Number]:
            '''Specifies the maximum amount of time, in minutes, that the batch build must be completed in.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectbuildbatchconfig.html#cfn-codebuild-project-projectbuildbatchconfig-timeoutinmins
            '''
            result = self._values.get("timeout_in_mins")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectBuildBatchConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.ProjectCacheProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cache_namespace": "cacheNamespace",
            "location": "location",
            "modes": "modes",
            "type": "type",
        },
    )
    class ProjectCacheProperty:
        def __init__(
            self,
            *,
            cache_namespace: typing.Optional[builtins.str] = None,
            location: typing.Optional[builtins.str] = None,
            modes: typing.Optional[typing.Sequence[builtins.str]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``ProjectCache`` is a property of the `AWS CodeBuild Project <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html>`_ resource that specifies information about the cache for the build project. If ``ProjectCache`` is not specified, then both of its properties default to ``NO_CACHE`` .

            :param cache_namespace: Defines the scope of the cache. You can use this namespace to share a cache across multiple projects. For more information, see `Cache sharing between projects <https://docs.aws.amazon.com/codebuild/latest/userguide/caching-s3.html#caching-s3-sharing>`_ in the *AWS CodeBuild User Guide* .
            :param location: Information about the cache location:. - ``NO_CACHE`` or ``LOCAL`` : This value is ignored. - ``S3`` : This is the S3 bucket name/prefix.
            :param modes: An array of strings that specify the local cache modes. You can use one or more local cache modes at the same time. This is only used for ``LOCAL`` cache types. Possible values are: - **LOCAL_SOURCE_CACHE** - Caches Git metadata for primary and secondary sources. After the cache is created, subsequent builds pull only the change between commits. This mode is a good choice for projects with a clean working directory and a source that is a large Git repository. If you choose this option and your project does not use a Git repository (GitHub, GitHub Enterprise, or Bitbucket), the option is ignored. - **LOCAL_DOCKER_LAYER_CACHE** - Caches existing Docker layers. This mode is a good choice for projects that build or pull large Docker images. It can prevent the performance issues caused by pulling large Docker images down from the network. .. epigraph:: - You can use a Docker layer cache in the Linux environment only. - The ``privileged`` flag must be set so that your project has the required Docker permissions. - You should consider the security implications before you use a Docker layer cache. - **LOCAL_CUSTOM_CACHE** - Caches directories you specify in the buildspec file. This mode is a good choice if your build scenario is not suited to one of the other three local cache modes. If you use a custom cache: - Only directories can be specified for caching. You cannot specify individual files. - Symlinks are used to reference cached directories. - Cached directories are linked to your build before it downloads its project sources. Cached items are overridden if a source item has the same name. Directories are specified using cache paths in the buildspec file.
            :param type: The type of cache used by the build project. Valid values include:. - ``NO_CACHE`` : The build project does not use any cache. - ``S3`` : The build project reads and writes from and to S3. - ``LOCAL`` : The build project stores a cache locally on a build host that is only available to that build host.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectcache.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                project_cache_property = codebuild_mixins.CfnProjectPropsMixin.ProjectCacheProperty(
                    cache_namespace="cacheNamespace",
                    location="location",
                    modes=["modes"],
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1029b48e621a58acde3ddfe58fed521bedfafbdcecc836549c65773b16f9679c)
                check_type(argname="argument cache_namespace", value=cache_namespace, expected_type=type_hints["cache_namespace"])
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
                check_type(argname="argument modes", value=modes, expected_type=type_hints["modes"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cache_namespace is not None:
                self._values["cache_namespace"] = cache_namespace
            if location is not None:
                self._values["location"] = location
            if modes is not None:
                self._values["modes"] = modes
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def cache_namespace(self) -> typing.Optional[builtins.str]:
            '''Defines the scope of the cache.

            You can use this namespace to share a cache across multiple projects. For more information, see `Cache sharing between projects <https://docs.aws.amazon.com/codebuild/latest/userguide/caching-s3.html#caching-s3-sharing>`_ in the *AWS CodeBuild User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectcache.html#cfn-codebuild-project-projectcache-cachenamespace
            '''
            result = self._values.get("cache_namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def location(self) -> typing.Optional[builtins.str]:
            '''Information about the cache location:.

            - ``NO_CACHE`` or ``LOCAL`` : This value is ignored.
            - ``S3`` : This is the S3 bucket name/prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectcache.html#cfn-codebuild-project-projectcache-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def modes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of strings that specify the local cache modes.

            You can use one or more local cache modes at the same time. This is only used for ``LOCAL`` cache types.

            Possible values are:

            - **LOCAL_SOURCE_CACHE** - Caches Git metadata for primary and secondary sources. After the cache is created, subsequent builds pull only the change between commits. This mode is a good choice for projects with a clean working directory and a source that is a large Git repository. If you choose this option and your project does not use a Git repository (GitHub, GitHub Enterprise, or Bitbucket), the option is ignored.
            - **LOCAL_DOCKER_LAYER_CACHE** - Caches existing Docker layers. This mode is a good choice for projects that build or pull large Docker images. It can prevent the performance issues caused by pulling large Docker images down from the network.

            .. epigraph::

               - You can use a Docker layer cache in the Linux environment only.
               - The ``privileged`` flag must be set so that your project has the required Docker permissions.
               - You should consider the security implications before you use a Docker layer cache.

            - **LOCAL_CUSTOM_CACHE** - Caches directories you specify in the buildspec file. This mode is a good choice if your build scenario is not suited to one of the other three local cache modes. If you use a custom cache:
            - Only directories can be specified for caching. You cannot specify individual files.
            - Symlinks are used to reference cached directories.
            - Cached directories are linked to your build before it downloads its project sources. Cached items are overridden if a source item has the same name. Directories are specified using cache paths in the buildspec file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectcache.html#cfn-codebuild-project-projectcache-modes
            '''
            result = self._values.get("modes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of cache used by the build project. Valid values include:.

            - ``NO_CACHE`` : The build project does not use any cache.
            - ``S3`` : The build project reads and writes from and to S3.
            - ``LOCAL`` : The build project stores a cache locally on a build host that is only available to that build host.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectcache.html#cfn-codebuild-project-projectcache-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectCacheProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.ProjectFileSystemLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "identifier": "identifier",
            "location": "location",
            "mount_options": "mountOptions",
            "mount_point": "mountPoint",
            "type": "type",
        },
    )
    class ProjectFileSystemLocationProperty:
        def __init__(
            self,
            *,
            identifier: typing.Optional[builtins.str] = None,
            location: typing.Optional[builtins.str] = None,
            mount_options: typing.Optional[builtins.str] = None,
            mount_point: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a file system created by Amazon Elastic File System (EFS).

            For more information, see `What Is Amazon Elastic File System? <https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html>`_

            :param identifier: The name used to access a file system created by Amazon EFS. CodeBuild creates an environment variable by appending the ``identifier`` in all capital letters to ``CODEBUILD_`` . For example, if you specify ``my_efs`` for ``identifier`` , a new environment variable is create named ``CODEBUILD_MY_EFS`` . The ``identifier`` is used to mount your file system.
            :param location: A string that specifies the location of the file system created by Amazon EFS. Its format is ``efs-dns-name:/directory-path`` . You can find the DNS name of file system when you view it in the Amazon EFS console. The directory path is a path to a directory in the file system that CodeBuild mounts. For example, if the DNS name of a file system is ``fs-abcd1234.efs.us-west-2.amazonaws.com`` , and its mount directory is ``my-efs-mount-directory`` , then the ``location`` is ``fs-abcd1234.efs.us-west-2.amazonaws.com:/my-efs-mount-directory`` . The directory path in the format ``efs-dns-name:/directory-path`` is optional. If you do not specify a directory path, the location is only the DNS name and CodeBuild mounts the entire file system.
            :param mount_options: The mount options for a file system created by Amazon EFS. The default mount options used by CodeBuild are ``nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2`` . For more information, see `Recommended NFS Mount Options <https://docs.aws.amazon.com/efs/latest/ug/mounting-fs-nfs-mount-settings.html>`_ .
            :param mount_point: The location in the container where you mount the file system.
            :param type: The type of the file system. The one supported type is ``EFS`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfilesystemlocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                project_file_system_location_property = codebuild_mixins.CfnProjectPropsMixin.ProjectFileSystemLocationProperty(
                    identifier="identifier",
                    location="location",
                    mount_options="mountOptions",
                    mount_point="mountPoint",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2fbf0ad63512fec69ddcc34266342e70ba00553896b45dec36d46a07661d801b)
                check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
                check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
                check_type(argname="argument mount_point", value=mount_point, expected_type=type_hints["mount_point"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if identifier is not None:
                self._values["identifier"] = identifier
            if location is not None:
                self._values["location"] = location
            if mount_options is not None:
                self._values["mount_options"] = mount_options
            if mount_point is not None:
                self._values["mount_point"] = mount_point
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def identifier(self) -> typing.Optional[builtins.str]:
            '''The name used to access a file system created by Amazon EFS.

            CodeBuild creates an environment variable by appending the ``identifier`` in all capital letters to ``CODEBUILD_`` . For example, if you specify ``my_efs`` for ``identifier`` , a new environment variable is create named ``CODEBUILD_MY_EFS`` .

            The ``identifier`` is used to mount your file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfilesystemlocation.html#cfn-codebuild-project-projectfilesystemlocation-identifier
            '''
            result = self._values.get("identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def location(self) -> typing.Optional[builtins.str]:
            '''A string that specifies the location of the file system created by Amazon EFS.

            Its format is ``efs-dns-name:/directory-path`` . You can find the DNS name of file system when you view it in the Amazon EFS console. The directory path is a path to a directory in the file system that CodeBuild mounts. For example, if the DNS name of a file system is ``fs-abcd1234.efs.us-west-2.amazonaws.com`` , and its mount directory is ``my-efs-mount-directory`` , then the ``location`` is ``fs-abcd1234.efs.us-west-2.amazonaws.com:/my-efs-mount-directory`` .

            The directory path in the format ``efs-dns-name:/directory-path`` is optional. If you do not specify a directory path, the location is only the DNS name and CodeBuild mounts the entire file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfilesystemlocation.html#cfn-codebuild-project-projectfilesystemlocation-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mount_options(self) -> typing.Optional[builtins.str]:
            '''The mount options for a file system created by Amazon EFS.

            The default mount options used by CodeBuild are ``nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2`` . For more information, see `Recommended NFS Mount Options <https://docs.aws.amazon.com/efs/latest/ug/mounting-fs-nfs-mount-settings.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfilesystemlocation.html#cfn-codebuild-project-projectfilesystemlocation-mountoptions
            '''
            result = self._values.get("mount_options")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mount_point(self) -> typing.Optional[builtins.str]:
            '''The location in the container where you mount the file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfilesystemlocation.html#cfn-codebuild-project-projectfilesystemlocation-mountpoint
            '''
            result = self._values.get("mount_point")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the file system.

            The one supported type is ``EFS`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfilesystemlocation.html#cfn-codebuild-project-projectfilesystemlocation-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectFileSystemLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.ProjectFleetProperty",
        jsii_struct_bases=[],
        name_mapping={"fleet_arn": "fleetArn"},
    )
    class ProjectFleetProperty:
        def __init__(self, *, fleet_arn: typing.Optional[builtins.str] = None) -> None:
            '''Information about the compute fleet of the build project.

            For more information, see `Working with reserved capacity in AWS CodeBuild <https://docs.aws.amazon.com/codebuild/latest/userguide/fleets.html>`_ .

            :param fleet_arn: Specifies the compute fleet ARN for the build project.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfleet.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                project_fleet_property = codebuild_mixins.CfnProjectPropsMixin.ProjectFleetProperty(
                    fleet_arn="fleetArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__34ca8ac8975c78adfb642f1cefb3645b5eae62b0bc80dc0db3f8f93fb5e79b68)
                check_type(argname="argument fleet_arn", value=fleet_arn, expected_type=type_hints["fleet_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if fleet_arn is not None:
                self._values["fleet_arn"] = fleet_arn

        @builtins.property
        def fleet_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the compute fleet ARN for the build project.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectfleet.html#cfn-codebuild-project-projectfleet-fleetarn
            '''
            result = self._values.get("fleet_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectFleetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.ProjectSourceVersionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "source_identifier": "sourceIdentifier",
            "source_version": "sourceVersion",
        },
    )
    class ProjectSourceVersionProperty:
        def __init__(
            self,
            *,
            source_identifier: typing.Optional[builtins.str] = None,
            source_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A source identifier and its corresponding version.

            :param source_identifier: An identifier for a source in the build project. The identifier can only contain alphanumeric characters and underscores, and must be less than 128 characters in length.
            :param source_version: The source version for the corresponding source identifier. If specified, must be one of:. - For CodeCommit: the commit ID, branch, or Git tag to use. - For GitHub: the commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build. If a pull request ID is specified, it must use the format ``pr/pull-request-ID`` (for example, ``pr/25`` ). If a branch name is specified, the branch's HEAD commit ID is used. If not specified, the default branch's HEAD commit ID is used. - For GitLab: the commit ID, branch, or Git tag to use. - For Bitbucket: the commit ID, branch name, or tag name that corresponds to the version of the source code you want to build. If a branch name is specified, the branch's HEAD commit ID is used. If not specified, the default branch's HEAD commit ID is used. - For Amazon S3: the version ID of the object that represents the build input ZIP file to use. For more information, see `Source Version Sample with CodeBuild <https://docs.aws.amazon.com/codebuild/latest/userguide/sample-source-version.html>`_ in the *AWS CodeBuild User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectsourceversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                project_source_version_property = codebuild_mixins.CfnProjectPropsMixin.ProjectSourceVersionProperty(
                    source_identifier="sourceIdentifier",
                    source_version="sourceVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__94fe2d11da8c3414a7e1ad29f64759df534b925e1f448ece8d3f7e004a87ab04)
                check_type(argname="argument source_identifier", value=source_identifier, expected_type=type_hints["source_identifier"])
                check_type(argname="argument source_version", value=source_version, expected_type=type_hints["source_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source_identifier is not None:
                self._values["source_identifier"] = source_identifier
            if source_version is not None:
                self._values["source_version"] = source_version

        @builtins.property
        def source_identifier(self) -> typing.Optional[builtins.str]:
            '''An identifier for a source in the build project.

            The identifier can only contain alphanumeric characters and underscores, and must be less than 128 characters in length.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectsourceversion.html#cfn-codebuild-project-projectsourceversion-sourceidentifier
            '''
            result = self._values.get("source_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_version(self) -> typing.Optional[builtins.str]:
            '''The source version for the corresponding source identifier. If specified, must be one of:.

            - For CodeCommit: the commit ID, branch, or Git tag to use.
            - For GitHub: the commit ID, pull request ID, branch name, or tag name that corresponds to the version of the source code you want to build. If a pull request ID is specified, it must use the format ``pr/pull-request-ID`` (for example, ``pr/25`` ). If a branch name is specified, the branch's HEAD commit ID is used. If not specified, the default branch's HEAD commit ID is used.
            - For GitLab: the commit ID, branch, or Git tag to use.
            - For Bitbucket: the commit ID, branch name, or tag name that corresponds to the version of the source code you want to build. If a branch name is specified, the branch's HEAD commit ID is used. If not specified, the default branch's HEAD commit ID is used.
            - For Amazon S3: the version ID of the object that represents the build input ZIP file to use.

            For more information, see `Source Version Sample with CodeBuild <https://docs.aws.amazon.com/codebuild/latest/userguide/sample-source-version.html>`_ in the *AWS CodeBuild User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectsourceversion.html#cfn-codebuild-project-projectsourceversion-sourceversion
            '''
            result = self._values.get("source_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectSourceVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.ProjectTriggersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "build_type": "buildType",
            "filter_groups": "filterGroups",
            "pull_request_build_policy": "pullRequestBuildPolicy",
            "scope_configuration": "scopeConfiguration",
            "webhook": "webhook",
        },
    )
    class ProjectTriggersProperty:
        def __init__(
            self,
            *,
            build_type: typing.Optional[builtins.str] = None,
            filter_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.WebhookFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]]]] = None,
            pull_request_build_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.PullRequestBuildPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            scope_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.ScopeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            webhook: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''``ProjectTriggers`` is a property of the `AWS CodeBuild Project <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html>`_ resource that specifies webhooks that trigger an AWS CodeBuild build.

            .. epigraph::

               The Webhook feature isn't available in AWS CloudFormation for GitHub Enterprise projects. Use the AWS CLI or AWS CodeBuild console to create the webhook.

            :param build_type: Specifies the type of build this webhook will trigger. Allowed values are:. - **BUILD** - A single build - **BUILD_BATCH** - A batch build
            :param filter_groups: A list of lists of ``WebhookFilter`` objects used to determine which webhook events are triggered. At least one ``WebhookFilter`` in the array must specify ``EVENT`` as its type.
            :param pull_request_build_policy: 
            :param scope_configuration: Contains configuration information about the scope for a webhook.
            :param webhook: Specifies whether or not to begin automatically rebuilding the source code every time a code change is pushed to the repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projecttriggers.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                project_triggers_property = codebuild_mixins.CfnProjectPropsMixin.ProjectTriggersProperty(
                    build_type="buildType",
                    filter_groups=[[codebuild_mixins.CfnProjectPropsMixin.WebhookFilterProperty(
                        exclude_matched_pattern=False,
                        pattern="pattern",
                        type="type"
                    )]],
                    pull_request_build_policy=codebuild_mixins.CfnProjectPropsMixin.PullRequestBuildPolicyProperty(
                        approver_roles=["approverRoles"],
                        requires_comment_approval="requiresCommentApproval"
                    ),
                    scope_configuration=codebuild_mixins.CfnProjectPropsMixin.ScopeConfigurationProperty(
                        domain="domain",
                        name="name",
                        scope="scope"
                    ),
                    webhook=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a82270fb8fc5b574fdd43367823cb0be400327115dea0f0debf802962be96631)
                check_type(argname="argument build_type", value=build_type, expected_type=type_hints["build_type"])
                check_type(argname="argument filter_groups", value=filter_groups, expected_type=type_hints["filter_groups"])
                check_type(argname="argument pull_request_build_policy", value=pull_request_build_policy, expected_type=type_hints["pull_request_build_policy"])
                check_type(argname="argument scope_configuration", value=scope_configuration, expected_type=type_hints["scope_configuration"])
                check_type(argname="argument webhook", value=webhook, expected_type=type_hints["webhook"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if build_type is not None:
                self._values["build_type"] = build_type
            if filter_groups is not None:
                self._values["filter_groups"] = filter_groups
            if pull_request_build_policy is not None:
                self._values["pull_request_build_policy"] = pull_request_build_policy
            if scope_configuration is not None:
                self._values["scope_configuration"] = scope_configuration
            if webhook is not None:
                self._values["webhook"] = webhook

        @builtins.property
        def build_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of build this webhook will trigger. Allowed values are:.

            - **BUILD** - A single build
            - **BUILD_BATCH** - A batch build

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projecttriggers.html#cfn-codebuild-project-projecttriggers-buildtype
            '''
            result = self._values.get("build_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def filter_groups(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.WebhookFilterProperty"]]]]]]:
            '''A list of lists of ``WebhookFilter`` objects used to determine which webhook events are triggered.

            At least one ``WebhookFilter`` in the array must specify ``EVENT`` as its type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projecttriggers.html#cfn-codebuild-project-projecttriggers-filtergroups
            '''
            result = self._values.get("filter_groups")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.WebhookFilterProperty"]]]]]], result)

        @builtins.property
        def pull_request_build_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.PullRequestBuildPolicyProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projecttriggers.html#cfn-codebuild-project-projecttriggers-pullrequestbuildpolicy
            '''
            result = self._values.get("pull_request_build_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.PullRequestBuildPolicyProperty"]], result)

        @builtins.property
        def scope_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.ScopeConfigurationProperty"]]:
            '''Contains configuration information about the scope for a webhook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projecttriggers.html#cfn-codebuild-project-projecttriggers-scopeconfiguration
            '''
            result = self._values.get("scope_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.ScopeConfigurationProperty"]], result)

        @builtins.property
        def webhook(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether or not to begin automatically rebuilding the source code every time a code change is pushed to the repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projecttriggers.html#cfn-codebuild-project-projecttriggers-webhook
            '''
            result = self._values.get("webhook")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectTriggersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.PullRequestBuildPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "approver_roles": "approverRoles",
            "requires_comment_approval": "requiresCommentApproval",
        },
    )
    class PullRequestBuildPolicyProperty:
        def __init__(
            self,
            *,
            approver_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
            requires_comment_approval: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param approver_roles: 
            :param requires_comment_approval: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-pullrequestbuildpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                pull_request_build_policy_property = codebuild_mixins.CfnProjectPropsMixin.PullRequestBuildPolicyProperty(
                    approver_roles=["approverRoles"],
                    requires_comment_approval="requiresCommentApproval"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3d65d5e1f87540f9d71c8daf3fd22d1705e998a53250f5fd4ae1b0fb70703fc1)
                check_type(argname="argument approver_roles", value=approver_roles, expected_type=type_hints["approver_roles"])
                check_type(argname="argument requires_comment_approval", value=requires_comment_approval, expected_type=type_hints["requires_comment_approval"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if approver_roles is not None:
                self._values["approver_roles"] = approver_roles
            if requires_comment_approval is not None:
                self._values["requires_comment_approval"] = requires_comment_approval

        @builtins.property
        def approver_roles(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-pullrequestbuildpolicy.html#cfn-codebuild-project-pullrequestbuildpolicy-approverroles
            '''
            result = self._values.get("approver_roles")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def requires_comment_approval(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-pullrequestbuildpolicy.html#cfn-codebuild-project-pullrequestbuildpolicy-requirescommentapproval
            '''
            result = self._values.get("requires_comment_approval")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PullRequestBuildPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.RegistryCredentialProperty",
        jsii_struct_bases=[],
        name_mapping={
            "credential": "credential",
            "credential_provider": "credentialProvider",
        },
    )
    class RegistryCredentialProperty:
        def __init__(
            self,
            *,
            credential: typing.Optional[builtins.str] = None,
            credential_provider: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``RegistryCredential`` is a property of the `AWS CodeBuild Project Environment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html>`_ property type that specifies information about credentials that provide access to a private Docker registry. When this is set:.

            - ``imagePullCredentialsType`` must be set to ``SERVICE_ROLE`` .
            - images cannot be curated or an Amazon ECR image.

            For more information, see `Private Registry with AWS Secrets Manager Sample for AWS CodeBuild <https://docs.aws.amazon.com/codebuild/latest/userguide/sample-private-registry.html>`_ .

            :param credential: The Amazon Resource Name (ARN) or name of credentials created using AWS Secrets Manager . .. epigraph:: The ``credential`` can use the name of the credentials only if they exist in your current AWS Region .
            :param credential_provider: The service that created the credentials to access a private Docker registry. The valid value, SECRETS_MANAGER, is for AWS Secrets Manager .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-registrycredential.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                registry_credential_property = codebuild_mixins.CfnProjectPropsMixin.RegistryCredentialProperty(
                    credential="credential",
                    credential_provider="credentialProvider"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7435fbf0e2aa06a6a36f7347351e392f58a343a28ae50026b9cf995502a7c87c)
                check_type(argname="argument credential", value=credential, expected_type=type_hints["credential"])
                check_type(argname="argument credential_provider", value=credential_provider, expected_type=type_hints["credential_provider"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if credential is not None:
                self._values["credential"] = credential
            if credential_provider is not None:
                self._values["credential_provider"] = credential_provider

        @builtins.property
        def credential(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) or name of credentials created using AWS Secrets Manager .

            .. epigraph::

               The ``credential`` can use the name of the credentials only if they exist in your current AWS Region .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-registrycredential.html#cfn-codebuild-project-registrycredential-credential
            '''
            result = self._values.get("credential")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def credential_provider(self) -> typing.Optional[builtins.str]:
            '''The service that created the credentials to access a private Docker registry.

            The valid value, SECRETS_MANAGER, is for AWS Secrets Manager .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-registrycredential.html#cfn-codebuild-project-registrycredential-credentialprovider
            '''
            result = self._values.get("credential_provider")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RegistryCredentialProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.S3LogsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_disabled": "encryptionDisabled",
            "location": "location",
            "status": "status",
        },
    )
    class S3LogsConfigProperty:
        def __init__(
            self,
            *,
            encryption_disabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            location: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``S3Logs`` is a property of the `AWS CodeBuild Project LogsConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-logsconfig.html>`_ property type that specifies settings for logs generated by an AWS CodeBuild build in an S3 bucket.

            :param encryption_disabled: Set to true if you do not want your S3 build log output encrypted. By default S3 build logs are encrypted.
            :param location: The ARN of an S3 bucket and the path prefix for S3 logs. If your Amazon S3 bucket name is ``my-bucket`` , and your path prefix is ``build-log`` , then acceptable formats are ``my-bucket/build-log`` or ``arn:aws:s3:::my-bucket/build-log`` .
            :param status: The current status of the S3 build logs. Valid values are:. - ``ENABLED`` : S3 build logs are enabled for this build project. - ``DISABLED`` : S3 build logs are not enabled for this build project.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-s3logsconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                s3_logs_config_property = codebuild_mixins.CfnProjectPropsMixin.S3LogsConfigProperty(
                    encryption_disabled=False,
                    location="location",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e8155973c9de5473419a6c78000ed49cdb6d7973d6cd9cd655a65d417bc7fc1c)
                check_type(argname="argument encryption_disabled", value=encryption_disabled, expected_type=type_hints["encryption_disabled"])
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_disabled is not None:
                self._values["encryption_disabled"] = encryption_disabled
            if location is not None:
                self._values["location"] = location
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def encryption_disabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set to true if you do not want your S3 build log output encrypted.

            By default S3 build logs are encrypted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-s3logsconfig.html#cfn-codebuild-project-s3logsconfig-encryptiondisabled
            '''
            result = self._values.get("encryption_disabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def location(self) -> typing.Optional[builtins.str]:
            '''The ARN of an S3 bucket and the path prefix for S3 logs.

            If your Amazon S3 bucket name is ``my-bucket`` , and your path prefix is ``build-log`` , then acceptable formats are ``my-bucket/build-log`` or ``arn:aws:s3:::my-bucket/build-log`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-s3logsconfig.html#cfn-codebuild-project-s3logsconfig-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The current status of the S3 build logs. Valid values are:.

            - ``ENABLED`` : S3 build logs are enabled for this build project.
            - ``DISABLED`` : S3 build logs are not enabled for this build project.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-s3logsconfig.html#cfn-codebuild-project-s3logsconfig-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LogsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.ScopeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"domain": "domain", "name": "name", "scope": "scope"},
    )
    class ScopeConfigurationProperty:
        def __init__(
            self,
            *,
            domain: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            scope: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains configuration information about the scope for a webhook.

            :param domain: The domain of the GitHub Enterprise organization or the GitLab Self Managed group. Note that this parameter is only required if your project's source type is GITHUB_ENTERPRISE or GITLAB_SELF_MANAGED.
            :param name: The name of either the enterprise or organization that will send webhook events to CodeBuild , depending on if the webhook is a global or organization webhook respectively.
            :param scope: The type of scope for a GitHub or GitLab webhook. The scope default is GITHUB_ORGANIZATION.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-scopeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                scope_configuration_property = codebuild_mixins.CfnProjectPropsMixin.ScopeConfigurationProperty(
                    domain="domain",
                    name="name",
                    scope="scope"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5446740b535cb89b1c8c2d3f665968f5fe41dd964ef3b1e9e2dde778d0e0cc9a)
                check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain is not None:
                self._values["domain"] = domain
            if name is not None:
                self._values["name"] = name
            if scope is not None:
                self._values["scope"] = scope

        @builtins.property
        def domain(self) -> typing.Optional[builtins.str]:
            '''The domain of the GitHub Enterprise organization or the GitLab Self Managed group.

            Note that this parameter is only required if your project's source type is GITHUB_ENTERPRISE or GITLAB_SELF_MANAGED.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-scopeconfiguration.html#cfn-codebuild-project-scopeconfiguration-domain
            '''
            result = self._values.get("domain")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of either the enterprise or organization that will send webhook events to CodeBuild , depending on if the webhook is a global or organization webhook respectively.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-scopeconfiguration.html#cfn-codebuild-project-scopeconfiguration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            '''The type of scope for a GitHub or GitLab webhook.

            The scope default is GITHUB_ORGANIZATION.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-scopeconfiguration.html#cfn-codebuild-project-scopeconfiguration-scope
            '''
            result = self._values.get("scope")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScopeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.SourceAuthProperty",
        jsii_struct_bases=[],
        name_mapping={"resource": "resource", "type": "type"},
    )
    class SourceAuthProperty:
        def __init__(
            self,
            *,
            resource: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``SourceAuth`` is a property of the `AWS CodeBuild Project Source <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html>`_ property type that specifies authorization settings for AWS CodeBuild to access the source code to be built.

            :param resource: The resource value that applies to the specified authorization type.
            :param type: The authorization type to use. Valid options are OAUTH, CODECONNECTIONS, or SECRETS_MANAGER.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-sourceauth.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                source_auth_property = codebuild_mixins.CfnProjectPropsMixin.SourceAuthProperty(
                    resource="resource",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9c68115cb903c8e13747e2f1090df2d00e9c5ab731e63324a728e2c59001618d)
                check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource is not None:
                self._values["resource"] = resource
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def resource(self) -> typing.Optional[builtins.str]:
            '''The resource value that applies to the specified authorization type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-sourceauth.html#cfn-codebuild-project-sourceauth-resource
            '''
            result = self._values.get("resource")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The authorization type to use.

            Valid options are OAUTH, CODECONNECTIONS, or SECRETS_MANAGER.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-sourceauth.html#cfn-codebuild-project-sourceauth-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceAuthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.SourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auth": "auth",
            "build_spec": "buildSpec",
            "build_status_config": "buildStatusConfig",
            "git_clone_depth": "gitCloneDepth",
            "git_submodules_config": "gitSubmodulesConfig",
            "insecure_ssl": "insecureSsl",
            "location": "location",
            "report_build_status": "reportBuildStatus",
            "source_identifier": "sourceIdentifier",
            "type": "type",
        },
    )
    class SourceProperty:
        def __init__(
            self,
            *,
            auth: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.SourceAuthProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            build_spec: typing.Optional[builtins.str] = None,
            build_status_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.BuildStatusConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            git_clone_depth: typing.Optional[jsii.Number] = None,
            git_submodules_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.GitSubmodulesConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            insecure_ssl: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            location: typing.Optional[builtins.str] = None,
            report_build_status: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            source_identifier: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``Source`` is a property of the `AWS::CodeBuild::Project <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html>`_ resource that specifies the source code settings for the project, such as the source code's repository type and location.

            :param auth: Information about the authorization settings for AWS CodeBuild to access the source code to be built.
            :param build_spec: The build specification for the project. If this value is not provided, then the source code must contain a buildspec file named ``buildspec.yml`` at the root level. If this value is provided, it can be either a single string containing the entire build specification, or the path to an alternate buildspec file relative to the value of the built-in environment variable ``CODEBUILD_SRC_DIR`` . The alternate buildspec file can have a name other than ``buildspec.yml`` , for example ``myspec.yml`` or ``build_spec_qa.yml`` or similar. For more information, see the `Build Spec Reference <https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec-ref-example>`_ in the *AWS CodeBuild User Guide* .
            :param build_status_config: Contains information that defines how the build project reports the build status to the source provider. This option is only used when the source provider is ``GITHUB`` , ``GITHUB_ENTERPRISE`` , or ``BITBUCKET`` .
            :param git_clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build project. If your source type is Amazon S3, this value is not supported.
            :param git_submodules_config: Information about the Git submodules configuration for the build project.
            :param insecure_ssl: This is used with GitHub Enterprise only. Set to true to ignore SSL warnings while connecting to your GitHub Enterprise project repository. The default value is ``false`` . ``InsecureSsl`` should be used for testing purposes only. It should not be used in a production environment.
            :param location: Information about the location of the source code to be built. Valid values include:. - For source code settings that are specified in the source action of a pipeline in CodePipeline, ``location`` should not be specified. If it is specified, CodePipeline ignores it. This is because CodePipeline uses the settings in a pipeline's source action instead of this value. - For source code in an CodeCommit repository, the HTTPS clone URL to the repository that contains the source code and the buildspec file (for example, ``https://git-codecommit.<region-ID>.amazonaws.com/v1/repos/<repo-name>`` ). - For source code in an Amazon S3 input bucket, one of the following. - The path to the ZIP file that contains the source code (for example, ``<bucket-name>/<path>/<object-name>.zip`` ). - The path to the folder that contains the source code (for example, ``<bucket-name>/<path-to-source-code>/<folder>/`` ). - For source code in a GitHub repository, the HTTPS clone URL to the repository that contains the source and the buildspec file. You must connect your AWS account to your GitHub account. Use the AWS CodeBuild console to start creating a build project. When you use the console to connect (or reconnect) with GitHub, on the GitHub *Authorize application* page, for *Organization access* , choose *Request access* next to each repository you want to allow AWS CodeBuild to have access to, and then choose *Authorize application* . (After you have connected to your GitHub account, you do not need to finish creating the build project. You can leave the AWS CodeBuild console.) To instruct AWS CodeBuild to use this connection, in the ``source`` object, set the ``auth`` object's ``type`` value to ``OAUTH`` . - For source code in an GitLab or self-managed GitLab repository, the HTTPS clone URL to the repository that contains the source and the buildspec file. You must connect your AWS account to your GitLab account. Use the AWS CodeBuild console to start creating a build project. When you use the console to connect (or reconnect) with GitLab, on the Connections *Authorize application* page, choose *Authorize* . Then on the AWS CodeConnections *Create GitLab connection* page, choose *Connect to GitLab* . (After you have connected to your GitLab account, you do not need to finish creating the build project. You can leave the AWS CodeBuild console.) To instruct AWS CodeBuild to override the default connection and use this connection instead, set the ``auth`` object's ``type`` value to ``CODECONNECTIONS`` in the ``source`` object. - For source code in a Bitbucket repository, the HTTPS clone URL to the repository that contains the source and the buildspec file. You must connect your AWS account to your Bitbucket account. Use the AWS CodeBuild console to start creating a build project. When you use the console to connect (or reconnect) with Bitbucket, on the Bitbucket *Confirm access to your account* page, choose *Grant access* . (After you have connected to your Bitbucket account, you do not need to finish creating the build project. You can leave the AWS CodeBuild console.) To instruct AWS CodeBuild to use this connection, in the ``source`` object, set the ``auth`` object's ``type`` value to ``OAUTH`` . If you specify ``CODEPIPELINE`` for the ``Type`` property, don't specify this property. For all of the other types, you must specify ``Location`` .
            :param report_build_status: Set to true to report the status of a build's start and finish to your source provider. This option is valid only when your source provider is GitHub, GitHub Enterprise, GitLab, GitLab Self Managed, or Bitbucket. If this is set and you use a different source provider, an ``invalidInputException`` is thrown.
            :param source_identifier: An identifier for this project source. The identifier can only contain alphanumeric characters and underscores, and must be less than 128 characters in length.
            :param type: The type of repository that contains the source code to be built. Valid values include:. - ``BITBUCKET`` : The source code is in a Bitbucket repository. - ``CODECOMMIT`` : The source code is in an CodeCommit repository. - ``CODEPIPELINE`` : The source code settings are specified in the source action of a pipeline in CodePipeline. - ``GITHUB`` : The source code is in a GitHub repository. - ``GITHUB_ENTERPRISE`` : The source code is in a GitHub Enterprise Server repository. - ``GITLAB`` : The source code is in a GitLab repository. - ``GITLAB_SELF_MANAGED`` : The source code is in a self-managed GitLab repository. - ``NO_SOURCE`` : The project does not have input source code. - ``S3`` : The source code is in an Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                source_property = codebuild_mixins.CfnProjectPropsMixin.SourceProperty(
                    auth=codebuild_mixins.CfnProjectPropsMixin.SourceAuthProperty(
                        resource="resource",
                        type="type"
                    ),
                    build_spec="buildSpec",
                    build_status_config=codebuild_mixins.CfnProjectPropsMixin.BuildStatusConfigProperty(
                        context="context",
                        target_url="targetUrl"
                    ),
                    git_clone_depth=123,
                    git_submodules_config=codebuild_mixins.CfnProjectPropsMixin.GitSubmodulesConfigProperty(
                        fetch_submodules=False
                    ),
                    insecure_ssl=False,
                    location="location",
                    report_build_status=False,
                    source_identifier="sourceIdentifier",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__103701bb968de376f03791b4fdbaf793cbeee3000d4aa9931fe0fde434105a27)
                check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
                check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
                check_type(argname="argument build_status_config", value=build_status_config, expected_type=type_hints["build_status_config"])
                check_type(argname="argument git_clone_depth", value=git_clone_depth, expected_type=type_hints["git_clone_depth"])
                check_type(argname="argument git_submodules_config", value=git_submodules_config, expected_type=type_hints["git_submodules_config"])
                check_type(argname="argument insecure_ssl", value=insecure_ssl, expected_type=type_hints["insecure_ssl"])
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
                check_type(argname="argument report_build_status", value=report_build_status, expected_type=type_hints["report_build_status"])
                check_type(argname="argument source_identifier", value=source_identifier, expected_type=type_hints["source_identifier"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth is not None:
                self._values["auth"] = auth
            if build_spec is not None:
                self._values["build_spec"] = build_spec
            if build_status_config is not None:
                self._values["build_status_config"] = build_status_config
            if git_clone_depth is not None:
                self._values["git_clone_depth"] = git_clone_depth
            if git_submodules_config is not None:
                self._values["git_submodules_config"] = git_submodules_config
            if insecure_ssl is not None:
                self._values["insecure_ssl"] = insecure_ssl
            if location is not None:
                self._values["location"] = location
            if report_build_status is not None:
                self._values["report_build_status"] = report_build_status
            if source_identifier is not None:
                self._values["source_identifier"] = source_identifier
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def auth(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.SourceAuthProperty"]]:
            '''Information about the authorization settings for AWS CodeBuild to access the source code to be built.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-auth
            '''
            result = self._values.get("auth")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.SourceAuthProperty"]], result)

        @builtins.property
        def build_spec(self) -> typing.Optional[builtins.str]:
            '''The build specification for the project.

            If this value is not provided, then the source code must contain a buildspec file named ``buildspec.yml`` at the root level. If this value is provided, it can be either a single string containing the entire build specification, or the path to an alternate buildspec file relative to the value of the built-in environment variable ``CODEBUILD_SRC_DIR`` . The alternate buildspec file can have a name other than ``buildspec.yml`` , for example ``myspec.yml`` or ``build_spec_qa.yml`` or similar. For more information, see the `Build Spec Reference <https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec-ref-example>`_ in the *AWS CodeBuild User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-buildspec
            '''
            result = self._values.get("build_spec")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def build_status_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.BuildStatusConfigProperty"]]:
            '''Contains information that defines how the build project reports the build status to the source provider.

            This option is only used when the source provider is ``GITHUB`` , ``GITHUB_ENTERPRISE`` , or ``BITBUCKET`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-buildstatusconfig
            '''
            result = self._values.get("build_status_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.BuildStatusConfigProperty"]], result)

        @builtins.property
        def git_clone_depth(self) -> typing.Optional[jsii.Number]:
            '''The depth of history to download.

            Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build project. If your source type is Amazon S3, this value is not supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-gitclonedepth
            '''
            result = self._values.get("git_clone_depth")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def git_submodules_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.GitSubmodulesConfigProperty"]]:
            '''Information about the Git submodules configuration for the build project.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-gitsubmodulesconfig
            '''
            result = self._values.get("git_submodules_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.GitSubmodulesConfigProperty"]], result)

        @builtins.property
        def insecure_ssl(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''This is used with GitHub Enterprise only.

            Set to true to ignore SSL warnings while connecting to your GitHub Enterprise project repository. The default value is ``false`` . ``InsecureSsl`` should be used for testing purposes only. It should not be used in a production environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-insecuressl
            '''
            result = self._values.get("insecure_ssl")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def location(self) -> typing.Optional[builtins.str]:
            '''Information about the location of the source code to be built. Valid values include:.

            - For source code settings that are specified in the source action of a pipeline in CodePipeline, ``location`` should not be specified. If it is specified, CodePipeline ignores it. This is because CodePipeline uses the settings in a pipeline's source action instead of this value.
            - For source code in an CodeCommit repository, the HTTPS clone URL to the repository that contains the source code and the buildspec file (for example, ``https://git-codecommit.<region-ID>.amazonaws.com/v1/repos/<repo-name>`` ).
            - For source code in an Amazon S3 input bucket, one of the following.
            - The path to the ZIP file that contains the source code (for example, ``<bucket-name>/<path>/<object-name>.zip`` ).
            - The path to the folder that contains the source code (for example, ``<bucket-name>/<path-to-source-code>/<folder>/`` ).
            - For source code in a GitHub repository, the HTTPS clone URL to the repository that contains the source and the buildspec file. You must connect your AWS account to your GitHub account. Use the AWS CodeBuild console to start creating a build project. When you use the console to connect (or reconnect) with GitHub, on the GitHub *Authorize application* page, for *Organization access* , choose *Request access* next to each repository you want to allow AWS CodeBuild to have access to, and then choose *Authorize application* . (After you have connected to your GitHub account, you do not need to finish creating the build project. You can leave the AWS CodeBuild console.) To instruct AWS CodeBuild to use this connection, in the ``source`` object, set the ``auth`` object's ``type`` value to ``OAUTH`` .
            - For source code in an GitLab or self-managed GitLab repository, the HTTPS clone URL to the repository that contains the source and the buildspec file. You must connect your AWS account to your GitLab account. Use the AWS CodeBuild console to start creating a build project. When you use the console to connect (or reconnect) with GitLab, on the Connections *Authorize application* page, choose *Authorize* . Then on the AWS CodeConnections *Create GitLab connection* page, choose *Connect to GitLab* . (After you have connected to your GitLab account, you do not need to finish creating the build project. You can leave the AWS CodeBuild console.) To instruct AWS CodeBuild to override the default connection and use this connection instead, set the ``auth`` object's ``type`` value to ``CODECONNECTIONS`` in the ``source`` object.
            - For source code in a Bitbucket repository, the HTTPS clone URL to the repository that contains the source and the buildspec file. You must connect your AWS account to your Bitbucket account. Use the AWS CodeBuild console to start creating a build project. When you use the console to connect (or reconnect) with Bitbucket, on the Bitbucket *Confirm access to your account* page, choose *Grant access* . (After you have connected to your Bitbucket account, you do not need to finish creating the build project. You can leave the AWS CodeBuild console.) To instruct AWS CodeBuild to use this connection, in the ``source`` object, set the ``auth`` object's ``type`` value to ``OAUTH`` .

            If you specify ``CODEPIPELINE`` for the ``Type`` property, don't specify this property. For all of the other types, you must specify ``Location`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def report_build_status(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set to true to report the status of a build's start and finish to your source provider.

            This option is valid only when your source provider is GitHub, GitHub Enterprise, GitLab, GitLab Self Managed, or Bitbucket. If this is set and you use a different source provider, an ``invalidInputException`` is thrown.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-reportbuildstatus
            '''
            result = self._values.get("report_build_status")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def source_identifier(self) -> typing.Optional[builtins.str]:
            '''An identifier for this project source.

            The identifier can only contain alphanumeric characters and underscores, and must be less than 128 characters in length.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-sourceidentifier
            '''
            result = self._values.get("source_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of repository that contains the source code to be built. Valid values include:.

            - ``BITBUCKET`` : The source code is in a Bitbucket repository.
            - ``CODECOMMIT`` : The source code is in an CodeCommit repository.
            - ``CODEPIPELINE`` : The source code settings are specified in the source action of a pipeline in CodePipeline.
            - ``GITHUB`` : The source code is in a GitHub repository.
            - ``GITHUB_ENTERPRISE`` : The source code is in a GitHub Enterprise Server repository.
            - ``GITLAB`` : The source code is in a GitLab repository.
            - ``GITLAB_SELF_MANAGED`` : The source code is in a self-managed GitLab repository.
            - ``NO_SOURCE`` : The project does not have input source code.
            - ``S3`` : The source code is in an Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnets": "subnets",
            "vpc_id": "vpcId",
        },
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
            vpc_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``VpcConfig`` is a property of the `AWS::CodeBuild::Project <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html>`_ resource that enable AWS CodeBuild to access resources in an Amazon VPC. For more information, see `Use AWS CodeBuild with Amazon Virtual Private Cloud <https://docs.aws.amazon.com/codebuild/latest/userguide/vpc-support.html>`_ in the *AWS CodeBuild User Guide* .

            :param security_group_ids: A list of one or more security groups IDs in your Amazon VPC. The maximum count is 5.
            :param subnets: A list of one or more subnet IDs in your Amazon VPC. The maximum count is 16.
            :param vpc_id: The ID of the Amazon VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                vpc_config_property = codebuild_mixins.CfnProjectPropsMixin.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnets=["subnets"],
                    vpc_id="vpcId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__92a14847fda0410dea4a1cdcc706a5efba0052168e0ce29f09c25309636d6424)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnets is not None:
                self._values["subnets"] = subnets
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of one or more security groups IDs in your Amazon VPC.

            The maximum count is 5.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-vpcconfig.html#cfn-codebuild-project-vpcconfig-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of one or more subnet IDs in your Amazon VPC.

            The maximum count is 16.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-vpcconfig.html#cfn-codebuild-project-vpcconfig-subnets
            '''
            result = self._values.get("subnets")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the Amazon VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-vpcconfig.html#cfn-codebuild-project-vpcconfig-vpcid
            '''
            result = self._values.get("vpc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnProjectPropsMixin.WebhookFilterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exclude_matched_pattern": "excludeMatchedPattern",
            "pattern": "pattern",
            "type": "type",
        },
    )
    class WebhookFilterProperty:
        def __init__(
            self,
            *,
            exclude_matched_pattern: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            pattern: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``WebhookFilter`` is a structure of the ``FilterGroups`` property on the `AWS CodeBuild Project ProjectTriggers <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projecttriggers.html>`_ property type that specifies which webhooks trigger an AWS CodeBuild build.

            .. epigraph::

               The Webhook feature isn't available in AWS CloudFormation for GitHub Enterprise projects. Use the AWS CLI or AWS CodeBuild console to create the webhook.

            :param exclude_matched_pattern: Used to indicate that the ``pattern`` determines which webhook events do not trigger a build. If true, then a webhook event that does not match the ``pattern`` triggers a build. If false, then a webhook event that matches the ``pattern`` triggers a build.
            :param pattern: For a ``WebHookFilter`` that uses ``EVENT`` type, a comma-separated string that specifies one or more events. For example, the webhook filter ``PUSH, PULL_REQUEST_CREATED, PULL_REQUEST_UPDATED`` allows all push, pull request created, and pull request updated events to trigger a build. For a ``WebHookFilter`` that uses any of the other filter types, a regular expression pattern. For example, a ``WebHookFilter`` that uses ``HEAD_REF`` for its ``type`` and the pattern ``^refs/heads/`` triggers a build when the head reference is a branch with a reference name ``refs/heads/branch-name`` .
            :param type: The type of webhook filter. There are 11 webhook filter types: ``EVENT`` , ``ACTOR_ACCOUNT_ID`` , ``HEAD_REF`` , ``BASE_REF`` , ``FILE_PATH`` , ``COMMIT_MESSAGE`` , ``TAG_NAME`` , ``RELEASE_NAME`` , ``REPOSITORY_NAME`` , ``ORGANIZATION_NAME`` , and ``WORKFLOW_NAME`` . - EVENT - A webhook event triggers a build when the provided ``pattern`` matches one of nine event types: ``PUSH`` , ``PULL_REQUEST_CREATED`` , ``PULL_REQUEST_UPDATED`` , ``PULL_REQUEST_CLOSED`` , ``PULL_REQUEST_REOPENED`` , ``PULL_REQUEST_MERGED`` , ``RELEASED`` , ``PRERELEASED`` , and ``WORKFLOW_JOB_QUEUED`` . The ``EVENT`` patterns are specified as a comma-separated string. For example, ``PUSH, PULL_REQUEST_CREATED, PULL_REQUEST_UPDATED`` filters all push, pull request created, and pull request updated events. .. epigraph:: Types ``PULL_REQUEST_REOPENED`` and ``WORKFLOW_JOB_QUEUED`` work with GitHub and GitHub Enterprise only. Types ``RELEASED`` and ``PRERELEASED`` work with GitHub only. - ACTOR_ACCOUNT_ID - A webhook event triggers a build when a GitHub, GitHub Enterprise, or Bitbucket account ID matches the regular expression ``pattern`` . - HEAD_REF - A webhook event triggers a build when the head reference matches the regular expression ``pattern`` . For example, ``refs/heads/branch-name`` and ``refs/tags/tag-name`` . .. epigraph:: Works with GitHub and GitHub Enterprise push, GitHub and GitHub Enterprise pull request, Bitbucket push, and Bitbucket pull request events. - BASE_REF - A webhook event triggers a build when the base reference matches the regular expression ``pattern`` . For example, ``refs/heads/branch-name`` . .. epigraph:: Works with pull request events only. - FILE_PATH - A webhook triggers a build when the path of a changed file matches the regular expression ``pattern`` . .. epigraph:: Works with push and pull request events only. - COMMIT_MESSAGE - A webhook triggers a build when the head commit message matches the regular expression ``pattern`` . .. epigraph:: Works with push and pull request events only. - TAG_NAME - A webhook triggers a build when the tag name of the release matches the regular expression ``pattern`` . .. epigraph:: Works with ``RELEASED`` and ``PRERELEASED`` events only. - RELEASE_NAME - A webhook triggers a build when the release name matches the regular expression ``pattern`` . .. epigraph:: Works with ``RELEASED`` and ``PRERELEASED`` events only. - REPOSITORY_NAME - A webhook triggers a build when the repository name matches the regular expression ``pattern`` . .. epigraph:: Works with GitHub global or organization webhooks only. - ORGANIZATION_NAME - A webhook triggers a build when the organization name matches the regular expression ``pattern`` . .. epigraph:: Works with GitHub global webhooks only. - WORKFLOW_NAME - A webhook triggers a build when the workflow name matches the regular expression ``pattern`` . .. epigraph:: Works with ``WORKFLOW_JOB_QUEUED`` events only. > For CodeBuild-hosted Buildkite runner builds, WORKFLOW_NAME filters will filter by pipeline name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-webhookfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                webhook_filter_property = codebuild_mixins.CfnProjectPropsMixin.WebhookFilterProperty(
                    exclude_matched_pattern=False,
                    pattern="pattern",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ba7aa0d880fe9292dcc53f3e1856f4f5926d808e9666b1e802a2736aff05be45)
                check_type(argname="argument exclude_matched_pattern", value=exclude_matched_pattern, expected_type=type_hints["exclude_matched_pattern"])
                check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclude_matched_pattern is not None:
                self._values["exclude_matched_pattern"] = exclude_matched_pattern
            if pattern is not None:
                self._values["pattern"] = pattern
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def exclude_matched_pattern(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Used to indicate that the ``pattern`` determines which webhook events do not trigger a build.

            If true, then a webhook event that does not match the ``pattern`` triggers a build. If false, then a webhook event that matches the ``pattern`` triggers a build.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-webhookfilter.html#cfn-codebuild-project-webhookfilter-excludematchedpattern
            '''
            result = self._values.get("exclude_matched_pattern")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def pattern(self) -> typing.Optional[builtins.str]:
            '''For a ``WebHookFilter`` that uses ``EVENT`` type, a comma-separated string that specifies one or more events.

            For example, the webhook filter ``PUSH, PULL_REQUEST_CREATED, PULL_REQUEST_UPDATED`` allows all push, pull request created, and pull request updated events to trigger a build.

            For a ``WebHookFilter`` that uses any of the other filter types, a regular expression pattern. For example, a ``WebHookFilter`` that uses ``HEAD_REF`` for its ``type`` and the pattern ``^refs/heads/`` triggers a build when the head reference is a branch with a reference name ``refs/heads/branch-name`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-webhookfilter.html#cfn-codebuild-project-webhookfilter-pattern
            '''
            result = self._values.get("pattern")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of webhook filter.

            There are 11 webhook filter types: ``EVENT`` , ``ACTOR_ACCOUNT_ID`` , ``HEAD_REF`` , ``BASE_REF`` , ``FILE_PATH`` , ``COMMIT_MESSAGE`` , ``TAG_NAME`` , ``RELEASE_NAME`` , ``REPOSITORY_NAME`` , ``ORGANIZATION_NAME`` , and ``WORKFLOW_NAME`` .

            - EVENT
            - A webhook event triggers a build when the provided ``pattern`` matches one of nine event types: ``PUSH`` , ``PULL_REQUEST_CREATED`` , ``PULL_REQUEST_UPDATED`` , ``PULL_REQUEST_CLOSED`` , ``PULL_REQUEST_REOPENED`` , ``PULL_REQUEST_MERGED`` , ``RELEASED`` , ``PRERELEASED`` , and ``WORKFLOW_JOB_QUEUED`` . The ``EVENT`` patterns are specified as a comma-separated string. For example, ``PUSH, PULL_REQUEST_CREATED, PULL_REQUEST_UPDATED`` filters all push, pull request created, and pull request updated events.

            .. epigraph::

               Types ``PULL_REQUEST_REOPENED`` and ``WORKFLOW_JOB_QUEUED`` work with GitHub and GitHub Enterprise only. Types ``RELEASED`` and ``PRERELEASED`` work with GitHub only.

            - ACTOR_ACCOUNT_ID
            - A webhook event triggers a build when a GitHub, GitHub Enterprise, or Bitbucket account ID matches the regular expression ``pattern`` .
            - HEAD_REF
            - A webhook event triggers a build when the head reference matches the regular expression ``pattern`` . For example, ``refs/heads/branch-name`` and ``refs/tags/tag-name`` .

            .. epigraph::

               Works with GitHub and GitHub Enterprise push, GitHub and GitHub Enterprise pull request, Bitbucket push, and Bitbucket pull request events.

            - BASE_REF
            - A webhook event triggers a build when the base reference matches the regular expression ``pattern`` . For example, ``refs/heads/branch-name`` .

            .. epigraph::

               Works with pull request events only.

            - FILE_PATH
            - A webhook triggers a build when the path of a changed file matches the regular expression ``pattern`` .

            .. epigraph::

               Works with push and pull request events only.

            - COMMIT_MESSAGE
            - A webhook triggers a build when the head commit message matches the regular expression ``pattern`` .

            .. epigraph::

               Works with push and pull request events only.

            - TAG_NAME
            - A webhook triggers a build when the tag name of the release matches the regular expression ``pattern`` .

            .. epigraph::

               Works with ``RELEASED`` and ``PRERELEASED`` events only.

            - RELEASE_NAME
            - A webhook triggers a build when the release name matches the regular expression ``pattern`` .

            .. epigraph::

               Works with ``RELEASED`` and ``PRERELEASED`` events only.

            - REPOSITORY_NAME
            - A webhook triggers a build when the repository name matches the regular expression ``pattern`` .

            .. epigraph::

               Works with GitHub global or organization webhooks only.

            - ORGANIZATION_NAME
            - A webhook triggers a build when the organization name matches the regular expression ``pattern`` .

            .. epigraph::

               Works with GitHub global webhooks only.

            - WORKFLOW_NAME
            - A webhook triggers a build when the workflow name matches the regular expression ``pattern`` .

            .. epigraph::

               Works with ``WORKFLOW_JOB_QUEUED`` events only. > For CodeBuild-hosted Buildkite runner builds, WORKFLOW_NAME filters will filter by pipeline name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-webhookfilter.html#cfn-codebuild-project-webhookfilter-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebhookFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnReportGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "delete_reports": "deleteReports",
        "export_config": "exportConfig",
        "name": "name",
        "tags": "tags",
        "type": "type",
    },
)
class CfnReportGroupMixinProps:
    def __init__(
        self,
        *,
        delete_reports: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        export_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReportGroupPropsMixin.ReportExportConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnReportGroupPropsMixin.

        :param delete_reports: When deleting a report group, specifies if reports within the report group should be deleted. - **true** - Deletes any reports that belong to the report group before deleting the report group. - **false** - You must delete any reports in the report group. This is the default value. If you delete a report group that contains one or more reports, an exception is thrown.
        :param export_config: Information about the destination where the raw data of this ``ReportGroup`` is exported.
        :param name: The name of the ``ReportGroup`` .
        :param tags: A list of tag key and value pairs associated with this report group. These tags are available for use by AWS services that support AWS CodeBuild report group tags.
        :param type: The type of the ``ReportGroup`` . This can be one of the following values:. - **CODE_COVERAGE** - The report group contains code coverage reports. - **TEST** - The report group contains test reports.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
            
            cfn_report_group_mixin_props = codebuild_mixins.CfnReportGroupMixinProps(
                delete_reports=False,
                export_config=codebuild_mixins.CfnReportGroupPropsMixin.ReportExportConfigProperty(
                    export_config_type="exportConfigType",
                    s3_destination=codebuild_mixins.CfnReportGroupPropsMixin.S3ReportExportConfigProperty(
                        bucket="bucket",
                        bucket_owner="bucketOwner",
                        encryption_disabled=False,
                        encryption_key="encryptionKey",
                        packaging="packaging",
                        path="path"
                    )
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4be03dd935e39d0a2121ba7806f0c696b6a51ec2cc578074642e7d7b86837a0)
            check_type(argname="argument delete_reports", value=delete_reports, expected_type=type_hints["delete_reports"])
            check_type(argname="argument export_config", value=export_config, expected_type=type_hints["export_config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delete_reports is not None:
            self._values["delete_reports"] = delete_reports
        if export_config is not None:
            self._values["export_config"] = export_config
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def delete_reports(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''When deleting a report group, specifies if reports within the report group should be deleted.

        - **true** - Deletes any reports that belong to the report group before deleting the report group.
        - **false** - You must delete any reports in the report group. This is the default value. If you delete a report group that contains one or more reports, an exception is thrown.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-deletereports
        '''
        result = self._values.get("delete_reports")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def export_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReportGroupPropsMixin.ReportExportConfigProperty"]]:
        '''Information about the destination where the raw data of this ``ReportGroup`` is exported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-exportconfig
        '''
        result = self._values.get("export_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReportGroupPropsMixin.ReportExportConfigProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the ``ReportGroup`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tag key and value pairs associated with this report group.

        These tags are available for use by AWS services that support AWS CodeBuild report group tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the ``ReportGroup`` . This can be one of the following values:.

        - **CODE_COVERAGE** - The report group contains code coverage reports.
        - **TEST** - The report group contains test reports.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html#cfn-codebuild-reportgroup-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReportGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnReportGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnReportGroupPropsMixin",
):
    '''Represents a report group.

    A report group contains a collection of reports.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-reportgroup.html
    :cloudformationResource: AWS::CodeBuild::ReportGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
        
        cfn_report_group_props_mixin = codebuild_mixins.CfnReportGroupPropsMixin(codebuild_mixins.CfnReportGroupMixinProps(
            delete_reports=False,
            export_config=codebuild_mixins.CfnReportGroupPropsMixin.ReportExportConfigProperty(
                export_config_type="exportConfigType",
                s3_destination=codebuild_mixins.CfnReportGroupPropsMixin.S3ReportExportConfigProperty(
                    bucket="bucket",
                    bucket_owner="bucketOwner",
                    encryption_disabled=False,
                    encryption_key="encryptionKey",
                    packaging="packaging",
                    path="path"
                )
            ),
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnReportGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CodeBuild::ReportGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7efa4348141238565831767a5a935a2d089a3c035e6e14f7e28d03ce80ddf8d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be69a99db22499f2d2c0f00617199d85f784c01b53779dba8ba346c8371411ce)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__837d462e3388e637561e6a054814907e86eca8c4cb4b3db991a14c285d5e15f6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnReportGroupMixinProps:
        return typing.cast(CfnReportGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnReportGroupPropsMixin.ReportExportConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "export_config_type": "exportConfigType",
            "s3_destination": "s3Destination",
        },
    )
    class ReportExportConfigProperty:
        def __init__(
            self,
            *,
            export_config_type: typing.Optional[builtins.str] = None,
            s3_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReportGroupPropsMixin.S3ReportExportConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about the location where the run of a report is exported.

            :param export_config_type: The export configuration type. Valid values are:. - ``S3`` : The report results are exported to an S3 bucket. - ``NO_EXPORT`` : The report results are not exported.
            :param s3_destination: A ``S3ReportExportConfig`` object that contains information about the S3 bucket where the run of a report is exported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-reportexportconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                report_export_config_property = codebuild_mixins.CfnReportGroupPropsMixin.ReportExportConfigProperty(
                    export_config_type="exportConfigType",
                    s3_destination=codebuild_mixins.CfnReportGroupPropsMixin.S3ReportExportConfigProperty(
                        bucket="bucket",
                        bucket_owner="bucketOwner",
                        encryption_disabled=False,
                        encryption_key="encryptionKey",
                        packaging="packaging",
                        path="path"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__56f1354bc978823be7f42a8f78628f82f36bf33f0eed85178cc7d484185af5c6)
                check_type(argname="argument export_config_type", value=export_config_type, expected_type=type_hints["export_config_type"])
                check_type(argname="argument s3_destination", value=s3_destination, expected_type=type_hints["s3_destination"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if export_config_type is not None:
                self._values["export_config_type"] = export_config_type
            if s3_destination is not None:
                self._values["s3_destination"] = s3_destination

        @builtins.property
        def export_config_type(self) -> typing.Optional[builtins.str]:
            '''The export configuration type. Valid values are:.

            - ``S3`` : The report results are exported to an S3 bucket.
            - ``NO_EXPORT`` : The report results are not exported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-reportexportconfig.html#cfn-codebuild-reportgroup-reportexportconfig-exportconfigtype
            '''
            result = self._values.get("export_config_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReportGroupPropsMixin.S3ReportExportConfigProperty"]]:
            '''A ``S3ReportExportConfig`` object that contains information about the S3 bucket where the run of a report is exported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-reportexportconfig.html#cfn-codebuild-reportgroup-reportexportconfig-s3destination
            '''
            result = self._values.get("s3_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReportGroupPropsMixin.S3ReportExportConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReportExportConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnReportGroupPropsMixin.S3ReportExportConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "bucket_owner": "bucketOwner",
            "encryption_disabled": "encryptionDisabled",
            "encryption_key": "encryptionKey",
            "packaging": "packaging",
            "path": "path",
        },
    )
    class S3ReportExportConfigProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            bucket_owner: typing.Optional[builtins.str] = None,
            encryption_disabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            encryption_key: typing.Optional[builtins.str] = None,
            packaging: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the S3 bucket where the raw data of a report are exported.

            :param bucket: The name of the S3 bucket where the raw data of a report are exported.
            :param bucket_owner: The AWS account identifier of the owner of the Amazon S3 bucket. This allows report data to be exported to an Amazon S3 bucket that is owned by an account other than the account running the build.
            :param encryption_disabled: A boolean value that specifies if the results of a report are encrypted.
            :param encryption_key: The encryption key for the report's encrypted raw data.
            :param packaging: The type of build output artifact to create. Valid values include:. - ``NONE`` : CodeBuild creates the raw data in the output bucket. This is the default if packaging is not specified. - ``ZIP`` : CodeBuild creates a ZIP file with the raw data in the output bucket.
            :param path: The path to the exported report's raw data results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-s3reportexportconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
                
                s3_report_export_config_property = codebuild_mixins.CfnReportGroupPropsMixin.S3ReportExportConfigProperty(
                    bucket="bucket",
                    bucket_owner="bucketOwner",
                    encryption_disabled=False,
                    encryption_key="encryptionKey",
                    packaging="packaging",
                    path="path"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__46cf47a2bdc2339570124ccef0aab2f050ef9892fe386e531ad7d2991a921815)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument bucket_owner", value=bucket_owner, expected_type=type_hints["bucket_owner"])
                check_type(argname="argument encryption_disabled", value=encryption_disabled, expected_type=type_hints["encryption_disabled"])
                check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
                check_type(argname="argument packaging", value=packaging, expected_type=type_hints["packaging"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if bucket_owner is not None:
                self._values["bucket_owner"] = bucket_owner
            if encryption_disabled is not None:
                self._values["encryption_disabled"] = encryption_disabled
            if encryption_key is not None:
                self._values["encryption_key"] = encryption_key
            if packaging is not None:
                self._values["packaging"] = packaging
            if path is not None:
                self._values["path"] = path

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The name of the S3 bucket where the raw data of a report are exported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-s3reportexportconfig.html#cfn-codebuild-reportgroup-s3reportexportconfig-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_owner(self) -> typing.Optional[builtins.str]:
            '''The AWS account identifier of the owner of the Amazon S3 bucket.

            This allows report data to be exported to an Amazon S3 bucket that is owned by an account other than the account running the build.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-s3reportexportconfig.html#cfn-codebuild-reportgroup-s3reportexportconfig-bucketowner
            '''
            result = self._values.get("bucket_owner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_disabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A boolean value that specifies if the results of a report are encrypted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-s3reportexportconfig.html#cfn-codebuild-reportgroup-s3reportexportconfig-encryptiondisabled
            '''
            result = self._values.get("encryption_disabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def encryption_key(self) -> typing.Optional[builtins.str]:
            '''The encryption key for the report's encrypted raw data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-s3reportexportconfig.html#cfn-codebuild-reportgroup-s3reportexportconfig-encryptionkey
            '''
            result = self._values.get("encryption_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def packaging(self) -> typing.Optional[builtins.str]:
            '''The type of build output artifact to create. Valid values include:.

            - ``NONE`` : CodeBuild creates the raw data in the output bucket. This is the default if packaging is not specified.
            - ``ZIP`` : CodeBuild creates a ZIP file with the raw data in the output bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-s3reportexportconfig.html#cfn-codebuild-reportgroup-s3reportexportconfig-packaging
            '''
            result = self._values.get("packaging")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The path to the exported report's raw data results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-reportgroup-s3reportexportconfig.html#cfn-codebuild-reportgroup-s3reportexportconfig-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ReportExportConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnSourceCredentialMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auth_type": "authType",
        "server_type": "serverType",
        "token": "token",
        "username": "username",
    },
)
class CfnSourceCredentialMixinProps:
    def __init__(
        self,
        *,
        auth_type: typing.Optional[builtins.str] = None,
        server_type: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSourceCredentialPropsMixin.

        :param auth_type: The type of authentication used by the credentials. Valid options are OAUTH, BASIC_AUTH, PERSONAL_ACCESS_TOKEN, CODECONNECTIONS, or SECRETS_MANAGER.
        :param server_type: The type of source provider. The valid options are GITHUB, GITHUB_ENTERPRISE, GITLAB, GITLAB_SELF_MANAGED, or BITBUCKET.
        :param token: For GitHub or GitHub Enterprise, this is the personal access token. For Bitbucket, this is either the access token or the app password. For the ``authType`` CODECONNECTIONS, this is the ``connectionArn`` . For the ``authType`` SECRETS_MANAGER, this is the ``secretArn`` .
        :param username: The Bitbucket username when the ``authType`` is BASIC_AUTH. This parameter is not valid for other types of source providers or connections.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
            
            cfn_source_credential_mixin_props = codebuild_mixins.CfnSourceCredentialMixinProps(
                auth_type="authType",
                server_type="serverType",
                token="token",
                username="username"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__153db2d924c969de8a3e67102422e9c02145d0c8e20ca5def874b4ad5cacea49)
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument server_type", value=server_type, expected_type=type_hints["server_type"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if server_type is not None:
            self._values["server_type"] = server_type
        if token is not None:
            self._values["token"] = token
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''The type of authentication used by the credentials.

        Valid options are OAUTH, BASIC_AUTH, PERSONAL_ACCESS_TOKEN, CODECONNECTIONS, or SECRETS_MANAGER.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-authtype
        '''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_type(self) -> typing.Optional[builtins.str]:
        '''The type of source provider.

        The valid options are GITHUB, GITHUB_ENTERPRISE, GITLAB, GITLAB_SELF_MANAGED, or BITBUCKET.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-servertype
        '''
        result = self._values.get("server_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''For GitHub or GitHub Enterprise, this is the personal access token.

        For Bitbucket, this is either the access token or the app password. For the ``authType`` CODECONNECTIONS, this is the ``connectionArn`` . For the ``authType`` SECRETS_MANAGER, this is the ``secretArn`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-token
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The Bitbucket username when the ``authType`` is BASIC_AUTH.

        This parameter is not valid for other types of source providers or connections.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-username
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSourceCredentialMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSourceCredentialPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_codebuild.mixins.CfnSourceCredentialPropsMixin",
):
    '''Information about the credentials for a GitHub, GitHub Enterprise, or Bitbucket repository.

    We strongly recommend that you use AWS Secrets Manager to store your credentials. If you use Secrets Manager , you must have secrets in your secrets manager. For more information, see `Using Dynamic References to Specify Template Values <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html#dynamic-references-secretsmanager>`_ .
    .. epigraph::

       For security purposes, do not use plain text in your CloudFormation template to store your credentials.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html
    :cloudformationResource: AWS::CodeBuild::SourceCredential
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_codebuild import mixins as codebuild_mixins
        
        cfn_source_credential_props_mixin = codebuild_mixins.CfnSourceCredentialPropsMixin(codebuild_mixins.CfnSourceCredentialMixinProps(
            auth_type="authType",
            server_type="serverType",
            token="token",
            username="username"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSourceCredentialMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CodeBuild::SourceCredential``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b51c65f3e0b21ec8ebc5908adcf142cb49ead0057b525a29d7379d3ceae1925)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c21419d578ddbde2f595cfd246cb80561272be8b7e668bb9ac0b317d21a78e05)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f74e8e74ce4d58935be431538b003126dc62deee811734f734ed9a7f91b4d73)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSourceCredentialMixinProps:
        return typing.cast(CfnSourceCredentialMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnFleetMixinProps",
    "CfnFleetPropsMixin",
    "CfnProjectMixinProps",
    "CfnProjectPropsMixin",
    "CfnReportGroupMixinProps",
    "CfnReportGroupPropsMixin",
    "CfnSourceCredentialMixinProps",
    "CfnSourceCredentialPropsMixin",
]

publication.publish()

def _typecheckingstub__6678bade3381671cdb1bbd3e6a97e3ce64fda51990f47ab419711fe21bf8d8d3(
    *,
    base_capacity: typing.Optional[jsii.Number] = None,
    compute_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.ComputeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    compute_type: typing.Optional[builtins.str] = None,
    environment_type: typing.Optional[builtins.str] = None,
    fleet_proxy_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.ProxyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    fleet_service_role: typing.Optional[builtins.str] = None,
    fleet_vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    overflow_behavior: typing.Optional[builtins.str] = None,
    scaling_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.ScalingConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718c89f510f8f36254066217c006415cf2775f8e4294a7fd3b5d07237b730f99(
    props: typing.Union[CfnFleetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe16a895a96c60080d533e506ce9f66058e7a5085eeba733b5d3262f0793b54(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35073713375292328621156a58409c2cc65795d1292fa03c868de27c6da6f24a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36496bf890fb5555997aaa5bcb4f405a0df84fce23768fa8d1796ad346e6c347(
    *,
    disk: typing.Optional[jsii.Number] = None,
    instance_type: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    memory: typing.Optional[jsii.Number] = None,
    v_cpu: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f21ac34db3816fd5c46ec904caf734d78caa5eb0899fc7c3a07b09ff4164b6e(
    *,
    effect: typing.Optional[builtins.str] = None,
    entities: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fff32fccca2ecaa6f3ab0abb011879cbb4f3c5861cf2b3237eac252e387e4da(
    *,
    default_behavior: typing.Optional[builtins.str] = None,
    ordered_proxy_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.FleetProxyRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be2b2ed8505f87c03005008bc0d1f19baba425d999a32dc6e29e02596cedc477(
    *,
    max_capacity: typing.Optional[jsii.Number] = None,
    scaling_type: typing.Optional[builtins.str] = None,
    target_tracking_scaling_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.TargetTrackingScalingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9bd1dbca62fae1e55c2e132857619e77e611696c879d74538dab037676de48(
    *,
    metric_type: typing.Optional[builtins.str] = None,
    target_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ecb007eb53ddbd27387fb5bebdc46bd5df61d257791aa98e32b84078e1bea6b(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03dcb5ea218ae77f7f0a499b9b551c15ff81dab0a63c28f507fb7d04dfe6be04(
    *,
    artifacts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.ArtifactsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    auto_retry_limit: typing.Optional[jsii.Number] = None,
    badge_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    build_batch_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.ProjectBuildBatchConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cache: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.ProjectCacheProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    concurrent_build_limit: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.EnvironmentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    file_system_locations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.ProjectFileSystemLocationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    logs_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.LogsConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    queued_timeout_in_minutes: typing.Optional[jsii.Number] = None,
    resource_access_role: typing.Optional[builtins.str] = None,
    secondary_artifacts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.ArtifactsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    secondary_sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.SourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    secondary_source_versions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.ProjectSourceVersionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    service_role: typing.Optional[builtins.str] = None,
    source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.SourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_in_minutes: typing.Optional[jsii.Number] = None,
    triggers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.ProjectTriggersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    visibility: typing.Optional[builtins.str] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e820c4fb87defc15f1f7369a60d940aa0fc3198cfa29f64cdc7de5970d49aa03(
    props: typing.Union[CfnProjectMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a2e7bf795968abbaf9854d277d64c7af1ea3c08e9aa6a134af6129dc1acae2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735c5733d23b5f48be52c275e4628ede948c6c00a05fb658e9b02ef875176f16(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a135ac3b59f3895642ca7505b1aed677a00babe61adbc6e58dea0d55f3837e32(
    *,
    artifact_identifier: typing.Optional[builtins.str] = None,
    encryption_disabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    namespace_type: typing.Optional[builtins.str] = None,
    override_artifact_name: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    packaging: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b0dff32ec4b3300b2453ab7d0a0b6f1acdf28514b93708adc9006268a106fe7(
    *,
    compute_types_allowed: typing.Optional[typing.Sequence[builtins.str]] = None,
    maximum_builds_allowed: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a98f56da1090ea1e89b6e2a7fb26d0e5de501644a344fbf365fb81c8debe90(
    *,
    context: typing.Optional[builtins.str] = None,
    target_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd4bb2c4f79828358477c1c05f129f9d97a4b42e85af0c1e3bf5b7a1f2e1b4f(
    *,
    group_name: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__535488f59b2f039eb8b90a0bca679bb769a6faab1c65ef3fbd5d1013c992c2e5(
    *,
    compute_type: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bab9cd2b7c7243228a80d9f1258671a08a6841c0ddc864cf30b42c835cd9c93(
    *,
    certificate: typing.Optional[builtins.str] = None,
    compute_type: typing.Optional[builtins.str] = None,
    docker_server: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.DockerServerProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    environment_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    fleet: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.ProjectFleetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image: typing.Optional[builtins.str] = None,
    image_pull_credentials_type: typing.Optional[builtins.str] = None,
    privileged_mode: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    registry_credential: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.RegistryCredentialProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb7394aeaeea10758c1328f55277665c3c00485e04a53c996701ac999e8f951(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac370c31aa6c99135c2627e8f720c15c0f8d4038972e3ec23345a0426a6c6638(
    *,
    fetch_submodules: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__942868f8f1c4666aaca036001345c8a55b4485bda695304913fa1306720c926d(
    *,
    cloud_watch_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.CloudWatchLogsConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.S3LogsConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45b1fa0e682d0af5e6fa077c0bc6893e22db272022ee3a72e167e6ed575ce779(
    *,
    batch_report_mode: typing.Optional[builtins.str] = None,
    combine_artifacts: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    restrictions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.BatchRestrictionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_role: typing.Optional[builtins.str] = None,
    timeout_in_mins: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1029b48e621a58acde3ddfe58fed521bedfafbdcecc836549c65773b16f9679c(
    *,
    cache_namespace: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    modes: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fbf0ad63512fec69ddcc34266342e70ba00553896b45dec36d46a07661d801b(
    *,
    identifier: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    mount_options: typing.Optional[builtins.str] = None,
    mount_point: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ca8ac8975c78adfb642f1cefb3645b5eae62b0bc80dc0db3f8f93fb5e79b68(
    *,
    fleet_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94fe2d11da8c3414a7e1ad29f64759df534b925e1f448ece8d3f7e004a87ab04(
    *,
    source_identifier: typing.Optional[builtins.str] = None,
    source_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a82270fb8fc5b574fdd43367823cb0be400327115dea0f0debf802962be96631(
    *,
    build_type: typing.Optional[builtins.str] = None,
    filter_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.WebhookFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]]]] = None,
    pull_request_build_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.PullRequestBuildPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scope_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.ScopeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    webhook: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d65d5e1f87540f9d71c8daf3fd22d1705e998a53250f5fd4ae1b0fb70703fc1(
    *,
    approver_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    requires_comment_approval: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7435fbf0e2aa06a6a36f7347351e392f58a343a28ae50026b9cf995502a7c87c(
    *,
    credential: typing.Optional[builtins.str] = None,
    credential_provider: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8155973c9de5473419a6c78000ed49cdb6d7973d6cd9cd655a65d417bc7fc1c(
    *,
    encryption_disabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    location: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5446740b535cb89b1c8c2d3f665968f5fe41dd964ef3b1e9e2dde778d0e0cc9a(
    *,
    domain: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c68115cb903c8e13747e2f1090df2d00e9c5ab731e63324a728e2c59001618d(
    *,
    resource: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103701bb968de376f03791b4fdbaf793cbeee3000d4aa9931fe0fde434105a27(
    *,
    auth: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.SourceAuthProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    build_spec: typing.Optional[builtins.str] = None,
    build_status_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.BuildStatusConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    git_clone_depth: typing.Optional[jsii.Number] = None,
    git_submodules_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.GitSubmodulesConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    insecure_ssl: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    location: typing.Optional[builtins.str] = None,
    report_build_status: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    source_identifier: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a14847fda0410dea4a1cdcc706a5efba0052168e0ce29f09c25309636d6424(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba7aa0d880fe9292dcc53f3e1856f4f5926d808e9666b1e802a2736aff05be45(
    *,
    exclude_matched_pattern: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    pattern: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4be03dd935e39d0a2121ba7806f0c696b6a51ec2cc578074642e7d7b86837a0(
    *,
    delete_reports: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    export_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReportGroupPropsMixin.ReportExportConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7efa4348141238565831767a5a935a2d089a3c035e6e14f7e28d03ce80ddf8d4(
    props: typing.Union[CfnReportGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be69a99db22499f2d2c0f00617199d85f784c01b53779dba8ba346c8371411ce(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__837d462e3388e637561e6a054814907e86eca8c4cb4b3db991a14c285d5e15f6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56f1354bc978823be7f42a8f78628f82f36bf33f0eed85178cc7d484185af5c6(
    *,
    export_config_type: typing.Optional[builtins.str] = None,
    s3_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReportGroupPropsMixin.S3ReportExportConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46cf47a2bdc2339570124ccef0aab2f050ef9892fe386e531ad7d2991a921815(
    *,
    bucket: typing.Optional[builtins.str] = None,
    bucket_owner: typing.Optional[builtins.str] = None,
    encryption_disabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    encryption_key: typing.Optional[builtins.str] = None,
    packaging: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__153db2d924c969de8a3e67102422e9c02145d0c8e20ca5def874b4ad5cacea49(
    *,
    auth_type: typing.Optional[builtins.str] = None,
    server_type: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b51c65f3e0b21ec8ebc5908adcf142cb49ead0057b525a29d7379d3ceae1925(
    props: typing.Union[CfnSourceCredentialMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c21419d578ddbde2f595cfd246cb80561272be8b7e668bb9ac0b317d21a78e05(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f74e8e74ce4d58935be431538b003126dc62deee811734f734ed9a7f91b4d73(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
