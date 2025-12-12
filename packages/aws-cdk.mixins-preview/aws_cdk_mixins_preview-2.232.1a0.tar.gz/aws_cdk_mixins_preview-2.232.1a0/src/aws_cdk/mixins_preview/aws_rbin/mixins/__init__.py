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
    jsii_type="@aws-cdk/mixins-preview.aws_rbin.mixins.CfnRuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "exclude_resource_tags": "excludeResourceTags",
        "lock_configuration": "lockConfiguration",
        "resource_tags": "resourceTags",
        "resource_type": "resourceType",
        "retention_period": "retentionPeriod",
        "status": "status",
        "tags": "tags",
    },
)
class CfnRuleMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        exclude_resource_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.ResourceTagProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        lock_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.UnlockDelayProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        resource_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.ResourceTagProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        resource_type: typing.Optional[builtins.str] = None,
        retention_period: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.RetentionPeriodProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnRulePropsMixin.

        :param description: The retention rule description.
        :param exclude_resource_tags: [Region-level retention rules only] Specifies the exclusion tags to use to identify resources that are to be excluded, or ignored, by a Region-level retention rule. Resources that have any of these tags are not retained by the retention rule upon deletion. You can't specify exclusion tags for tag-level retention rules.
        :param lock_configuration: Information about the retention rule lock configuration.
        :param resource_tags: [Tag-level retention rules only] Specifies the resource tags to use to identify resources that are to be retained by a tag-level retention rule. For tag-level retention rules, only deleted resources, of the specified resource type, that have one or more of the specified tag key and value pairs are retained. If a resource is deleted, but it does not have any of the specified tag key and value pairs, it is immediately deleted without being retained by the retention rule. You can add the same tag key and value pair to a maximum or five retention rules. To create a Region-level retention rule, omit this parameter. A Region-level retention rule does not have any resource tags specified. It retains all deleted resources of the specified resource type in the Region in which the rule is created, even if the resources are not tagged.
        :param resource_type: The resource type to be retained by the retention rule. Currently, only EBS volumes, EBS snapshots, and EBS-backed AMIs are supported. - To retain EBS volumes, specify ``EBS_VOLUME`` . - To retain EBS snapshots, specify ``EBS_SNAPSHOT`` - To retain EBS-backed AMIs, specify ``EC2_IMAGE`` .
        :param retention_period: Information about the retention period for which the retention rule is to retain resources.
        :param status: The state of the retention rule. Only retention rules that are in the ``available`` state retain resources.
        :param tags: Information about the tags to assign to the retention rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rbin-rule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rbin import mixins as rbin_mixins
            
            cfn_rule_mixin_props = rbin_mixins.CfnRuleMixinProps(
                description="description",
                exclude_resource_tags=[rbin_mixins.CfnRulePropsMixin.ResourceTagProperty(
                    resource_tag_key="resourceTagKey",
                    resource_tag_value="resourceTagValue"
                )],
                lock_configuration=rbin_mixins.CfnRulePropsMixin.UnlockDelayProperty(
                    unlock_delay_unit="unlockDelayUnit",
                    unlock_delay_value=123
                ),
                resource_tags=[rbin_mixins.CfnRulePropsMixin.ResourceTagProperty(
                    resource_tag_key="resourceTagKey",
                    resource_tag_value="resourceTagValue"
                )],
                resource_type="resourceType",
                retention_period=rbin_mixins.CfnRulePropsMixin.RetentionPeriodProperty(
                    retention_period_unit="retentionPeriodUnit",
                    retention_period_value=123
                ),
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66bc12f64f07b179bb04ccccb79c4dc2db5837ab5097cb37bda927c139ea2a07)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument exclude_resource_tags", value=exclude_resource_tags, expected_type=type_hints["exclude_resource_tags"])
            check_type(argname="argument lock_configuration", value=lock_configuration, expected_type=type_hints["lock_configuration"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if exclude_resource_tags is not None:
            self._values["exclude_resource_tags"] = exclude_resource_tags
        if lock_configuration is not None:
            self._values["lock_configuration"] = lock_configuration
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if retention_period is not None:
            self._values["retention_period"] = retention_period
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The retention rule description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rbin-rule.html#cfn-rbin-rule-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclude_resource_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.ResourceTagProperty"]]]]:
        '''[Region-level retention rules only] Specifies the exclusion tags to use to identify resources that are to be excluded, or ignored, by a Region-level retention rule.

        Resources that have any of these tags are not retained by the retention rule upon deletion.

        You can't specify exclusion tags for tag-level retention rules.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rbin-rule.html#cfn-rbin-rule-excluderesourcetags
        '''
        result = self._values.get("exclude_resource_tags")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.ResourceTagProperty"]]]], result)

    @builtins.property
    def lock_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.UnlockDelayProperty"]]:
        '''Information about the retention rule lock configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rbin-rule.html#cfn-rbin-rule-lockconfiguration
        '''
        result = self._values.get("lock_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.UnlockDelayProperty"]], result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.ResourceTagProperty"]]]]:
        '''[Tag-level retention rules only] Specifies the resource tags to use to identify resources that are to be retained by a tag-level retention rule.

        For tag-level retention rules, only deleted resources, of the specified resource type, that have one or more of the specified tag key and value pairs are retained. If a resource is deleted, but it does not have any of the specified tag key and value pairs, it is immediately deleted without being retained by the retention rule.

        You can add the same tag key and value pair to a maximum or five retention rules.

        To create a Region-level retention rule, omit this parameter. A Region-level retention rule does not have any resource tags specified. It retains all deleted resources of the specified resource type in the Region in which the rule is created, even if the resources are not tagged.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rbin-rule.html#cfn-rbin-rule-resourcetags
        '''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.ResourceTagProperty"]]]], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''The resource type to be retained by the retention rule.

        Currently, only EBS volumes, EBS snapshots, and EBS-backed AMIs are supported.

        - To retain EBS volumes, specify ``EBS_VOLUME`` .
        - To retain EBS snapshots, specify ``EBS_SNAPSHOT``
        - To retain EBS-backed AMIs, specify ``EC2_IMAGE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rbin-rule.html#cfn-rbin-rule-resourcetype
        '''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_period(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.RetentionPeriodProperty"]]:
        '''Information about the retention period for which the retention rule is to retain resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rbin-rule.html#cfn-rbin-rule-retentionperiod
        '''
        result = self._values.get("retention_period")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.RetentionPeriodProperty"]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The state of the retention rule.

        Only retention rules that are in the ``available`` state retain resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rbin-rule.html#cfn-rbin-rule-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Information about the tags to assign to the retention rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rbin-rule.html#cfn-rbin-rule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rbin.mixins.CfnRulePropsMixin",
):
    '''Creates a Recycle Bin retention rule. You can create two types of retention rules:.

    - *Tag-level retention rules* - These retention rules use resource tags to identify the resources to protect. For each retention rule, you specify one or more tag key and value pairs. Resources (of the specified type) that have at least one of these tag key and value pairs are automatically retained in the Recycle Bin upon deletion. Use this type of retention rule to protect specific resources in your account based on their tags.
    - *Region-level retention rules* - These retention rules, by default, apply to all of the resources (of the specified type) in the Region, even if the resources are not tagged. However, you can specify exclusion tags to exclude resources that have specific tags. Use this type of retention rule to protect all resources of a specific type in a Region.

    For more information, see `Create Recycle Bin retention rules <https://docs.aws.amazon.com/ebs/latest/userguide/recycle-bin.html>`_ in the *Amazon EBS User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rbin-rule.html
    :cloudformationResource: AWS::Rbin::Rule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rbin import mixins as rbin_mixins
        
        cfn_rule_props_mixin = rbin_mixins.CfnRulePropsMixin(rbin_mixins.CfnRuleMixinProps(
            description="description",
            exclude_resource_tags=[rbin_mixins.CfnRulePropsMixin.ResourceTagProperty(
                resource_tag_key="resourceTagKey",
                resource_tag_value="resourceTagValue"
            )],
            lock_configuration=rbin_mixins.CfnRulePropsMixin.UnlockDelayProperty(
                unlock_delay_unit="unlockDelayUnit",
                unlock_delay_value=123
            ),
            resource_tags=[rbin_mixins.CfnRulePropsMixin.ResourceTagProperty(
                resource_tag_key="resourceTagKey",
                resource_tag_value="resourceTagValue"
            )],
            resource_type="resourceType",
            retention_period=rbin_mixins.CfnRulePropsMixin.RetentionPeriodProperty(
                retention_period_unit="retentionPeriodUnit",
                retention_period_value=123
            ),
            status="status",
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
        props: typing.Union[CfnRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Rbin::Rule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d391f2317ab2965262f6864a9f2108a4ea86197deec81e0373ae4cd0fcfd150)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff19ff46bb72a8ed4f5aedbda9128879d23756b079a821dd3f3a61f31d8f481f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__795151247890368b7151f840689f2f6e576cd4f73be73ac04adfe6744d637320)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRuleMixinProps:
        return typing.cast(CfnRuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rbin.mixins.CfnRulePropsMixin.ResourceTagProperty",
        jsii_struct_bases=[],
        name_mapping={
            "resource_tag_key": "resourceTagKey",
            "resource_tag_value": "resourceTagValue",
        },
    )
    class ResourceTagProperty:
        def __init__(
            self,
            *,
            resource_tag_key: typing.Optional[builtins.str] = None,
            resource_tag_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''[Tag-level retention rules only] Information about the resource tags used to identify resources that are retained by the retention rule.

            :param resource_tag_key: The tag key.
            :param resource_tag_value: The tag value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rbin-rule-resourcetag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rbin import mixins as rbin_mixins
                
                resource_tag_property = rbin_mixins.CfnRulePropsMixin.ResourceTagProperty(
                    resource_tag_key="resourceTagKey",
                    resource_tag_value="resourceTagValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8ff7f1ac87d7ede7c40a40c3000c252b1bbec616da530df300834cf8503cd249)
                check_type(argname="argument resource_tag_key", value=resource_tag_key, expected_type=type_hints["resource_tag_key"])
                check_type(argname="argument resource_tag_value", value=resource_tag_value, expected_type=type_hints["resource_tag_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_tag_key is not None:
                self._values["resource_tag_key"] = resource_tag_key
            if resource_tag_value is not None:
                self._values["resource_tag_value"] = resource_tag_value

        @builtins.property
        def resource_tag_key(self) -> typing.Optional[builtins.str]:
            '''The tag key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rbin-rule-resourcetag.html#cfn-rbin-rule-resourcetag-resourcetagkey
            '''
            result = self._values.get("resource_tag_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_tag_value(self) -> typing.Optional[builtins.str]:
            '''The tag value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rbin-rule-resourcetag.html#cfn-rbin-rule-resourcetag-resourcetagvalue
            '''
            result = self._values.get("resource_tag_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rbin.mixins.CfnRulePropsMixin.RetentionPeriodProperty",
        jsii_struct_bases=[],
        name_mapping={
            "retention_period_unit": "retentionPeriodUnit",
            "retention_period_value": "retentionPeriodValue",
        },
    )
    class RetentionPeriodProperty:
        def __init__(
            self,
            *,
            retention_period_unit: typing.Optional[builtins.str] = None,
            retention_period_value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about the retention period for which the retention rule is to retain resources.

            :param retention_period_unit: The unit of time in which the retention period is measured. Currently, only ``DAYS`` is supported.
            :param retention_period_value: The period value for which the retention rule is to retain resources, measured in days. The supported retention periods are: - EBS volumes: 1 - 7 days - EBS snapshots and EBS-backed AMIs: 1 - 365 days

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rbin-rule-retentionperiod.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rbin import mixins as rbin_mixins
                
                retention_period_property = rbin_mixins.CfnRulePropsMixin.RetentionPeriodProperty(
                    retention_period_unit="retentionPeriodUnit",
                    retention_period_value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__63c6a11243048331922d056da969dab10aad005a7f1a2a4425464bc99cbbe1ac)
                check_type(argname="argument retention_period_unit", value=retention_period_unit, expected_type=type_hints["retention_period_unit"])
                check_type(argname="argument retention_period_value", value=retention_period_value, expected_type=type_hints["retention_period_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if retention_period_unit is not None:
                self._values["retention_period_unit"] = retention_period_unit
            if retention_period_value is not None:
                self._values["retention_period_value"] = retention_period_value

        @builtins.property
        def retention_period_unit(self) -> typing.Optional[builtins.str]:
            '''The unit of time in which the retention period is measured.

            Currently, only ``DAYS`` is supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rbin-rule-retentionperiod.html#cfn-rbin-rule-retentionperiod-retentionperiodunit
            '''
            result = self._values.get("retention_period_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def retention_period_value(self) -> typing.Optional[jsii.Number]:
            '''The period value for which the retention rule is to retain resources, measured in days.

            The supported retention periods are:

            - EBS volumes: 1 - 7 days
            - EBS snapshots and EBS-backed AMIs: 1 - 365 days

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rbin-rule-retentionperiod.html#cfn-rbin-rule-retentionperiod-retentionperiodvalue
            '''
            result = self._values.get("retention_period_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetentionPeriodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rbin.mixins.CfnRulePropsMixin.UnlockDelayProperty",
        jsii_struct_bases=[],
        name_mapping={
            "unlock_delay_unit": "unlockDelayUnit",
            "unlock_delay_value": "unlockDelayValue",
        },
    )
    class UnlockDelayProperty:
        def __init__(
            self,
            *,
            unlock_delay_unit: typing.Optional[builtins.str] = None,
            unlock_delay_value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about the retention rule unlock delay.

            The unlock delay is the period after which a retention rule can be modified or edited after it has been unlocked by a user with the required permissions. The retention rule can't be modified or deleted during the unlock delay.

            :param unlock_delay_unit: The unit of time in which to measure the unlock delay. Currently, the unlock delay can be measured only in days.
            :param unlock_delay_value: The unlock delay period, measured in the unit specified for *UnlockDelayUnit* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rbin-rule-unlockdelay.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rbin import mixins as rbin_mixins
                
                unlock_delay_property = rbin_mixins.CfnRulePropsMixin.UnlockDelayProperty(
                    unlock_delay_unit="unlockDelayUnit",
                    unlock_delay_value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__de67a31a42a110d319ea9cca2b72799cf053c23a72862b6baf37001be85b7aad)
                check_type(argname="argument unlock_delay_unit", value=unlock_delay_unit, expected_type=type_hints["unlock_delay_unit"])
                check_type(argname="argument unlock_delay_value", value=unlock_delay_value, expected_type=type_hints["unlock_delay_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if unlock_delay_unit is not None:
                self._values["unlock_delay_unit"] = unlock_delay_unit
            if unlock_delay_value is not None:
                self._values["unlock_delay_value"] = unlock_delay_value

        @builtins.property
        def unlock_delay_unit(self) -> typing.Optional[builtins.str]:
            '''The unit of time in which to measure the unlock delay.

            Currently, the unlock delay can be measured only in days.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rbin-rule-unlockdelay.html#cfn-rbin-rule-unlockdelay-unlockdelayunit
            '''
            result = self._values.get("unlock_delay_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unlock_delay_value(self) -> typing.Optional[jsii.Number]:
            '''The unlock delay period, measured in the unit specified for *UnlockDelayUnit* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rbin-rule-unlockdelay.html#cfn-rbin-rule-unlockdelay-unlockdelayvalue
            '''
            result = self._values.get("unlock_delay_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UnlockDelayProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnRuleMixinProps",
    "CfnRulePropsMixin",
]

publication.publish()

def _typecheckingstub__66bc12f64f07b179bb04ccccb79c4dc2db5837ab5097cb37bda927c139ea2a07(
    *,
    description: typing.Optional[builtins.str] = None,
    exclude_resource_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.ResourceTagProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    lock_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.UnlockDelayProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.ResourceTagProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_type: typing.Optional[builtins.str] = None,
    retention_period: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.RetentionPeriodProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d391f2317ab2965262f6864a9f2108a4ea86197deec81e0373ae4cd0fcfd150(
    props: typing.Union[CfnRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff19ff46bb72a8ed4f5aedbda9128879d23756b079a821dd3f3a61f31d8f481f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795151247890368b7151f840689f2f6e576cd4f73be73ac04adfe6744d637320(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff7f1ac87d7ede7c40a40c3000c252b1bbec616da530df300834cf8503cd249(
    *,
    resource_tag_key: typing.Optional[builtins.str] = None,
    resource_tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c6a11243048331922d056da969dab10aad005a7f1a2a4425464bc99cbbe1ac(
    *,
    retention_period_unit: typing.Optional[builtins.str] = None,
    retention_period_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de67a31a42a110d319ea9cca2b72799cf053c23a72862b6baf37001be85b7aad(
    *,
    unlock_delay_unit: typing.Optional[builtins.str] = None,
    unlock_delay_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
