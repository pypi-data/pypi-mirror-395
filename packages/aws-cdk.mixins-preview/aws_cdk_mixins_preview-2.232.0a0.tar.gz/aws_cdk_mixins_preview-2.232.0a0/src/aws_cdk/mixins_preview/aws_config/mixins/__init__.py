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
    jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnAggregationAuthorizationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "authorized_account_id": "authorizedAccountId",
        "authorized_aws_region": "authorizedAwsRegion",
        "tags": "tags",
    },
)
class CfnAggregationAuthorizationMixinProps:
    def __init__(
        self,
        *,
        authorized_account_id: typing.Optional[builtins.str] = None,
        authorized_aws_region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAggregationAuthorizationPropsMixin.

        :param authorized_account_id: The 12-digit account ID of the account authorized to aggregate data.
        :param authorized_aws_region: The region authorized to collect aggregated data.
        :param tags: An array of tag object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-aggregationauthorization.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
            
            cfn_aggregation_authorization_mixin_props = config_mixins.CfnAggregationAuthorizationMixinProps(
                authorized_account_id="authorizedAccountId",
                authorized_aws_region="authorizedAwsRegion",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbf7de0329f059c0ee5e7430e91c5a8c69a393b9cfd1324d50aa3f1c97a244e4)
            check_type(argname="argument authorized_account_id", value=authorized_account_id, expected_type=type_hints["authorized_account_id"])
            check_type(argname="argument authorized_aws_region", value=authorized_aws_region, expected_type=type_hints["authorized_aws_region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authorized_account_id is not None:
            self._values["authorized_account_id"] = authorized_account_id
        if authorized_aws_region is not None:
            self._values["authorized_aws_region"] = authorized_aws_region
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def authorized_account_id(self) -> typing.Optional[builtins.str]:
        '''The 12-digit account ID of the account authorized to aggregate data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-aggregationauthorization.html#cfn-config-aggregationauthorization-authorizedaccountid
        '''
        result = self._values.get("authorized_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorized_aws_region(self) -> typing.Optional[builtins.str]:
        '''The region authorized to collect aggregated data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-aggregationauthorization.html#cfn-config-aggregationauthorization-authorizedawsregion
        '''
        result = self._values.get("authorized_aws_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of tag object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-aggregationauthorization.html#cfn-config-aggregationauthorization-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAggregationAuthorizationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAggregationAuthorizationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnAggregationAuthorizationPropsMixin",
):
    '''An object that represents the authorizations granted to aggregator accounts and regions.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-aggregationauthorization.html
    :cloudformationResource: AWS::Config::AggregationAuthorization
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
        
        cfn_aggregation_authorization_props_mixin = config_mixins.CfnAggregationAuthorizationPropsMixin(config_mixins.CfnAggregationAuthorizationMixinProps(
            authorized_account_id="authorizedAccountId",
            authorized_aws_region="authorizedAwsRegion",
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
        props: typing.Union[CfnAggregationAuthorizationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Config::AggregationAuthorization``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d10565420414adff209b91d0ec585b0bc7de0155bb61c877b6d698d6df44b706)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c69d51d1d3a2afbdc2af3c88ee522b16c864bdfef43fb9a216673ea6b0735c25)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__028dda4cabbc5f3ec993afd0d1af8eac8084e2d30489826950acb45847850cc2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAggregationAuthorizationMixinProps:
        return typing.cast(CfnAggregationAuthorizationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConfigRuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "compliance": "compliance",
        "config_rule_name": "configRuleName",
        "description": "description",
        "evaluation_modes": "evaluationModes",
        "input_parameters": "inputParameters",
        "maximum_execution_frequency": "maximumExecutionFrequency",
        "scope": "scope",
        "source": "source",
    },
)
class CfnConfigRuleMixinProps:
    def __init__(
        self,
        *,
        compliance: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigRulePropsMixin.ComplianceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        config_rule_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        evaluation_modes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigRulePropsMixin.EvaluationModeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        input_parameters: typing.Any = None,
        maximum_execution_frequency: typing.Optional[builtins.str] = None,
        scope: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigRulePropsMixin.ScopeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigRulePropsMixin.SourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnConfigRulePropsMixin.

        :param compliance: Indicates whether an AWS resource or AWS Config rule is compliant and provides the number of contributors that affect the compliance.
        :param config_rule_name: A name for the AWS Config rule. If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        :param description: The description that you provide for the AWS Config rule.
        :param evaluation_modes: The modes the AWS Config rule can be evaluated in. The valid values are distinct objects. By default, the value is Detective evaluation mode only.
        :param input_parameters: A string, in JSON format, that is passed to the AWS Config rule Lambda function.
        :param maximum_execution_frequency: The maximum frequency with which AWS Config runs evaluations for a rule. You can specify a value for ``MaximumExecutionFrequency`` when: - You are using an AWS managed rule that is triggered at a periodic frequency. - Your custom rule is triggered when AWS Config delivers the configuration snapshot. For more information, see `ConfigSnapshotDeliveryProperties <https://docs.aws.amazon.com/config/latest/APIReference/API_ConfigSnapshotDeliveryProperties.html>`_ . .. epigraph:: By default, rules with a periodic trigger are evaluated every 24 hours. To change the frequency, specify a valid value for the ``MaximumExecutionFrequency`` parameter.
        :param scope: Defines which resources can trigger an evaluation for the rule. The scope can include one or more resource types, a combination of one resource type and one resource ID, or a combination of a tag key and value. Specify a scope to constrain the resources that can trigger an evaluation for the rule. If you do not specify a scope, evaluations are triggered when any resource in the recording group changes.
        :param source: Provides the rule owner ( ``AWS`` for managed rules, ``CUSTOM_POLICY`` for Custom Policy rules, and ``CUSTOM_LAMBDA`` for Custom Lambda rules), the rule identifier, and the notifications that cause the function to evaluate your AWS resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
            
            # input_parameters: Any
            
            cfn_config_rule_mixin_props = config_mixins.CfnConfigRuleMixinProps(
                compliance=config_mixins.CfnConfigRulePropsMixin.ComplianceProperty(
                    type="type"
                ),
                config_rule_name="configRuleName",
                description="description",
                evaluation_modes=[config_mixins.CfnConfigRulePropsMixin.EvaluationModeConfigurationProperty(
                    mode="mode"
                )],
                input_parameters=input_parameters,
                maximum_execution_frequency="maximumExecutionFrequency",
                scope=config_mixins.CfnConfigRulePropsMixin.ScopeProperty(
                    compliance_resource_id="complianceResourceId",
                    compliance_resource_types=["complianceResourceTypes"],
                    tag_key="tagKey",
                    tag_value="tagValue"
                ),
                source=config_mixins.CfnConfigRulePropsMixin.SourceProperty(
                    custom_policy_details=config_mixins.CfnConfigRulePropsMixin.CustomPolicyDetailsProperty(
                        enable_debug_log_delivery=False,
                        policy_runtime="policyRuntime",
                        policy_text="policyText"
                    ),
                    owner="owner",
                    source_details=[config_mixins.CfnConfigRulePropsMixin.SourceDetailProperty(
                        event_source="eventSource",
                        maximum_execution_frequency="maximumExecutionFrequency",
                        message_type="messageType"
                    )],
                    source_identifier="sourceIdentifier"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96254716dfc4c7c2ffdf382a40ede98329eee4dd28b72533de300fe1b9debd09)
            check_type(argname="argument compliance", value=compliance, expected_type=type_hints["compliance"])
            check_type(argname="argument config_rule_name", value=config_rule_name, expected_type=type_hints["config_rule_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument evaluation_modes", value=evaluation_modes, expected_type=type_hints["evaluation_modes"])
            check_type(argname="argument input_parameters", value=input_parameters, expected_type=type_hints["input_parameters"])
            check_type(argname="argument maximum_execution_frequency", value=maximum_execution_frequency, expected_type=type_hints["maximum_execution_frequency"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compliance is not None:
            self._values["compliance"] = compliance
        if config_rule_name is not None:
            self._values["config_rule_name"] = config_rule_name
        if description is not None:
            self._values["description"] = description
        if evaluation_modes is not None:
            self._values["evaluation_modes"] = evaluation_modes
        if input_parameters is not None:
            self._values["input_parameters"] = input_parameters
        if maximum_execution_frequency is not None:
            self._values["maximum_execution_frequency"] = maximum_execution_frequency
        if scope is not None:
            self._values["scope"] = scope
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def compliance(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigRulePropsMixin.ComplianceProperty"]]:
        '''Indicates whether an AWS resource or AWS Config rule is compliant and provides the number of contributors that affect the compliance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-compliance
        '''
        result = self._values.get("compliance")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigRulePropsMixin.ComplianceProperty"]], result)

    @builtins.property
    def config_rule_name(self) -> typing.Optional[builtins.str]:
        '''A name for the AWS Config rule.

        If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-configrulename
        '''
        result = self._values.get("config_rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description that you provide for the AWS Config rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def evaluation_modes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigRulePropsMixin.EvaluationModeConfigurationProperty"]]]]:
        '''The modes the AWS Config rule can be evaluated in.

        The valid values are distinct objects. By default, the value is Detective evaluation mode only.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-evaluationmodes
        '''
        result = self._values.get("evaluation_modes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigRulePropsMixin.EvaluationModeConfigurationProperty"]]]], result)

    @builtins.property
    def input_parameters(self) -> typing.Any:
        '''A string, in JSON format, that is passed to the AWS Config rule Lambda function.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-inputparameters
        '''
        result = self._values.get("input_parameters")
        return typing.cast(typing.Any, result)

    @builtins.property
    def maximum_execution_frequency(self) -> typing.Optional[builtins.str]:
        '''The maximum frequency with which AWS Config runs evaluations for a rule.

        You can specify a value for ``MaximumExecutionFrequency`` when:

        - You are using an AWS managed rule that is triggered at a periodic frequency.
        - Your custom rule is triggered when AWS Config delivers the configuration snapshot. For more information, see `ConfigSnapshotDeliveryProperties <https://docs.aws.amazon.com/config/latest/APIReference/API_ConfigSnapshotDeliveryProperties.html>`_ .

        .. epigraph::

           By default, rules with a periodic trigger are evaluated every 24 hours. To change the frequency, specify a valid value for the ``MaximumExecutionFrequency`` parameter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-maximumexecutionfrequency
        '''
        result = self._values.get("maximum_execution_frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigRulePropsMixin.ScopeProperty"]]:
        '''Defines which resources can trigger an evaluation for the rule.

        The scope can include one or more resource types, a combination of one resource type and one resource ID, or a combination of a tag key and value. Specify a scope to constrain the resources that can trigger an evaluation for the rule. If you do not specify a scope, evaluations are triggered when any resource in the recording group changes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-scope
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigRulePropsMixin.ScopeProperty"]], result)

    @builtins.property
    def source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigRulePropsMixin.SourceProperty"]]:
        '''Provides the rule owner ( ``AWS`` for managed rules, ``CUSTOM_POLICY`` for Custom Policy rules, and ``CUSTOM_LAMBDA`` for Custom Lambda rules), the rule identifier, and the notifications that cause the function to evaluate your AWS resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-source
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigRulePropsMixin.SourceProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigRuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConfigRulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConfigRulePropsMixin",
):
    '''.. epigraph::

   You must first create and start the AWS Config configuration recorder in order to create AWS Config managed rules with AWS CloudFormation .

    For more information, see `Managing the Configuration Recorder <https://docs.aws.amazon.com/config/latest/developerguide/stop-start-recorder.html>`_ .

    Adds or updates an AWS Config rule to evaluate if your AWS resources comply with your desired configurations. For information on how many AWS Config rules you can have per account, see `*Service Limits* <https://docs.aws.amazon.com/config/latest/developerguide/configlimits.html>`_ in the *AWS Config Developer Guide* .

    There are two types of rules: *AWS Config Managed Rules* and *AWS Config Custom Rules* . You can use the ``ConfigRule`` resource to create both AWS Config Managed Rules and AWS Config Custom Rules.

    AWS Config Managed Rules are predefined, customizable rules created by AWS Config . For a list of managed rules, see `List of AWS Config Managed Rules <https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html>`_ . If you are adding an AWS Config managed rule, you must specify the rule's identifier for the ``SourceIdentifier`` key.

    AWS Config Custom Rules are rules that you create from scratch. There are two ways to create AWS Config custom rules: with Lambda functions ( `AWS Lambda Developer Guide <https://docs.aws.amazon.com/config/latest/developerguide/gettingstarted-concepts.html#gettingstarted-concepts-function>`_ ) and with Guard ( `Guard GitHub Repository <https://docs.aws.amazon.com/https://github.com/aws-cloudformation/cloudformation-guard>`_ ), a policy-as-code language. AWS Config custom rules created with AWS Lambda are called *AWS Config Custom Lambda Rules* and AWS Config custom rules created with Guard are called *AWS Config Custom Policy Rules* .

    If you are adding a new AWS Config Custom Lambda rule, you first need to create an AWS Lambda function that the rule invokes to evaluate your resources. When you use the ``ConfigRule`` resource to add a Custom Lambda rule to AWS Config , you must specify the Amazon Resource Name (ARN) that AWS Lambda assigns to the function. You specify the ARN in the ``SourceIdentifier`` key. This key is part of the ``Source`` object, which is part of the ``ConfigRule`` object.

    For any new AWS Config rule that you add, specify the ``ConfigRuleName`` in the ``ConfigRule`` object. Do not specify the ``ConfigRuleArn`` or the ``ConfigRuleId`` . These values are generated by AWS Config for new rules.

    If you are updating a rule that you added previously, you can specify the rule by ``ConfigRuleName`` , ``ConfigRuleId`` , or ``ConfigRuleArn`` in the ``ConfigRule`` data type that you use in this request.

    For more information about developing and using AWS Config rules, see `Evaluating Resources with AWS Config Rules <https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config.html>`_ in the *AWS Config Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html
    :cloudformationResource: AWS::Config::ConfigRule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
        
        # input_parameters: Any
        
        cfn_config_rule_props_mixin = config_mixins.CfnConfigRulePropsMixin(config_mixins.CfnConfigRuleMixinProps(
            compliance=config_mixins.CfnConfigRulePropsMixin.ComplianceProperty(
                type="type"
            ),
            config_rule_name="configRuleName",
            description="description",
            evaluation_modes=[config_mixins.CfnConfigRulePropsMixin.EvaluationModeConfigurationProperty(
                mode="mode"
            )],
            input_parameters=input_parameters,
            maximum_execution_frequency="maximumExecutionFrequency",
            scope=config_mixins.CfnConfigRulePropsMixin.ScopeProperty(
                compliance_resource_id="complianceResourceId",
                compliance_resource_types=["complianceResourceTypes"],
                tag_key="tagKey",
                tag_value="tagValue"
            ),
            source=config_mixins.CfnConfigRulePropsMixin.SourceProperty(
                custom_policy_details=config_mixins.CfnConfigRulePropsMixin.CustomPolicyDetailsProperty(
                    enable_debug_log_delivery=False,
                    policy_runtime="policyRuntime",
                    policy_text="policyText"
                ),
                owner="owner",
                source_details=[config_mixins.CfnConfigRulePropsMixin.SourceDetailProperty(
                    event_source="eventSource",
                    maximum_execution_frequency="maximumExecutionFrequency",
                    message_type="messageType"
                )],
                source_identifier="sourceIdentifier"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnConfigRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Config::ConfigRule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c04eb612ba7243700149422e94a28626e30f0324b4dd33a04ee70977eefda1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ad0cdbc649ee2d926cddaf66b61c0297162ed760abdf934a2b4922a80f1e723)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20a08cda2de5407d414779e81ec194f6567c4867a090a8952ca6c633de999319)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConfigRuleMixinProps:
        return typing.cast(CfnConfigRuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConfigRulePropsMixin.ComplianceProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type"},
    )
    class ComplianceProperty:
        def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
            '''Indicates whether an AWS resource or AWS Config rule is compliant and provides the number of contributors that affect the compliance.

            :param type: Indicates whether an AWS resource or AWS Config rule is compliant. A resource is compliant if it complies with all of the AWS Config rules that evaluate it. A resource is noncompliant if it does not comply with one or more of these rules. A rule is compliant if all of the resources that the rule evaluates comply with it. A rule is noncompliant if any of these resources do not comply. AWS Config returns the ``INSUFFICIENT_DATA`` value when no evaluation results are available for the AWS resource or AWS Config rule. For the ``Compliance`` data type, AWS Config supports only ``COMPLIANT`` , ``NON_COMPLIANT`` , and ``INSUFFICIENT_DATA`` values. AWS Config does not support the ``NOT_APPLICABLE`` value for the ``Compliance`` data type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-compliance.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                compliance_property = config_mixins.CfnConfigRulePropsMixin.ComplianceProperty(
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__942655d2e7090afa7864f1ce7b83a290185487d6e4f4e2891680c6c4cb10d3f6)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Indicates whether an AWS resource or AWS Config rule is compliant.

            A resource is compliant if it complies with all of the AWS Config rules that evaluate it. A resource is noncompliant if it does not comply with one or more of these rules.

            A rule is compliant if all of the resources that the rule evaluates comply with it. A rule is noncompliant if any of these resources do not comply.

            AWS Config returns the ``INSUFFICIENT_DATA`` value when no evaluation results are available for the AWS resource or AWS Config rule.

            For the ``Compliance`` data type, AWS Config supports only ``COMPLIANT`` , ``NON_COMPLIANT`` , and ``INSUFFICIENT_DATA`` values. AWS Config does not support the ``NOT_APPLICABLE`` value for the ``Compliance`` data type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-compliance.html#cfn-config-configrule-compliance-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComplianceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConfigRulePropsMixin.CustomPolicyDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enable_debug_log_delivery": "enableDebugLogDelivery",
            "policy_runtime": "policyRuntime",
            "policy_text": "policyText",
        },
    )
    class CustomPolicyDetailsProperty:
        def __init__(
            self,
            *,
            enable_debug_log_delivery: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            policy_runtime: typing.Optional[builtins.str] = None,
            policy_text: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the CustomPolicyDetails, the rule owner ( ``AWS`` for managed rules, ``CUSTOM_POLICY`` for Custom Policy rules, and ``CUSTOM_LAMBDA`` for Custom Lambda rules), the rule identifier, and the events that cause the evaluation of your AWS resources.

            :param enable_debug_log_delivery: The boolean expression for enabling debug logging for your AWS Config Custom Policy rule. The default value is ``false`` .
            :param policy_runtime: The runtime system for your AWS Config Custom Policy rule. Guard is a policy-as-code language that allows you to write policies that are enforced by AWS Config Custom Policy rules. For more information about Guard, see the `Guard GitHub Repository <https://docs.aws.amazon.com/https://github.com/aws-cloudformation/cloudformation-guard>`_ .
            :param policy_text: The policy definition containing the logic for your AWS Config Custom Policy rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-custompolicydetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                custom_policy_details_property = config_mixins.CfnConfigRulePropsMixin.CustomPolicyDetailsProperty(
                    enable_debug_log_delivery=False,
                    policy_runtime="policyRuntime",
                    policy_text="policyText"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6985fc4a6494e2bf5d1d159054d9898c47008aeeeca538e2ef4d4eb19359f0ad)
                check_type(argname="argument enable_debug_log_delivery", value=enable_debug_log_delivery, expected_type=type_hints["enable_debug_log_delivery"])
                check_type(argname="argument policy_runtime", value=policy_runtime, expected_type=type_hints["policy_runtime"])
                check_type(argname="argument policy_text", value=policy_text, expected_type=type_hints["policy_text"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_debug_log_delivery is not None:
                self._values["enable_debug_log_delivery"] = enable_debug_log_delivery
            if policy_runtime is not None:
                self._values["policy_runtime"] = policy_runtime
            if policy_text is not None:
                self._values["policy_text"] = policy_text

        @builtins.property
        def enable_debug_log_delivery(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The boolean expression for enabling debug logging for your AWS Config Custom Policy rule.

            The default value is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-custompolicydetails.html#cfn-config-configrule-custompolicydetails-enabledebuglogdelivery
            '''
            result = self._values.get("enable_debug_log_delivery")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def policy_runtime(self) -> typing.Optional[builtins.str]:
            '''The runtime system for your AWS Config Custom Policy rule.

            Guard is a policy-as-code language that allows you to write policies that are enforced by AWS Config Custom Policy rules. For more information about Guard, see the `Guard GitHub Repository <https://docs.aws.amazon.com/https://github.com/aws-cloudformation/cloudformation-guard>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-custompolicydetails.html#cfn-config-configrule-custompolicydetails-policyruntime
            '''
            result = self._values.get("policy_runtime")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def policy_text(self) -> typing.Optional[builtins.str]:
            '''The policy definition containing the logic for your AWS Config Custom Policy rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-custompolicydetails.html#cfn-config-configrule-custompolicydetails-policytext
            '''
            result = self._values.get("policy_text")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomPolicyDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConfigRulePropsMixin.EvaluationModeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"mode": "mode"},
    )
    class EvaluationModeConfigurationProperty:
        def __init__(self, *, mode: typing.Optional[builtins.str] = None) -> None:
            '''The configuration object for AWS Config rule evaluation mode.

            The supported valid values are Detective or Proactive.

            :param mode: The mode of an evaluation. The valid values are Detective or Proactive.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-evaluationmodeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                evaluation_mode_configuration_property = config_mixins.CfnConfigRulePropsMixin.EvaluationModeConfigurationProperty(
                    mode="mode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__171dd3b9d615a78cadfa9495d42b1f66498acbccf027cddbf1af32ee7f63d04e)
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mode is not None:
                self._values["mode"] = mode

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''The mode of an evaluation.

            The valid values are Detective or Proactive.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-evaluationmodeconfiguration.html#cfn-config-configrule-evaluationmodeconfiguration-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationModeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConfigRulePropsMixin.ScopeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "compliance_resource_id": "complianceResourceId",
            "compliance_resource_types": "complianceResourceTypes",
            "tag_key": "tagKey",
            "tag_value": "tagValue",
        },
    )
    class ScopeProperty:
        def __init__(
            self,
            *,
            compliance_resource_id: typing.Optional[builtins.str] = None,
            compliance_resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            tag_key: typing.Optional[builtins.str] = None,
            tag_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines which resources trigger an evaluation for an AWS Config rule.

            The scope can include one or more resource types, a combination of a tag key and value, or a combination of one resource type and one resource ID. Specify a scope to constrain which resources trigger an evaluation for a rule. Otherwise, evaluations for the rule are triggered when any resource in your recording group changes in configuration.

            :param compliance_resource_id: The ID of the only AWS resource that you want to trigger an evaluation for the rule. If you specify a resource ID, you must specify one resource type for ``ComplianceResourceTypes`` .
            :param compliance_resource_types: The resource types of only those AWS resources that you want to trigger an evaluation for the rule. You can only specify one type if you also specify a resource ID for ``ComplianceResourceId`` .
            :param tag_key: The tag key that is applied to only those AWS resources that you want to trigger an evaluation for the rule.
            :param tag_value: The tag value applied to only those AWS resources that you want to trigger an evaluation for the rule. If you specify a value for ``TagValue`` , you must also specify a value for ``TagKey`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-scope.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                scope_property = config_mixins.CfnConfigRulePropsMixin.ScopeProperty(
                    compliance_resource_id="complianceResourceId",
                    compliance_resource_types=["complianceResourceTypes"],
                    tag_key="tagKey",
                    tag_value="tagValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__31e1fa2712a72994ace57e3a583076c58fcfefd0b1a19722987ab4f137065828)
                check_type(argname="argument compliance_resource_id", value=compliance_resource_id, expected_type=type_hints["compliance_resource_id"])
                check_type(argname="argument compliance_resource_types", value=compliance_resource_types, expected_type=type_hints["compliance_resource_types"])
                check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
                check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if compliance_resource_id is not None:
                self._values["compliance_resource_id"] = compliance_resource_id
            if compliance_resource_types is not None:
                self._values["compliance_resource_types"] = compliance_resource_types
            if tag_key is not None:
                self._values["tag_key"] = tag_key
            if tag_value is not None:
                self._values["tag_value"] = tag_value

        @builtins.property
        def compliance_resource_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the only AWS resource that you want to trigger an evaluation for the rule.

            If you specify a resource ID, you must specify one resource type for ``ComplianceResourceTypes`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-scope.html#cfn-config-configrule-scope-complianceresourceid
            '''
            result = self._values.get("compliance_resource_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def compliance_resource_types(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The resource types of only those AWS resources that you want to trigger an evaluation for the rule.

            You can only specify one type if you also specify a resource ID for ``ComplianceResourceId`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-scope.html#cfn-config-configrule-scope-complianceresourcetypes
            '''
            result = self._values.get("compliance_resource_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def tag_key(self) -> typing.Optional[builtins.str]:
            '''The tag key that is applied to only those AWS resources that you want to trigger an evaluation for the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-scope.html#cfn-config-configrule-scope-tagkey
            '''
            result = self._values.get("tag_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_value(self) -> typing.Optional[builtins.str]:
            '''The tag value applied to only those AWS resources that you want to trigger an evaluation for the rule.

            If you specify a value for ``TagValue`` , you must also specify a value for ``TagKey`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-scope.html#cfn-config-configrule-scope-tagvalue
            '''
            result = self._values.get("tag_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScopeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConfigRulePropsMixin.SourceDetailProperty",
        jsii_struct_bases=[],
        name_mapping={
            "event_source": "eventSource",
            "maximum_execution_frequency": "maximumExecutionFrequency",
            "message_type": "messageType",
        },
    )
    class SourceDetailProperty:
        def __init__(
            self,
            *,
            event_source: typing.Optional[builtins.str] = None,
            maximum_execution_frequency: typing.Optional[builtins.str] = None,
            message_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the source and the message types that trigger AWS Config to evaluate your AWS resources against a rule.

            It also provides the frequency with which you want AWS Config to run evaluations for the rule if the trigger type is periodic. You can specify the parameter values for ``SourceDetail`` only for custom rules.

            :param event_source: The source of the event, such as an AWS service, that triggers AWS Config to evaluate your AWS resources.
            :param maximum_execution_frequency: The frequency at which you want AWS Config to run evaluations for a custom rule with a periodic trigger. If you specify a value for ``MaximumExecutionFrequency`` , then ``MessageType`` must use the ``ScheduledNotification`` value. .. epigraph:: By default, rules with a periodic trigger are evaluated every 24 hours. To change the frequency, specify a valid value for the ``MaximumExecutionFrequency`` parameter. Based on the valid value you choose, AWS Config runs evaluations once for each valid value. For example, if you choose ``Three_Hours`` , AWS Config runs evaluations once every three hours. In this case, ``Three_Hours`` is the frequency of this rule.
            :param message_type: The type of notification that triggers AWS Config to run an evaluation for a rule. You can specify the following notification types: - ``ConfigurationItemChangeNotification`` - Triggers an evaluation when AWS Config delivers a configuration item as a result of a resource change. - ``OversizedConfigurationItemChangeNotification`` - Triggers an evaluation when AWS Config delivers an oversized configuration item. AWS Config may generate this notification type when a resource changes and the notification exceeds the maximum size allowed by Amazon SNS. - ``ScheduledNotification`` - Triggers a periodic evaluation at the frequency specified for ``MaximumExecutionFrequency`` . - ``ConfigurationSnapshotDeliveryCompleted`` - Triggers a periodic evaluation when AWS Config delivers a configuration snapshot. If you want your custom rule to be triggered by configuration changes, specify two SourceDetail objects, one for ``ConfigurationItemChangeNotification`` and one for ``OversizedConfigurationItemChangeNotification`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-sourcedetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                source_detail_property = config_mixins.CfnConfigRulePropsMixin.SourceDetailProperty(
                    event_source="eventSource",
                    maximum_execution_frequency="maximumExecutionFrequency",
                    message_type="messageType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a25ab91915725cee35e3082b4bfba298141a156b3199408b7315f77d7ba3e87f)
                check_type(argname="argument event_source", value=event_source, expected_type=type_hints["event_source"])
                check_type(argname="argument maximum_execution_frequency", value=maximum_execution_frequency, expected_type=type_hints["maximum_execution_frequency"])
                check_type(argname="argument message_type", value=message_type, expected_type=type_hints["message_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event_source is not None:
                self._values["event_source"] = event_source
            if maximum_execution_frequency is not None:
                self._values["maximum_execution_frequency"] = maximum_execution_frequency
            if message_type is not None:
                self._values["message_type"] = message_type

        @builtins.property
        def event_source(self) -> typing.Optional[builtins.str]:
            '''The source of the event, such as an AWS service, that triggers AWS Config to evaluate your AWS resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-sourcedetail.html#cfn-config-configrule-sourcedetail-eventsource
            '''
            result = self._values.get("event_source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def maximum_execution_frequency(self) -> typing.Optional[builtins.str]:
            '''The frequency at which you want AWS Config to run evaluations for a custom rule with a periodic trigger.

            If you specify a value for ``MaximumExecutionFrequency`` , then ``MessageType`` must use the ``ScheduledNotification`` value.
            .. epigraph::

               By default, rules with a periodic trigger are evaluated every 24 hours. To change the frequency, specify a valid value for the ``MaximumExecutionFrequency`` parameter.

               Based on the valid value you choose, AWS Config runs evaluations once for each valid value. For example, if you choose ``Three_Hours`` , AWS Config runs evaluations once every three hours. In this case, ``Three_Hours`` is the frequency of this rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-sourcedetail.html#cfn-config-configrule-sourcedetail-maximumexecutionfrequency
            '''
            result = self._values.get("maximum_execution_frequency")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message_type(self) -> typing.Optional[builtins.str]:
            '''The type of notification that triggers AWS Config to run an evaluation for a rule.

            You can specify the following notification types:

            - ``ConfigurationItemChangeNotification`` - Triggers an evaluation when AWS Config delivers a configuration item as a result of a resource change.
            - ``OversizedConfigurationItemChangeNotification`` - Triggers an evaluation when AWS Config delivers an oversized configuration item. AWS Config may generate this notification type when a resource changes and the notification exceeds the maximum size allowed by Amazon SNS.
            - ``ScheduledNotification`` - Triggers a periodic evaluation at the frequency specified for ``MaximumExecutionFrequency`` .
            - ``ConfigurationSnapshotDeliveryCompleted`` - Triggers a periodic evaluation when AWS Config delivers a configuration snapshot.

            If you want your custom rule to be triggered by configuration changes, specify two SourceDetail objects, one for ``ConfigurationItemChangeNotification`` and one for ``OversizedConfigurationItemChangeNotification`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-sourcedetail.html#cfn-config-configrule-sourcedetail-messagetype
            '''
            result = self._values.get("message_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConfigRulePropsMixin.SourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_policy_details": "customPolicyDetails",
            "owner": "owner",
            "source_details": "sourceDetails",
            "source_identifier": "sourceIdentifier",
        },
    )
    class SourceProperty:
        def __init__(
            self,
            *,
            custom_policy_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigRulePropsMixin.CustomPolicyDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            owner: typing.Optional[builtins.str] = None,
            source_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigRulePropsMixin.SourceDetailProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            source_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the CustomPolicyDetails, the rule owner ( ``AWS`` for managed rules, ``CUSTOM_POLICY`` for Custom Policy rules, and ``CUSTOM_LAMBDA`` for Custom Lambda rules), the rule identifier, and the events that cause the evaluation of your AWS resources.

            :param custom_policy_details: Provides the runtime system, policy definition, and whether debug logging is enabled. Required when owner is set to ``CUSTOM_POLICY`` .
            :param owner: Indicates whether AWS or the customer owns and manages the AWS Config rule. AWS Config Managed Rules are predefined rules owned by AWS . For more information, see `AWS Config Managed Rules <https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_use-managed-rules.html>`_ in the *AWS Config developer guide* . AWS Config Custom Rules are rules that you can develop either with Guard ( ``CUSTOM_POLICY`` ) or AWS Lambda ( ``CUSTOM_LAMBDA`` ). For more information, see `AWS Config Custom Rules <https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_develop-rules.html>`_ in the *AWS Config developer guide* .
            :param source_details: Provides the source and the message types that cause AWS Config to evaluate your AWS resources against a rule. It also provides the frequency with which you want AWS Config to run evaluations for the rule if the trigger type is periodic. If the owner is set to ``CUSTOM_POLICY`` , the only acceptable values for the AWS Config rule trigger message type are ``ConfigurationItemChangeNotification`` and ``OversizedConfigurationItemChangeNotification`` .
            :param source_identifier: For AWS Config Managed rules, a predefined identifier from a list. For example, ``IAM_PASSWORD_POLICY`` is a managed rule. To reference a managed rule, see `List of AWS Config Managed Rules <https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html>`_ . For AWS Config Custom Lambda rules, the identifier is the Amazon Resource Name (ARN) of the rule's AWS Lambda function, such as ``arn:aws:lambda:us-east-2:123456789012:function:custom_rule_name`` . For AWS Config Custom Policy rules, this field will be ignored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                source_property = config_mixins.CfnConfigRulePropsMixin.SourceProperty(
                    custom_policy_details=config_mixins.CfnConfigRulePropsMixin.CustomPolicyDetailsProperty(
                        enable_debug_log_delivery=False,
                        policy_runtime="policyRuntime",
                        policy_text="policyText"
                    ),
                    owner="owner",
                    source_details=[config_mixins.CfnConfigRulePropsMixin.SourceDetailProperty(
                        event_source="eventSource",
                        maximum_execution_frequency="maximumExecutionFrequency",
                        message_type="messageType"
                    )],
                    source_identifier="sourceIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e13f77c9cc5081c54dc4b29bf02dd1e56062ab06ef219148e0a87d0d35188ab7)
                check_type(argname="argument custom_policy_details", value=custom_policy_details, expected_type=type_hints["custom_policy_details"])
                check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
                check_type(argname="argument source_details", value=source_details, expected_type=type_hints["source_details"])
                check_type(argname="argument source_identifier", value=source_identifier, expected_type=type_hints["source_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_policy_details is not None:
                self._values["custom_policy_details"] = custom_policy_details
            if owner is not None:
                self._values["owner"] = owner
            if source_details is not None:
                self._values["source_details"] = source_details
            if source_identifier is not None:
                self._values["source_identifier"] = source_identifier

        @builtins.property
        def custom_policy_details(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigRulePropsMixin.CustomPolicyDetailsProperty"]]:
            '''Provides the runtime system, policy definition, and whether debug logging is enabled.

            Required when owner is set to ``CUSTOM_POLICY`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source.html#cfn-config-configrule-source-custompolicydetails
            '''
            result = self._values.get("custom_policy_details")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigRulePropsMixin.CustomPolicyDetailsProperty"]], result)

        @builtins.property
        def owner(self) -> typing.Optional[builtins.str]:
            '''Indicates whether AWS or the customer owns and manages the AWS Config rule.

            AWS Config Managed Rules are predefined rules owned by AWS . For more information, see `AWS Config Managed Rules <https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_use-managed-rules.html>`_ in the *AWS Config developer guide* .

            AWS Config Custom Rules are rules that you can develop either with Guard ( ``CUSTOM_POLICY`` ) or AWS Lambda ( ``CUSTOM_LAMBDA`` ). For more information, see `AWS Config Custom Rules <https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_develop-rules.html>`_ in the *AWS Config developer guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source.html#cfn-config-configrule-source-owner
            '''
            result = self._values.get("owner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_details(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigRulePropsMixin.SourceDetailProperty"]]]]:
            '''Provides the source and the message types that cause AWS Config to evaluate your AWS resources against a rule.

            It also provides the frequency with which you want AWS Config to run evaluations for the rule if the trigger type is periodic.

            If the owner is set to ``CUSTOM_POLICY`` , the only acceptable values for the AWS Config rule trigger message type are ``ConfigurationItemChangeNotification`` and ``OversizedConfigurationItemChangeNotification`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source.html#cfn-config-configrule-source-sourcedetails
            '''
            result = self._values.get("source_details")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigRulePropsMixin.SourceDetailProperty"]]]], result)

        @builtins.property
        def source_identifier(self) -> typing.Optional[builtins.str]:
            '''For AWS Config Managed rules, a predefined identifier from a list.

            For example, ``IAM_PASSWORD_POLICY`` is a managed rule. To reference a managed rule, see `List of AWS Config Managed Rules <https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html>`_ .

            For AWS Config Custom Lambda rules, the identifier is the Amazon Resource Name (ARN) of the rule's AWS Lambda function, such as ``arn:aws:lambda:us-east-2:123456789012:function:custom_rule_name`` .

            For AWS Config Custom Policy rules, this field will be ignored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source.html#cfn-config-configrule-source-sourceidentifier
            '''
            result = self._values.get("source_identifier")
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
    jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConfigurationAggregatorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_aggregation_sources": "accountAggregationSources",
        "configuration_aggregator_name": "configurationAggregatorName",
        "organization_aggregation_source": "organizationAggregationSource",
        "tags": "tags",
    },
)
class CfnConfigurationAggregatorMixinProps:
    def __init__(
        self,
        *,
        account_aggregation_sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationAggregatorPropsMixin.AccountAggregationSourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        configuration_aggregator_name: typing.Optional[builtins.str] = None,
        organization_aggregation_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationAggregatorPropsMixin.OrganizationAggregationSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnConfigurationAggregatorPropsMixin.

        :param account_aggregation_sources: Provides a list of source accounts and regions to be aggregated.
        :param configuration_aggregator_name: The name of the aggregator.
        :param organization_aggregation_source: Provides an organization and list of regions to be aggregated.
        :param tags: An array of tag object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
            
            cfn_configuration_aggregator_mixin_props = config_mixins.CfnConfigurationAggregatorMixinProps(
                account_aggregation_sources=[config_mixins.CfnConfigurationAggregatorPropsMixin.AccountAggregationSourceProperty(
                    account_ids=["accountIds"],
                    all_aws_regions=False,
                    aws_regions=["awsRegions"]
                )],
                configuration_aggregator_name="configurationAggregatorName",
                organization_aggregation_source=config_mixins.CfnConfigurationAggregatorPropsMixin.OrganizationAggregationSourceProperty(
                    all_aws_regions=False,
                    aws_regions=["awsRegions"],
                    role_arn="roleArn"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0381f19f39525ff3a932ec25afc47652e45308ad8a07a797e3fc74aa8eb317c)
            check_type(argname="argument account_aggregation_sources", value=account_aggregation_sources, expected_type=type_hints["account_aggregation_sources"])
            check_type(argname="argument configuration_aggregator_name", value=configuration_aggregator_name, expected_type=type_hints["configuration_aggregator_name"])
            check_type(argname="argument organization_aggregation_source", value=organization_aggregation_source, expected_type=type_hints["organization_aggregation_source"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_aggregation_sources is not None:
            self._values["account_aggregation_sources"] = account_aggregation_sources
        if configuration_aggregator_name is not None:
            self._values["configuration_aggregator_name"] = configuration_aggregator_name
        if organization_aggregation_source is not None:
            self._values["organization_aggregation_source"] = organization_aggregation_source
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def account_aggregation_sources(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationAggregatorPropsMixin.AccountAggregationSourceProperty"]]]]:
        '''Provides a list of source accounts and regions to be aggregated.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html#cfn-config-configurationaggregator-accountaggregationsources
        '''
        result = self._values.get("account_aggregation_sources")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationAggregatorPropsMixin.AccountAggregationSourceProperty"]]]], result)

    @builtins.property
    def configuration_aggregator_name(self) -> typing.Optional[builtins.str]:
        '''The name of the aggregator.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html#cfn-config-configurationaggregator-configurationaggregatorname
        '''
        result = self._values.get("configuration_aggregator_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization_aggregation_source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationAggregatorPropsMixin.OrganizationAggregationSourceProperty"]]:
        '''Provides an organization and list of regions to be aggregated.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html#cfn-config-configurationaggregator-organizationaggregationsource
        '''
        result = self._values.get("organization_aggregation_source")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationAggregatorPropsMixin.OrganizationAggregationSourceProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of tag object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html#cfn-config-configurationaggregator-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationAggregatorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConfigurationAggregatorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConfigurationAggregatorPropsMixin",
):
    '''The details about the configuration aggregator, including information about source accounts, regions, and metadata of the aggregator.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html
    :cloudformationResource: AWS::Config::ConfigurationAggregator
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
        
        cfn_configuration_aggregator_props_mixin = config_mixins.CfnConfigurationAggregatorPropsMixin(config_mixins.CfnConfigurationAggregatorMixinProps(
            account_aggregation_sources=[config_mixins.CfnConfigurationAggregatorPropsMixin.AccountAggregationSourceProperty(
                account_ids=["accountIds"],
                all_aws_regions=False,
                aws_regions=["awsRegions"]
            )],
            configuration_aggregator_name="configurationAggregatorName",
            organization_aggregation_source=config_mixins.CfnConfigurationAggregatorPropsMixin.OrganizationAggregationSourceProperty(
                all_aws_regions=False,
                aws_regions=["awsRegions"],
                role_arn="roleArn"
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
        props: typing.Union[CfnConfigurationAggregatorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Config::ConfigurationAggregator``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c71a3eeae8bb1b428f5a41fd3d615c8958c9bc9da0a4211beb45d2d69635aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83dc801e229b2a30fa7b3c2fded0d84305176c6ba038f295c1e9408007e20cc9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d49662de6cb1d93c298c704aec9f6be9ff14e2c087f74e752a838e46b57f64b5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConfigurationAggregatorMixinProps:
        return typing.cast(CfnConfigurationAggregatorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConfigurationAggregatorPropsMixin.AccountAggregationSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_ids": "accountIds",
            "all_aws_regions": "allAwsRegions",
            "aws_regions": "awsRegions",
        },
    )
    class AccountAggregationSourceProperty:
        def __init__(
            self,
            *,
            account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            all_aws_regions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A collection of accounts and regions.

            :param account_ids: The 12-digit account ID of the account being aggregated.
            :param all_aws_regions: If true, aggregate existing AWS Config regions and future regions.
            :param aws_regions: The source regions being aggregated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-accountaggregationsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                account_aggregation_source_property = config_mixins.CfnConfigurationAggregatorPropsMixin.AccountAggregationSourceProperty(
                    account_ids=["accountIds"],
                    all_aws_regions=False,
                    aws_regions=["awsRegions"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__982f70e15b26c35d548bb09482d4c9f010a7763be3aa0ac42a008594ef732dfa)
                check_type(argname="argument account_ids", value=account_ids, expected_type=type_hints["account_ids"])
                check_type(argname="argument all_aws_regions", value=all_aws_regions, expected_type=type_hints["all_aws_regions"])
                check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_ids is not None:
                self._values["account_ids"] = account_ids
            if all_aws_regions is not None:
                self._values["all_aws_regions"] = all_aws_regions
            if aws_regions is not None:
                self._values["aws_regions"] = aws_regions

        @builtins.property
        def account_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The 12-digit account ID of the account being aggregated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-accountaggregationsource.html#cfn-config-configurationaggregator-accountaggregationsource-accountids
            '''
            result = self._values.get("account_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def all_aws_regions(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If true, aggregate existing AWS Config regions and future regions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-accountaggregationsource.html#cfn-config-configurationaggregator-accountaggregationsource-allawsregions
            '''
            result = self._values.get("all_aws_regions")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The source regions being aggregated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-accountaggregationsource.html#cfn-config-configurationaggregator-accountaggregationsource-awsregions
            '''
            result = self._values.get("aws_regions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccountAggregationSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConfigurationAggregatorPropsMixin.OrganizationAggregationSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "all_aws_regions": "allAwsRegions",
            "aws_regions": "awsRegions",
            "role_arn": "roleArn",
        },
    )
    class OrganizationAggregationSourceProperty:
        def __init__(
            self,
            *,
            all_aws_regions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This object contains regions to set up the aggregator and an IAM role to retrieve organization details.

            :param all_aws_regions: If true, aggregate existing AWS Config regions and future regions.
            :param aws_regions: The source regions being aggregated.
            :param role_arn: ARN of the IAM role used to retrieve AWS Organizations details associated with the aggregator account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-organizationaggregationsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                organization_aggregation_source_property = config_mixins.CfnConfigurationAggregatorPropsMixin.OrganizationAggregationSourceProperty(
                    all_aws_regions=False,
                    aws_regions=["awsRegions"],
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0ffaba91f122a12bf9cdabdc4a50595d22f75f5bf9466c23e01b53910376c9bb)
                check_type(argname="argument all_aws_regions", value=all_aws_regions, expected_type=type_hints["all_aws_regions"])
                check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if all_aws_regions is not None:
                self._values["all_aws_regions"] = all_aws_regions
            if aws_regions is not None:
                self._values["aws_regions"] = aws_regions
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def all_aws_regions(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If true, aggregate existing AWS Config regions and future regions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-organizationaggregationsource.html#cfn-config-configurationaggregator-organizationaggregationsource-allawsregions
            '''
            result = self._values.get("all_aws_regions")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The source regions being aggregated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-organizationaggregationsource.html#cfn-config-configurationaggregator-organizationaggregationsource-awsregions
            '''
            result = self._values.get("aws_regions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the IAM role used to retrieve AWS Organizations details associated with the aggregator account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-organizationaggregationsource.html#cfn-config-configurationaggregator-organizationaggregationsource-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OrganizationAggregationSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConfigurationRecorderMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "recording_group": "recordingGroup",
        "recording_mode": "recordingMode",
        "role_arn": "roleArn",
    },
)
class CfnConfigurationRecorderMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        recording_group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationRecorderPropsMixin.RecordingGroupProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        recording_mode: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationRecorderPropsMixin.RecordingModeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnConfigurationRecorderPropsMixin.

        :param name: The name of the configuration recorder. AWS Config automatically assigns the name of "default" when creating the configuration recorder. You cannot change the name of the configuration recorder after it has been created. To change the configuration recorder name, you must delete it and create a new configuration recorder with a new name.
        :param recording_group: Specifies which resource types AWS Config records for configuration changes. .. epigraph:: *High Number of AWS Config Evaluations* You may notice increased activity in your account during your initial month recording with AWS Config when compared to subsequent months. During the initial bootstrapping process, AWS Config runs evaluations on all the resources in your account that you have selected for AWS Config to record. If you are running ephemeral workloads, you may see increased activity from AWS Config as it records configuration changes associated with creating and deleting these temporary resources. An *ephemeral workload* is a temporary use of computing resources that are loaded and run when needed. Examples include Amazon Elastic Compute Cloud ( Amazon EC2 ) Spot Instances, Amazon EMR jobs, and AWS Auto Scaling . If you want to avoid the increased activity from running ephemeral workloads, you can run these types of workloads in a separate account with AWS Config turned off to avoid increased configuration recording and rule evaluations.
        :param recording_mode: Specifies the default recording frequency for the configuration recorder. AWS Config supports *Continuous recording* and *Daily recording* . - Continuous recording allows you to record configuration changes continuously whenever a change occurs. - Daily recording allows you to receive a configuration item (CI) representing the most recent state of your resources over the last 24-hour period, only if it’s different from the previous CI recorded. .. epigraph:: *Some resource types require continuous recording* AWS Firewall Manager depends on continuous recording to monitor your resources. If you are using Firewall Manager, it is recommended that you set the recording frequency to Continuous. You can also override the recording frequency for specific resource types.
        :param role_arn: Amazon Resource Name (ARN) of the IAM role assumed by AWS Config and used by the configuration recorder. For more information, see `Permissions for the IAM Role Assigned <https://docs.aws.amazon.com/config/latest/developerguide/iamrole-permissions.html>`_ to AWS Config in the AWS Config Developer Guide. .. epigraph:: *Pre-existing AWS Config role* If you have used an AWS service that uses AWS Config , such as Security Hub or AWS Control Tower , and an AWS Config role has already been created, make sure that the IAM role that you use when setting up AWS Config keeps the same minimum permissions as the already created AWS Config role. You must do this so that the other AWS service continues to run as expected. For example, if AWS Control Tower has an IAM role that allows AWS Config to read Amazon Simple Storage Service ( Amazon S3 ) objects, make sure that the same permissions are granted within the IAM role you use when setting up AWS Config . Otherwise, it may interfere with how AWS Control Tower operates. For more information about IAM roles for AWS Config , see `*Identity and Access Management for AWS Config* <https://docs.aws.amazon.com/config/latest/developerguide/security-iam.html>`_ in the *AWS Config Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
            
            cfn_configuration_recorder_mixin_props = config_mixins.CfnConfigurationRecorderMixinProps(
                name="name",
                recording_group=config_mixins.CfnConfigurationRecorderPropsMixin.RecordingGroupProperty(
                    all_supported=False,
                    exclusion_by_resource_types=config_mixins.CfnConfigurationRecorderPropsMixin.ExclusionByResourceTypesProperty(
                        resource_types=["resourceTypes"]
                    ),
                    include_global_resource_types=False,
                    recording_strategy=config_mixins.CfnConfigurationRecorderPropsMixin.RecordingStrategyProperty(
                        use_only="useOnly"
                    ),
                    resource_types=["resourceTypes"]
                ),
                recording_mode=config_mixins.CfnConfigurationRecorderPropsMixin.RecordingModeProperty(
                    recording_frequency="recordingFrequency",
                    recording_mode_overrides=[config_mixins.CfnConfigurationRecorderPropsMixin.RecordingModeOverrideProperty(
                        description="description",
                        recording_frequency="recordingFrequency",
                        resource_types=["resourceTypes"]
                    )]
                ),
                role_arn="roleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8da3e650909252ee7badd1d153a9c8bb8be2c6125c266398da94410eb48439d4)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument recording_group", value=recording_group, expected_type=type_hints["recording_group"])
            check_type(argname="argument recording_mode", value=recording_mode, expected_type=type_hints["recording_mode"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if recording_group is not None:
            self._values["recording_group"] = recording_group
        if recording_mode is not None:
            self._values["recording_mode"] = recording_mode
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the configuration recorder. AWS Config automatically assigns the name of "default" when creating the configuration recorder.

        You cannot change the name of the configuration recorder after it has been created. To change the configuration recorder name, you must delete it and create a new configuration recorder with a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html#cfn-config-configurationrecorder-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recording_group(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationRecorderPropsMixin.RecordingGroupProperty"]]:
        '''Specifies which resource types AWS Config records for configuration changes.

        .. epigraph::

           *High Number of AWS Config Evaluations*

           You may notice increased activity in your account during your initial month recording with AWS Config when compared to subsequent months. During the initial bootstrapping process, AWS Config runs evaluations on all the resources in your account that you have selected for AWS Config to record.

           If you are running ephemeral workloads, you may see increased activity from AWS Config as it records configuration changes associated with creating and deleting these temporary resources. An *ephemeral workload* is a temporary use of computing resources that are loaded and run when needed. Examples include Amazon Elastic Compute Cloud ( Amazon EC2 ) Spot Instances, Amazon EMR jobs, and AWS Auto Scaling . If you want to avoid the increased activity from running ephemeral workloads, you can run these types of workloads in a separate account with AWS Config turned off to avoid increased configuration recording and rule evaluations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html#cfn-config-configurationrecorder-recordinggroup
        '''
        result = self._values.get("recording_group")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationRecorderPropsMixin.RecordingGroupProperty"]], result)

    @builtins.property
    def recording_mode(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationRecorderPropsMixin.RecordingModeProperty"]]:
        '''Specifies the default recording frequency for the configuration recorder. AWS Config supports *Continuous recording* and *Daily recording* .

        - Continuous recording allows you to record configuration changes continuously whenever a change occurs.
        - Daily recording allows you to receive a configuration item (CI) representing the most recent state of your resources over the last 24-hour period, only if it’s different from the previous CI recorded.

        .. epigraph::

           *Some resource types require continuous recording*

           AWS Firewall Manager depends on continuous recording to monitor your resources. If you are using Firewall Manager, it is recommended that you set the recording frequency to Continuous.

        You can also override the recording frequency for specific resource types.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html#cfn-config-configurationrecorder-recordingmode
        '''
        result = self._values.get("recording_mode")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationRecorderPropsMixin.RecordingModeProperty"]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''Amazon Resource Name (ARN) of the IAM role assumed by AWS Config and used by the configuration recorder.

        For more information, see `Permissions for the IAM Role Assigned <https://docs.aws.amazon.com/config/latest/developerguide/iamrole-permissions.html>`_ to AWS Config in the AWS Config Developer Guide.
        .. epigraph::

           *Pre-existing AWS Config role*

           If you have used an AWS service that uses AWS Config , such as Security Hub or AWS Control Tower , and an AWS Config role has already been created, make sure that the IAM role that you use when setting up AWS Config keeps the same minimum permissions as the already created AWS Config role. You must do this so that the other AWS service continues to run as expected.

           For example, if AWS Control Tower has an IAM role that allows AWS Config to read Amazon Simple Storage Service ( Amazon S3 ) objects, make sure that the same permissions are granted within the IAM role you use when setting up AWS Config . Otherwise, it may interfere with how AWS Control Tower operates. For more information about IAM roles for AWS Config , see `*Identity and Access Management for AWS Config* <https://docs.aws.amazon.com/config/latest/developerguide/security-iam.html>`_ in the *AWS Config Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html#cfn-config-configurationrecorder-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationRecorderMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConfigurationRecorderPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConfigurationRecorderPropsMixin",
):
    '''The ``AWS::Config::ConfigurationRecorder`` resource type describes the AWS resource types that AWS Config records for configuration changes.

    The configuration recorder stores the configuration changes of the specified resources in your account as configuration items.
    .. epigraph::

       To enable AWS Config , you must create a configuration recorder and a delivery channel.

       AWS Config uses the delivery channel to deliver the configuration changes to your Amazon S3 bucket or Amazon  topic. For more information, see `AWS::Config::DeliveryChannel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html>`_ .

    AWS CloudFormation starts the recorder as soon as the delivery channel is available.

    To stop the recorder and delete it, delete the configuration recorder from your stack. To stop the recorder without deleting it, call the `StopConfigurationRecorder <https://docs.aws.amazon.com/config/latest/APIReference/API_StopConfigurationRecorder.html>`_ action of the AWS Config API directly.

    For more information, see `Configuration Recorder <https://docs.aws.amazon.com/config/latest/developerguide/config-concepts.html#config-recorder>`_ in the AWS Config Developer Guide.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html
    :cloudformationResource: AWS::Config::ConfigurationRecorder
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
        
        cfn_configuration_recorder_props_mixin = config_mixins.CfnConfigurationRecorderPropsMixin(config_mixins.CfnConfigurationRecorderMixinProps(
            name="name",
            recording_group=config_mixins.CfnConfigurationRecorderPropsMixin.RecordingGroupProperty(
                all_supported=False,
                exclusion_by_resource_types=config_mixins.CfnConfigurationRecorderPropsMixin.ExclusionByResourceTypesProperty(
                    resource_types=["resourceTypes"]
                ),
                include_global_resource_types=False,
                recording_strategy=config_mixins.CfnConfigurationRecorderPropsMixin.RecordingStrategyProperty(
                    use_only="useOnly"
                ),
                resource_types=["resourceTypes"]
            ),
            recording_mode=config_mixins.CfnConfigurationRecorderPropsMixin.RecordingModeProperty(
                recording_frequency="recordingFrequency",
                recording_mode_overrides=[config_mixins.CfnConfigurationRecorderPropsMixin.RecordingModeOverrideProperty(
                    description="description",
                    recording_frequency="recordingFrequency",
                    resource_types=["resourceTypes"]
                )]
            ),
            role_arn="roleArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnConfigurationRecorderMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Config::ConfigurationRecorder``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__219c3f861c0cd4cc17f82ec1a5cf3a0e84894fbbe11507f18e3f6b8591fec990)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a68941b4b53c7b6783110d704b2d5b00b936b5d04958ac81fb9711ab6c3991c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cc729bc4fdb06fff057a3fd98a12b3d227e4bfb4652d659bc46e61018fd0984)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConfigurationRecorderMixinProps:
        return typing.cast(CfnConfigurationRecorderMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConfigurationRecorderPropsMixin.ExclusionByResourceTypesProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_types": "resourceTypes"},
    )
    class ExclusionByResourceTypesProperty:
        def __init__(
            self,
            *,
            resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies whether the configuration recorder excludes certain resource types from being recorded.

            Use the ``ResourceTypes`` field to enter a comma-separated list of resource types you want to exclude from recording.

            By default, when AWS Config adds support for a new resource type in the Region where you set up the configuration recorder, including global resource types, AWS Config starts recording resources of that type automatically.
            .. epigraph::

               *How to use the exclusion recording strategy*

               To use this option, you must set the ``useOnly`` field of `RecordingStrategy <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingStrategy.html>`_ to ``EXCLUSION_BY_RESOURCE_TYPES`` .

               AWS Config will then record configuration changes for all supported resource types, except the resource types that you specify to exclude from being recorded.

               *Global resource types and the exclusion recording strategy*

               Unless specifically listed as exclusions, ``AWS::RDS::GlobalCluster`` will be recorded automatically in all supported AWS Config Regions were the configuration recorder is enabled.

               IAM users, groups, roles, and customer managed policies will be recorded in the Region where you set up the configuration recorder if that is a Region where AWS Config was available before February 2022. You cannot be record the global IAM resouce types in Regions supported by AWS Config after February 2022. This list where you cannot record the global IAM resource types includes the following Regions:

               - Asia Pacific (Hyderabad)
               - Asia Pacific (Melbourne)
               - Canada West (Calgary)
               - Europe (Spain)
               - Europe (Zurich)
               - Israel (Tel Aviv)
               - Middle East (UAE)

            :param resource_types: A comma-separated list of resource types to exclude from recording by the configuration recorder.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-exclusionbyresourcetypes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                exclusion_by_resource_types_property = config_mixins.CfnConfigurationRecorderPropsMixin.ExclusionByResourceTypesProperty(
                    resource_types=["resourceTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd7a67fbac2c9b50c32be49998332ad7ae51631546058cfbc8ce060e050aae81)
                check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_types is not None:
                self._values["resource_types"] = resource_types

        @builtins.property
        def resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A comma-separated list of resource types to exclude from recording by the configuration recorder.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-exclusionbyresourcetypes.html#cfn-config-configurationrecorder-exclusionbyresourcetypes-resourcetypes
            '''
            result = self._values.get("resource_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExclusionByResourceTypesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConfigurationRecorderPropsMixin.RecordingGroupProperty",
        jsii_struct_bases=[],
        name_mapping={
            "all_supported": "allSupported",
            "exclusion_by_resource_types": "exclusionByResourceTypes",
            "include_global_resource_types": "includeGlobalResourceTypes",
            "recording_strategy": "recordingStrategy",
            "resource_types": "resourceTypes",
        },
    )
    class RecordingGroupProperty:
        def __init__(
            self,
            *,
            all_supported: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            exclusion_by_resource_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationRecorderPropsMixin.ExclusionByResourceTypesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            include_global_resource_types: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            recording_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationRecorderPropsMixin.RecordingStrategyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies which resource types AWS Config records for configuration changes.

            By default, AWS Config records configuration changes for all current and future supported resource types in the AWS Region where you have enabled AWS Config , excluding the global IAM resource types: IAM users, groups, roles, and customer managed policies.

            In the recording group, you specify whether you want to record all supported current and future supported resource types or to include or exclude specific resources types. For a list of supported resource types, see `Supported Resource Types <https://docs.aws.amazon.com/config/latest/developerguide/resource-config-reference.html#supported-resources>`_ in the *AWS Config developer guide* .

            If you don't want AWS Config to record all current and future supported resource types (excluding the global IAM resource types), use one of the following recording strategies:

            - *Record all current and future resource types with exclusions* ( ``EXCLUSION_BY_RESOURCE_TYPES`` ), or
            - *Record specific resource types* ( ``INCLUSION_BY_RESOURCE_TYPES`` ).

            If you use the recording strategy to *Record all current and future resource types* ( ``ALL_SUPPORTED_RESOURCE_TYPES`` ), you can use the flag ``IncludeGlobalResourceTypes`` to include the global IAM resource types in your recording.
            .. epigraph::

               *Aurora global clusters are recorded in all enabled Regions*

               The ``AWS::RDS::GlobalCluster`` resource type will be recorded in all supported AWS Config Regions where the configuration recorder is enabled.

               If you do not want to record ``AWS::RDS::GlobalCluster`` in all enabled Regions, use the ``EXCLUSION_BY_RESOURCE_TYPES`` or ``INCLUSION_BY_RESOURCE_TYPES`` recording strategy.

            :param all_supported: Specifies whether AWS Config records configuration changes for all supported resource types, excluding the global IAM resource types. If you set this field to ``true`` , when AWS Config adds support for a new resource type, AWS Config starts recording resources of that type automatically. If you set this field to ``true`` , you cannot enumerate specific resource types to record in the ``resourceTypes`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ , or to exclude in the ``resourceTypes`` field of `ExclusionByResourceTypes <https://docs.aws.amazon.com/config/latest/APIReference/API_ExclusionByResourceTypes.html>`_ . .. epigraph:: *Region availability* Check `Resource Coverage by Region Availability <https://docs.aws.amazon.com/config/latest/developerguide/what-is-resource-config-coverage.html>`_ to see if a resource type is supported in the AWS Region where you set up AWS Config .
            :param exclusion_by_resource_types: An object that specifies how AWS Config excludes resource types from being recorded by the configuration recorder. To use this option, you must set the ``useOnly`` field of `AWS::Config::ConfigurationRecorder RecordingStrategy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordingstrategy.html>`_ to ``EXCLUSION_BY_RESOURCE_TYPES`` .
            :param include_global_resource_types: This option is a bundle which only applies to the global IAM resource types: IAM users, groups, roles, and customer managed policies. These global IAM resource types can only be recorded by AWS Config in Regions where AWS Config was available before February 2022. You cannot be record the global IAM resouce types in Regions supported by AWS Config after February 2022. This list where you cannot record the global IAM resource types includes the following Regions: - Asia Pacific (Hyderabad) - Asia Pacific (Melbourne) - Canada West (Calgary) - Europe (Spain) - Europe (Zurich) - Israel (Tel Aviv) - Middle East (UAE) .. epigraph:: *Aurora global clusters are recorded in all enabled Regions* The ``AWS::RDS::GlobalCluster`` resource type will be recorded in all supported AWS Config Regions where the configuration recorder is enabled, even if ``IncludeGlobalResourceTypes`` is set to ``false`` . The ``IncludeGlobalResourceTypes`` option is a bundle which only applies to IAM users, groups, roles, and customer managed policies. If you do not want to record ``AWS::RDS::GlobalCluster`` in all enabled Regions, use one of the following recording strategies: - *Record all current and future resource types with exclusions* ( ``EXCLUSION_BY_RESOURCE_TYPES`` ), or - *Record specific resource types* ( ``INCLUSION_BY_RESOURCE_TYPES`` ). For more information, see `Selecting Which Resources are Recorded <https://docs.aws.amazon.com/config/latest/developerguide/select-resources.html#select-resources-all>`_ in the *AWS Config developer guide* . > *IncludeGlobalResourceTypes and the exclusion recording strategy* The ``IncludeGlobalResourceTypes`` field has no impact on the ``EXCLUSION_BY_RESOURCE_TYPES`` recording strategy. This means that the global IAM resource types ( IAM users, groups, roles, and customer managed policies) will not be automatically added as exclusions for ``ExclusionByResourceTypes`` when ``IncludeGlobalResourceTypes`` is set to ``false`` . The ``IncludeGlobalResourceTypes`` field should only be used to modify the ``AllSupported`` field, as the default for the ``AllSupported`` field is to record configuration changes for all supported resource types excluding the global IAM resource types. To include the global IAM resource types when ``AllSupported`` is set to ``true`` , make sure to set ``IncludeGlobalResourceTypes`` to ``true`` . To exclude the global IAM resource types for the ``EXCLUSION_BY_RESOURCE_TYPES`` recording strategy, you need to manually add them to the ``ResourceTypes`` field of ``ExclusionByResourceTypes`` . > *Required and optional fields* Before you set this field to ``true`` , set the ``AllSupported`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ to ``true`` . Optionally, you can set the ``useOnly`` field of `RecordingStrategy <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingStrategy.html>`_ to ``ALL_SUPPORTED_RESOURCE_TYPES`` . > *Overriding fields* If you set this field to ``false`` but list global IAM resource types in the ``ResourceTypes`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ , AWS Config will still record configuration changes for those specified resource types *regardless* of if you set the ``IncludeGlobalResourceTypes`` field to false. If you do not want to record configuration changes to the global IAM resource types (IAM users, groups, roles, and customer managed policies), make sure to not list them in the ``ResourceTypes`` field in addition to setting the ``IncludeGlobalResourceTypes`` field to false.
            :param recording_strategy: An object that specifies the recording strategy for the configuration recorder. - If you set the ``useOnly`` field of `RecordingStrategy <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingStrategy.html>`_ to ``ALL_SUPPORTED_RESOURCE_TYPES`` , AWS Config records configuration changes for all supported resource types, excluding the global IAM resource types. You also must set the ``AllSupported`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ to ``true`` . When AWS Config adds support for a new resource type, AWS Config automatically starts recording resources of that type. - If you set the ``useOnly`` field of `RecordingStrategy <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingStrategy.html>`_ to ``INCLUSION_BY_RESOURCE_TYPES`` , AWS Config records configuration changes for only the resource types you specify in the ``ResourceTypes`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ . - If you set the ``useOnly`` field of `RecordingStrategy <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingStrategy.html>`_ to ``EXCLUSION_BY_RESOURCE_TYPES`` , AWS Config records configuration changes for all supported resource types except the resource types that you specify to exclude from being recorded in the ``ResourceTypes`` field of `ExclusionByResourceTypes <https://docs.aws.amazon.com/config/latest/APIReference/API_ExclusionByResourceTypes.html>`_ . .. epigraph:: *Required and optional fields* The ``recordingStrategy`` field is optional when you set the ``AllSupported`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ to ``true`` . The ``recordingStrategy`` field is optional when you list resource types in the ``ResourceTypes`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ . The ``recordingStrategy`` field is required if you list resource types to exclude from recording in the ``ResourceTypes`` field of `ExclusionByResourceTypes <https://docs.aws.amazon.com/config/latest/APIReference/API_ExclusionByResourceTypes.html>`_ . > *Overriding fields* If you choose ``EXCLUSION_BY_RESOURCE_TYPES`` for the recording strategy, the ``ExclusionByResourceTypes`` field will override other properties in the request. For example, even if you set ``IncludeGlobalResourceTypes`` to false, global IAM resource types will still be automatically recorded in this option unless those resource types are specifically listed as exclusions in the ``ResourceTypes`` field of ``ExclusionByResourceTypes`` . > *Global resources types and the resource exclusion recording strategy* By default, if you choose the ``EXCLUSION_BY_RESOURCE_TYPES`` recording strategy, when AWS Config adds support for a new resource type in the Region where you set up the configuration recorder, including global resource types, AWS Config starts recording resources of that type automatically. Unless specifically listed as exclusions, ``AWS::RDS::GlobalCluster`` will be recorded automatically in all supported AWS Config Regions were the configuration recorder is enabled. IAM users, groups, roles, and customer managed policies will be recorded in the Region where you set up the configuration recorder if that is a Region where AWS Config was available before February 2022. You cannot be record the global IAM resouce types in Regions supported by AWS Config after February 2022. This list where you cannot record the global IAM resource types includes the following Regions: - Asia Pacific (Hyderabad) - Asia Pacific (Melbourne) - Canada West (Calgary) - Europe (Spain) - Europe (Zurich) - Israel (Tel Aviv) - Middle East (UAE)
            :param resource_types: A comma-separated list that specifies which resource types AWS Config records. For a list of valid ``ResourceTypes`` values, see the *Resource Type Value* column in `Supported AWS resource Types <https://docs.aws.amazon.com/config/latest/developerguide/resource-config-reference.html#supported-resources>`_ in the *AWS Config developer guide* . .. epigraph:: *Required and optional fields* Optionally, you can set the ``useOnly`` field of `RecordingStrategy <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingStrategy.html>`_ to ``INCLUSION_BY_RESOURCE_TYPES`` . To record all configuration changes, set the ``AllSupported`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ to ``true`` , and either omit this field or don't specify any resource types in this field. If you set the ``AllSupported`` field to ``false`` and specify values for ``ResourceTypes`` , when AWS Config adds support for a new type of resource, it will not record resources of that type unless you manually add that type to your recording group. > *Region availability* Before specifying a resource type for AWS Config to track, check `Resource Coverage by Region Availability <https://docs.aws.amazon.com/config/latest/developerguide/what-is-resource-config-coverage.html>`_ to see if the resource type is supported in the AWS Region where you set up AWS Config . If a resource type is supported by AWS Config in at least one Region, you can enable the recording of that resource type in all Regions supported by AWS Config , even if the specified resource type is not supported in the AWS Region where you set up AWS Config .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordinggroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                recording_group_property = config_mixins.CfnConfigurationRecorderPropsMixin.RecordingGroupProperty(
                    all_supported=False,
                    exclusion_by_resource_types=config_mixins.CfnConfigurationRecorderPropsMixin.ExclusionByResourceTypesProperty(
                        resource_types=["resourceTypes"]
                    ),
                    include_global_resource_types=False,
                    recording_strategy=config_mixins.CfnConfigurationRecorderPropsMixin.RecordingStrategyProperty(
                        use_only="useOnly"
                    ),
                    resource_types=["resourceTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__27106b46ac4f7b2c70d9d63635ec89e3e5f81eddc6a87529e600dc3ec9922964)
                check_type(argname="argument all_supported", value=all_supported, expected_type=type_hints["all_supported"])
                check_type(argname="argument exclusion_by_resource_types", value=exclusion_by_resource_types, expected_type=type_hints["exclusion_by_resource_types"])
                check_type(argname="argument include_global_resource_types", value=include_global_resource_types, expected_type=type_hints["include_global_resource_types"])
                check_type(argname="argument recording_strategy", value=recording_strategy, expected_type=type_hints["recording_strategy"])
                check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if all_supported is not None:
                self._values["all_supported"] = all_supported
            if exclusion_by_resource_types is not None:
                self._values["exclusion_by_resource_types"] = exclusion_by_resource_types
            if include_global_resource_types is not None:
                self._values["include_global_resource_types"] = include_global_resource_types
            if recording_strategy is not None:
                self._values["recording_strategy"] = recording_strategy
            if resource_types is not None:
                self._values["resource_types"] = resource_types

        @builtins.property
        def all_supported(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether AWS Config records configuration changes for all supported resource types, excluding the global IAM resource types.

            If you set this field to ``true`` , when AWS Config adds support for a new resource type, AWS Config starts recording resources of that type automatically.

            If you set this field to ``true`` , you cannot enumerate specific resource types to record in the ``resourceTypes`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ , or to exclude in the ``resourceTypes`` field of `ExclusionByResourceTypes <https://docs.aws.amazon.com/config/latest/APIReference/API_ExclusionByResourceTypes.html>`_ .
            .. epigraph::

               *Region availability*

               Check `Resource Coverage by Region Availability <https://docs.aws.amazon.com/config/latest/developerguide/what-is-resource-config-coverage.html>`_ to see if a resource type is supported in the AWS Region where you set up AWS Config .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordinggroup.html#cfn-config-configurationrecorder-recordinggroup-allsupported
            '''
            result = self._values.get("all_supported")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def exclusion_by_resource_types(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationRecorderPropsMixin.ExclusionByResourceTypesProperty"]]:
            '''An object that specifies how AWS Config excludes resource types from being recorded by the configuration recorder.

            To use this option, you must set the ``useOnly`` field of `AWS::Config::ConfigurationRecorder RecordingStrategy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordingstrategy.html>`_ to ``EXCLUSION_BY_RESOURCE_TYPES`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordinggroup.html#cfn-config-configurationrecorder-recordinggroup-exclusionbyresourcetypes
            '''
            result = self._values.get("exclusion_by_resource_types")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationRecorderPropsMixin.ExclusionByResourceTypesProperty"]], result)

        @builtins.property
        def include_global_resource_types(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''This option is a bundle which only applies to the global IAM resource types: IAM users, groups, roles, and customer managed policies.

            These global IAM resource types can only be recorded by AWS Config in Regions where AWS Config was available before February 2022. You cannot be record the global IAM resouce types in Regions supported by AWS Config after February 2022. This list where you cannot record the global IAM resource types includes the following Regions:

            - Asia Pacific (Hyderabad)
            - Asia Pacific (Melbourne)
            - Canada West (Calgary)
            - Europe (Spain)
            - Europe (Zurich)
            - Israel (Tel Aviv)
            - Middle East (UAE)

            .. epigraph::

               *Aurora global clusters are recorded in all enabled Regions*

               The ``AWS::RDS::GlobalCluster`` resource type will be recorded in all supported AWS Config Regions where the configuration recorder is enabled, even if ``IncludeGlobalResourceTypes`` is set to ``false`` . The ``IncludeGlobalResourceTypes`` option is a bundle which only applies to IAM users, groups, roles, and customer managed policies.

               If you do not want to record ``AWS::RDS::GlobalCluster`` in all enabled Regions, use one of the following recording strategies:

               - *Record all current and future resource types with exclusions* ( ``EXCLUSION_BY_RESOURCE_TYPES`` ), or
               - *Record specific resource types* ( ``INCLUSION_BY_RESOURCE_TYPES`` ).

               For more information, see `Selecting Which Resources are Recorded <https://docs.aws.amazon.com/config/latest/developerguide/select-resources.html#select-resources-all>`_ in the *AWS Config developer guide* . > *IncludeGlobalResourceTypes and the exclusion recording strategy*

               The ``IncludeGlobalResourceTypes`` field has no impact on the ``EXCLUSION_BY_RESOURCE_TYPES`` recording strategy. This means that the global IAM resource types ( IAM users, groups, roles, and customer managed policies) will not be automatically added as exclusions for ``ExclusionByResourceTypes`` when ``IncludeGlobalResourceTypes`` is set to ``false`` .

               The ``IncludeGlobalResourceTypes`` field should only be used to modify the ``AllSupported`` field, as the default for the ``AllSupported`` field is to record configuration changes for all supported resource types excluding the global IAM resource types. To include the global IAM resource types when ``AllSupported`` is set to ``true`` , make sure to set ``IncludeGlobalResourceTypes`` to ``true`` .

               To exclude the global IAM resource types for the ``EXCLUSION_BY_RESOURCE_TYPES`` recording strategy, you need to manually add them to the ``ResourceTypes`` field of ``ExclusionByResourceTypes`` . > *Required and optional fields*

               Before you set this field to ``true`` , set the ``AllSupported`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ to ``true`` . Optionally, you can set the ``useOnly`` field of `RecordingStrategy <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingStrategy.html>`_ to ``ALL_SUPPORTED_RESOURCE_TYPES`` . > *Overriding fields*

               If you set this field to ``false`` but list global IAM resource types in the ``ResourceTypes`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ , AWS Config will still record configuration changes for those specified resource types *regardless* of if you set the ``IncludeGlobalResourceTypes`` field to false.

               If you do not want to record configuration changes to the global IAM resource types (IAM users, groups, roles, and customer managed policies), make sure to not list them in the ``ResourceTypes`` field in addition to setting the ``IncludeGlobalResourceTypes`` field to false.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordinggroup.html#cfn-config-configurationrecorder-recordinggroup-includeglobalresourcetypes
            '''
            result = self._values.get("include_global_resource_types")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def recording_strategy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationRecorderPropsMixin.RecordingStrategyProperty"]]:
            '''An object that specifies the recording strategy for the configuration recorder.

            - If you set the ``useOnly`` field of `RecordingStrategy <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingStrategy.html>`_ to ``ALL_SUPPORTED_RESOURCE_TYPES`` , AWS Config records configuration changes for all supported resource types, excluding the global IAM resource types. You also must set the ``AllSupported`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ to ``true`` . When AWS Config adds support for a new resource type, AWS Config automatically starts recording resources of that type.
            - If you set the ``useOnly`` field of `RecordingStrategy <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingStrategy.html>`_ to ``INCLUSION_BY_RESOURCE_TYPES`` , AWS Config records configuration changes for only the resource types you specify in the ``ResourceTypes`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ .
            - If you set the ``useOnly`` field of `RecordingStrategy <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingStrategy.html>`_ to ``EXCLUSION_BY_RESOURCE_TYPES`` , AWS Config records configuration changes for all supported resource types except the resource types that you specify to exclude from being recorded in the ``ResourceTypes`` field of `ExclusionByResourceTypes <https://docs.aws.amazon.com/config/latest/APIReference/API_ExclusionByResourceTypes.html>`_ .

            .. epigraph::

               *Required and optional fields*

               The ``recordingStrategy`` field is optional when you set the ``AllSupported`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ to ``true`` .

               The ``recordingStrategy`` field is optional when you list resource types in the ``ResourceTypes`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ .

               The ``recordingStrategy`` field is required if you list resource types to exclude from recording in the ``ResourceTypes`` field of `ExclusionByResourceTypes <https://docs.aws.amazon.com/config/latest/APIReference/API_ExclusionByResourceTypes.html>`_ . > *Overriding fields*

               If you choose ``EXCLUSION_BY_RESOURCE_TYPES`` for the recording strategy, the ``ExclusionByResourceTypes`` field will override other properties in the request.

               For example, even if you set ``IncludeGlobalResourceTypes`` to false, global IAM resource types will still be automatically recorded in this option unless those resource types are specifically listed as exclusions in the ``ResourceTypes`` field of ``ExclusionByResourceTypes`` . > *Global resources types and the resource exclusion recording strategy*

               By default, if you choose the ``EXCLUSION_BY_RESOURCE_TYPES`` recording strategy, when AWS Config adds support for a new resource type in the Region where you set up the configuration recorder, including global resource types, AWS Config starts recording resources of that type automatically.

               Unless specifically listed as exclusions, ``AWS::RDS::GlobalCluster`` will be recorded automatically in all supported AWS Config Regions were the configuration recorder is enabled.

               IAM users, groups, roles, and customer managed policies will be recorded in the Region where you set up the configuration recorder if that is a Region where AWS Config was available before February 2022. You cannot be record the global IAM resouce types in Regions supported by AWS Config after February 2022. This list where you cannot record the global IAM resource types includes the following Regions:

               - Asia Pacific (Hyderabad)
               - Asia Pacific (Melbourne)
               - Canada West (Calgary)
               - Europe (Spain)
               - Europe (Zurich)
               - Israel (Tel Aviv)
               - Middle East (UAE)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordinggroup.html#cfn-config-configurationrecorder-recordinggroup-recordingstrategy
            '''
            result = self._values.get("recording_strategy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationRecorderPropsMixin.RecordingStrategyProperty"]], result)

        @builtins.property
        def resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A comma-separated list that specifies which resource types AWS Config records.

            For a list of valid ``ResourceTypes`` values, see the *Resource Type Value* column in `Supported AWS resource Types <https://docs.aws.amazon.com/config/latest/developerguide/resource-config-reference.html#supported-resources>`_ in the *AWS Config developer guide* .
            .. epigraph::

               *Required and optional fields*

               Optionally, you can set the ``useOnly`` field of `RecordingStrategy <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingStrategy.html>`_ to ``INCLUSION_BY_RESOURCE_TYPES`` .

               To record all configuration changes, set the ``AllSupported`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ to ``true`` , and either omit this field or don't specify any resource types in this field. If you set the ``AllSupported`` field to ``false`` and specify values for ``ResourceTypes`` , when AWS Config adds support for a new type of resource, it will not record resources of that type unless you manually add that type to your recording group. > *Region availability*

               Before specifying a resource type for AWS Config to track, check `Resource Coverage by Region Availability <https://docs.aws.amazon.com/config/latest/developerguide/what-is-resource-config-coverage.html>`_ to see if the resource type is supported in the AWS Region where you set up AWS Config . If a resource type is supported by AWS Config in at least one Region, you can enable the recording of that resource type in all Regions supported by AWS Config , even if the specified resource type is not supported in the AWS Region where you set up AWS Config .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordinggroup.html#cfn-config-configurationrecorder-recordinggroup-resourcetypes
            '''
            result = self._values.get("resource_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordingGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConfigurationRecorderPropsMixin.RecordingModeOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "recording_frequency": "recordingFrequency",
            "resource_types": "resourceTypes",
        },
    )
    class RecordingModeOverrideProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            recording_frequency: typing.Optional[builtins.str] = None,
            resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''An object for you to specify your overrides for the recording mode.

            :param description: A description that you provide for the override.
            :param recording_frequency: The recording frequency that will be applied to all the resource types specified in the override. - Continuous recording allows you to record configuration changes continuously whenever a change occurs. - Daily recording allows you to receive a configuration item (CI) representing the most recent state of your resources over the last 24-hour period, only if it’s different from the previous CI recorded. .. epigraph:: AWS Firewall Manager depends on continuous recording to monitor your resources. If you are using Firewall Manager, it is recommended that you set the recording frequency to Continuous.
            :param resource_types: A comma-separated list that specifies which resource types AWS Config includes in the override. .. epigraph:: Daily recording cannot be specified for the following resource types: - ``AWS::Config::ResourceCompliance`` - ``AWS::Config::ConformancePackCompliance`` - ``AWS::Config::ConfigurationRecorder``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordingmodeoverride.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                recording_mode_override_property = config_mixins.CfnConfigurationRecorderPropsMixin.RecordingModeOverrideProperty(
                    description="description",
                    recording_frequency="recordingFrequency",
                    resource_types=["resourceTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__48dee59e25d6cebe211fa945acbfacb206a8f0f97b7c124bbd35039b444ec561)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument recording_frequency", value=recording_frequency, expected_type=type_hints["recording_frequency"])
                check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if recording_frequency is not None:
                self._values["recording_frequency"] = recording_frequency
            if resource_types is not None:
                self._values["resource_types"] = resource_types

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description that you provide for the override.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordingmodeoverride.html#cfn-config-configurationrecorder-recordingmodeoverride-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def recording_frequency(self) -> typing.Optional[builtins.str]:
            '''The recording frequency that will be applied to all the resource types specified in the override.

            - Continuous recording allows you to record configuration changes continuously whenever a change occurs.
            - Daily recording allows you to receive a configuration item (CI) representing the most recent state of your resources over the last 24-hour period, only if it’s different from the previous CI recorded.

            .. epigraph::

               AWS Firewall Manager depends on continuous recording to monitor your resources. If you are using Firewall Manager, it is recommended that you set the recording frequency to Continuous.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordingmodeoverride.html#cfn-config-configurationrecorder-recordingmodeoverride-recordingfrequency
            '''
            result = self._values.get("recording_frequency")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A comma-separated list that specifies which resource types AWS Config includes in the override.

            .. epigraph::

               Daily recording cannot be specified for the following resource types:

               - ``AWS::Config::ResourceCompliance``
               - ``AWS::Config::ConformancePackCompliance``
               - ``AWS::Config::ConfigurationRecorder``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordingmodeoverride.html#cfn-config-configurationrecorder-recordingmodeoverride-resourcetypes
            '''
            result = self._values.get("resource_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordingModeOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConfigurationRecorderPropsMixin.RecordingModeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "recording_frequency": "recordingFrequency",
            "recording_mode_overrides": "recordingModeOverrides",
        },
    )
    class RecordingModeProperty:
        def __init__(
            self,
            *,
            recording_frequency: typing.Optional[builtins.str] = None,
            recording_mode_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationRecorderPropsMixin.RecordingModeOverrideProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies the default recording frequency that AWS Config uses to record configuration changes.

            AWS Config supports *Continuous recording* and *Daily recording* .

            - Continuous recording allows you to record configuration changes continuously whenever a change occurs.
            - Daily recording allows you to receive a configuration item (CI) representing the most recent state of your resources over the last 24-hour period, only if it’s different from the previous CI recorded.

            .. epigraph::

               AWS Firewall Manager depends on continuous recording to monitor your resources. If you are using Firewall Manager, it is recommended that you set the recording frequency to Continuous.

            You can also override the recording frequency for specific resource types.

            :param recording_frequency: The default recording frequency that AWS Config uses to record configuration changes. .. epigraph:: Daily recording cannot be specified for the following resource types: - ``AWS::Config::ResourceCompliance`` - ``AWS::Config::ConformancePackCompliance`` - ``AWS::Config::ConfigurationRecorder`` For the *allSupported* ( ``ALL_SUPPORTED_RESOURCE_TYPES`` ) recording strategy, these resource types will be set to Continuous recording.
            :param recording_mode_overrides: An array of ``recordingModeOverride`` objects for you to specify your overrides for the recording mode. The ``recordingModeOverride`` object in the ``recordingModeOverrides`` array consists of three fields: a ``description`` , the new ``recordingFrequency`` , and an array of ``resourceTypes`` to override.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordingmode.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                recording_mode_property = config_mixins.CfnConfigurationRecorderPropsMixin.RecordingModeProperty(
                    recording_frequency="recordingFrequency",
                    recording_mode_overrides=[config_mixins.CfnConfigurationRecorderPropsMixin.RecordingModeOverrideProperty(
                        description="description",
                        recording_frequency="recordingFrequency",
                        resource_types=["resourceTypes"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f007638a2c68499f55be10916c861d32d1245b5d680986dd54bb03250f9ddc7e)
                check_type(argname="argument recording_frequency", value=recording_frequency, expected_type=type_hints["recording_frequency"])
                check_type(argname="argument recording_mode_overrides", value=recording_mode_overrides, expected_type=type_hints["recording_mode_overrides"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if recording_frequency is not None:
                self._values["recording_frequency"] = recording_frequency
            if recording_mode_overrides is not None:
                self._values["recording_mode_overrides"] = recording_mode_overrides

        @builtins.property
        def recording_frequency(self) -> typing.Optional[builtins.str]:
            '''The default recording frequency that AWS Config uses to record configuration changes.

            .. epigraph::

               Daily recording cannot be specified for the following resource types:

               - ``AWS::Config::ResourceCompliance``
               - ``AWS::Config::ConformancePackCompliance``
               - ``AWS::Config::ConfigurationRecorder``

               For the *allSupported* ( ``ALL_SUPPORTED_RESOURCE_TYPES`` ) recording strategy, these resource types will be set to Continuous recording.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordingmode.html#cfn-config-configurationrecorder-recordingmode-recordingfrequency
            '''
            result = self._values.get("recording_frequency")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def recording_mode_overrides(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationRecorderPropsMixin.RecordingModeOverrideProperty"]]]]:
            '''An array of ``recordingModeOverride`` objects for you to specify your overrides for the recording mode.

            The ``recordingModeOverride`` object in the ``recordingModeOverrides`` array consists of three fields: a ``description`` , the new ``recordingFrequency`` , and an array of ``resourceTypes`` to override.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordingmode.html#cfn-config-configurationrecorder-recordingmode-recordingmodeoverrides
            '''
            result = self._values.get("recording_mode_overrides")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationRecorderPropsMixin.RecordingModeOverrideProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordingModeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConfigurationRecorderPropsMixin.RecordingStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={"use_only": "useOnly"},
    )
    class RecordingStrategyProperty:
        def __init__(self, *, use_only: typing.Optional[builtins.str] = None) -> None:
            '''Specifies the recording strategy of the configuration recorder.

            Valid values include: ``ALL_SUPPORTED_RESOURCE_TYPES`` , ``INCLUSION_BY_RESOURCE_TYPES`` , and ``EXCLUSION_BY_RESOURCE_TYPES`` .

            :param use_only: The recording strategy for the configuration recorder. - If you set this option to ``ALL_SUPPORTED_RESOURCE_TYPES`` , AWS Config records configuration changes for all supported resource types, excluding the global IAM resource types. You also must set the ``AllSupported`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ to ``true`` . When AWS Config adds support for a new resource type, AWS Config automatically starts recording resources of that type. For a list of supported resource types, see `Supported Resource Types <https://docs.aws.amazon.com/config/latest/developerguide/resource-config-reference.html#supported-resources>`_ in the *AWS Config developer guide* . - If you set this option to ``INCLUSION_BY_RESOURCE_TYPES`` , AWS Config records configuration changes for only the resource types that you specify in the ``ResourceTypes`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ . - If you set this option to ``EXCLUSION_BY_RESOURCE_TYPES`` , AWS Config records configuration changes for all supported resource types, except the resource types that you specify to exclude from being recorded in the ``ResourceTypes`` field of `ExclusionByResourceTypes <https://docs.aws.amazon.com/config/latest/APIReference/API_ExclusionByResourceTypes.html>`_ . .. epigraph:: *Required and optional fields* The ``recordingStrategy`` field is optional when you set the ``AllSupported`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ to ``true`` . The ``recordingStrategy`` field is optional when you list resource types in the ``ResourceTypes`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ . The ``recordingStrategy`` field is required if you list resource types to exclude from recording in the ``ResourceTypes`` field of `ExclusionByResourceTypes <https://docs.aws.amazon.com/config/latest/APIReference/API_ExclusionByResourceTypes.html>`_ . > *Overriding fields* If you choose ``EXCLUSION_BY_RESOURCE_TYPES`` for the recording strategy, the ``ExclusionByResourceTypes`` field will override other properties in the request. For example, even if you set ``IncludeGlobalResourceTypes`` to false, global IAM resource types will still be automatically recorded in this option unless those resource types are specifically listed as exclusions in the ``ResourceTypes`` field of ``ExclusionByResourceTypes`` . > *Global resource types and the exclusion recording strategy* By default, if you choose the ``EXCLUSION_BY_RESOURCE_TYPES`` recording strategy, when AWS Config adds support for a new resource type in the Region where you set up the configuration recorder, including global resource types, AWS Config starts recording resources of that type automatically. Unless specifically listed as exclusions, ``AWS::RDS::GlobalCluster`` will be recorded automatically in all supported AWS Config Regions were the configuration recorder is enabled. IAM users, groups, roles, and customer managed policies will be recorded in the Region where you set up the configuration recorder if that is a Region where AWS Config was available before February 2022. You cannot be record the global IAM resouce types in Regions supported by AWS Config after February 2022. This list where you cannot record the global IAM resource types includes the following Regions: - Asia Pacific (Hyderabad) - Asia Pacific (Melbourne) - Canada West (Calgary) - Europe (Spain) - Europe (Zurich) - Israel (Tel Aviv) - Middle East (UAE)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordingstrategy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                recording_strategy_property = config_mixins.CfnConfigurationRecorderPropsMixin.RecordingStrategyProperty(
                    use_only="useOnly"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f96de9412d46cc852fa90db63fe9fc49a2c0fde09029fef0e195e3dd3caec1b5)
                check_type(argname="argument use_only", value=use_only, expected_type=type_hints["use_only"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if use_only is not None:
                self._values["use_only"] = use_only

        @builtins.property
        def use_only(self) -> typing.Optional[builtins.str]:
            '''The recording strategy for the configuration recorder.

            - If you set this option to ``ALL_SUPPORTED_RESOURCE_TYPES`` , AWS Config records configuration changes for all supported resource types, excluding the global IAM resource types. You also must set the ``AllSupported`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ to ``true`` . When AWS Config adds support for a new resource type, AWS Config automatically starts recording resources of that type. For a list of supported resource types, see `Supported Resource Types <https://docs.aws.amazon.com/config/latest/developerguide/resource-config-reference.html#supported-resources>`_ in the *AWS Config developer guide* .
            - If you set this option to ``INCLUSION_BY_RESOURCE_TYPES`` , AWS Config records configuration changes for only the resource types that you specify in the ``ResourceTypes`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ .
            - If you set this option to ``EXCLUSION_BY_RESOURCE_TYPES`` , AWS Config records configuration changes for all supported resource types, except the resource types that you specify to exclude from being recorded in the ``ResourceTypes`` field of `ExclusionByResourceTypes <https://docs.aws.amazon.com/config/latest/APIReference/API_ExclusionByResourceTypes.html>`_ .

            .. epigraph::

               *Required and optional fields*

               The ``recordingStrategy`` field is optional when you set the ``AllSupported`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ to ``true`` .

               The ``recordingStrategy`` field is optional when you list resource types in the ``ResourceTypes`` field of `RecordingGroup <https://docs.aws.amazon.com/config/latest/APIReference/API_RecordingGroup.html>`_ .

               The ``recordingStrategy`` field is required if you list resource types to exclude from recording in the ``ResourceTypes`` field of `ExclusionByResourceTypes <https://docs.aws.amazon.com/config/latest/APIReference/API_ExclusionByResourceTypes.html>`_ . > *Overriding fields*

               If you choose ``EXCLUSION_BY_RESOURCE_TYPES`` for the recording strategy, the ``ExclusionByResourceTypes`` field will override other properties in the request.

               For example, even if you set ``IncludeGlobalResourceTypes`` to false, global IAM resource types will still be automatically recorded in this option unless those resource types are specifically listed as exclusions in the ``ResourceTypes`` field of ``ExclusionByResourceTypes`` . > *Global resource types and the exclusion recording strategy*

               By default, if you choose the ``EXCLUSION_BY_RESOURCE_TYPES`` recording strategy, when AWS Config adds support for a new resource type in the Region where you set up the configuration recorder, including global resource types, AWS Config starts recording resources of that type automatically.

               Unless specifically listed as exclusions, ``AWS::RDS::GlobalCluster`` will be recorded automatically in all supported AWS Config Regions were the configuration recorder is enabled.

               IAM users, groups, roles, and customer managed policies will be recorded in the Region where you set up the configuration recorder if that is a Region where AWS Config was available before February 2022. You cannot be record the global IAM resouce types in Regions supported by AWS Config after February 2022. This list where you cannot record the global IAM resource types includes the following Regions:

               - Asia Pacific (Hyderabad)
               - Asia Pacific (Melbourne)
               - Canada West (Calgary)
               - Europe (Spain)
               - Europe (Zurich)
               - Israel (Tel Aviv)
               - Middle East (UAE)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordingstrategy.html#cfn-config-configurationrecorder-recordingstrategy-useonly
            '''
            result = self._values.get("use_only")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordingStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConformancePackMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "conformance_pack_input_parameters": "conformancePackInputParameters",
        "conformance_pack_name": "conformancePackName",
        "delivery_s3_bucket": "deliveryS3Bucket",
        "delivery_s3_key_prefix": "deliveryS3KeyPrefix",
        "template_body": "templateBody",
        "template_s3_uri": "templateS3Uri",
        "template_ssm_document_details": "templateSsmDocumentDetails",
    },
)
class CfnConformancePackMixinProps:
    def __init__(
        self,
        *,
        conformance_pack_input_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConformancePackPropsMixin.ConformancePackInputParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        conformance_pack_name: typing.Optional[builtins.str] = None,
        delivery_s3_bucket: typing.Optional[builtins.str] = None,
        delivery_s3_key_prefix: typing.Optional[builtins.str] = None,
        template_body: typing.Optional[builtins.str] = None,
        template_s3_uri: typing.Optional[builtins.str] = None,
        template_ssm_document_details: typing.Any = None,
    ) -> None:
        '''Properties for CfnConformancePackPropsMixin.

        :param conformance_pack_input_parameters: A list of ConformancePackInputParameter objects.
        :param conformance_pack_name: Name of the conformance pack you want to create.
        :param delivery_s3_bucket: The name of the Amazon S3 bucket where AWS Config stores conformance pack templates.
        :param delivery_s3_key_prefix: The prefix for the Amazon S3 bucket.
        :param template_body: A string containing full conformance pack template body. Structure containing the template body with a minimum length of 1 byte and a maximum length of 51,200 bytes. .. epigraph:: You can only use a YAML template with two resource types: config rule ( ``AWS::Config::ConfigRule`` ) and a remediation action ( ``AWS::Config::RemediationConfiguration`` ).
        :param template_s3_uri: Location of file containing the template body (s3://bucketname/prefix). The uri must point to the conformance pack template (max size: 300 KB) that is located in an Amazon S3 bucket. .. epigraph:: You must have access to read Amazon S3 bucket.
        :param template_ssm_document_details: An object that contains the name or Amazon Resource Name (ARN) of the AWS Systems Manager document (SSM document) and the version of the SSM document that is used to create a conformance pack.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
            
            # template_ssm_document_details: Any
            
            cfn_conformance_pack_mixin_props = config_mixins.CfnConformancePackMixinProps(
                conformance_pack_input_parameters=[config_mixins.CfnConformancePackPropsMixin.ConformancePackInputParameterProperty(
                    parameter_name="parameterName",
                    parameter_value="parameterValue"
                )],
                conformance_pack_name="conformancePackName",
                delivery_s3_bucket="deliveryS3Bucket",
                delivery_s3_key_prefix="deliveryS3KeyPrefix",
                template_body="templateBody",
                template_s3_uri="templateS3Uri",
                template_ssm_document_details=template_ssm_document_details
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fb9f6ef9d5eecaa89815597a470365902805bc9c6432fcd44a3e508d0d37112)
            check_type(argname="argument conformance_pack_input_parameters", value=conformance_pack_input_parameters, expected_type=type_hints["conformance_pack_input_parameters"])
            check_type(argname="argument conformance_pack_name", value=conformance_pack_name, expected_type=type_hints["conformance_pack_name"])
            check_type(argname="argument delivery_s3_bucket", value=delivery_s3_bucket, expected_type=type_hints["delivery_s3_bucket"])
            check_type(argname="argument delivery_s3_key_prefix", value=delivery_s3_key_prefix, expected_type=type_hints["delivery_s3_key_prefix"])
            check_type(argname="argument template_body", value=template_body, expected_type=type_hints["template_body"])
            check_type(argname="argument template_s3_uri", value=template_s3_uri, expected_type=type_hints["template_s3_uri"])
            check_type(argname="argument template_ssm_document_details", value=template_ssm_document_details, expected_type=type_hints["template_ssm_document_details"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if conformance_pack_input_parameters is not None:
            self._values["conformance_pack_input_parameters"] = conformance_pack_input_parameters
        if conformance_pack_name is not None:
            self._values["conformance_pack_name"] = conformance_pack_name
        if delivery_s3_bucket is not None:
            self._values["delivery_s3_bucket"] = delivery_s3_bucket
        if delivery_s3_key_prefix is not None:
            self._values["delivery_s3_key_prefix"] = delivery_s3_key_prefix
        if template_body is not None:
            self._values["template_body"] = template_body
        if template_s3_uri is not None:
            self._values["template_s3_uri"] = template_s3_uri
        if template_ssm_document_details is not None:
            self._values["template_ssm_document_details"] = template_ssm_document_details

    @builtins.property
    def conformance_pack_input_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConformancePackPropsMixin.ConformancePackInputParameterProperty"]]]]:
        '''A list of ConformancePackInputParameter objects.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html#cfn-config-conformancepack-conformancepackinputparameters
        '''
        result = self._values.get("conformance_pack_input_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConformancePackPropsMixin.ConformancePackInputParameterProperty"]]]], result)

    @builtins.property
    def conformance_pack_name(self) -> typing.Optional[builtins.str]:
        '''Name of the conformance pack you want to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html#cfn-config-conformancepack-conformancepackname
        '''
        result = self._values.get("conformance_pack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delivery_s3_bucket(self) -> typing.Optional[builtins.str]:
        '''The name of the Amazon S3 bucket where AWS Config stores conformance pack templates.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html#cfn-config-conformancepack-deliverys3bucket
        '''
        result = self._values.get("delivery_s3_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delivery_s3_key_prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix for the Amazon S3 bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html#cfn-config-conformancepack-deliverys3keyprefix
        '''
        result = self._values.get("delivery_s3_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_body(self) -> typing.Optional[builtins.str]:
        '''A string containing full conformance pack template body.

        Structure containing the template body with a minimum length of 1 byte and a maximum length of 51,200 bytes.
        .. epigraph::

           You can only use a YAML template with two resource types: config rule ( ``AWS::Config::ConfigRule`` ) and a remediation action ( ``AWS::Config::RemediationConfiguration`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html#cfn-config-conformancepack-templatebody
        '''
        result = self._values.get("template_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_s3_uri(self) -> typing.Optional[builtins.str]:
        '''Location of file containing the template body (s3://bucketname/prefix).

        The uri must point to the conformance pack template (max size: 300 KB) that is located in an Amazon S3 bucket.
        .. epigraph::

           You must have access to read Amazon S3 bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html#cfn-config-conformancepack-templates3uri
        '''
        result = self._values.get("template_s3_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_ssm_document_details(self) -> typing.Any:
        '''An object that contains the name or Amazon Resource Name (ARN) of the AWS Systems Manager document (SSM document) and the version of the SSM document that is used to create a conformance pack.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html#cfn-config-conformancepack-templatessmdocumentdetails
        '''
        result = self._values.get("template_ssm_document_details")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConformancePackMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConformancePackPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConformancePackPropsMixin",
):
    '''A conformance pack is a collection of AWS Config rules and remediation actions that can be easily deployed in an account and a region.

    ConformancePack creates a service linked role in your account. The service linked role is created only when the role does not exist in your account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html
    :cloudformationResource: AWS::Config::ConformancePack
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
        
        # template_ssm_document_details: Any
        
        cfn_conformance_pack_props_mixin = config_mixins.CfnConformancePackPropsMixin(config_mixins.CfnConformancePackMixinProps(
            conformance_pack_input_parameters=[config_mixins.CfnConformancePackPropsMixin.ConformancePackInputParameterProperty(
                parameter_name="parameterName",
                parameter_value="parameterValue"
            )],
            conformance_pack_name="conformancePackName",
            delivery_s3_bucket="deliveryS3Bucket",
            delivery_s3_key_prefix="deliveryS3KeyPrefix",
            template_body="templateBody",
            template_s3_uri="templateS3Uri",
            template_ssm_document_details=template_ssm_document_details
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnConformancePackMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Config::ConformancePack``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb044d7d257af531883568bc635254d9a8e7d80db77f425670a0bdc2f5ef3be4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f0a1ca960223c5b9794b247313cfc5beb253134a7ddc5076436060d31f6fc8d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd71e4f6459fea8599f040ecbc595b14b1ac9843d36144d762b170bbd3cd21c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConformancePackMixinProps:
        return typing.cast(CfnConformancePackMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConformancePackPropsMixin.ConformancePackInputParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameter_name": "parameterName",
            "parameter_value": "parameterValue",
        },
    )
    class ConformancePackInputParameterProperty:
        def __init__(
            self,
            *,
            parameter_name: typing.Optional[builtins.str] = None,
            parameter_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Input parameters in the form of key-value pairs for the conformance pack, both of which you define.

            Keys can have a maximum character length of 255 characters, and values can have a maximum length of 4096 characters.

            :param parameter_name: One part of a key-value pair.
            :param parameter_value: Another part of the key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-conformancepack-conformancepackinputparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                conformance_pack_input_parameter_property = config_mixins.CfnConformancePackPropsMixin.ConformancePackInputParameterProperty(
                    parameter_name="parameterName",
                    parameter_value="parameterValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fa1fc3d0b95b6aab3f3ecc407d8a4306a816e6d1b4516c9282ede4df458d335e)
                check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
                check_type(argname="argument parameter_value", value=parameter_value, expected_type=type_hints["parameter_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parameter_name is not None:
                self._values["parameter_name"] = parameter_name
            if parameter_value is not None:
                self._values["parameter_value"] = parameter_value

        @builtins.property
        def parameter_name(self) -> typing.Optional[builtins.str]:
            '''One part of a key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-conformancepack-conformancepackinputparameter.html#cfn-config-conformancepack-conformancepackinputparameter-parametername
            '''
            result = self._values.get("parameter_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameter_value(self) -> typing.Optional[builtins.str]:
            '''Another part of the key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-conformancepack-conformancepackinputparameter.html#cfn-config-conformancepack-conformancepackinputparameter-parametervalue
            '''
            result = self._values.get("parameter_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConformancePackInputParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnConformancePackPropsMixin.TemplateSSMDocumentDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "document_name": "documentName",
            "document_version": "documentVersion",
        },
    )
    class TemplateSSMDocumentDetailsProperty:
        def __init__(
            self,
            *,
            document_name: typing.Optional[builtins.str] = None,
            document_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This API allows you to create a conformance pack template with an AWS Systems Manager document (SSM document).

            To deploy a conformance pack using an SSM document, first create an SSM document with conformance pack content, and then provide the ``DocumentName`` in the `PutConformancePack API <https://docs.aws.amazon.com/config/latest/APIReference/API_PutConformancePack.html>`_ . You can also provide the ``DocumentVersion`` .

            The ``TemplateSSMDocumentDetails`` object contains the name of the SSM document and the version of the SSM document.

            :param document_name: The name or Amazon Resource Name (ARN) of the SSM document to use to create a conformance pack. If you use the document name, AWS Config checks only your account and AWS Region for the SSM document.
            :param document_version: The version of the SSM document to use to create a conformance pack. By default, AWS Config uses the latest version. .. epigraph:: This field is optional.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-conformancepack-templatessmdocumentdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                template_sSMDocument_details_property = config_mixins.CfnConformancePackPropsMixin.TemplateSSMDocumentDetailsProperty(
                    document_name="documentName",
                    document_version="documentVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1c3885c83ef78db2a39d791a66e7c9597c947cdb179b1a076c739bb106741f4b)
                check_type(argname="argument document_name", value=document_name, expected_type=type_hints["document_name"])
                check_type(argname="argument document_version", value=document_version, expected_type=type_hints["document_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if document_name is not None:
                self._values["document_name"] = document_name
            if document_version is not None:
                self._values["document_version"] = document_version

        @builtins.property
        def document_name(self) -> typing.Optional[builtins.str]:
            '''The name or Amazon Resource Name (ARN) of the SSM document to use to create a conformance pack.

            If you use the document name, AWS Config checks only your account and AWS Region for the SSM document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-conformancepack-templatessmdocumentdetails.html#cfn-config-conformancepack-templatessmdocumentdetails-documentname
            '''
            result = self._values.get("document_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def document_version(self) -> typing.Optional[builtins.str]:
            '''The version of the SSM document to use to create a conformance pack.

            By default, AWS Config uses the latest version.
            .. epigraph::

               This field is optional.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-conformancepack-templatessmdocumentdetails.html#cfn-config-conformancepack-templatessmdocumentdetails-documentversion
            '''
            result = self._values.get("document_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TemplateSSMDocumentDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnDeliveryChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "config_snapshot_delivery_properties": "configSnapshotDeliveryProperties",
        "name": "name",
        "s3_bucket_name": "s3BucketName",
        "s3_key_prefix": "s3KeyPrefix",
        "s3_kms_key_arn": "s3KmsKeyArn",
        "sns_topic_arn": "snsTopicArn",
    },
)
class CfnDeliveryChannelMixinProps:
    def __init__(
        self,
        *,
        config_snapshot_delivery_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryChannelPropsMixin.ConfigSnapshotDeliveryPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        s3_bucket_name: typing.Optional[builtins.str] = None,
        s3_key_prefix: typing.Optional[builtins.str] = None,
        s3_kms_key_arn: typing.Optional[builtins.str] = None,
        sns_topic_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDeliveryChannelPropsMixin.

        :param config_snapshot_delivery_properties: The options for how often AWS Config delivers configuration snapshots to the Amazon S3 bucket.
        :param name: A name for the delivery channel. If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the delivery channel name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . Updates are not supported. To change the name, you must run two separate updates. In the first update, delete this resource, and then recreate it with a new name in the second update.
        :param s3_bucket_name: The name of the Amazon S3 bucket to which AWS Config delivers configuration snapshots and configuration history files. If you specify a bucket that belongs to another AWS account , that bucket must have policies that grant access permissions to AWS Config . For more information, see `Permissions for the Amazon S3 Bucket <https://docs.aws.amazon.com/config/latest/developerguide/s3-bucket-policy.html>`_ in the *AWS Config Developer Guide* .
        :param s3_key_prefix: The prefix for the specified Amazon S3 bucket.
        :param s3_kms_key_arn: The Amazon Resource Name (ARN) of the AWS Key Management Service ( AWS ) AWS KMS key (KMS key) used to encrypt objects delivered by AWS Config . Must belong to the same Region as the destination S3 bucket.
        :param sns_topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic to which AWS Config sends notifications about configuration changes. If you choose a topic from another account, the topic must have policies that grant access permissions to AWS Config . For more information, see `Permissions for the Amazon SNS Topic <https://docs.aws.amazon.com/config/latest/developerguide/sns-topic-policy.html>`_ in the *AWS Config Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
            
            cfn_delivery_channel_mixin_props = config_mixins.CfnDeliveryChannelMixinProps(
                config_snapshot_delivery_properties=config_mixins.CfnDeliveryChannelPropsMixin.ConfigSnapshotDeliveryPropertiesProperty(
                    delivery_frequency="deliveryFrequency"
                ),
                name="name",
                s3_bucket_name="s3BucketName",
                s3_key_prefix="s3KeyPrefix",
                s3_kms_key_arn="s3KmsKeyArn",
                sns_topic_arn="snsTopicArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee83557e421fe53984a72b9f220e86b12e480c8e317c2c9fda593d85e691a95)
            check_type(argname="argument config_snapshot_delivery_properties", value=config_snapshot_delivery_properties, expected_type=type_hints["config_snapshot_delivery_properties"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
            check_type(argname="argument s3_key_prefix", value=s3_key_prefix, expected_type=type_hints["s3_key_prefix"])
            check_type(argname="argument s3_kms_key_arn", value=s3_kms_key_arn, expected_type=type_hints["s3_kms_key_arn"])
            check_type(argname="argument sns_topic_arn", value=sns_topic_arn, expected_type=type_hints["sns_topic_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config_snapshot_delivery_properties is not None:
            self._values["config_snapshot_delivery_properties"] = config_snapshot_delivery_properties
        if name is not None:
            self._values["name"] = name
        if s3_bucket_name is not None:
            self._values["s3_bucket_name"] = s3_bucket_name
        if s3_key_prefix is not None:
            self._values["s3_key_prefix"] = s3_key_prefix
        if s3_kms_key_arn is not None:
            self._values["s3_kms_key_arn"] = s3_kms_key_arn
        if sns_topic_arn is not None:
            self._values["sns_topic_arn"] = sns_topic_arn

    @builtins.property
    def config_snapshot_delivery_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryChannelPropsMixin.ConfigSnapshotDeliveryPropertiesProperty"]]:
        '''The options for how often AWS Config delivers configuration snapshots to the Amazon S3 bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-configsnapshotdeliveryproperties
        '''
        result = self._values.get("config_snapshot_delivery_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryChannelPropsMixin.ConfigSnapshotDeliveryPropertiesProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the delivery channel.

        If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the delivery channel name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .

        Updates are not supported. To change the name, you must run two separate updates. In the first update, delete this resource, and then recreate it with a new name in the second update.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_bucket_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Amazon S3 bucket to which AWS Config delivers configuration snapshots and configuration history files.

        If you specify a bucket that belongs to another AWS account , that bucket must have policies that grant access permissions to AWS Config . For more information, see `Permissions for the Amazon S3 Bucket <https://docs.aws.amazon.com/config/latest/developerguide/s3-bucket-policy.html>`_ in the *AWS Config Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-s3bucketname
        '''
        result = self._values.get("s3_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_key_prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix for the specified Amazon S3 bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-s3keyprefix
        '''
        result = self._values.get("s3_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS Key Management Service ( AWS  ) AWS KMS key (KMS key) used to encrypt objects delivered by AWS Config .

        Must belong to the same Region as the destination S3 bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-s3kmskeyarn
        '''
        result = self._values.get("s3_kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sns_topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon SNS topic to which AWS Config sends notifications about configuration changes.

        If you choose a topic from another account, the topic must have policies that grant access permissions to AWS Config . For more information, see `Permissions for the Amazon SNS Topic <https://docs.aws.amazon.com/config/latest/developerguide/sns-topic-policy.html>`_ in the *AWS Config Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-snstopicarn
        '''
        result = self._values.get("sns_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeliveryChannelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDeliveryChannelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnDeliveryChannelPropsMixin",
):
    '''Specifies a delivery channel object to deliver configuration information to an Amazon S3 bucket and Amazon  topic.

    Before you can create a delivery channel, you must create a configuration recorder. You can use this action to change the Amazon S3 bucket or an Amazon  topic of the existing delivery channel. To change the Amazon S3 bucket or an Amazon  topic, call this action and specify the changed values for the S3 bucket and the SNS topic. If you specify a different value for either the S3 bucket or the SNS topic, this action will keep the existing value for the parameter that is not changed.
    .. epigraph::

       In the China (Beijing) Region, when you call this action, the Amazon S3 bucket must also be in the China (Beijing) Region. In all the other regions, AWS Config supports cross-region and cross-account delivery channels.

    You can have only one delivery channel per region per AWS account, and the delivery channel is required to use AWS Config .
    .. epigraph::

       AWS Config does not support the delivery channel to an Amazon S3 bucket bucket where object lock is enabled. For more information, see `How S3 Object Lock works <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-overview.html>`_ .

    When you create the delivery channel, you can specify; how often AWS Config delivers configuration snapshots to your Amazon S3 bucket (for example, 24 hours), the S3 bucket to which AWS Config sends configuration snapshots and configuration history files, and the Amazon  topic to which AWS Config sends notifications about configuration changes, such as updated resources, AWS Config rule evaluations, and when AWS Config delivers the configuration snapshot to your S3 bucket. For more information, see `Deliver Configuration Items <https://docs.aws.amazon.com/config/latest/developerguide/how-does-config-work.html#delivery-channel>`_ in the AWS Config Developer Guide.
    .. epigraph::

       To enable AWS Config , you must create a configuration recorder and a delivery channel. If you want to create the resources separately, you must create a configuration recorder before you can create a delivery channel. AWS Config uses the configuration recorder to capture configuration changes to your resources. For more information, see `AWS::Config::ConfigurationRecorder <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html>`_ .

    For more information, see `Managing the Delivery Channel <https://docs.aws.amazon.com/config/latest/developerguide/manage-delivery-channel.html>`_ in the AWS Config Developer Guide.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html
    :cloudformationResource: AWS::Config::DeliveryChannel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
        
        cfn_delivery_channel_props_mixin = config_mixins.CfnDeliveryChannelPropsMixin(config_mixins.CfnDeliveryChannelMixinProps(
            config_snapshot_delivery_properties=config_mixins.CfnDeliveryChannelPropsMixin.ConfigSnapshotDeliveryPropertiesProperty(
                delivery_frequency="deliveryFrequency"
            ),
            name="name",
            s3_bucket_name="s3BucketName",
            s3_key_prefix="s3KeyPrefix",
            s3_kms_key_arn="s3KmsKeyArn",
            sns_topic_arn="snsTopicArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDeliveryChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Config::DeliveryChannel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a97a1539b5f2f5775063a4bbad348812127bb15baf1f394f189efaa3e700e01b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8414b09aa63d890b109dd74c7a521710af612ae905b6d0044aef322d3d915644)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b96aac7dffa5fe7ebb2a721eba0ef11280402ee07c543566e5e88f457712b0f2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDeliveryChannelMixinProps:
        return typing.cast(CfnDeliveryChannelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnDeliveryChannelPropsMixin.ConfigSnapshotDeliveryPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"delivery_frequency": "deliveryFrequency"},
    )
    class ConfigSnapshotDeliveryPropertiesProperty:
        def __init__(
            self,
            *,
            delivery_frequency: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides options for how often AWS Config delivers configuration snapshots to the Amazon S3 bucket in your delivery channel.

            .. epigraph::

               If you want to create a rule that triggers evaluations for your resources when AWS Config delivers the configuration snapshot, see the following:

            The frequency for a rule that triggers evaluations for your resources when AWS Config delivers the configuration snapshot is set by one of two values, depending on which is less frequent:

            - The value for the ``deliveryFrequency`` parameter within the delivery channel configuration, which sets how often AWS Config delivers configuration snapshots. This value also sets how often AWS Config invokes evaluations for AWS Config rules.
            - The value for the ``MaximumExecutionFrequency`` parameter, which sets the maximum frequency with which AWS Config invokes evaluations for the rule. For more information, see `ConfigRule <https://docs.aws.amazon.com/config/latest/APIReference/API_ConfigRule.html>`_ .

            If the ``deliveryFrequency`` value is less frequent than the ``MaximumExecutionFrequency`` value for a rule, AWS Config invokes the rule only as often as the ``deliveryFrequency`` value.

            - For example, you want your rule to run evaluations when AWS Config delivers the configuration snapshot.
            - You specify the ``MaximumExecutionFrequency`` value for ``Six_Hours`` .
            - You then specify the delivery channel ``deliveryFrequency`` value for ``TwentyFour_Hours`` .
            - Because the value for ``deliveryFrequency`` is less frequent than ``MaximumExecutionFrequency`` , AWS Config invokes evaluations for the rule every 24 hours.

            You should set the ``MaximumExecutionFrequency`` value to be at least as frequent as the ``deliveryFrequency`` value. You can view the ``deliveryFrequency`` value by using the ``DescribeDeliveryChannnels`` action.

            To update the ``deliveryFrequency`` with which AWS Config delivers your configuration snapshots, use the ``PutDeliveryChannel`` action.

            :param delivery_frequency: The frequency with which AWS Config delivers configuration snapshots.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-deliverychannel-configsnapshotdeliveryproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                config_snapshot_delivery_properties_property = config_mixins.CfnDeliveryChannelPropsMixin.ConfigSnapshotDeliveryPropertiesProperty(
                    delivery_frequency="deliveryFrequency"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__63dd428f004388c1078c41d0dee2b39fbd9aa129b4ae9de897f1ed0577491e6d)
                check_type(argname="argument delivery_frequency", value=delivery_frequency, expected_type=type_hints["delivery_frequency"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delivery_frequency is not None:
                self._values["delivery_frequency"] = delivery_frequency

        @builtins.property
        def delivery_frequency(self) -> typing.Optional[builtins.str]:
            '''The frequency with which AWS Config delivers configuration snapshots.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-deliverychannel-configsnapshotdeliveryproperties.html#cfn-config-deliverychannel-configsnapshotdeliveryproperties-deliveryfrequency
            '''
            result = self._values.get("delivery_frequency")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigSnapshotDeliveryPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnOrganizationConfigRuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "excluded_accounts": "excludedAccounts",
        "organization_config_rule_name": "organizationConfigRuleName",
        "organization_custom_policy_rule_metadata": "organizationCustomPolicyRuleMetadata",
        "organization_custom_rule_metadata": "organizationCustomRuleMetadata",
        "organization_managed_rule_metadata": "organizationManagedRuleMetadata",
    },
)
class CfnOrganizationConfigRuleMixinProps:
    def __init__(
        self,
        *,
        excluded_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        organization_config_rule_name: typing.Optional[builtins.str] = None,
        organization_custom_policy_rule_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOrganizationConfigRulePropsMixin.OrganizationCustomPolicyRuleMetadataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        organization_custom_rule_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOrganizationConfigRulePropsMixin.OrganizationCustomRuleMetadataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        organization_managed_rule_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOrganizationConfigRulePropsMixin.OrganizationManagedRuleMetadataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnOrganizationConfigRulePropsMixin.

        :param excluded_accounts: A comma-separated list of accounts excluded from organization AWS Config rule.
        :param organization_config_rule_name: The name that you assign to organization AWS Config rule.
        :param organization_custom_policy_rule_metadata: An object that specifies metadata for your organization's AWS Config Custom Policy rule. The metadata includes the runtime system in use, which accounts have debug logging enabled, and other custom rule metadata, such as resource type, resource ID of AWS resource, and organization trigger types that initiate AWS Config to evaluate AWS resources against a rule.
        :param organization_custom_rule_metadata: An ``OrganizationCustomRuleMetadata`` object.
        :param organization_managed_rule_metadata: An ``OrganizationManagedRuleMetadata`` object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconfigrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
            
            cfn_organization_config_rule_mixin_props = config_mixins.CfnOrganizationConfigRuleMixinProps(
                excluded_accounts=["excludedAccounts"],
                organization_config_rule_name="organizationConfigRuleName",
                organization_custom_policy_rule_metadata=config_mixins.CfnOrganizationConfigRulePropsMixin.OrganizationCustomPolicyRuleMetadataProperty(
                    debug_log_delivery_accounts=["debugLogDeliveryAccounts"],
                    description="description",
                    input_parameters="inputParameters",
                    maximum_execution_frequency="maximumExecutionFrequency",
                    organization_config_rule_trigger_types=["organizationConfigRuleTriggerTypes"],
                    policy_text="policyText",
                    resource_id_scope="resourceIdScope",
                    resource_types_scope=["resourceTypesScope"],
                    runtime="runtime",
                    tag_key_scope="tagKeyScope",
                    tag_value_scope="tagValueScope"
                ),
                organization_custom_rule_metadata=config_mixins.CfnOrganizationConfigRulePropsMixin.OrganizationCustomRuleMetadataProperty(
                    description="description",
                    input_parameters="inputParameters",
                    lambda_function_arn="lambdaFunctionArn",
                    maximum_execution_frequency="maximumExecutionFrequency",
                    organization_config_rule_trigger_types=["organizationConfigRuleTriggerTypes"],
                    resource_id_scope="resourceIdScope",
                    resource_types_scope=["resourceTypesScope"],
                    tag_key_scope="tagKeyScope",
                    tag_value_scope="tagValueScope"
                ),
                organization_managed_rule_metadata=config_mixins.CfnOrganizationConfigRulePropsMixin.OrganizationManagedRuleMetadataProperty(
                    description="description",
                    input_parameters="inputParameters",
                    maximum_execution_frequency="maximumExecutionFrequency",
                    resource_id_scope="resourceIdScope",
                    resource_types_scope=["resourceTypesScope"],
                    rule_identifier="ruleIdentifier",
                    tag_key_scope="tagKeyScope",
                    tag_value_scope="tagValueScope"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f6a3761525560a19d757059100c12a59824a57d8036a27f27411a5143b3ccbf)
            check_type(argname="argument excluded_accounts", value=excluded_accounts, expected_type=type_hints["excluded_accounts"])
            check_type(argname="argument organization_config_rule_name", value=organization_config_rule_name, expected_type=type_hints["organization_config_rule_name"])
            check_type(argname="argument organization_custom_policy_rule_metadata", value=organization_custom_policy_rule_metadata, expected_type=type_hints["organization_custom_policy_rule_metadata"])
            check_type(argname="argument organization_custom_rule_metadata", value=organization_custom_rule_metadata, expected_type=type_hints["organization_custom_rule_metadata"])
            check_type(argname="argument organization_managed_rule_metadata", value=organization_managed_rule_metadata, expected_type=type_hints["organization_managed_rule_metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if excluded_accounts is not None:
            self._values["excluded_accounts"] = excluded_accounts
        if organization_config_rule_name is not None:
            self._values["organization_config_rule_name"] = organization_config_rule_name
        if organization_custom_policy_rule_metadata is not None:
            self._values["organization_custom_policy_rule_metadata"] = organization_custom_policy_rule_metadata
        if organization_custom_rule_metadata is not None:
            self._values["organization_custom_rule_metadata"] = organization_custom_rule_metadata
        if organization_managed_rule_metadata is not None:
            self._values["organization_managed_rule_metadata"] = organization_managed_rule_metadata

    @builtins.property
    def excluded_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A comma-separated list of accounts excluded from organization AWS Config rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconfigrule.html#cfn-config-organizationconfigrule-excludedaccounts
        '''
        result = self._values.get("excluded_accounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def organization_config_rule_name(self) -> typing.Optional[builtins.str]:
        '''The name that you assign to organization AWS Config rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconfigrule.html#cfn-config-organizationconfigrule-organizationconfigrulename
        '''
        result = self._values.get("organization_config_rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization_custom_policy_rule_metadata(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationConfigRulePropsMixin.OrganizationCustomPolicyRuleMetadataProperty"]]:
        '''An object that specifies metadata for your organization's AWS Config Custom Policy rule.

        The metadata includes the runtime system in use, which accounts have debug logging enabled, and other custom rule metadata, such as resource type, resource ID of AWS resource, and organization trigger types that initiate AWS Config to evaluate AWS resources against a rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconfigrule.html#cfn-config-organizationconfigrule-organizationcustompolicyrulemetadata
        '''
        result = self._values.get("organization_custom_policy_rule_metadata")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationConfigRulePropsMixin.OrganizationCustomPolicyRuleMetadataProperty"]], result)

    @builtins.property
    def organization_custom_rule_metadata(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationConfigRulePropsMixin.OrganizationCustomRuleMetadataProperty"]]:
        '''An ``OrganizationCustomRuleMetadata`` object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconfigrule.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata
        '''
        result = self._values.get("organization_custom_rule_metadata")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationConfigRulePropsMixin.OrganizationCustomRuleMetadataProperty"]], result)

    @builtins.property
    def organization_managed_rule_metadata(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationConfigRulePropsMixin.OrganizationManagedRuleMetadataProperty"]]:
        '''An ``OrganizationManagedRuleMetadata`` object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconfigrule.html#cfn-config-organizationconfigrule-organizationmanagedrulemetadata
        '''
        result = self._values.get("organization_managed_rule_metadata")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationConfigRulePropsMixin.OrganizationManagedRuleMetadataProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOrganizationConfigRuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnOrganizationConfigRulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnOrganizationConfigRulePropsMixin",
):
    '''Adds or updates an AWS Config rule for your entire organization to evaluate if your AWS resources comply with your desired configurations.

    For information on how many organization AWS Config rules you can have per account, see `*Service Limits* <https://docs.aws.amazon.com/config/latest/developerguide/configlimits.html>`_ in the *AWS Config Developer Guide* .

    Only a management account and a delegated administrator can create or update an organization AWS Config rule. When calling the ``OrganizationConfigRule`` resource with a delegated administrator, you must ensure AWS Organizations ``ListDelegatedAdministrator`` permissions are added. An organization can have up to 3 delegated administrators.

    The ``OrganizationConfigRule`` resource enables organization service access through the ``EnableAWSServiceAccess`` action and creates a service-linked role ``AWSServiceRoleForConfigMultiAccountSetup`` in the management or delegated administrator account of your organization. The service-linked role is created only when the role does not exist in the caller account. AWS Config verifies the existence of role with ``GetRole`` action.

    To use the ``OrganizationConfigRule`` resource with delegated administrator, register a delegated administrator by calling AWS Organization ``register-delegated-administrator`` for ``config-multiaccountsetup.amazonaws.com`` .

    There are two types of rules: *AWS Config Managed Rules* and *AWS Config Custom Rules* . You can use ``PutOrganizationConfigRule`` to create both AWS Config Managed Rules and AWS Config Custom Rules.

    AWS Config Managed Rules are predefined, customizable rules created by AWS Config . For a list of managed rules, see `List of AWS Config Managed Rules <https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html>`_ . If you are adding an AWS Config managed rule, you must specify the rule's identifier for the ``RuleIdentifier`` key.

    AWS Config Custom Rules are rules that you create from scratch. There are two ways to create AWS Config custom rules: with Lambda functions ( `AWS Lambda Developer Guide <https://docs.aws.amazon.com/config/latest/developerguide/gettingstarted-concepts.html#gettingstarted-concepts-function>`_ ) and with Guard ( `Guard GitHub Repository <https://docs.aws.amazon.com/https://github.com/aws-cloudformation/cloudformation-guard>`_ ), a policy-as-code language. AWS Config custom rules created with AWS Lambda are called *AWS Config Custom Lambda Rules* and AWS Config custom rules created with Guard are called *AWS Config Custom Policy Rules* .

    If you are adding a new AWS Config Custom Lambda rule, you first need to create an AWS Lambda function in the management account or a delegated administrator that the rule invokes to evaluate your resources. You also need to create an IAM role in the managed account that can be assumed by the Lambda function. When you use ``PutOrganizationConfigRule`` to add a Custom Lambda rule to AWS Config , you must specify the Amazon Resource Name (ARN) that AWS Lambda assigns to the function.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconfigrule.html
    :cloudformationResource: AWS::Config::OrganizationConfigRule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
        
        cfn_organization_config_rule_props_mixin = config_mixins.CfnOrganizationConfigRulePropsMixin(config_mixins.CfnOrganizationConfigRuleMixinProps(
            excluded_accounts=["excludedAccounts"],
            organization_config_rule_name="organizationConfigRuleName",
            organization_custom_policy_rule_metadata=config_mixins.CfnOrganizationConfigRulePropsMixin.OrganizationCustomPolicyRuleMetadataProperty(
                debug_log_delivery_accounts=["debugLogDeliveryAccounts"],
                description="description",
                input_parameters="inputParameters",
                maximum_execution_frequency="maximumExecutionFrequency",
                organization_config_rule_trigger_types=["organizationConfigRuleTriggerTypes"],
                policy_text="policyText",
                resource_id_scope="resourceIdScope",
                resource_types_scope=["resourceTypesScope"],
                runtime="runtime",
                tag_key_scope="tagKeyScope",
                tag_value_scope="tagValueScope"
            ),
            organization_custom_rule_metadata=config_mixins.CfnOrganizationConfigRulePropsMixin.OrganizationCustomRuleMetadataProperty(
                description="description",
                input_parameters="inputParameters",
                lambda_function_arn="lambdaFunctionArn",
                maximum_execution_frequency="maximumExecutionFrequency",
                organization_config_rule_trigger_types=["organizationConfigRuleTriggerTypes"],
                resource_id_scope="resourceIdScope",
                resource_types_scope=["resourceTypesScope"],
                tag_key_scope="tagKeyScope",
                tag_value_scope="tagValueScope"
            ),
            organization_managed_rule_metadata=config_mixins.CfnOrganizationConfigRulePropsMixin.OrganizationManagedRuleMetadataProperty(
                description="description",
                input_parameters="inputParameters",
                maximum_execution_frequency="maximumExecutionFrequency",
                resource_id_scope="resourceIdScope",
                resource_types_scope=["resourceTypesScope"],
                rule_identifier="ruleIdentifier",
                tag_key_scope="tagKeyScope",
                tag_value_scope="tagValueScope"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnOrganizationConfigRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Config::OrganizationConfigRule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c15695996c8070fb29dc227440159e0aa4de702c1864379bc523b0024d1da40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab87ba3514fd65504344ef6ccef9deb6d40b1cd4274ad58509a3e2b2495185bb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c2380eb7149f0a7ee4c5ce1c7268fac69c379a45dc55026bc79349df061ff5a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOrganizationConfigRuleMixinProps:
        return typing.cast(CfnOrganizationConfigRuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnOrganizationConfigRulePropsMixin.OrganizationCustomPolicyRuleMetadataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "debug_log_delivery_accounts": "debugLogDeliveryAccounts",
            "description": "description",
            "input_parameters": "inputParameters",
            "maximum_execution_frequency": "maximumExecutionFrequency",
            "organization_config_rule_trigger_types": "organizationConfigRuleTriggerTypes",
            "policy_text": "policyText",
            "resource_id_scope": "resourceIdScope",
            "resource_types_scope": "resourceTypesScope",
            "runtime": "runtime",
            "tag_key_scope": "tagKeyScope",
            "tag_value_scope": "tagValueScope",
        },
    )
    class OrganizationCustomPolicyRuleMetadataProperty:
        def __init__(
            self,
            *,
            debug_log_delivery_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
            description: typing.Optional[builtins.str] = None,
            input_parameters: typing.Optional[builtins.str] = None,
            maximum_execution_frequency: typing.Optional[builtins.str] = None,
            organization_config_rule_trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            policy_text: typing.Optional[builtins.str] = None,
            resource_id_scope: typing.Optional[builtins.str] = None,
            resource_types_scope: typing.Optional[typing.Sequence[builtins.str]] = None,
            runtime: typing.Optional[builtins.str] = None,
            tag_key_scope: typing.Optional[builtins.str] = None,
            tag_value_scope: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that specifies metadata for your organization's AWS Config Custom Policy rule.

            The metadata includes the runtime system in use, which accounts have debug logging enabled, and other custom rule metadata, such as resource type, resource ID of AWS resource, and organization trigger types that initiate AWS Config to evaluate AWS resources against a rule.

            :param debug_log_delivery_accounts: A list of accounts that you can enable debug logging for your organization AWS Config Custom Policy rule. List is null when debug logging is enabled for all accounts.
            :param description: The description that you provide for your organization AWS Config Custom Policy rule.
            :param input_parameters: A string, in JSON format, that is passed to your organization AWS Config Custom Policy rule.
            :param maximum_execution_frequency: The maximum frequency with which AWS Config runs evaluations for a rule. Your AWS Config Custom Policy rule is triggered when AWS Config delivers the configuration snapshot. For more information, see ``ConfigSnapshotDeliveryProperties`` .
            :param organization_config_rule_trigger_types: The type of notification that initiates AWS Config to run an evaluation for a rule. For AWS Config Custom Policy rules, AWS Config supports change-initiated notification types: - ``ConfigurationItemChangeNotification`` - Initiates an evaluation when AWS Config delivers a configuration item as a result of a resource change. - ``OversizedConfigurationItemChangeNotification`` - Initiates an evaluation when AWS Config delivers an oversized configuration item. AWS Config may generate this notification type when a resource changes and the notification exceeds the maximum size allowed by Amazon SNS.
            :param policy_text: The policy definition containing the logic for your organization AWS Config Custom Policy rule.
            :param resource_id_scope: The ID of the AWS resource that was evaluated.
            :param resource_types_scope: The type of the AWS resource that was evaluated.
            :param runtime: The runtime system for your organization AWS Config Custom Policy rules. Guard is a policy-as-code language that allows you to write policies that are enforced by AWS Config Custom Policy rules. For more information about Guard, see the `Guard GitHub Repository <https://docs.aws.amazon.com/https://github.com/aws-cloudformation/cloudformation-guard>`_ .
            :param tag_key_scope: One part of a key-value pair that make up a tag. A key is a general label that acts like a category for more specific tag values.
            :param tag_value_scope: The optional part of a key-value pair that make up a tag. A value acts as a descriptor within a tag category (key).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustompolicyrulemetadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                organization_custom_policy_rule_metadata_property = config_mixins.CfnOrganizationConfigRulePropsMixin.OrganizationCustomPolicyRuleMetadataProperty(
                    debug_log_delivery_accounts=["debugLogDeliveryAccounts"],
                    description="description",
                    input_parameters="inputParameters",
                    maximum_execution_frequency="maximumExecutionFrequency",
                    organization_config_rule_trigger_types=["organizationConfigRuleTriggerTypes"],
                    policy_text="policyText",
                    resource_id_scope="resourceIdScope",
                    resource_types_scope=["resourceTypesScope"],
                    runtime="runtime",
                    tag_key_scope="tagKeyScope",
                    tag_value_scope="tagValueScope"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__88ff11641d26c5e240dfade391c6b18d677a6078b60fede222c0cb22435b5121)
                check_type(argname="argument debug_log_delivery_accounts", value=debug_log_delivery_accounts, expected_type=type_hints["debug_log_delivery_accounts"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument input_parameters", value=input_parameters, expected_type=type_hints["input_parameters"])
                check_type(argname="argument maximum_execution_frequency", value=maximum_execution_frequency, expected_type=type_hints["maximum_execution_frequency"])
                check_type(argname="argument organization_config_rule_trigger_types", value=organization_config_rule_trigger_types, expected_type=type_hints["organization_config_rule_trigger_types"])
                check_type(argname="argument policy_text", value=policy_text, expected_type=type_hints["policy_text"])
                check_type(argname="argument resource_id_scope", value=resource_id_scope, expected_type=type_hints["resource_id_scope"])
                check_type(argname="argument resource_types_scope", value=resource_types_scope, expected_type=type_hints["resource_types_scope"])
                check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
                check_type(argname="argument tag_key_scope", value=tag_key_scope, expected_type=type_hints["tag_key_scope"])
                check_type(argname="argument tag_value_scope", value=tag_value_scope, expected_type=type_hints["tag_value_scope"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if debug_log_delivery_accounts is not None:
                self._values["debug_log_delivery_accounts"] = debug_log_delivery_accounts
            if description is not None:
                self._values["description"] = description
            if input_parameters is not None:
                self._values["input_parameters"] = input_parameters
            if maximum_execution_frequency is not None:
                self._values["maximum_execution_frequency"] = maximum_execution_frequency
            if organization_config_rule_trigger_types is not None:
                self._values["organization_config_rule_trigger_types"] = organization_config_rule_trigger_types
            if policy_text is not None:
                self._values["policy_text"] = policy_text
            if resource_id_scope is not None:
                self._values["resource_id_scope"] = resource_id_scope
            if resource_types_scope is not None:
                self._values["resource_types_scope"] = resource_types_scope
            if runtime is not None:
                self._values["runtime"] = runtime
            if tag_key_scope is not None:
                self._values["tag_key_scope"] = tag_key_scope
            if tag_value_scope is not None:
                self._values["tag_value_scope"] = tag_value_scope

        @builtins.property
        def debug_log_delivery_accounts(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of accounts that you can enable debug logging for your organization AWS Config Custom Policy rule.

            List is null when debug logging is enabled for all accounts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustompolicyrulemetadata.html#cfn-config-organizationconfigrule-organizationcustompolicyrulemetadata-debuglogdeliveryaccounts
            '''
            result = self._values.get("debug_log_delivery_accounts")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description that you provide for your organization AWS Config Custom Policy rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustompolicyrulemetadata.html#cfn-config-organizationconfigrule-organizationcustompolicyrulemetadata-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_parameters(self) -> typing.Optional[builtins.str]:
            '''A string, in JSON format, that is passed to your organization AWS Config Custom Policy rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustompolicyrulemetadata.html#cfn-config-organizationconfigrule-organizationcustompolicyrulemetadata-inputparameters
            '''
            result = self._values.get("input_parameters")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def maximum_execution_frequency(self) -> typing.Optional[builtins.str]:
            '''The maximum frequency with which AWS Config runs evaluations for a rule.

            Your AWS Config Custom Policy rule is triggered when AWS Config delivers the configuration snapshot. For more information, see ``ConfigSnapshotDeliveryProperties`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustompolicyrulemetadata.html#cfn-config-organizationconfigrule-organizationcustompolicyrulemetadata-maximumexecutionfrequency
            '''
            result = self._values.get("maximum_execution_frequency")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def organization_config_rule_trigger_types(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The type of notification that initiates AWS Config to run an evaluation for a rule.

            For AWS Config Custom Policy rules, AWS Config supports change-initiated notification types:

            - ``ConfigurationItemChangeNotification`` - Initiates an evaluation when AWS Config delivers a configuration item as a result of a resource change.
            - ``OversizedConfigurationItemChangeNotification`` - Initiates an evaluation when AWS Config delivers an oversized configuration item. AWS Config may generate this notification type when a resource changes and the notification exceeds the maximum size allowed by Amazon SNS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustompolicyrulemetadata.html#cfn-config-organizationconfigrule-organizationcustompolicyrulemetadata-organizationconfigruletriggertypes
            '''
            result = self._values.get("organization_config_rule_trigger_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def policy_text(self) -> typing.Optional[builtins.str]:
            '''The policy definition containing the logic for your organization AWS Config Custom Policy rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustompolicyrulemetadata.html#cfn-config-organizationconfigrule-organizationcustompolicyrulemetadata-policytext
            '''
            result = self._values.get("policy_text")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_id_scope(self) -> typing.Optional[builtins.str]:
            '''The ID of the AWS resource that was evaluated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustompolicyrulemetadata.html#cfn-config-organizationconfigrule-organizationcustompolicyrulemetadata-resourceidscope
            '''
            result = self._values.get("resource_id_scope")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_types_scope(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The type of the AWS resource that was evaluated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustompolicyrulemetadata.html#cfn-config-organizationconfigrule-organizationcustompolicyrulemetadata-resourcetypesscope
            '''
            result = self._values.get("resource_types_scope")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def runtime(self) -> typing.Optional[builtins.str]:
            '''The runtime system for your organization AWS Config Custom Policy rules.

            Guard is a policy-as-code language that allows you to write policies that are enforced by AWS Config Custom Policy rules. For more information about Guard, see the `Guard GitHub Repository <https://docs.aws.amazon.com/https://github.com/aws-cloudformation/cloudformation-guard>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustompolicyrulemetadata.html#cfn-config-organizationconfigrule-organizationcustompolicyrulemetadata-runtime
            '''
            result = self._values.get("runtime")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_key_scope(self) -> typing.Optional[builtins.str]:
            '''One part of a key-value pair that make up a tag.

            A key is a general label that acts like a category for more specific tag values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustompolicyrulemetadata.html#cfn-config-organizationconfigrule-organizationcustompolicyrulemetadata-tagkeyscope
            '''
            result = self._values.get("tag_key_scope")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_value_scope(self) -> typing.Optional[builtins.str]:
            '''The optional part of a key-value pair that make up a tag.

            A value acts as a descriptor within a tag category (key).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustompolicyrulemetadata.html#cfn-config-organizationconfigrule-organizationcustompolicyrulemetadata-tagvaluescope
            '''
            result = self._values.get("tag_value_scope")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OrganizationCustomPolicyRuleMetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnOrganizationConfigRulePropsMixin.OrganizationCustomRuleMetadataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "input_parameters": "inputParameters",
            "lambda_function_arn": "lambdaFunctionArn",
            "maximum_execution_frequency": "maximumExecutionFrequency",
            "organization_config_rule_trigger_types": "organizationConfigRuleTriggerTypes",
            "resource_id_scope": "resourceIdScope",
            "resource_types_scope": "resourceTypesScope",
            "tag_key_scope": "tagKeyScope",
            "tag_value_scope": "tagValueScope",
        },
    )
    class OrganizationCustomRuleMetadataProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            input_parameters: typing.Optional[builtins.str] = None,
            lambda_function_arn: typing.Optional[builtins.str] = None,
            maximum_execution_frequency: typing.Optional[builtins.str] = None,
            organization_config_rule_trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            resource_id_scope: typing.Optional[builtins.str] = None,
            resource_types_scope: typing.Optional[typing.Sequence[builtins.str]] = None,
            tag_key_scope: typing.Optional[builtins.str] = None,
            tag_value_scope: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that specifies organization custom rule metadata such as resource type, resource ID of AWS resource, Lambda function ARN, and organization trigger types that trigger AWS Config to evaluate your AWS resources against a rule.

            It also provides the frequency with which you want AWS Config to run evaluations for the rule if the trigger type is periodic.

            :param description: The description that you provide for your organization AWS Config rule.
            :param input_parameters: A string, in JSON format, that is passed to your organization AWS Config rule Lambda function.
            :param lambda_function_arn: The lambda function ARN.
            :param maximum_execution_frequency: The maximum frequency with which AWS Config runs evaluations for a rule. Your custom rule is triggered when AWS Config delivers the configuration snapshot. For more information, see ``ConfigSnapshotDeliveryProperties`` . .. epigraph:: By default, rules with a periodic trigger are evaluated every 24 hours. To change the frequency, specify a valid value for the ``MaximumExecutionFrequency`` parameter.
            :param organization_config_rule_trigger_types: The type of notification that triggers AWS Config to run an evaluation for a rule. You can specify the following notification types: - ``ConfigurationItemChangeNotification`` - Triggers an evaluation when AWS Config delivers a configuration item as a result of a resource change. - ``OversizedConfigurationItemChangeNotification`` - Triggers an evaluation when AWS Config delivers an oversized configuration item. AWS Config may generate this notification type when a resource changes and the notification exceeds the maximum size allowed by Amazon SNS. - ``ScheduledNotification`` - Triggers a periodic evaluation at the frequency specified for ``MaximumExecutionFrequency`` .
            :param resource_id_scope: The ID of the AWS resource that was evaluated.
            :param resource_types_scope: The type of the AWS resource that was evaluated.
            :param tag_key_scope: One part of a key-value pair that make up a tag. A key is a general label that acts like a category for more specific tag values.
            :param tag_value_scope: The optional part of a key-value pair that make up a tag. A value acts as a descriptor within a tag category (key).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustomrulemetadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                organization_custom_rule_metadata_property = config_mixins.CfnOrganizationConfigRulePropsMixin.OrganizationCustomRuleMetadataProperty(
                    description="description",
                    input_parameters="inputParameters",
                    lambda_function_arn="lambdaFunctionArn",
                    maximum_execution_frequency="maximumExecutionFrequency",
                    organization_config_rule_trigger_types=["organizationConfigRuleTriggerTypes"],
                    resource_id_scope="resourceIdScope",
                    resource_types_scope=["resourceTypesScope"],
                    tag_key_scope="tagKeyScope",
                    tag_value_scope="tagValueScope"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f9ccaa5b324031de41fd89447ed356de726c38aa567da9702bb64c9a6c172f16)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument input_parameters", value=input_parameters, expected_type=type_hints["input_parameters"])
                check_type(argname="argument lambda_function_arn", value=lambda_function_arn, expected_type=type_hints["lambda_function_arn"])
                check_type(argname="argument maximum_execution_frequency", value=maximum_execution_frequency, expected_type=type_hints["maximum_execution_frequency"])
                check_type(argname="argument organization_config_rule_trigger_types", value=organization_config_rule_trigger_types, expected_type=type_hints["organization_config_rule_trigger_types"])
                check_type(argname="argument resource_id_scope", value=resource_id_scope, expected_type=type_hints["resource_id_scope"])
                check_type(argname="argument resource_types_scope", value=resource_types_scope, expected_type=type_hints["resource_types_scope"])
                check_type(argname="argument tag_key_scope", value=tag_key_scope, expected_type=type_hints["tag_key_scope"])
                check_type(argname="argument tag_value_scope", value=tag_value_scope, expected_type=type_hints["tag_value_scope"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if input_parameters is not None:
                self._values["input_parameters"] = input_parameters
            if lambda_function_arn is not None:
                self._values["lambda_function_arn"] = lambda_function_arn
            if maximum_execution_frequency is not None:
                self._values["maximum_execution_frequency"] = maximum_execution_frequency
            if organization_config_rule_trigger_types is not None:
                self._values["organization_config_rule_trigger_types"] = organization_config_rule_trigger_types
            if resource_id_scope is not None:
                self._values["resource_id_scope"] = resource_id_scope
            if resource_types_scope is not None:
                self._values["resource_types_scope"] = resource_types_scope
            if tag_key_scope is not None:
                self._values["tag_key_scope"] = tag_key_scope
            if tag_value_scope is not None:
                self._values["tag_value_scope"] = tag_value_scope

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description that you provide for your organization AWS Config rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustomrulemetadata.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_parameters(self) -> typing.Optional[builtins.str]:
            '''A string, in JSON format, that is passed to your organization AWS Config rule Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustomrulemetadata.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata-inputparameters
            '''
            result = self._values.get("input_parameters")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def lambda_function_arn(self) -> typing.Optional[builtins.str]:
            '''The lambda function ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustomrulemetadata.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata-lambdafunctionarn
            '''
            result = self._values.get("lambda_function_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def maximum_execution_frequency(self) -> typing.Optional[builtins.str]:
            '''The maximum frequency with which AWS Config runs evaluations for a rule.

            Your custom rule is triggered when AWS Config delivers the configuration snapshot. For more information, see ``ConfigSnapshotDeliveryProperties`` .
            .. epigraph::

               By default, rules with a periodic trigger are evaluated every 24 hours. To change the frequency, specify a valid value for the ``MaximumExecutionFrequency`` parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustomrulemetadata.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata-maximumexecutionfrequency
            '''
            result = self._values.get("maximum_execution_frequency")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def organization_config_rule_trigger_types(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The type of notification that triggers AWS Config to run an evaluation for a rule.

            You can specify the following notification types:

            - ``ConfigurationItemChangeNotification`` - Triggers an evaluation when AWS Config delivers a configuration item as a result of a resource change.
            - ``OversizedConfigurationItemChangeNotification`` - Triggers an evaluation when AWS Config delivers an oversized configuration item. AWS Config may generate this notification type when a resource changes and the notification exceeds the maximum size allowed by Amazon SNS.
            - ``ScheduledNotification`` - Triggers a periodic evaluation at the frequency specified for ``MaximumExecutionFrequency`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustomrulemetadata.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata-organizationconfigruletriggertypes
            '''
            result = self._values.get("organization_config_rule_trigger_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def resource_id_scope(self) -> typing.Optional[builtins.str]:
            '''The ID of the AWS resource that was evaluated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustomrulemetadata.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata-resourceidscope
            '''
            result = self._values.get("resource_id_scope")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_types_scope(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The type of the AWS resource that was evaluated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustomrulemetadata.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata-resourcetypesscope
            '''
            result = self._values.get("resource_types_scope")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def tag_key_scope(self) -> typing.Optional[builtins.str]:
            '''One part of a key-value pair that make up a tag.

            A key is a general label that acts like a category for more specific tag values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustomrulemetadata.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata-tagkeyscope
            '''
            result = self._values.get("tag_key_scope")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_value_scope(self) -> typing.Optional[builtins.str]:
            '''The optional part of a key-value pair that make up a tag.

            A value acts as a descriptor within a tag category (key).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationcustomrulemetadata.html#cfn-config-organizationconfigrule-organizationcustomrulemetadata-tagvaluescope
            '''
            result = self._values.get("tag_value_scope")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OrganizationCustomRuleMetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnOrganizationConfigRulePropsMixin.OrganizationManagedRuleMetadataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "input_parameters": "inputParameters",
            "maximum_execution_frequency": "maximumExecutionFrequency",
            "resource_id_scope": "resourceIdScope",
            "resource_types_scope": "resourceTypesScope",
            "rule_identifier": "ruleIdentifier",
            "tag_key_scope": "tagKeyScope",
            "tag_value_scope": "tagValueScope",
        },
    )
    class OrganizationManagedRuleMetadataProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            input_parameters: typing.Optional[builtins.str] = None,
            maximum_execution_frequency: typing.Optional[builtins.str] = None,
            resource_id_scope: typing.Optional[builtins.str] = None,
            resource_types_scope: typing.Optional[typing.Sequence[builtins.str]] = None,
            rule_identifier: typing.Optional[builtins.str] = None,
            tag_key_scope: typing.Optional[builtins.str] = None,
            tag_value_scope: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that specifies organization managed rule metadata such as resource type and ID of AWS resource along with the rule identifier.

            It also provides the frequency with which you want AWS Config to run evaluations for the rule if the trigger type is periodic.

            :param description: The description that you provide for your organization AWS Config rule.
            :param input_parameters: A string, in JSON format, that is passed to your organization AWS Config rule Lambda function.
            :param maximum_execution_frequency: The maximum frequency with which AWS Config runs evaluations for a rule. This is for an AWS Config managed rule that is triggered at a periodic frequency. .. epigraph:: By default, rules with a periodic trigger are evaluated every 24 hours. To change the frequency, specify a valid value for the ``MaximumExecutionFrequency`` parameter.
            :param resource_id_scope: The ID of the AWS resource that was evaluated.
            :param resource_types_scope: The type of the AWS resource that was evaluated.
            :param rule_identifier: For organization config managed rules, a predefined identifier from a list. For example, ``IAM_PASSWORD_POLICY`` is a managed rule. To reference a managed rule, see `Using AWS Config managed rules <https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_use-managed-rules.html>`_ .
            :param tag_key_scope: One part of a key-value pair that make up a tag. A key is a general label that acts like a category for more specific tag values.
            :param tag_value_scope: The optional part of a key-value pair that make up a tag. A value acts as a descriptor within a tag category (key).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationmanagedrulemetadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                organization_managed_rule_metadata_property = config_mixins.CfnOrganizationConfigRulePropsMixin.OrganizationManagedRuleMetadataProperty(
                    description="description",
                    input_parameters="inputParameters",
                    maximum_execution_frequency="maximumExecutionFrequency",
                    resource_id_scope="resourceIdScope",
                    resource_types_scope=["resourceTypesScope"],
                    rule_identifier="ruleIdentifier",
                    tag_key_scope="tagKeyScope",
                    tag_value_scope="tagValueScope"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f59685a3c0265e0cbfd3929ad629d84f9bd01df52f06c13fe11b2cf3441dd212)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument input_parameters", value=input_parameters, expected_type=type_hints["input_parameters"])
                check_type(argname="argument maximum_execution_frequency", value=maximum_execution_frequency, expected_type=type_hints["maximum_execution_frequency"])
                check_type(argname="argument resource_id_scope", value=resource_id_scope, expected_type=type_hints["resource_id_scope"])
                check_type(argname="argument resource_types_scope", value=resource_types_scope, expected_type=type_hints["resource_types_scope"])
                check_type(argname="argument rule_identifier", value=rule_identifier, expected_type=type_hints["rule_identifier"])
                check_type(argname="argument tag_key_scope", value=tag_key_scope, expected_type=type_hints["tag_key_scope"])
                check_type(argname="argument tag_value_scope", value=tag_value_scope, expected_type=type_hints["tag_value_scope"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if input_parameters is not None:
                self._values["input_parameters"] = input_parameters
            if maximum_execution_frequency is not None:
                self._values["maximum_execution_frequency"] = maximum_execution_frequency
            if resource_id_scope is not None:
                self._values["resource_id_scope"] = resource_id_scope
            if resource_types_scope is not None:
                self._values["resource_types_scope"] = resource_types_scope
            if rule_identifier is not None:
                self._values["rule_identifier"] = rule_identifier
            if tag_key_scope is not None:
                self._values["tag_key_scope"] = tag_key_scope
            if tag_value_scope is not None:
                self._values["tag_value_scope"] = tag_value_scope

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description that you provide for your organization AWS Config rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationmanagedrulemetadata.html#cfn-config-organizationconfigrule-organizationmanagedrulemetadata-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_parameters(self) -> typing.Optional[builtins.str]:
            '''A string, in JSON format, that is passed to your organization AWS Config rule Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationmanagedrulemetadata.html#cfn-config-organizationconfigrule-organizationmanagedrulemetadata-inputparameters
            '''
            result = self._values.get("input_parameters")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def maximum_execution_frequency(self) -> typing.Optional[builtins.str]:
            '''The maximum frequency with which AWS Config runs evaluations for a rule.

            This is for an AWS Config managed rule that is triggered at a periodic frequency.
            .. epigraph::

               By default, rules with a periodic trigger are evaluated every 24 hours. To change the frequency, specify a valid value for the ``MaximumExecutionFrequency`` parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationmanagedrulemetadata.html#cfn-config-organizationconfigrule-organizationmanagedrulemetadata-maximumexecutionfrequency
            '''
            result = self._values.get("maximum_execution_frequency")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_id_scope(self) -> typing.Optional[builtins.str]:
            '''The ID of the AWS resource that was evaluated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationmanagedrulemetadata.html#cfn-config-organizationconfigrule-organizationmanagedrulemetadata-resourceidscope
            '''
            result = self._values.get("resource_id_scope")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_types_scope(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The type of the AWS resource that was evaluated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationmanagedrulemetadata.html#cfn-config-organizationconfigrule-organizationmanagedrulemetadata-resourcetypesscope
            '''
            result = self._values.get("resource_types_scope")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def rule_identifier(self) -> typing.Optional[builtins.str]:
            '''For organization config managed rules, a predefined identifier from a list.

            For example, ``IAM_PASSWORD_POLICY`` is a managed rule. To reference a managed rule, see `Using AWS Config managed rules <https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_use-managed-rules.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationmanagedrulemetadata.html#cfn-config-organizationconfigrule-organizationmanagedrulemetadata-ruleidentifier
            '''
            result = self._values.get("rule_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_key_scope(self) -> typing.Optional[builtins.str]:
            '''One part of a key-value pair that make up a tag.

            A key is a general label that acts like a category for more specific tag values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationmanagedrulemetadata.html#cfn-config-organizationconfigrule-organizationmanagedrulemetadata-tagkeyscope
            '''
            result = self._values.get("tag_key_scope")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_value_scope(self) -> typing.Optional[builtins.str]:
            '''The optional part of a key-value pair that make up a tag.

            A value acts as a descriptor within a tag category (key).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconfigrule-organizationmanagedrulemetadata.html#cfn-config-organizationconfigrule-organizationmanagedrulemetadata-tagvaluescope
            '''
            result = self._values.get("tag_value_scope")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OrganizationManagedRuleMetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnOrganizationConformancePackMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "conformance_pack_input_parameters": "conformancePackInputParameters",
        "delivery_s3_bucket": "deliveryS3Bucket",
        "delivery_s3_key_prefix": "deliveryS3KeyPrefix",
        "excluded_accounts": "excludedAccounts",
        "organization_conformance_pack_name": "organizationConformancePackName",
        "template_body": "templateBody",
        "template_s3_uri": "templateS3Uri",
    },
)
class CfnOrganizationConformancePackMixinProps:
    def __init__(
        self,
        *,
        conformance_pack_input_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOrganizationConformancePackPropsMixin.ConformancePackInputParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        delivery_s3_bucket: typing.Optional[builtins.str] = None,
        delivery_s3_key_prefix: typing.Optional[builtins.str] = None,
        excluded_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        organization_conformance_pack_name: typing.Optional[builtins.str] = None,
        template_body: typing.Optional[builtins.str] = None,
        template_s3_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnOrganizationConformancePackPropsMixin.

        :param conformance_pack_input_parameters: A list of ``ConformancePackInputParameter`` objects.
        :param delivery_s3_bucket: The name of the Amazon S3 bucket where AWS Config stores conformance pack templates. .. epigraph:: This field is optional.
        :param delivery_s3_key_prefix: Any folder structure you want to add to an Amazon S3 bucket. .. epigraph:: This field is optional.
        :param excluded_accounts: A comma-separated list of accounts excluded from organization conformance pack.
        :param organization_conformance_pack_name: The name you assign to an organization conformance pack.
        :param template_body: A string containing full conformance pack template body. Structure containing the template body with a minimum length of 1 byte and a maximum length of 51,200 bytes.
        :param template_s3_uri: Location of file containing the template body. The uri must point to the conformance pack template (max size: 300 KB).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
            
            cfn_organization_conformance_pack_mixin_props = config_mixins.CfnOrganizationConformancePackMixinProps(
                conformance_pack_input_parameters=[config_mixins.CfnOrganizationConformancePackPropsMixin.ConformancePackInputParameterProperty(
                    parameter_name="parameterName",
                    parameter_value="parameterValue"
                )],
                delivery_s3_bucket="deliveryS3Bucket",
                delivery_s3_key_prefix="deliveryS3KeyPrefix",
                excluded_accounts=["excludedAccounts"],
                organization_conformance_pack_name="organizationConformancePackName",
                template_body="templateBody",
                template_s3_uri="templateS3Uri"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67af5ee0ec84ebb73383fef5539313ec9f424903a938bd791b267cd3578e1fe4)
            check_type(argname="argument conformance_pack_input_parameters", value=conformance_pack_input_parameters, expected_type=type_hints["conformance_pack_input_parameters"])
            check_type(argname="argument delivery_s3_bucket", value=delivery_s3_bucket, expected_type=type_hints["delivery_s3_bucket"])
            check_type(argname="argument delivery_s3_key_prefix", value=delivery_s3_key_prefix, expected_type=type_hints["delivery_s3_key_prefix"])
            check_type(argname="argument excluded_accounts", value=excluded_accounts, expected_type=type_hints["excluded_accounts"])
            check_type(argname="argument organization_conformance_pack_name", value=organization_conformance_pack_name, expected_type=type_hints["organization_conformance_pack_name"])
            check_type(argname="argument template_body", value=template_body, expected_type=type_hints["template_body"])
            check_type(argname="argument template_s3_uri", value=template_s3_uri, expected_type=type_hints["template_s3_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if conformance_pack_input_parameters is not None:
            self._values["conformance_pack_input_parameters"] = conformance_pack_input_parameters
        if delivery_s3_bucket is not None:
            self._values["delivery_s3_bucket"] = delivery_s3_bucket
        if delivery_s3_key_prefix is not None:
            self._values["delivery_s3_key_prefix"] = delivery_s3_key_prefix
        if excluded_accounts is not None:
            self._values["excluded_accounts"] = excluded_accounts
        if organization_conformance_pack_name is not None:
            self._values["organization_conformance_pack_name"] = organization_conformance_pack_name
        if template_body is not None:
            self._values["template_body"] = template_body
        if template_s3_uri is not None:
            self._values["template_s3_uri"] = template_s3_uri

    @builtins.property
    def conformance_pack_input_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationConformancePackPropsMixin.ConformancePackInputParameterProperty"]]]]:
        '''A list of ``ConformancePackInputParameter`` objects.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-conformancepackinputparameters
        '''
        result = self._values.get("conformance_pack_input_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOrganizationConformancePackPropsMixin.ConformancePackInputParameterProperty"]]]], result)

    @builtins.property
    def delivery_s3_bucket(self) -> typing.Optional[builtins.str]:
        '''The name of the Amazon S3 bucket where AWS Config stores conformance pack templates.

        .. epigraph::

           This field is optional.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-deliverys3bucket
        '''
        result = self._values.get("delivery_s3_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delivery_s3_key_prefix(self) -> typing.Optional[builtins.str]:
        '''Any folder structure you want to add to an Amazon S3 bucket.

        .. epigraph::

           This field is optional.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-deliverys3keyprefix
        '''
        result = self._values.get("delivery_s3_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def excluded_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A comma-separated list of accounts excluded from organization conformance pack.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-excludedaccounts
        '''
        result = self._values.get("excluded_accounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def organization_conformance_pack_name(self) -> typing.Optional[builtins.str]:
        '''The name you assign to an organization conformance pack.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-organizationconformancepackname
        '''
        result = self._values.get("organization_conformance_pack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_body(self) -> typing.Optional[builtins.str]:
        '''A string containing full conformance pack template body.

        Structure containing the template body with a minimum length of 1 byte and a maximum length of 51,200 bytes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-templatebody
        '''
        result = self._values.get("template_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_s3_uri(self) -> typing.Optional[builtins.str]:
        '''Location of file containing the template body.

        The uri must point to the conformance pack template (max size: 300 KB).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html#cfn-config-organizationconformancepack-templates3uri
        '''
        result = self._values.get("template_s3_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOrganizationConformancePackMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnOrganizationConformancePackPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnOrganizationConformancePackPropsMixin",
):
    '''OrganizationConformancePack deploys conformance packs across member accounts in an AWS Organizations .

    OrganizationConformancePack enables organization service access for ``config-multiaccountsetup.amazonaws.com`` through the ``EnableAWSServiceAccess`` action and creates a service linked role in the master account of your organization. The service linked role is created only when the role does not exist in the master account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html
    :cloudformationResource: AWS::Config::OrganizationConformancePack
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
        
        cfn_organization_conformance_pack_props_mixin = config_mixins.CfnOrganizationConformancePackPropsMixin(config_mixins.CfnOrganizationConformancePackMixinProps(
            conformance_pack_input_parameters=[config_mixins.CfnOrganizationConformancePackPropsMixin.ConformancePackInputParameterProperty(
                parameter_name="parameterName",
                parameter_value="parameterValue"
            )],
            delivery_s3_bucket="deliveryS3Bucket",
            delivery_s3_key_prefix="deliveryS3KeyPrefix",
            excluded_accounts=["excludedAccounts"],
            organization_conformance_pack_name="organizationConformancePackName",
            template_body="templateBody",
            template_s3_uri="templateS3Uri"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnOrganizationConformancePackMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Config::OrganizationConformancePack``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__748f09781f965ba393be6c08be4f1bed65c7dd82ca64f31be5ec201dfde0ce1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c6d7c669d20f00486b974a801d9ca5c4e41d6af4ef5ff7cc1b86f6f541074b7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df8d744751f9e2bc20141f8c0a1a2992e3c1a111f430dedbcd908af03d4c484f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOrganizationConformancePackMixinProps:
        return typing.cast(CfnOrganizationConformancePackMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnOrganizationConformancePackPropsMixin.ConformancePackInputParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameter_name": "parameterName",
            "parameter_value": "parameterValue",
        },
    )
    class ConformancePackInputParameterProperty:
        def __init__(
            self,
            *,
            parameter_name: typing.Optional[builtins.str] = None,
            parameter_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Input parameters in the form of key-value pairs for the conformance pack, both of which you define.

            Keys can have a maximum character length of 255 characters, and values can have a maximum length of 4096 characters.

            :param parameter_name: One part of a key-value pair.
            :param parameter_value: One part of a key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconformancepack-conformancepackinputparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                conformance_pack_input_parameter_property = config_mixins.CfnOrganizationConformancePackPropsMixin.ConformancePackInputParameterProperty(
                    parameter_name="parameterName",
                    parameter_value="parameterValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__11a7852ac3130258fa5689c3a70cc9b809e040a04c6b30f7563937184b299812)
                check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
                check_type(argname="argument parameter_value", value=parameter_value, expected_type=type_hints["parameter_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parameter_name is not None:
                self._values["parameter_name"] = parameter_name
            if parameter_value is not None:
                self._values["parameter_value"] = parameter_value

        @builtins.property
        def parameter_name(self) -> typing.Optional[builtins.str]:
            '''One part of a key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconformancepack-conformancepackinputparameter.html#cfn-config-organizationconformancepack-conformancepackinputparameter-parametername
            '''
            result = self._values.get("parameter_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameter_value(self) -> typing.Optional[builtins.str]:
            '''One part of a key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-organizationconformancepack-conformancepackinputparameter.html#cfn-config-organizationconformancepack-conformancepackinputparameter-parametervalue
            '''
            result = self._values.get("parameter_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConformancePackInputParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnRemediationConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "automatic": "automatic",
        "config_rule_name": "configRuleName",
        "execution_controls": "executionControls",
        "maximum_automatic_attempts": "maximumAutomaticAttempts",
        "parameters": "parameters",
        "resource_type": "resourceType",
        "retry_attempt_seconds": "retryAttemptSeconds",
        "target_id": "targetId",
        "target_type": "targetType",
        "target_version": "targetVersion",
    },
)
class CfnRemediationConfigurationMixinProps:
    def __init__(
        self,
        *,
        automatic: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        config_rule_name: typing.Optional[builtins.str] = None,
        execution_controls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRemediationConfigurationPropsMixin.ExecutionControlsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        maximum_automatic_attempts: typing.Optional[jsii.Number] = None,
        parameters: typing.Any = None,
        resource_type: typing.Optional[builtins.str] = None,
        retry_attempt_seconds: typing.Optional[jsii.Number] = None,
        target_id: typing.Optional[builtins.str] = None,
        target_type: typing.Optional[builtins.str] = None,
        target_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnRemediationConfigurationPropsMixin.

        :param automatic: The remediation is triggered automatically.
        :param config_rule_name: The name of the AWS Config rule.
        :param execution_controls: An ExecutionControls object.
        :param maximum_automatic_attempts: The maximum number of failed attempts for auto-remediation. If you do not select a number, the default is 5. For example, if you specify MaximumAutomaticAttempts as 5 with RetryAttemptSeconds as 50 seconds, AWS Config will put a RemediationException on your behalf for the failing resource after the 5th failed attempt within 50 seconds.
        :param parameters: An object of the RemediationParameterValue. For more information, see `RemediationParameterValue <https://docs.aws.amazon.com/config/latest/APIReference/API_RemediationParameterValue.html>`_ . .. epigraph:: The type is a map of strings to RemediationParameterValue.
        :param resource_type: The type of a resource.
        :param retry_attempt_seconds: Time window to determine whether or not to add a remediation exception to prevent infinite remediation attempts. If ``MaximumAutomaticAttempts`` remediation attempts have been made under ``RetryAttemptSeconds`` , a remediation exception will be added to the resource. If you do not select a number, the default is 60 seconds. For example, if you specify ``RetryAttemptSeconds`` as 50 seconds and ``MaximumAutomaticAttempts`` as 5, AWS Config will run auto-remediations 5 times within 50 seconds before adding a remediation exception to the resource.
        :param target_id: Target ID is the name of the SSM document.
        :param target_type: The type of the target. Target executes remediation. For example, SSM document.
        :param target_version: Version of the target. For example, version of the SSM document. .. epigraph:: If you make backward incompatible changes to the SSM document, you must call PutRemediationConfiguration API again to ensure the remediations can run.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
            
            # parameters: Any
            
            cfn_remediation_configuration_mixin_props = config_mixins.CfnRemediationConfigurationMixinProps(
                automatic=False,
                config_rule_name="configRuleName",
                execution_controls=config_mixins.CfnRemediationConfigurationPropsMixin.ExecutionControlsProperty(
                    ssm_controls=config_mixins.CfnRemediationConfigurationPropsMixin.SsmControlsProperty(
                        concurrent_execution_rate_percentage=123,
                        error_percentage=123
                    )
                ),
                maximum_automatic_attempts=123,
                parameters=parameters,
                resource_type="resourceType",
                retry_attempt_seconds=123,
                target_id="targetId",
                target_type="targetType",
                target_version="targetVersion"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc446eb86aef3accb4ece8da19d3cc7d968016c59a3dbdd5136d68915d388c7e)
            check_type(argname="argument automatic", value=automatic, expected_type=type_hints["automatic"])
            check_type(argname="argument config_rule_name", value=config_rule_name, expected_type=type_hints["config_rule_name"])
            check_type(argname="argument execution_controls", value=execution_controls, expected_type=type_hints["execution_controls"])
            check_type(argname="argument maximum_automatic_attempts", value=maximum_automatic_attempts, expected_type=type_hints["maximum_automatic_attempts"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument retry_attempt_seconds", value=retry_attempt_seconds, expected_type=type_hints["retry_attempt_seconds"])
            check_type(argname="argument target_id", value=target_id, expected_type=type_hints["target_id"])
            check_type(argname="argument target_type", value=target_type, expected_type=type_hints["target_type"])
            check_type(argname="argument target_version", value=target_version, expected_type=type_hints["target_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if automatic is not None:
            self._values["automatic"] = automatic
        if config_rule_name is not None:
            self._values["config_rule_name"] = config_rule_name
        if execution_controls is not None:
            self._values["execution_controls"] = execution_controls
        if maximum_automatic_attempts is not None:
            self._values["maximum_automatic_attempts"] = maximum_automatic_attempts
        if parameters is not None:
            self._values["parameters"] = parameters
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if retry_attempt_seconds is not None:
            self._values["retry_attempt_seconds"] = retry_attempt_seconds
        if target_id is not None:
            self._values["target_id"] = target_id
        if target_type is not None:
            self._values["target_type"] = target_type
        if target_version is not None:
            self._values["target_version"] = target_version

    @builtins.property
    def automatic(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''The remediation is triggered automatically.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-automatic
        '''
        result = self._values.get("automatic")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def config_rule_name(self) -> typing.Optional[builtins.str]:
        '''The name of the AWS Config rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-configrulename
        '''
        result = self._values.get("config_rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_controls(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRemediationConfigurationPropsMixin.ExecutionControlsProperty"]]:
        '''An ExecutionControls object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-executioncontrols
        '''
        result = self._values.get("execution_controls")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRemediationConfigurationPropsMixin.ExecutionControlsProperty"]], result)

    @builtins.property
    def maximum_automatic_attempts(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of failed attempts for auto-remediation. If you do not select a number, the default is 5.

        For example, if you specify MaximumAutomaticAttempts as 5 with RetryAttemptSeconds as 50 seconds, AWS Config will put a RemediationException on your behalf for the failing resource after the 5th failed attempt within 50 seconds.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-maximumautomaticattempts
        '''
        result = self._values.get("maximum_automatic_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''An object of the RemediationParameterValue. For more information, see `RemediationParameterValue <https://docs.aws.amazon.com/config/latest/APIReference/API_RemediationParameterValue.html>`_ .

        .. epigraph::

           The type is a map of strings to RemediationParameterValue.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''The type of a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-resourcetype
        '''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retry_attempt_seconds(self) -> typing.Optional[jsii.Number]:
        '''Time window to determine whether or not to add a remediation exception to prevent infinite remediation attempts.

        If ``MaximumAutomaticAttempts`` remediation attempts have been made under ``RetryAttemptSeconds`` , a remediation exception will be added to the resource. If you do not select a number, the default is 60 seconds.

        For example, if you specify ``RetryAttemptSeconds`` as 50 seconds and ``MaximumAutomaticAttempts`` as 5, AWS Config will run auto-remediations 5 times within 50 seconds before adding a remediation exception to the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-retryattemptseconds
        '''
        result = self._values.get("retry_attempt_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_id(self) -> typing.Optional[builtins.str]:
        '''Target ID is the name of the SSM document.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-targetid
        '''
        result = self._values.get("target_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_type(self) -> typing.Optional[builtins.str]:
        '''The type of the target.

        Target executes remediation. For example, SSM document.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-targettype
        '''
        result = self._values.get("target_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_version(self) -> typing.Optional[builtins.str]:
        '''Version of the target. For example, version of the SSM document.

        .. epigraph::

           If you make backward incompatible changes to the SSM document, you must call PutRemediationConfiguration API again to ensure the remediations can run.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html#cfn-config-remediationconfiguration-targetversion
        '''
        result = self._values.get("target_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRemediationConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRemediationConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnRemediationConfigurationPropsMixin",
):
    '''An object that represents the details about the remediation configuration that includes the remediation action, parameters, and data to execute the action.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html
    :cloudformationResource: AWS::Config::RemediationConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
        
        # parameters: Any
        
        cfn_remediation_configuration_props_mixin = config_mixins.CfnRemediationConfigurationPropsMixin(config_mixins.CfnRemediationConfigurationMixinProps(
            automatic=False,
            config_rule_name="configRuleName",
            execution_controls=config_mixins.CfnRemediationConfigurationPropsMixin.ExecutionControlsProperty(
                ssm_controls=config_mixins.CfnRemediationConfigurationPropsMixin.SsmControlsProperty(
                    concurrent_execution_rate_percentage=123,
                    error_percentage=123
                )
            ),
            maximum_automatic_attempts=123,
            parameters=parameters,
            resource_type="resourceType",
            retry_attempt_seconds=123,
            target_id="targetId",
            target_type="targetType",
            target_version="targetVersion"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRemediationConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Config::RemediationConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff22ea5eb6429e634b830633d276f83ece896b6d5c18d0e8f9ea7e647d8acc5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__127311a252c5e5192738cdddf41c5924476b8778edac6af4e80e277161c3cc74)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03796608801e9ed63ffb2a304e0f6be27d7a7cc73c80e13aada04cdf5b33501f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRemediationConfigurationMixinProps:
        return typing.cast(CfnRemediationConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnRemediationConfigurationPropsMixin.ExecutionControlsProperty",
        jsii_struct_bases=[],
        name_mapping={"ssm_controls": "ssmControls"},
    )
    class ExecutionControlsProperty:
        def __init__(
            self,
            *,
            ssm_controls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRemediationConfigurationPropsMixin.SsmControlsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An ExecutionControls object.

            :param ssm_controls: A SsmControls object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-executioncontrols.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                execution_controls_property = config_mixins.CfnRemediationConfigurationPropsMixin.ExecutionControlsProperty(
                    ssm_controls=config_mixins.CfnRemediationConfigurationPropsMixin.SsmControlsProperty(
                        concurrent_execution_rate_percentage=123,
                        error_percentage=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a7be56e536ed416a4d20664ed7d4ead07827baee3dc426f7bdc789d7a8feb9a7)
                check_type(argname="argument ssm_controls", value=ssm_controls, expected_type=type_hints["ssm_controls"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ssm_controls is not None:
                self._values["ssm_controls"] = ssm_controls

        @builtins.property
        def ssm_controls(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRemediationConfigurationPropsMixin.SsmControlsProperty"]]:
            '''A SsmControls object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-executioncontrols.html#cfn-config-remediationconfiguration-executioncontrols-ssmcontrols
            '''
            result = self._values.get("ssm_controls")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRemediationConfigurationPropsMixin.SsmControlsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExecutionControlsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnRemediationConfigurationPropsMixin.RemediationParameterValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "resource_value": "resourceValue",
            "static_value": "staticValue",
        },
    )
    class RemediationParameterValueProperty:
        def __init__(
            self,
            *,
            resource_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRemediationConfigurationPropsMixin.ResourceValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            static_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRemediationConfigurationPropsMixin.StaticValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The value is either a dynamic (resource) value or a static value.

            You must select either a dynamic value or a static value.

            :param resource_value: The value is dynamic and changes at run-time.
            :param static_value: The value is static and does not change at run-time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-remediationparametervalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                remediation_parameter_value_property = config_mixins.CfnRemediationConfigurationPropsMixin.RemediationParameterValueProperty(
                    resource_value=config_mixins.CfnRemediationConfigurationPropsMixin.ResourceValueProperty(
                        value="value"
                    ),
                    static_value=config_mixins.CfnRemediationConfigurationPropsMixin.StaticValueProperty(
                        value=["value"],
                        values=["values"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__21d967d450525639f90ca40adde3cb9fb342eab5e3e86989a66366ab2d7f40ec)
                check_type(argname="argument resource_value", value=resource_value, expected_type=type_hints["resource_value"])
                check_type(argname="argument static_value", value=static_value, expected_type=type_hints["static_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_value is not None:
                self._values["resource_value"] = resource_value
            if static_value is not None:
                self._values["static_value"] = static_value

        @builtins.property
        def resource_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRemediationConfigurationPropsMixin.ResourceValueProperty"]]:
            '''The value is dynamic and changes at run-time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-remediationparametervalue.html#cfn-config-remediationconfiguration-remediationparametervalue-resourcevalue
            '''
            result = self._values.get("resource_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRemediationConfigurationPropsMixin.ResourceValueProperty"]], result)

        @builtins.property
        def static_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRemediationConfigurationPropsMixin.StaticValueProperty"]]:
            '''The value is static and does not change at run-time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-remediationparametervalue.html#cfn-config-remediationconfiguration-remediationparametervalue-staticvalue
            '''
            result = self._values.get("static_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRemediationConfigurationPropsMixin.StaticValueProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RemediationParameterValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnRemediationConfigurationPropsMixin.ResourceValueProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class ResourceValueProperty:
        def __init__(self, *, value: typing.Optional[builtins.str] = None) -> None:
            '''
            :param value: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-resourcevalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                resource_value_property = config_mixins.CfnRemediationConfigurationPropsMixin.ResourceValueProperty(
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d7d408c52b9e8ecdbea582fb460665bfb81dfa3152ee3e8e08eb05ffd5d3c767)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-resourcevalue.html#cfn-config-remediationconfiguration-resourcevalue-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnRemediationConfigurationPropsMixin.SsmControlsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "concurrent_execution_rate_percentage": "concurrentExecutionRatePercentage",
            "error_percentage": "errorPercentage",
        },
    )
    class SsmControlsProperty:
        def __init__(
            self,
            *,
            concurrent_execution_rate_percentage: typing.Optional[jsii.Number] = None,
            error_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''AWS Systems Manager (SSM) specific remediation controls.

            :param concurrent_execution_rate_percentage: The maximum percentage of remediation actions allowed to run in parallel on the non-compliant resources for that specific rule. You can specify a percentage, such as 10%. The default value is 10.
            :param error_percentage: The percentage of errors that are allowed before SSM stops running automations on non-compliant resources for that specific rule. You can specify a percentage of errors, for example 10%. If you do not specifiy a percentage, the default is 50%. For example, if you set the ErrorPercentage to 40% for 10 non-compliant resources, then SSM stops running the automations when the fifth error is received.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-ssmcontrols.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                ssm_controls_property = config_mixins.CfnRemediationConfigurationPropsMixin.SsmControlsProperty(
                    concurrent_execution_rate_percentage=123,
                    error_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9c17a290c113c04210a31996aeb4500d2127a97f5faf7fddd375bb96eace7ffa)
                check_type(argname="argument concurrent_execution_rate_percentage", value=concurrent_execution_rate_percentage, expected_type=type_hints["concurrent_execution_rate_percentage"])
                check_type(argname="argument error_percentage", value=error_percentage, expected_type=type_hints["error_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if concurrent_execution_rate_percentage is not None:
                self._values["concurrent_execution_rate_percentage"] = concurrent_execution_rate_percentage
            if error_percentage is not None:
                self._values["error_percentage"] = error_percentage

        @builtins.property
        def concurrent_execution_rate_percentage(self) -> typing.Optional[jsii.Number]:
            '''The maximum percentage of remediation actions allowed to run in parallel on the non-compliant resources for that specific rule.

            You can specify a percentage, such as 10%. The default value is 10.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-ssmcontrols.html#cfn-config-remediationconfiguration-ssmcontrols-concurrentexecutionratepercentage
            '''
            result = self._values.get("concurrent_execution_rate_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def error_percentage(self) -> typing.Optional[jsii.Number]:
            '''The percentage of errors that are allowed before SSM stops running automations on non-compliant resources for that specific rule.

            You can specify a percentage of errors, for example 10%. If you do not specifiy a percentage, the default is 50%. For example, if you set the ErrorPercentage to 40% for 10 non-compliant resources, then SSM stops running the automations when the fifth error is received.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-ssmcontrols.html#cfn-config-remediationconfiguration-ssmcontrols-errorpercentage
            '''
            result = self._values.get("error_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SsmControlsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnRemediationConfigurationPropsMixin.StaticValueProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value", "values": "values"},
    )
    class StaticValueProperty:
        def __init__(
            self,
            *,
            value: typing.Optional[typing.Sequence[builtins.str]] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param value: 
            :param values: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-staticvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
                
                static_value_property = config_mixins.CfnRemediationConfigurationPropsMixin.StaticValueProperty(
                    value=["value"],
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b14e9e2245fd18773919d5b1f9f9a927c1593db40e1d9e20d2adac370dd3affc)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if value is not None:
                self._values["value"] = value
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def value(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-staticvalue.html#cfn-config-remediationconfiguration-staticvalue-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-remediationconfiguration-staticvalue.html#cfn-config-remediationconfiguration-staticvalue-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StaticValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnStoredQueryMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "query_description": "queryDescription",
        "query_expression": "queryExpression",
        "query_name": "queryName",
        "tags": "tags",
    },
)
class CfnStoredQueryMixinProps:
    def __init__(
        self,
        *,
        query_description: typing.Optional[builtins.str] = None,
        query_expression: typing.Optional[builtins.str] = None,
        query_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnStoredQueryPropsMixin.

        :param query_description: A unique description for the query.
        :param query_expression: The expression of the query. For example, ``SELECT resourceId, resourceType, supplementaryConfiguration.BucketVersioningConfiguration.status WHERE resourceType = 'AWS::S3::Bucket' AND supplementaryConfiguration.BucketVersioningConfiguration.status = 'Off'.``
        :param query_name: The name of the query.
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-storedquery.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
            
            cfn_stored_query_mixin_props = config_mixins.CfnStoredQueryMixinProps(
                query_description="queryDescription",
                query_expression="queryExpression",
                query_name="queryName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__565cbc75e0b6bae4bcfbfb8da02f19fc7472ca7ec98b50f25ace9ec19224f042)
            check_type(argname="argument query_description", value=query_description, expected_type=type_hints["query_description"])
            check_type(argname="argument query_expression", value=query_expression, expected_type=type_hints["query_expression"])
            check_type(argname="argument query_name", value=query_name, expected_type=type_hints["query_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if query_description is not None:
            self._values["query_description"] = query_description
        if query_expression is not None:
            self._values["query_expression"] = query_expression
        if query_name is not None:
            self._values["query_name"] = query_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def query_description(self) -> typing.Optional[builtins.str]:
        '''A unique description for the query.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-storedquery.html#cfn-config-storedquery-querydescription
        '''
        result = self._values.get("query_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_expression(self) -> typing.Optional[builtins.str]:
        '''The expression of the query.

        For example, ``SELECT resourceId, resourceType, supplementaryConfiguration.BucketVersioningConfiguration.status WHERE resourceType = 'AWS::S3::Bucket' AND supplementaryConfiguration.BucketVersioningConfiguration.status = 'Off'.``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-storedquery.html#cfn-config-storedquery-queryexpression
        '''
        result = self._values.get("query_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_name(self) -> typing.Optional[builtins.str]:
        '''The name of the query.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-storedquery.html#cfn-config-storedquery-queryname
        '''
        result = self._values.get("query_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-storedquery.html#cfn-config-storedquery-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStoredQueryMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStoredQueryPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_config.mixins.CfnStoredQueryPropsMixin",
):
    '''Provides the details of a stored query.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-storedquery.html
    :cloudformationResource: AWS::Config::StoredQuery
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_config import mixins as config_mixins
        
        cfn_stored_query_props_mixin = config_mixins.CfnStoredQueryPropsMixin(config_mixins.CfnStoredQueryMixinProps(
            query_description="queryDescription",
            query_expression="queryExpression",
            query_name="queryName",
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
        props: typing.Union[CfnStoredQueryMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Config::StoredQuery``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__913678532afe2639928d78e095d73081b88df4a03f4840a5dabf5987c7c99265)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c149df98518a28be56a73ed5b11e57360caf63d49b0cadf0ef9a2f5f1cb3e37)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9429501fc56ebd877664dde7eeb282e46c0aa45c08c91a164f671ac3fc6ae1cf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStoredQueryMixinProps:
        return typing.cast(CfnStoredQueryMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnAggregationAuthorizationMixinProps",
    "CfnAggregationAuthorizationPropsMixin",
    "CfnConfigRuleMixinProps",
    "CfnConfigRulePropsMixin",
    "CfnConfigurationAggregatorMixinProps",
    "CfnConfigurationAggregatorPropsMixin",
    "CfnConfigurationRecorderMixinProps",
    "CfnConfigurationRecorderPropsMixin",
    "CfnConformancePackMixinProps",
    "CfnConformancePackPropsMixin",
    "CfnDeliveryChannelMixinProps",
    "CfnDeliveryChannelPropsMixin",
    "CfnOrganizationConfigRuleMixinProps",
    "CfnOrganizationConfigRulePropsMixin",
    "CfnOrganizationConformancePackMixinProps",
    "CfnOrganizationConformancePackPropsMixin",
    "CfnRemediationConfigurationMixinProps",
    "CfnRemediationConfigurationPropsMixin",
    "CfnStoredQueryMixinProps",
    "CfnStoredQueryPropsMixin",
]

publication.publish()

def _typecheckingstub__cbf7de0329f059c0ee5e7430e91c5a8c69a393b9cfd1324d50aa3f1c97a244e4(
    *,
    authorized_account_id: typing.Optional[builtins.str] = None,
    authorized_aws_region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10565420414adff209b91d0ec585b0bc7de0155bb61c877b6d698d6df44b706(
    props: typing.Union[CfnAggregationAuthorizationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69d51d1d3a2afbdc2af3c88ee522b16c864bdfef43fb9a216673ea6b0735c25(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028dda4cabbc5f3ec993afd0d1af8eac8084e2d30489826950acb45847850cc2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96254716dfc4c7c2ffdf382a40ede98329eee4dd28b72533de300fe1b9debd09(
    *,
    compliance: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigRulePropsMixin.ComplianceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    config_rule_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    evaluation_modes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigRulePropsMixin.EvaluationModeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    input_parameters: typing.Any = None,
    maximum_execution_frequency: typing.Optional[builtins.str] = None,
    scope: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigRulePropsMixin.ScopeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigRulePropsMixin.SourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c04eb612ba7243700149422e94a28626e30f0324b4dd33a04ee70977eefda1f(
    props: typing.Union[CfnConfigRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad0cdbc649ee2d926cddaf66b61c0297162ed760abdf934a2b4922a80f1e723(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a08cda2de5407d414779e81ec194f6567c4867a090a8952ca6c633de999319(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__942655d2e7090afa7864f1ce7b83a290185487d6e4f4e2891680c6c4cb10d3f6(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6985fc4a6494e2bf5d1d159054d9898c47008aeeeca538e2ef4d4eb19359f0ad(
    *,
    enable_debug_log_delivery: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    policy_runtime: typing.Optional[builtins.str] = None,
    policy_text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171dd3b9d615a78cadfa9495d42b1f66498acbccf027cddbf1af32ee7f63d04e(
    *,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e1fa2712a72994ace57e3a583076c58fcfefd0b1a19722987ab4f137065828(
    *,
    compliance_resource_id: typing.Optional[builtins.str] = None,
    compliance_resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a25ab91915725cee35e3082b4bfba298141a156b3199408b7315f77d7ba3e87f(
    *,
    event_source: typing.Optional[builtins.str] = None,
    maximum_execution_frequency: typing.Optional[builtins.str] = None,
    message_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e13f77c9cc5081c54dc4b29bf02dd1e56062ab06ef219148e0a87d0d35188ab7(
    *,
    custom_policy_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigRulePropsMixin.CustomPolicyDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    owner: typing.Optional[builtins.str] = None,
    source_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigRulePropsMixin.SourceDetailProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    source_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0381f19f39525ff3a932ec25afc47652e45308ad8a07a797e3fc74aa8eb317c(
    *,
    account_aggregation_sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationAggregatorPropsMixin.AccountAggregationSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    configuration_aggregator_name: typing.Optional[builtins.str] = None,
    organization_aggregation_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationAggregatorPropsMixin.OrganizationAggregationSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c71a3eeae8bb1b428f5a41fd3d615c8958c9bc9da0a4211beb45d2d69635aa(
    props: typing.Union[CfnConfigurationAggregatorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83dc801e229b2a30fa7b3c2fded0d84305176c6ba038f295c1e9408007e20cc9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d49662de6cb1d93c298c704aec9f6be9ff14e2c087f74e752a838e46b57f64b5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__982f70e15b26c35d548bb09482d4c9f010a7763be3aa0ac42a008594ef732dfa(
    *,
    account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    all_aws_regions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ffaba91f122a12bf9cdabdc4a50595d22f75f5bf9466c23e01b53910376c9bb(
    *,
    all_aws_regions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da3e650909252ee7badd1d153a9c8bb8be2c6125c266398da94410eb48439d4(
    *,
    name: typing.Optional[builtins.str] = None,
    recording_group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationRecorderPropsMixin.RecordingGroupProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    recording_mode: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationRecorderPropsMixin.RecordingModeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__219c3f861c0cd4cc17f82ec1a5cf3a0e84894fbbe11507f18e3f6b8591fec990(
    props: typing.Union[CfnConfigurationRecorderMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a68941b4b53c7b6783110d704b2d5b00b936b5d04958ac81fb9711ab6c3991c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cc729bc4fdb06fff057a3fd98a12b3d227e4bfb4652d659bc46e61018fd0984(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7a67fbac2c9b50c32be49998332ad7ae51631546058cfbc8ce060e050aae81(
    *,
    resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27106b46ac4f7b2c70d9d63635ec89e3e5f81eddc6a87529e600dc3ec9922964(
    *,
    all_supported: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    exclusion_by_resource_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationRecorderPropsMixin.ExclusionByResourceTypesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    include_global_resource_types: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    recording_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationRecorderPropsMixin.RecordingStrategyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48dee59e25d6cebe211fa945acbfacb206a8f0f97b7c124bbd35039b444ec561(
    *,
    description: typing.Optional[builtins.str] = None,
    recording_frequency: typing.Optional[builtins.str] = None,
    resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f007638a2c68499f55be10916c861d32d1245b5d680986dd54bb03250f9ddc7e(
    *,
    recording_frequency: typing.Optional[builtins.str] = None,
    recording_mode_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationRecorderPropsMixin.RecordingModeOverrideProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f96de9412d46cc852fa90db63fe9fc49a2c0fde09029fef0e195e3dd3caec1b5(
    *,
    use_only: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fb9f6ef9d5eecaa89815597a470365902805bc9c6432fcd44a3e508d0d37112(
    *,
    conformance_pack_input_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConformancePackPropsMixin.ConformancePackInputParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    conformance_pack_name: typing.Optional[builtins.str] = None,
    delivery_s3_bucket: typing.Optional[builtins.str] = None,
    delivery_s3_key_prefix: typing.Optional[builtins.str] = None,
    template_body: typing.Optional[builtins.str] = None,
    template_s3_uri: typing.Optional[builtins.str] = None,
    template_ssm_document_details: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb044d7d257af531883568bc635254d9a8e7d80db77f425670a0bdc2f5ef3be4(
    props: typing.Union[CfnConformancePackMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f0a1ca960223c5b9794b247313cfc5beb253134a7ddc5076436060d31f6fc8d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd71e4f6459fea8599f040ecbc595b14b1ac9843d36144d762b170bbd3cd21c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1fc3d0b95b6aab3f3ecc407d8a4306a816e6d1b4516c9282ede4df458d335e(
    *,
    parameter_name: typing.Optional[builtins.str] = None,
    parameter_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3885c83ef78db2a39d791a66e7c9597c947cdb179b1a076c739bb106741f4b(
    *,
    document_name: typing.Optional[builtins.str] = None,
    document_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee83557e421fe53984a72b9f220e86b12e480c8e317c2c9fda593d85e691a95(
    *,
    config_snapshot_delivery_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryChannelPropsMixin.ConfigSnapshotDeliveryPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    s3_bucket_name: typing.Optional[builtins.str] = None,
    s3_key_prefix: typing.Optional[builtins.str] = None,
    s3_kms_key_arn: typing.Optional[builtins.str] = None,
    sns_topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a97a1539b5f2f5775063a4bbad348812127bb15baf1f394f189efaa3e700e01b(
    props: typing.Union[CfnDeliveryChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8414b09aa63d890b109dd74c7a521710af612ae905b6d0044aef322d3d915644(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b96aac7dffa5fe7ebb2a721eba0ef11280402ee07c543566e5e88f457712b0f2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63dd428f004388c1078c41d0dee2b39fbd9aa129b4ae9de897f1ed0577491e6d(
    *,
    delivery_frequency: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f6a3761525560a19d757059100c12a59824a57d8036a27f27411a5143b3ccbf(
    *,
    excluded_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    organization_config_rule_name: typing.Optional[builtins.str] = None,
    organization_custom_policy_rule_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOrganizationConfigRulePropsMixin.OrganizationCustomPolicyRuleMetadataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    organization_custom_rule_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOrganizationConfigRulePropsMixin.OrganizationCustomRuleMetadataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    organization_managed_rule_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOrganizationConfigRulePropsMixin.OrganizationManagedRuleMetadataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c15695996c8070fb29dc227440159e0aa4de702c1864379bc523b0024d1da40(
    props: typing.Union[CfnOrganizationConfigRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab87ba3514fd65504344ef6ccef9deb6d40b1cd4274ad58509a3e2b2495185bb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c2380eb7149f0a7ee4c5ce1c7268fac69c379a45dc55026bc79349df061ff5a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88ff11641d26c5e240dfade391c6b18d677a6078b60fede222c0cb22435b5121(
    *,
    debug_log_delivery_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    input_parameters: typing.Optional[builtins.str] = None,
    maximum_execution_frequency: typing.Optional[builtins.str] = None,
    organization_config_rule_trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    policy_text: typing.Optional[builtins.str] = None,
    resource_id_scope: typing.Optional[builtins.str] = None,
    resource_types_scope: typing.Optional[typing.Sequence[builtins.str]] = None,
    runtime: typing.Optional[builtins.str] = None,
    tag_key_scope: typing.Optional[builtins.str] = None,
    tag_value_scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ccaa5b324031de41fd89447ed356de726c38aa567da9702bb64c9a6c172f16(
    *,
    description: typing.Optional[builtins.str] = None,
    input_parameters: typing.Optional[builtins.str] = None,
    lambda_function_arn: typing.Optional[builtins.str] = None,
    maximum_execution_frequency: typing.Optional[builtins.str] = None,
    organization_config_rule_trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_id_scope: typing.Optional[builtins.str] = None,
    resource_types_scope: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_key_scope: typing.Optional[builtins.str] = None,
    tag_value_scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f59685a3c0265e0cbfd3929ad629d84f9bd01df52f06c13fe11b2cf3441dd212(
    *,
    description: typing.Optional[builtins.str] = None,
    input_parameters: typing.Optional[builtins.str] = None,
    maximum_execution_frequency: typing.Optional[builtins.str] = None,
    resource_id_scope: typing.Optional[builtins.str] = None,
    resource_types_scope: typing.Optional[typing.Sequence[builtins.str]] = None,
    rule_identifier: typing.Optional[builtins.str] = None,
    tag_key_scope: typing.Optional[builtins.str] = None,
    tag_value_scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67af5ee0ec84ebb73383fef5539313ec9f424903a938bd791b267cd3578e1fe4(
    *,
    conformance_pack_input_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOrganizationConformancePackPropsMixin.ConformancePackInputParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    delivery_s3_bucket: typing.Optional[builtins.str] = None,
    delivery_s3_key_prefix: typing.Optional[builtins.str] = None,
    excluded_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    organization_conformance_pack_name: typing.Optional[builtins.str] = None,
    template_body: typing.Optional[builtins.str] = None,
    template_s3_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__748f09781f965ba393be6c08be4f1bed65c7dd82ca64f31be5ec201dfde0ce1a(
    props: typing.Union[CfnOrganizationConformancePackMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c6d7c669d20f00486b974a801d9ca5c4e41d6af4ef5ff7cc1b86f6f541074b7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df8d744751f9e2bc20141f8c0a1a2992e3c1a111f430dedbcd908af03d4c484f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a7852ac3130258fa5689c3a70cc9b809e040a04c6b30f7563937184b299812(
    *,
    parameter_name: typing.Optional[builtins.str] = None,
    parameter_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc446eb86aef3accb4ece8da19d3cc7d968016c59a3dbdd5136d68915d388c7e(
    *,
    automatic: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    config_rule_name: typing.Optional[builtins.str] = None,
    execution_controls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRemediationConfigurationPropsMixin.ExecutionControlsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maximum_automatic_attempts: typing.Optional[jsii.Number] = None,
    parameters: typing.Any = None,
    resource_type: typing.Optional[builtins.str] = None,
    retry_attempt_seconds: typing.Optional[jsii.Number] = None,
    target_id: typing.Optional[builtins.str] = None,
    target_type: typing.Optional[builtins.str] = None,
    target_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff22ea5eb6429e634b830633d276f83ece896b6d5c18d0e8f9ea7e647d8acc5(
    props: typing.Union[CfnRemediationConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__127311a252c5e5192738cdddf41c5924476b8778edac6af4e80e277161c3cc74(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03796608801e9ed63ffb2a304e0f6be27d7a7cc73c80e13aada04cdf5b33501f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7be56e536ed416a4d20664ed7d4ead07827baee3dc426f7bdc789d7a8feb9a7(
    *,
    ssm_controls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRemediationConfigurationPropsMixin.SsmControlsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21d967d450525639f90ca40adde3cb9fb342eab5e3e86989a66366ab2d7f40ec(
    *,
    resource_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRemediationConfigurationPropsMixin.ResourceValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    static_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRemediationConfigurationPropsMixin.StaticValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7d408c52b9e8ecdbea582fb460665bfb81dfa3152ee3e8e08eb05ffd5d3c767(
    *,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c17a290c113c04210a31996aeb4500d2127a97f5faf7fddd375bb96eace7ffa(
    *,
    concurrent_execution_rate_percentage: typing.Optional[jsii.Number] = None,
    error_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14e9e2245fd18773919d5b1f9f9a927c1593db40e1d9e20d2adac370dd3affc(
    *,
    value: typing.Optional[typing.Sequence[builtins.str]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__565cbc75e0b6bae4bcfbfb8da02f19fc7472ca7ec98b50f25ace9ec19224f042(
    *,
    query_description: typing.Optional[builtins.str] = None,
    query_expression: typing.Optional[builtins.str] = None,
    query_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__913678532afe2639928d78e095d73081b88df4a03f4840a5dabf5987c7c99265(
    props: typing.Union[CfnStoredQueryMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c149df98518a28be56a73ed5b11e57360caf63d49b0cadf0ef9a2f5f1cb3e37(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9429501fc56ebd877664dde7eeb282e46c0aa45c08c91a164f671ac3fc6ae1cf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
