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
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFarmMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "display_name": "displayName",
        "kms_key_arn": "kmsKeyArn",
        "tags": "tags",
    },
)
class CfnFarmMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFarmPropsMixin.

        :param description: A description of the farm that helps identify what the farm is used for. .. epigraph:: This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field. Default: - ""
        :param display_name: The display name of the farm. .. epigraph:: This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.
        :param kms_key_arn: The ARN for the KMS key.
        :param tags: The tags to add to your farm. Each tag consists of a tag key and a tag value. Tag keys and values are both required, but tag values can be empty strings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-farm.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
            
            cfn_farm_mixin_props = deadline_mixins.CfnFarmMixinProps(
                description="description",
                display_name="displayName",
                kms_key_arn="kmsKeyArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2df8ba71ae997ba65799f5ac27c965b17eafc7116b60ea7ea7cda67fb4dfb2a)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the farm that helps identify what the farm is used for.

        .. epigraph::

           This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.

        :default: - ""

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-farm.html#cfn-deadline-farm-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the farm.

        .. epigraph::

           This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-farm.html#cfn-deadline-farm-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN for the KMS key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-farm.html#cfn-deadline-farm-kmskeyarn
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to add to your farm.

        Each tag consists of a tag key and a tag value. Tag keys and values are both required, but tag values can be empty strings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-farm.html#cfn-deadline-farm-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFarmMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFarmPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFarmPropsMixin",
):
    '''Creates a farm to allow space for queues and fleets.

    Farms are the space where the components of your renders gather and are pieced together in the cloud. Farms contain budgets and allow you to enforce permissions. Deadline Cloud farms are a useful container for large projects.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-farm.html
    :cloudformationResource: AWS::Deadline::Farm
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
        
        cfn_farm_props_mixin = deadline_mixins.CfnFarmPropsMixin(deadline_mixins.CfnFarmMixinProps(
            description="description",
            display_name="displayName",
            kms_key_arn="kmsKeyArn",
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
        props: typing.Union[CfnFarmMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Deadline::Farm``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73364b54e637816086e29282ea6d68de797186b04e8038a2e3a861c1774aee95)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69b5ca645657d0411362cf8732895d2bc667d29e7bb3faaec4779c9162288ef2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe3992a85be6840d9b880f5bcf70b9dcedb375651ab91ae85d344c253da4dc68)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFarmMixinProps:
        return typing.cast(CfnFarmMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFleetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration": "configuration",
        "description": "description",
        "display_name": "displayName",
        "farm_id": "farmId",
        "host_configuration": "hostConfiguration",
        "max_worker_count": "maxWorkerCount",
        "min_worker_count": "minWorkerCount",
        "role_arn": "roleArn",
        "tags": "tags",
    },
)
class CfnFleetMixinProps:
    def __init__(
        self,
        *,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.FleetConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        farm_id: typing.Optional[builtins.str] = None,
        host_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.HostConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        max_worker_count: typing.Optional[jsii.Number] = None,
        min_worker_count: typing.Optional[jsii.Number] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFleetPropsMixin.

        :param configuration: The configuration details for the fleet.
        :param description: A description that helps identify what the fleet is used for. .. epigraph:: This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field. Default: - ""
        :param display_name: The display name of the fleet summary to update. .. epigraph:: This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.
        :param farm_id: The farm ID.
        :param host_configuration: Provides a script that runs as a worker is starting up that you can use to provide additional configuration for workers in your fleet. To remove a script from a fleet, use the `UpdateFleet <https://docs.aws.amazon.com/deadline-cloud/latest/APIReference/API_UpdateFleet.html>`_ operation with the ``hostConfiguration`` ``scriptBody`` parameter set to an empty string ("").
        :param max_worker_count: The maximum number of workers specified in the fleet.
        :param min_worker_count: The minimum number of workers in the fleet. Default: - 0
        :param role_arn: The IAM role that workers in the fleet use when processing jobs.
        :param tags: The tags to add to your fleet. Each tag consists of a tag key and a tag value. Tag keys and values are both required, but tag values can be empty strings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-fleet.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
            
            cfn_fleet_mixin_props = deadline_mixins.CfnFleetMixinProps(
                configuration=deadline_mixins.CfnFleetPropsMixin.FleetConfigurationProperty(
                    customer_managed=deadline_mixins.CfnFleetPropsMixin.CustomerManagedFleetConfigurationProperty(
                        mode="mode",
                        storage_profile_id="storageProfileId",
                        tag_propagation_mode="tagPropagationMode",
                        worker_capabilities=deadline_mixins.CfnFleetPropsMixin.CustomerManagedWorkerCapabilitiesProperty(
                            accelerator_count=deadline_mixins.CfnFleetPropsMixin.AcceleratorCountRangeProperty(
                                max=123,
                                min=123
                            ),
                            accelerator_total_memory_mi_b=deadline_mixins.CfnFleetPropsMixin.AcceleratorTotalMemoryMiBRangeProperty(
                                max=123,
                                min=123
                            ),
                            accelerator_types=["acceleratorTypes"],
                            cpu_architecture_type="cpuArchitectureType",
                            custom_amounts=[deadline_mixins.CfnFleetPropsMixin.FleetAmountCapabilityProperty(
                                max=123,
                                min=123,
                                name="name"
                            )],
                            custom_attributes=[deadline_mixins.CfnFleetPropsMixin.FleetAttributeCapabilityProperty(
                                name="name",
                                values=["values"]
                            )],
                            memory_mi_b=deadline_mixins.CfnFleetPropsMixin.MemoryMiBRangeProperty(
                                max=123,
                                min=123
                            ),
                            os_family="osFamily",
                            v_cpu_count=deadline_mixins.CfnFleetPropsMixin.VCpuCountRangeProperty(
                                max=123,
                                min=123
                            )
                        )
                    ),
                    service_managed_ec2=deadline_mixins.CfnFleetPropsMixin.ServiceManagedEc2FleetConfigurationProperty(
                        instance_capabilities=deadline_mixins.CfnFleetPropsMixin.ServiceManagedEc2InstanceCapabilitiesProperty(
                            accelerator_capabilities=deadline_mixins.CfnFleetPropsMixin.AcceleratorCapabilitiesProperty(
                                count=deadline_mixins.CfnFleetPropsMixin.AcceleratorCountRangeProperty(
                                    max=123,
                                    min=123
                                ),
                                selections=[deadline_mixins.CfnFleetPropsMixin.AcceleratorSelectionProperty(
                                    name="name",
                                    runtime="runtime"
                                )]
                            ),
                            allowed_instance_types=["allowedInstanceTypes"],
                            cpu_architecture_type="cpuArchitectureType",
                            custom_amounts=[deadline_mixins.CfnFleetPropsMixin.FleetAmountCapabilityProperty(
                                max=123,
                                min=123,
                                name="name"
                            )],
                            custom_attributes=[deadline_mixins.CfnFleetPropsMixin.FleetAttributeCapabilityProperty(
                                name="name",
                                values=["values"]
                            )],
                            excluded_instance_types=["excludedInstanceTypes"],
                            memory_mi_b=deadline_mixins.CfnFleetPropsMixin.MemoryMiBRangeProperty(
                                max=123,
                                min=123
                            ),
                            os_family="osFamily",
                            root_ebs_volume=deadline_mixins.CfnFleetPropsMixin.Ec2EbsVolumeProperty(
                                iops=123,
                                size_gi_b=123,
                                throughput_mi_b=123
                            ),
                            v_cpu_count=deadline_mixins.CfnFleetPropsMixin.VCpuCountRangeProperty(
                                max=123,
                                min=123
                            )
                        ),
                        instance_market_options=deadline_mixins.CfnFleetPropsMixin.ServiceManagedEc2InstanceMarketOptionsProperty(
                            type="type"
                        ),
                        storage_profile_id="storageProfileId",
                        vpc_configuration=deadline_mixins.CfnFleetPropsMixin.VpcConfigurationProperty(
                            resource_configuration_arns=["resourceConfigurationArns"]
                        )
                    )
                ),
                description="description",
                display_name="displayName",
                farm_id="farmId",
                host_configuration=deadline_mixins.CfnFleetPropsMixin.HostConfigurationProperty(
                    script_body="scriptBody",
                    script_timeout_seconds=123
                ),
                max_worker_count=123,
                min_worker_count=123,
                role_arn="roleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d04ae7694ea50baf6f78be852c4941b3e89922a4c55f4feacd71af93d50cb861)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument farm_id", value=farm_id, expected_type=type_hints["farm_id"])
            check_type(argname="argument host_configuration", value=host_configuration, expected_type=type_hints["host_configuration"])
            check_type(argname="argument max_worker_count", value=max_worker_count, expected_type=type_hints["max_worker_count"])
            check_type(argname="argument min_worker_count", value=min_worker_count, expected_type=type_hints["min_worker_count"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration is not None:
            self._values["configuration"] = configuration
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if farm_id is not None:
            self._values["farm_id"] = farm_id
        if host_configuration is not None:
            self._values["host_configuration"] = host_configuration
        if max_worker_count is not None:
            self._values["max_worker_count"] = max_worker_count
        if min_worker_count is not None:
            self._values["min_worker_count"] = min_worker_count
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.FleetConfigurationProperty"]]:
        '''The configuration details for the fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-fleet.html#cfn-deadline-fleet-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.FleetConfigurationProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description that helps identify what the fleet is used for.

        .. epigraph::

           This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.

        :default: - ""

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-fleet.html#cfn-deadline-fleet-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the fleet summary to update.

        .. epigraph::

           This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-fleet.html#cfn-deadline-fleet-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def farm_id(self) -> typing.Optional[builtins.str]:
        '''The farm ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-fleet.html#cfn-deadline-fleet-farmid
        '''
        result = self._values.get("farm_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.HostConfigurationProperty"]]:
        '''Provides a script that runs as a worker is starting up that you can use to provide additional configuration for workers in your fleet.

        To remove a script from a fleet, use the `UpdateFleet <https://docs.aws.amazon.com/deadline-cloud/latest/APIReference/API_UpdateFleet.html>`_ operation with the ``hostConfiguration`` ``scriptBody`` parameter set to an empty string ("").

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-fleet.html#cfn-deadline-fleet-hostconfiguration
        '''
        result = self._values.get("host_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.HostConfigurationProperty"]], result)

    @builtins.property
    def max_worker_count(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of workers specified in the fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-fleet.html#cfn-deadline-fleet-maxworkercount
        '''
        result = self._values.get("max_worker_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_worker_count(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of workers in the fleet.

        :default: - 0

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-fleet.html#cfn-deadline-fleet-minworkercount
        '''
        result = self._values.get("min_worker_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The IAM role that workers in the fleet use when processing jobs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-fleet.html#cfn-deadline-fleet-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to add to your fleet.

        Each tag consists of a tag key and a tag value. Tag keys and values are both required, but tag values can be empty strings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-fleet.html#cfn-deadline-fleet-tags
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
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFleetPropsMixin",
):
    '''Creates a fleet.

    Fleets gather information relating to compute, or capacity, for renders within your farms. You can choose to manage your own capacity or opt to have fleets fully managed by Deadline Cloud.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-fleet.html
    :cloudformationResource: AWS::Deadline::Fleet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
        
        cfn_fleet_props_mixin = deadline_mixins.CfnFleetPropsMixin(deadline_mixins.CfnFleetMixinProps(
            configuration=deadline_mixins.CfnFleetPropsMixin.FleetConfigurationProperty(
                customer_managed=deadline_mixins.CfnFleetPropsMixin.CustomerManagedFleetConfigurationProperty(
                    mode="mode",
                    storage_profile_id="storageProfileId",
                    tag_propagation_mode="tagPropagationMode",
                    worker_capabilities=deadline_mixins.CfnFleetPropsMixin.CustomerManagedWorkerCapabilitiesProperty(
                        accelerator_count=deadline_mixins.CfnFleetPropsMixin.AcceleratorCountRangeProperty(
                            max=123,
                            min=123
                        ),
                        accelerator_total_memory_mi_b=deadline_mixins.CfnFleetPropsMixin.AcceleratorTotalMemoryMiBRangeProperty(
                            max=123,
                            min=123
                        ),
                        accelerator_types=["acceleratorTypes"],
                        cpu_architecture_type="cpuArchitectureType",
                        custom_amounts=[deadline_mixins.CfnFleetPropsMixin.FleetAmountCapabilityProperty(
                            max=123,
                            min=123,
                            name="name"
                        )],
                        custom_attributes=[deadline_mixins.CfnFleetPropsMixin.FleetAttributeCapabilityProperty(
                            name="name",
                            values=["values"]
                        )],
                        memory_mi_b=deadline_mixins.CfnFleetPropsMixin.MemoryMiBRangeProperty(
                            max=123,
                            min=123
                        ),
                        os_family="osFamily",
                        v_cpu_count=deadline_mixins.CfnFleetPropsMixin.VCpuCountRangeProperty(
                            max=123,
                            min=123
                        )
                    )
                ),
                service_managed_ec2=deadline_mixins.CfnFleetPropsMixin.ServiceManagedEc2FleetConfigurationProperty(
                    instance_capabilities=deadline_mixins.CfnFleetPropsMixin.ServiceManagedEc2InstanceCapabilitiesProperty(
                        accelerator_capabilities=deadline_mixins.CfnFleetPropsMixin.AcceleratorCapabilitiesProperty(
                            count=deadline_mixins.CfnFleetPropsMixin.AcceleratorCountRangeProperty(
                                max=123,
                                min=123
                            ),
                            selections=[deadline_mixins.CfnFleetPropsMixin.AcceleratorSelectionProperty(
                                name="name",
                                runtime="runtime"
                            )]
                        ),
                        allowed_instance_types=["allowedInstanceTypes"],
                        cpu_architecture_type="cpuArchitectureType",
                        custom_amounts=[deadline_mixins.CfnFleetPropsMixin.FleetAmountCapabilityProperty(
                            max=123,
                            min=123,
                            name="name"
                        )],
                        custom_attributes=[deadline_mixins.CfnFleetPropsMixin.FleetAttributeCapabilityProperty(
                            name="name",
                            values=["values"]
                        )],
                        excluded_instance_types=["excludedInstanceTypes"],
                        memory_mi_b=deadline_mixins.CfnFleetPropsMixin.MemoryMiBRangeProperty(
                            max=123,
                            min=123
                        ),
                        os_family="osFamily",
                        root_ebs_volume=deadline_mixins.CfnFleetPropsMixin.Ec2EbsVolumeProperty(
                            iops=123,
                            size_gi_b=123,
                            throughput_mi_b=123
                        ),
                        v_cpu_count=deadline_mixins.CfnFleetPropsMixin.VCpuCountRangeProperty(
                            max=123,
                            min=123
                        )
                    ),
                    instance_market_options=deadline_mixins.CfnFleetPropsMixin.ServiceManagedEc2InstanceMarketOptionsProperty(
                        type="type"
                    ),
                    storage_profile_id="storageProfileId",
                    vpc_configuration=deadline_mixins.CfnFleetPropsMixin.VpcConfigurationProperty(
                        resource_configuration_arns=["resourceConfigurationArns"]
                    )
                )
            ),
            description="description",
            display_name="displayName",
            farm_id="farmId",
            host_configuration=deadline_mixins.CfnFleetPropsMixin.HostConfigurationProperty(
                script_body="scriptBody",
                script_timeout_seconds=123
            ),
            max_worker_count=123,
            min_worker_count=123,
            role_arn="roleArn",
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
        '''Create a mixin to apply properties to ``AWS::Deadline::Fleet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8fe7923e3c23a21781df8ca59e3d8f8c31316c18b9173672707f5a5812a26b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44cd05278eb50cc23b4fff034c9dc5ea2ee8bdb9609105c8593db8a245e39d85)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2efa1e7e6815ed767373e01b394a1fef6c69ee023970e0a5f20169134c53a52)
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
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFleetPropsMixin.AcceleratorCapabilitiesProperty",
        jsii_struct_bases=[],
        name_mapping={"count": "count", "selections": "selections"},
    )
    class AcceleratorCapabilitiesProperty:
        def __init__(
            self,
            *,
            count: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.AcceleratorCountRangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            selections: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.AcceleratorSelectionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Provides information about the GPU accelerators used for jobs processed by a fleet.

            :param count: The number of GPU accelerators specified for worker hosts in this fleet.
            :param selections: A list of accelerator capabilities requested for this fleet. Only Amazon Elastic Compute Cloud instances that provide these capabilities will be used. For example, if you specify both L4 and T4 chips, AWS Deadline Cloud will use Amazon EC2 instances that have either the L4 or the T4 chip installed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-acceleratorcapabilities.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                accelerator_capabilities_property = deadline_mixins.CfnFleetPropsMixin.AcceleratorCapabilitiesProperty(
                    count=deadline_mixins.CfnFleetPropsMixin.AcceleratorCountRangeProperty(
                        max=123,
                        min=123
                    ),
                    selections=[deadline_mixins.CfnFleetPropsMixin.AcceleratorSelectionProperty(
                        name="name",
                        runtime="runtime"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__615a3db5a18205301277a9a683b993ef55e80b47b25a09e256523b7f031fabe8)
                check_type(argname="argument count", value=count, expected_type=type_hints["count"])
                check_type(argname="argument selections", value=selections, expected_type=type_hints["selections"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if count is not None:
                self._values["count"] = count
            if selections is not None:
                self._values["selections"] = selections

        @builtins.property
        def count(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.AcceleratorCountRangeProperty"]]:
            '''The number of GPU accelerators specified for worker hosts in this fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-acceleratorcapabilities.html#cfn-deadline-fleet-acceleratorcapabilities-count
            '''
            result = self._values.get("count")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.AcceleratorCountRangeProperty"]], result)

        @builtins.property
        def selections(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.AcceleratorSelectionProperty"]]]]:
            '''A list of accelerator capabilities requested for this fleet.

            Only Amazon Elastic Compute Cloud instances that provide these capabilities will be used. For example, if you specify both L4 and T4 chips, AWS Deadline Cloud will use Amazon EC2 instances that have either the L4 or the T4 chip installed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-acceleratorcapabilities.html#cfn-deadline-fleet-acceleratorcapabilities-selections
            '''
            result = self._values.get("selections")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.AcceleratorSelectionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AcceleratorCapabilitiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFleetPropsMixin.AcceleratorCountRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"max": "max", "min": "min"},
    )
    class AcceleratorCountRangeProperty:
        def __init__(
            self,
            *,
            max: typing.Optional[jsii.Number] = None,
            min: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines the maximum and minimum number of GPU accelerators required for a worker instance..

            :param max: The maximum number of GPU accelerators in the worker host.
            :param min: The minimum number of GPU accelerators in the worker host.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-acceleratorcountrange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                accelerator_count_range_property = deadline_mixins.CfnFleetPropsMixin.AcceleratorCountRangeProperty(
                    max=123,
                    min=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0e1308ca47d748cf0d52a37c93dce9b51bf2bc946d9ad163c6b9ee65f0b366da)
                check_type(argname="argument max", value=max, expected_type=type_hints["max"])
                check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max is not None:
                self._values["max"] = max
            if min is not None:
                self._values["min"] = min

        @builtins.property
        def max(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of GPU accelerators in the worker host.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-acceleratorcountrange.html#cfn-deadline-fleet-acceleratorcountrange-max
            '''
            result = self._values.get("max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min(self) -> typing.Optional[jsii.Number]:
            '''The minimum number of GPU accelerators in the worker host.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-acceleratorcountrange.html#cfn-deadline-fleet-acceleratorcountrange-min
            '''
            result = self._values.get("min")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AcceleratorCountRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFleetPropsMixin.AcceleratorSelectionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "runtime": "runtime"},
    )
    class AcceleratorSelectionProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            runtime: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a specific GPU accelerator required for an Amazon Elastic Compute Cloud worker host.

            :param name: The name of the chip used by the GPU accelerator. If you specify ``l4`` as the name of the accelerator, you must specify ``latest`` or ``grid:r570`` as the runtime. The available GPU accelerators are: - ``t4`` - NVIDIA T4 Tensor Core GPU - ``a10g`` - NVIDIA A10G Tensor Core GPU - ``l4`` - NVIDIA L4 Tensor Core GPU - ``l40s`` - NVIDIA L40S Tensor Core GPU
            :param runtime: Specifies the runtime driver to use for the GPU accelerator. You must use the same runtime for all GPUs. You can choose from the following runtimes: - ``latest`` - Use the latest runtime available for the chip. If you specify ``latest`` and a new version of the runtime is released, the new version of the runtime is used. - ``grid:r570`` - `NVIDIA vGPU software 18 <https://docs.aws.amazon.com/https://docs.nvidia.com/vgpu/18.0/index.html>`_ - ``grid:r535`` - `NVIDIA vGPU software 16 <https://docs.aws.amazon.com/https://docs.nvidia.com/vgpu/16.0/index.html>`_ If you don't specify a runtime, AWS Deadline Cloud uses ``latest`` as the default. However, if you have multiple accelerators and specify ``latest`` for some and leave others blank, AWS Deadline Cloud raises an exception.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-acceleratorselection.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                accelerator_selection_property = deadline_mixins.CfnFleetPropsMixin.AcceleratorSelectionProperty(
                    name="name",
                    runtime="runtime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f563d51f47dda6d80604bbf899c89b034791231d83f04a531685058fe71c2ba)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if runtime is not None:
                self._values["runtime"] = runtime

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the chip used by the GPU accelerator.

            If you specify ``l4`` as the name of the accelerator, you must specify ``latest`` or ``grid:r570`` as the runtime.

            The available GPU accelerators are:

            - ``t4`` - NVIDIA T4 Tensor Core GPU
            - ``a10g`` - NVIDIA A10G Tensor Core GPU
            - ``l4`` - NVIDIA L4 Tensor Core GPU
            - ``l40s`` - NVIDIA L40S Tensor Core GPU

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-acceleratorselection.html#cfn-deadline-fleet-acceleratorselection-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def runtime(self) -> typing.Optional[builtins.str]:
            '''Specifies the runtime driver to use for the GPU accelerator. You must use the same runtime for all GPUs.

            You can choose from the following runtimes:

            - ``latest`` - Use the latest runtime available for the chip. If you specify ``latest`` and a new version of the runtime is released, the new version of the runtime is used.
            - ``grid:r570`` - `NVIDIA vGPU software 18 <https://docs.aws.amazon.com/https://docs.nvidia.com/vgpu/18.0/index.html>`_
            - ``grid:r535`` - `NVIDIA vGPU software 16 <https://docs.aws.amazon.com/https://docs.nvidia.com/vgpu/16.0/index.html>`_

            If you don't specify a runtime, AWS Deadline Cloud uses ``latest`` as the default. However, if you have multiple accelerators and specify ``latest`` for some and leave others blank, AWS Deadline Cloud raises an exception.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-acceleratorselection.html#cfn-deadline-fleet-acceleratorselection-runtime
            '''
            result = self._values.get("runtime")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AcceleratorSelectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFleetPropsMixin.AcceleratorTotalMemoryMiBRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"max": "max", "min": "min"},
    )
    class AcceleratorTotalMemoryMiBRangeProperty:
        def __init__(
            self,
            *,
            max: typing.Optional[jsii.Number] = None,
            min: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines the maximum and minimum amount of memory, in MiB, to use for the accelerator.

            :param max: The maximum amount of memory to use for the accelerator, measured in MiB.
            :param min: The minimum amount of memory to use for the accelerator, measured in MiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-acceleratortotalmemorymibrange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                accelerator_total_memory_mi_bRange_property = deadline_mixins.CfnFleetPropsMixin.AcceleratorTotalMemoryMiBRangeProperty(
                    max=123,
                    min=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f22615b3b4c8df76a0a1af2c9ea2e08464a53390c4263381a4b93bf315011584)
                check_type(argname="argument max", value=max, expected_type=type_hints["max"])
                check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max is not None:
                self._values["max"] = max
            if min is not None:
                self._values["min"] = min

        @builtins.property
        def max(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of memory to use for the accelerator, measured in MiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-acceleratortotalmemorymibrange.html#cfn-deadline-fleet-acceleratortotalmemorymibrange-max
            '''
            result = self._values.get("max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min(self) -> typing.Optional[jsii.Number]:
            '''The minimum amount of memory to use for the accelerator, measured in MiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-acceleratortotalmemorymibrange.html#cfn-deadline-fleet-acceleratortotalmemorymibrange-min
            '''
            result = self._values.get("min")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AcceleratorTotalMemoryMiBRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFleetPropsMixin.CustomerManagedFleetConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "mode": "mode",
            "storage_profile_id": "storageProfileId",
            "tag_propagation_mode": "tagPropagationMode",
            "worker_capabilities": "workerCapabilities",
        },
    )
    class CustomerManagedFleetConfigurationProperty:
        def __init__(
            self,
            *,
            mode: typing.Optional[builtins.str] = None,
            storage_profile_id: typing.Optional[builtins.str] = None,
            tag_propagation_mode: typing.Optional[builtins.str] = None,
            worker_capabilities: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.CustomerManagedWorkerCapabilitiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration details for a customer managed fleet.

            :param mode: The Auto Scaling mode for the customer managed fleet.
            :param storage_profile_id: The storage profile ID for the customer managed fleet.
            :param tag_propagation_mode: The tag propagation mode for the customer managed fleet.
            :param worker_capabilities: The worker capabilities for the customer managed fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-customermanagedfleetconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                customer_managed_fleet_configuration_property = deadline_mixins.CfnFleetPropsMixin.CustomerManagedFleetConfigurationProperty(
                    mode="mode",
                    storage_profile_id="storageProfileId",
                    tag_propagation_mode="tagPropagationMode",
                    worker_capabilities=deadline_mixins.CfnFleetPropsMixin.CustomerManagedWorkerCapabilitiesProperty(
                        accelerator_count=deadline_mixins.CfnFleetPropsMixin.AcceleratorCountRangeProperty(
                            max=123,
                            min=123
                        ),
                        accelerator_total_memory_mi_b=deadline_mixins.CfnFleetPropsMixin.AcceleratorTotalMemoryMiBRangeProperty(
                            max=123,
                            min=123
                        ),
                        accelerator_types=["acceleratorTypes"],
                        cpu_architecture_type="cpuArchitectureType",
                        custom_amounts=[deadline_mixins.CfnFleetPropsMixin.FleetAmountCapabilityProperty(
                            max=123,
                            min=123,
                            name="name"
                        )],
                        custom_attributes=[deadline_mixins.CfnFleetPropsMixin.FleetAttributeCapabilityProperty(
                            name="name",
                            values=["values"]
                        )],
                        memory_mi_b=deadline_mixins.CfnFleetPropsMixin.MemoryMiBRangeProperty(
                            max=123,
                            min=123
                        ),
                        os_family="osFamily",
                        v_cpu_count=deadline_mixins.CfnFleetPropsMixin.VCpuCountRangeProperty(
                            max=123,
                            min=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e112161d4c500188f7155aa04ec4aec4ea219bc01c1175855d167b57b88bc171)
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument storage_profile_id", value=storage_profile_id, expected_type=type_hints["storage_profile_id"])
                check_type(argname="argument tag_propagation_mode", value=tag_propagation_mode, expected_type=type_hints["tag_propagation_mode"])
                check_type(argname="argument worker_capabilities", value=worker_capabilities, expected_type=type_hints["worker_capabilities"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mode is not None:
                self._values["mode"] = mode
            if storage_profile_id is not None:
                self._values["storage_profile_id"] = storage_profile_id
            if tag_propagation_mode is not None:
                self._values["tag_propagation_mode"] = tag_propagation_mode
            if worker_capabilities is not None:
                self._values["worker_capabilities"] = worker_capabilities

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''The Auto Scaling mode for the customer managed fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-customermanagedfleetconfiguration.html#cfn-deadline-fleet-customermanagedfleetconfiguration-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def storage_profile_id(self) -> typing.Optional[builtins.str]:
            '''The storage profile ID for the customer managed fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-customermanagedfleetconfiguration.html#cfn-deadline-fleet-customermanagedfleetconfiguration-storageprofileid
            '''
            result = self._values.get("storage_profile_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_propagation_mode(self) -> typing.Optional[builtins.str]:
            '''The tag propagation mode for the customer managed fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-customermanagedfleetconfiguration.html#cfn-deadline-fleet-customermanagedfleetconfiguration-tagpropagationmode
            '''
            result = self._values.get("tag_propagation_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def worker_capabilities(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.CustomerManagedWorkerCapabilitiesProperty"]]:
            '''The worker capabilities for the customer managed fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-customermanagedfleetconfiguration.html#cfn-deadline-fleet-customermanagedfleetconfiguration-workercapabilities
            '''
            result = self._values.get("worker_capabilities")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.CustomerManagedWorkerCapabilitiesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomerManagedFleetConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFleetPropsMixin.CustomerManagedWorkerCapabilitiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "accelerator_count": "acceleratorCount",
            "accelerator_total_memory_mib": "acceleratorTotalMemoryMiB",
            "accelerator_types": "acceleratorTypes",
            "cpu_architecture_type": "cpuArchitectureType",
            "custom_amounts": "customAmounts",
            "custom_attributes": "customAttributes",
            "memory_mib": "memoryMiB",
            "os_family": "osFamily",
            "v_cpu_count": "vCpuCount",
        },
    )
    class CustomerManagedWorkerCapabilitiesProperty:
        def __init__(
            self,
            *,
            accelerator_count: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.AcceleratorCountRangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            accelerator_total_memory_mib: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.AcceleratorTotalMemoryMiBRangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            accelerator_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            cpu_architecture_type: typing.Optional[builtins.str] = None,
            custom_amounts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.FleetAmountCapabilityProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            custom_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.FleetAttributeCapabilityProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            memory_mib: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.MemoryMiBRangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            os_family: typing.Optional[builtins.str] = None,
            v_cpu_count: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.VCpuCountRangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The worker capabilities for a customer managed workflow.

            :param accelerator_count: The range of the accelerator.
            :param accelerator_total_memory_mib: The total memory (MiB) for the customer managed worker capabilities.
            :param accelerator_types: The accelerator types for the customer managed worker capabilities.
            :param cpu_architecture_type: The CPU architecture type for the customer managed worker capabilities.
            :param custom_amounts: Custom requirement ranges for customer managed worker capabilities.
            :param custom_attributes: Custom attributes for the customer manged worker capabilities.
            :param memory_mib: The memory (MiB).
            :param os_family: The operating system (OS) family.
            :param v_cpu_count: The vCPU count for the customer manged worker capabilities.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-customermanagedworkercapabilities.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                customer_managed_worker_capabilities_property = deadline_mixins.CfnFleetPropsMixin.CustomerManagedWorkerCapabilitiesProperty(
                    accelerator_count=deadline_mixins.CfnFleetPropsMixin.AcceleratorCountRangeProperty(
                        max=123,
                        min=123
                    ),
                    accelerator_total_memory_mi_b=deadline_mixins.CfnFleetPropsMixin.AcceleratorTotalMemoryMiBRangeProperty(
                        max=123,
                        min=123
                    ),
                    accelerator_types=["acceleratorTypes"],
                    cpu_architecture_type="cpuArchitectureType",
                    custom_amounts=[deadline_mixins.CfnFleetPropsMixin.FleetAmountCapabilityProperty(
                        max=123,
                        min=123,
                        name="name"
                    )],
                    custom_attributes=[deadline_mixins.CfnFleetPropsMixin.FleetAttributeCapabilityProperty(
                        name="name",
                        values=["values"]
                    )],
                    memory_mi_b=deadline_mixins.CfnFleetPropsMixin.MemoryMiBRangeProperty(
                        max=123,
                        min=123
                    ),
                    os_family="osFamily",
                    v_cpu_count=deadline_mixins.CfnFleetPropsMixin.VCpuCountRangeProperty(
                        max=123,
                        min=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__137e014a3abac45c704760e14d6a1693e53c0098e4c3485fb98426671a35b07f)
                check_type(argname="argument accelerator_count", value=accelerator_count, expected_type=type_hints["accelerator_count"])
                check_type(argname="argument accelerator_total_memory_mib", value=accelerator_total_memory_mib, expected_type=type_hints["accelerator_total_memory_mib"])
                check_type(argname="argument accelerator_types", value=accelerator_types, expected_type=type_hints["accelerator_types"])
                check_type(argname="argument cpu_architecture_type", value=cpu_architecture_type, expected_type=type_hints["cpu_architecture_type"])
                check_type(argname="argument custom_amounts", value=custom_amounts, expected_type=type_hints["custom_amounts"])
                check_type(argname="argument custom_attributes", value=custom_attributes, expected_type=type_hints["custom_attributes"])
                check_type(argname="argument memory_mib", value=memory_mib, expected_type=type_hints["memory_mib"])
                check_type(argname="argument os_family", value=os_family, expected_type=type_hints["os_family"])
                check_type(argname="argument v_cpu_count", value=v_cpu_count, expected_type=type_hints["v_cpu_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if accelerator_count is not None:
                self._values["accelerator_count"] = accelerator_count
            if accelerator_total_memory_mib is not None:
                self._values["accelerator_total_memory_mib"] = accelerator_total_memory_mib
            if accelerator_types is not None:
                self._values["accelerator_types"] = accelerator_types
            if cpu_architecture_type is not None:
                self._values["cpu_architecture_type"] = cpu_architecture_type
            if custom_amounts is not None:
                self._values["custom_amounts"] = custom_amounts
            if custom_attributes is not None:
                self._values["custom_attributes"] = custom_attributes
            if memory_mib is not None:
                self._values["memory_mib"] = memory_mib
            if os_family is not None:
                self._values["os_family"] = os_family
            if v_cpu_count is not None:
                self._values["v_cpu_count"] = v_cpu_count

        @builtins.property
        def accelerator_count(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.AcceleratorCountRangeProperty"]]:
            '''The range of the accelerator.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-customermanagedworkercapabilities.html#cfn-deadline-fleet-customermanagedworkercapabilities-acceleratorcount
            '''
            result = self._values.get("accelerator_count")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.AcceleratorCountRangeProperty"]], result)

        @builtins.property
        def accelerator_total_memory_mib(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.AcceleratorTotalMemoryMiBRangeProperty"]]:
            '''The total memory (MiB) for the customer managed worker capabilities.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-customermanagedworkercapabilities.html#cfn-deadline-fleet-customermanagedworkercapabilities-acceleratortotalmemorymib
            '''
            result = self._values.get("accelerator_total_memory_mib")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.AcceleratorTotalMemoryMiBRangeProperty"]], result)

        @builtins.property
        def accelerator_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The accelerator types for the customer managed worker capabilities.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-customermanagedworkercapabilities.html#cfn-deadline-fleet-customermanagedworkercapabilities-acceleratortypes
            '''
            result = self._values.get("accelerator_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def cpu_architecture_type(self) -> typing.Optional[builtins.str]:
            '''The CPU architecture type for the customer managed worker capabilities.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-customermanagedworkercapabilities.html#cfn-deadline-fleet-customermanagedworkercapabilities-cpuarchitecturetype
            '''
            result = self._values.get("cpu_architecture_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_amounts(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.FleetAmountCapabilityProperty"]]]]:
            '''Custom requirement ranges for customer managed worker capabilities.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-customermanagedworkercapabilities.html#cfn-deadline-fleet-customermanagedworkercapabilities-customamounts
            '''
            result = self._values.get("custom_amounts")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.FleetAmountCapabilityProperty"]]]], result)

        @builtins.property
        def custom_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.FleetAttributeCapabilityProperty"]]]]:
            '''Custom attributes for the customer manged worker capabilities.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-customermanagedworkercapabilities.html#cfn-deadline-fleet-customermanagedworkercapabilities-customattributes
            '''
            result = self._values.get("custom_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.FleetAttributeCapabilityProperty"]]]], result)

        @builtins.property
        def memory_mib(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.MemoryMiBRangeProperty"]]:
            '''The memory (MiB).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-customermanagedworkercapabilities.html#cfn-deadline-fleet-customermanagedworkercapabilities-memorymib
            '''
            result = self._values.get("memory_mib")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.MemoryMiBRangeProperty"]], result)

        @builtins.property
        def os_family(self) -> typing.Optional[builtins.str]:
            '''The operating system (OS) family.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-customermanagedworkercapabilities.html#cfn-deadline-fleet-customermanagedworkercapabilities-osfamily
            '''
            result = self._values.get("os_family")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def v_cpu_count(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.VCpuCountRangeProperty"]]:
            '''The vCPU count for the customer manged worker capabilities.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-customermanagedworkercapabilities.html#cfn-deadline-fleet-customermanagedworkercapabilities-vcpucount
            '''
            result = self._values.get("v_cpu_count")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.VCpuCountRangeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomerManagedWorkerCapabilitiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFleetPropsMixin.Ec2EbsVolumeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "iops": "iops",
            "size_gib": "sizeGiB",
            "throughput_mib": "throughputMiB",
        },
    )
    class Ec2EbsVolumeProperty:
        def __init__(
            self,
            *,
            iops: typing.Optional[jsii.Number] = None,
            size_gib: typing.Optional[jsii.Number] = None,
            throughput_mib: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the EBS volume.

            :param iops: The IOPS per volume. Default: - 3000
            :param size_gib: The EBS volume size in GiB. Default: - 250
            :param throughput_mib: The throughput per volume in MiB. Default: - 125

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-ec2ebsvolume.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                ec2_ebs_volume_property = deadline_mixins.CfnFleetPropsMixin.Ec2EbsVolumeProperty(
                    iops=123,
                    size_gi_b=123,
                    throughput_mi_b=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__359083b8a91ba19721baa3abc36eae18dc3c9e3cbf3186ff91ff76e0349ea904)
                check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
                check_type(argname="argument size_gib", value=size_gib, expected_type=type_hints["size_gib"])
                check_type(argname="argument throughput_mib", value=throughput_mib, expected_type=type_hints["throughput_mib"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iops is not None:
                self._values["iops"] = iops
            if size_gib is not None:
                self._values["size_gib"] = size_gib
            if throughput_mib is not None:
                self._values["throughput_mib"] = throughput_mib

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            '''The IOPS per volume.

            :default: - 3000

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-ec2ebsvolume.html#cfn-deadline-fleet-ec2ebsvolume-iops
            '''
            result = self._values.get("iops")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def size_gib(self) -> typing.Optional[jsii.Number]:
            '''The EBS volume size in GiB.

            :default: - 250

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-ec2ebsvolume.html#cfn-deadline-fleet-ec2ebsvolume-sizegib
            '''
            result = self._values.get("size_gib")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throughput_mib(self) -> typing.Optional[jsii.Number]:
            '''The throughput per volume in MiB.

            :default: - 125

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-ec2ebsvolume.html#cfn-deadline-fleet-ec2ebsvolume-throughputmib
            '''
            result = self._values.get("throughput_mib")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "Ec2EbsVolumeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFleetPropsMixin.FleetAmountCapabilityProperty",
        jsii_struct_bases=[],
        name_mapping={"max": "max", "min": "min", "name": "name"},
    )
    class FleetAmountCapabilityProperty:
        def __init__(
            self,
            *,
            max: typing.Optional[jsii.Number] = None,
            min: typing.Optional[jsii.Number] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The fleet amount and attribute capabilities.

            :param max: The maximum amount of the fleet worker capability.
            :param min: The minimum amount of fleet worker capability.
            :param name: The name of the fleet capability.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-fleetamountcapability.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                fleet_amount_capability_property = deadline_mixins.CfnFleetPropsMixin.FleetAmountCapabilityProperty(
                    max=123,
                    min=123,
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d8335870bb662bae87b2bf9409ea6c05c99bf2d270430dcd5914a733f9b22bd6)
                check_type(argname="argument max", value=max, expected_type=type_hints["max"])
                check_type(argname="argument min", value=min, expected_type=type_hints["min"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max is not None:
                self._values["max"] = max
            if min is not None:
                self._values["min"] = min
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def max(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of the fleet worker capability.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-fleetamountcapability.html#cfn-deadline-fleet-fleetamountcapability-max
            '''
            result = self._values.get("max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min(self) -> typing.Optional[jsii.Number]:
            '''The minimum amount of fleet worker capability.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-fleetamountcapability.html#cfn-deadline-fleet-fleetamountcapability-min
            '''
            result = self._values.get("min")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the fleet capability.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-fleetamountcapability.html#cfn-deadline-fleet-fleetamountcapability-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FleetAmountCapabilityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFleetPropsMixin.FleetAttributeCapabilityProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "values": "values"},
    )
    class FleetAttributeCapabilityProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Defines the fleet's capability name, minimum, and maximum.

            :param name: The name of the fleet attribute capability for the worker.
            :param values: The number of fleet attribute capabilities.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-fleetattributecapability.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                fleet_attribute_capability_property = deadline_mixins.CfnFleetPropsMixin.FleetAttributeCapabilityProperty(
                    name="name",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8973c1508221de9dd62fc896e62fefb7af719381073d5be5f6af668e6dafd391)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the fleet attribute capability for the worker.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-fleetattributecapability.html#cfn-deadline-fleet-fleetattributecapability-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The number of fleet attribute capabilities.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-fleetattributecapability.html#cfn-deadline-fleet-fleetattributecapability-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FleetAttributeCapabilityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFleetPropsMixin.FleetCapabilitiesProperty",
        jsii_struct_bases=[],
        name_mapping={"amounts": "amounts", "attributes": "attributes"},
    )
    class FleetCapabilitiesProperty:
        def __init__(
            self,
            *,
            amounts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.FleetAmountCapabilityProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.FleetAttributeCapabilityProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The amounts and attributes of fleets.

            :param amounts: Amount capabilities of the fleet.
            :param attributes: Attribute capabilities of the fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-fleetcapabilities.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                fleet_capabilities_property = deadline_mixins.CfnFleetPropsMixin.FleetCapabilitiesProperty(
                    amounts=[deadline_mixins.CfnFleetPropsMixin.FleetAmountCapabilityProperty(
                        max=123,
                        min=123,
                        name="name"
                    )],
                    attributes=[deadline_mixins.CfnFleetPropsMixin.FleetAttributeCapabilityProperty(
                        name="name",
                        values=["values"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__64d38790a2d13f6b579851039500f9a8732f5ccb2d23941a8661e4c6ef7e68c9)
                check_type(argname="argument amounts", value=amounts, expected_type=type_hints["amounts"])
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if amounts is not None:
                self._values["amounts"] = amounts
            if attributes is not None:
                self._values["attributes"] = attributes

        @builtins.property
        def amounts(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.FleetAmountCapabilityProperty"]]]]:
            '''Amount capabilities of the fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-fleetcapabilities.html#cfn-deadline-fleet-fleetcapabilities-amounts
            '''
            result = self._values.get("amounts")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.FleetAmountCapabilityProperty"]]]], result)

        @builtins.property
        def attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.FleetAttributeCapabilityProperty"]]]]:
            '''Attribute capabilities of the fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-fleetcapabilities.html#cfn-deadline-fleet-fleetcapabilities-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.FleetAttributeCapabilityProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FleetCapabilitiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFleetPropsMixin.FleetConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "customer_managed": "customerManaged",
            "service_managed_ec2": "serviceManagedEc2",
        },
    )
    class FleetConfigurationProperty:
        def __init__(
            self,
            *,
            customer_managed: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.CustomerManagedFleetConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_managed_ec2: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.ServiceManagedEc2FleetConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Fleet configuration details.

            :param customer_managed: The customer managed fleets within a fleet configuration.
            :param service_managed_ec2: The service managed Amazon EC2 instances for a fleet configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-fleetconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                fleet_configuration_property = deadline_mixins.CfnFleetPropsMixin.FleetConfigurationProperty(
                    customer_managed=deadline_mixins.CfnFleetPropsMixin.CustomerManagedFleetConfigurationProperty(
                        mode="mode",
                        storage_profile_id="storageProfileId",
                        tag_propagation_mode="tagPropagationMode",
                        worker_capabilities=deadline_mixins.CfnFleetPropsMixin.CustomerManagedWorkerCapabilitiesProperty(
                            accelerator_count=deadline_mixins.CfnFleetPropsMixin.AcceleratorCountRangeProperty(
                                max=123,
                                min=123
                            ),
                            accelerator_total_memory_mi_b=deadline_mixins.CfnFleetPropsMixin.AcceleratorTotalMemoryMiBRangeProperty(
                                max=123,
                                min=123
                            ),
                            accelerator_types=["acceleratorTypes"],
                            cpu_architecture_type="cpuArchitectureType",
                            custom_amounts=[deadline_mixins.CfnFleetPropsMixin.FleetAmountCapabilityProperty(
                                max=123,
                                min=123,
                                name="name"
                            )],
                            custom_attributes=[deadline_mixins.CfnFleetPropsMixin.FleetAttributeCapabilityProperty(
                                name="name",
                                values=["values"]
                            )],
                            memory_mi_b=deadline_mixins.CfnFleetPropsMixin.MemoryMiBRangeProperty(
                                max=123,
                                min=123
                            ),
                            os_family="osFamily",
                            v_cpu_count=deadline_mixins.CfnFleetPropsMixin.VCpuCountRangeProperty(
                                max=123,
                                min=123
                            )
                        )
                    ),
                    service_managed_ec2=deadline_mixins.CfnFleetPropsMixin.ServiceManagedEc2FleetConfigurationProperty(
                        instance_capabilities=deadline_mixins.CfnFleetPropsMixin.ServiceManagedEc2InstanceCapabilitiesProperty(
                            accelerator_capabilities=deadline_mixins.CfnFleetPropsMixin.AcceleratorCapabilitiesProperty(
                                count=deadline_mixins.CfnFleetPropsMixin.AcceleratorCountRangeProperty(
                                    max=123,
                                    min=123
                                ),
                                selections=[deadline_mixins.CfnFleetPropsMixin.AcceleratorSelectionProperty(
                                    name="name",
                                    runtime="runtime"
                                )]
                            ),
                            allowed_instance_types=["allowedInstanceTypes"],
                            cpu_architecture_type="cpuArchitectureType",
                            custom_amounts=[deadline_mixins.CfnFleetPropsMixin.FleetAmountCapabilityProperty(
                                max=123,
                                min=123,
                                name="name"
                            )],
                            custom_attributes=[deadline_mixins.CfnFleetPropsMixin.FleetAttributeCapabilityProperty(
                                name="name",
                                values=["values"]
                            )],
                            excluded_instance_types=["excludedInstanceTypes"],
                            memory_mi_b=deadline_mixins.CfnFleetPropsMixin.MemoryMiBRangeProperty(
                                max=123,
                                min=123
                            ),
                            os_family="osFamily",
                            root_ebs_volume=deadline_mixins.CfnFleetPropsMixin.Ec2EbsVolumeProperty(
                                iops=123,
                                size_gi_b=123,
                                throughput_mi_b=123
                            ),
                            v_cpu_count=deadline_mixins.CfnFleetPropsMixin.VCpuCountRangeProperty(
                                max=123,
                                min=123
                            )
                        ),
                        instance_market_options=deadline_mixins.CfnFleetPropsMixin.ServiceManagedEc2InstanceMarketOptionsProperty(
                            type="type"
                        ),
                        storage_profile_id="storageProfileId",
                        vpc_configuration=deadline_mixins.CfnFleetPropsMixin.VpcConfigurationProperty(
                            resource_configuration_arns=["resourceConfigurationArns"]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f9ada7c8b4bdb0b51a04fcbe0d38580fabcadeb7a3814eea58457055caa5adc3)
                check_type(argname="argument customer_managed", value=customer_managed, expected_type=type_hints["customer_managed"])
                check_type(argname="argument service_managed_ec2", value=service_managed_ec2, expected_type=type_hints["service_managed_ec2"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if customer_managed is not None:
                self._values["customer_managed"] = customer_managed
            if service_managed_ec2 is not None:
                self._values["service_managed_ec2"] = service_managed_ec2

        @builtins.property
        def customer_managed(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.CustomerManagedFleetConfigurationProperty"]]:
            '''The customer managed fleets within a fleet configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-fleetconfiguration.html#cfn-deadline-fleet-fleetconfiguration-customermanaged
            '''
            result = self._values.get("customer_managed")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.CustomerManagedFleetConfigurationProperty"]], result)

        @builtins.property
        def service_managed_ec2(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.ServiceManagedEc2FleetConfigurationProperty"]]:
            '''The service managed Amazon EC2 instances for a fleet configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-fleetconfiguration.html#cfn-deadline-fleet-fleetconfiguration-servicemanagedec2
            '''
            result = self._values.get("service_managed_ec2")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.ServiceManagedEc2FleetConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FleetConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFleetPropsMixin.HostConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "script_body": "scriptBody",
            "script_timeout_seconds": "scriptTimeoutSeconds",
        },
    )
    class HostConfigurationProperty:
        def __init__(
            self,
            *,
            script_body: typing.Optional[builtins.str] = None,
            script_timeout_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Provides a script that runs as a worker is starting up that you can use to provide additional configuration for workers in your fleet.

            To remove a script from a fleet, use the `UpdateFleet <https://docs.aws.amazon.com/deadline-cloud/latest/APIReference/API_UpdateFleet.html>`_ operation with the ``hostConfiguration`` ``scriptBody`` parameter set to an empty string ("").

            :param script_body: The text of the script that runs as a worker is starting up that you can use to provide additional configuration for workers in your fleet. The script runs after a worker enters the ``STARTING`` state and before the worker processes tasks. For more information about using the script, see `Run scripts as an administrator to configure workers <https://docs.aws.amazon.com/deadline-cloud/latest/developerguide/smf-admin.html>`_ in the *Deadline Cloud Developer Guide* . .. epigraph:: The script runs as an administrative user ( ``sudo root`` on Linux, as an Administrator on Windows).
            :param script_timeout_seconds: The maximum time that the host configuration can run. If the timeout expires, the worker enters the ``NOT RESPONDING`` state and shuts down. You are charged for the time that the worker is running the host configuration script. .. epigraph:: You should configure your fleet for a maximum of one worker while testing your host configuration script to avoid starting additional workers. The default is 300 seconds (5 minutes). Default: - 300

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-hostconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                host_configuration_property = deadline_mixins.CfnFleetPropsMixin.HostConfigurationProperty(
                    script_body="scriptBody",
                    script_timeout_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__17334a96ecc5531cee85fe4631f71280797fc8db3121d638d8c084c974e67410)
                check_type(argname="argument script_body", value=script_body, expected_type=type_hints["script_body"])
                check_type(argname="argument script_timeout_seconds", value=script_timeout_seconds, expected_type=type_hints["script_timeout_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if script_body is not None:
                self._values["script_body"] = script_body
            if script_timeout_seconds is not None:
                self._values["script_timeout_seconds"] = script_timeout_seconds

        @builtins.property
        def script_body(self) -> typing.Optional[builtins.str]:
            '''The text of the script that runs as a worker is starting up that you can use to provide additional configuration for workers in your fleet.

            The script runs after a worker enters the ``STARTING`` state and before the worker processes tasks.

            For more information about using the script, see `Run scripts as an administrator to configure workers <https://docs.aws.amazon.com/deadline-cloud/latest/developerguide/smf-admin.html>`_ in the *Deadline Cloud Developer Guide* .
            .. epigraph::

               The script runs as an administrative user ( ``sudo root`` on Linux, as an Administrator on Windows).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-hostconfiguration.html#cfn-deadline-fleet-hostconfiguration-scriptbody
            '''
            result = self._values.get("script_body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def script_timeout_seconds(self) -> typing.Optional[jsii.Number]:
            '''The maximum time that the host configuration can run.

            If the timeout expires, the worker enters the ``NOT RESPONDING`` state and shuts down. You are charged for the time that the worker is running the host configuration script.
            .. epigraph::

               You should configure your fleet for a maximum of one worker while testing your host configuration script to avoid starting additional workers.

            The default is 300 seconds (5 minutes).

            :default: - 300

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-hostconfiguration.html#cfn-deadline-fleet-hostconfiguration-scripttimeoutseconds
            '''
            result = self._values.get("script_timeout_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HostConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFleetPropsMixin.MemoryMiBRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"max": "max", "min": "min"},
    )
    class MemoryMiBRangeProperty:
        def __init__(
            self,
            *,
            max: typing.Optional[jsii.Number] = None,
            min: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The range of memory in MiB.

            :param max: The maximum amount of memory (in MiB).
            :param min: The minimum amount of memory (in MiB).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-memorymibrange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                memory_mi_bRange_property = deadline_mixins.CfnFleetPropsMixin.MemoryMiBRangeProperty(
                    max=123,
                    min=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5aaa3be25a74ed5edc057bdf76ad354a621d48c35be0e75a591c9879fc3900e9)
                check_type(argname="argument max", value=max, expected_type=type_hints["max"])
                check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max is not None:
                self._values["max"] = max
            if min is not None:
                self._values["min"] = min

        @builtins.property
        def max(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of memory (in MiB).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-memorymibrange.html#cfn-deadline-fleet-memorymibrange-max
            '''
            result = self._values.get("max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min(self) -> typing.Optional[jsii.Number]:
            '''The minimum amount of memory (in MiB).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-memorymibrange.html#cfn-deadline-fleet-memorymibrange-min
            '''
            result = self._values.get("min")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MemoryMiBRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFleetPropsMixin.ServiceManagedEc2FleetConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instance_capabilities": "instanceCapabilities",
            "instance_market_options": "instanceMarketOptions",
            "storage_profile_id": "storageProfileId",
            "vpc_configuration": "vpcConfiguration",
        },
    )
    class ServiceManagedEc2FleetConfigurationProperty:
        def __init__(
            self,
            *,
            instance_capabilities: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.ServiceManagedEc2InstanceCapabilitiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            instance_market_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.ServiceManagedEc2InstanceMarketOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            storage_profile_id: typing.Optional[builtins.str] = None,
            vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.VpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration details for a service managed EC2 fleet.

            :param instance_capabilities: The instance capabilities for the service managed EC2 fleet.
            :param instance_market_options: The instance market options for the service managed EC2 fleet.
            :param storage_profile_id: The storage profile ID for the service managed EC2 fleet.
            :param vpc_configuration: The VPC configuration for the service managed EC2 fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-servicemanagedec2fleetconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                service_managed_ec2_fleet_configuration_property = deadline_mixins.CfnFleetPropsMixin.ServiceManagedEc2FleetConfigurationProperty(
                    instance_capabilities=deadline_mixins.CfnFleetPropsMixin.ServiceManagedEc2InstanceCapabilitiesProperty(
                        accelerator_capabilities=deadline_mixins.CfnFleetPropsMixin.AcceleratorCapabilitiesProperty(
                            count=deadline_mixins.CfnFleetPropsMixin.AcceleratorCountRangeProperty(
                                max=123,
                                min=123
                            ),
                            selections=[deadline_mixins.CfnFleetPropsMixin.AcceleratorSelectionProperty(
                                name="name",
                                runtime="runtime"
                            )]
                        ),
                        allowed_instance_types=["allowedInstanceTypes"],
                        cpu_architecture_type="cpuArchitectureType",
                        custom_amounts=[deadline_mixins.CfnFleetPropsMixin.FleetAmountCapabilityProperty(
                            max=123,
                            min=123,
                            name="name"
                        )],
                        custom_attributes=[deadline_mixins.CfnFleetPropsMixin.FleetAttributeCapabilityProperty(
                            name="name",
                            values=["values"]
                        )],
                        excluded_instance_types=["excludedInstanceTypes"],
                        memory_mi_b=deadline_mixins.CfnFleetPropsMixin.MemoryMiBRangeProperty(
                            max=123,
                            min=123
                        ),
                        os_family="osFamily",
                        root_ebs_volume=deadline_mixins.CfnFleetPropsMixin.Ec2EbsVolumeProperty(
                            iops=123,
                            size_gi_b=123,
                            throughput_mi_b=123
                        ),
                        v_cpu_count=deadline_mixins.CfnFleetPropsMixin.VCpuCountRangeProperty(
                            max=123,
                            min=123
                        )
                    ),
                    instance_market_options=deadline_mixins.CfnFleetPropsMixin.ServiceManagedEc2InstanceMarketOptionsProperty(
                        type="type"
                    ),
                    storage_profile_id="storageProfileId",
                    vpc_configuration=deadline_mixins.CfnFleetPropsMixin.VpcConfigurationProperty(
                        resource_configuration_arns=["resourceConfigurationArns"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__830bb132c3c5149884ddbcfe2d48fff41261b1ae284d0a10b64a9a9c794e80dc)
                check_type(argname="argument instance_capabilities", value=instance_capabilities, expected_type=type_hints["instance_capabilities"])
                check_type(argname="argument instance_market_options", value=instance_market_options, expected_type=type_hints["instance_market_options"])
                check_type(argname="argument storage_profile_id", value=storage_profile_id, expected_type=type_hints["storage_profile_id"])
                check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_capabilities is not None:
                self._values["instance_capabilities"] = instance_capabilities
            if instance_market_options is not None:
                self._values["instance_market_options"] = instance_market_options
            if storage_profile_id is not None:
                self._values["storage_profile_id"] = storage_profile_id
            if vpc_configuration is not None:
                self._values["vpc_configuration"] = vpc_configuration

        @builtins.property
        def instance_capabilities(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.ServiceManagedEc2InstanceCapabilitiesProperty"]]:
            '''The instance capabilities for the service managed EC2 fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-servicemanagedec2fleetconfiguration.html#cfn-deadline-fleet-servicemanagedec2fleetconfiguration-instancecapabilities
            '''
            result = self._values.get("instance_capabilities")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.ServiceManagedEc2InstanceCapabilitiesProperty"]], result)

        @builtins.property
        def instance_market_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.ServiceManagedEc2InstanceMarketOptionsProperty"]]:
            '''The instance market options for the service managed EC2 fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-servicemanagedec2fleetconfiguration.html#cfn-deadline-fleet-servicemanagedec2fleetconfiguration-instancemarketoptions
            '''
            result = self._values.get("instance_market_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.ServiceManagedEc2InstanceMarketOptionsProperty"]], result)

        @builtins.property
        def storage_profile_id(self) -> typing.Optional[builtins.str]:
            '''The storage profile ID for the service managed EC2 fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-servicemanagedec2fleetconfiguration.html#cfn-deadline-fleet-servicemanagedec2fleetconfiguration-storageprofileid
            '''
            result = self._values.get("storage_profile_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.VpcConfigurationProperty"]]:
            '''The VPC configuration for the service managed EC2 fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-servicemanagedec2fleetconfiguration.html#cfn-deadline-fleet-servicemanagedec2fleetconfiguration-vpcconfiguration
            '''
            result = self._values.get("vpc_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.VpcConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceManagedEc2FleetConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFleetPropsMixin.ServiceManagedEc2InstanceCapabilitiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "accelerator_capabilities": "acceleratorCapabilities",
            "allowed_instance_types": "allowedInstanceTypes",
            "cpu_architecture_type": "cpuArchitectureType",
            "custom_amounts": "customAmounts",
            "custom_attributes": "customAttributes",
            "excluded_instance_types": "excludedInstanceTypes",
            "memory_mib": "memoryMiB",
            "os_family": "osFamily",
            "root_ebs_volume": "rootEbsVolume",
            "v_cpu_count": "vCpuCount",
        },
    )
    class ServiceManagedEc2InstanceCapabilitiesProperty:
        def __init__(
            self,
            *,
            accelerator_capabilities: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.AcceleratorCapabilitiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            allowed_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            cpu_architecture_type: typing.Optional[builtins.str] = None,
            custom_amounts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.FleetAmountCapabilityProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            custom_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.FleetAttributeCapabilityProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            excluded_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            memory_mib: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.MemoryMiBRangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            os_family: typing.Optional[builtins.str] = None,
            root_ebs_volume: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.Ec2EbsVolumeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            v_cpu_count: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.VCpuCountRangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The Amazon EC2 instance capabilities.

            :param accelerator_capabilities: Describes the GPU accelerator capabilities required for worker host instances in this fleet.
            :param allowed_instance_types: The allowable Amazon EC2 instance types.
            :param cpu_architecture_type: The CPU architecture type.
            :param custom_amounts: The custom capability amounts to require for instances in this fleet.
            :param custom_attributes: The custom capability attributes to require for instances in this fleet.
            :param excluded_instance_types: The instance types to exclude from the fleet.
            :param memory_mib: The memory, as MiB, for the Amazon EC2 instance type.
            :param os_family: The operating system (OS) family.
            :param root_ebs_volume: The root EBS volume.
            :param v_cpu_count: The amount of vCPU to require for instances in this fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-servicemanagedec2instancecapabilities.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                service_managed_ec2_instance_capabilities_property = deadline_mixins.CfnFleetPropsMixin.ServiceManagedEc2InstanceCapabilitiesProperty(
                    accelerator_capabilities=deadline_mixins.CfnFleetPropsMixin.AcceleratorCapabilitiesProperty(
                        count=deadline_mixins.CfnFleetPropsMixin.AcceleratorCountRangeProperty(
                            max=123,
                            min=123
                        ),
                        selections=[deadline_mixins.CfnFleetPropsMixin.AcceleratorSelectionProperty(
                            name="name",
                            runtime="runtime"
                        )]
                    ),
                    allowed_instance_types=["allowedInstanceTypes"],
                    cpu_architecture_type="cpuArchitectureType",
                    custom_amounts=[deadline_mixins.CfnFleetPropsMixin.FleetAmountCapabilityProperty(
                        max=123,
                        min=123,
                        name="name"
                    )],
                    custom_attributes=[deadline_mixins.CfnFleetPropsMixin.FleetAttributeCapabilityProperty(
                        name="name",
                        values=["values"]
                    )],
                    excluded_instance_types=["excludedInstanceTypes"],
                    memory_mi_b=deadline_mixins.CfnFleetPropsMixin.MemoryMiBRangeProperty(
                        max=123,
                        min=123
                    ),
                    os_family="osFamily",
                    root_ebs_volume=deadline_mixins.CfnFleetPropsMixin.Ec2EbsVolumeProperty(
                        iops=123,
                        size_gi_b=123,
                        throughput_mi_b=123
                    ),
                    v_cpu_count=deadline_mixins.CfnFleetPropsMixin.VCpuCountRangeProperty(
                        max=123,
                        min=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__855b722e9d5e0e80aae97b20946bbc37aac4393c77912a35dcf1c51f76e160d2)
                check_type(argname="argument accelerator_capabilities", value=accelerator_capabilities, expected_type=type_hints["accelerator_capabilities"])
                check_type(argname="argument allowed_instance_types", value=allowed_instance_types, expected_type=type_hints["allowed_instance_types"])
                check_type(argname="argument cpu_architecture_type", value=cpu_architecture_type, expected_type=type_hints["cpu_architecture_type"])
                check_type(argname="argument custom_amounts", value=custom_amounts, expected_type=type_hints["custom_amounts"])
                check_type(argname="argument custom_attributes", value=custom_attributes, expected_type=type_hints["custom_attributes"])
                check_type(argname="argument excluded_instance_types", value=excluded_instance_types, expected_type=type_hints["excluded_instance_types"])
                check_type(argname="argument memory_mib", value=memory_mib, expected_type=type_hints["memory_mib"])
                check_type(argname="argument os_family", value=os_family, expected_type=type_hints["os_family"])
                check_type(argname="argument root_ebs_volume", value=root_ebs_volume, expected_type=type_hints["root_ebs_volume"])
                check_type(argname="argument v_cpu_count", value=v_cpu_count, expected_type=type_hints["v_cpu_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if accelerator_capabilities is not None:
                self._values["accelerator_capabilities"] = accelerator_capabilities
            if allowed_instance_types is not None:
                self._values["allowed_instance_types"] = allowed_instance_types
            if cpu_architecture_type is not None:
                self._values["cpu_architecture_type"] = cpu_architecture_type
            if custom_amounts is not None:
                self._values["custom_amounts"] = custom_amounts
            if custom_attributes is not None:
                self._values["custom_attributes"] = custom_attributes
            if excluded_instance_types is not None:
                self._values["excluded_instance_types"] = excluded_instance_types
            if memory_mib is not None:
                self._values["memory_mib"] = memory_mib
            if os_family is not None:
                self._values["os_family"] = os_family
            if root_ebs_volume is not None:
                self._values["root_ebs_volume"] = root_ebs_volume
            if v_cpu_count is not None:
                self._values["v_cpu_count"] = v_cpu_count

        @builtins.property
        def accelerator_capabilities(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.AcceleratorCapabilitiesProperty"]]:
            '''Describes the GPU accelerator capabilities required for worker host instances in this fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-servicemanagedec2instancecapabilities.html#cfn-deadline-fleet-servicemanagedec2instancecapabilities-acceleratorcapabilities
            '''
            result = self._values.get("accelerator_capabilities")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.AcceleratorCapabilitiesProperty"]], result)

        @builtins.property
        def allowed_instance_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The allowable Amazon EC2 instance types.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-servicemanagedec2instancecapabilities.html#cfn-deadline-fleet-servicemanagedec2instancecapabilities-allowedinstancetypes
            '''
            result = self._values.get("allowed_instance_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def cpu_architecture_type(self) -> typing.Optional[builtins.str]:
            '''The CPU architecture type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-servicemanagedec2instancecapabilities.html#cfn-deadline-fleet-servicemanagedec2instancecapabilities-cpuarchitecturetype
            '''
            result = self._values.get("cpu_architecture_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_amounts(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.FleetAmountCapabilityProperty"]]]]:
            '''The custom capability amounts to require for instances in this fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-servicemanagedec2instancecapabilities.html#cfn-deadline-fleet-servicemanagedec2instancecapabilities-customamounts
            '''
            result = self._values.get("custom_amounts")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.FleetAmountCapabilityProperty"]]]], result)

        @builtins.property
        def custom_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.FleetAttributeCapabilityProperty"]]]]:
            '''The custom capability attributes to require for instances in this fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-servicemanagedec2instancecapabilities.html#cfn-deadline-fleet-servicemanagedec2instancecapabilities-customattributes
            '''
            result = self._values.get("custom_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.FleetAttributeCapabilityProperty"]]]], result)

        @builtins.property
        def excluded_instance_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The instance types to exclude from the fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-servicemanagedec2instancecapabilities.html#cfn-deadline-fleet-servicemanagedec2instancecapabilities-excludedinstancetypes
            '''
            result = self._values.get("excluded_instance_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def memory_mib(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.MemoryMiBRangeProperty"]]:
            '''The memory, as MiB, for the Amazon EC2 instance type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-servicemanagedec2instancecapabilities.html#cfn-deadline-fleet-servicemanagedec2instancecapabilities-memorymib
            '''
            result = self._values.get("memory_mib")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.MemoryMiBRangeProperty"]], result)

        @builtins.property
        def os_family(self) -> typing.Optional[builtins.str]:
            '''The operating system (OS) family.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-servicemanagedec2instancecapabilities.html#cfn-deadline-fleet-servicemanagedec2instancecapabilities-osfamily
            '''
            result = self._values.get("os_family")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def root_ebs_volume(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.Ec2EbsVolumeProperty"]]:
            '''The root EBS volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-servicemanagedec2instancecapabilities.html#cfn-deadline-fleet-servicemanagedec2instancecapabilities-rootebsvolume
            '''
            result = self._values.get("root_ebs_volume")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.Ec2EbsVolumeProperty"]], result)

        @builtins.property
        def v_cpu_count(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.VCpuCountRangeProperty"]]:
            '''The amount of vCPU to require for instances in this fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-servicemanagedec2instancecapabilities.html#cfn-deadline-fleet-servicemanagedec2instancecapabilities-vcpucount
            '''
            result = self._values.get("v_cpu_count")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.VCpuCountRangeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceManagedEc2InstanceCapabilitiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFleetPropsMixin.ServiceManagedEc2InstanceMarketOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type"},
    )
    class ServiceManagedEc2InstanceMarketOptionsProperty:
        def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
            '''The details of the Amazon EC2 instance market options for a service managed fleet.

            :param type: The Amazon EC2 instance type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-servicemanagedec2instancemarketoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                service_managed_ec2_instance_market_options_property = deadline_mixins.CfnFleetPropsMixin.ServiceManagedEc2InstanceMarketOptionsProperty(
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c381613bc0eec7d8acef73e175ff26bec05118685314b37430b5456e14f1b4b)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The Amazon EC2 instance type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-servicemanagedec2instancemarketoptions.html#cfn-deadline-fleet-servicemanagedec2instancemarketoptions-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceManagedEc2InstanceMarketOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFleetPropsMixin.VCpuCountRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"max": "max", "min": "min"},
    )
    class VCpuCountRangeProperty:
        def __init__(
            self,
            *,
            max: typing.Optional[jsii.Number] = None,
            min: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The allowable range of vCPU processing power for the fleet.

            :param max: The maximum amount of vCPU.
            :param min: The minimum amount of vCPU.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-vcpucountrange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                v_cpu_count_range_property = deadline_mixins.CfnFleetPropsMixin.VCpuCountRangeProperty(
                    max=123,
                    min=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b2eada1759cd1cd4f65fa4417cd1193f72e0f889f20602276156d70e5e97a5e)
                check_type(argname="argument max", value=max, expected_type=type_hints["max"])
                check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max is not None:
                self._values["max"] = max
            if min is not None:
                self._values["min"] = min

        @builtins.property
        def max(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of vCPU.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-vcpucountrange.html#cfn-deadline-fleet-vcpucountrange-max
            '''
            result = self._values.get("max")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min(self) -> typing.Optional[jsii.Number]:
            '''The minimum amount of vCPU.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-vcpucountrange.html#cfn-deadline-fleet-vcpucountrange-min
            '''
            result = self._values.get("min")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VCpuCountRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnFleetPropsMixin.VpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_configuration_arns": "resourceConfigurationArns"},
    )
    class VpcConfigurationProperty:
        def __init__(
            self,
            *,
            resource_configuration_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The configuration options for a service managed fleet's VPC.

            :param resource_configuration_arns: The ARNs of the VPC Lattice resource configurations attached to the fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-vpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                vpc_configuration_property = deadline_mixins.CfnFleetPropsMixin.VpcConfigurationProperty(
                    resource_configuration_arns=["resourceConfigurationArns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9067a6087728fb79500cccaecada40abefce168b582a35c0a88510df6c0ede39)
                check_type(argname="argument resource_configuration_arns", value=resource_configuration_arns, expected_type=type_hints["resource_configuration_arns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_configuration_arns is not None:
                self._values["resource_configuration_arns"] = resource_configuration_arns

        @builtins.property
        def resource_configuration_arns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The ARNs of the VPC Lattice resource configurations attached to the fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-fleet-vpcconfiguration.html#cfn-deadline-fleet-vpcconfiguration-resourceconfigurationarns
            '''
            result = self._values.get("resource_configuration_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnLicenseEndpointMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "security_group_ids": "securityGroupIds",
        "subnet_ids": "subnetIds",
        "tags": "tags",
        "vpc_id": "vpcId",
    },
)
class CfnLicenseEndpointMixinProps:
    def __init__(
        self,
        *,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnLicenseEndpointPropsMixin.

        :param security_group_ids: The identifier of the Amazon EC2 security group that controls access to the license endpoint.
        :param subnet_ids: Identifies the VPC subnets that can connect to a license endpoint.
        :param tags: The tags to add to your license endpoint. Each tag consists of a tag key and a tag value. Tag keys and values are both required, but tag values can be empty strings.
        :param vpc_id: The VPC (virtual private cloud) ID associated with the license endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-licenseendpoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
            
            cfn_license_endpoint_mixin_props = deadline_mixins.CfnLicenseEndpointMixinProps(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_id="vpcId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35ddc36b4ff6dfab52f6354cd8f40ade7aed7963ecdb998f1d0b56580740e5c6)
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The identifier of the Amazon EC2 security group that controls access to the license endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-licenseendpoint.html#cfn-deadline-licenseendpoint-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Identifies the VPC subnets that can connect to a license endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-licenseendpoint.html#cfn-deadline-licenseendpoint-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to add to your license endpoint.

        Each tag consists of a tag key and a tag value. Tag keys and values are both required, but tag values can be empty strings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-licenseendpoint.html#cfn-deadline-licenseendpoint-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The VPC (virtual private cloud) ID associated with the license endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-licenseendpoint.html#cfn-deadline-licenseendpoint-vpcid
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLicenseEndpointMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLicenseEndpointPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnLicenseEndpointPropsMixin",
):
    '''Creates a license endpoint to integrate your various licensed software used for rendering on Deadline Cloud.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-licenseendpoint.html
    :cloudformationResource: AWS::Deadline::LicenseEndpoint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
        
        cfn_license_endpoint_props_mixin = deadline_mixins.CfnLicenseEndpointPropsMixin(deadline_mixins.CfnLicenseEndpointMixinProps(
            security_group_ids=["securityGroupIds"],
            subnet_ids=["subnetIds"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_id="vpcId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLicenseEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Deadline::LicenseEndpoint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3b44ddeaa5e20720b2cd9be8bd7f8e8ee656c0d46cfa78fcaef393cba5a2e40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f21bca8a664e46cfc6c7e41b28884452bbe3dfb4c4cd5307e1a9b2d461e74047)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c47cfbeb28f97d5ec9377244969f67062a1de349d69a238d82d8f903f01a89)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLicenseEndpointMixinProps:
        return typing.cast(CfnLicenseEndpointMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnLimitMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "amount_requirement_name": "amountRequirementName",
        "description": "description",
        "display_name": "displayName",
        "farm_id": "farmId",
        "max_count": "maxCount",
    },
)
class CfnLimitMixinProps:
    def __init__(
        self,
        *,
        amount_requirement_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        farm_id: typing.Optional[builtins.str] = None,
        max_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnLimitPropsMixin.

        :param amount_requirement_name: The value that you specify as the ``name`` in the ``amounts`` field of the ``hostRequirements`` in a step of a job template to declare the limit requirement.
        :param description: A description of the limit. A clear description helps you identify the purpose of the limit. .. epigraph:: This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field. Default: - ""
        :param display_name: The name of the limit used in lists to identify the limit. .. epigraph:: This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.
        :param farm_id: The unique identifier of the farm that contains the limit.
        :param max_count: The maximum number of resources constrained by this limit. When all of the resources are in use, steps that require the limit won't be scheduled until the resource is available. The ``maxValue`` must not be 0. If the value is -1, there is no restriction on the number of resources that can be acquired for this limit.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-limit.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
            
            cfn_limit_mixin_props = deadline_mixins.CfnLimitMixinProps(
                amount_requirement_name="amountRequirementName",
                description="description",
                display_name="displayName",
                farm_id="farmId",
                max_count=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__968f7cd0bf8413021097edce3e6ae7c990be5bf68bf8cb6bc597e3f59f7b43eb)
            check_type(argname="argument amount_requirement_name", value=amount_requirement_name, expected_type=type_hints["amount_requirement_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument farm_id", value=farm_id, expected_type=type_hints["farm_id"])
            check_type(argname="argument max_count", value=max_count, expected_type=type_hints["max_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if amount_requirement_name is not None:
            self._values["amount_requirement_name"] = amount_requirement_name
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if farm_id is not None:
            self._values["farm_id"] = farm_id
        if max_count is not None:
            self._values["max_count"] = max_count

    @builtins.property
    def amount_requirement_name(self) -> typing.Optional[builtins.str]:
        '''The value that you specify as the ``name`` in the ``amounts`` field of the ``hostRequirements`` in a step of a job template to declare the limit requirement.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-limit.html#cfn-deadline-limit-amountrequirementname
        '''
        result = self._values.get("amount_requirement_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the limit. A clear description helps you identify the purpose of the limit.

        .. epigraph::

           This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.

        :default: - ""

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-limit.html#cfn-deadline-limit-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The name of the limit used in lists to identify the limit.

        .. epigraph::

           This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-limit.html#cfn-deadline-limit-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def farm_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the farm that contains the limit.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-limit.html#cfn-deadline-limit-farmid
        '''
        result = self._values.get("farm_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_count(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of resources constrained by this limit.

        When all of the resources are in use, steps that require the limit won't be scheduled until the resource is available.

        The ``maxValue`` must not be 0. If the value is -1, there is no restriction on the number of resources that can be acquired for this limit.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-limit.html#cfn-deadline-limit-maxcount
        '''
        result = self._values.get("max_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLimitMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLimitPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnLimitPropsMixin",
):
    '''Creates a limit that manages the distribution of shared resources, such as floating licenses.

    A limit can throttle work assignments, help manage workloads, and track current usage. Before you use a limit, you must associate the limit with one or more queues.

    You must add the ``amountRequirementName`` to a step in a job template to declare the limit requirement.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-limit.html
    :cloudformationResource: AWS::Deadline::Limit
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
        
        cfn_limit_props_mixin = deadline_mixins.CfnLimitPropsMixin(deadline_mixins.CfnLimitMixinProps(
            amount_requirement_name="amountRequirementName",
            description="description",
            display_name="displayName",
            farm_id="farmId",
            max_count=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLimitMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Deadline::Limit``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a468bb3741af7e7aa0ef0b9a0bf70674cc6f3d0cfc2a9741dc63c59b4b9a6945)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a3dabe49a663e8c4991f89861399c4ea30a50a7233c683fae4da566ed8f48a6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06e64e294d3cd7141ec0b4b2ddd72af537ec2d632585bc1baed52eaaed14bbb7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLimitMixinProps:
        return typing.cast(CfnLimitMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnMeteredProductMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "license_endpoint_id": "licenseEndpointId",
        "product_id": "productId",
    },
)
class CfnMeteredProductMixinProps:
    def __init__(
        self,
        *,
        license_endpoint_id: typing.Optional[builtins.str] = None,
        product_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnMeteredProductPropsMixin.

        :param license_endpoint_id: The Amazon EC2 identifier of the license endpoint.
        :param product_id: The product ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-meteredproduct.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
            
            cfn_metered_product_mixin_props = deadline_mixins.CfnMeteredProductMixinProps(
                license_endpoint_id="licenseEndpointId",
                product_id="productId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f95db545aa88d94eae9171909c2a6dd12eb9fb1786c50a54d8f6befef809c2)
            check_type(argname="argument license_endpoint_id", value=license_endpoint_id, expected_type=type_hints["license_endpoint_id"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if license_endpoint_id is not None:
            self._values["license_endpoint_id"] = license_endpoint_id
        if product_id is not None:
            self._values["product_id"] = product_id

    @builtins.property
    def license_endpoint_id(self) -> typing.Optional[builtins.str]:
        '''The Amazon EC2 identifier of the license endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-meteredproduct.html#cfn-deadline-meteredproduct-licenseendpointid
        '''
        result = self._values.get("license_endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def product_id(self) -> typing.Optional[builtins.str]:
        '''The product ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-meteredproduct.html#cfn-deadline-meteredproduct-productid
        '''
        result = self._values.get("product_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMeteredProductMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMeteredProductPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnMeteredProductPropsMixin",
):
    '''Adds a metered product.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-meteredproduct.html
    :cloudformationResource: AWS::Deadline::MeteredProduct
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
        
        cfn_metered_product_props_mixin = deadline_mixins.CfnMeteredProductPropsMixin(deadline_mixins.CfnMeteredProductMixinProps(
            license_endpoint_id="licenseEndpointId",
            product_id="productId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMeteredProductMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Deadline::MeteredProduct``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c40b9be0a679c65c89d14eae81c65650e69e172f9c1fdd278bfa99484954f400)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7e6ead475cd8e1f5d285f618c9f87d72f8415905df20e878f9ed9ea4abac838)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe647329e49365fdf05db0d9093efbd5f02e1c1f48b72556afd3d35ab27ae914)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMeteredProductMixinProps:
        return typing.cast(CfnMeteredProductMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnMonitorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "display_name": "displayName",
        "identity_center_instance_arn": "identityCenterInstanceArn",
        "role_arn": "roleArn",
        "subdomain": "subdomain",
        "tags": "tags",
    },
)
class CfnMonitorMixinProps:
    def __init__(
        self,
        *,
        display_name: typing.Optional[builtins.str] = None,
        identity_center_instance_arn: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        subdomain: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnMonitorPropsMixin.

        :param display_name: The name of the monitor that displays on the Deadline Cloud console. .. epigraph:: This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.
        :param identity_center_instance_arn: The Amazon Resource Name of the IAM Identity Center instance responsible for authenticating monitor users.
        :param role_arn: The Amazon Resource Name of the IAM role for the monitor. Users of the monitor use this role to access Deadline Cloud resources.
        :param subdomain: The subdomain used for the monitor URL. The full URL of the monitor is subdomain.Region.deadlinecloud.amazonaws.com.
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-monitor.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
            
            cfn_monitor_mixin_props = deadline_mixins.CfnMonitorMixinProps(
                display_name="displayName",
                identity_center_instance_arn="identityCenterInstanceArn",
                role_arn="roleArn",
                subdomain="subdomain",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfb8381dc82fc57b2c41babe433c36cc933e9b2a23c53d1ad6a480b887a45690)
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument identity_center_instance_arn", value=identity_center_instance_arn, expected_type=type_hints["identity_center_instance_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument subdomain", value=subdomain, expected_type=type_hints["subdomain"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if display_name is not None:
            self._values["display_name"] = display_name
        if identity_center_instance_arn is not None:
            self._values["identity_center_instance_arn"] = identity_center_instance_arn
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if subdomain is not None:
            self._values["subdomain"] = subdomain
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The name of the monitor that displays on the Deadline Cloud console.

        .. epigraph::

           This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-monitor.html#cfn-deadline-monitor-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_center_instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name of the IAM Identity Center instance responsible for authenticating monitor users.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-monitor.html#cfn-deadline-monitor-identitycenterinstancearn
        '''
        result = self._values.get("identity_center_instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name of the IAM role for the monitor.

        Users of the monitor use this role to access Deadline Cloud resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-monitor.html#cfn-deadline-monitor-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdomain(self) -> typing.Optional[builtins.str]:
        '''The subdomain used for the monitor URL.

        The full URL of the monitor is subdomain.Region.deadlinecloud.amazonaws.com.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-monitor.html#cfn-deadline-monitor-subdomain
        '''
        result = self._values.get("subdomain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-monitor.html#cfn-deadline-monitor-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMonitorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMonitorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnMonitorPropsMixin",
):
    '''Creates an AWS Deadline Cloud monitor that you can use to view your farms, queues, and fleets.

    After you submit a job, you can track the progress of the tasks and steps that make up the job, and then download the job's results.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-monitor.html
    :cloudformationResource: AWS::Deadline::Monitor
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
        
        cfn_monitor_props_mixin = deadline_mixins.CfnMonitorPropsMixin(deadline_mixins.CfnMonitorMixinProps(
            display_name="displayName",
            identity_center_instance_arn="identityCenterInstanceArn",
            role_arn="roleArn",
            subdomain="subdomain",
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
        props: typing.Union[CfnMonitorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Deadline::Monitor``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8529515356f8c00d77580c79ecc51fb80e18909c3d8881257032c063ca375189)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a980650f13bbd8cfee236987664026bc59c6f1c5b531d24bd087a1c9adc3007)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eccc8f20f2d0ffef8ca63b5bfada2a2a5a920d2c0cf883bf2618cde93f3eba0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMonitorMixinProps:
        return typing.cast(CfnMonitorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnQueueEnvironmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "farm_id": "farmId",
        "priority": "priority",
        "queue_id": "queueId",
        "template": "template",
        "template_type": "templateType",
    },
)
class CfnQueueEnvironmentMixinProps:
    def __init__(
        self,
        *,
        farm_id: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        queue_id: typing.Optional[builtins.str] = None,
        template: typing.Optional[builtins.str] = None,
        template_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnQueueEnvironmentPropsMixin.

        :param farm_id: The identifier assigned to the farm that contains the queue.
        :param priority: The queue environment's priority.
        :param queue_id: The unique identifier of the queue that contains the environment.
        :param template: A JSON or YAML template that describes the processing environment for the queue.
        :param template_type: Specifies whether the template for the queue environment is JSON or YAML.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queueenvironment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
            
            cfn_queue_environment_mixin_props = deadline_mixins.CfnQueueEnvironmentMixinProps(
                farm_id="farmId",
                priority=123,
                queue_id="queueId",
                template="template",
                template_type="templateType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67df7ce93d35948fe0f3a69ab175341dac3851c6bac1f9560dd2c7a3d98a7633)
            check_type(argname="argument farm_id", value=farm_id, expected_type=type_hints["farm_id"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument queue_id", value=queue_id, expected_type=type_hints["queue_id"])
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
            check_type(argname="argument template_type", value=template_type, expected_type=type_hints["template_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if farm_id is not None:
            self._values["farm_id"] = farm_id
        if priority is not None:
            self._values["priority"] = priority
        if queue_id is not None:
            self._values["queue_id"] = queue_id
        if template is not None:
            self._values["template"] = template
        if template_type is not None:
            self._values["template_type"] = template_type

    @builtins.property
    def farm_id(self) -> typing.Optional[builtins.str]:
        '''The identifier assigned to the farm that contains the queue.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queueenvironment.html#cfn-deadline-queueenvironment-farmid
        '''
        result = self._values.get("farm_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''The queue environment's priority.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queueenvironment.html#cfn-deadline-queueenvironment-priority
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def queue_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the queue that contains the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queueenvironment.html#cfn-deadline-queueenvironment-queueid
        '''
        result = self._values.get("queue_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional[builtins.str]:
        '''A JSON or YAML template that describes the processing environment for the queue.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queueenvironment.html#cfn-deadline-queueenvironment-template
        '''
        result = self._values.get("template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_type(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the template for the queue environment is JSON or YAML.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queueenvironment.html#cfn-deadline-queueenvironment-templatetype
        '''
        result = self._values.get("template_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnQueueEnvironmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnQueueEnvironmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnQueueEnvironmentPropsMixin",
):
    '''Creates an environment for a queue that defines how jobs in the queue run.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queueenvironment.html
    :cloudformationResource: AWS::Deadline::QueueEnvironment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
        
        cfn_queue_environment_props_mixin = deadline_mixins.CfnQueueEnvironmentPropsMixin(deadline_mixins.CfnQueueEnvironmentMixinProps(
            farm_id="farmId",
            priority=123,
            queue_id="queueId",
            template="template",
            template_type="templateType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnQueueEnvironmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Deadline::QueueEnvironment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ef3902b3573a6781fea14a9a9bc5904c0f9240a103aee077850820764a26105)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fed88421eb467ef1e14448ee97818817deef9829fd5b99f9dc3c4c9e52b7c66)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63bf7283f154b8f10b522859fd4c4243472afd364c9bb29e6bc960ee9496dd74)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnQueueEnvironmentMixinProps:
        return typing.cast(CfnQueueEnvironmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnQueueFleetAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"farm_id": "farmId", "fleet_id": "fleetId", "queue_id": "queueId"},
)
class CfnQueueFleetAssociationMixinProps:
    def __init__(
        self,
        *,
        farm_id: typing.Optional[builtins.str] = None,
        fleet_id: typing.Optional[builtins.str] = None,
        queue_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnQueueFleetAssociationPropsMixin.

        :param farm_id: The identifier of the farm that contains the queue and the fleet.
        :param fleet_id: The fleet ID.
        :param queue_id: The queue ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queuefleetassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
            
            cfn_queue_fleet_association_mixin_props = deadline_mixins.CfnQueueFleetAssociationMixinProps(
                farm_id="farmId",
                fleet_id="fleetId",
                queue_id="queueId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02ee59d4d40caf9bdabd53c9c5d701c681c1005ad67329e2981acc0bd35867d2)
            check_type(argname="argument farm_id", value=farm_id, expected_type=type_hints["farm_id"])
            check_type(argname="argument fleet_id", value=fleet_id, expected_type=type_hints["fleet_id"])
            check_type(argname="argument queue_id", value=queue_id, expected_type=type_hints["queue_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if farm_id is not None:
            self._values["farm_id"] = farm_id
        if fleet_id is not None:
            self._values["fleet_id"] = fleet_id
        if queue_id is not None:
            self._values["queue_id"] = queue_id

    @builtins.property
    def farm_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the farm that contains the queue and the fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queuefleetassociation.html#cfn-deadline-queuefleetassociation-farmid
        '''
        result = self._values.get("farm_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fleet_id(self) -> typing.Optional[builtins.str]:
        '''The fleet ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queuefleetassociation.html#cfn-deadline-queuefleetassociation-fleetid
        '''
        result = self._values.get("fleet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def queue_id(self) -> typing.Optional[builtins.str]:
        '''The queue ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queuefleetassociation.html#cfn-deadline-queuefleetassociation-queueid
        '''
        result = self._values.get("queue_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnQueueFleetAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnQueueFleetAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnQueueFleetAssociationPropsMixin",
):
    '''Creates an association between a queue and a fleet.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queuefleetassociation.html
    :cloudformationResource: AWS::Deadline::QueueFleetAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
        
        cfn_queue_fleet_association_props_mixin = deadline_mixins.CfnQueueFleetAssociationPropsMixin(deadline_mixins.CfnQueueFleetAssociationMixinProps(
            farm_id="farmId",
            fleet_id="fleetId",
            queue_id="queueId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnQueueFleetAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Deadline::QueueFleetAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7891962916de661a316728d677d70480ec7ac3ac23ae783791b0c5427b516ce1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f50f62a907c60aefb30fb9d215674d362a339b636095e5dff1fe409f5b7a7d3e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__162e3491a1197dad05a0c35f7c846c61767567ea9626727de77b1fd2c84104e1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnQueueFleetAssociationMixinProps:
        return typing.cast(CfnQueueFleetAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnQueueLimitAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"farm_id": "farmId", "limit_id": "limitId", "queue_id": "queueId"},
)
class CfnQueueLimitAssociationMixinProps:
    def __init__(
        self,
        *,
        farm_id: typing.Optional[builtins.str] = None,
        limit_id: typing.Optional[builtins.str] = None,
        queue_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnQueueLimitAssociationPropsMixin.

        :param farm_id: The unique identifier of the farm that contains the queue-limit association.
        :param limit_id: The unique identifier of the limit in the association.
        :param queue_id: The unique identifier of the queue in the association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queuelimitassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
            
            cfn_queue_limit_association_mixin_props = deadline_mixins.CfnQueueLimitAssociationMixinProps(
                farm_id="farmId",
                limit_id="limitId",
                queue_id="queueId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbc8364578231240386e7d7672f756b4ed77c489eea2abf55864c09e433e6dc2)
            check_type(argname="argument farm_id", value=farm_id, expected_type=type_hints["farm_id"])
            check_type(argname="argument limit_id", value=limit_id, expected_type=type_hints["limit_id"])
            check_type(argname="argument queue_id", value=queue_id, expected_type=type_hints["queue_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if farm_id is not None:
            self._values["farm_id"] = farm_id
        if limit_id is not None:
            self._values["limit_id"] = limit_id
        if queue_id is not None:
            self._values["queue_id"] = queue_id

    @builtins.property
    def farm_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the farm that contains the queue-limit association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queuelimitassociation.html#cfn-deadline-queuelimitassociation-farmid
        '''
        result = self._values.get("farm_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def limit_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the limit in the association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queuelimitassociation.html#cfn-deadline-queuelimitassociation-limitid
        '''
        result = self._values.get("limit_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def queue_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the queue in the association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queuelimitassociation.html#cfn-deadline-queuelimitassociation-queueid
        '''
        result = self._values.get("queue_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnQueueLimitAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnQueueLimitAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnQueueLimitAssociationPropsMixin",
):
    '''Associates a limit with a particular queue.

    After the limit is associated, all workers for jobs that specify the limit associated with the queue are subject to the limit. You can't associate two limits with the same ``amountRequirementName`` to the same queue.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queuelimitassociation.html
    :cloudformationResource: AWS::Deadline::QueueLimitAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
        
        cfn_queue_limit_association_props_mixin = deadline_mixins.CfnQueueLimitAssociationPropsMixin(deadline_mixins.CfnQueueLimitAssociationMixinProps(
            farm_id="farmId",
            limit_id="limitId",
            queue_id="queueId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnQueueLimitAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Deadline::QueueLimitAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b4ef756be91f92dd163e166f0606a0d3d8ff414b402f6dc0816692276e96ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__628168c9879931eb3e01ab06f3b172cfc7423fd7a63a2957489db29f6a87922d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff285d3f5de546d6dc47859ce17b7efabf13c6268f43aea7aeee6bdaffed0b4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnQueueLimitAssociationMixinProps:
        return typing.cast(CfnQueueLimitAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnQueueMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_storage_profile_ids": "allowedStorageProfileIds",
        "default_budget_action": "defaultBudgetAction",
        "description": "description",
        "display_name": "displayName",
        "farm_id": "farmId",
        "job_attachment_settings": "jobAttachmentSettings",
        "job_run_as_user": "jobRunAsUser",
        "required_file_system_location_names": "requiredFileSystemLocationNames",
        "role_arn": "roleArn",
        "tags": "tags",
    },
)
class CfnQueueMixinProps:
    def __init__(
        self,
        *,
        allowed_storage_profile_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_budget_action: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        farm_id: typing.Optional[builtins.str] = None,
        job_attachment_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnQueuePropsMixin.JobAttachmentSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        job_run_as_user: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnQueuePropsMixin.JobRunAsUserProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        required_file_system_location_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnQueuePropsMixin.

        :param allowed_storage_profile_ids: The identifiers of the storage profiles that this queue can use to share assets between workers using different operating systems.
        :param default_budget_action: The default action taken on a queue summary if a budget wasn't configured. Default: - "NONE"
        :param description: A description of the queue that helps identify what the queue is used for. .. epigraph:: This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field. Default: - ""
        :param display_name: The display name of the queue summary to update. .. epigraph:: This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.
        :param farm_id: The farm ID.
        :param job_attachment_settings: The job attachment settings. These are the Amazon S3 bucket name and the Amazon S3 prefix.
        :param job_run_as_user: Identifies the user for a job.
        :param required_file_system_location_names: The file system location that the queue uses.
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role that workers use when running jobs in this queue.
        :param tags: The tags to add to your queue. Each tag consists of a tag key and a tag value. Tag keys and values are both required, but tag values can be empty strings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queue.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
            
            cfn_queue_mixin_props = deadline_mixins.CfnQueueMixinProps(
                allowed_storage_profile_ids=["allowedStorageProfileIds"],
                default_budget_action="defaultBudgetAction",
                description="description",
                display_name="displayName",
                farm_id="farmId",
                job_attachment_settings=deadline_mixins.CfnQueuePropsMixin.JobAttachmentSettingsProperty(
                    root_prefix="rootPrefix",
                    s3_bucket_name="s3BucketName"
                ),
                job_run_as_user=deadline_mixins.CfnQueuePropsMixin.JobRunAsUserProperty(
                    posix=deadline_mixins.CfnQueuePropsMixin.PosixUserProperty(
                        group="group",
                        user="user"
                    ),
                    run_as="runAs",
                    windows=deadline_mixins.CfnQueuePropsMixin.WindowsUserProperty(
                        password_arn="passwordArn",
                        user="user"
                    )
                ),
                required_file_system_location_names=["requiredFileSystemLocationNames"],
                role_arn="roleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ad21f2d6559820d37afa9ab46c774a64ae0d9de14ebf94b325aac369be85dd1)
            check_type(argname="argument allowed_storage_profile_ids", value=allowed_storage_profile_ids, expected_type=type_hints["allowed_storage_profile_ids"])
            check_type(argname="argument default_budget_action", value=default_budget_action, expected_type=type_hints["default_budget_action"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument farm_id", value=farm_id, expected_type=type_hints["farm_id"])
            check_type(argname="argument job_attachment_settings", value=job_attachment_settings, expected_type=type_hints["job_attachment_settings"])
            check_type(argname="argument job_run_as_user", value=job_run_as_user, expected_type=type_hints["job_run_as_user"])
            check_type(argname="argument required_file_system_location_names", value=required_file_system_location_names, expected_type=type_hints["required_file_system_location_names"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_storage_profile_ids is not None:
            self._values["allowed_storage_profile_ids"] = allowed_storage_profile_ids
        if default_budget_action is not None:
            self._values["default_budget_action"] = default_budget_action
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if farm_id is not None:
            self._values["farm_id"] = farm_id
        if job_attachment_settings is not None:
            self._values["job_attachment_settings"] = job_attachment_settings
        if job_run_as_user is not None:
            self._values["job_run_as_user"] = job_run_as_user
        if required_file_system_location_names is not None:
            self._values["required_file_system_location_names"] = required_file_system_location_names
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def allowed_storage_profile_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The identifiers of the storage profiles that this queue can use to share assets between workers using different operating systems.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queue.html#cfn-deadline-queue-allowedstorageprofileids
        '''
        result = self._values.get("allowed_storage_profile_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_budget_action(self) -> typing.Optional[builtins.str]:
        '''The default action taken on a queue summary if a budget wasn't configured.

        :default: - "NONE"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queue.html#cfn-deadline-queue-defaultbudgetaction
        '''
        result = self._values.get("default_budget_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the queue that helps identify what the queue is used for.

        .. epigraph::

           This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.

        :default: - ""

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queue.html#cfn-deadline-queue-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the queue summary to update.

        .. epigraph::

           This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queue.html#cfn-deadline-queue-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def farm_id(self) -> typing.Optional[builtins.str]:
        '''The farm ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queue.html#cfn-deadline-queue-farmid
        '''
        result = self._values.get("farm_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_attachment_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQueuePropsMixin.JobAttachmentSettingsProperty"]]:
        '''The job attachment settings.

        These are the Amazon S3 bucket name and the Amazon S3 prefix.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queue.html#cfn-deadline-queue-jobattachmentsettings
        '''
        result = self._values.get("job_attachment_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQueuePropsMixin.JobAttachmentSettingsProperty"]], result)

    @builtins.property
    def job_run_as_user(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQueuePropsMixin.JobRunAsUserProperty"]]:
        '''Identifies the user for a job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queue.html#cfn-deadline-queue-jobrunasuser
        '''
        result = self._values.get("job_run_as_user")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQueuePropsMixin.JobRunAsUserProperty"]], result)

    @builtins.property
    def required_file_system_location_names(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The file system location that the queue uses.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queue.html#cfn-deadline-queue-requiredfilesystemlocationnames
        '''
        result = self._values.get("required_file_system_location_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role that workers use when running jobs in this queue.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queue.html#cfn-deadline-queue-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to add to your queue.

        Each tag consists of a tag key and a tag value. Tag keys and values are both required, but tag values can be empty strings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queue.html#cfn-deadline-queue-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnQueueMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnQueuePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnQueuePropsMixin",
):
    '''Creates a queue to coordinate the order in which jobs run on a farm.

    A queue can also specify where to pull resources and indicate where to output completed jobs.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-queue.html
    :cloudformationResource: AWS::Deadline::Queue
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
        
        cfn_queue_props_mixin = deadline_mixins.CfnQueuePropsMixin(deadline_mixins.CfnQueueMixinProps(
            allowed_storage_profile_ids=["allowedStorageProfileIds"],
            default_budget_action="defaultBudgetAction",
            description="description",
            display_name="displayName",
            farm_id="farmId",
            job_attachment_settings=deadline_mixins.CfnQueuePropsMixin.JobAttachmentSettingsProperty(
                root_prefix="rootPrefix",
                s3_bucket_name="s3BucketName"
            ),
            job_run_as_user=deadline_mixins.CfnQueuePropsMixin.JobRunAsUserProperty(
                posix=deadline_mixins.CfnQueuePropsMixin.PosixUserProperty(
                    group="group",
                    user="user"
                ),
                run_as="runAs",
                windows=deadline_mixins.CfnQueuePropsMixin.WindowsUserProperty(
                    password_arn="passwordArn",
                    user="user"
                )
            ),
            required_file_system_location_names=["requiredFileSystemLocationNames"],
            role_arn="roleArn",
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
        props: typing.Union[CfnQueueMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Deadline::Queue``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe6b51dc4c9ba04ee88fbfaa4d3c0db4c9d9a58dbca7915aa9be68b09a99cee4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0adaf535a7ebe119f76d006db552c36127b98cfe46540b894474c3af5fc8d19d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7602ffd0419a5e87223e281230d5ceb2ae25450b1dbb86016b0b06706291cf9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnQueueMixinProps:
        return typing.cast(CfnQueueMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnQueuePropsMixin.JobAttachmentSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"root_prefix": "rootPrefix", "s3_bucket_name": "s3BucketName"},
    )
    class JobAttachmentSettingsProperty:
        def __init__(
            self,
            *,
            root_prefix: typing.Optional[builtins.str] = None,
            s3_bucket_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The job attachment settings.

            These are the Amazon S3 bucket name and the Amazon S3 prefix.

            :param root_prefix: The root prefix.
            :param s3_bucket_name: The Amazon S3 bucket name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-queue-jobattachmentsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                job_attachment_settings_property = deadline_mixins.CfnQueuePropsMixin.JobAttachmentSettingsProperty(
                    root_prefix="rootPrefix",
                    s3_bucket_name="s3BucketName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a6f0b544e2c27573358d0e65297cb3e4e0b8064760ec2fbca2c1d7118f30295)
                check_type(argname="argument root_prefix", value=root_prefix, expected_type=type_hints["root_prefix"])
                check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if root_prefix is not None:
                self._values["root_prefix"] = root_prefix
            if s3_bucket_name is not None:
                self._values["s3_bucket_name"] = s3_bucket_name

        @builtins.property
        def root_prefix(self) -> typing.Optional[builtins.str]:
            '''The root prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-queue-jobattachmentsettings.html#cfn-deadline-queue-jobattachmentsettings-rootprefix
            '''
            result = self._values.get("root_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_bucket_name(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 bucket name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-queue-jobattachmentsettings.html#cfn-deadline-queue-jobattachmentsettings-s3bucketname
            '''
            result = self._values.get("s3_bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JobAttachmentSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnQueuePropsMixin.JobRunAsUserProperty",
        jsii_struct_bases=[],
        name_mapping={"posix": "posix", "run_as": "runAs", "windows": "windows"},
    )
    class JobRunAsUserProperty:
        def __init__(
            self,
            *,
            posix: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnQueuePropsMixin.PosixUserProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            run_as: typing.Optional[builtins.str] = None,
            windows: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnQueuePropsMixin.WindowsUserProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Identifies the user for a job.

            :param posix: The user and group that the jobs in the queue run as.
            :param run_as: Specifies whether the job should run using the queue's system user or if the job should run using the worker agent system user.
            :param windows: Identifies a Microsoft Windows user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-queue-jobrunasuser.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                job_run_as_user_property = deadline_mixins.CfnQueuePropsMixin.JobRunAsUserProperty(
                    posix=deadline_mixins.CfnQueuePropsMixin.PosixUserProperty(
                        group="group",
                        user="user"
                    ),
                    run_as="runAs",
                    windows=deadline_mixins.CfnQueuePropsMixin.WindowsUserProperty(
                        password_arn="passwordArn",
                        user="user"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__efe80a3994fb75d3590ca08c4e2de8f9512c7c392c0739bd5d43974b8c8554fa)
                check_type(argname="argument posix", value=posix, expected_type=type_hints["posix"])
                check_type(argname="argument run_as", value=run_as, expected_type=type_hints["run_as"])
                check_type(argname="argument windows", value=windows, expected_type=type_hints["windows"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if posix is not None:
                self._values["posix"] = posix
            if run_as is not None:
                self._values["run_as"] = run_as
            if windows is not None:
                self._values["windows"] = windows

        @builtins.property
        def posix(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQueuePropsMixin.PosixUserProperty"]]:
            '''The user and group that the jobs in the queue run as.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-queue-jobrunasuser.html#cfn-deadline-queue-jobrunasuser-posix
            '''
            result = self._values.get("posix")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQueuePropsMixin.PosixUserProperty"]], result)

        @builtins.property
        def run_as(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the job should run using the queue's system user or if the job should run using the worker agent system user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-queue-jobrunasuser.html#cfn-deadline-queue-jobrunasuser-runas
            '''
            result = self._values.get("run_as")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def windows(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQueuePropsMixin.WindowsUserProperty"]]:
            '''Identifies a Microsoft Windows user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-queue-jobrunasuser.html#cfn-deadline-queue-jobrunasuser-windows
            '''
            result = self._values.get("windows")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQueuePropsMixin.WindowsUserProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JobRunAsUserProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnQueuePropsMixin.PosixUserProperty",
        jsii_struct_bases=[],
        name_mapping={"group": "group", "user": "user"},
    )
    class PosixUserProperty:
        def __init__(
            self,
            *,
            group: typing.Optional[builtins.str] = None,
            user: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The POSIX user.

            :param group: The name of the POSIX user's group.
            :param user: The name of the POSIX user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-queue-posixuser.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                posix_user_property = deadline_mixins.CfnQueuePropsMixin.PosixUserProperty(
                    group="group",
                    user="user"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b477342c05f17c0a3c8a180d0ea583b13589bb9258e5d3f9806b8e1ce03c3755)
                check_type(argname="argument group", value=group, expected_type=type_hints["group"])
                check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group is not None:
                self._values["group"] = group
            if user is not None:
                self._values["user"] = user

        @builtins.property
        def group(self) -> typing.Optional[builtins.str]:
            '''The name of the POSIX user's group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-queue-posixuser.html#cfn-deadline-queue-posixuser-group
            '''
            result = self._values.get("group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user(self) -> typing.Optional[builtins.str]:
            '''The name of the POSIX user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-queue-posixuser.html#cfn-deadline-queue-posixuser-user
            '''
            result = self._values.get("user")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PosixUserProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnQueuePropsMixin.WindowsUserProperty",
        jsii_struct_bases=[],
        name_mapping={"password_arn": "passwordArn", "user": "user"},
    )
    class WindowsUserProperty:
        def __init__(
            self,
            *,
            password_arn: typing.Optional[builtins.str] = None,
            user: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Windows user details.

            :param password_arn: The password ARN for the Windows user.
            :param user: The user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-queue-windowsuser.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                windows_user_property = deadline_mixins.CfnQueuePropsMixin.WindowsUserProperty(
                    password_arn="passwordArn",
                    user="user"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9aaea62a10b246e26bf01ca61073feb31ac5778e304e5a68fe589899219d68cd)
                check_type(argname="argument password_arn", value=password_arn, expected_type=type_hints["password_arn"])
                check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if password_arn is not None:
                self._values["password_arn"] = password_arn
            if user is not None:
                self._values["user"] = user

        @builtins.property
        def password_arn(self) -> typing.Optional[builtins.str]:
            '''The password ARN for the Windows user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-queue-windowsuser.html#cfn-deadline-queue-windowsuser-passwordarn
            '''
            result = self._values.get("password_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user(self) -> typing.Optional[builtins.str]:
            '''The user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-queue-windowsuser.html#cfn-deadline-queue-windowsuser-user
            '''
            result = self._values.get("user")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WindowsUserProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnStorageProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "display_name": "displayName",
        "farm_id": "farmId",
        "file_system_locations": "fileSystemLocations",
        "os_family": "osFamily",
    },
)
class CfnStorageProfileMixinProps:
    def __init__(
        self,
        *,
        display_name: typing.Optional[builtins.str] = None,
        farm_id: typing.Optional[builtins.str] = None,
        file_system_locations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageProfilePropsMixin.FileSystemLocationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        os_family: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnStorageProfilePropsMixin.

        :param display_name: The display name of the storage profile summary to update. .. epigraph:: This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.
        :param farm_id: The unique identifier of the farm that contains the storage profile.
        :param file_system_locations: Operating system specific file system path to the storage location.
        :param os_family: The operating system (OS) family.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-storageprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
            
            cfn_storage_profile_mixin_props = deadline_mixins.CfnStorageProfileMixinProps(
                display_name="displayName",
                farm_id="farmId",
                file_system_locations=[deadline_mixins.CfnStorageProfilePropsMixin.FileSystemLocationProperty(
                    name="name",
                    path="path",
                    type="type"
                )],
                os_family="osFamily"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a78f6c713151d7cd644701784f4ec3983ea9538df69e7e3db8efff40d90b9e)
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument farm_id", value=farm_id, expected_type=type_hints["farm_id"])
            check_type(argname="argument file_system_locations", value=file_system_locations, expected_type=type_hints["file_system_locations"])
            check_type(argname="argument os_family", value=os_family, expected_type=type_hints["os_family"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if display_name is not None:
            self._values["display_name"] = display_name
        if farm_id is not None:
            self._values["farm_id"] = farm_id
        if file_system_locations is not None:
            self._values["file_system_locations"] = file_system_locations
        if os_family is not None:
            self._values["os_family"] = os_family

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the storage profile summary to update.

        .. epigraph::

           This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-storageprofile.html#cfn-deadline-storageprofile-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def farm_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the farm that contains the storage profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-storageprofile.html#cfn-deadline-storageprofile-farmid
        '''
        result = self._values.get("farm_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_system_locations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageProfilePropsMixin.FileSystemLocationProperty"]]]]:
        '''Operating system specific file system path to the storage location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-storageprofile.html#cfn-deadline-storageprofile-filesystemlocations
        '''
        result = self._values.get("file_system_locations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageProfilePropsMixin.FileSystemLocationProperty"]]]], result)

    @builtins.property
    def os_family(self) -> typing.Optional[builtins.str]:
        '''The operating system (OS) family.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-storageprofile.html#cfn-deadline-storageprofile-osfamily
        '''
        result = self._values.get("os_family")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStorageProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStorageProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnStorageProfilePropsMixin",
):
    '''Creates a storage profile that specifies the operating system, file type, and file location of resources used on a farm.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-deadline-storageprofile.html
    :cloudformationResource: AWS::Deadline::StorageProfile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
        
        cfn_storage_profile_props_mixin = deadline_mixins.CfnStorageProfilePropsMixin(deadline_mixins.CfnStorageProfileMixinProps(
            display_name="displayName",
            farm_id="farmId",
            file_system_locations=[deadline_mixins.CfnStorageProfilePropsMixin.FileSystemLocationProperty(
                name="name",
                path="path",
                type="type"
            )],
            os_family="osFamily"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStorageProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Deadline::StorageProfile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eb79f64a3c3de1e5a7b07239662f536540994376dffd0e691fca7c664d9a37e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3962cc4d291ca30d16a6ff6cf3f44f4566261a23a5af4e60a275a41ddad6abe5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec4fd9b48bce793373c984e6553fa0e5ac0c4826b5a3a4eb4919490b2c2297eb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStorageProfileMixinProps:
        return typing.cast(CfnStorageProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_deadline.mixins.CfnStorageProfilePropsMixin.FileSystemLocationProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "path": "path", "type": "type"},
    )
    class FileSystemLocationProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The details of the file system location for the resource.

            :param name: The location name.
            :param path: The file path.
            :param type: The type of file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-storageprofile-filesystemlocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_deadline import mixins as deadline_mixins
                
                file_system_location_property = deadline_mixins.CfnStorageProfilePropsMixin.FileSystemLocationProperty(
                    name="name",
                    path="path",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c37daca99871e2556d64fe8f5396f2925e7f9cc82eccd18d42341546089813ba)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if path is not None:
                self._values["path"] = path
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The location name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-storageprofile-filesystemlocation.html#cfn-deadline-storageprofile-filesystemlocation-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The file path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-storageprofile-filesystemlocation.html#cfn-deadline-storageprofile-filesystemlocation-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-deadline-storageprofile-filesystemlocation.html#cfn-deadline-storageprofile-filesystemlocation-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FileSystemLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnFarmMixinProps",
    "CfnFarmPropsMixin",
    "CfnFleetMixinProps",
    "CfnFleetPropsMixin",
    "CfnLicenseEndpointMixinProps",
    "CfnLicenseEndpointPropsMixin",
    "CfnLimitMixinProps",
    "CfnLimitPropsMixin",
    "CfnMeteredProductMixinProps",
    "CfnMeteredProductPropsMixin",
    "CfnMonitorMixinProps",
    "CfnMonitorPropsMixin",
    "CfnQueueEnvironmentMixinProps",
    "CfnQueueEnvironmentPropsMixin",
    "CfnQueueFleetAssociationMixinProps",
    "CfnQueueFleetAssociationPropsMixin",
    "CfnQueueLimitAssociationMixinProps",
    "CfnQueueLimitAssociationPropsMixin",
    "CfnQueueMixinProps",
    "CfnQueuePropsMixin",
    "CfnStorageProfileMixinProps",
    "CfnStorageProfilePropsMixin",
]

publication.publish()

def _typecheckingstub__b2df8ba71ae997ba65799f5ac27c965b17eafc7116b60ea7ea7cda67fb4dfb2a(
    *,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73364b54e637816086e29282ea6d68de797186b04e8038a2e3a861c1774aee95(
    props: typing.Union[CfnFarmMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b5ca645657d0411362cf8732895d2bc667d29e7bb3faaec4779c9162288ef2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3992a85be6840d9b880f5bcf70b9dcedb375651ab91ae85d344c253da4dc68(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04ae7694ea50baf6f78be852c4941b3e89922a4c55f4feacd71af93d50cb861(
    *,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.FleetConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    farm_id: typing.Optional[builtins.str] = None,
    host_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.HostConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_worker_count: typing.Optional[jsii.Number] = None,
    min_worker_count: typing.Optional[jsii.Number] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8fe7923e3c23a21781df8ca59e3d8f8c31316c18b9173672707f5a5812a26b7(
    props: typing.Union[CfnFleetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44cd05278eb50cc23b4fff034c9dc5ea2ee8bdb9609105c8593db8a245e39d85(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2efa1e7e6815ed767373e01b394a1fef6c69ee023970e0a5f20169134c53a52(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__615a3db5a18205301277a9a683b993ef55e80b47b25a09e256523b7f031fabe8(
    *,
    count: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.AcceleratorCountRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    selections: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.AcceleratorSelectionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1308ca47d748cf0d52a37c93dce9b51bf2bc946d9ad163c6b9ee65f0b366da(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f563d51f47dda6d80604bbf899c89b034791231d83f04a531685058fe71c2ba(
    *,
    name: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f22615b3b4c8df76a0a1af2c9ea2e08464a53390c4263381a4b93bf315011584(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e112161d4c500188f7155aa04ec4aec4ea219bc01c1175855d167b57b88bc171(
    *,
    mode: typing.Optional[builtins.str] = None,
    storage_profile_id: typing.Optional[builtins.str] = None,
    tag_propagation_mode: typing.Optional[builtins.str] = None,
    worker_capabilities: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.CustomerManagedWorkerCapabilitiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__137e014a3abac45c704760e14d6a1693e53c0098e4c3485fb98426671a35b07f(
    *,
    accelerator_count: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.AcceleratorCountRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    accelerator_total_memory_mib: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.AcceleratorTotalMemoryMiBRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    accelerator_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    cpu_architecture_type: typing.Optional[builtins.str] = None,
    custom_amounts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.FleetAmountCapabilityProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    custom_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.FleetAttributeCapabilityProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    memory_mib: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.MemoryMiBRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    os_family: typing.Optional[builtins.str] = None,
    v_cpu_count: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.VCpuCountRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__359083b8a91ba19721baa3abc36eae18dc3c9e3cbf3186ff91ff76e0349ea904(
    *,
    iops: typing.Optional[jsii.Number] = None,
    size_gib: typing.Optional[jsii.Number] = None,
    throughput_mib: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8335870bb662bae87b2bf9409ea6c05c99bf2d270430dcd5914a733f9b22bd6(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8973c1508221de9dd62fc896e62fefb7af719381073d5be5f6af668e6dafd391(
    *,
    name: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d38790a2d13f6b579851039500f9a8732f5ccb2d23941a8661e4c6ef7e68c9(
    *,
    amounts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.FleetAmountCapabilityProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.FleetAttributeCapabilityProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ada7c8b4bdb0b51a04fcbe0d38580fabcadeb7a3814eea58457055caa5adc3(
    *,
    customer_managed: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.CustomerManagedFleetConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_managed_ec2: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.ServiceManagedEc2FleetConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17334a96ecc5531cee85fe4631f71280797fc8db3121d638d8c084c974e67410(
    *,
    script_body: typing.Optional[builtins.str] = None,
    script_timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aaa3be25a74ed5edc057bdf76ad354a621d48c35be0e75a591c9879fc3900e9(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__830bb132c3c5149884ddbcfe2d48fff41261b1ae284d0a10b64a9a9c794e80dc(
    *,
    instance_capabilities: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.ServiceManagedEc2InstanceCapabilitiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_market_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.ServiceManagedEc2InstanceMarketOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    storage_profile_id: typing.Optional[builtins.str] = None,
    vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.VpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__855b722e9d5e0e80aae97b20946bbc37aac4393c77912a35dcf1c51f76e160d2(
    *,
    accelerator_capabilities: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.AcceleratorCapabilitiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    allowed_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    cpu_architecture_type: typing.Optional[builtins.str] = None,
    custom_amounts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.FleetAmountCapabilityProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    custom_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.FleetAttributeCapabilityProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    excluded_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory_mib: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.MemoryMiBRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    os_family: typing.Optional[builtins.str] = None,
    root_ebs_volume: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.Ec2EbsVolumeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    v_cpu_count: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.VCpuCountRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c381613bc0eec7d8acef73e175ff26bec05118685314b37430b5456e14f1b4b(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b2eada1759cd1cd4f65fa4417cd1193f72e0f889f20602276156d70e5e97a5e(
    *,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9067a6087728fb79500cccaecada40abefce168b582a35c0a88510df6c0ede39(
    *,
    resource_configuration_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ddc36b4ff6dfab52f6354cd8f40ade7aed7963ecdb998f1d0b56580740e5c6(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3b44ddeaa5e20720b2cd9be8bd7f8e8ee656c0d46cfa78fcaef393cba5a2e40(
    props: typing.Union[CfnLicenseEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f21bca8a664e46cfc6c7e41b28884452bbe3dfb4c4cd5307e1a9b2d461e74047(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c47cfbeb28f97d5ec9377244969f67062a1de349d69a238d82d8f903f01a89(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__968f7cd0bf8413021097edce3e6ae7c990be5bf68bf8cb6bc597e3f59f7b43eb(
    *,
    amount_requirement_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    farm_id: typing.Optional[builtins.str] = None,
    max_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a468bb3741af7e7aa0ef0b9a0bf70674cc6f3d0cfc2a9741dc63c59b4b9a6945(
    props: typing.Union[CfnLimitMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a3dabe49a663e8c4991f89861399c4ea30a50a7233c683fae4da566ed8f48a6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e64e294d3cd7141ec0b4b2ddd72af537ec2d632585bc1baed52eaaed14bbb7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f95db545aa88d94eae9171909c2a6dd12eb9fb1786c50a54d8f6befef809c2(
    *,
    license_endpoint_id: typing.Optional[builtins.str] = None,
    product_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c40b9be0a679c65c89d14eae81c65650e69e172f9c1fdd278bfa99484954f400(
    props: typing.Union[CfnMeteredProductMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7e6ead475cd8e1f5d285f618c9f87d72f8415905df20e878f9ed9ea4abac838(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe647329e49365fdf05db0d9093efbd5f02e1c1f48b72556afd3d35ab27ae914(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb8381dc82fc57b2c41babe433c36cc933e9b2a23c53d1ad6a480b887a45690(
    *,
    display_name: typing.Optional[builtins.str] = None,
    identity_center_instance_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    subdomain: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8529515356f8c00d77580c79ecc51fb80e18909c3d8881257032c063ca375189(
    props: typing.Union[CfnMonitorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a980650f13bbd8cfee236987664026bc59c6f1c5b531d24bd087a1c9adc3007(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eccc8f20f2d0ffef8ca63b5bfada2a2a5a920d2c0cf883bf2618cde93f3eba0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67df7ce93d35948fe0f3a69ab175341dac3851c6bac1f9560dd2c7a3d98a7633(
    *,
    farm_id: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    queue_id: typing.Optional[builtins.str] = None,
    template: typing.Optional[builtins.str] = None,
    template_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef3902b3573a6781fea14a9a9bc5904c0f9240a103aee077850820764a26105(
    props: typing.Union[CfnQueueEnvironmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fed88421eb467ef1e14448ee97818817deef9829fd5b99f9dc3c4c9e52b7c66(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63bf7283f154b8f10b522859fd4c4243472afd364c9bb29e6bc960ee9496dd74(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ee59d4d40caf9bdabd53c9c5d701c681c1005ad67329e2981acc0bd35867d2(
    *,
    farm_id: typing.Optional[builtins.str] = None,
    fleet_id: typing.Optional[builtins.str] = None,
    queue_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7891962916de661a316728d677d70480ec7ac3ac23ae783791b0c5427b516ce1(
    props: typing.Union[CfnQueueFleetAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f50f62a907c60aefb30fb9d215674d362a339b636095e5dff1fe409f5b7a7d3e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__162e3491a1197dad05a0c35f7c846c61767567ea9626727de77b1fd2c84104e1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbc8364578231240386e7d7672f756b4ed77c489eea2abf55864c09e433e6dc2(
    *,
    farm_id: typing.Optional[builtins.str] = None,
    limit_id: typing.Optional[builtins.str] = None,
    queue_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b4ef756be91f92dd163e166f0606a0d3d8ff414b402f6dc0816692276e96ab(
    props: typing.Union[CfnQueueLimitAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__628168c9879931eb3e01ab06f3b172cfc7423fd7a63a2957489db29f6a87922d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff285d3f5de546d6dc47859ce17b7efabf13c6268f43aea7aeee6bdaffed0b4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad21f2d6559820d37afa9ab46c774a64ae0d9de14ebf94b325aac369be85dd1(
    *,
    allowed_storage_profile_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_budget_action: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    farm_id: typing.Optional[builtins.str] = None,
    job_attachment_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnQueuePropsMixin.JobAttachmentSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    job_run_as_user: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnQueuePropsMixin.JobRunAsUserProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    required_file_system_location_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe6b51dc4c9ba04ee88fbfaa4d3c0db4c9d9a58dbca7915aa9be68b09a99cee4(
    props: typing.Union[CfnQueueMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0adaf535a7ebe119f76d006db552c36127b98cfe46540b894474c3af5fc8d19d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7602ffd0419a5e87223e281230d5ceb2ae25450b1dbb86016b0b06706291cf9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a6f0b544e2c27573358d0e65297cb3e4e0b8064760ec2fbca2c1d7118f30295(
    *,
    root_prefix: typing.Optional[builtins.str] = None,
    s3_bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe80a3994fb75d3590ca08c4e2de8f9512c7c392c0739bd5d43974b8c8554fa(
    *,
    posix: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnQueuePropsMixin.PosixUserProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    run_as: typing.Optional[builtins.str] = None,
    windows: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnQueuePropsMixin.WindowsUserProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b477342c05f17c0a3c8a180d0ea583b13589bb9258e5d3f9806b8e1ce03c3755(
    *,
    group: typing.Optional[builtins.str] = None,
    user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aaea62a10b246e26bf01ca61073feb31ac5778e304e5a68fe589899219d68cd(
    *,
    password_arn: typing.Optional[builtins.str] = None,
    user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a78f6c713151d7cd644701784f4ec3983ea9538df69e7e3db8efff40d90b9e(
    *,
    display_name: typing.Optional[builtins.str] = None,
    farm_id: typing.Optional[builtins.str] = None,
    file_system_locations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageProfilePropsMixin.FileSystemLocationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    os_family: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eb79f64a3c3de1e5a7b07239662f536540994376dffd0e691fca7c664d9a37e(
    props: typing.Union[CfnStorageProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3962cc4d291ca30d16a6ff6cf3f44f4566261a23a5af4e60a275a41ddad6abe5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec4fd9b48bce793373c984e6553fa0e5ac0c4826b5a3a4eb4919490b2c2297eb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37daca99871e2556d64fe8f5396f2925e7f9cc82eccd18d42341546089813ba(
    *,
    name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
