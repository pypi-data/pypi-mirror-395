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
    jsii_type="@aws-cdk/mixins-preview.aws_inspector.mixins.CfnAssessmentTargetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "assessment_target_name": "assessmentTargetName",
        "resource_group_arn": "resourceGroupArn",
    },
)
class CfnAssessmentTargetMixinProps:
    def __init__(
        self,
        *,
        assessment_target_name: typing.Optional[builtins.str] = None,
        resource_group_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAssessmentTargetPropsMixin.

        :param assessment_target_name: The name of the Amazon Inspector assessment target. The name must be unique within the AWS account .
        :param resource_group_arn: The ARN that specifies the resource group that is used to create the assessment target. If ``resourceGroupArn`` is not specified, all EC2 instances in the current AWS account and Region are included in the assessment target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttarget.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_inspector import mixins as inspector_mixins
            
            cfn_assessment_target_mixin_props = inspector_mixins.CfnAssessmentTargetMixinProps(
                assessment_target_name="assessmentTargetName",
                resource_group_arn="resourceGroupArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afef135de08d7a10a613109512d49f1cf427d44b02d134618ae8323339b2e892)
            check_type(argname="argument assessment_target_name", value=assessment_target_name, expected_type=type_hints["assessment_target_name"])
            check_type(argname="argument resource_group_arn", value=resource_group_arn, expected_type=type_hints["resource_group_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assessment_target_name is not None:
            self._values["assessment_target_name"] = assessment_target_name
        if resource_group_arn is not None:
            self._values["resource_group_arn"] = resource_group_arn

    @builtins.property
    def assessment_target_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Amazon Inspector assessment target.

        The name must be unique within the AWS account .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttarget.html#cfn-inspector-assessmenttarget-assessmenttargetname
        '''
        result = self._values.get("assessment_target_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_group_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN that specifies the resource group that is used to create the assessment target.

        If ``resourceGroupArn`` is not specified, all EC2 instances in the current AWS account and Region are included in the assessment target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttarget.html#cfn-inspector-assessmenttarget-resourcegrouparn
        '''
        result = self._values.get("resource_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssessmentTargetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAssessmentTargetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_inspector.mixins.CfnAssessmentTargetPropsMixin",
):
    '''The ``AWS::Inspector::AssessmentTarget`` resource is used to create Amazon Inspector assessment targets, which specify the Amazon EC2 instances that will be analyzed during an assessment run.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttarget.html
    :cloudformationResource: AWS::Inspector::AssessmentTarget
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_inspector import mixins as inspector_mixins
        
        cfn_assessment_target_props_mixin = inspector_mixins.CfnAssessmentTargetPropsMixin(inspector_mixins.CfnAssessmentTargetMixinProps(
            assessment_target_name="assessmentTargetName",
            resource_group_arn="resourceGroupArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAssessmentTargetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Inspector::AssessmentTarget``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63e225f6468a90910856a787c4d118838efad422902257a8e83b27fbf9bb41ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__160dd8c74db4bca1b44efc3eca9b38470936479382f4d11a7750b542c08f7bd1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86bf520217f9551521a9930fccccae1603ee81eb371788318d44dcc5c2497764)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAssessmentTargetMixinProps:
        return typing.cast(CfnAssessmentTargetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_inspector.mixins.CfnAssessmentTemplateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "assessment_target_arn": "assessmentTargetArn",
        "assessment_template_name": "assessmentTemplateName",
        "duration_in_seconds": "durationInSeconds",
        "rules_package_arns": "rulesPackageArns",
        "user_attributes_for_findings": "userAttributesForFindings",
    },
)
class CfnAssessmentTemplateMixinProps:
    def __init__(
        self,
        *,
        assessment_target_arn: typing.Optional[builtins.str] = None,
        assessment_template_name: typing.Optional[builtins.str] = None,
        duration_in_seconds: typing.Optional[jsii.Number] = None,
        rules_package_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_attributes_for_findings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnAssessmentTemplatePropsMixin.

        :param assessment_target_arn: The ARN of the assessment target to be included in the assessment template.
        :param assessment_template_name: The user-defined name that identifies the assessment template that you want to create. You can create several assessment templates for the same assessment target. The names of the assessment templates that correspond to a particular assessment target must be unique.
        :param duration_in_seconds: The duration of the assessment run in seconds.
        :param rules_package_arns: The ARNs of the rules packages that you want to use in the assessment template.
        :param user_attributes_for_findings: The user-defined attributes that are assigned to every finding that is generated by the assessment run that uses this assessment template. Within an assessment template, each key must be unique.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_inspector import mixins as inspector_mixins
            
            cfn_assessment_template_mixin_props = inspector_mixins.CfnAssessmentTemplateMixinProps(
                assessment_target_arn="assessmentTargetArn",
                assessment_template_name="assessmentTemplateName",
                duration_in_seconds=123,
                rules_package_arns=["rulesPackageArns"],
                user_attributes_for_findings=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc754a2e2736bee55fcc6dee172827ccf6421f6ec9d1d251713b39bf19616ea1)
            check_type(argname="argument assessment_target_arn", value=assessment_target_arn, expected_type=type_hints["assessment_target_arn"])
            check_type(argname="argument assessment_template_name", value=assessment_template_name, expected_type=type_hints["assessment_template_name"])
            check_type(argname="argument duration_in_seconds", value=duration_in_seconds, expected_type=type_hints["duration_in_seconds"])
            check_type(argname="argument rules_package_arns", value=rules_package_arns, expected_type=type_hints["rules_package_arns"])
            check_type(argname="argument user_attributes_for_findings", value=user_attributes_for_findings, expected_type=type_hints["user_attributes_for_findings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assessment_target_arn is not None:
            self._values["assessment_target_arn"] = assessment_target_arn
        if assessment_template_name is not None:
            self._values["assessment_template_name"] = assessment_template_name
        if duration_in_seconds is not None:
            self._values["duration_in_seconds"] = duration_in_seconds
        if rules_package_arns is not None:
            self._values["rules_package_arns"] = rules_package_arns
        if user_attributes_for_findings is not None:
            self._values["user_attributes_for_findings"] = user_attributes_for_findings

    @builtins.property
    def assessment_target_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the assessment target to be included in the assessment template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-assessmenttargetarn
        '''
        result = self._values.get("assessment_target_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assessment_template_name(self) -> typing.Optional[builtins.str]:
        '''The user-defined name that identifies the assessment template that you want to create.

        You can create several assessment templates for the same assessment target. The names of the assessment templates that correspond to a particular assessment target must be unique.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-assessmenttemplatename
        '''
        result = self._values.get("assessment_template_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def duration_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The duration of the assessment run in seconds.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-durationinseconds
        '''
        result = self._values.get("duration_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rules_package_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARNs of the rules packages that you want to use in the assessment template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-rulespackagearns
        '''
        result = self._values.get("rules_package_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_attributes_for_findings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]]:
        '''The user-defined attributes that are assigned to every finding that is generated by the assessment run that uses this assessment template.

        Within an assessment template, each key must be unique.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-userattributesforfindings
        '''
        result = self._values.get("user_attributes_for_findings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssessmentTemplateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAssessmentTemplatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_inspector.mixins.CfnAssessmentTemplatePropsMixin",
):
    '''The ``AWS::Inspector::AssessmentTemplate`` resource creates an Amazon Inspector assessment template, which specifies the Inspector assessment targets that will be evaluated by an assessment run and its related configurations.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html
    :cloudformationResource: AWS::Inspector::AssessmentTemplate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_inspector import mixins as inspector_mixins
        
        cfn_assessment_template_props_mixin = inspector_mixins.CfnAssessmentTemplatePropsMixin(inspector_mixins.CfnAssessmentTemplateMixinProps(
            assessment_target_arn="assessmentTargetArn",
            assessment_template_name="assessmentTemplateName",
            duration_in_seconds=123,
            rules_package_arns=["rulesPackageArns"],
            user_attributes_for_findings=[CfnTag(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAssessmentTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Inspector::AssessmentTemplate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7d6a4bc9f57a9266b2b3637d99101bbf7dddb8fdaafdbf4cfacd1aa25810d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d65b63bbadbab346f686ab282109f9bb6278efee4283512bf5b303068458742)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cca43e8006992ee8cc8ce6ec6c41466c814424a71b1983d5e672480e69b74642)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAssessmentTemplateMixinProps:
        return typing.cast(CfnAssessmentTemplateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_inspector.mixins.CfnResourceGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={"resource_group_tags": "resourceGroupTags"},
)
class CfnResourceGroupMixinProps:
    def __init__(
        self,
        *,
        resource_group_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnResourceGroupPropsMixin.

        :param resource_group_tags: The tags (key and value pairs) that will be associated with the resource group. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-resourcegroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_inspector import mixins as inspector_mixins
            
            cfn_resource_group_mixin_props = inspector_mixins.CfnResourceGroupMixinProps(
                resource_group_tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d460f81d8697cdd6a96d5310293faccb0d266943b2cc772321299ae4836b434d)
            check_type(argname="argument resource_group_tags", value=resource_group_tags, expected_type=type_hints["resource_group_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_group_tags is not None:
            self._values["resource_group_tags"] = resource_group_tags

    @builtins.property
    def resource_group_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]]:
        '''The tags (key and value pairs) that will be associated with the resource group.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-resourcegroup.html#cfn-inspector-resourcegroup-resourcegrouptags
        '''
        result = self._values.get("resource_group_tags")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResourceGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_inspector.mixins.CfnResourceGroupPropsMixin",
):
    '''The ``AWS::Inspector::ResourceGroup`` resource is used to create Amazon Inspector resource groups.

    A resource group defines a set of tags that, when queried, identify the AWS resources that make up the assessment target.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-resourcegroup.html
    :cloudformationResource: AWS::Inspector::ResourceGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_inspector import mixins as inspector_mixins
        
        cfn_resource_group_props_mixin = inspector_mixins.CfnResourceGroupPropsMixin(inspector_mixins.CfnResourceGroupMixinProps(
            resource_group_tags=[CfnTag(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResourceGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Inspector::ResourceGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa427c149a1336c38f4329cc928a5d85a1352f1fe9f0ea6f6603cd448a93218c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a73c59b0a992da532edea765b66b82f695f398e5cff71c7ced8ffd0d5d0338aa)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ad2bfc9175f4c35fc3f8a4e4a9cd30075b1bee5cf0603601bea7f90b39270d8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResourceGroupMixinProps:
        return typing.cast(CfnResourceGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnAssessmentTargetMixinProps",
    "CfnAssessmentTargetPropsMixin",
    "CfnAssessmentTemplateMixinProps",
    "CfnAssessmentTemplatePropsMixin",
    "CfnResourceGroupMixinProps",
    "CfnResourceGroupPropsMixin",
]

publication.publish()

def _typecheckingstub__afef135de08d7a10a613109512d49f1cf427d44b02d134618ae8323339b2e892(
    *,
    assessment_target_name: typing.Optional[builtins.str] = None,
    resource_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63e225f6468a90910856a787c4d118838efad422902257a8e83b27fbf9bb41ca(
    props: typing.Union[CfnAssessmentTargetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160dd8c74db4bca1b44efc3eca9b38470936479382f4d11a7750b542c08f7bd1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86bf520217f9551521a9930fccccae1603ee81eb371788318d44dcc5c2497764(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc754a2e2736bee55fcc6dee172827ccf6421f6ec9d1d251713b39bf19616ea1(
    *,
    assessment_target_arn: typing.Optional[builtins.str] = None,
    assessment_template_name: typing.Optional[builtins.str] = None,
    duration_in_seconds: typing.Optional[jsii.Number] = None,
    rules_package_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_attributes_for_findings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7d6a4bc9f57a9266b2b3637d99101bbf7dddb8fdaafdbf4cfacd1aa25810d1(
    props: typing.Union[CfnAssessmentTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d65b63bbadbab346f686ab282109f9bb6278efee4283512bf5b303068458742(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cca43e8006992ee8cc8ce6ec6c41466c814424a71b1983d5e672480e69b74642(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d460f81d8697cdd6a96d5310293faccb0d266943b2cc772321299ae4836b434d(
    *,
    resource_group_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa427c149a1336c38f4329cc928a5d85a1352f1fe9f0ea6f6603cd448a93218c(
    props: typing.Union[CfnResourceGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73c59b0a992da532edea765b66b82f695f398e5cff71c7ced8ffd0d5d0338aa(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad2bfc9175f4c35fc3f8a4e4a9cd30075b1bee5cf0603601bea7f90b39270d8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
