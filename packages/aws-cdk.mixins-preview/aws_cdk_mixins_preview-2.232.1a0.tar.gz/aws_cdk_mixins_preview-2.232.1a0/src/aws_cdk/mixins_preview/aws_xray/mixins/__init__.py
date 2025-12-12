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
    jsii_type="@aws-cdk/mixins-preview.aws_xray.mixins.CfnGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "filter_expression": "filterExpression",
        "group_name": "groupName",
        "insights_configuration": "insightsConfiguration",
        "tags": "tags",
    },
)
class CfnGroupMixinProps:
    def __init__(
        self,
        *,
        filter_expression: typing.Optional[builtins.str] = None,
        group_name: typing.Optional[builtins.str] = None,
        insights_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGroupPropsMixin.InsightsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnGroupPropsMixin.

        :param filter_expression: The filter expression defining the parameters to include traces.
        :param group_name: The unique case-sensitive name of the group.
        :param insights_configuration: The structure containing configurations related to insights. - The InsightsEnabled boolean can be set to true to enable insights for the group or false to disable insights for the group. - The NotificationsEnabled boolean can be set to true to enable insights notifications through Amazon EventBridge for the group.
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-group.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_xray import mixins as xray_mixins
            
            cfn_group_mixin_props = xray_mixins.CfnGroupMixinProps(
                filter_expression="filterExpression",
                group_name="groupName",
                insights_configuration=xray_mixins.CfnGroupPropsMixin.InsightsConfigurationProperty(
                    insights_enabled=False,
                    notifications_enabled=False
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbee3eff0fb839505c89ced72cac64848146fdf29d062a36afdd16effbb81b20)
            check_type(argname="argument filter_expression", value=filter_expression, expected_type=type_hints["filter_expression"])
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument insights_configuration", value=insights_configuration, expected_type=type_hints["insights_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter_expression is not None:
            self._values["filter_expression"] = filter_expression
        if group_name is not None:
            self._values["group_name"] = group_name
        if insights_configuration is not None:
            self._values["insights_configuration"] = insights_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def filter_expression(self) -> typing.Optional[builtins.str]:
        '''The filter expression defining the parameters to include traces.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-group.html#cfn-xray-group-filterexpression
        '''
        result = self._values.get("filter_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_name(self) -> typing.Optional[builtins.str]:
        '''The unique case-sensitive name of the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-group.html#cfn-xray-group-groupname
        '''
        result = self._values.get("group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insights_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGroupPropsMixin.InsightsConfigurationProperty"]]:
        '''The structure containing configurations related to insights.

        - The InsightsEnabled boolean can be set to true to enable insights for the group or false to disable insights for the group.
        - The NotificationsEnabled boolean can be set to true to enable insights notifications through Amazon EventBridge for the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-group.html#cfn-xray-group-insightsconfiguration
        '''
        result = self._values.get("insights_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGroupPropsMixin.InsightsConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-group.html#cfn-xray-group-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_xray.mixins.CfnGroupPropsMixin",
):
    '''Use the ``AWS::XRay::Group`` resource to specify a group with a name and a filter expression.

    Groups enable the collection of traces that match the filter expression, can be used to filter service graphs and traces, and to supply Amazon CloudWatch metrics.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-group.html
    :cloudformationResource: AWS::XRay::Group
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_xray import mixins as xray_mixins
        
        cfn_group_props_mixin = xray_mixins.CfnGroupPropsMixin(xray_mixins.CfnGroupMixinProps(
            filter_expression="filterExpression",
            group_name="groupName",
            insights_configuration=xray_mixins.CfnGroupPropsMixin.InsightsConfigurationProperty(
                insights_enabled=False,
                notifications_enabled=False
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
        props: typing.Union[CfnGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::XRay::Group``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cab8c2c4baa0175223756a5edf712d3bdf2bd4ae7960a6d7cdeb9894e8f8d70c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__306e289944022c576c47a60af5cd247f378fa386533dda3ced6d47d80ab256f3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a2577c673299a615e6902dc2214dcd0cdaa7b471321c5b356d92959f70e572c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGroupMixinProps:
        return typing.cast(CfnGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_xray.mixins.CfnGroupPropsMixin.InsightsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "insights_enabled": "insightsEnabled",
            "notifications_enabled": "notificationsEnabled",
        },
    )
    class InsightsConfigurationProperty:
        def __init__(
            self,
            *,
            insights_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            notifications_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The structure containing configurations related to insights.

            :param insights_enabled: Set the InsightsEnabled value to true to enable insights or false to disable insights.
            :param notifications_enabled: Set the NotificationsEnabled value to true to enable insights notifications. Notifications can only be enabled on a group with InsightsEnabled set to true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-group-insightsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_xray import mixins as xray_mixins
                
                insights_configuration_property = xray_mixins.CfnGroupPropsMixin.InsightsConfigurationProperty(
                    insights_enabled=False,
                    notifications_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8d85dc488e2ae9bb772bad22ddbd206549a3ac694021761bdb4d7025d9ca9351)
                check_type(argname="argument insights_enabled", value=insights_enabled, expected_type=type_hints["insights_enabled"])
                check_type(argname="argument notifications_enabled", value=notifications_enabled, expected_type=type_hints["notifications_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if insights_enabled is not None:
                self._values["insights_enabled"] = insights_enabled
            if notifications_enabled is not None:
                self._values["notifications_enabled"] = notifications_enabled

        @builtins.property
        def insights_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set the InsightsEnabled value to true to enable insights or false to disable insights.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-group-insightsconfiguration.html#cfn-xray-group-insightsconfiguration-insightsenabled
            '''
            result = self._values.get("insights_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def notifications_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set the NotificationsEnabled value to true to enable insights notifications.

            Notifications can only be enabled on a group with InsightsEnabled set to true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-group-insightsconfiguration.html#cfn-xray-group-insightsconfiguration-notificationsenabled
            '''
            result = self._values.get("notifications_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InsightsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_xray.mixins.CfnResourcePolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "bypass_policy_lockout_check": "bypassPolicyLockoutCheck",
        "policy_document": "policyDocument",
        "policy_name": "policyName",
    },
)
class CfnResourcePolicyMixinProps:
    def __init__(
        self,
        *,
        bypass_policy_lockout_check: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        policy_document: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResourcePolicyPropsMixin.

        :param bypass_policy_lockout_check: A flag to indicate whether to bypass the resource-based policy lockout safety check.
        :param policy_document: The resource-based policy document, which can be up to 5kb in size.
        :param policy_name: The name of the resource-based policy. Must be unique within a specific AWS account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-resourcepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_xray import mixins as xray_mixins
            
            cfn_resource_policy_mixin_props = xray_mixins.CfnResourcePolicyMixinProps(
                bypass_policy_lockout_check=False,
                policy_document="policyDocument",
                policy_name="policyName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca85f0de0f62761757324672de71cbf48bbc905008b4a184cf73ef615357a961)
            check_type(argname="argument bypass_policy_lockout_check", value=bypass_policy_lockout_check, expected_type=type_hints["bypass_policy_lockout_check"])
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bypass_policy_lockout_check is not None:
            self._values["bypass_policy_lockout_check"] = bypass_policy_lockout_check
        if policy_document is not None:
            self._values["policy_document"] = policy_document
        if policy_name is not None:
            self._values["policy_name"] = policy_name

    @builtins.property
    def bypass_policy_lockout_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A flag to indicate whether to bypass the resource-based policy lockout safety check.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-resourcepolicy.html#cfn-xray-resourcepolicy-bypasspolicylockoutcheck
        '''
        result = self._values.get("bypass_policy_lockout_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def policy_document(self) -> typing.Optional[builtins.str]:
        '''The resource-based policy document, which can be up to 5kb in size.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-resourcepolicy.html#cfn-xray-resourcepolicy-policydocument
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the resource-based policy.

        Must be unique within a specific AWS account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-resourcepolicy.html#cfn-xray-resourcepolicy-policyname
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourcePolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResourcePolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_xray.mixins.CfnResourcePolicyPropsMixin",
):
    '''Use ``AWS::XRay::ResourcePolicy`` to specify an X-Ray resource-based policy, which grants one or more AWS services and accounts permissions to access X-Ray .

    Each resource-based policy is associated with a specific AWS account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-resourcepolicy.html
    :cloudformationResource: AWS::XRay::ResourcePolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_xray import mixins as xray_mixins
        
        cfn_resource_policy_props_mixin = xray_mixins.CfnResourcePolicyPropsMixin(xray_mixins.CfnResourcePolicyMixinProps(
            bypass_policy_lockout_check=False,
            policy_document="policyDocument",
            policy_name="policyName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResourcePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::XRay::ResourcePolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ac1d012e233692ab858c70c73d53cb8771eea499e5cf0865aa0d0ce92c16d80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e30ee73b2d8685c98c78c9f85668150a25d7ec499d0e26be0af2c2493dfdf80b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__084d26fbec0de90606ef69bd4d2a86771472e76e3688d5a799dacb837fa55af5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResourcePolicyMixinProps:
        return typing.cast(CfnResourcePolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_xray.mixins.CfnSamplingRuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "rule_name": "ruleName",
        "sampling_rule": "samplingRule",
        "sampling_rule_record": "samplingRuleRecord",
        "sampling_rule_update": "samplingRuleUpdate",
        "tags": "tags",
    },
)
class CfnSamplingRuleMixinProps:
    def __init__(
        self,
        *,
        rule_name: typing.Optional[builtins.str] = None,
        sampling_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSamplingRulePropsMixin.SamplingRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sampling_rule_record: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSamplingRulePropsMixin.SamplingRuleRecordProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sampling_rule_update: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSamplingRulePropsMixin.SamplingRuleUpdateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSamplingRulePropsMixin.

        :param rule_name: (deprecated) The ARN of the sampling rule. Specify a rule by either name or ARN, but not both.
        :param sampling_rule: The sampling rule to be created or updated.
        :param sampling_rule_record: 
        :param sampling_rule_update: 
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-samplingrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_xray import mixins as xray_mixins
            
            cfn_sampling_rule_mixin_props = xray_mixins.CfnSamplingRuleMixinProps(
                rule_name="ruleName",
                sampling_rule=xray_mixins.CfnSamplingRulePropsMixin.SamplingRuleProperty(
                    attributes={
                        "attributes_key": "attributes"
                    },
                    fixed_rate=123,
                    host="host",
                    http_method="httpMethod",
                    priority=123,
                    reservoir_size=123,
                    resource_arn="resourceArn",
                    rule_arn="ruleArn",
                    rule_name="ruleName",
                    service_name="serviceName",
                    service_type="serviceType",
                    url_path="urlPath",
                    version=123
                ),
                sampling_rule_record=xray_mixins.CfnSamplingRulePropsMixin.SamplingRuleRecordProperty(
                    created_at="createdAt",
                    modified_at="modifiedAt",
                    sampling_rule=xray_mixins.CfnSamplingRulePropsMixin.SamplingRuleProperty(
                        attributes={
                            "attributes_key": "attributes"
                        },
                        fixed_rate=123,
                        host="host",
                        http_method="httpMethod",
                        priority=123,
                        reservoir_size=123,
                        resource_arn="resourceArn",
                        rule_arn="ruleArn",
                        rule_name="ruleName",
                        service_name="serviceName",
                        service_type="serviceType",
                        url_path="urlPath",
                        version=123
                    )
                ),
                sampling_rule_update=xray_mixins.CfnSamplingRulePropsMixin.SamplingRuleUpdateProperty(
                    attributes={
                        "attributes_key": "attributes"
                    },
                    fixed_rate=123,
                    host="host",
                    http_method="httpMethod",
                    priority=123,
                    reservoir_size=123,
                    resource_arn="resourceArn",
                    rule_arn="ruleArn",
                    rule_name="ruleName",
                    service_name="serviceName",
                    service_type="serviceType",
                    url_path="urlPath"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91b73304c68fdb060e66b97ad72f2127b163924ada5c42777d495810de163af1)
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument sampling_rule", value=sampling_rule, expected_type=type_hints["sampling_rule"])
            check_type(argname="argument sampling_rule_record", value=sampling_rule_record, expected_type=type_hints["sampling_rule_record"])
            check_type(argname="argument sampling_rule_update", value=sampling_rule_update, expected_type=type_hints["sampling_rule_update"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if sampling_rule is not None:
            self._values["sampling_rule"] = sampling_rule
        if sampling_rule_record is not None:
            self._values["sampling_rule_record"] = sampling_rule_record
        if sampling_rule_update is not None:
            self._values["sampling_rule_update"] = sampling_rule_update
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The ARN of the sampling rule.

        Specify a rule by either name or ARN, but not both.

        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-samplingrule.html#cfn-xray-samplingrule-rulename
        :stability: deprecated
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sampling_rule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSamplingRulePropsMixin.SamplingRuleProperty"]]:
        '''The sampling rule to be created or updated.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-samplingrule.html#cfn-xray-samplingrule-samplingrule
        '''
        result = self._values.get("sampling_rule")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSamplingRulePropsMixin.SamplingRuleProperty"]], result)

    @builtins.property
    def sampling_rule_record(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSamplingRulePropsMixin.SamplingRuleRecordProperty"]]:
        '''
        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-samplingrule.html#cfn-xray-samplingrule-samplingrulerecord
        :stability: deprecated
        '''
        result = self._values.get("sampling_rule_record")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSamplingRulePropsMixin.SamplingRuleRecordProperty"]], result)

    @builtins.property
    def sampling_rule_update(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSamplingRulePropsMixin.SamplingRuleUpdateProperty"]]:
        '''
        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-samplingrule.html#cfn-xray-samplingrule-samplingruleupdate
        :stability: deprecated
        '''
        result = self._values.get("sampling_rule_update")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSamplingRulePropsMixin.SamplingRuleUpdateProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-samplingrule.html#cfn-xray-samplingrule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSamplingRuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSamplingRulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_xray.mixins.CfnSamplingRulePropsMixin",
):
    '''Use the ``AWS::XRay::SamplingRule`` resource to specify a sampling rule, which controls sampling behavior for instrumented applications.

    Include a ``SamplingRule`` entity to create or update a sampling rule.
    .. epigraph::

       ``SamplingRule.Version`` can only be set when creating a sampling rule. Updating the version will cause the update to fail.

    Services retrieve rules with `GetSamplingRules <https://docs.aws.amazon.com//xray/latest/api/API_GetSamplingRules.html>`_ , and evaluate each rule in ascending order of *priority* for each request. If a rule matches, the service records a trace, borrowing it from the reservoir size. After 10 seconds, the service reports back to X-Ray with `GetSamplingTargets <https://docs.aws.amazon.com//xray/latest/api/API_GetSamplingTargets.html>`_ to get updated versions of each in-use rule. The updated rule contains a trace quota that the service can use instead of borrowing from the reservoir.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-samplingrule.html
    :cloudformationResource: AWS::XRay::SamplingRule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_xray import mixins as xray_mixins
        
        cfn_sampling_rule_props_mixin = xray_mixins.CfnSamplingRulePropsMixin(xray_mixins.CfnSamplingRuleMixinProps(
            rule_name="ruleName",
            sampling_rule=xray_mixins.CfnSamplingRulePropsMixin.SamplingRuleProperty(
                attributes={
                    "attributes_key": "attributes"
                },
                fixed_rate=123,
                host="host",
                http_method="httpMethod",
                priority=123,
                reservoir_size=123,
                resource_arn="resourceArn",
                rule_arn="ruleArn",
                rule_name="ruleName",
                service_name="serviceName",
                service_type="serviceType",
                url_path="urlPath",
                version=123
            ),
            sampling_rule_record=xray_mixins.CfnSamplingRulePropsMixin.SamplingRuleRecordProperty(
                created_at="createdAt",
                modified_at="modifiedAt",
                sampling_rule=xray_mixins.CfnSamplingRulePropsMixin.SamplingRuleProperty(
                    attributes={
                        "attributes_key": "attributes"
                    },
                    fixed_rate=123,
                    host="host",
                    http_method="httpMethod",
                    priority=123,
                    reservoir_size=123,
                    resource_arn="resourceArn",
                    rule_arn="ruleArn",
                    rule_name="ruleName",
                    service_name="serviceName",
                    service_type="serviceType",
                    url_path="urlPath",
                    version=123
                )
            ),
            sampling_rule_update=xray_mixins.CfnSamplingRulePropsMixin.SamplingRuleUpdateProperty(
                attributes={
                    "attributes_key": "attributes"
                },
                fixed_rate=123,
                host="host",
                http_method="httpMethod",
                priority=123,
                reservoir_size=123,
                resource_arn="resourceArn",
                rule_arn="ruleArn",
                rule_name="ruleName",
                service_name="serviceName",
                service_type="serviceType",
                url_path="urlPath"
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
        props: typing.Union[CfnSamplingRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::XRay::SamplingRule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed39549dd89a5981d7e83130b32c531b80e2ac1f986834eeb3ae30a8eeeb3c33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f30f3874acfef2e7efdd0ddf888ee71046b139d9dbeeb9a956abafbc44fe7c85)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc9340f21dda1b331f06c61d9fc62d36ebb5232363fddb1c8b0b31bc1689ca8f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSamplingRuleMixinProps:
        return typing.cast(CfnSamplingRuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_xray.mixins.CfnSamplingRulePropsMixin.SamplingRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attributes": "attributes",
            "fixed_rate": "fixedRate",
            "host": "host",
            "http_method": "httpMethod",
            "priority": "priority",
            "reservoir_size": "reservoirSize",
            "resource_arn": "resourceArn",
            "rule_arn": "ruleArn",
            "rule_name": "ruleName",
            "service_name": "serviceName",
            "service_type": "serviceType",
            "url_path": "urlPath",
            "version": "version",
        },
    )
    class SamplingRuleProperty:
        def __init__(
            self,
            *,
            attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            fixed_rate: typing.Optional[jsii.Number] = None,
            host: typing.Optional[builtins.str] = None,
            http_method: typing.Optional[builtins.str] = None,
            priority: typing.Optional[jsii.Number] = None,
            reservoir_size: typing.Optional[jsii.Number] = None,
            resource_arn: typing.Optional[builtins.str] = None,
            rule_arn: typing.Optional[builtins.str] = None,
            rule_name: typing.Optional[builtins.str] = None,
            service_name: typing.Optional[builtins.str] = None,
            service_type: typing.Optional[builtins.str] = None,
            url_path: typing.Optional[builtins.str] = None,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A sampling rule that services use to decide whether to instrument a request.

            Rule fields can match properties of the service, or properties of a request. The service can ignore rules that don't match its properties.

            :param attributes: Matches attributes derived from the request. *Map Entries:* Maximum number of 5 items. *Key Length Constraints:* Minimum length of 1. Maximum length of 32. *Value Length Constraints:* Minimum length of 1. Maximum length of 32.
            :param fixed_rate: The percentage of matching requests to instrument, after the reservoir is exhausted.
            :param host: Matches the hostname from a request URL.
            :param http_method: Matches the HTTP method of a request.
            :param priority: The priority of the sampling rule.
            :param reservoir_size: A fixed number of matching requests to instrument per second, prior to applying the fixed rate. The reservoir is not used directly by services, but applies to all services using the rule collectively.
            :param resource_arn: Matches the ARN of the AWS resource on which the service runs.
            :param rule_arn: The ARN of the sampling rule. Specify a rule by either name or ARN, but not both. .. epigraph:: Specifying a sampling rule by name is recommended, as specifying by ARN will be deprecated in future.
            :param rule_name: The name of the sampling rule. Specify a rule by either name or ARN, but not both.
            :param service_name: Matches the ``name`` that the service uses to identify itself in segments.
            :param service_type: Matches the ``origin`` that the service uses to identify its type in segments.
            :param url_path: Matches the path from a request URL.
            :param version: The version of the sampling rule. ``Version`` can only be set when creating a new sampling rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_xray import mixins as xray_mixins
                
                sampling_rule_property = xray_mixins.CfnSamplingRulePropsMixin.SamplingRuleProperty(
                    attributes={
                        "attributes_key": "attributes"
                    },
                    fixed_rate=123,
                    host="host",
                    http_method="httpMethod",
                    priority=123,
                    reservoir_size=123,
                    resource_arn="resourceArn",
                    rule_arn="ruleArn",
                    rule_name="ruleName",
                    service_name="serviceName",
                    service_type="serviceType",
                    url_path="urlPath",
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a36355ed040ff727a2916656cf6caa274477160fedb1d0235e57587345a4ce6)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument fixed_rate", value=fixed_rate, expected_type=type_hints["fixed_rate"])
                check_type(argname="argument host", value=host, expected_type=type_hints["host"])
                check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument reservoir_size", value=reservoir_size, expected_type=type_hints["reservoir_size"])
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
                check_type(argname="argument rule_arn", value=rule_arn, expected_type=type_hints["rule_arn"])
                check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
                check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
                check_type(argname="argument service_type", value=service_type, expected_type=type_hints["service_type"])
                check_type(argname="argument url_path", value=url_path, expected_type=type_hints["url_path"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if fixed_rate is not None:
                self._values["fixed_rate"] = fixed_rate
            if host is not None:
                self._values["host"] = host
            if http_method is not None:
                self._values["http_method"] = http_method
            if priority is not None:
                self._values["priority"] = priority
            if reservoir_size is not None:
                self._values["reservoir_size"] = reservoir_size
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn
            if rule_arn is not None:
                self._values["rule_arn"] = rule_arn
            if rule_name is not None:
                self._values["rule_name"] = rule_name
            if service_name is not None:
                self._values["service_name"] = service_name
            if service_type is not None:
                self._values["service_type"] = service_type
            if url_path is not None:
                self._values["url_path"] = url_path
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def attributes(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Matches attributes derived from the request.

            *Map Entries:* Maximum number of 5 items.

            *Key Length Constraints:* Minimum length of 1. Maximum length of 32.

            *Value Length Constraints:* Minimum length of 1. Maximum length of 32.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def fixed_rate(self) -> typing.Optional[jsii.Number]:
            '''The percentage of matching requests to instrument, after the reservoir is exhausted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-fixedrate
            '''
            result = self._values.get("fixed_rate")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def host(self) -> typing.Optional[builtins.str]:
            '''Matches the hostname from a request URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-host
            '''
            result = self._values.get("host")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def http_method(self) -> typing.Optional[builtins.str]:
            '''Matches the HTTP method of a request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-httpmethod
            '''
            result = self._values.get("http_method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            '''The priority of the sampling rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-priority
            '''
            result = self._values.get("priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def reservoir_size(self) -> typing.Optional[jsii.Number]:
            '''A fixed number of matching requests to instrument per second, prior to applying the fixed rate.

            The reservoir is not used directly by services, but applies to all services using the rule collectively.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-reservoirsize
            '''
            result = self._values.get("reservoir_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''Matches the ARN of the AWS resource on which the service runs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-resourcearn
            '''
            result = self._values.get("resource_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rule_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the sampling rule. Specify a rule by either name or ARN, but not both.

            .. epigraph::

               Specifying a sampling rule by name is recommended, as specifying by ARN will be deprecated in future.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-rulearn
            '''
            result = self._values.get("rule_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rule_name(self) -> typing.Optional[builtins.str]:
            '''The name of the sampling rule.

            Specify a rule by either name or ARN, but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-rulename
            '''
            result = self._values.get("rule_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_name(self) -> typing.Optional[builtins.str]:
            '''Matches the ``name`` that the service uses to identify itself in segments.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-servicename
            '''
            result = self._values.get("service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_type(self) -> typing.Optional[builtins.str]:
            '''Matches the ``origin`` that the service uses to identify its type in segments.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-servicetype
            '''
            result = self._values.get("service_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url_path(self) -> typing.Optional[builtins.str]:
            '''Matches the path from a request URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-urlpath
            '''
            result = self._values.get("url_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            '''The version of the sampling rule.

            ``Version`` can only be set when creating a new sampling rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SamplingRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_xray.mixins.CfnSamplingRulePropsMixin.SamplingRuleRecordProperty",
        jsii_struct_bases=[],
        name_mapping={
            "created_at": "createdAt",
            "modified_at": "modifiedAt",
            "sampling_rule": "samplingRule",
        },
    )
    class SamplingRuleRecordProperty:
        def __init__(
            self,
            *,
            created_at: typing.Optional[builtins.str] = None,
            modified_at: typing.Optional[builtins.str] = None,
            sampling_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSamplingRulePropsMixin.SamplingRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param created_at: When the rule was created, in Unix time seconds.
            :param modified_at: When the rule was modified, in Unix time seconds.
            :param sampling_rule: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrulerecord.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_xray import mixins as xray_mixins
                
                sampling_rule_record_property = xray_mixins.CfnSamplingRulePropsMixin.SamplingRuleRecordProperty(
                    created_at="createdAt",
                    modified_at="modifiedAt",
                    sampling_rule=xray_mixins.CfnSamplingRulePropsMixin.SamplingRuleProperty(
                        attributes={
                            "attributes_key": "attributes"
                        },
                        fixed_rate=123,
                        host="host",
                        http_method="httpMethod",
                        priority=123,
                        reservoir_size=123,
                        resource_arn="resourceArn",
                        rule_arn="ruleArn",
                        rule_name="ruleName",
                        service_name="serviceName",
                        service_type="serviceType",
                        url_path="urlPath",
                        version=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4d7f4a556ca9fae8ea69409936a3112a0bcb8f72c030ed8d8cd7fb877a348559)
                check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
                check_type(argname="argument modified_at", value=modified_at, expected_type=type_hints["modified_at"])
                check_type(argname="argument sampling_rule", value=sampling_rule, expected_type=type_hints["sampling_rule"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if created_at is not None:
                self._values["created_at"] = created_at
            if modified_at is not None:
                self._values["modified_at"] = modified_at
            if sampling_rule is not None:
                self._values["sampling_rule"] = sampling_rule

        @builtins.property
        def created_at(self) -> typing.Optional[builtins.str]:
            '''When the rule was created, in Unix time seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrulerecord.html#cfn-xray-samplingrule-samplingrulerecord-createdat
            '''
            result = self._values.get("created_at")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def modified_at(self) -> typing.Optional[builtins.str]:
            '''When the rule was modified, in Unix time seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrulerecord.html#cfn-xray-samplingrule-samplingrulerecord-modifiedat
            '''
            result = self._values.get("modified_at")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sampling_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSamplingRulePropsMixin.SamplingRuleProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrulerecord.html#cfn-xray-samplingrule-samplingrulerecord-samplingrule
            '''
            result = self._values.get("sampling_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSamplingRulePropsMixin.SamplingRuleProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SamplingRuleRecordProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_xray.mixins.CfnSamplingRulePropsMixin.SamplingRuleUpdateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attributes": "attributes",
            "fixed_rate": "fixedRate",
            "host": "host",
            "http_method": "httpMethod",
            "priority": "priority",
            "reservoir_size": "reservoirSize",
            "resource_arn": "resourceArn",
            "rule_arn": "ruleArn",
            "rule_name": "ruleName",
            "service_name": "serviceName",
            "service_type": "serviceType",
            "url_path": "urlPath",
        },
    )
    class SamplingRuleUpdateProperty:
        def __init__(
            self,
            *,
            attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            fixed_rate: typing.Optional[jsii.Number] = None,
            host: typing.Optional[builtins.str] = None,
            http_method: typing.Optional[builtins.str] = None,
            priority: typing.Optional[jsii.Number] = None,
            reservoir_size: typing.Optional[jsii.Number] = None,
            resource_arn: typing.Optional[builtins.str] = None,
            rule_arn: typing.Optional[builtins.str] = None,
            rule_name: typing.Optional[builtins.str] = None,
            service_name: typing.Optional[builtins.str] = None,
            service_type: typing.Optional[builtins.str] = None,
            url_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param attributes: Matches attributes derived from the request.
            :param fixed_rate: The percentage of matching requests to instrument, after the reservoir is exhausted.
            :param host: Matches the hostname from a request URL.
            :param http_method: Matches the HTTP method from a request URL.
            :param priority: The priority of the sampling rule.
            :param reservoir_size: A fixed number of matching requests to instrument per second, prior to applying the fixed rate. The reservoir is not used directly by services, but applies to all services using the rule collectively.
            :param resource_arn: Matches the ARN of the AWS resource on which the service runs.
            :param rule_arn: The ARN of the sampling rule. Specify a rule by either name or ARN, but not both.
            :param rule_name: The ARN of the sampling rule. Specify a rule by either name or ARN, but not both.
            :param service_name: Matches the name that the service uses to identify itself in segments.
            :param service_type: Matches the origin that the service uses to identify its type in segments.
            :param url_path: Matches the path from a request URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_xray import mixins as xray_mixins
                
                sampling_rule_update_property = xray_mixins.CfnSamplingRulePropsMixin.SamplingRuleUpdateProperty(
                    attributes={
                        "attributes_key": "attributes"
                    },
                    fixed_rate=123,
                    host="host",
                    http_method="httpMethod",
                    priority=123,
                    reservoir_size=123,
                    resource_arn="resourceArn",
                    rule_arn="ruleArn",
                    rule_name="ruleName",
                    service_name="serviceName",
                    service_type="serviceType",
                    url_path="urlPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d8b3cb244693bde425512c74c305a6ec7218bc4029a371e5185317e80757c321)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument fixed_rate", value=fixed_rate, expected_type=type_hints["fixed_rate"])
                check_type(argname="argument host", value=host, expected_type=type_hints["host"])
                check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument reservoir_size", value=reservoir_size, expected_type=type_hints["reservoir_size"])
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
                check_type(argname="argument rule_arn", value=rule_arn, expected_type=type_hints["rule_arn"])
                check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
                check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
                check_type(argname="argument service_type", value=service_type, expected_type=type_hints["service_type"])
                check_type(argname="argument url_path", value=url_path, expected_type=type_hints["url_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if fixed_rate is not None:
                self._values["fixed_rate"] = fixed_rate
            if host is not None:
                self._values["host"] = host
            if http_method is not None:
                self._values["http_method"] = http_method
            if priority is not None:
                self._values["priority"] = priority
            if reservoir_size is not None:
                self._values["reservoir_size"] = reservoir_size
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn
            if rule_arn is not None:
                self._values["rule_arn"] = rule_arn
            if rule_name is not None:
                self._values["rule_name"] = rule_name
            if service_name is not None:
                self._values["service_name"] = service_name
            if service_type is not None:
                self._values["service_type"] = service_type
            if url_path is not None:
                self._values["url_path"] = url_path

        @builtins.property
        def attributes(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Matches attributes derived from the request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def fixed_rate(self) -> typing.Optional[jsii.Number]:
            '''The percentage of matching requests to instrument, after the reservoir is exhausted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-fixedrate
            '''
            result = self._values.get("fixed_rate")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def host(self) -> typing.Optional[builtins.str]:
            '''Matches the hostname from a request URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-host
            '''
            result = self._values.get("host")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def http_method(self) -> typing.Optional[builtins.str]:
            '''Matches the HTTP method from a request URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-httpmethod
            '''
            result = self._values.get("http_method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            '''The priority of the sampling rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-priority
            '''
            result = self._values.get("priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def reservoir_size(self) -> typing.Optional[jsii.Number]:
            '''A fixed number of matching requests to instrument per second, prior to applying the fixed rate.

            The reservoir is not used directly by services, but applies to all services using the rule collectively.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-reservoirsize
            '''
            result = self._values.get("reservoir_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''Matches the ARN of the AWS resource on which the service runs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-resourcearn
            '''
            result = self._values.get("resource_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rule_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the sampling rule.

            Specify a rule by either name or ARN, but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-rulearn
            '''
            result = self._values.get("rule_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rule_name(self) -> typing.Optional[builtins.str]:
            '''The ARN of the sampling rule.

            Specify a rule by either name or ARN, but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-rulename
            '''
            result = self._values.get("rule_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_name(self) -> typing.Optional[builtins.str]:
            '''Matches the name that the service uses to identify itself in segments.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-servicename
            '''
            result = self._values.get("service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_type(self) -> typing.Optional[builtins.str]:
            '''Matches the origin that the service uses to identify its type in segments.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-servicetype
            '''
            result = self._values.get("service_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url_path(self) -> typing.Optional[builtins.str]:
            '''Matches the path from a request URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-urlpath
            '''
            result = self._values.get("url_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SamplingRuleUpdateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_xray.mixins.CfnTransactionSearchConfigMixinProps",
    jsii_struct_bases=[],
    name_mapping={"indexing_percentage": "indexingPercentage"},
)
class CfnTransactionSearchConfigMixinProps:
    def __init__(
        self,
        *,
        indexing_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnTransactionSearchConfigPropsMixin.

        :param indexing_percentage: Determines the percentage of traces indexed from CloudWatch Logs to X-Ray.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-transactionsearchconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_xray import mixins as xray_mixins
            
            cfn_transaction_search_config_mixin_props = xray_mixins.CfnTransactionSearchConfigMixinProps(
                indexing_percentage=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c52b3e2ca82f5e9920341900922063c3ab927303f7b804e5fb0b586e15ac9772)
            check_type(argname="argument indexing_percentage", value=indexing_percentage, expected_type=type_hints["indexing_percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if indexing_percentage is not None:
            self._values["indexing_percentage"] = indexing_percentage

    @builtins.property
    def indexing_percentage(self) -> typing.Optional[jsii.Number]:
        '''Determines the percentage of traces indexed from CloudWatch Logs to X-Ray.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-transactionsearchconfig.html#cfn-xray-transactionsearchconfig-indexingpercentage
        '''
        result = self._values.get("indexing_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTransactionSearchConfigMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTransactionSearchConfigPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_xray.mixins.CfnTransactionSearchConfigPropsMixin",
):
    '''This schema provides construct and validation rules for AWS-XRay TransactionSearchConfig resource parameters.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-transactionsearchconfig.html
    :cloudformationResource: AWS::XRay::TransactionSearchConfig
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_xray import mixins as xray_mixins
        
        cfn_transaction_search_config_props_mixin = xray_mixins.CfnTransactionSearchConfigPropsMixin(xray_mixins.CfnTransactionSearchConfigMixinProps(
            indexing_percentage=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTransactionSearchConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::XRay::TransactionSearchConfig``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e648e581c85effcc4443162cfdc4093a79cc13220748fd00ce47863193cbd8c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cf8e905f20105325732d9d67c9f6ba30d70fe52f7bf56d006a24136e3d55f01)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9707f6c3f882592501b32ffd325634afd94ad1fa6a33d104ef11749738da6a5a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTransactionSearchConfigMixinProps:
        return typing.cast(CfnTransactionSearchConfigMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnGroupMixinProps",
    "CfnGroupPropsMixin",
    "CfnResourcePolicyMixinProps",
    "CfnResourcePolicyPropsMixin",
    "CfnSamplingRuleMixinProps",
    "CfnSamplingRulePropsMixin",
    "CfnTransactionSearchConfigMixinProps",
    "CfnTransactionSearchConfigPropsMixin",
]

publication.publish()

def _typecheckingstub__dbee3eff0fb839505c89ced72cac64848146fdf29d062a36afdd16effbb81b20(
    *,
    filter_expression: typing.Optional[builtins.str] = None,
    group_name: typing.Optional[builtins.str] = None,
    insights_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGroupPropsMixin.InsightsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab8c2c4baa0175223756a5edf712d3bdf2bd4ae7960a6d7cdeb9894e8f8d70c(
    props: typing.Union[CfnGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306e289944022c576c47a60af5cd247f378fa386533dda3ced6d47d80ab256f3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2577c673299a615e6902dc2214dcd0cdaa7b471321c5b356d92959f70e572c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d85dc488e2ae9bb772bad22ddbd206549a3ac694021761bdb4d7025d9ca9351(
    *,
    insights_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    notifications_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca85f0de0f62761757324672de71cbf48bbc905008b4a184cf73ef615357a961(
    *,
    bypass_policy_lockout_check: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    policy_document: typing.Optional[builtins.str] = None,
    policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac1d012e233692ab858c70c73d53cb8771eea499e5cf0865aa0d0ce92c16d80(
    props: typing.Union[CfnResourcePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e30ee73b2d8685c98c78c9f85668150a25d7ec499d0e26be0af2c2493dfdf80b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__084d26fbec0de90606ef69bd4d2a86771472e76e3688d5a799dacb837fa55af5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91b73304c68fdb060e66b97ad72f2127b163924ada5c42777d495810de163af1(
    *,
    rule_name: typing.Optional[builtins.str] = None,
    sampling_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSamplingRulePropsMixin.SamplingRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sampling_rule_record: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSamplingRulePropsMixin.SamplingRuleRecordProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sampling_rule_update: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSamplingRulePropsMixin.SamplingRuleUpdateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed39549dd89a5981d7e83130b32c531b80e2ac1f986834eeb3ae30a8eeeb3c33(
    props: typing.Union[CfnSamplingRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f30f3874acfef2e7efdd0ddf888ee71046b139d9dbeeb9a956abafbc44fe7c85(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc9340f21dda1b331f06c61d9fc62d36ebb5232363fddb1c8b0b31bc1689ca8f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a36355ed040ff727a2916656cf6caa274477160fedb1d0235e57587345a4ce6(
    *,
    attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    fixed_rate: typing.Optional[jsii.Number] = None,
    host: typing.Optional[builtins.str] = None,
    http_method: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    reservoir_size: typing.Optional[jsii.Number] = None,
    resource_arn: typing.Optional[builtins.str] = None,
    rule_arn: typing.Optional[builtins.str] = None,
    rule_name: typing.Optional[builtins.str] = None,
    service_name: typing.Optional[builtins.str] = None,
    service_type: typing.Optional[builtins.str] = None,
    url_path: typing.Optional[builtins.str] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d7f4a556ca9fae8ea69409936a3112a0bcb8f72c030ed8d8cd7fb877a348559(
    *,
    created_at: typing.Optional[builtins.str] = None,
    modified_at: typing.Optional[builtins.str] = None,
    sampling_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSamplingRulePropsMixin.SamplingRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b3cb244693bde425512c74c305a6ec7218bc4029a371e5185317e80757c321(
    *,
    attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    fixed_rate: typing.Optional[jsii.Number] = None,
    host: typing.Optional[builtins.str] = None,
    http_method: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    reservoir_size: typing.Optional[jsii.Number] = None,
    resource_arn: typing.Optional[builtins.str] = None,
    rule_arn: typing.Optional[builtins.str] = None,
    rule_name: typing.Optional[builtins.str] = None,
    service_name: typing.Optional[builtins.str] = None,
    service_type: typing.Optional[builtins.str] = None,
    url_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52b3e2ca82f5e9920341900922063c3ab927303f7b804e5fb0b586e15ac9772(
    *,
    indexing_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e648e581c85effcc4443162cfdc4093a79cc13220748fd00ce47863193cbd8c9(
    props: typing.Union[CfnTransactionSearchConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cf8e905f20105325732d9d67c9f6ba30d70fe52f7bf56d006a24136e3d55f01(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9707f6c3f882592501b32ffd325634afd94ad1fa6a33d104ef11749738da6a5a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
