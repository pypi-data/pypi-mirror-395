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
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAggregatorV2MixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "linked_regions": "linkedRegions",
        "region_linking_mode": "regionLinkingMode",
        "tags": "tags",
    },
)
class CfnAggregatorV2MixinProps:
    def __init__(
        self,
        *,
        linked_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        region_linking_mode: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnAggregatorV2PropsMixin.

        :param linked_regions: The list of Regions that are linked to the aggregation Region.
        :param region_linking_mode: Determines how Regions are linked to an Aggregator V2.
        :param tags: A list of key-value pairs to be applied to the AggregatorV2.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-aggregatorv2.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
            
            cfn_aggregator_v2_mixin_props = securityhub_mixins.CfnAggregatorV2MixinProps(
                linked_regions=["linkedRegions"],
                region_linking_mode="regionLinkingMode",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94a0be53248e71505756e873712b092f8245a8ee330ec1d0f3d45f835de94e65)
            check_type(argname="argument linked_regions", value=linked_regions, expected_type=type_hints["linked_regions"])
            check_type(argname="argument region_linking_mode", value=region_linking_mode, expected_type=type_hints["region_linking_mode"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if linked_regions is not None:
            self._values["linked_regions"] = linked_regions
        if region_linking_mode is not None:
            self._values["region_linking_mode"] = region_linking_mode
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def linked_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of Regions that are linked to the aggregation Region.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-aggregatorv2.html#cfn-securityhub-aggregatorv2-linkedregions
        '''
        result = self._values.get("linked_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def region_linking_mode(self) -> typing.Optional[builtins.str]:
        '''Determines how Regions are linked to an Aggregator V2.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-aggregatorv2.html#cfn-securityhub-aggregatorv2-regionlinkingmode
        '''
        result = self._values.get("region_linking_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A list of key-value pairs to be applied to the AggregatorV2.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-aggregatorv2.html#cfn-securityhub-aggregatorv2-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAggregatorV2MixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAggregatorV2PropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAggregatorV2PropsMixin",
):
    '''Enables aggregation across AWS Regions .

    This API is in public preview and subject to change.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-aggregatorv2.html
    :cloudformationResource: AWS::SecurityHub::AggregatorV2
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
        
        cfn_aggregator_v2_props_mixin = securityhub_mixins.CfnAggregatorV2PropsMixin(securityhub_mixins.CfnAggregatorV2MixinProps(
            linked_regions=["linkedRegions"],
            region_linking_mode="regionLinkingMode",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAggregatorV2MixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecurityHub::AggregatorV2``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__787e8b8e0c660635784e53469a8f18424e99616ae5d978f19b7a41f73a9e7da2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89b2fdd2580683bc5efbbdf48eee650b494ce24eb35ea15873beac6fd51ca8d6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5173e7e30309ba7ec3a2a6730cc669ee64c39c8d47c8ac56e248c21c7f86fc3a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAggregatorV2MixinProps:
        return typing.cast(CfnAggregatorV2MixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "criteria": "criteria",
        "description": "description",
        "is_terminal": "isTerminal",
        "rule_name": "ruleName",
        "rule_order": "ruleOrder",
        "rule_status": "ruleStatus",
        "tags": "tags",
    },
)
class CfnAutomationRuleMixinProps:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.AutomationRulesActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.AutomationRulesFindingFiltersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        is_terminal: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        rule_order: typing.Optional[jsii.Number] = None,
        rule_status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnAutomationRulePropsMixin.

        :param actions: One or more actions to update finding fields if a finding matches the conditions specified in ``Criteria`` .
        :param criteria: A set of `AWS Security Finding Format (ASFF) <https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-findings-format.html>`_ finding field attributes and corresponding expected values that Security Hub uses to filter findings. If a rule is enabled and a finding matches the criteria specified in this parameter, Security Hub applies the rule action to the finding.
        :param description: A description of the rule.
        :param is_terminal: Specifies whether a rule is the last to be applied with respect to a finding that matches the rule criteria. This is useful when a finding matches the criteria for multiple rules, and each rule has different actions. If a rule is terminal, Security Hub applies the rule action to a finding that matches the rule criteria and doesn't evaluate other rules for the finding. By default, a rule isn't terminal.
        :param rule_name: The name of the rule.
        :param rule_order: An integer ranging from 1 to 1000 that represents the order in which the rule action is applied to findings. Security Hub applies rules with lower values for this parameter first.
        :param rule_status: Whether the rule is active after it is created. If this parameter is equal to ``ENABLED`` , Security Hub applies the rule to findings and finding updates after the rule is created.
        :param tags: User-defined tags associated with an automation rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-automationrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
            
            cfn_automation_rule_mixin_props = securityhub_mixins.CfnAutomationRuleMixinProps(
                actions=[securityhub_mixins.CfnAutomationRulePropsMixin.AutomationRulesActionProperty(
                    finding_fields_update=securityhub_mixins.CfnAutomationRulePropsMixin.AutomationRulesFindingFieldsUpdateProperty(
                        confidence=123,
                        criticality=123,
                        note=securityhub_mixins.CfnAutomationRulePropsMixin.NoteUpdateProperty(
                            text="text",
                            updated_by="updatedBy"
                        ),
                        related_findings=[securityhub_mixins.CfnAutomationRulePropsMixin.RelatedFindingProperty(
                            id="id",
                            product_arn="productArn"
                        )],
                        severity=securityhub_mixins.CfnAutomationRulePropsMixin.SeverityUpdateProperty(
                            label="label",
                            normalized=123,
                            product=123
                        ),
                        types=["types"],
                        user_defined_fields={
                            "user_defined_fields_key": "userDefinedFields"
                        },
                        verification_state="verificationState",
                        workflow=securityhub_mixins.CfnAutomationRulePropsMixin.WorkflowUpdateProperty(
                            status="status"
                        )
                    ),
                    type="type"
                )],
                criteria=securityhub_mixins.CfnAutomationRulePropsMixin.AutomationRulesFindingFiltersProperty(
                    aws_account_id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    company_name=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    compliance_associated_standards_id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    compliance_security_control_id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    compliance_status=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    confidence=[securityhub_mixins.CfnAutomationRulePropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    created_at=[securityhub_mixins.CfnAutomationRulePropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnAutomationRulePropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    criticality=[securityhub_mixins.CfnAutomationRulePropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    description=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    first_observed_at=[securityhub_mixins.CfnAutomationRulePropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnAutomationRulePropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    generator_id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    last_observed_at=[securityhub_mixins.CfnAutomationRulePropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnAutomationRulePropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    note_text=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    note_updated_at=[securityhub_mixins.CfnAutomationRulePropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnAutomationRulePropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    note_updated_by=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    product_arn=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    product_name=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    record_state=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    related_findings_id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    related_findings_product_arn=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_details_other=[securityhub_mixins.CfnAutomationRulePropsMixin.MapFilterProperty(
                        comparison="comparison",
                        key="key",
                        value="value"
                    )],
                    resource_id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_partition=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_region=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_tags=[securityhub_mixins.CfnAutomationRulePropsMixin.MapFilterProperty(
                        comparison="comparison",
                        key="key",
                        value="value"
                    )],
                    resource_type=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    severity_label=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    source_url=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    title=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    type=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    updated_at=[securityhub_mixins.CfnAutomationRulePropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnAutomationRulePropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    user_defined_fields=[securityhub_mixins.CfnAutomationRulePropsMixin.MapFilterProperty(
                        comparison="comparison",
                        key="key",
                        value="value"
                    )],
                    verification_state=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    workflow_status=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )]
                ),
                description="description",
                is_terminal=False,
                rule_name="ruleName",
                rule_order=123,
                rule_status="ruleStatus",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a70cef8f5a998ff81255474b5ecd87ae9262528abe56d7e08471607a3f3087a)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument is_terminal", value=is_terminal, expected_type=type_hints["is_terminal"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument rule_order", value=rule_order, expected_type=type_hints["rule_order"])
            check_type(argname="argument rule_status", value=rule_status, expected_type=type_hints["rule_status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if criteria is not None:
            self._values["criteria"] = criteria
        if description is not None:
            self._values["description"] = description
        if is_terminal is not None:
            self._values["is_terminal"] = is_terminal
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if rule_order is not None:
            self._values["rule_order"] = rule_order
        if rule_status is not None:
            self._values["rule_status"] = rule_status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def actions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.AutomationRulesActionProperty"]]]]:
        '''One or more actions to update finding fields if a finding matches the conditions specified in ``Criteria`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-automationrule.html#cfn-securityhub-automationrule-actions
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.AutomationRulesActionProperty"]]]], result)

    @builtins.property
    def criteria(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.AutomationRulesFindingFiltersProperty"]]:
        '''A set of `AWS Security Finding Format (ASFF) <https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-findings-format.html>`_ finding field attributes and corresponding expected values that Security Hub uses to filter findings. If a rule is enabled and a finding matches the criteria specified in this parameter, Security Hub applies the rule action to the finding.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-automationrule.html#cfn-securityhub-automationrule-criteria
        '''
        result = self._values.get("criteria")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.AutomationRulesFindingFiltersProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-automationrule.html#cfn-securityhub-automationrule-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_terminal(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether a rule is the last to be applied with respect to a finding that matches the rule criteria.

        This is useful when a finding matches the criteria for multiple rules, and each rule has different actions. If a rule is terminal, Security Hub applies the rule action to a finding that matches the rule criteria and doesn't evaluate other rules for the finding. By default, a rule isn't terminal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-automationrule.html#cfn-securityhub-automationrule-isterminal
        '''
        result = self._values.get("is_terminal")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''The name of the rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-automationrule.html#cfn-securityhub-automationrule-rulename
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_order(self) -> typing.Optional[jsii.Number]:
        '''An integer ranging from 1 to 1000 that represents the order in which the rule action is applied to findings.

        Security Hub applies rules with lower values for this parameter first.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-automationrule.html#cfn-securityhub-automationrule-ruleorder
        '''
        result = self._values.get("rule_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rule_status(self) -> typing.Optional[builtins.str]:
        '''Whether the rule is active after it is created.

        If this parameter is equal to ``ENABLED`` , Security Hub applies the rule to findings and finding updates after the rule is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-automationrule.html#cfn-securityhub-automationrule-rulestatus
        '''
        result = self._values.get("rule_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined tags associated with an automation rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-automationrule.html#cfn-securityhub-automationrule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAutomationRuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAutomationRulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRulePropsMixin",
):
    '''The ``AWS::SecurityHub::AutomationRule`` resource specifies an automation rule based on input parameters.

    For more information, see `Automation rules <https://docs.aws.amazon.com/securityhub/latest/userguide/automation-rules.html>`_ in the *Security Hub User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-automationrule.html
    :cloudformationResource: AWS::SecurityHub::AutomationRule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
        
        cfn_automation_rule_props_mixin = securityhub_mixins.CfnAutomationRulePropsMixin(securityhub_mixins.CfnAutomationRuleMixinProps(
            actions=[securityhub_mixins.CfnAutomationRulePropsMixin.AutomationRulesActionProperty(
                finding_fields_update=securityhub_mixins.CfnAutomationRulePropsMixin.AutomationRulesFindingFieldsUpdateProperty(
                    confidence=123,
                    criticality=123,
                    note=securityhub_mixins.CfnAutomationRulePropsMixin.NoteUpdateProperty(
                        text="text",
                        updated_by="updatedBy"
                    ),
                    related_findings=[securityhub_mixins.CfnAutomationRulePropsMixin.RelatedFindingProperty(
                        id="id",
                        product_arn="productArn"
                    )],
                    severity=securityhub_mixins.CfnAutomationRulePropsMixin.SeverityUpdateProperty(
                        label="label",
                        normalized=123,
                        product=123
                    ),
                    types=["types"],
                    user_defined_fields={
                        "user_defined_fields_key": "userDefinedFields"
                    },
                    verification_state="verificationState",
                    workflow=securityhub_mixins.CfnAutomationRulePropsMixin.WorkflowUpdateProperty(
                        status="status"
                    )
                ),
                type="type"
            )],
            criteria=securityhub_mixins.CfnAutomationRulePropsMixin.AutomationRulesFindingFiltersProperty(
                aws_account_id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                company_name=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                compliance_associated_standards_id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                compliance_security_control_id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                compliance_status=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                confidence=[securityhub_mixins.CfnAutomationRulePropsMixin.NumberFilterProperty(
                    eq=123,
                    gte=123,
                    lte=123
                )],
                created_at=[securityhub_mixins.CfnAutomationRulePropsMixin.DateFilterProperty(
                    date_range=securityhub_mixins.CfnAutomationRulePropsMixin.DateRangeProperty(
                        unit="unit",
                        value=123
                    ),
                    end="end",
                    start="start"
                )],
                criticality=[securityhub_mixins.CfnAutomationRulePropsMixin.NumberFilterProperty(
                    eq=123,
                    gte=123,
                    lte=123
                )],
                description=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                first_observed_at=[securityhub_mixins.CfnAutomationRulePropsMixin.DateFilterProperty(
                    date_range=securityhub_mixins.CfnAutomationRulePropsMixin.DateRangeProperty(
                        unit="unit",
                        value=123
                    ),
                    end="end",
                    start="start"
                )],
                generator_id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                last_observed_at=[securityhub_mixins.CfnAutomationRulePropsMixin.DateFilterProperty(
                    date_range=securityhub_mixins.CfnAutomationRulePropsMixin.DateRangeProperty(
                        unit="unit",
                        value=123
                    ),
                    end="end",
                    start="start"
                )],
                note_text=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                note_updated_at=[securityhub_mixins.CfnAutomationRulePropsMixin.DateFilterProperty(
                    date_range=securityhub_mixins.CfnAutomationRulePropsMixin.DateRangeProperty(
                        unit="unit",
                        value=123
                    ),
                    end="end",
                    start="start"
                )],
                note_updated_by=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                product_arn=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                product_name=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                record_state=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                related_findings_id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                related_findings_product_arn=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_details_other=[securityhub_mixins.CfnAutomationRulePropsMixin.MapFilterProperty(
                    comparison="comparison",
                    key="key",
                    value="value"
                )],
                resource_id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_partition=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_region=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_tags=[securityhub_mixins.CfnAutomationRulePropsMixin.MapFilterProperty(
                    comparison="comparison",
                    key="key",
                    value="value"
                )],
                resource_type=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                severity_label=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                source_url=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                title=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                type=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                updated_at=[securityhub_mixins.CfnAutomationRulePropsMixin.DateFilterProperty(
                    date_range=securityhub_mixins.CfnAutomationRulePropsMixin.DateRangeProperty(
                        unit="unit",
                        value=123
                    ),
                    end="end",
                    start="start"
                )],
                user_defined_fields=[securityhub_mixins.CfnAutomationRulePropsMixin.MapFilterProperty(
                    comparison="comparison",
                    key="key",
                    value="value"
                )],
                verification_state=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                workflow_status=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )]
            ),
            description="description",
            is_terminal=False,
            rule_name="ruleName",
            rule_order=123,
            rule_status="ruleStatus",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAutomationRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecurityHub::AutomationRule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c6748fd3a79a421df9da6fcbf09f3ca9ae5755d1006a8da6ec298b899962475)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93dd561ebd751e2dc39fcc38423895e06bb109c4f9bad51ec2e3d4827ed2b7ec)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__394061078b77abb48e8a4a1d13eb12f1b81c87aab225a608f708f254ffe3ed2a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAutomationRuleMixinProps:
        return typing.cast(CfnAutomationRuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRulePropsMixin.AutomationRulesActionProperty",
        jsii_struct_bases=[],
        name_mapping={"finding_fields_update": "findingFieldsUpdate", "type": "type"},
    )
    class AutomationRulesActionProperty:
        def __init__(
            self,
            *,
            finding_fields_update: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.AutomationRulesFindingFieldsUpdateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''One or more actions that Security Hub takes when a finding matches the defined criteria of a rule.

            :param finding_fields_update: Specifies that the automation rule action is an update to a finding field.
            :param type: Specifies the type of action that Security Hub takes when a finding matches the defined criteria of a rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                automation_rules_action_property = securityhub_mixins.CfnAutomationRulePropsMixin.AutomationRulesActionProperty(
                    finding_fields_update=securityhub_mixins.CfnAutomationRulePropsMixin.AutomationRulesFindingFieldsUpdateProperty(
                        confidence=123,
                        criticality=123,
                        note=securityhub_mixins.CfnAutomationRulePropsMixin.NoteUpdateProperty(
                            text="text",
                            updated_by="updatedBy"
                        ),
                        related_findings=[securityhub_mixins.CfnAutomationRulePropsMixin.RelatedFindingProperty(
                            id="id",
                            product_arn="productArn"
                        )],
                        severity=securityhub_mixins.CfnAutomationRulePropsMixin.SeverityUpdateProperty(
                            label="label",
                            normalized=123,
                            product=123
                        ),
                        types=["types"],
                        user_defined_fields={
                            "user_defined_fields_key": "userDefinedFields"
                        },
                        verification_state="verificationState",
                        workflow=securityhub_mixins.CfnAutomationRulePropsMixin.WorkflowUpdateProperty(
                            status="status"
                        )
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__89ce770db050ea565f4c3954a65295943e200ab82c04c708fe4b4c69e93f8765)
                check_type(argname="argument finding_fields_update", value=finding_fields_update, expected_type=type_hints["finding_fields_update"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if finding_fields_update is not None:
                self._values["finding_fields_update"] = finding_fields_update
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def finding_fields_update(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.AutomationRulesFindingFieldsUpdateProperty"]]:
            '''Specifies that the automation rule action is an update to a finding field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesaction.html#cfn-securityhub-automationrule-automationrulesaction-findingfieldsupdate
            '''
            result = self._values.get("finding_fields_update")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.AutomationRulesFindingFieldsUpdateProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of action that Security Hub takes when a finding matches the defined criteria of a rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesaction.html#cfn-securityhub-automationrule-automationrulesaction-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutomationRulesActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRulePropsMixin.AutomationRulesFindingFieldsUpdateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "confidence": "confidence",
            "criticality": "criticality",
            "note": "note",
            "related_findings": "relatedFindings",
            "severity": "severity",
            "types": "types",
            "user_defined_fields": "userDefinedFields",
            "verification_state": "verificationState",
            "workflow": "workflow",
        },
    )
    class AutomationRulesFindingFieldsUpdateProperty:
        def __init__(
            self,
            *,
            confidence: typing.Optional[jsii.Number] = None,
            criticality: typing.Optional[jsii.Number] = None,
            note: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.NoteUpdateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            related_findings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.RelatedFindingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            severity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.SeverityUpdateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            types: typing.Optional[typing.Sequence[builtins.str]] = None,
            user_defined_fields: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            verification_state: typing.Optional[builtins.str] = None,
            workflow: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.WorkflowUpdateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Identifies the finding fields that the automation rule action updates when a finding matches the defined criteria.

            :param confidence: The rule action updates the ``Confidence`` field of a finding.
            :param criticality: The rule action updates the ``Criticality`` field of a finding.
            :param note: The rule action will update the ``Note`` field of a finding.
            :param related_findings: The rule action will update the ``RelatedFindings`` field of a finding.
            :param severity: The rule action will update the ``Severity`` field of a finding.
            :param types: The rule action updates the ``Types`` field of a finding.
            :param user_defined_fields: The rule action updates the ``UserDefinedFields`` field of a finding.
            :param verification_state: The rule action updates the ``VerificationState`` field of a finding.
            :param workflow: The rule action will update the ``Workflow`` field of a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfieldsupdate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                automation_rules_finding_fields_update_property = securityhub_mixins.CfnAutomationRulePropsMixin.AutomationRulesFindingFieldsUpdateProperty(
                    confidence=123,
                    criticality=123,
                    note=securityhub_mixins.CfnAutomationRulePropsMixin.NoteUpdateProperty(
                        text="text",
                        updated_by="updatedBy"
                    ),
                    related_findings=[securityhub_mixins.CfnAutomationRulePropsMixin.RelatedFindingProperty(
                        id="id",
                        product_arn="productArn"
                    )],
                    severity=securityhub_mixins.CfnAutomationRulePropsMixin.SeverityUpdateProperty(
                        label="label",
                        normalized=123,
                        product=123
                    ),
                    types=["types"],
                    user_defined_fields={
                        "user_defined_fields_key": "userDefinedFields"
                    },
                    verification_state="verificationState",
                    workflow=securityhub_mixins.CfnAutomationRulePropsMixin.WorkflowUpdateProperty(
                        status="status"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9d9caccaffd68cfa73b75727e86e1bfd297f74176363a2ee21b154e03dfd4a64)
                check_type(argname="argument confidence", value=confidence, expected_type=type_hints["confidence"])
                check_type(argname="argument criticality", value=criticality, expected_type=type_hints["criticality"])
                check_type(argname="argument note", value=note, expected_type=type_hints["note"])
                check_type(argname="argument related_findings", value=related_findings, expected_type=type_hints["related_findings"])
                check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
                check_type(argname="argument types", value=types, expected_type=type_hints["types"])
                check_type(argname="argument user_defined_fields", value=user_defined_fields, expected_type=type_hints["user_defined_fields"])
                check_type(argname="argument verification_state", value=verification_state, expected_type=type_hints["verification_state"])
                check_type(argname="argument workflow", value=workflow, expected_type=type_hints["workflow"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if confidence is not None:
                self._values["confidence"] = confidence
            if criticality is not None:
                self._values["criticality"] = criticality
            if note is not None:
                self._values["note"] = note
            if related_findings is not None:
                self._values["related_findings"] = related_findings
            if severity is not None:
                self._values["severity"] = severity
            if types is not None:
                self._values["types"] = types
            if user_defined_fields is not None:
                self._values["user_defined_fields"] = user_defined_fields
            if verification_state is not None:
                self._values["verification_state"] = verification_state
            if workflow is not None:
                self._values["workflow"] = workflow

        @builtins.property
        def confidence(self) -> typing.Optional[jsii.Number]:
            '''The rule action updates the ``Confidence`` field of a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfieldsupdate.html#cfn-securityhub-automationrule-automationrulesfindingfieldsupdate-confidence
            '''
            result = self._values.get("confidence")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def criticality(self) -> typing.Optional[jsii.Number]:
            '''The rule action updates the ``Criticality`` field of a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfieldsupdate.html#cfn-securityhub-automationrule-automationrulesfindingfieldsupdate-criticality
            '''
            result = self._values.get("criticality")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def note(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.NoteUpdateProperty"]]:
            '''The rule action will update the ``Note`` field of a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfieldsupdate.html#cfn-securityhub-automationrule-automationrulesfindingfieldsupdate-note
            '''
            result = self._values.get("note")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.NoteUpdateProperty"]], result)

        @builtins.property
        def related_findings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.RelatedFindingProperty"]]]]:
            '''The rule action will update the ``RelatedFindings`` field of a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfieldsupdate.html#cfn-securityhub-automationrule-automationrulesfindingfieldsupdate-relatedfindings
            '''
            result = self._values.get("related_findings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.RelatedFindingProperty"]]]], result)

        @builtins.property
        def severity(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.SeverityUpdateProperty"]]:
            '''The rule action will update the ``Severity`` field of a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfieldsupdate.html#cfn-securityhub-automationrule-automationrulesfindingfieldsupdate-severity
            '''
            result = self._values.get("severity")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.SeverityUpdateProperty"]], result)

        @builtins.property
        def types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The rule action updates the ``Types`` field of a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfieldsupdate.html#cfn-securityhub-automationrule-automationrulesfindingfieldsupdate-types
            '''
            result = self._values.get("types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def user_defined_fields(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The rule action updates the ``UserDefinedFields`` field of a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfieldsupdate.html#cfn-securityhub-automationrule-automationrulesfindingfieldsupdate-userdefinedfields
            '''
            result = self._values.get("user_defined_fields")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def verification_state(self) -> typing.Optional[builtins.str]:
            '''The rule action updates the ``VerificationState`` field of a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfieldsupdate.html#cfn-securityhub-automationrule-automationrulesfindingfieldsupdate-verificationstate
            '''
            result = self._values.get("verification_state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def workflow(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.WorkflowUpdateProperty"]]:
            '''The rule action will update the ``Workflow`` field of a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfieldsupdate.html#cfn-securityhub-automationrule-automationrulesfindingfieldsupdate-workflow
            '''
            result = self._values.get("workflow")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.WorkflowUpdateProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutomationRulesFindingFieldsUpdateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRulePropsMixin.AutomationRulesFindingFiltersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_account_id": "awsAccountId",
            "company_name": "companyName",
            "compliance_associated_standards_id": "complianceAssociatedStandardsId",
            "compliance_security_control_id": "complianceSecurityControlId",
            "compliance_status": "complianceStatus",
            "confidence": "confidence",
            "created_at": "createdAt",
            "criticality": "criticality",
            "description": "description",
            "first_observed_at": "firstObservedAt",
            "generator_id": "generatorId",
            "id": "id",
            "last_observed_at": "lastObservedAt",
            "note_text": "noteText",
            "note_updated_at": "noteUpdatedAt",
            "note_updated_by": "noteUpdatedBy",
            "product_arn": "productArn",
            "product_name": "productName",
            "record_state": "recordState",
            "related_findings_id": "relatedFindingsId",
            "related_findings_product_arn": "relatedFindingsProductArn",
            "resource_details_other": "resourceDetailsOther",
            "resource_id": "resourceId",
            "resource_partition": "resourcePartition",
            "resource_region": "resourceRegion",
            "resource_tags": "resourceTags",
            "resource_type": "resourceType",
            "severity_label": "severityLabel",
            "source_url": "sourceUrl",
            "title": "title",
            "type": "type",
            "updated_at": "updatedAt",
            "user_defined_fields": "userDefinedFields",
            "verification_state": "verificationState",
            "workflow_status": "workflowStatus",
        },
    )
    class AutomationRulesFindingFiltersProperty:
        def __init__(
            self,
            *,
            aws_account_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            company_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            compliance_associated_standards_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            compliance_security_control_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            compliance_status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            confidence: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.NumberFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            created_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            criticality: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.NumberFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            description: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            first_observed_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            generator_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            last_observed_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            note_text: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            note_updated_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            note_updated_by: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            product_arn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            product_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            record_state: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            related_findings_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            related_findings_product_arn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_details_other: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.MapFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_partition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_region: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.MapFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            severity_label: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            source_url: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            title: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            updated_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            user_defined_fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.MapFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            verification_state: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            workflow_status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The criteria that determine which findings a rule applies to.

            :param aws_account_id: The AWS account ID in which a finding was generated. Array Members: Minimum number of 1 item. Maximum number of 100 items.
            :param company_name: The name of the company for the product that generated the finding. For control-based findings, the company is AWS . Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param compliance_associated_standards_id: The unique identifier of a standard in which a control is enabled. This field consists of the resource portion of the Amazon Resource Name (ARN) returned for a standard in the `DescribeStandards <https://docs.aws.amazon.com/securityhub/1.0/APIReference/API_DescribeStandards.html>`_ API response. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param compliance_security_control_id: The security control ID for which a finding was generated. Security control IDs are the same across standards. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param compliance_status: The result of a security check. This field is only used for findings generated from controls. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param confidence: The likelihood that a finding accurately identifies the behavior or issue that it was intended to identify. ``Confidence`` is scored on a 0–100 basis using a ratio scale. A value of ``0`` means 0 percent confidence, and a value of ``100`` means 100 percent confidence. For example, a data exfiltration detection based on a statistical deviation of network traffic has low confidence because an actual exfiltration hasn't been verified. For more information, see `Confidence <https://docs.aws.amazon.com/securityhub/latest/userguide/asff-top-level-attributes.html#asff-confidence>`_ in the *Security Hub User Guide* . Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param created_at: A timestamp that indicates when this finding record was created. For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ . Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param criticality: The level of importance that is assigned to the resources that are associated with a finding. ``Criticality`` is scored on a 0–100 basis, using a ratio scale that supports only full integers. A score of ``0`` means that the underlying resources have no criticality, and a score of ``100`` is reserved for the most critical resources. For more information, see `Criticality <https://docs.aws.amazon.com/securityhub/latest/userguide/asff-top-level-attributes.html#asff-criticality>`_ in the *Security Hub User Guide* . Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param description: A finding's description. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param first_observed_at: A timestamp that indicates when the potential security issue captured by a finding was first observed by the security findings product. For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ . Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param generator_id: The identifier for the solution-specific component that generated a finding. Array Members: Minimum number of 1 item. Maximum number of 100 items.
            :param id: The product-specific identifier for a finding. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param last_observed_at: A timestamp that indicates when the security findings provider most recently observed a change in the resource that is involved in the finding. For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ . Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param note_text: The text of a user-defined note that's added to a finding. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param note_updated_at: The timestamp of when the note was updated. For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ . Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param note_updated_by: The principal that created a note. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param product_arn: The Amazon Resource Name (ARN) for a third-party product that generated a finding in Security Hub. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param product_name: Provides the name of the product that generated the finding. For control-based findings, the product name is Security Hub. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param record_state: Provides the current state of a finding. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param related_findings_id: The product-generated identifier for a related finding. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param related_findings_product_arn: The ARN for the product that generated a related finding. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param resource_details_other: Custom fields and values about the resource that a finding pertains to. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param resource_id: The identifier for the given resource type. For AWS resources that are identified by Amazon Resource Names (ARNs), this is the ARN. For AWS resources that lack ARNs, this is the identifier as defined by the AWS service that created the resource. For non- AWS resources, this is a unique identifier that is associated with the resource. Array Members: Minimum number of 1 item. Maximum number of 100 items.
            :param resource_partition: The partition in which the resource that the finding pertains to is located. A partition is a group of AWS Regions . Each AWS account is scoped to one partition. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param resource_region: The AWS Region where the resource that a finding pertains to is located. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param resource_tags: A list of AWS tags associated with a resource at the time the finding was processed. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param resource_type: A finding's title. Array Members: Minimum number of 1 item. Maximum number of 100 items.
            :param severity_label: The severity value of the finding. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param source_url: Provides a URL that links to a page about the current finding in the finding product. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param title: A finding's title. Array Members: Minimum number of 1 item. Maximum number of 100 items.
            :param type: One or more finding types in the format of namespace/category/classifier that classify a finding. For a list of namespaces, classifiers, and categories, see `Types taxonomy for ASFF <https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-findings-format-type-taxonomy.html>`_ in the *Security Hub User Guide* . Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param updated_at: A timestamp that indicates when the finding record was most recently updated. For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ . Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param user_defined_fields: A list of user-defined name and value string pairs added to a finding. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param verification_state: Provides the veracity of a finding. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param workflow_status: Provides information about the status of the investigation into a finding. Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                automation_rules_finding_filters_property = securityhub_mixins.CfnAutomationRulePropsMixin.AutomationRulesFindingFiltersProperty(
                    aws_account_id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    company_name=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    compliance_associated_standards_id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    compliance_security_control_id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    compliance_status=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    confidence=[securityhub_mixins.CfnAutomationRulePropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    created_at=[securityhub_mixins.CfnAutomationRulePropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnAutomationRulePropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    criticality=[securityhub_mixins.CfnAutomationRulePropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    description=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    first_observed_at=[securityhub_mixins.CfnAutomationRulePropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnAutomationRulePropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    generator_id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    last_observed_at=[securityhub_mixins.CfnAutomationRulePropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnAutomationRulePropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    note_text=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    note_updated_at=[securityhub_mixins.CfnAutomationRulePropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnAutomationRulePropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    note_updated_by=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    product_arn=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    product_name=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    record_state=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    related_findings_id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    related_findings_product_arn=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_details_other=[securityhub_mixins.CfnAutomationRulePropsMixin.MapFilterProperty(
                        comparison="comparison",
                        key="key",
                        value="value"
                    )],
                    resource_id=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_partition=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_region=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_tags=[securityhub_mixins.CfnAutomationRulePropsMixin.MapFilterProperty(
                        comparison="comparison",
                        key="key",
                        value="value"
                    )],
                    resource_type=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    severity_label=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    source_url=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    title=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    type=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    updated_at=[securityhub_mixins.CfnAutomationRulePropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnAutomationRulePropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    user_defined_fields=[securityhub_mixins.CfnAutomationRulePropsMixin.MapFilterProperty(
                        comparison="comparison",
                        key="key",
                        value="value"
                    )],
                    verification_state=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    workflow_status=[securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8127f519a65ecfc36503e83965da3e3b1c879e797289424cddc8dbf795def5a2)
                check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
                check_type(argname="argument company_name", value=company_name, expected_type=type_hints["company_name"])
                check_type(argname="argument compliance_associated_standards_id", value=compliance_associated_standards_id, expected_type=type_hints["compliance_associated_standards_id"])
                check_type(argname="argument compliance_security_control_id", value=compliance_security_control_id, expected_type=type_hints["compliance_security_control_id"])
                check_type(argname="argument compliance_status", value=compliance_status, expected_type=type_hints["compliance_status"])
                check_type(argname="argument confidence", value=confidence, expected_type=type_hints["confidence"])
                check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
                check_type(argname="argument criticality", value=criticality, expected_type=type_hints["criticality"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument first_observed_at", value=first_observed_at, expected_type=type_hints["first_observed_at"])
                check_type(argname="argument generator_id", value=generator_id, expected_type=type_hints["generator_id"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument last_observed_at", value=last_observed_at, expected_type=type_hints["last_observed_at"])
                check_type(argname="argument note_text", value=note_text, expected_type=type_hints["note_text"])
                check_type(argname="argument note_updated_at", value=note_updated_at, expected_type=type_hints["note_updated_at"])
                check_type(argname="argument note_updated_by", value=note_updated_by, expected_type=type_hints["note_updated_by"])
                check_type(argname="argument product_arn", value=product_arn, expected_type=type_hints["product_arn"])
                check_type(argname="argument product_name", value=product_name, expected_type=type_hints["product_name"])
                check_type(argname="argument record_state", value=record_state, expected_type=type_hints["record_state"])
                check_type(argname="argument related_findings_id", value=related_findings_id, expected_type=type_hints["related_findings_id"])
                check_type(argname="argument related_findings_product_arn", value=related_findings_product_arn, expected_type=type_hints["related_findings_product_arn"])
                check_type(argname="argument resource_details_other", value=resource_details_other, expected_type=type_hints["resource_details_other"])
                check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
                check_type(argname="argument resource_partition", value=resource_partition, expected_type=type_hints["resource_partition"])
                check_type(argname="argument resource_region", value=resource_region, expected_type=type_hints["resource_region"])
                check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
                check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
                check_type(argname="argument severity_label", value=severity_label, expected_type=type_hints["severity_label"])
                check_type(argname="argument source_url", value=source_url, expected_type=type_hints["source_url"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
                check_type(argname="argument user_defined_fields", value=user_defined_fields, expected_type=type_hints["user_defined_fields"])
                check_type(argname="argument verification_state", value=verification_state, expected_type=type_hints["verification_state"])
                check_type(argname="argument workflow_status", value=workflow_status, expected_type=type_hints["workflow_status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_account_id is not None:
                self._values["aws_account_id"] = aws_account_id
            if company_name is not None:
                self._values["company_name"] = company_name
            if compliance_associated_standards_id is not None:
                self._values["compliance_associated_standards_id"] = compliance_associated_standards_id
            if compliance_security_control_id is not None:
                self._values["compliance_security_control_id"] = compliance_security_control_id
            if compliance_status is not None:
                self._values["compliance_status"] = compliance_status
            if confidence is not None:
                self._values["confidence"] = confidence
            if created_at is not None:
                self._values["created_at"] = created_at
            if criticality is not None:
                self._values["criticality"] = criticality
            if description is not None:
                self._values["description"] = description
            if first_observed_at is not None:
                self._values["first_observed_at"] = first_observed_at
            if generator_id is not None:
                self._values["generator_id"] = generator_id
            if id is not None:
                self._values["id"] = id
            if last_observed_at is not None:
                self._values["last_observed_at"] = last_observed_at
            if note_text is not None:
                self._values["note_text"] = note_text
            if note_updated_at is not None:
                self._values["note_updated_at"] = note_updated_at
            if note_updated_by is not None:
                self._values["note_updated_by"] = note_updated_by
            if product_arn is not None:
                self._values["product_arn"] = product_arn
            if product_name is not None:
                self._values["product_name"] = product_name
            if record_state is not None:
                self._values["record_state"] = record_state
            if related_findings_id is not None:
                self._values["related_findings_id"] = related_findings_id
            if related_findings_product_arn is not None:
                self._values["related_findings_product_arn"] = related_findings_product_arn
            if resource_details_other is not None:
                self._values["resource_details_other"] = resource_details_other
            if resource_id is not None:
                self._values["resource_id"] = resource_id
            if resource_partition is not None:
                self._values["resource_partition"] = resource_partition
            if resource_region is not None:
                self._values["resource_region"] = resource_region
            if resource_tags is not None:
                self._values["resource_tags"] = resource_tags
            if resource_type is not None:
                self._values["resource_type"] = resource_type
            if severity_label is not None:
                self._values["severity_label"] = severity_label
            if source_url is not None:
                self._values["source_url"] = source_url
            if title is not None:
                self._values["title"] = title
            if type is not None:
                self._values["type"] = type
            if updated_at is not None:
                self._values["updated_at"] = updated_at
            if user_defined_fields is not None:
                self._values["user_defined_fields"] = user_defined_fields
            if verification_state is not None:
                self._values["verification_state"] = verification_state
            if workflow_status is not None:
                self._values["workflow_status"] = workflow_status

        @builtins.property
        def aws_account_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''The AWS account ID in which a finding was generated.

            Array Members: Minimum number of 1 item. Maximum number of 100 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-awsaccountid
            '''
            result = self._values.get("aws_account_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def company_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''The name of the company for the product that generated the finding.

            For control-based findings, the company is AWS .

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-companyname
            '''
            result = self._values.get("company_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def compliance_associated_standards_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''The unique identifier of a standard in which a control is enabled.

            This field consists of the resource portion of the Amazon Resource Name (ARN) returned for a standard in the `DescribeStandards <https://docs.aws.amazon.com/securityhub/1.0/APIReference/API_DescribeStandards.html>`_ API response.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-complianceassociatedstandardsid
            '''
            result = self._values.get("compliance_associated_standards_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def compliance_security_control_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''The security control ID for which a finding was generated. Security control IDs are the same across standards.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-compliancesecuritycontrolid
            '''
            result = self._values.get("compliance_security_control_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def compliance_status(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''The result of a security check. This field is only used for findings generated from controls.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-compliancestatus
            '''
            result = self._values.get("compliance_status")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def confidence(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.NumberFilterProperty"]]]]:
            '''The likelihood that a finding accurately identifies the behavior or issue that it was intended to identify.

            ``Confidence`` is scored on a 0–100 basis using a ratio scale. A value of ``0`` means 0 percent confidence, and a value of ``100`` means 100 percent confidence. For example, a data exfiltration detection based on a statistical deviation of network traffic has low confidence because an actual exfiltration hasn't been verified. For more information, see `Confidence <https://docs.aws.amazon.com/securityhub/latest/userguide/asff-top-level-attributes.html#asff-confidence>`_ in the *Security Hub User Guide* .

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-confidence
            '''
            result = self._values.get("confidence")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.NumberFilterProperty"]]]], result)

        @builtins.property
        def created_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.DateFilterProperty"]]]]:
            '''A timestamp that indicates when this finding record was created.

            For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-createdat
            '''
            result = self._values.get("created_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def criticality(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.NumberFilterProperty"]]]]:
            '''The level of importance that is assigned to the resources that are associated with a finding.

            ``Criticality`` is scored on a 0–100 basis, using a ratio scale that supports only full integers. A score of ``0`` means that the underlying resources have no criticality, and a score of ``100`` is reserved for the most critical resources. For more information, see `Criticality <https://docs.aws.amazon.com/securityhub/latest/userguide/asff-top-level-attributes.html#asff-criticality>`_ in the *Security Hub User Guide* .

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-criticality
            '''
            result = self._values.get("criticality")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.NumberFilterProperty"]]]], result)

        @builtins.property
        def description(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''A finding's description.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def first_observed_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.DateFilterProperty"]]]]:
            '''A timestamp that indicates when the potential security issue captured by a finding was first observed by the security findings product.

            For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-firstobservedat
            '''
            result = self._values.get("first_observed_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def generator_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''The identifier for the solution-specific component that generated a finding.

            Array Members: Minimum number of 1 item. Maximum number of 100 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-generatorid
            '''
            result = self._values.get("generator_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''The product-specific identifier for a finding.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def last_observed_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.DateFilterProperty"]]]]:
            '''A timestamp that indicates when the security findings provider most recently observed a change in the resource that is involved in the finding.

            For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-lastobservedat
            '''
            result = self._values.get("last_observed_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def note_text(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''The text of a user-defined note that's added to a finding.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-notetext
            '''
            result = self._values.get("note_text")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def note_updated_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.DateFilterProperty"]]]]:
            '''The timestamp of when the note was updated.

            For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-noteupdatedat
            '''
            result = self._values.get("note_updated_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def note_updated_by(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''The principal that created a note.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-noteupdatedby
            '''
            result = self._values.get("note_updated_by")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def product_arn(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''The Amazon Resource Name (ARN) for a third-party product that generated a finding in Security Hub.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-productarn
            '''
            result = self._values.get("product_arn")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def product_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''Provides the name of the product that generated the finding. For control-based findings, the product name is Security Hub.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-productname
            '''
            result = self._values.get("product_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def record_state(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''Provides the current state of a finding.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-recordstate
            '''
            result = self._values.get("record_state")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def related_findings_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''The product-generated identifier for a related finding.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-relatedfindingsid
            '''
            result = self._values.get("related_findings_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def related_findings_product_arn(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''The ARN for the product that generated a related finding.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-relatedfindingsproductarn
            '''
            result = self._values.get("related_findings_product_arn")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_details_other(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.MapFilterProperty"]]]]:
            '''Custom fields and values about the resource that a finding pertains to.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-resourcedetailsother
            '''
            result = self._values.get("resource_details_other")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.MapFilterProperty"]]]], result)

        @builtins.property
        def resource_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''The identifier for the given resource type.

            For AWS resources that are identified by Amazon Resource Names (ARNs), this is the ARN. For AWS resources that lack ARNs, this is the identifier as defined by the AWS service that created the resource. For non- AWS resources, this is a unique identifier that is associated with the resource.

            Array Members: Minimum number of 1 item. Maximum number of 100 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-resourceid
            '''
            result = self._values.get("resource_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_partition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''The partition in which the resource that the finding pertains to is located.

            A partition is a group of AWS Regions . Each AWS account is scoped to one partition.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-resourcepartition
            '''
            result = self._values.get("resource_partition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_region(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''The AWS Region where the resource that a finding pertains to is located.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-resourceregion
            '''
            result = self._values.get("resource_region")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_tags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.MapFilterProperty"]]]]:
            '''A list of AWS tags associated with a resource at the time the finding was processed.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-resourcetags
            '''
            result = self._values.get("resource_tags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.MapFilterProperty"]]]], result)

        @builtins.property
        def resource_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''A finding's title.

            Array Members: Minimum number of 1 item. Maximum number of 100 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-resourcetype
            '''
            result = self._values.get("resource_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def severity_label(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''The severity value of the finding.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-severitylabel
            '''
            result = self._values.get("severity_label")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def source_url(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''Provides a URL that links to a page about the current finding in the finding product.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-sourceurl
            '''
            result = self._values.get("source_url")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def title(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''A finding's title.

            Array Members: Minimum number of 1 item. Maximum number of 100 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''One or more finding types in the format of namespace/category/classifier that classify a finding.

            For a list of namespaces, classifiers, and categories, see `Types taxonomy for ASFF <https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-findings-format-type-taxonomy.html>`_ in the *Security Hub User Guide* .

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def updated_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.DateFilterProperty"]]]]:
            '''A timestamp that indicates when the finding record was most recently updated.

            For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-updatedat
            '''
            result = self._values.get("updated_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def user_defined_fields(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.MapFilterProperty"]]]]:
            '''A list of user-defined name and value string pairs added to a finding.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-userdefinedfields
            '''
            result = self._values.get("user_defined_fields")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.MapFilterProperty"]]]], result)

        @builtins.property
        def verification_state(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''Provides the veracity of a finding.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-verificationstate
            '''
            result = self._values.get("verification_state")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def workflow_status(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]]:
            '''Provides information about the status of the investigation into a finding.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-automationrulesfindingfilters.html#cfn-securityhub-automationrule-automationrulesfindingfilters-workflowstatus
            '''
            result = self._values.get("workflow_status")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.StringFilterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutomationRulesFindingFiltersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRulePropsMixin.DateFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"date_range": "dateRange", "end": "end", "start": "start"},
    )
    class DateFilterProperty:
        def __init__(
            self,
            *,
            date_range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRulePropsMixin.DateRangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            end: typing.Optional[builtins.str] = None,
            start: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A date filter for querying findings.

            :param date_range: A date range for the date filter.
            :param end: A timestamp that provides the end date for the date filter. For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .
            :param start: A timestamp that provides the start date for the date filter. For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-datefilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                date_filter_property = securityhub_mixins.CfnAutomationRulePropsMixin.DateFilterProperty(
                    date_range=securityhub_mixins.CfnAutomationRulePropsMixin.DateRangeProperty(
                        unit="unit",
                        value=123
                    ),
                    end="end",
                    start="start"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__887ee0b850afa49cf671af6f233fa520e9eeff3942f097b5662298458928ca39)
                check_type(argname="argument date_range", value=date_range, expected_type=type_hints["date_range"])
                check_type(argname="argument end", value=end, expected_type=type_hints["end"])
                check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if date_range is not None:
                self._values["date_range"] = date_range
            if end is not None:
                self._values["end"] = end
            if start is not None:
                self._values["start"] = start

        @builtins.property
        def date_range(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.DateRangeProperty"]]:
            '''A date range for the date filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-datefilter.html#cfn-securityhub-automationrule-datefilter-daterange
            '''
            result = self._values.get("date_range")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRulePropsMixin.DateRangeProperty"]], result)

        @builtins.property
        def end(self) -> typing.Optional[builtins.str]:
            '''A timestamp that provides the end date for the date filter.

            For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-datefilter.html#cfn-securityhub-automationrule-datefilter-end
            '''
            result = self._values.get("end")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start(self) -> typing.Optional[builtins.str]:
            '''A timestamp that provides the start date for the date filter.

            For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-datefilter.html#cfn-securityhub-automationrule-datefilter-start
            '''
            result = self._values.get("start")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DateFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRulePropsMixin.DateRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"unit": "unit", "value": "value"},
    )
    class DateRangeProperty:
        def __init__(
            self,
            *,
            unit: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A date range for the date filter.

            :param unit: A date range unit for the date filter.
            :param value: A date range value for the date filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-daterange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                date_range_property = securityhub_mixins.CfnAutomationRulePropsMixin.DateRangeProperty(
                    unit="unit",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3c335575fda70574a4598a85fa398ae9ac244bdd2aa1325aefaa206d38565a6f)
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if unit is not None:
                self._values["unit"] = unit
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''A date range unit for the date filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-daterange.html#cfn-securityhub-automationrule-daterange-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''A date range value for the date filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-daterange.html#cfn-securityhub-automationrule-daterange-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DateRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRulePropsMixin.MapFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"comparison": "comparison", "key": "key", "value": "value"},
    )
    class MapFilterProperty:
        def __init__(
            self,
            *,
            comparison: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A map filter for filtering Security Hub findings.

            Each map filter provides the field to check for, the value to check for, and the comparison operator.

            :param comparison: The condition to apply to the key value when filtering Security Hub findings with a map filter. To search for values that have the filter value, use one of the following comparison operators: - To search for values that include the filter value, use ``CONTAINS`` . For example, for the ``ResourceTags`` field, the filter ``Department CONTAINS Security`` matches findings that include the value ``Security`` for the ``Department`` tag. In the same example, a finding with a value of ``Security team`` for the ``Department`` tag is a match. - To search for values that exactly match the filter value, use ``EQUALS`` . For example, for the ``ResourceTags`` field, the filter ``Department EQUALS Security`` matches findings that have the value ``Security`` for the ``Department`` tag. ``CONTAINS`` and ``EQUALS`` filters on the same field are joined by ``OR`` . A finding matches if it matches any one of those filters. For example, the filters ``Department CONTAINS Security OR Department CONTAINS Finance`` match a finding that includes either ``Security`` , ``Finance`` , or both values. To search for values that don't have the filter value, use one of the following comparison operators: - To search for values that exclude the filter value, use ``NOT_CONTAINS`` . For example, for the ``ResourceTags`` field, the filter ``Department NOT_CONTAINS Finance`` matches findings that exclude the value ``Finance`` for the ``Department`` tag. - To search for values other than the filter value, use ``NOT_EQUALS`` . For example, for the ``ResourceTags`` field, the filter ``Department NOT_EQUALS Finance`` matches findings that don’t have the value ``Finance`` for the ``Department`` tag. ``NOT_CONTAINS`` and ``NOT_EQUALS`` filters on the same field are joined by ``AND`` . A finding matches only if it matches all of those filters. For example, the filters ``Department NOT_CONTAINS Security AND Department NOT_CONTAINS Finance`` match a finding that excludes both the ``Security`` and ``Finance`` values. ``CONTAINS`` filters can only be used with other ``CONTAINS`` filters. ``NOT_CONTAINS`` filters can only be used with other ``NOT_CONTAINS`` filters. You can’t have both a ``CONTAINS`` filter and a ``NOT_CONTAINS`` filter on the same field. Similarly, you can’t have both an ``EQUALS`` filter and a ``NOT_EQUALS`` filter on the same field. Combining filters in this way returns an error. ``CONTAINS`` and ``NOT_CONTAINS`` operators can be used only with automation rules. For more information, see `Automation rules <https://docs.aws.amazon.com/securityhub/latest/userguide/automation-rules.html>`_ in the *Security Hub User Guide* .
            :param key: The key of the map filter. For example, for ``ResourceTags`` , ``Key`` identifies the name of the tag. For ``UserDefinedFields`` , ``Key`` is the name of the field.
            :param value: The value for the key in the map filter. Filter values are case sensitive. For example, one of the values for a tag called ``Department`` might be ``Security`` . If you provide ``security`` as the filter value, then there's no match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-mapfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                map_filter_property = securityhub_mixins.CfnAutomationRulePropsMixin.MapFilterProperty(
                    comparison="comparison",
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1e5190129c990b1ca04431029e9500d9cdfc4f210df966a29bf52a3d3fa7afc4)
                check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparison is not None:
                self._values["comparison"] = comparison
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def comparison(self) -> typing.Optional[builtins.str]:
            '''The condition to apply to the key value when filtering Security Hub findings with a map filter.

            To search for values that have the filter value, use one of the following comparison operators:

            - To search for values that include the filter value, use ``CONTAINS`` . For example, for the ``ResourceTags`` field, the filter ``Department CONTAINS Security`` matches findings that include the value ``Security`` for the ``Department`` tag. In the same example, a finding with a value of ``Security team`` for the ``Department`` tag is a match.
            - To search for values that exactly match the filter value, use ``EQUALS`` . For example, for the ``ResourceTags`` field, the filter ``Department EQUALS Security`` matches findings that have the value ``Security`` for the ``Department`` tag.

            ``CONTAINS`` and ``EQUALS`` filters on the same field are joined by ``OR`` . A finding matches if it matches any one of those filters. For example, the filters ``Department CONTAINS Security OR Department CONTAINS Finance`` match a finding that includes either ``Security`` , ``Finance`` , or both values.

            To search for values that don't have the filter value, use one of the following comparison operators:

            - To search for values that exclude the filter value, use ``NOT_CONTAINS`` . For example, for the ``ResourceTags`` field, the filter ``Department NOT_CONTAINS Finance`` matches findings that exclude the value ``Finance`` for the ``Department`` tag.
            - To search for values other than the filter value, use ``NOT_EQUALS`` . For example, for the ``ResourceTags`` field, the filter ``Department NOT_EQUALS Finance`` matches findings that don’t have the value ``Finance`` for the ``Department`` tag.

            ``NOT_CONTAINS`` and ``NOT_EQUALS`` filters on the same field are joined by ``AND`` . A finding matches only if it matches all of those filters. For example, the filters ``Department NOT_CONTAINS Security AND Department NOT_CONTAINS Finance`` match a finding that excludes both the ``Security`` and ``Finance`` values.

            ``CONTAINS`` filters can only be used with other ``CONTAINS`` filters. ``NOT_CONTAINS`` filters can only be used with other ``NOT_CONTAINS`` filters.

            You can’t have both a ``CONTAINS`` filter and a ``NOT_CONTAINS`` filter on the same field. Similarly, you can’t have both an ``EQUALS`` filter and a ``NOT_EQUALS`` filter on the same field. Combining filters in this way returns an error.

            ``CONTAINS`` and ``NOT_CONTAINS`` operators can be used only with automation rules. For more information, see `Automation rules <https://docs.aws.amazon.com/securityhub/latest/userguide/automation-rules.html>`_ in the *Security Hub User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-mapfilter.html#cfn-securityhub-automationrule-mapfilter-comparison
            '''
            result = self._values.get("comparison")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key of the map filter.

            For example, for ``ResourceTags`` , ``Key`` identifies the name of the tag. For ``UserDefinedFields`` , ``Key`` is the name of the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-mapfilter.html#cfn-securityhub-automationrule-mapfilter-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value for the key in the map filter.

            Filter values are case sensitive. For example, one of the values for a tag called ``Department`` might be ``Security`` . If you provide ``security`` as the filter value, then there's no match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-mapfilter.html#cfn-securityhub-automationrule-mapfilter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MapFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRulePropsMixin.NoteUpdateProperty",
        jsii_struct_bases=[],
        name_mapping={"text": "text", "updated_by": "updatedBy"},
    )
    class NoteUpdateProperty:
        def __init__(
            self,
            *,
            text: typing.Optional[builtins.str] = None,
            updated_by: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The updated note.

            :param text: The updated note text.
            :param updated_by: The principal that updated the note.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-noteupdate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                note_update_property = securityhub_mixins.CfnAutomationRulePropsMixin.NoteUpdateProperty(
                    text="text",
                    updated_by="updatedBy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ad083af91387ea6a85dd77ee35e7fa6f8506afb1560e352c6847ae1e6e2a0255)
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
                check_type(argname="argument updated_by", value=updated_by, expected_type=type_hints["updated_by"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if text is not None:
                self._values["text"] = text
            if updated_by is not None:
                self._values["updated_by"] = updated_by

        @builtins.property
        def text(self) -> typing.Optional[builtins.str]:
            '''The updated note text.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-noteupdate.html#cfn-securityhub-automationrule-noteupdate-text
            '''
            result = self._values.get("text")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def updated_by(self) -> typing.Optional[builtins.str]:
            '''The principal that updated the note.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-noteupdate.html#cfn-securityhub-automationrule-noteupdate-updatedby
            '''
            result = self._values.get("updated_by")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NoteUpdateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRulePropsMixin.NumberFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"eq": "eq", "gte": "gte", "lte": "lte"},
    )
    class NumberFilterProperty:
        def __init__(
            self,
            *,
            eq: typing.Optional[jsii.Number] = None,
            gte: typing.Optional[jsii.Number] = None,
            lte: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A number filter for querying findings.

            :param eq: The equal-to condition to be applied to a single field when querying for findings.
            :param gte: The greater-than-equal condition to be applied to a single field when querying for findings.
            :param lte: The less-than-equal condition to be applied to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-numberfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                number_filter_property = securityhub_mixins.CfnAutomationRulePropsMixin.NumberFilterProperty(
                    eq=123,
                    gte=123,
                    lte=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4f4153abc33c162931c5d6ae0e1d5ae3729ccc732bbc75d33a331fbdeda019e9)
                check_type(argname="argument eq", value=eq, expected_type=type_hints["eq"])
                check_type(argname="argument gte", value=gte, expected_type=type_hints["gte"])
                check_type(argname="argument lte", value=lte, expected_type=type_hints["lte"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if eq is not None:
                self._values["eq"] = eq
            if gte is not None:
                self._values["gte"] = gte
            if lte is not None:
                self._values["lte"] = lte

        @builtins.property
        def eq(self) -> typing.Optional[jsii.Number]:
            '''The equal-to condition to be applied to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-numberfilter.html#cfn-securityhub-automationrule-numberfilter-eq
            '''
            result = self._values.get("eq")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def gte(self) -> typing.Optional[jsii.Number]:
            '''The greater-than-equal condition to be applied to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-numberfilter.html#cfn-securityhub-automationrule-numberfilter-gte
            '''
            result = self._values.get("gte")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def lte(self) -> typing.Optional[jsii.Number]:
            '''The less-than-equal condition to be applied to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-numberfilter.html#cfn-securityhub-automationrule-numberfilter-lte
            '''
            result = self._values.get("lte")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NumberFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRulePropsMixin.RelatedFindingProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "product_arn": "productArn"},
    )
    class RelatedFindingProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            product_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides details about a list of findings that the current finding relates to.

            :param id: The product-generated identifier for a related finding. Array Members: Minimum number of 1 item. Maximum number of 20 items.
            :param product_arn: The Amazon Resource Name (ARN) for the product that generated a related finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-relatedfinding.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                related_finding_property = securityhub_mixins.CfnAutomationRulePropsMixin.RelatedFindingProperty(
                    id="id",
                    product_arn="productArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0f15cfd2baa345c2c93664ca3e713784a5968626d0dca86de0e11ab7e6deb2a5)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument product_arn", value=product_arn, expected_type=type_hints["product_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if product_arn is not None:
                self._values["product_arn"] = product_arn

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The product-generated identifier for a related finding.

            Array Members: Minimum number of 1 item. Maximum number of 20 items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-relatedfinding.html#cfn-securityhub-automationrule-relatedfinding-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def product_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the product that generated a related finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-relatedfinding.html#cfn-securityhub-automationrule-relatedfinding-productarn
            '''
            result = self._values.get("product_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RelatedFindingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRulePropsMixin.SeverityUpdateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "label": "label",
            "normalized": "normalized",
            "product": "product",
        },
    )
    class SeverityUpdateProperty:
        def __init__(
            self,
            *,
            label: typing.Optional[builtins.str] = None,
            normalized: typing.Optional[jsii.Number] = None,
            product: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Updates to the severity information for a finding.

            :param label: The severity value of the finding. The allowed values are the following. - ``INFORMATIONAL`` - No issue was found. - ``LOW`` - The issue does not require action on its own. - ``MEDIUM`` - The issue must be addressed but not urgently. - ``HIGH`` - The issue must be addressed as a priority. - ``CRITICAL`` - The issue must be remediated immediately to avoid it escalating.
            :param normalized: The normalized severity for the finding. This attribute is to be deprecated in favor of ``Label`` . If you provide ``Normalized`` and don't provide ``Label`` , ``Label`` is set automatically as follows. - 0 - ``INFORMATIONAL`` - 1–39 - ``LOW`` - 40–69 - ``MEDIUM`` - 70–89 - ``HIGH`` - 90–100 - ``CRITICAL``
            :param product: The native severity as defined by the AWS service or integrated partner product that generated the finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-severityupdate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                severity_update_property = securityhub_mixins.CfnAutomationRulePropsMixin.SeverityUpdateProperty(
                    label="label",
                    normalized=123,
                    product=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0d580b2b8ab190975a635761224118468a0eb39d45a62d66d4e1d0819a78eca6)
                check_type(argname="argument label", value=label, expected_type=type_hints["label"])
                check_type(argname="argument normalized", value=normalized, expected_type=type_hints["normalized"])
                check_type(argname="argument product", value=product, expected_type=type_hints["product"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if label is not None:
                self._values["label"] = label
            if normalized is not None:
                self._values["normalized"] = normalized
            if product is not None:
                self._values["product"] = product

        @builtins.property
        def label(self) -> typing.Optional[builtins.str]:
            '''The severity value of the finding. The allowed values are the following.

            - ``INFORMATIONAL`` - No issue was found.
            - ``LOW`` - The issue does not require action on its own.
            - ``MEDIUM`` - The issue must be addressed but not urgently.
            - ``HIGH`` - The issue must be addressed as a priority.
            - ``CRITICAL`` - The issue must be remediated immediately to avoid it escalating.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-severityupdate.html#cfn-securityhub-automationrule-severityupdate-label
            '''
            result = self._values.get("label")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def normalized(self) -> typing.Optional[jsii.Number]:
            '''The normalized severity for the finding. This attribute is to be deprecated in favor of ``Label`` .

            If you provide ``Normalized`` and don't provide ``Label`` , ``Label`` is set automatically as follows.

            - 0 - ``INFORMATIONAL``
            - 1–39 - ``LOW``
            - 40–69 - ``MEDIUM``
            - 70–89 - ``HIGH``
            - 90–100 - ``CRITICAL``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-severityupdate.html#cfn-securityhub-automationrule-severityupdate-normalized
            '''
            result = self._values.get("normalized")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def product(self) -> typing.Optional[jsii.Number]:
            '''The native severity as defined by the AWS service or integrated partner product that generated the finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-severityupdate.html#cfn-securityhub-automationrule-severityupdate-product
            '''
            result = self._values.get("product")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SeverityUpdateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRulePropsMixin.StringFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"comparison": "comparison", "value": "value"},
    )
    class StringFilterProperty:
        def __init__(
            self,
            *,
            comparison: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A string filter for filtering Security Hub findings.

            :param comparison: The condition to apply to a string value when filtering Security Hub findings. To search for values that have the filter value, use one of the following comparison operators: - To search for values that include the filter value, use ``CONTAINS`` . For example, the filter ``Title CONTAINS CloudFront`` matches findings that have a ``Title`` that includes the string CloudFront. - To search for values that exactly match the filter value, use ``EQUALS`` . For example, the filter ``AwsAccountId EQUALS 123456789012`` only matches findings that have an account ID of ``123456789012`` . - To search for values that start with the filter value, use ``PREFIX`` . For example, the filter ``ResourceRegion PREFIX us`` matches findings that have a ``ResourceRegion`` that starts with ``us`` . A ``ResourceRegion`` that starts with a different value, such as ``af`` , ``ap`` , or ``ca`` , doesn't match. ``CONTAINS`` , ``EQUALS`` , and ``PREFIX`` filters on the same field are joined by ``OR`` . A finding matches if it matches any one of those filters. For example, the filters ``Title CONTAINS CloudFront OR Title CONTAINS CloudWatch`` match a finding that includes either ``CloudFront`` , ``CloudWatch`` , or both strings in the title. To search for values that don’t have the filter value, use one of the following comparison operators: - To search for values that exclude the filter value, use ``NOT_CONTAINS`` . For example, the filter ``Title NOT_CONTAINS CloudFront`` matches findings that have a ``Title`` that excludes the string CloudFront. - To search for values other than the filter value, use ``NOT_EQUALS`` . For example, the filter ``AwsAccountId NOT_EQUALS 123456789012`` only matches findings that have an account ID other than ``123456789012`` . - To search for values that don't start with the filter value, use ``PREFIX_NOT_EQUALS`` . For example, the filter ``ResourceRegion PREFIX_NOT_EQUALS us`` matches findings with a ``ResourceRegion`` that starts with a value other than ``us`` . ``NOT_CONTAINS`` , ``NOT_EQUALS`` , and ``PREFIX_NOT_EQUALS`` filters on the same field are joined by ``AND`` . A finding matches only if it matches all of those filters. For example, the filters ``Title NOT_CONTAINS CloudFront AND Title NOT_CONTAINS CloudWatch`` match a finding that excludes both ``CloudFront`` and ``CloudWatch`` in the title. You can’t have both a ``CONTAINS`` filter and a ``NOT_CONTAINS`` filter on the same field. Similarly, you can't provide both an ``EQUALS`` filter and a ``NOT_EQUALS`` or ``PREFIX_NOT_EQUALS`` filter on the same field. Combining filters in this way returns an error. ``CONTAINS`` filters can only be used with other ``CONTAINS`` filters. ``NOT_CONTAINS`` filters can only be used with other ``NOT_CONTAINS`` filters. You can combine ``PREFIX`` filters with ``NOT_EQUALS`` or ``PREFIX_NOT_EQUALS`` filters for the same field. Security Hub first processes the ``PREFIX`` filters, and then the ``NOT_EQUALS`` or ``PREFIX_NOT_EQUALS`` filters. For example, for the following filters, Security Hub first identifies findings that have resource types that start with either ``AwsIam`` or ``AwsEc2`` . It then excludes findings that have a resource type of ``AwsIamPolicy`` and findings that have a resource type of ``AwsEc2NetworkInterface`` . - ``ResourceType PREFIX AwsIam`` - ``ResourceType PREFIX AwsEc2`` - ``ResourceType NOT_EQUALS AwsIamPolicy`` - ``ResourceType NOT_EQUALS AwsEc2NetworkInterface`` ``CONTAINS`` and ``NOT_CONTAINS`` operators can be used only with automation rules V1. ``CONTAINS_WORD`` operator is only supported in ``GetFindingsV2`` , ``GetFindingStatisticsV2`` , ``GetResourcesV2`` , and ``GetResourceStatisticsV2`` APIs. For more information, see `Automation rules <https://docs.aws.amazon.com/securityhub/latest/userguide/automation-rules.html>`_ in the *Security Hub User Guide* .
            :param value: The string filter value. Filter values are case sensitive. For example, the product name for control-based findings is ``Security Hub`` . If you provide ``security hub`` as the filter value, there's no match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-stringfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                string_filter_property = securityhub_mixins.CfnAutomationRulePropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c5af0045035d0ec226bafd57a68aea5745b5a6c67d531f3f221a3d63d36a0de)
                check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparison is not None:
                self._values["comparison"] = comparison
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def comparison(self) -> typing.Optional[builtins.str]:
            '''The condition to apply to a string value when filtering Security Hub findings.

            To search for values that have the filter value, use one of the following comparison operators:

            - To search for values that include the filter value, use ``CONTAINS`` . For example, the filter ``Title CONTAINS CloudFront`` matches findings that have a ``Title`` that includes the string CloudFront.
            - To search for values that exactly match the filter value, use ``EQUALS`` . For example, the filter ``AwsAccountId EQUALS 123456789012`` only matches findings that have an account ID of ``123456789012`` .
            - To search for values that start with the filter value, use ``PREFIX`` . For example, the filter ``ResourceRegion PREFIX us`` matches findings that have a ``ResourceRegion`` that starts with ``us`` . A ``ResourceRegion`` that starts with a different value, such as ``af`` , ``ap`` , or ``ca`` , doesn't match.

            ``CONTAINS`` , ``EQUALS`` , and ``PREFIX`` filters on the same field are joined by ``OR`` . A finding matches if it matches any one of those filters. For example, the filters ``Title CONTAINS CloudFront OR Title CONTAINS CloudWatch`` match a finding that includes either ``CloudFront`` , ``CloudWatch`` , or both strings in the title.

            To search for values that don’t have the filter value, use one of the following comparison operators:

            - To search for values that exclude the filter value, use ``NOT_CONTAINS`` . For example, the filter ``Title NOT_CONTAINS CloudFront`` matches findings that have a ``Title`` that excludes the string CloudFront.
            - To search for values other than the filter value, use ``NOT_EQUALS`` . For example, the filter ``AwsAccountId NOT_EQUALS 123456789012`` only matches findings that have an account ID other than ``123456789012`` .
            - To search for values that don't start with the filter value, use ``PREFIX_NOT_EQUALS`` . For example, the filter ``ResourceRegion PREFIX_NOT_EQUALS us`` matches findings with a ``ResourceRegion`` that starts with a value other than ``us`` .

            ``NOT_CONTAINS`` , ``NOT_EQUALS`` , and ``PREFIX_NOT_EQUALS`` filters on the same field are joined by ``AND`` . A finding matches only if it matches all of those filters. For example, the filters ``Title NOT_CONTAINS CloudFront AND Title NOT_CONTAINS CloudWatch`` match a finding that excludes both ``CloudFront`` and ``CloudWatch`` in the title.

            You can’t have both a ``CONTAINS`` filter and a ``NOT_CONTAINS`` filter on the same field. Similarly, you can't provide both an ``EQUALS`` filter and a ``NOT_EQUALS`` or ``PREFIX_NOT_EQUALS`` filter on the same field. Combining filters in this way returns an error. ``CONTAINS`` filters can only be used with other ``CONTAINS`` filters. ``NOT_CONTAINS`` filters can only be used with other ``NOT_CONTAINS`` filters.

            You can combine ``PREFIX`` filters with ``NOT_EQUALS`` or ``PREFIX_NOT_EQUALS`` filters for the same field. Security Hub first processes the ``PREFIX`` filters, and then the ``NOT_EQUALS`` or ``PREFIX_NOT_EQUALS`` filters.

            For example, for the following filters, Security Hub first identifies findings that have resource types that start with either ``AwsIam`` or ``AwsEc2`` . It then excludes findings that have a resource type of ``AwsIamPolicy`` and findings that have a resource type of ``AwsEc2NetworkInterface`` .

            - ``ResourceType PREFIX AwsIam``
            - ``ResourceType PREFIX AwsEc2``
            - ``ResourceType NOT_EQUALS AwsIamPolicy``
            - ``ResourceType NOT_EQUALS AwsEc2NetworkInterface``

            ``CONTAINS`` and ``NOT_CONTAINS`` operators can be used only with automation rules V1. ``CONTAINS_WORD`` operator is only supported in ``GetFindingsV2`` , ``GetFindingStatisticsV2`` , ``GetResourcesV2`` , and ``GetResourceStatisticsV2`` APIs. For more information, see `Automation rules <https://docs.aws.amazon.com/securityhub/latest/userguide/automation-rules.html>`_ in the *Security Hub User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-stringfilter.html#cfn-securityhub-automationrule-stringfilter-comparison
            '''
            result = self._values.get("comparison")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The string filter value.

            Filter values are case sensitive. For example, the product name for control-based findings is ``Security Hub`` . If you provide ``security hub`` as the filter value, there's no match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-stringfilter.html#cfn-securityhub-automationrule-stringfilter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StringFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRulePropsMixin.WorkflowUpdateProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status"},
    )
    class WorkflowUpdateProperty:
        def __init__(self, *, status: typing.Optional[builtins.str] = None) -> None:
            '''Used to update information about the investigation into the finding.

            :param status: The status of the investigation into the finding. The workflow status is specific to an individual finding. It does not affect the generation of new findings. For example, setting the workflow status to ``SUPPRESSED`` or ``RESOLVED`` does not prevent a new finding for the same issue. The allowed values are the following. - ``NEW`` - The initial state of a finding, before it is reviewed. Security Hub also resets ``WorkFlowStatus`` from ``NOTIFIED`` or ``RESOLVED`` to ``NEW`` in the following cases: - The record state changes from ``ARCHIVED`` to ``ACTIVE`` . - The compliance status changes from ``PASSED`` to either ``WARNING`` , ``FAILED`` , or ``NOT_AVAILABLE`` . - ``NOTIFIED`` - Indicates that you notified the resource owner about the security issue. Used when the initial reviewer is not the resource owner, and needs intervention from the resource owner. - ``RESOLVED`` - The finding was reviewed and remediated and is now considered resolved. - ``SUPPRESSED`` - Indicates that you reviewed the finding and don't believe that any action is needed. The finding is no longer updated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-workflowupdate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                workflow_update_property = securityhub_mixins.CfnAutomationRulePropsMixin.WorkflowUpdateProperty(
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__987c6edb8b6d55217ef13ccf0cad34a20a0f4b7df6cebac361796031f5494456)
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the investigation into the finding.

            The workflow status is specific to an individual finding. It does not affect the generation of new findings. For example, setting the workflow status to ``SUPPRESSED`` or ``RESOLVED`` does not prevent a new finding for the same issue.

            The allowed values are the following.

            - ``NEW`` - The initial state of a finding, before it is reviewed.

            Security Hub also resets ``WorkFlowStatus`` from ``NOTIFIED`` or ``RESOLVED`` to ``NEW`` in the following cases:

            - The record state changes from ``ARCHIVED`` to ``ACTIVE`` .
            - The compliance status changes from ``PASSED`` to either ``WARNING`` , ``FAILED`` , or ``NOT_AVAILABLE`` .
            - ``NOTIFIED`` - Indicates that you notified the resource owner about the security issue. Used when the initial reviewer is not the resource owner, and needs intervention from the resource owner.
            - ``RESOLVED`` - The finding was reviewed and remediated and is now considered resolved.
            - ``SUPPRESSED`` - Indicates that you reviewed the finding and don't believe that any action is needed. The finding is no longer updated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrule-workflowupdate.html#cfn-securityhub-automationrule-workflowupdate-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkflowUpdateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRuleV2MixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "criteria": "criteria",
        "description": "description",
        "rule_name": "ruleName",
        "rule_order": "ruleOrder",
        "rule_status": "ruleStatus",
        "tags": "tags",
    },
)
class CfnAutomationRuleV2MixinProps:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRuleV2PropsMixin.AutomationRulesActionV2Property", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRuleV2PropsMixin.CriteriaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        rule_name: typing.Optional[builtins.str] = None,
        rule_order: typing.Optional[jsii.Number] = None,
        rule_status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnAutomationRuleV2PropsMixin.

        :param actions: A list of actions to be performed when the rule criteria is met.
        :param criteria: The filtering type and configuration of the automation rule.
        :param description: A description of the V2 automation rule.
        :param rule_name: The name of the V2 automation rule.
        :param rule_order: The value for the rule priority.
        :param rule_status: The status of the V2 automation rule.
        :param tags: A list of key-value pairs associated with the V2 automation rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-automationrulev2.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
            
            cfn_automation_rule_v2_mixin_props = securityhub_mixins.CfnAutomationRuleV2MixinProps(
                actions=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.AutomationRulesActionV2Property(
                    external_integration_configuration=securityhub_mixins.CfnAutomationRuleV2PropsMixin.ExternalIntegrationConfigurationProperty(
                        connector_arn="connectorArn"
                    ),
                    finding_fields_update=securityhub_mixins.CfnAutomationRuleV2PropsMixin.AutomationRulesFindingFieldsUpdateV2Property(
                        comment="comment",
                        severity_id=123,
                        status_id=123
                    ),
                    type="type"
                )],
                criteria=securityhub_mixins.CfnAutomationRuleV2PropsMixin.CriteriaProperty(
                    ocsf_finding_criteria=securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfFindingFiltersProperty(
                        composite_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.CompositeFilterProperty(
                            boolean_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfBooleanFilterProperty(
                                field_name="fieldName",
                                filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.BooleanFilterProperty(
                                    value=False
                                )
                            )],
                            date_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfDateFilterProperty(
                                field_name="fieldName",
                                filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.DateFilterProperty(
                                    date_range=securityhub_mixins.CfnAutomationRuleV2PropsMixin.DateRangeProperty(
                                        unit="unit",
                                        value=123
                                    ),
                                    end="end",
                                    start="start"
                                )
                            )],
                            map_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfMapFilterProperty(
                                field_name="fieldName",
                                filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.MapFilterProperty(
                                    comparison="comparison",
                                    key="key",
                                    value="value"
                                )
                            )],
                            number_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfNumberFilterProperty(
                                field_name="fieldName",
                                filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.NumberFilterProperty(
                                    eq=123,
                                    gte=123,
                                    lte=123
                                )
                            )],
                            operator="operator",
                            string_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfStringFilterProperty(
                                field_name="fieldName",
                                filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.StringFilterProperty(
                                    comparison="comparison",
                                    value="value"
                                )
                            )]
                        )],
                        composite_operator="compositeOperator"
                    )
                ),
                description="description",
                rule_name="ruleName",
                rule_order=123,
                rule_status="ruleStatus",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9d12e74f0b1b682f2c83ae4d3f8d880b607ca7874f0baa478df278f8c8926de)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument rule_order", value=rule_order, expected_type=type_hints["rule_order"])
            check_type(argname="argument rule_status", value=rule_status, expected_type=type_hints["rule_status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if criteria is not None:
            self._values["criteria"] = criteria
        if description is not None:
            self._values["description"] = description
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if rule_order is not None:
            self._values["rule_order"] = rule_order
        if rule_status is not None:
            self._values["rule_status"] = rule_status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def actions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.AutomationRulesActionV2Property"]]]]:
        '''A list of actions to be performed when the rule criteria is met.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-automationrulev2.html#cfn-securityhub-automationrulev2-actions
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.AutomationRulesActionV2Property"]]]], result)

    @builtins.property
    def criteria(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.CriteriaProperty"]]:
        '''The filtering type and configuration of the automation rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-automationrulev2.html#cfn-securityhub-automationrulev2-criteria
        '''
        result = self._values.get("criteria")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.CriteriaProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the V2 automation rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-automationrulev2.html#cfn-securityhub-automationrulev2-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''The name of the V2 automation rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-automationrulev2.html#cfn-securityhub-automationrulev2-rulename
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_order(self) -> typing.Optional[jsii.Number]:
        '''The value for the rule priority.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-automationrulev2.html#cfn-securityhub-automationrulev2-ruleorder
        '''
        result = self._values.get("rule_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rule_status(self) -> typing.Optional[builtins.str]:
        '''The status of the V2 automation rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-automationrulev2.html#cfn-securityhub-automationrulev2-rulestatus
        '''
        result = self._values.get("rule_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A list of key-value pairs associated with the V2 automation rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-automationrulev2.html#cfn-securityhub-automationrulev2-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAutomationRuleV2MixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAutomationRuleV2PropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRuleV2PropsMixin",
):
    '''Creates a V2 automation rule.

    This API is in public preview and subject to change.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-automationrulev2.html
    :cloudformationResource: AWS::SecurityHub::AutomationRuleV2
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
        
        cfn_automation_rule_v2_props_mixin = securityhub_mixins.CfnAutomationRuleV2PropsMixin(securityhub_mixins.CfnAutomationRuleV2MixinProps(
            actions=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.AutomationRulesActionV2Property(
                external_integration_configuration=securityhub_mixins.CfnAutomationRuleV2PropsMixin.ExternalIntegrationConfigurationProperty(
                    connector_arn="connectorArn"
                ),
                finding_fields_update=securityhub_mixins.CfnAutomationRuleV2PropsMixin.AutomationRulesFindingFieldsUpdateV2Property(
                    comment="comment",
                    severity_id=123,
                    status_id=123
                ),
                type="type"
            )],
            criteria=securityhub_mixins.CfnAutomationRuleV2PropsMixin.CriteriaProperty(
                ocsf_finding_criteria=securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfFindingFiltersProperty(
                    composite_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.CompositeFilterProperty(
                        boolean_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfBooleanFilterProperty(
                            field_name="fieldName",
                            filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.BooleanFilterProperty(
                                value=False
                            )
                        )],
                        date_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfDateFilterProperty(
                            field_name="fieldName",
                            filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.DateFilterProperty(
                                date_range=securityhub_mixins.CfnAutomationRuleV2PropsMixin.DateRangeProperty(
                                    unit="unit",
                                    value=123
                                ),
                                end="end",
                                start="start"
                            )
                        )],
                        map_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfMapFilterProperty(
                            field_name="fieldName",
                            filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.MapFilterProperty(
                                comparison="comparison",
                                key="key",
                                value="value"
                            )
                        )],
                        number_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfNumberFilterProperty(
                            field_name="fieldName",
                            filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.NumberFilterProperty(
                                eq=123,
                                gte=123,
                                lte=123
                            )
                        )],
                        operator="operator",
                        string_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfStringFilterProperty(
                            field_name="fieldName",
                            filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.StringFilterProperty(
                                comparison="comparison",
                                value="value"
                            )
                        )]
                    )],
                    composite_operator="compositeOperator"
                )
            ),
            description="description",
            rule_name="ruleName",
            rule_order=123,
            rule_status="ruleStatus",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAutomationRuleV2MixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecurityHub::AutomationRuleV2``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9bb1402ffecec33af1d0d0c40b081f11637786ef53f78c3532dd2fd0cb3bc43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__878fd859efe37ae68cf1ff9304252db7df901d4e4ed255dbfa68175255803a40)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93b49aeb4ee3f1af4846212e9be8b88783cb2d04630f6b244e8c2897ecaba631)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAutomationRuleV2MixinProps:
        return typing.cast(CfnAutomationRuleV2MixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRuleV2PropsMixin.AutomationRulesActionV2Property",
        jsii_struct_bases=[],
        name_mapping={
            "external_integration_configuration": "externalIntegrationConfiguration",
            "finding_fields_update": "findingFieldsUpdate",
            "type": "type",
        },
    )
    class AutomationRulesActionV2Property:
        def __init__(
            self,
            *,
            external_integration_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRuleV2PropsMixin.ExternalIntegrationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            finding_fields_update: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRuleV2PropsMixin.AutomationRulesFindingFieldsUpdateV2Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Allows you to configure automated responses.

            :param external_integration_configuration: The settings for integrating automation rule actions with external systems or service.
            :param finding_fields_update: Specifies that the automation rule action is an update to a finding field.
            :param type: Specifies the type of action that Security Hub takes when a finding matches the defined criteria of a rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-automationrulesactionv2.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                automation_rules_action_v2_property = securityhub_mixins.CfnAutomationRuleV2PropsMixin.AutomationRulesActionV2Property(
                    external_integration_configuration=securityhub_mixins.CfnAutomationRuleV2PropsMixin.ExternalIntegrationConfigurationProperty(
                        connector_arn="connectorArn"
                    ),
                    finding_fields_update=securityhub_mixins.CfnAutomationRuleV2PropsMixin.AutomationRulesFindingFieldsUpdateV2Property(
                        comment="comment",
                        severity_id=123,
                        status_id=123
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a5f9a6a4ec16cf9afb43324ebbd34e60ec01211a91ff01927c40cce4f0cc97b)
                check_type(argname="argument external_integration_configuration", value=external_integration_configuration, expected_type=type_hints["external_integration_configuration"])
                check_type(argname="argument finding_fields_update", value=finding_fields_update, expected_type=type_hints["finding_fields_update"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if external_integration_configuration is not None:
                self._values["external_integration_configuration"] = external_integration_configuration
            if finding_fields_update is not None:
                self._values["finding_fields_update"] = finding_fields_update
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def external_integration_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.ExternalIntegrationConfigurationProperty"]]:
            '''The settings for integrating automation rule actions with external systems or service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-automationrulesactionv2.html#cfn-securityhub-automationrulev2-automationrulesactionv2-externalintegrationconfiguration
            '''
            result = self._values.get("external_integration_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.ExternalIntegrationConfigurationProperty"]], result)

        @builtins.property
        def finding_fields_update(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.AutomationRulesFindingFieldsUpdateV2Property"]]:
            '''Specifies that the automation rule action is an update to a finding field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-automationrulesactionv2.html#cfn-securityhub-automationrulev2-automationrulesactionv2-findingfieldsupdate
            '''
            result = self._values.get("finding_fields_update")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.AutomationRulesFindingFieldsUpdateV2Property"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of action that Security Hub takes when a finding matches the defined criteria of a rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-automationrulesactionv2.html#cfn-securityhub-automationrulev2-automationrulesactionv2-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutomationRulesActionV2Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRuleV2PropsMixin.AutomationRulesFindingFieldsUpdateV2Property",
        jsii_struct_bases=[],
        name_mapping={
            "comment": "comment",
            "severity_id": "severityId",
            "status_id": "statusId",
        },
    )
    class AutomationRulesFindingFieldsUpdateV2Property:
        def __init__(
            self,
            *,
            comment: typing.Optional[builtins.str] = None,
            severity_id: typing.Optional[jsii.Number] = None,
            status_id: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Allows you to define the structure for modifying specific fields in security findings.

            :param comment: Notes or contextual information for findings that are modified by the automation rule.
            :param severity_id: The severity level to be assigned to findings that match the automation rule criteria.
            :param status_id: The status to be applied to findings that match automation rule criteria.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-automationrulesfindingfieldsupdatev2.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                automation_rules_finding_fields_update_v2_property = securityhub_mixins.CfnAutomationRuleV2PropsMixin.AutomationRulesFindingFieldsUpdateV2Property(
                    comment="comment",
                    severity_id=123,
                    status_id=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ba2aed98906c741a9bd2fbe66dd1c32466fc8e648cc422e94de9724787a733e5)
                check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
                check_type(argname="argument severity_id", value=severity_id, expected_type=type_hints["severity_id"])
                check_type(argname="argument status_id", value=status_id, expected_type=type_hints["status_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comment is not None:
                self._values["comment"] = comment
            if severity_id is not None:
                self._values["severity_id"] = severity_id
            if status_id is not None:
                self._values["status_id"] = status_id

        @builtins.property
        def comment(self) -> typing.Optional[builtins.str]:
            '''Notes or contextual information for findings that are modified by the automation rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-automationrulesfindingfieldsupdatev2.html#cfn-securityhub-automationrulev2-automationrulesfindingfieldsupdatev2-comment
            '''
            result = self._values.get("comment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def severity_id(self) -> typing.Optional[jsii.Number]:
            '''The severity level to be assigned to findings that match the automation rule criteria.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-automationrulesfindingfieldsupdatev2.html#cfn-securityhub-automationrulev2-automationrulesfindingfieldsupdatev2-severityid
            '''
            result = self._values.get("severity_id")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def status_id(self) -> typing.Optional[jsii.Number]:
            '''The status to be applied to findings that match automation rule criteria.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-automationrulesfindingfieldsupdatev2.html#cfn-securityhub-automationrulev2-automationrulesfindingfieldsupdatev2-statusid
            '''
            result = self._values.get("status_id")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutomationRulesFindingFieldsUpdateV2Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRuleV2PropsMixin.BooleanFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class BooleanFilterProperty:
        def __init__(
            self,
            *,
            value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Boolean filter for querying findings.

            :param value: The value of the boolean.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-booleanfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                boolean_filter_property = securityhub_mixins.CfnAutomationRuleV2PropsMixin.BooleanFilterProperty(
                    value=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e72cadef72fcac5d45eecf8613e805dcebeb42086dc987d581a4bb67368b4493)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The value of the boolean.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-booleanfilter.html#cfn-securityhub-automationrulev2-booleanfilter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BooleanFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRuleV2PropsMixin.CompositeFilterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "boolean_filters": "booleanFilters",
            "date_filters": "dateFilters",
            "map_filters": "mapFilters",
            "number_filters": "numberFilters",
            "operator": "operator",
            "string_filters": "stringFilters",
        },
    )
    class CompositeFilterProperty:
        def __init__(
            self,
            *,
            boolean_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRuleV2PropsMixin.OcsfBooleanFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            date_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRuleV2PropsMixin.OcsfDateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            map_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRuleV2PropsMixin.OcsfMapFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            number_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRuleV2PropsMixin.OcsfNumberFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            operator: typing.Optional[builtins.str] = None,
            string_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRuleV2PropsMixin.OcsfStringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Enables the creation of filtering criteria for security findings.

            :param boolean_filters: Enables filtering based on boolean field values.
            :param date_filters: Enables filtering based on date and timestamp fields.
            :param map_filters: Enables the creation of filtering criteria for security findings.
            :param number_filters: Enables filtering based on numerical field values.
            :param operator: The logical operator used to combine multiple filter conditions.
            :param string_filters: Enables filtering based on string field values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-compositefilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                composite_filter_property = securityhub_mixins.CfnAutomationRuleV2PropsMixin.CompositeFilterProperty(
                    boolean_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfBooleanFilterProperty(
                        field_name="fieldName",
                        filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.BooleanFilterProperty(
                            value=False
                        )
                    )],
                    date_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfDateFilterProperty(
                        field_name="fieldName",
                        filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.DateFilterProperty(
                            date_range=securityhub_mixins.CfnAutomationRuleV2PropsMixin.DateRangeProperty(
                                unit="unit",
                                value=123
                            ),
                            end="end",
                            start="start"
                        )
                    )],
                    map_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfMapFilterProperty(
                        field_name="fieldName",
                        filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.MapFilterProperty(
                            comparison="comparison",
                            key="key",
                            value="value"
                        )
                    )],
                    number_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfNumberFilterProperty(
                        field_name="fieldName",
                        filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.NumberFilterProperty(
                            eq=123,
                            gte=123,
                            lte=123
                        )
                    )],
                    operator="operator",
                    string_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfStringFilterProperty(
                        field_name="fieldName",
                        filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.StringFilterProperty(
                            comparison="comparison",
                            value="value"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__36e833683d7b1f7c421c9ee85f415dd03466d176834b653f19b93275f35f43a7)
                check_type(argname="argument boolean_filters", value=boolean_filters, expected_type=type_hints["boolean_filters"])
                check_type(argname="argument date_filters", value=date_filters, expected_type=type_hints["date_filters"])
                check_type(argname="argument map_filters", value=map_filters, expected_type=type_hints["map_filters"])
                check_type(argname="argument number_filters", value=number_filters, expected_type=type_hints["number_filters"])
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
                check_type(argname="argument string_filters", value=string_filters, expected_type=type_hints["string_filters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if boolean_filters is not None:
                self._values["boolean_filters"] = boolean_filters
            if date_filters is not None:
                self._values["date_filters"] = date_filters
            if map_filters is not None:
                self._values["map_filters"] = map_filters
            if number_filters is not None:
                self._values["number_filters"] = number_filters
            if operator is not None:
                self._values["operator"] = operator
            if string_filters is not None:
                self._values["string_filters"] = string_filters

        @builtins.property
        def boolean_filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.OcsfBooleanFilterProperty"]]]]:
            '''Enables filtering based on boolean field values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-compositefilter.html#cfn-securityhub-automationrulev2-compositefilter-booleanfilters
            '''
            result = self._values.get("boolean_filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.OcsfBooleanFilterProperty"]]]], result)

        @builtins.property
        def date_filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.OcsfDateFilterProperty"]]]]:
            '''Enables filtering based on date and timestamp fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-compositefilter.html#cfn-securityhub-automationrulev2-compositefilter-datefilters
            '''
            result = self._values.get("date_filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.OcsfDateFilterProperty"]]]], result)

        @builtins.property
        def map_filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.OcsfMapFilterProperty"]]]]:
            '''Enables the creation of filtering criteria for security findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-compositefilter.html#cfn-securityhub-automationrulev2-compositefilter-mapfilters
            '''
            result = self._values.get("map_filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.OcsfMapFilterProperty"]]]], result)

        @builtins.property
        def number_filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.OcsfNumberFilterProperty"]]]]:
            '''Enables filtering based on numerical field values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-compositefilter.html#cfn-securityhub-automationrulev2-compositefilter-numberfilters
            '''
            result = self._values.get("number_filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.OcsfNumberFilterProperty"]]]], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''The logical operator used to combine multiple filter conditions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-compositefilter.html#cfn-securityhub-automationrulev2-compositefilter-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def string_filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.OcsfStringFilterProperty"]]]]:
            '''Enables filtering based on string field values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-compositefilter.html#cfn-securityhub-automationrulev2-compositefilter-stringfilters
            '''
            result = self._values.get("string_filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.OcsfStringFilterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CompositeFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRuleV2PropsMixin.CriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={"ocsf_finding_criteria": "ocsfFindingCriteria"},
    )
    class CriteriaProperty:
        def __init__(
            self,
            *,
            ocsf_finding_criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRuleV2PropsMixin.OcsfFindingFiltersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The filtering type and configuration of the automation rule.

            :param ocsf_finding_criteria: The filtering conditions that align with OCSF standards.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-criteria.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                criteria_property = securityhub_mixins.CfnAutomationRuleV2PropsMixin.CriteriaProperty(
                    ocsf_finding_criteria=securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfFindingFiltersProperty(
                        composite_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.CompositeFilterProperty(
                            boolean_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfBooleanFilterProperty(
                                field_name="fieldName",
                                filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.BooleanFilterProperty(
                                    value=False
                                )
                            )],
                            date_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfDateFilterProperty(
                                field_name="fieldName",
                                filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.DateFilterProperty(
                                    date_range=securityhub_mixins.CfnAutomationRuleV2PropsMixin.DateRangeProperty(
                                        unit="unit",
                                        value=123
                                    ),
                                    end="end",
                                    start="start"
                                )
                            )],
                            map_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfMapFilterProperty(
                                field_name="fieldName",
                                filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.MapFilterProperty(
                                    comparison="comparison",
                                    key="key",
                                    value="value"
                                )
                            )],
                            number_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfNumberFilterProperty(
                                field_name="fieldName",
                                filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.NumberFilterProperty(
                                    eq=123,
                                    gte=123,
                                    lte=123
                                )
                            )],
                            operator="operator",
                            string_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfStringFilterProperty(
                                field_name="fieldName",
                                filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.StringFilterProperty(
                                    comparison="comparison",
                                    value="value"
                                )
                            )]
                        )],
                        composite_operator="compositeOperator"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__729e7751a827d45283d5d908d2e5650dad538a290161d1ea6591a6deaa72c8bb)
                check_type(argname="argument ocsf_finding_criteria", value=ocsf_finding_criteria, expected_type=type_hints["ocsf_finding_criteria"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ocsf_finding_criteria is not None:
                self._values["ocsf_finding_criteria"] = ocsf_finding_criteria

        @builtins.property
        def ocsf_finding_criteria(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.OcsfFindingFiltersProperty"]]:
            '''The filtering conditions that align with OCSF standards.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-criteria.html#cfn-securityhub-automationrulev2-criteria-ocsffindingcriteria
            '''
            result = self._values.get("ocsf_finding_criteria")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.OcsfFindingFiltersProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRuleV2PropsMixin.DateFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"date_range": "dateRange", "end": "end", "start": "start"},
    )
    class DateFilterProperty:
        def __init__(
            self,
            *,
            date_range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRuleV2PropsMixin.DateRangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            end: typing.Optional[builtins.str] = None,
            start: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A date filter for querying findings.

            :param date_range: A date range for the date filter.
            :param end: A timestamp that provides the end date for the date filter. For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .
            :param start: A timestamp that provides the start date for the date filter. For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-datefilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                date_filter_property = securityhub_mixins.CfnAutomationRuleV2PropsMixin.DateFilterProperty(
                    date_range=securityhub_mixins.CfnAutomationRuleV2PropsMixin.DateRangeProperty(
                        unit="unit",
                        value=123
                    ),
                    end="end",
                    start="start"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__64cd3498225ef1f5db7396e7502e89a686745f296b4bbde01699c5a83ab34fa4)
                check_type(argname="argument date_range", value=date_range, expected_type=type_hints["date_range"])
                check_type(argname="argument end", value=end, expected_type=type_hints["end"])
                check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if date_range is not None:
                self._values["date_range"] = date_range
            if end is not None:
                self._values["end"] = end
            if start is not None:
                self._values["start"] = start

        @builtins.property
        def date_range(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.DateRangeProperty"]]:
            '''A date range for the date filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-datefilter.html#cfn-securityhub-automationrulev2-datefilter-daterange
            '''
            result = self._values.get("date_range")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.DateRangeProperty"]], result)

        @builtins.property
        def end(self) -> typing.Optional[builtins.str]:
            '''A timestamp that provides the end date for the date filter.

            For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-datefilter.html#cfn-securityhub-automationrulev2-datefilter-end
            '''
            result = self._values.get("end")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start(self) -> typing.Optional[builtins.str]:
            '''A timestamp that provides the start date for the date filter.

            For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-datefilter.html#cfn-securityhub-automationrulev2-datefilter-start
            '''
            result = self._values.get("start")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DateFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRuleV2PropsMixin.DateRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"unit": "unit", "value": "value"},
    )
    class DateRangeProperty:
        def __init__(
            self,
            *,
            unit: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A date range for the date filter.

            :param unit: A date range unit for the date filter.
            :param value: A date range value for the date filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-daterange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                date_range_property = securityhub_mixins.CfnAutomationRuleV2PropsMixin.DateRangeProperty(
                    unit="unit",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__82e9e1f885af03664275a31b1e42d75c036733ea2ef9ce19143b89a8b6ec8b26)
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if unit is not None:
                self._values["unit"] = unit
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''A date range unit for the date filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-daterange.html#cfn-securityhub-automationrulev2-daterange-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''A date range value for the date filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-daterange.html#cfn-securityhub-automationrulev2-daterange-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DateRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRuleV2PropsMixin.ExternalIntegrationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"connector_arn": "connectorArn"},
    )
    class ExternalIntegrationConfigurationProperty:
        def __init__(
            self,
            *,
            connector_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The settings for integrating automation rule actions with external systems or service.

            :param connector_arn: The ARN of the connector that establishes the integration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-externalintegrationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                external_integration_configuration_property = securityhub_mixins.CfnAutomationRuleV2PropsMixin.ExternalIntegrationConfigurationProperty(
                    connector_arn="connectorArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__132a13ec3c8311d3f3566f788d9037f9b65e87d870ab887fa10b541e4c98dda7)
                check_type(argname="argument connector_arn", value=connector_arn, expected_type=type_hints["connector_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connector_arn is not None:
                self._values["connector_arn"] = connector_arn

        @builtins.property
        def connector_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the connector that establishes the integration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-externalintegrationconfiguration.html#cfn-securityhub-automationrulev2-externalintegrationconfiguration-connectorarn
            '''
            result = self._values.get("connector_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExternalIntegrationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRuleV2PropsMixin.MapFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"comparison": "comparison", "key": "key", "value": "value"},
    )
    class MapFilterProperty:
        def __init__(
            self,
            *,
            comparison: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A map filter for filtering Security Hub findings.

            Each map filter provides the field to check for, the value to check for, and the comparison operator.

            :param comparison: The condition to apply to the key value when filtering Security Hub findings with a map filter. To search for values that have the filter value, use one of the following comparison operators: - To search for values that include the filter value, use ``CONTAINS`` . For example, for the ``ResourceTags`` field, the filter ``Department CONTAINS Security`` matches findings that include the value ``Security`` for the ``Department`` tag. In the same example, a finding with a value of ``Security team`` for the ``Department`` tag is a match. - To search for values that exactly match the filter value, use ``EQUALS`` . For example, for the ``ResourceTags`` field, the filter ``Department EQUALS Security`` matches findings that have the value ``Security`` for the ``Department`` tag. ``CONTAINS`` and ``EQUALS`` filters on the same field are joined by ``OR`` . A finding matches if it matches any one of those filters. For example, the filters ``Department CONTAINS Security OR Department CONTAINS Finance`` match a finding that includes either ``Security`` , ``Finance`` , or both values. To search for values that don't have the filter value, use one of the following comparison operators: - To search for values that exclude the filter value, use ``NOT_CONTAINS`` . For example, for the ``ResourceTags`` field, the filter ``Department NOT_CONTAINS Finance`` matches findings that exclude the value ``Finance`` for the ``Department`` tag. - To search for values other than the filter value, use ``NOT_EQUALS`` . For example, for the ``ResourceTags`` field, the filter ``Department NOT_EQUALS Finance`` matches findings that don’t have the value ``Finance`` for the ``Department`` tag. ``NOT_CONTAINS`` and ``NOT_EQUALS`` filters on the same field are joined by ``AND`` . A finding matches only if it matches all of those filters. For example, the filters ``Department NOT_CONTAINS Security AND Department NOT_CONTAINS Finance`` match a finding that excludes both the ``Security`` and ``Finance`` values. ``CONTAINS`` filters can only be used with other ``CONTAINS`` filters. ``NOT_CONTAINS`` filters can only be used with other ``NOT_CONTAINS`` filters. You can’t have both a ``CONTAINS`` filter and a ``NOT_CONTAINS`` filter on the same field. Similarly, you can’t have both an ``EQUALS`` filter and a ``NOT_EQUALS`` filter on the same field. Combining filters in this way returns an error. ``CONTAINS`` and ``NOT_CONTAINS`` operators can be used only with automation rules. For more information, see `Automation rules <https://docs.aws.amazon.com/securityhub/latest/userguide/automation-rules.html>`_ in the *Security Hub User Guide* .
            :param key: The key of the map filter. For example, for ``ResourceTags`` , ``Key`` identifies the name of the tag. For ``UserDefinedFields`` , ``Key`` is the name of the field.
            :param value: The value for the key in the map filter. Filter values are case sensitive. For example, one of the values for a tag called ``Department`` might be ``Security`` . If you provide ``security`` as the filter value, then there's no match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-mapfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                map_filter_property = securityhub_mixins.CfnAutomationRuleV2PropsMixin.MapFilterProperty(
                    comparison="comparison",
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fb7145a119909f83b1489396d9999910a45e7d3197a046bafabd777f208dc3b8)
                check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparison is not None:
                self._values["comparison"] = comparison
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def comparison(self) -> typing.Optional[builtins.str]:
            '''The condition to apply to the key value when filtering Security Hub findings with a map filter.

            To search for values that have the filter value, use one of the following comparison operators:

            - To search for values that include the filter value, use ``CONTAINS`` . For example, for the ``ResourceTags`` field, the filter ``Department CONTAINS Security`` matches findings that include the value ``Security`` for the ``Department`` tag. In the same example, a finding with a value of ``Security team`` for the ``Department`` tag is a match.
            - To search for values that exactly match the filter value, use ``EQUALS`` . For example, for the ``ResourceTags`` field, the filter ``Department EQUALS Security`` matches findings that have the value ``Security`` for the ``Department`` tag.

            ``CONTAINS`` and ``EQUALS`` filters on the same field are joined by ``OR`` . A finding matches if it matches any one of those filters. For example, the filters ``Department CONTAINS Security OR Department CONTAINS Finance`` match a finding that includes either ``Security`` , ``Finance`` , or both values.

            To search for values that don't have the filter value, use one of the following comparison operators:

            - To search for values that exclude the filter value, use ``NOT_CONTAINS`` . For example, for the ``ResourceTags`` field, the filter ``Department NOT_CONTAINS Finance`` matches findings that exclude the value ``Finance`` for the ``Department`` tag.
            - To search for values other than the filter value, use ``NOT_EQUALS`` . For example, for the ``ResourceTags`` field, the filter ``Department NOT_EQUALS Finance`` matches findings that don’t have the value ``Finance`` for the ``Department`` tag.

            ``NOT_CONTAINS`` and ``NOT_EQUALS`` filters on the same field are joined by ``AND`` . A finding matches only if it matches all of those filters. For example, the filters ``Department NOT_CONTAINS Security AND Department NOT_CONTAINS Finance`` match a finding that excludes both the ``Security`` and ``Finance`` values.

            ``CONTAINS`` filters can only be used with other ``CONTAINS`` filters. ``NOT_CONTAINS`` filters can only be used with other ``NOT_CONTAINS`` filters.

            You can’t have both a ``CONTAINS`` filter and a ``NOT_CONTAINS`` filter on the same field. Similarly, you can’t have both an ``EQUALS`` filter and a ``NOT_EQUALS`` filter on the same field. Combining filters in this way returns an error.

            ``CONTAINS`` and ``NOT_CONTAINS`` operators can be used only with automation rules. For more information, see `Automation rules <https://docs.aws.amazon.com/securityhub/latest/userguide/automation-rules.html>`_ in the *Security Hub User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-mapfilter.html#cfn-securityhub-automationrulev2-mapfilter-comparison
            '''
            result = self._values.get("comparison")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key of the map filter.

            For example, for ``ResourceTags`` , ``Key`` identifies the name of the tag. For ``UserDefinedFields`` , ``Key`` is the name of the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-mapfilter.html#cfn-securityhub-automationrulev2-mapfilter-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value for the key in the map filter.

            Filter values are case sensitive. For example, one of the values for a tag called ``Department`` might be ``Security`` . If you provide ``security`` as the filter value, then there's no match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-mapfilter.html#cfn-securityhub-automationrulev2-mapfilter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MapFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRuleV2PropsMixin.NumberFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"eq": "eq", "gte": "gte", "lte": "lte"},
    )
    class NumberFilterProperty:
        def __init__(
            self,
            *,
            eq: typing.Optional[jsii.Number] = None,
            gte: typing.Optional[jsii.Number] = None,
            lte: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A number filter for querying findings.

            :param eq: The equal-to condition to be applied to a single field when querying for findings.
            :param gte: The greater-than-equal condition to be applied to a single field when querying for findings.
            :param lte: The less-than-equal condition to be applied to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-numberfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                number_filter_property = securityhub_mixins.CfnAutomationRuleV2PropsMixin.NumberFilterProperty(
                    eq=123,
                    gte=123,
                    lte=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cd1d5a8d0a884dc06297e8458dc5067836aa260871c82c300a95d3f6b4126355)
                check_type(argname="argument eq", value=eq, expected_type=type_hints["eq"])
                check_type(argname="argument gte", value=gte, expected_type=type_hints["gte"])
                check_type(argname="argument lte", value=lte, expected_type=type_hints["lte"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if eq is not None:
                self._values["eq"] = eq
            if gte is not None:
                self._values["gte"] = gte
            if lte is not None:
                self._values["lte"] = lte

        @builtins.property
        def eq(self) -> typing.Optional[jsii.Number]:
            '''The equal-to condition to be applied to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-numberfilter.html#cfn-securityhub-automationrulev2-numberfilter-eq
            '''
            result = self._values.get("eq")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def gte(self) -> typing.Optional[jsii.Number]:
            '''The greater-than-equal condition to be applied to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-numberfilter.html#cfn-securityhub-automationrulev2-numberfilter-gte
            '''
            result = self._values.get("gte")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def lte(self) -> typing.Optional[jsii.Number]:
            '''The less-than-equal condition to be applied to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-numberfilter.html#cfn-securityhub-automationrulev2-numberfilter-lte
            '''
            result = self._values.get("lte")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NumberFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRuleV2PropsMixin.OcsfBooleanFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"field_name": "fieldName", "filter": "filter"},
    )
    class OcsfBooleanFilterProperty:
        def __init__(
            self,
            *,
            field_name: typing.Optional[builtins.str] = None,
            filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRuleV2PropsMixin.BooleanFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Enables filtering of security findings based on boolean field values in OCSF.

            :param field_name: The name of the field.
            :param filter: Enables filtering of security findings based on boolean field values in OCSF.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-ocsfbooleanfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                ocsf_boolean_filter_property = securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfBooleanFilterProperty(
                    field_name="fieldName",
                    filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.BooleanFilterProperty(
                        value=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a84fa5467bc5586d94f4dc420529fd5c80f7efbcc01d0cc6d5c5b7c008c0022)
                check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if field_name is not None:
                self._values["field_name"] = field_name
            if filter is not None:
                self._values["filter"] = filter

        @builtins.property
        def field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-ocsfbooleanfilter.html#cfn-securityhub-automationrulev2-ocsfbooleanfilter-fieldname
            '''
            result = self._values.get("field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.BooleanFilterProperty"]]:
            '''Enables filtering of security findings based on boolean field values in OCSF.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-ocsfbooleanfilter.html#cfn-securityhub-automationrulev2-ocsfbooleanfilter-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.BooleanFilterProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OcsfBooleanFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRuleV2PropsMixin.OcsfDateFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"field_name": "fieldName", "filter": "filter"},
    )
    class OcsfDateFilterProperty:
        def __init__(
            self,
            *,
            field_name: typing.Optional[builtins.str] = None,
            filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRuleV2PropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Enables filtering of security findings based on date and timestamp fields in OCSF.

            :param field_name: The name of the field.
            :param filter: Enables filtering of security findings based on date and timestamp fields in OCSF.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-ocsfdatefilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                ocsf_date_filter_property = securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfDateFilterProperty(
                    field_name="fieldName",
                    filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnAutomationRuleV2PropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__100d8a84541df070a70ab96b9d8f6ccbbc7317ce35bfe72aa5671b58fbe2fe5b)
                check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if field_name is not None:
                self._values["field_name"] = field_name
            if filter is not None:
                self._values["filter"] = filter

        @builtins.property
        def field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-ocsfdatefilter.html#cfn-securityhub-automationrulev2-ocsfdatefilter-fieldname
            '''
            result = self._values.get("field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.DateFilterProperty"]]:
            '''Enables filtering of security findings based on date and timestamp fields in OCSF.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-ocsfdatefilter.html#cfn-securityhub-automationrulev2-ocsfdatefilter-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.DateFilterProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OcsfDateFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRuleV2PropsMixin.OcsfFindingFiltersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "composite_filters": "compositeFilters",
            "composite_operator": "compositeOperator",
        },
    )
    class OcsfFindingFiltersProperty:
        def __init__(
            self,
            *,
            composite_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRuleV2PropsMixin.CompositeFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            composite_operator: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the filtering criteria for security findings using OCSF.

            :param composite_filters: Enables the creation of complex filtering conditions by combining filter criteria.
            :param composite_operator: The logical operators used to combine the filtering on multiple ``CompositeFilters`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-ocsffindingfilters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                ocsf_finding_filters_property = securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfFindingFiltersProperty(
                    composite_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.CompositeFilterProperty(
                        boolean_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfBooleanFilterProperty(
                            field_name="fieldName",
                            filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.BooleanFilterProperty(
                                value=False
                            )
                        )],
                        date_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfDateFilterProperty(
                            field_name="fieldName",
                            filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.DateFilterProperty(
                                date_range=securityhub_mixins.CfnAutomationRuleV2PropsMixin.DateRangeProperty(
                                    unit="unit",
                                    value=123
                                ),
                                end="end",
                                start="start"
                            )
                        )],
                        map_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfMapFilterProperty(
                            field_name="fieldName",
                            filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.MapFilterProperty(
                                comparison="comparison",
                                key="key",
                                value="value"
                            )
                        )],
                        number_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfNumberFilterProperty(
                            field_name="fieldName",
                            filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.NumberFilterProperty(
                                eq=123,
                                gte=123,
                                lte=123
                            )
                        )],
                        operator="operator",
                        string_filters=[securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfStringFilterProperty(
                            field_name="fieldName",
                            filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.StringFilterProperty(
                                comparison="comparison",
                                value="value"
                            )
                        )]
                    )],
                    composite_operator="compositeOperator"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4e9abbd14e681a3715371939d3dc05934f3f9e5a9edb34c097b7e76a7aabde2f)
                check_type(argname="argument composite_filters", value=composite_filters, expected_type=type_hints["composite_filters"])
                check_type(argname="argument composite_operator", value=composite_operator, expected_type=type_hints["composite_operator"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if composite_filters is not None:
                self._values["composite_filters"] = composite_filters
            if composite_operator is not None:
                self._values["composite_operator"] = composite_operator

        @builtins.property
        def composite_filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.CompositeFilterProperty"]]]]:
            '''Enables the creation of complex filtering conditions by combining filter criteria.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-ocsffindingfilters.html#cfn-securityhub-automationrulev2-ocsffindingfilters-compositefilters
            '''
            result = self._values.get("composite_filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.CompositeFilterProperty"]]]], result)

        @builtins.property
        def composite_operator(self) -> typing.Optional[builtins.str]:
            '''The logical operators used to combine the filtering on multiple ``CompositeFilters`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-ocsffindingfilters.html#cfn-securityhub-automationrulev2-ocsffindingfilters-compositeoperator
            '''
            result = self._values.get("composite_operator")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OcsfFindingFiltersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRuleV2PropsMixin.OcsfMapFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"field_name": "fieldName", "filter": "filter"},
    )
    class OcsfMapFilterProperty:
        def __init__(
            self,
            *,
            field_name: typing.Optional[builtins.str] = None,
            filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRuleV2PropsMixin.MapFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Enables filtering of security findings based on map field values in OCSF.

            :param field_name: The name of the field.
            :param filter: Enables filtering of security findings based on map field values in OCSF.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-ocsfmapfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                ocsf_map_filter_property = securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfMapFilterProperty(
                    field_name="fieldName",
                    filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.MapFilterProperty(
                        comparison="comparison",
                        key="key",
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4937851c68bd1c796025a3d3a917d11501c9785832334283ee57ea0d9b350ca1)
                check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if field_name is not None:
                self._values["field_name"] = field_name
            if filter is not None:
                self._values["filter"] = filter

        @builtins.property
        def field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-ocsfmapfilter.html#cfn-securityhub-automationrulev2-ocsfmapfilter-fieldname
            '''
            result = self._values.get("field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.MapFilterProperty"]]:
            '''Enables filtering of security findings based on map field values in OCSF.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-ocsfmapfilter.html#cfn-securityhub-automationrulev2-ocsfmapfilter-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.MapFilterProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OcsfMapFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRuleV2PropsMixin.OcsfNumberFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"field_name": "fieldName", "filter": "filter"},
    )
    class OcsfNumberFilterProperty:
        def __init__(
            self,
            *,
            field_name: typing.Optional[builtins.str] = None,
            filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRuleV2PropsMixin.NumberFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Enables filtering of security findings based on numerical field values in OCSF.

            :param field_name: The name of the field.
            :param filter: Enables filtering of security findings based on numerical field values in OCSF.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-ocsfnumberfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                ocsf_number_filter_property = securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfNumberFilterProperty(
                    field_name="fieldName",
                    filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__13a786d7a7db9d2c2715f32c47900a6ccf157404ad71aed5ec7e2c2d6d6313d7)
                check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if field_name is not None:
                self._values["field_name"] = field_name
            if filter is not None:
                self._values["filter"] = filter

        @builtins.property
        def field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-ocsfnumberfilter.html#cfn-securityhub-automationrulev2-ocsfnumberfilter-fieldname
            '''
            result = self._values.get("field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.NumberFilterProperty"]]:
            '''Enables filtering of security findings based on numerical field values in OCSF.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-ocsfnumberfilter.html#cfn-securityhub-automationrulev2-ocsfnumberfilter-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.NumberFilterProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OcsfNumberFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRuleV2PropsMixin.OcsfStringFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"field_name": "fieldName", "filter": "filter"},
    )
    class OcsfStringFilterProperty:
        def __init__(
            self,
            *,
            field_name: typing.Optional[builtins.str] = None,
            filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAutomationRuleV2PropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Enables filtering of security findings based on string field values in OCSF.

            :param field_name: The name of the field.
            :param filter: Enables filtering of security findings based on string field values in OCSF.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-ocsfstringfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                ocsf_string_filter_property = securityhub_mixins.CfnAutomationRuleV2PropsMixin.OcsfStringFilterProperty(
                    field_name="fieldName",
                    filter=securityhub_mixins.CfnAutomationRuleV2PropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d5861d0c9ca94acbe1fa13925e1d37574617eefac15192f106468b646e38b63e)
                check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if field_name is not None:
                self._values["field_name"] = field_name
            if filter is not None:
                self._values["filter"] = filter

        @builtins.property
        def field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-ocsfstringfilter.html#cfn-securityhub-automationrulev2-ocsfstringfilter-fieldname
            '''
            result = self._values.get("field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.StringFilterProperty"]]:
            '''Enables filtering of security findings based on string field values in OCSF.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-ocsfstringfilter.html#cfn-securityhub-automationrulev2-ocsfstringfilter-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAutomationRuleV2PropsMixin.StringFilterProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OcsfStringFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnAutomationRuleV2PropsMixin.StringFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"comparison": "comparison", "value": "value"},
    )
    class StringFilterProperty:
        def __init__(
            self,
            *,
            comparison: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A string filter for filtering Security Hub findings.

            :param comparison: The condition to apply to a string value when filtering Security Hub findings. To search for values that have the filter value, use one of the following comparison operators: - To search for values that include the filter value, use ``CONTAINS`` . For example, the filter ``Title CONTAINS CloudFront`` matches findings that have a ``Title`` that includes the string CloudFront. - To search for values that exactly match the filter value, use ``EQUALS`` . For example, the filter ``AwsAccountId EQUALS 123456789012`` only matches findings that have an account ID of ``123456789012`` . - To search for values that start with the filter value, use ``PREFIX`` . For example, the filter ``ResourceRegion PREFIX us`` matches findings that have a ``ResourceRegion`` that starts with ``us`` . A ``ResourceRegion`` that starts with a different value, such as ``af`` , ``ap`` , or ``ca`` , doesn't match. ``CONTAINS`` , ``EQUALS`` , and ``PREFIX`` filters on the same field are joined by ``OR`` . A finding matches if it matches any one of those filters. For example, the filters ``Title CONTAINS CloudFront OR Title CONTAINS CloudWatch`` match a finding that includes either ``CloudFront`` , ``CloudWatch`` , or both strings in the title. To search for values that don’t have the filter value, use one of the following comparison operators: - To search for values that exclude the filter value, use ``NOT_CONTAINS`` . For example, the filter ``Title NOT_CONTAINS CloudFront`` matches findings that have a ``Title`` that excludes the string CloudFront. - To search for values other than the filter value, use ``NOT_EQUALS`` . For example, the filter ``AwsAccountId NOT_EQUALS 123456789012`` only matches findings that have an account ID other than ``123456789012`` . - To search for values that don't start with the filter value, use ``PREFIX_NOT_EQUALS`` . For example, the filter ``ResourceRegion PREFIX_NOT_EQUALS us`` matches findings with a ``ResourceRegion`` that starts with a value other than ``us`` . ``NOT_CONTAINS`` , ``NOT_EQUALS`` , and ``PREFIX_NOT_EQUALS`` filters on the same field are joined by ``AND`` . A finding matches only if it matches all of those filters. For example, the filters ``Title NOT_CONTAINS CloudFront AND Title NOT_CONTAINS CloudWatch`` match a finding that excludes both ``CloudFront`` and ``CloudWatch`` in the title. You can’t have both a ``CONTAINS`` filter and a ``NOT_CONTAINS`` filter on the same field. Similarly, you can't provide both an ``EQUALS`` filter and a ``NOT_EQUALS`` or ``PREFIX_NOT_EQUALS`` filter on the same field. Combining filters in this way returns an error. ``CONTAINS`` filters can only be used with other ``CONTAINS`` filters. ``NOT_CONTAINS`` filters can only be used with other ``NOT_CONTAINS`` filters. You can combine ``PREFIX`` filters with ``NOT_EQUALS`` or ``PREFIX_NOT_EQUALS`` filters for the same field. Security Hub first processes the ``PREFIX`` filters, and then the ``NOT_EQUALS`` or ``PREFIX_NOT_EQUALS`` filters. For example, for the following filters, Security Hub first identifies findings that have resource types that start with either ``AwsIam`` or ``AwsEc2`` . It then excludes findings that have a resource type of ``AwsIamPolicy`` and findings that have a resource type of ``AwsEc2NetworkInterface`` . - ``ResourceType PREFIX AwsIam`` - ``ResourceType PREFIX AwsEc2`` - ``ResourceType NOT_EQUALS AwsIamPolicy`` - ``ResourceType NOT_EQUALS AwsEc2NetworkInterface`` ``CONTAINS`` and ``NOT_CONTAINS`` operators can be used only with automation rules V1. ``CONTAINS_WORD`` operator is only supported in ``GetFindingsV2`` , ``GetFindingStatisticsV2`` , ``GetResourcesV2`` , and ``GetResourceStatisticsV2`` APIs. For more information, see `Automation rules <https://docs.aws.amazon.com/securityhub/latest/userguide/automation-rules.html>`_ in the *Security Hub User Guide* .
            :param value: The string filter value. Filter values are case sensitive. For example, the product name for control-based findings is ``Security Hub`` . If you provide ``security hub`` as the filter value, there's no match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-stringfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                string_filter_property = securityhub_mixins.CfnAutomationRuleV2PropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9937d4f883461d4a8a0676685218ae1013eda27bd7ad0a856c9aaf064f7ff7db)
                check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparison is not None:
                self._values["comparison"] = comparison
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def comparison(self) -> typing.Optional[builtins.str]:
            '''The condition to apply to a string value when filtering Security Hub findings.

            To search for values that have the filter value, use one of the following comparison operators:

            - To search for values that include the filter value, use ``CONTAINS`` . For example, the filter ``Title CONTAINS CloudFront`` matches findings that have a ``Title`` that includes the string CloudFront.
            - To search for values that exactly match the filter value, use ``EQUALS`` . For example, the filter ``AwsAccountId EQUALS 123456789012`` only matches findings that have an account ID of ``123456789012`` .
            - To search for values that start with the filter value, use ``PREFIX`` . For example, the filter ``ResourceRegion PREFIX us`` matches findings that have a ``ResourceRegion`` that starts with ``us`` . A ``ResourceRegion`` that starts with a different value, such as ``af`` , ``ap`` , or ``ca`` , doesn't match.

            ``CONTAINS`` , ``EQUALS`` , and ``PREFIX`` filters on the same field are joined by ``OR`` . A finding matches if it matches any one of those filters. For example, the filters ``Title CONTAINS CloudFront OR Title CONTAINS CloudWatch`` match a finding that includes either ``CloudFront`` , ``CloudWatch`` , or both strings in the title.

            To search for values that don’t have the filter value, use one of the following comparison operators:

            - To search for values that exclude the filter value, use ``NOT_CONTAINS`` . For example, the filter ``Title NOT_CONTAINS CloudFront`` matches findings that have a ``Title`` that excludes the string CloudFront.
            - To search for values other than the filter value, use ``NOT_EQUALS`` . For example, the filter ``AwsAccountId NOT_EQUALS 123456789012`` only matches findings that have an account ID other than ``123456789012`` .
            - To search for values that don't start with the filter value, use ``PREFIX_NOT_EQUALS`` . For example, the filter ``ResourceRegion PREFIX_NOT_EQUALS us`` matches findings with a ``ResourceRegion`` that starts with a value other than ``us`` .

            ``NOT_CONTAINS`` , ``NOT_EQUALS`` , and ``PREFIX_NOT_EQUALS`` filters on the same field are joined by ``AND`` . A finding matches only if it matches all of those filters. For example, the filters ``Title NOT_CONTAINS CloudFront AND Title NOT_CONTAINS CloudWatch`` match a finding that excludes both ``CloudFront`` and ``CloudWatch`` in the title.

            You can’t have both a ``CONTAINS`` filter and a ``NOT_CONTAINS`` filter on the same field. Similarly, you can't provide both an ``EQUALS`` filter and a ``NOT_EQUALS`` or ``PREFIX_NOT_EQUALS`` filter on the same field. Combining filters in this way returns an error. ``CONTAINS`` filters can only be used with other ``CONTAINS`` filters. ``NOT_CONTAINS`` filters can only be used with other ``NOT_CONTAINS`` filters.

            You can combine ``PREFIX`` filters with ``NOT_EQUALS`` or ``PREFIX_NOT_EQUALS`` filters for the same field. Security Hub first processes the ``PREFIX`` filters, and then the ``NOT_EQUALS`` or ``PREFIX_NOT_EQUALS`` filters.

            For example, for the following filters, Security Hub first identifies findings that have resource types that start with either ``AwsIam`` or ``AwsEc2`` . It then excludes findings that have a resource type of ``AwsIamPolicy`` and findings that have a resource type of ``AwsEc2NetworkInterface`` .

            - ``ResourceType PREFIX AwsIam``
            - ``ResourceType PREFIX AwsEc2``
            - ``ResourceType NOT_EQUALS AwsIamPolicy``
            - ``ResourceType NOT_EQUALS AwsEc2NetworkInterface``

            ``CONTAINS`` and ``NOT_CONTAINS`` operators can be used only with automation rules V1. ``CONTAINS_WORD`` operator is only supported in ``GetFindingsV2`` , ``GetFindingStatisticsV2`` , ``GetResourcesV2`` , and ``GetResourceStatisticsV2`` APIs. For more information, see `Automation rules <https://docs.aws.amazon.com/securityhub/latest/userguide/automation-rules.html>`_ in the *Security Hub User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-stringfilter.html#cfn-securityhub-automationrulev2-stringfilter-comparison
            '''
            result = self._values.get("comparison")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The string filter value.

            Filter values are case sensitive. For example, the product name for control-based findings is ``Security Hub`` . If you provide ``security hub`` as the filter value, there's no match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-automationrulev2-stringfilter.html#cfn-securityhub-automationrulev2-stringfilter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StringFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnConfigurationPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_policy": "configurationPolicy",
        "description": "description",
        "name": "name",
        "tags": "tags",
    },
)
class CfnConfigurationPolicyMixinProps:
    def __init__(
        self,
        *,
        configuration_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationPolicyPropsMixin.PolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnConfigurationPolicyPropsMixin.

        :param configuration_policy: An object that defines how Security Hub is configured. It includes whether Security Hub is enabled or disabled, a list of enabled security standards, a list of enabled or disabled security controls, and a list of custom parameter values for specified controls. If you provide a list of security controls that are enabled in the configuration policy, Security Hub disables all other controls (including newly released controls). If you provide a list of security controls that are disabled in the configuration policy, Security Hub enables all other controls (including newly released controls).
        :param description: The description of the configuration policy.
        :param name: The name of the configuration policy. Alphanumeric characters and the following ASCII characters are permitted: ``-, ., !, *, /`` .
        :param tags: User-defined tags associated with a configuration policy. For more information, see `Tagging Security Hub resources <https://docs.aws.amazon.com/securityhub/latest/userguide/tagging-resources.html>`_ in the *Security Hub user guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-configurationpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
            
            cfn_configuration_policy_mixin_props = securityhub_mixins.CfnConfigurationPolicyMixinProps(
                configuration_policy=securityhub_mixins.CfnConfigurationPolicyPropsMixin.PolicyProperty(
                    security_hub=securityhub_mixins.CfnConfigurationPolicyPropsMixin.SecurityHubPolicyProperty(
                        enabled_standard_identifiers=["enabledStandardIdentifiers"],
                        security_controls_configuration=securityhub_mixins.CfnConfigurationPolicyPropsMixin.SecurityControlsConfigurationProperty(
                            disabled_security_control_identifiers=["disabledSecurityControlIdentifiers"],
                            enabled_security_control_identifiers=["enabledSecurityControlIdentifiers"],
                            security_control_custom_parameters=[securityhub_mixins.CfnConfigurationPolicyPropsMixin.SecurityControlCustomParameterProperty(
                                parameters={
                                    "parameters_key": securityhub_mixins.CfnConfigurationPolicyPropsMixin.ParameterConfigurationProperty(
                                        value=securityhub_mixins.CfnConfigurationPolicyPropsMixin.ParameterValueProperty(
                                            boolean=False,
                                            double=123,
                                            enum="enum",
                                            enum_list=["enumList"],
                                            integer=123,
                                            integer_list=[123],
                                            string="string",
                                            string_list=["stringList"]
                                        ),
                                        value_type="valueType"
                                    )
                                },
                                security_control_id="securityControlId"
                            )]
                        ),
                        service_enabled=False
                    )
                ),
                description="description",
                name="name",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82c67982d5b9eeb31b4268fd7a812fe836420897813487e5ddade98ae1e203d9)
            check_type(argname="argument configuration_policy", value=configuration_policy, expected_type=type_hints["configuration_policy"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration_policy is not None:
            self._values["configuration_policy"] = configuration_policy
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def configuration_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationPolicyPropsMixin.PolicyProperty"]]:
        '''An object that defines how Security Hub is configured.

        It includes whether Security Hub is enabled or disabled, a list of enabled security standards, a list of enabled or disabled security controls, and a list of custom parameter values for specified controls. If you provide a list of security controls that are enabled in the configuration policy, Security Hub disables all other controls (including newly released controls). If you provide a list of security controls that are disabled in the configuration policy, Security Hub enables all other controls (including newly released controls).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-configurationpolicy.html#cfn-securityhub-configurationpolicy-configurationpolicy
        '''
        result = self._values.get("configuration_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationPolicyPropsMixin.PolicyProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the configuration policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-configurationpolicy.html#cfn-securityhub-configurationpolicy-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the configuration policy.

        Alphanumeric characters and the following ASCII characters are permitted: ``-, ., !, *, /`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-configurationpolicy.html#cfn-securityhub-configurationpolicy-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined tags associated with a configuration policy.

        For more information, see `Tagging Security Hub resources <https://docs.aws.amazon.com/securityhub/latest/userguide/tagging-resources.html>`_ in the *Security Hub user guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-configurationpolicy.html#cfn-securityhub-configurationpolicy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConfigurationPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnConfigurationPolicyPropsMixin",
):
    '''The ``AWS::SecurityHub::ConfigurationPolicy`` resource creates a central configuration policy with the defined settings.

    Only the Security Hub delegated administrator can create this resource in the home Region. For more information, see `Central configuration in Security Hub <https://docs.aws.amazon.com/securityhub/latest/userguide/central-configuration-intro.html>`_ in the *Security Hub User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-configurationpolicy.html
    :cloudformationResource: AWS::SecurityHub::ConfigurationPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
        
        cfn_configuration_policy_props_mixin = securityhub_mixins.CfnConfigurationPolicyPropsMixin(securityhub_mixins.CfnConfigurationPolicyMixinProps(
            configuration_policy=securityhub_mixins.CfnConfigurationPolicyPropsMixin.PolicyProperty(
                security_hub=securityhub_mixins.CfnConfigurationPolicyPropsMixin.SecurityHubPolicyProperty(
                    enabled_standard_identifiers=["enabledStandardIdentifiers"],
                    security_controls_configuration=securityhub_mixins.CfnConfigurationPolicyPropsMixin.SecurityControlsConfigurationProperty(
                        disabled_security_control_identifiers=["disabledSecurityControlIdentifiers"],
                        enabled_security_control_identifiers=["enabledSecurityControlIdentifiers"],
                        security_control_custom_parameters=[securityhub_mixins.CfnConfigurationPolicyPropsMixin.SecurityControlCustomParameterProperty(
                            parameters={
                                "parameters_key": securityhub_mixins.CfnConfigurationPolicyPropsMixin.ParameterConfigurationProperty(
                                    value=securityhub_mixins.CfnConfigurationPolicyPropsMixin.ParameterValueProperty(
                                        boolean=False,
                                        double=123,
                                        enum="enum",
                                        enum_list=["enumList"],
                                        integer=123,
                                        integer_list=[123],
                                        string="string",
                                        string_list=["stringList"]
                                    ),
                                    value_type="valueType"
                                )
                            },
                            security_control_id="securityControlId"
                        )]
                    ),
                    service_enabled=False
                )
            ),
            description="description",
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
        props: typing.Union[CfnConfigurationPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecurityHub::ConfigurationPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c7c81e721bb900af9bf7d428c2c2752adea9b5ea90871fbe2ce3a970e8d800)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2db8731ab603f80b44b64a6b266f853bc19959f5c6f60a96cbbc2dec786f166)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a044a2446e8918746c91d966efd523716d0680cd3d64b6912e7919bca21de10)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConfigurationPolicyMixinProps:
        return typing.cast(CfnConfigurationPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnConfigurationPolicyPropsMixin.ParameterConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value", "value_type": "valueType"},
    )
    class ParameterConfigurationProperty:
        def __init__(
            self,
            *,
            value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationPolicyPropsMixin.ParameterValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            value_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that provides the current value of a security control parameter and identifies whether it has been customized.

            :param value: The current value of a control parameter.
            :param value_type: Identifies whether a control parameter uses a custom user-defined value or subscribes to the default Security Hub behavior. When ``ValueType`` is set equal to ``DEFAULT`` , the default behavior can be a specific Security Hub default value, or the default behavior can be to ignore a specific parameter. When ``ValueType`` is set equal to ``DEFAULT`` , Security Hub ignores user-provided input for the ``Value`` field. When ``ValueType`` is set equal to ``CUSTOM`` , the ``Value`` field can't be empty.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-parameterconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                parameter_configuration_property = securityhub_mixins.CfnConfigurationPolicyPropsMixin.ParameterConfigurationProperty(
                    value=securityhub_mixins.CfnConfigurationPolicyPropsMixin.ParameterValueProperty(
                        boolean=False,
                        double=123,
                        enum="enum",
                        enum_list=["enumList"],
                        integer=123,
                        integer_list=[123],
                        string="string",
                        string_list=["stringList"]
                    ),
                    value_type="valueType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7bde4000cb262bb351f3f5d290d5cbe013273260740c7ece9e08061246ac3105)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                check_type(argname="argument value_type", value=value_type, expected_type=type_hints["value_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if value is not None:
                self._values["value"] = value
            if value_type is not None:
                self._values["value_type"] = value_type

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationPolicyPropsMixin.ParameterValueProperty"]]:
            '''The current value of a control parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-parameterconfiguration.html#cfn-securityhub-configurationpolicy-parameterconfiguration-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationPolicyPropsMixin.ParameterValueProperty"]], result)

        @builtins.property
        def value_type(self) -> typing.Optional[builtins.str]:
            '''Identifies whether a control parameter uses a custom user-defined value or subscribes to the default Security Hub behavior.

            When ``ValueType`` is set equal to ``DEFAULT`` , the default behavior can be a specific Security Hub default value, or the default behavior can be to ignore a specific parameter. When ``ValueType`` is set equal to ``DEFAULT`` , Security Hub ignores user-provided input for the ``Value`` field.

            When ``ValueType`` is set equal to ``CUSTOM`` , the ``Value`` field can't be empty.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-parameterconfiguration.html#cfn-securityhub-configurationpolicy-parameterconfiguration-valuetype
            '''
            result = self._values.get("value_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnConfigurationPolicyPropsMixin.ParameterValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "boolean": "boolean",
            "double": "double",
            "enum": "enum",
            "enum_list": "enumList",
            "integer": "integer",
            "integer_list": "integerList",
            "string": "string",
            "string_list": "stringList",
        },
    )
    class ParameterValueProperty:
        def __init__(
            self,
            *,
            boolean: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            double: typing.Optional[jsii.Number] = None,
            enum: typing.Optional[builtins.str] = None,
            enum_list: typing.Optional[typing.Sequence[builtins.str]] = None,
            integer: typing.Optional[jsii.Number] = None,
            integer_list: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
            string: typing.Optional[builtins.str] = None,
            string_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''An object that includes the data type of a security control parameter and its current value.

            :param boolean: A control parameter that is a boolean.
            :param double: A control parameter that is a double.
            :param enum: A control parameter that is an enum.
            :param enum_list: A control parameter that is a list of enums.
            :param integer: A control parameter that is an integer.
            :param integer_list: A control parameter that is a list of integers.
            :param string: A control parameter that is a string.
            :param string_list: A control parameter that is a list of strings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-parametervalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                parameter_value_property = securityhub_mixins.CfnConfigurationPolicyPropsMixin.ParameterValueProperty(
                    boolean=False,
                    double=123,
                    enum="enum",
                    enum_list=["enumList"],
                    integer=123,
                    integer_list=[123],
                    string="string",
                    string_list=["stringList"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e99a664ea7a26fbe10e27f1366544baf139354b31677f334764990f528fbf2a4)
                check_type(argname="argument boolean", value=boolean, expected_type=type_hints["boolean"])
                check_type(argname="argument double", value=double, expected_type=type_hints["double"])
                check_type(argname="argument enum", value=enum, expected_type=type_hints["enum"])
                check_type(argname="argument enum_list", value=enum_list, expected_type=type_hints["enum_list"])
                check_type(argname="argument integer", value=integer, expected_type=type_hints["integer"])
                check_type(argname="argument integer_list", value=integer_list, expected_type=type_hints["integer_list"])
                check_type(argname="argument string", value=string, expected_type=type_hints["string"])
                check_type(argname="argument string_list", value=string_list, expected_type=type_hints["string_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if boolean is not None:
                self._values["boolean"] = boolean
            if double is not None:
                self._values["double"] = double
            if enum is not None:
                self._values["enum"] = enum
            if enum_list is not None:
                self._values["enum_list"] = enum_list
            if integer is not None:
                self._values["integer"] = integer
            if integer_list is not None:
                self._values["integer_list"] = integer_list
            if string is not None:
                self._values["string"] = string
            if string_list is not None:
                self._values["string_list"] = string_list

        @builtins.property
        def boolean(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A control parameter that is a boolean.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-parametervalue.html#cfn-securityhub-configurationpolicy-parametervalue-boolean
            '''
            result = self._values.get("boolean")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def double(self) -> typing.Optional[jsii.Number]:
            '''A control parameter that is a double.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-parametervalue.html#cfn-securityhub-configurationpolicy-parametervalue-double
            '''
            result = self._values.get("double")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def enum(self) -> typing.Optional[builtins.str]:
            '''A control parameter that is an enum.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-parametervalue.html#cfn-securityhub-configurationpolicy-parametervalue-enum
            '''
            result = self._values.get("enum")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enum_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A control parameter that is a list of enums.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-parametervalue.html#cfn-securityhub-configurationpolicy-parametervalue-enumlist
            '''
            result = self._values.get("enum_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def integer(self) -> typing.Optional[jsii.Number]:
            '''A control parameter that is an integer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-parametervalue.html#cfn-securityhub-configurationpolicy-parametervalue-integer
            '''
            result = self._values.get("integer")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def integer_list(
            self,
        ) -> typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]]:
            '''A control parameter that is a list of integers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-parametervalue.html#cfn-securityhub-configurationpolicy-parametervalue-integerlist
            '''
            result = self._values.get("integer_list")
            return typing.cast(typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def string(self) -> typing.Optional[builtins.str]:
            '''A control parameter that is a string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-parametervalue.html#cfn-securityhub-configurationpolicy-parametervalue-string
            '''
            result = self._values.get("string")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def string_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A control parameter that is a list of strings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-parametervalue.html#cfn-securityhub-configurationpolicy-parametervalue-stringlist
            '''
            result = self._values.get("string_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnConfigurationPolicyPropsMixin.PolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"security_hub": "securityHub"},
    )
    class PolicyProperty:
        def __init__(
            self,
            *,
            security_hub: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationPolicyPropsMixin.SecurityHubPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that defines how Security Hub is configured.

            It includes whether Security Hub is enabled or disabled, a list of enabled security standards, a list of enabled or disabled security controls, and a list of custom parameter values for specified controls. If you provide a list of security controls that are enabled in the configuration policy, Security Hub disables all other controls (including newly released controls). If you provide a list of security controls that are disabled in the configuration policy, Security Hub enables all other controls (including newly released controls).

            :param security_hub: The AWS service that the configuration policy applies to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-policy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                policy_property = securityhub_mixins.CfnConfigurationPolicyPropsMixin.PolicyProperty(
                    security_hub=securityhub_mixins.CfnConfigurationPolicyPropsMixin.SecurityHubPolicyProperty(
                        enabled_standard_identifiers=["enabledStandardIdentifiers"],
                        security_controls_configuration=securityhub_mixins.CfnConfigurationPolicyPropsMixin.SecurityControlsConfigurationProperty(
                            disabled_security_control_identifiers=["disabledSecurityControlIdentifiers"],
                            enabled_security_control_identifiers=["enabledSecurityControlIdentifiers"],
                            security_control_custom_parameters=[securityhub_mixins.CfnConfigurationPolicyPropsMixin.SecurityControlCustomParameterProperty(
                                parameters={
                                    "parameters_key": securityhub_mixins.CfnConfigurationPolicyPropsMixin.ParameterConfigurationProperty(
                                        value=securityhub_mixins.CfnConfigurationPolicyPropsMixin.ParameterValueProperty(
                                            boolean=False,
                                            double=123,
                                            enum="enum",
                                            enum_list=["enumList"],
                                            integer=123,
                                            integer_list=[123],
                                            string="string",
                                            string_list=["stringList"]
                                        ),
                                        value_type="valueType"
                                    )
                                },
                                security_control_id="securityControlId"
                            )]
                        ),
                        service_enabled=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cb8f5063963535e82785bc2685c614f68c3327834f3ace3d20e83efa4dae1969)
                check_type(argname="argument security_hub", value=security_hub, expected_type=type_hints["security_hub"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_hub is not None:
                self._values["security_hub"] = security_hub

        @builtins.property
        def security_hub(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationPolicyPropsMixin.SecurityHubPolicyProperty"]]:
            '''The AWS service that the configuration policy applies to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-policy.html#cfn-securityhub-configurationpolicy-policy-securityhub
            '''
            result = self._values.get("security_hub")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationPolicyPropsMixin.SecurityHubPolicyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnConfigurationPolicyPropsMixin.SecurityControlCustomParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameters": "parameters",
            "security_control_id": "securityControlId",
        },
    )
    class SecurityControlCustomParameterProperty:
        def __init__(
            self,
            *,
            parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationPolicyPropsMixin.ParameterConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            security_control_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A list of security controls and control parameter values that are included in a configuration policy.

            :param parameters: An object that specifies parameter values for a control in a configuration policy.
            :param security_control_id: The ID of the security control.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-securitycontrolcustomparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                security_control_custom_parameter_property = securityhub_mixins.CfnConfigurationPolicyPropsMixin.SecurityControlCustomParameterProperty(
                    parameters={
                        "parameters_key": securityhub_mixins.CfnConfigurationPolicyPropsMixin.ParameterConfigurationProperty(
                            value=securityhub_mixins.CfnConfigurationPolicyPropsMixin.ParameterValueProperty(
                                boolean=False,
                                double=123,
                                enum="enum",
                                enum_list=["enumList"],
                                integer=123,
                                integer_list=[123],
                                string="string",
                                string_list=["stringList"]
                            ),
                            value_type="valueType"
                        )
                    },
                    security_control_id="securityControlId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d9390657837a2f432cce4ea1dfe29cd420bc5c185e7c3d1508c55f331102e73f)
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument security_control_id", value=security_control_id, expected_type=type_hints["security_control_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parameters is not None:
                self._values["parameters"] = parameters
            if security_control_id is not None:
                self._values["security_control_id"] = security_control_id

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationPolicyPropsMixin.ParameterConfigurationProperty"]]]]:
            '''An object that specifies parameter values for a control in a configuration policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-securitycontrolcustomparameter.html#cfn-securityhub-configurationpolicy-securitycontrolcustomparameter-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationPolicyPropsMixin.ParameterConfigurationProperty"]]]], result)

        @builtins.property
        def security_control_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the security control.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-securitycontrolcustomparameter.html#cfn-securityhub-configurationpolicy-securitycontrolcustomparameter-securitycontrolid
            '''
            result = self._values.get("security_control_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecurityControlCustomParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnConfigurationPolicyPropsMixin.SecurityControlsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "disabled_security_control_identifiers": "disabledSecurityControlIdentifiers",
            "enabled_security_control_identifiers": "enabledSecurityControlIdentifiers",
            "security_control_custom_parameters": "securityControlCustomParameters",
        },
    )
    class SecurityControlsConfigurationProperty:
        def __init__(
            self,
            *,
            disabled_security_control_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
            enabled_security_control_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
            security_control_custom_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationPolicyPropsMixin.SecurityControlCustomParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''An object that defines which security controls are enabled in an Security Hub configuration policy.

            The enablement status of a control is aligned across all of the enabled standards in an account.

            This property is required only if ``ServiceEnabled`` is set to ``true`` in your configuration policy.

            :param disabled_security_control_identifiers: A list of security controls that are disabled in the configuration policy. Provide only one of ``EnabledSecurityControlIdentifiers`` or ``DisabledSecurityControlIdentifiers`` . If you provide ``DisabledSecurityControlIdentifiers`` , Security Hub enables all other controls not in the list, and enables `AutoEnableControls <https://docs.aws.amazon.com/securityhub/1.0/APIReference/API_UpdateSecurityHubConfiguration.html#securityhub-UpdateSecurityHubConfiguration-request-AutoEnableControls>`_ .
            :param enabled_security_control_identifiers: A list of security controls that are enabled in the configuration policy. Provide only one of ``EnabledSecurityControlIdentifiers`` or ``DisabledSecurityControlIdentifiers`` . If you provide ``EnabledSecurityControlIdentifiers`` , Security Hub disables all other controls not in the list, and disables `AutoEnableControls <https://docs.aws.amazon.com/securityhub/1.0/APIReference/API_UpdateSecurityHubConfiguration.html#securityhub-UpdateSecurityHubConfiguration-request-AutoEnableControls>`_ .
            :param security_control_custom_parameters: A list of security controls and control parameter values that are included in a configuration policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-securitycontrolsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                security_controls_configuration_property = securityhub_mixins.CfnConfigurationPolicyPropsMixin.SecurityControlsConfigurationProperty(
                    disabled_security_control_identifiers=["disabledSecurityControlIdentifiers"],
                    enabled_security_control_identifiers=["enabledSecurityControlIdentifiers"],
                    security_control_custom_parameters=[securityhub_mixins.CfnConfigurationPolicyPropsMixin.SecurityControlCustomParameterProperty(
                        parameters={
                            "parameters_key": securityhub_mixins.CfnConfigurationPolicyPropsMixin.ParameterConfigurationProperty(
                                value=securityhub_mixins.CfnConfigurationPolicyPropsMixin.ParameterValueProperty(
                                    boolean=False,
                                    double=123,
                                    enum="enum",
                                    enum_list=["enumList"],
                                    integer=123,
                                    integer_list=[123],
                                    string="string",
                                    string_list=["stringList"]
                                ),
                                value_type="valueType"
                            )
                        },
                        security_control_id="securityControlId"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__87ee235ad6ff1e9193ce9097890b6cb1e4fd139833d341d4ae6eb678de4656ff)
                check_type(argname="argument disabled_security_control_identifiers", value=disabled_security_control_identifiers, expected_type=type_hints["disabled_security_control_identifiers"])
                check_type(argname="argument enabled_security_control_identifiers", value=enabled_security_control_identifiers, expected_type=type_hints["enabled_security_control_identifiers"])
                check_type(argname="argument security_control_custom_parameters", value=security_control_custom_parameters, expected_type=type_hints["security_control_custom_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if disabled_security_control_identifiers is not None:
                self._values["disabled_security_control_identifiers"] = disabled_security_control_identifiers
            if enabled_security_control_identifiers is not None:
                self._values["enabled_security_control_identifiers"] = enabled_security_control_identifiers
            if security_control_custom_parameters is not None:
                self._values["security_control_custom_parameters"] = security_control_custom_parameters

        @builtins.property
        def disabled_security_control_identifiers(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of security controls that are disabled in the configuration policy.

            Provide only one of ``EnabledSecurityControlIdentifiers`` or ``DisabledSecurityControlIdentifiers`` .

            If you provide ``DisabledSecurityControlIdentifiers`` , Security Hub enables all other controls not in the list, and enables `AutoEnableControls <https://docs.aws.amazon.com/securityhub/1.0/APIReference/API_UpdateSecurityHubConfiguration.html#securityhub-UpdateSecurityHubConfiguration-request-AutoEnableControls>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-securitycontrolsconfiguration.html#cfn-securityhub-configurationpolicy-securitycontrolsconfiguration-disabledsecuritycontrolidentifiers
            '''
            result = self._values.get("disabled_security_control_identifiers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def enabled_security_control_identifiers(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of security controls that are enabled in the configuration policy.

            Provide only one of ``EnabledSecurityControlIdentifiers`` or ``DisabledSecurityControlIdentifiers`` .

            If you provide ``EnabledSecurityControlIdentifiers`` , Security Hub disables all other controls not in the list, and disables `AutoEnableControls <https://docs.aws.amazon.com/securityhub/1.0/APIReference/API_UpdateSecurityHubConfiguration.html#securityhub-UpdateSecurityHubConfiguration-request-AutoEnableControls>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-securitycontrolsconfiguration.html#cfn-securityhub-configurationpolicy-securitycontrolsconfiguration-enabledsecuritycontrolidentifiers
            '''
            result = self._values.get("enabled_security_control_identifiers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def security_control_custom_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationPolicyPropsMixin.SecurityControlCustomParameterProperty"]]]]:
            '''A list of security controls and control parameter values that are included in a configuration policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-securitycontrolsconfiguration.html#cfn-securityhub-configurationpolicy-securitycontrolsconfiguration-securitycontrolcustomparameters
            '''
            result = self._values.get("security_control_custom_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationPolicyPropsMixin.SecurityControlCustomParameterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecurityControlsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnConfigurationPolicyPropsMixin.SecurityHubPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled_standard_identifiers": "enabledStandardIdentifiers",
            "security_controls_configuration": "securityControlsConfiguration",
            "service_enabled": "serviceEnabled",
        },
    )
    class SecurityHubPolicyProperty:
        def __init__(
            self,
            *,
            enabled_standard_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
            security_controls_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationPolicyPropsMixin.SecurityControlsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''An object that defines how Security Hub is configured.

            The configuration policy includes whether Security Hub is enabled or disabled, a list of enabled security standards, a list of enabled or disabled security controls, and a list of custom parameter values for specified controls. If you provide a list of security controls that are enabled in the configuration policy, Security Hub disables all other controls (including newly released controls). If you provide a list of security controls that are disabled in the configuration policy, Security Hub enables all other controls (including newly released controls).

            :param enabled_standard_identifiers: A list that defines which security standards are enabled in the configuration policy. This property is required only if ``ServiceEnabled`` is set to ``true`` in your configuration policy.
            :param security_controls_configuration: An object that defines which security controls are enabled in the configuration policy. The enablement status of a control is aligned across all of the enabled standards in an account. This property is required only if ``ServiceEnabled`` is set to true in your configuration policy.
            :param service_enabled: Indicates whether Security Hub is enabled in the policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-securityhubpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                security_hub_policy_property = securityhub_mixins.CfnConfigurationPolicyPropsMixin.SecurityHubPolicyProperty(
                    enabled_standard_identifiers=["enabledStandardIdentifiers"],
                    security_controls_configuration=securityhub_mixins.CfnConfigurationPolicyPropsMixin.SecurityControlsConfigurationProperty(
                        disabled_security_control_identifiers=["disabledSecurityControlIdentifiers"],
                        enabled_security_control_identifiers=["enabledSecurityControlIdentifiers"],
                        security_control_custom_parameters=[securityhub_mixins.CfnConfigurationPolicyPropsMixin.SecurityControlCustomParameterProperty(
                            parameters={
                                "parameters_key": securityhub_mixins.CfnConfigurationPolicyPropsMixin.ParameterConfigurationProperty(
                                    value=securityhub_mixins.CfnConfigurationPolicyPropsMixin.ParameterValueProperty(
                                        boolean=False,
                                        double=123,
                                        enum="enum",
                                        enum_list=["enumList"],
                                        integer=123,
                                        integer_list=[123],
                                        string="string",
                                        string_list=["stringList"]
                                    ),
                                    value_type="valueType"
                                )
                            },
                            security_control_id="securityControlId"
                        )]
                    ),
                    service_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ff3f55cf550c41cd67ddd71b073a51ba5a935699977851da551d194a17ef1091)
                check_type(argname="argument enabled_standard_identifiers", value=enabled_standard_identifiers, expected_type=type_hints["enabled_standard_identifiers"])
                check_type(argname="argument security_controls_configuration", value=security_controls_configuration, expected_type=type_hints["security_controls_configuration"])
                check_type(argname="argument service_enabled", value=service_enabled, expected_type=type_hints["service_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled_standard_identifiers is not None:
                self._values["enabled_standard_identifiers"] = enabled_standard_identifiers
            if security_controls_configuration is not None:
                self._values["security_controls_configuration"] = security_controls_configuration
            if service_enabled is not None:
                self._values["service_enabled"] = service_enabled

        @builtins.property
        def enabled_standard_identifiers(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list that defines which security standards are enabled in the configuration policy.

            This property is required only if ``ServiceEnabled`` is set to ``true`` in your configuration policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-securityhubpolicy.html#cfn-securityhub-configurationpolicy-securityhubpolicy-enabledstandardidentifiers
            '''
            result = self._values.get("enabled_standard_identifiers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def security_controls_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationPolicyPropsMixin.SecurityControlsConfigurationProperty"]]:
            '''An object that defines which security controls are enabled in the configuration policy.

            The enablement status of a control is aligned across all of the enabled standards in an account.

            This property is required only if ``ServiceEnabled`` is set to true in your configuration policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-securityhubpolicy.html#cfn-securityhub-configurationpolicy-securityhubpolicy-securitycontrolsconfiguration
            '''
            result = self._values.get("security_controls_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationPolicyPropsMixin.SecurityControlsConfigurationProperty"]], result)

        @builtins.property
        def service_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether Security Hub is enabled in the policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-configurationpolicy-securityhubpolicy.html#cfn-securityhub-configurationpolicy-securityhubpolicy-serviceenabled
            '''
            result = self._values.get("service_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecurityHubPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnConnectorV2MixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "kms_key_arn": "kmsKeyArn",
        "name": "name",
        "provider": "provider",
        "tags": "tags",
    },
)
class CfnConnectorV2MixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorV2PropsMixin.ProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnConnectorV2PropsMixin.

        :param description: A description of the connector.
        :param kms_key_arn: The ARN of KMS key used for the connector.
        :param name: The name of the connector.
        :param provider: The provider configuration of the connector.
        :param tags: A key-value pair to associate with a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-connectorv2.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
            
            cfn_connector_v2_mixin_props = securityhub_mixins.CfnConnectorV2MixinProps(
                description="description",
                kms_key_arn="kmsKeyArn",
                name="name",
                provider=securityhub_mixins.CfnConnectorV2PropsMixin.ProviderProperty(
                    jira_cloud=securityhub_mixins.CfnConnectorV2PropsMixin.JiraCloudProperty(
                        auth_status="authStatus",
                        auth_url="authUrl",
                        cloud_id="cloudId",
                        domain="domain",
                        project_key="projectKey"
                    ),
                    service_now=securityhub_mixins.CfnConnectorV2PropsMixin.ServiceNowProperty(
                        auth_status="authStatus",
                        instance_name="instanceName",
                        secret_arn="secretArn"
                    )
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b22347b8af8ff6166538acb768c1292612f49946453d2e3ac3d5001855bc4d5)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if name is not None:
            self._values["name"] = name
        if provider is not None:
            self._values["provider"] = provider
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-connectorv2.html#cfn-securityhub-connectorv2-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of KMS key used for the connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-connectorv2.html#cfn-securityhub-connectorv2-kmskeyarn
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-connectorv2.html#cfn-securityhub-connectorv2-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorV2PropsMixin.ProviderProperty"]]:
        '''The provider configuration of the connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-connectorv2.html#cfn-securityhub-connectorv2-provider
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorV2PropsMixin.ProviderProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A key-value pair to associate with a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-connectorv2.html#cfn-securityhub-connectorv2-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectorV2MixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConnectorV2PropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnConnectorV2PropsMixin",
):
    '''Resource schema for AWS::SecurityHub::ConnectorV2.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-connectorv2.html
    :cloudformationResource: AWS::SecurityHub::ConnectorV2
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
        
        cfn_connector_v2_props_mixin = securityhub_mixins.CfnConnectorV2PropsMixin(securityhub_mixins.CfnConnectorV2MixinProps(
            description="description",
            kms_key_arn="kmsKeyArn",
            name="name",
            provider=securityhub_mixins.CfnConnectorV2PropsMixin.ProviderProperty(
                jira_cloud=securityhub_mixins.CfnConnectorV2PropsMixin.JiraCloudProperty(
                    auth_status="authStatus",
                    auth_url="authUrl",
                    cloud_id="cloudId",
                    domain="domain",
                    project_key="projectKey"
                ),
                service_now=securityhub_mixins.CfnConnectorV2PropsMixin.ServiceNowProperty(
                    auth_status="authStatus",
                    instance_name="instanceName",
                    secret_arn="secretArn"
                )
            ),
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnConnectorV2MixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecurityHub::ConnectorV2``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c2571ff827250644f09e77d1c7aeca64d2fad1da1353f066e7dab2abca4cc5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e86d742876fbfd018a3dfde3f24ddfed44e6523a0ae48088a72f02a1835e67c3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e3b25e8891a2ecafacb9224aeb43519cfeea9aab0fdfe23cf7c15a2b2ec51a3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConnectorV2MixinProps:
        return typing.cast(CfnConnectorV2MixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnConnectorV2PropsMixin.JiraCloudProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auth_status": "authStatus",
            "auth_url": "authUrl",
            "cloud_id": "cloudId",
            "domain": "domain",
            "project_key": "projectKey",
        },
    )
    class JiraCloudProperty:
        def __init__(
            self,
            *,
            auth_status: typing.Optional[builtins.str] = None,
            auth_url: typing.Optional[builtins.str] = None,
            cloud_id: typing.Optional[builtins.str] = None,
            domain: typing.Optional[builtins.str] = None,
            project_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param auth_status: The auth status of the connector.
            :param auth_url: The authUrl of the JiraCloud connector.
            :param cloud_id: 
            :param domain: 
            :param project_key: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-connectorv2-jiracloud.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                jira_cloud_property = securityhub_mixins.CfnConnectorV2PropsMixin.JiraCloudProperty(
                    auth_status="authStatus",
                    auth_url="authUrl",
                    cloud_id="cloudId",
                    domain="domain",
                    project_key="projectKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bd173e2ec00f03ba6bcbf862bdafacb962eee58cc2d81bb7e7e3d12f50301733)
                check_type(argname="argument auth_status", value=auth_status, expected_type=type_hints["auth_status"])
                check_type(argname="argument auth_url", value=auth_url, expected_type=type_hints["auth_url"])
                check_type(argname="argument cloud_id", value=cloud_id, expected_type=type_hints["cloud_id"])
                check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
                check_type(argname="argument project_key", value=project_key, expected_type=type_hints["project_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth_status is not None:
                self._values["auth_status"] = auth_status
            if auth_url is not None:
                self._values["auth_url"] = auth_url
            if cloud_id is not None:
                self._values["cloud_id"] = cloud_id
            if domain is not None:
                self._values["domain"] = domain
            if project_key is not None:
                self._values["project_key"] = project_key

        @builtins.property
        def auth_status(self) -> typing.Optional[builtins.str]:
            '''The auth status of the connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-connectorv2-jiracloud.html#cfn-securityhub-connectorv2-jiracloud-authstatus
            '''
            result = self._values.get("auth_status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def auth_url(self) -> typing.Optional[builtins.str]:
            '''The authUrl of the JiraCloud connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-connectorv2-jiracloud.html#cfn-securityhub-connectorv2-jiracloud-authurl
            '''
            result = self._values.get("auth_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cloud_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-connectorv2-jiracloud.html#cfn-securityhub-connectorv2-jiracloud-cloudid
            '''
            result = self._values.get("cloud_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def domain(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-connectorv2-jiracloud.html#cfn-securityhub-connectorv2-jiracloud-domain
            '''
            result = self._values.get("domain")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def project_key(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-connectorv2-jiracloud.html#cfn-securityhub-connectorv2-jiracloud-projectkey
            '''
            result = self._values.get("project_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JiraCloudProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnConnectorV2PropsMixin.ProviderProperty",
        jsii_struct_bases=[],
        name_mapping={"jira_cloud": "jiraCloud", "service_now": "serviceNow"},
    )
    class ProviderProperty:
        def __init__(
            self,
            *,
            jira_cloud: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorV2PropsMixin.JiraCloudProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_now: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorV2PropsMixin.ServiceNowProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param jira_cloud: 
            :param service_now: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-connectorv2-provider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                provider_property = securityhub_mixins.CfnConnectorV2PropsMixin.ProviderProperty(
                    jira_cloud=securityhub_mixins.CfnConnectorV2PropsMixin.JiraCloudProperty(
                        auth_status="authStatus",
                        auth_url="authUrl",
                        cloud_id="cloudId",
                        domain="domain",
                        project_key="projectKey"
                    ),
                    service_now=securityhub_mixins.CfnConnectorV2PropsMixin.ServiceNowProperty(
                        auth_status="authStatus",
                        instance_name="instanceName",
                        secret_arn="secretArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d3f7081c25d2848f6ae2b23694987a30d7a650e6d67210b5c7343b0b04102a05)
                check_type(argname="argument jira_cloud", value=jira_cloud, expected_type=type_hints["jira_cloud"])
                check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if jira_cloud is not None:
                self._values["jira_cloud"] = jira_cloud
            if service_now is not None:
                self._values["service_now"] = service_now

        @builtins.property
        def jira_cloud(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorV2PropsMixin.JiraCloudProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-connectorv2-provider.html#cfn-securityhub-connectorv2-provider-jiracloud
            '''
            result = self._values.get("jira_cloud")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorV2PropsMixin.JiraCloudProperty"]], result)

        @builtins.property
        def service_now(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorV2PropsMixin.ServiceNowProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-connectorv2-provider.html#cfn-securityhub-connectorv2-provider-servicenow
            '''
            result = self._values.get("service_now")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorV2PropsMixin.ServiceNowProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnConnectorV2PropsMixin.ServiceNowProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auth_status": "authStatus",
            "instance_name": "instanceName",
            "secret_arn": "secretArn",
        },
    )
    class ServiceNowProperty:
        def __init__(
            self,
            *,
            auth_status: typing.Optional[builtins.str] = None,
            instance_name: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param auth_status: The auth status of the connector.
            :param instance_name: 
            :param secret_arn: The ARN of secrets manager containing ClientId and ClientSecret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-connectorv2-servicenow.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                service_now_property = securityhub_mixins.CfnConnectorV2PropsMixin.ServiceNowProperty(
                    auth_status="authStatus",
                    instance_name="instanceName",
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__14e6ca319f5c8e3a5e3f2eacfaa71751100d76204608b43d90716d0cdf7d1736)
                check_type(argname="argument auth_status", value=auth_status, expected_type=type_hints["auth_status"])
                check_type(argname="argument instance_name", value=instance_name, expected_type=type_hints["instance_name"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth_status is not None:
                self._values["auth_status"] = auth_status
            if instance_name is not None:
                self._values["instance_name"] = instance_name
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def auth_status(self) -> typing.Optional[builtins.str]:
            '''The auth status of the connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-connectorv2-servicenow.html#cfn-securityhub-connectorv2-servicenow-authstatus
            '''
            result = self._values.get("auth_status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-connectorv2-servicenow.html#cfn-securityhub-connectorv2-servicenow-instancename
            '''
            result = self._values.get("instance_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of secrets manager containing ClientId and ClientSecret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-connectorv2-servicenow.html#cfn-securityhub-connectorv2-servicenow-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceNowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnDelegatedAdminMixinProps",
    jsii_struct_bases=[],
    name_mapping={"admin_account_id": "adminAccountId"},
)
class CfnDelegatedAdminMixinProps:
    def __init__(
        self,
        *,
        admin_account_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDelegatedAdminPropsMixin.

        :param admin_account_id: The AWS account identifier of the account to designate as the Security Hub administrator account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-delegatedadmin.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
            
            cfn_delegated_admin_mixin_props = securityhub_mixins.CfnDelegatedAdminMixinProps(
                admin_account_id="adminAccountId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8015c40264beb7267e661110c1c223c2d2d1152f3057d71d5be5c3d24371a905)
            check_type(argname="argument admin_account_id", value=admin_account_id, expected_type=type_hints["admin_account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if admin_account_id is not None:
            self._values["admin_account_id"] = admin_account_id

    @builtins.property
    def admin_account_id(self) -> typing.Optional[builtins.str]:
        '''The AWS account identifier of the account to designate as the Security Hub administrator account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-delegatedadmin.html#cfn-securityhub-delegatedadmin-adminaccountid
        '''
        result = self._values.get("admin_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDelegatedAdminMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDelegatedAdminPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnDelegatedAdminPropsMixin",
):
    '''The ``AWS::SecurityHub::DelegatedAdmin`` resource designates the delegated Security Hub administrator account for an organization.

    You must enable the integration between Security Hub and AWS Organizations before you can designate a delegated Security Hub administrator. Only the management account for an organization can designate the delegated Security Hub administrator account. For more information, see `Designating the delegated Security Hub administrator <https://docs.aws.amazon.com/securityhub/latest/userguide/designate-orgs-admin-account.html#designate-admin-instructions>`_ in the *Security Hub User Guide* .

    To change the delegated administrator account, remove the current delegated administrator account, and then designate the new account.

    To designate multiple delegated administrators in different organizations and AWS Regions , we recommend using `AWS CloudFormation mappings <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/mappings-section-structure.html>`_ .

    Tags aren't supported for this resource.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-delegatedadmin.html
    :cloudformationResource: AWS::SecurityHub::DelegatedAdmin
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
        
        cfn_delegated_admin_props_mixin = securityhub_mixins.CfnDelegatedAdminPropsMixin(securityhub_mixins.CfnDelegatedAdminMixinProps(
            admin_account_id="adminAccountId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDelegatedAdminMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecurityHub::DelegatedAdmin``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b99c1513192a76b80d79193b8862c81b1a3308580e69bc764209fb1d40390c27)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0677209278f2d317b3afd32dd57ef2f2a6c199d6d7ab65af9ef6dc32264a1724)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7374a76c97a42d33c0dee974acaa90beeaf655428cfab93aedc2ecce25b5e5cb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDelegatedAdminMixinProps:
        return typing.cast(CfnDelegatedAdminMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnFindingAggregatorMixinProps",
    jsii_struct_bases=[],
    name_mapping={"region_linking_mode": "regionLinkingMode", "regions": "regions"},
)
class CfnFindingAggregatorMixinProps:
    def __init__(
        self,
        *,
        region_linking_mode: typing.Optional[builtins.str] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnFindingAggregatorPropsMixin.

        :param region_linking_mode: Indicates whether to aggregate findings from all of the available Regions in the current partition. Also determines whether to automatically aggregate findings from new Regions as Security Hub supports them and you opt into them. The selected option also determines how to use the Regions provided in the Regions list. In CloudFormation , the options for this property are as follows: - ``ALL_REGIONS`` - Indicates to aggregate findings from all of the Regions where Security Hub is enabled. When you choose this option, Security Hub also automatically aggregates findings from new Regions as Security Hub supports them and you opt into them. - ``ALL_REGIONS_EXCEPT_SPECIFIED`` - Indicates to aggregate findings from all of the Regions where Security Hub is enabled, except for the Regions listed in the ``Regions`` parameter. When you choose this option, Security Hub also automatically aggregates findings from new Regions as Security Hub supports them and you opt into them. - ``SPECIFIED_REGIONS`` - Indicates to aggregate findings only from the Regions listed in the ``Regions`` parameter. Security Hub does not automatically aggregate findings from new Regions.
        :param regions: If ``RegionLinkingMode`` is ``ALL_REGIONS_EXCEPT_SPECIFIED`` , then this is a space-separated list of Regions that do not aggregate findings to the aggregation Region. If ``RegionLinkingMode`` is ``SPECIFIED_REGIONS`` , then this is a space-separated list of Regions that do aggregate findings to the aggregation Region.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-findingaggregator.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
            
            cfn_finding_aggregator_mixin_props = securityhub_mixins.CfnFindingAggregatorMixinProps(
                region_linking_mode="regionLinkingMode",
                regions=["regions"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f600bc6a7f51ab524f76ab1acec837910c25f7e719e77d0623cb9647ade2310)
            check_type(argname="argument region_linking_mode", value=region_linking_mode, expected_type=type_hints["region_linking_mode"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if region_linking_mode is not None:
            self._values["region_linking_mode"] = region_linking_mode
        if regions is not None:
            self._values["regions"] = regions

    @builtins.property
    def region_linking_mode(self) -> typing.Optional[builtins.str]:
        '''Indicates whether to aggregate findings from all of the available Regions in the current partition.

        Also determines whether to automatically aggregate findings from new Regions as Security Hub supports them and you opt into them.

        The selected option also determines how to use the Regions provided in the Regions list.

        In CloudFormation , the options for this property are as follows:

        - ``ALL_REGIONS`` - Indicates to aggregate findings from all of the Regions where Security Hub is enabled. When you choose this option, Security Hub also automatically aggregates findings from new Regions as Security Hub supports them and you opt into them.
        - ``ALL_REGIONS_EXCEPT_SPECIFIED`` - Indicates to aggregate findings from all of the Regions where Security Hub is enabled, except for the Regions listed in the ``Regions`` parameter. When you choose this option, Security Hub also automatically aggregates findings from new Regions as Security Hub supports them and you opt into them.
        - ``SPECIFIED_REGIONS`` - Indicates to aggregate findings only from the Regions listed in the ``Regions`` parameter. Security Hub does not automatically aggregate findings from new Regions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-findingaggregator.html#cfn-securityhub-findingaggregator-regionlinkingmode
        '''
        result = self._values.get("region_linking_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If ``RegionLinkingMode`` is ``ALL_REGIONS_EXCEPT_SPECIFIED`` , then this is a space-separated list of Regions that do not aggregate findings to the aggregation Region.

        If ``RegionLinkingMode`` is ``SPECIFIED_REGIONS`` , then this is a space-separated list of Regions that do aggregate findings to the aggregation Region.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-findingaggregator.html#cfn-securityhub-findingaggregator-regions
        '''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFindingAggregatorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFindingAggregatorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnFindingAggregatorPropsMixin",
):
    '''The ``AWS::SecurityHub::FindingAggregator`` resource enables cross-Region aggregation.

    When cross-Region aggregation is enabled, you can aggregate findings, finding updates, insights, control compliance statuses, and security scores from one or more linked Regions to a single aggregation Region. You can then view and manage all of this data from the aggregation Region. For more details about cross-Region aggregation, see `Cross-Region aggregation <https://docs.aws.amazon.com/securityhub/latest/userguide/finding-aggregation.html>`_ in the *Security Hub User Guide*

    This resource must be created in the Region that you want to designate as your aggregation Region.

    Cross-Region aggregation is also a prerequisite for using `central configuration <https://docs.aws.amazon.com/securityhub/latest/userguide/central-configuration-intro.html>`_ in Security Hub .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-findingaggregator.html
    :cloudformationResource: AWS::SecurityHub::FindingAggregator
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
        
        cfn_finding_aggregator_props_mixin = securityhub_mixins.CfnFindingAggregatorPropsMixin(securityhub_mixins.CfnFindingAggregatorMixinProps(
            region_linking_mode="regionLinkingMode",
            regions=["regions"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFindingAggregatorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecurityHub::FindingAggregator``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b15a52bd15cde4c4e9c19741a7be267f516ccb80c39709254ee52128508c2484)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1bd477a4af5c7507cbca9919aa2ff70bfe6ef5e8a573d51cd362e500e6b7858)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42085121f61127d737c25cc384e925737944b0bf2e6dd1a1b6c29fdde1a5c68e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFindingAggregatorMixinProps:
        return typing.cast(CfnFindingAggregatorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnHubMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_enable_controls": "autoEnableControls",
        "control_finding_generator": "controlFindingGenerator",
        "enable_default_standards": "enableDefaultStandards",
        "tags": "tags",
    },
)
class CfnHubMixinProps:
    def __init__(
        self,
        *,
        auto_enable_controls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        control_finding_generator: typing.Optional[builtins.str] = None,
        enable_default_standards: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for CfnHubPropsMixin.

        :param auto_enable_controls: Whether to automatically enable new controls when they are added to standards that are enabled. By default, this is set to ``true`` , and new controls are enabled automatically. To not automatically enable new controls, set this to ``false`` . When you automatically enable new controls, you can interact with the controls in the console and programmatically immediately after release. However, automatically enabled controls have a temporary default status of ``DISABLED`` . It can take up to several days for Security Hub to process the control release and designate the control as ``ENABLED`` in your account. During the processing period, you can manually enable or disable a control, and Security Hub will maintain that designation regardless of whether you have ``AutoEnableControls`` set to ``true`` .
        :param control_finding_generator: Specifies whether an account has consolidated control findings turned on or off. If the value for this field is set to ``SECURITY_CONTROL`` , Security Hub generates a single finding for a control check even when the check applies to multiple enabled standards. If the value for this field is set to ``STANDARD_CONTROL`` , Security Hub generates separate findings for a control check when the check applies to multiple enabled standards. The value for this field in a member account matches the value in the administrator account. For accounts that aren't part of an organization, the default value of this field is ``SECURITY_CONTROL`` if you enabled Security Hub on or after February 23, 2023.
        :param enable_default_standards: Whether to enable the security standards that Security Hub has designated as automatically enabled. If you don't provide a value for ``EnableDefaultStandards`` , it is set to ``true`` , and the designated standards are automatically enabled in each AWS Region where you enable Security Hub . If you don't want to enable the designated standards, set ``EnableDefaultStandards`` to ``false`` . Currently, the automatically enabled standards are the Center for Internet Security (CIS) AWS Foundations Benchmark v1.2.0 and AWS Foundational Security Best Practices (FSBP).
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-hub.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
            
            # tags: Any
            
            cfn_hub_mixin_props = securityhub_mixins.CfnHubMixinProps(
                auto_enable_controls=False,
                control_finding_generator="controlFindingGenerator",
                enable_default_standards=False,
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b16e6189f76d51cb37c62c4b36719cb50413f90512560854aada939a2c2eeab)
            check_type(argname="argument auto_enable_controls", value=auto_enable_controls, expected_type=type_hints["auto_enable_controls"])
            check_type(argname="argument control_finding_generator", value=control_finding_generator, expected_type=type_hints["control_finding_generator"])
            check_type(argname="argument enable_default_standards", value=enable_default_standards, expected_type=type_hints["enable_default_standards"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_enable_controls is not None:
            self._values["auto_enable_controls"] = auto_enable_controls
        if control_finding_generator is not None:
            self._values["control_finding_generator"] = control_finding_generator
        if enable_default_standards is not None:
            self._values["enable_default_standards"] = enable_default_standards
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def auto_enable_controls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to automatically enable new controls when they are added to standards that are enabled.

        By default, this is set to ``true`` , and new controls are enabled automatically. To not automatically enable new controls, set this to ``false`` .

        When you automatically enable new controls, you can interact with the controls in the console and programmatically immediately after release. However, automatically enabled controls have a temporary default status of ``DISABLED`` . It can take up to several days for Security Hub to process the control release and designate the control as ``ENABLED`` in your account. During the processing period, you can manually enable or disable a control, and Security Hub will maintain that designation regardless of whether you have ``AutoEnableControls`` set to ``true`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-hub.html#cfn-securityhub-hub-autoenablecontrols
        '''
        result = self._values.get("auto_enable_controls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def control_finding_generator(self) -> typing.Optional[builtins.str]:
        '''Specifies whether an account has consolidated control findings turned on or off.

        If the value for this field is set to ``SECURITY_CONTROL`` , Security Hub generates a single finding for a control check even when the check applies to multiple enabled standards.

        If the value for this field is set to ``STANDARD_CONTROL`` , Security Hub generates separate findings for a control check when the check applies to multiple enabled standards.

        The value for this field in a member account matches the value in the administrator account. For accounts that aren't part of an organization, the default value of this field is ``SECURITY_CONTROL`` if you enabled Security Hub on or after February 23, 2023.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-hub.html#cfn-securityhub-hub-controlfindinggenerator
        '''
        result = self._values.get("control_finding_generator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_default_standards(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to enable the security standards that Security Hub has designated as automatically enabled.

        If you don't provide a value for ``EnableDefaultStandards`` , it is set to ``true`` , and the designated standards are automatically enabled in each AWS Region where you enable Security Hub . If you don't want to enable the designated standards, set ``EnableDefaultStandards`` to ``false`` .

        Currently, the automatically enabled standards are the Center for Internet Security (CIS) AWS Foundations Benchmark v1.2.0 and AWS Foundational Security Best Practices (FSBP).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-hub.html#cfn-securityhub-hub-enabledefaultstandards
        '''
        result = self._values.get("enable_default_standards")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-hub.html#cfn-securityhub-hub-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHubMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnHubPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnHubPropsMixin",
):
    '''The ``AWS::SecurityHub::Hub`` resource specifies the enablement of the Security Hub service in your AWS account .

    The service is enabled in the current AWS Region or the specified Region. You create a separate ``Hub`` resource in each Region in which you want to enable Security Hub .

    When you use this resource to enable Security Hub , default security standards are enabled. To disable default standards, set the ``EnableDefaultStandards`` property to ``false`` . You can use the ```AWS::SecurityHub::Standard`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-standard.html>`_ resource to enable additional standards.

    When you use this resource to enable Security Hub , new controls are automatically enabled for your enabled standards. To disable automatic enablement of new controls, set the ``AutoEnableControls`` property to ``false`` .

    You must create an ``AWS::SecurityHub::Hub`` resource for an account before you can create other types of Security Hub resources for the account through CloudFormation . Use a `DependsOn attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ , such as ``"DependsOn": "Hub"`` , to ensure that you've created an ``AWS::SecurityHub::Hub`` resource before creating other Security Hub resources for an account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-hub.html
    :cloudformationResource: AWS::SecurityHub::Hub
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
        
        # tags: Any
        
        cfn_hub_props_mixin = securityhub_mixins.CfnHubPropsMixin(securityhub_mixins.CfnHubMixinProps(
            auto_enable_controls=False,
            control_finding_generator="controlFindingGenerator",
            enable_default_standards=False,
            tags=tags
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnHubMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecurityHub::Hub``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cffecc941a4a46096a36942db426921bf3a6167d394c0c36f633c608f8d598db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71d4c4cba6618837143bcfc8717e1a3d4cdbdf8fc648783f22a26eb2d1fdd48b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea50b08c74955869488b50ec99412131d74cfaed1e9d3271aafc319a91c1eee)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnHubMixinProps:
        return typing.cast(CfnHubMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnHubV2MixinProps",
    jsii_struct_bases=[],
    name_mapping={"tags": "tags"},
)
class CfnHubV2MixinProps:
    def __init__(
        self,
        *,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnHubV2PropsMixin.

        :param tags: The tags to add to the hub V2 resource when you enable Security Hub.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-hubv2.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
            
            cfn_hub_v2_mixin_props = securityhub_mixins.CfnHubV2MixinProps(
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bce1aeaf7e3934efe86c8a459bd1869f1a69eaaf9f811963b5b5d39ef825c37)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags to add to the hub V2 resource when you enable Security Hub.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-hubv2.html#cfn-securityhub-hubv2-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHubV2MixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnHubV2PropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnHubV2PropsMixin",
):
    '''Returns details about the service resource in your account.

    This API is in public preview and subject to change.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-hubv2.html
    :cloudformationResource: AWS::SecurityHub::HubV2
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
        
        cfn_hub_v2_props_mixin = securityhub_mixins.CfnHubV2PropsMixin(securityhub_mixins.CfnHubV2MixinProps(
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnHubV2MixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecurityHub::HubV2``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bd0d04ae0a27edbd9e9e8d7723c469ddf552fbd70b03f46d4245a8ed91fb4a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5005f813c187dcec86503e6ba1d184eeb2a25c6436d24a98828336dc9cea74d3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8a6e460c102a3458892fc1a3608cfb67c743d358f19ec2a8defb0637f7306e6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnHubV2MixinProps:
        return typing.cast(CfnHubV2MixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnInsightMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "filters": "filters",
        "group_by_attribute": "groupByAttribute",
        "name": "name",
    },
)
class CfnInsightMixinProps:
    def __init__(
        self,
        *,
        filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.AwsSecurityFindingFiltersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        group_by_attribute: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnInsightPropsMixin.

        :param filters: One or more attributes used to filter the findings included in the insight. The insight only includes findings that match the criteria defined in the filters. You can filter by up to ten finding attributes. For each attribute, you can provide up to 20 filter values.
        :param group_by_attribute: The grouping attribute for the insight's findings. Indicates how to group the matching findings, and identifies the type of item that the insight applies to. For example, if an insight is grouped by resource identifier, then the insight produces a list of resource identifiers.
        :param name: The name of a Security Hub insight.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-insight.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
            
            cfn_insight_mixin_props = securityhub_mixins.CfnInsightMixinProps(
                filters=securityhub_mixins.CfnInsightPropsMixin.AwsSecurityFindingFiltersProperty(
                    aws_account_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    aws_account_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    company_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    compliance_associated_standards_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    compliance_security_control_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    compliance_security_control_parameters_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    compliance_security_control_parameters_value=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    compliance_status=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    confidence=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    created_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    criticality=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    description=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    finding_provider_fields_confidence=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    finding_provider_fields_criticality=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    finding_provider_fields_related_findings_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    finding_provider_fields_related_findings_product_arn=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    finding_provider_fields_severity_label=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    finding_provider_fields_severity_original=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    finding_provider_fields_types=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    first_observed_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    generator_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    keyword=[securityhub_mixins.CfnInsightPropsMixin.KeywordFilterProperty(
                        value="value"
                    )],
                    last_observed_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    malware_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    malware_path=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    malware_state=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    malware_type=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    network_destination_domain=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    network_destination_ip_v4=[securityhub_mixins.CfnInsightPropsMixin.IpFilterProperty(
                        cidr="cidr"
                    )],
                    network_destination_ip_v6=[securityhub_mixins.CfnInsightPropsMixin.IpFilterProperty(
                        cidr="cidr"
                    )],
                    network_destination_port=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    network_direction=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    network_protocol=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    network_source_domain=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    network_source_ip_v4=[securityhub_mixins.CfnInsightPropsMixin.IpFilterProperty(
                        cidr="cidr"
                    )],
                    network_source_ip_v6=[securityhub_mixins.CfnInsightPropsMixin.IpFilterProperty(
                        cidr="cidr"
                    )],
                    network_source_mac=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    network_source_port=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    note_text=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    note_updated_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    note_updated_by=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    process_launched_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    process_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    process_parent_pid=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    process_path=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    process_pid=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    process_terminated_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    product_arn=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    product_fields=[securityhub_mixins.CfnInsightPropsMixin.MapFilterProperty(
                        comparison="comparison",
                        key="key",
                        value="value"
                    )],
                    product_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    recommendation_text=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    record_state=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    region=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    related_findings_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    related_findings_product_arn=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_application_arn=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_application_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_ec2_instance_iam_instance_profile_arn=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_ec2_instance_image_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_ec2_instance_ip_v4_addresses=[securityhub_mixins.CfnInsightPropsMixin.IpFilterProperty(
                        cidr="cidr"
                    )],
                    resource_aws_ec2_instance_ip_v6_addresses=[securityhub_mixins.CfnInsightPropsMixin.IpFilterProperty(
                        cidr="cidr"
                    )],
                    resource_aws_ec2_instance_key_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_ec2_instance_launched_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    resource_aws_ec2_instance_subnet_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_ec2_instance_type=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_ec2_instance_vpc_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_iam_access_key_created_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    resource_aws_iam_access_key_principal_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_iam_access_key_status=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_iam_access_key_user_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_iam_user_user_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_s3_bucket_owner_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_s3_bucket_owner_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_container_image_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_container_image_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_container_launched_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    resource_container_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_details_other=[securityhub_mixins.CfnInsightPropsMixin.MapFilterProperty(
                        comparison="comparison",
                        key="key",
                        value="value"
                    )],
                    resource_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_partition=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_region=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_tags=[securityhub_mixins.CfnInsightPropsMixin.MapFilterProperty(
                        comparison="comparison",
                        key="key",
                        value="value"
                    )],
                    resource_type=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    sample=[securityhub_mixins.CfnInsightPropsMixin.BooleanFilterProperty(
                        value=False
                    )],
                    severity_label=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    severity_normalized=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    severity_product=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    source_url=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    threat_intel_indicator_category=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    threat_intel_indicator_last_observed_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    threat_intel_indicator_source=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    threat_intel_indicator_source_url=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    threat_intel_indicator_type=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    threat_intel_indicator_value=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    title=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    type=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    updated_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    user_defined_fields=[securityhub_mixins.CfnInsightPropsMixin.MapFilterProperty(
                        comparison="comparison",
                        key="key",
                        value="value"
                    )],
                    verification_state=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    vulnerabilities_exploit_available=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    vulnerabilities_fix_available=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    workflow_state=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    workflow_status=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )]
                ),
                group_by_attribute="groupByAttribute",
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adc8ac0638e05ab2a5066ec5a09ecf1b0b18f778a3fd0aacaea32dad91d9e56b)
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument group_by_attribute", value=group_by_attribute, expected_type=type_hints["group_by_attribute"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filters is not None:
            self._values["filters"] = filters
        if group_by_attribute is not None:
            self._values["group_by_attribute"] = group_by_attribute
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def filters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.AwsSecurityFindingFiltersProperty"]]:
        '''One or more attributes used to filter the findings included in the insight.

        The insight only includes findings that match the criteria defined in the filters. You can filter by up to ten finding attributes. For each attribute, you can provide up to 20 filter values.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-insight.html#cfn-securityhub-insight-filters
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.AwsSecurityFindingFiltersProperty"]], result)

    @builtins.property
    def group_by_attribute(self) -> typing.Optional[builtins.str]:
        '''The grouping attribute for the insight's findings.

        Indicates how to group the matching findings, and identifies the type of item that the insight applies to. For example, if an insight is grouped by resource identifier, then the insight produces a list of resource identifiers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-insight.html#cfn-securityhub-insight-groupbyattribute
        '''
        result = self._values.get("group_by_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of a Security Hub insight.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-insight.html#cfn-securityhub-insight-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInsightMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInsightPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnInsightPropsMixin",
):
    '''The ``AWS::SecurityHub::Insight`` resource creates a custom insight in Security Hub .

    An insight is a collection of findings that relate to a security issue that requires attention or remediation. For more information, see `Insights in Security Hub <https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-insights.html>`_ in the *Security Hub User Guide* .

    Tags aren't supported for this resource.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-insight.html
    :cloudformationResource: AWS::SecurityHub::Insight
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
        
        cfn_insight_props_mixin = securityhub_mixins.CfnInsightPropsMixin(securityhub_mixins.CfnInsightMixinProps(
            filters=securityhub_mixins.CfnInsightPropsMixin.AwsSecurityFindingFiltersProperty(
                aws_account_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                aws_account_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                company_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                compliance_associated_standards_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                compliance_security_control_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                compliance_security_control_parameters_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                compliance_security_control_parameters_value=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                compliance_status=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                confidence=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                    eq=123,
                    gte=123,
                    lte=123
                )],
                created_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                    date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                        unit="unit",
                        value=123
                    ),
                    end="end",
                    start="start"
                )],
                criticality=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                    eq=123,
                    gte=123,
                    lte=123
                )],
                description=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                finding_provider_fields_confidence=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                    eq=123,
                    gte=123,
                    lte=123
                )],
                finding_provider_fields_criticality=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                    eq=123,
                    gte=123,
                    lte=123
                )],
                finding_provider_fields_related_findings_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                finding_provider_fields_related_findings_product_arn=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                finding_provider_fields_severity_label=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                finding_provider_fields_severity_original=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                finding_provider_fields_types=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                first_observed_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                    date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                        unit="unit",
                        value=123
                    ),
                    end="end",
                    start="start"
                )],
                generator_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                keyword=[securityhub_mixins.CfnInsightPropsMixin.KeywordFilterProperty(
                    value="value"
                )],
                last_observed_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                    date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                        unit="unit",
                        value=123
                    ),
                    end="end",
                    start="start"
                )],
                malware_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                malware_path=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                malware_state=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                malware_type=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                network_destination_domain=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                network_destination_ip_v4=[securityhub_mixins.CfnInsightPropsMixin.IpFilterProperty(
                    cidr="cidr"
                )],
                network_destination_ip_v6=[securityhub_mixins.CfnInsightPropsMixin.IpFilterProperty(
                    cidr="cidr"
                )],
                network_destination_port=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                    eq=123,
                    gte=123,
                    lte=123
                )],
                network_direction=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                network_protocol=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                network_source_domain=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                network_source_ip_v4=[securityhub_mixins.CfnInsightPropsMixin.IpFilterProperty(
                    cidr="cidr"
                )],
                network_source_ip_v6=[securityhub_mixins.CfnInsightPropsMixin.IpFilterProperty(
                    cidr="cidr"
                )],
                network_source_mac=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                network_source_port=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                    eq=123,
                    gte=123,
                    lte=123
                )],
                note_text=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                note_updated_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                    date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                        unit="unit",
                        value=123
                    ),
                    end="end",
                    start="start"
                )],
                note_updated_by=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                process_launched_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                    date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                        unit="unit",
                        value=123
                    ),
                    end="end",
                    start="start"
                )],
                process_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                process_parent_pid=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                    eq=123,
                    gte=123,
                    lte=123
                )],
                process_path=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                process_pid=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                    eq=123,
                    gte=123,
                    lte=123
                )],
                process_terminated_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                    date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                        unit="unit",
                        value=123
                    ),
                    end="end",
                    start="start"
                )],
                product_arn=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                product_fields=[securityhub_mixins.CfnInsightPropsMixin.MapFilterProperty(
                    comparison="comparison",
                    key="key",
                    value="value"
                )],
                product_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                recommendation_text=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                record_state=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                region=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                related_findings_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                related_findings_product_arn=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_application_arn=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_application_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_aws_ec2_instance_iam_instance_profile_arn=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_aws_ec2_instance_image_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_aws_ec2_instance_ip_v4_addresses=[securityhub_mixins.CfnInsightPropsMixin.IpFilterProperty(
                    cidr="cidr"
                )],
                resource_aws_ec2_instance_ip_v6_addresses=[securityhub_mixins.CfnInsightPropsMixin.IpFilterProperty(
                    cidr="cidr"
                )],
                resource_aws_ec2_instance_key_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_aws_ec2_instance_launched_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                    date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                        unit="unit",
                        value=123
                    ),
                    end="end",
                    start="start"
                )],
                resource_aws_ec2_instance_subnet_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_aws_ec2_instance_type=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_aws_ec2_instance_vpc_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_aws_iam_access_key_created_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                    date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                        unit="unit",
                        value=123
                    ),
                    end="end",
                    start="start"
                )],
                resource_aws_iam_access_key_principal_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_aws_iam_access_key_status=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_aws_iam_access_key_user_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_aws_iam_user_user_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_aws_s3_bucket_owner_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_aws_s3_bucket_owner_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_container_image_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_container_image_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_container_launched_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                    date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                        unit="unit",
                        value=123
                    ),
                    end="end",
                    start="start"
                )],
                resource_container_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_details_other=[securityhub_mixins.CfnInsightPropsMixin.MapFilterProperty(
                    comparison="comparison",
                    key="key",
                    value="value"
                )],
                resource_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_partition=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_region=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_tags=[securityhub_mixins.CfnInsightPropsMixin.MapFilterProperty(
                    comparison="comparison",
                    key="key",
                    value="value"
                )],
                resource_type=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                sample=[securityhub_mixins.CfnInsightPropsMixin.BooleanFilterProperty(
                    value=False
                )],
                severity_label=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                severity_normalized=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                    eq=123,
                    gte=123,
                    lte=123
                )],
                severity_product=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                    eq=123,
                    gte=123,
                    lte=123
                )],
                source_url=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                threat_intel_indicator_category=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                threat_intel_indicator_last_observed_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                    date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                        unit="unit",
                        value=123
                    ),
                    end="end",
                    start="start"
                )],
                threat_intel_indicator_source=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                threat_intel_indicator_source_url=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                threat_intel_indicator_type=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                threat_intel_indicator_value=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                title=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                type=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                updated_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                    date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                        unit="unit",
                        value=123
                    ),
                    end="end",
                    start="start"
                )],
                user_defined_fields=[securityhub_mixins.CfnInsightPropsMixin.MapFilterProperty(
                    comparison="comparison",
                    key="key",
                    value="value"
                )],
                verification_state=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                vulnerabilities_exploit_available=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                vulnerabilities_fix_available=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                workflow_state=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                workflow_status=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )]
            ),
            group_by_attribute="groupByAttribute",
            name="name"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnInsightMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecurityHub::Insight``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b99110acc2e8bbb88d64bb9620e6c1a41e4e9647d346603e3fa4498e29d6a8cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0164fd453745c82f3d08cf167797c4ced78a485127756da95765b0451b6c54a0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__490ecc20807184aba85a45af27d5580cc61fe2ca5d60d9331d2b69a926167bfa)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInsightMixinProps:
        return typing.cast(CfnInsightMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnInsightPropsMixin.AwsSecurityFindingFiltersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_account_id": "awsAccountId",
            "aws_account_name": "awsAccountName",
            "company_name": "companyName",
            "compliance_associated_standards_id": "complianceAssociatedStandardsId",
            "compliance_security_control_id": "complianceSecurityControlId",
            "compliance_security_control_parameters_name": "complianceSecurityControlParametersName",
            "compliance_security_control_parameters_value": "complianceSecurityControlParametersValue",
            "compliance_status": "complianceStatus",
            "confidence": "confidence",
            "created_at": "createdAt",
            "criticality": "criticality",
            "description": "description",
            "finding_provider_fields_confidence": "findingProviderFieldsConfidence",
            "finding_provider_fields_criticality": "findingProviderFieldsCriticality",
            "finding_provider_fields_related_findings_id": "findingProviderFieldsRelatedFindingsId",
            "finding_provider_fields_related_findings_product_arn": "findingProviderFieldsRelatedFindingsProductArn",
            "finding_provider_fields_severity_label": "findingProviderFieldsSeverityLabel",
            "finding_provider_fields_severity_original": "findingProviderFieldsSeverityOriginal",
            "finding_provider_fields_types": "findingProviderFieldsTypes",
            "first_observed_at": "firstObservedAt",
            "generator_id": "generatorId",
            "id": "id",
            "keyword": "keyword",
            "last_observed_at": "lastObservedAt",
            "malware_name": "malwareName",
            "malware_path": "malwarePath",
            "malware_state": "malwareState",
            "malware_type": "malwareType",
            "network_destination_domain": "networkDestinationDomain",
            "network_destination_ip_v4": "networkDestinationIpV4",
            "network_destination_ip_v6": "networkDestinationIpV6",
            "network_destination_port": "networkDestinationPort",
            "network_direction": "networkDirection",
            "network_protocol": "networkProtocol",
            "network_source_domain": "networkSourceDomain",
            "network_source_ip_v4": "networkSourceIpV4",
            "network_source_ip_v6": "networkSourceIpV6",
            "network_source_mac": "networkSourceMac",
            "network_source_port": "networkSourcePort",
            "note_text": "noteText",
            "note_updated_at": "noteUpdatedAt",
            "note_updated_by": "noteUpdatedBy",
            "process_launched_at": "processLaunchedAt",
            "process_name": "processName",
            "process_parent_pid": "processParentPid",
            "process_path": "processPath",
            "process_pid": "processPid",
            "process_terminated_at": "processTerminatedAt",
            "product_arn": "productArn",
            "product_fields": "productFields",
            "product_name": "productName",
            "recommendation_text": "recommendationText",
            "record_state": "recordState",
            "region": "region",
            "related_findings_id": "relatedFindingsId",
            "related_findings_product_arn": "relatedFindingsProductArn",
            "resource_application_arn": "resourceApplicationArn",
            "resource_application_name": "resourceApplicationName",
            "resource_aws_ec2_instance_iam_instance_profile_arn": "resourceAwsEc2InstanceIamInstanceProfileArn",
            "resource_aws_ec2_instance_image_id": "resourceAwsEc2InstanceImageId",
            "resource_aws_ec2_instance_ip_v4_addresses": "resourceAwsEc2InstanceIpV4Addresses",
            "resource_aws_ec2_instance_ip_v6_addresses": "resourceAwsEc2InstanceIpV6Addresses",
            "resource_aws_ec2_instance_key_name": "resourceAwsEc2InstanceKeyName",
            "resource_aws_ec2_instance_launched_at": "resourceAwsEc2InstanceLaunchedAt",
            "resource_aws_ec2_instance_subnet_id": "resourceAwsEc2InstanceSubnetId",
            "resource_aws_ec2_instance_type": "resourceAwsEc2InstanceType",
            "resource_aws_ec2_instance_vpc_id": "resourceAwsEc2InstanceVpcId",
            "resource_aws_iam_access_key_created_at": "resourceAwsIamAccessKeyCreatedAt",
            "resource_aws_iam_access_key_principal_name": "resourceAwsIamAccessKeyPrincipalName",
            "resource_aws_iam_access_key_status": "resourceAwsIamAccessKeyStatus",
            "resource_aws_iam_access_key_user_name": "resourceAwsIamAccessKeyUserName",
            "resource_aws_iam_user_user_name": "resourceAwsIamUserUserName",
            "resource_aws_s3_bucket_owner_id": "resourceAwsS3BucketOwnerId",
            "resource_aws_s3_bucket_owner_name": "resourceAwsS3BucketOwnerName",
            "resource_container_image_id": "resourceContainerImageId",
            "resource_container_image_name": "resourceContainerImageName",
            "resource_container_launched_at": "resourceContainerLaunchedAt",
            "resource_container_name": "resourceContainerName",
            "resource_details_other": "resourceDetailsOther",
            "resource_id": "resourceId",
            "resource_partition": "resourcePartition",
            "resource_region": "resourceRegion",
            "resource_tags": "resourceTags",
            "resource_type": "resourceType",
            "sample": "sample",
            "severity_label": "severityLabel",
            "severity_normalized": "severityNormalized",
            "severity_product": "severityProduct",
            "source_url": "sourceUrl",
            "threat_intel_indicator_category": "threatIntelIndicatorCategory",
            "threat_intel_indicator_last_observed_at": "threatIntelIndicatorLastObservedAt",
            "threat_intel_indicator_source": "threatIntelIndicatorSource",
            "threat_intel_indicator_source_url": "threatIntelIndicatorSourceUrl",
            "threat_intel_indicator_type": "threatIntelIndicatorType",
            "threat_intel_indicator_value": "threatIntelIndicatorValue",
            "title": "title",
            "type": "type",
            "updated_at": "updatedAt",
            "user_defined_fields": "userDefinedFields",
            "verification_state": "verificationState",
            "vulnerabilities_exploit_available": "vulnerabilitiesExploitAvailable",
            "vulnerabilities_fix_available": "vulnerabilitiesFixAvailable",
            "workflow_state": "workflowState",
            "workflow_status": "workflowStatus",
        },
    )
    class AwsSecurityFindingFiltersProperty:
        def __init__(
            self,
            *,
            aws_account_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            aws_account_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            company_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            compliance_associated_standards_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            compliance_security_control_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            compliance_security_control_parameters_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            compliance_security_control_parameters_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            compliance_status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            confidence: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.NumberFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            created_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            criticality: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.NumberFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            description: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            finding_provider_fields_confidence: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.NumberFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            finding_provider_fields_criticality: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.NumberFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            finding_provider_fields_related_findings_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            finding_provider_fields_related_findings_product_arn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            finding_provider_fields_severity_label: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            finding_provider_fields_severity_original: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            finding_provider_fields_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            first_observed_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            generator_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            keyword: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.KeywordFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            last_observed_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            malware_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            malware_path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            malware_state: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            malware_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            network_destination_domain: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            network_destination_ip_v4: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.IpFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            network_destination_ip_v6: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.IpFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            network_destination_port: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.NumberFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            network_direction: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            network_protocol: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            network_source_domain: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            network_source_ip_v4: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.IpFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            network_source_ip_v6: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.IpFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            network_source_mac: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            network_source_port: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.NumberFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            note_text: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            note_updated_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            note_updated_by: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            process_launched_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            process_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            process_parent_pid: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.NumberFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            process_path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            process_pid: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.NumberFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            process_terminated_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            product_arn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            product_fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.MapFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            product_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            recommendation_text: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            record_state: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            region: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            related_findings_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            related_findings_product_arn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_application_arn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_application_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_aws_ec2_instance_iam_instance_profile_arn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_aws_ec2_instance_image_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_aws_ec2_instance_ip_v4_addresses: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.IpFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_aws_ec2_instance_ip_v6_addresses: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.IpFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_aws_ec2_instance_key_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_aws_ec2_instance_launched_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_aws_ec2_instance_subnet_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_aws_ec2_instance_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_aws_ec2_instance_vpc_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_aws_iam_access_key_created_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_aws_iam_access_key_principal_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_aws_iam_access_key_status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_aws_iam_access_key_user_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_aws_iam_user_user_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_aws_s3_bucket_owner_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_aws_s3_bucket_owner_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_container_image_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_container_image_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_container_launched_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_container_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_details_other: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.MapFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_partition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_region: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.MapFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            sample: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.BooleanFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            severity_label: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            severity_normalized: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.NumberFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            severity_product: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.NumberFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            source_url: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            threat_intel_indicator_category: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            threat_intel_indicator_last_observed_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            threat_intel_indicator_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            threat_intel_indicator_source_url: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            threat_intel_indicator_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            threat_intel_indicator_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            title: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            updated_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            user_defined_fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.MapFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            verification_state: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            vulnerabilities_exploit_available: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            vulnerabilities_fix_available: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            workflow_state: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            workflow_status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A collection of filters that are applied to all active findings aggregated by Security Hub .

            You can filter by up to ten finding attributes. For each attribute, you can provide up to 20 filter values.

            :param aws_account_id: The AWS account ID in which a finding is generated.
            :param aws_account_name: The name of the AWS account in which a finding is generated.
            :param company_name: The name of the findings provider (company) that owns the solution (product) that generates findings.
            :param compliance_associated_standards_id: The unique identifier of a standard in which a control is enabled. This field consists of the resource portion of the Amazon Resource Name (ARN) returned for a standard in the `DescribeStandards <https://docs.aws.amazon.com/securityhub/1.0/APIReference/API_DescribeStandards.html>`_ API response.
            :param compliance_security_control_id: The unique identifier of a control across standards. Values for this field typically consist of an AWS service and a number, such as APIGateway.5.
            :param compliance_security_control_parameters_name: The name of a security control parameter.
            :param compliance_security_control_parameters_value: The current value of a security control parameter.
            :param compliance_status: Exclusive to findings that are generated as the result of a check run against a specific rule in a supported standard, such as CIS AWS Foundations. Contains security standard-related finding details.
            :param confidence: A finding's confidence. Confidence is defined as the likelihood that a finding accurately identifies the behavior or issue that it was intended to identify. Confidence is scored on a 0-100 basis using a ratio scale, where 0 means zero percent confidence and 100 means 100 percent confidence.
            :param created_at: A timestamp that indicates when the security findings provider created the potential security issue that a finding reflects. For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .
            :param criticality: The level of importance assigned to the resources associated with the finding. A score of 0 means that the underlying resources have no criticality, and a score of 100 is reserved for the most critical resources.
            :param description: A finding's description.
            :param finding_provider_fields_confidence: The finding provider value for the finding confidence. Confidence is defined as the likelihood that a finding accurately identifies the behavior or issue that it was intended to identify. Confidence is scored on a 0-100 basis using a ratio scale, where 0 means zero percent confidence and 100 means 100 percent confidence.
            :param finding_provider_fields_criticality: The finding provider value for the level of importance assigned to the resources associated with the findings. A score of 0 means that the underlying resources have no criticality, and a score of 100 is reserved for the most critical resources.
            :param finding_provider_fields_related_findings_id: The finding identifier of a related finding that is identified by the finding provider.
            :param finding_provider_fields_related_findings_product_arn: The ARN of the solution that generated a related finding that is identified by the finding provider.
            :param finding_provider_fields_severity_label: The finding provider value for the severity label.
            :param finding_provider_fields_severity_original: The finding provider's original value for the severity.
            :param finding_provider_fields_types: One or more finding types that the finding provider assigned to the finding. Uses the format of ``namespace/category/classifier`` that classify a finding. Valid namespace values are: Software and Configuration Checks | TTPs | Effects | Unusual Behaviors | Sensitive Data Identifications
            :param first_observed_at: A timestamp that indicates when the security findings provider first observed the potential security issue that a finding captured. For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .
            :param generator_id: The identifier for the solution-specific component (a discrete unit of logic) that generated a finding. In various security findings providers' solutions, this generator can be called a rule, a check, a detector, a plugin, etc.
            :param id: The security findings provider-specific identifier for a finding.
            :param keyword: This field is deprecated. A keyword for a finding.
            :param last_observed_at: A timestamp that indicates when the security findings provider most recently observed a change in the resource that is involved in the finding. For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .
            :param malware_name: The name of the malware that was observed.
            :param malware_path: The filesystem path of the malware that was observed.
            :param malware_state: The state of the malware that was observed.
            :param malware_type: The type of the malware that was observed.
            :param network_destination_domain: The destination domain of network-related information about a finding.
            :param network_destination_ip_v4: The destination IPv4 address of network-related information about a finding.
            :param network_destination_ip_v6: The destination IPv6 address of network-related information about a finding.
            :param network_destination_port: The destination port of network-related information about a finding.
            :param network_direction: Indicates the direction of network traffic associated with a finding.
            :param network_protocol: The protocol of network-related information about a finding.
            :param network_source_domain: The source domain of network-related information about a finding.
            :param network_source_ip_v4: The source IPv4 address of network-related information about a finding.
            :param network_source_ip_v6: The source IPv6 address of network-related information about a finding.
            :param network_source_mac: The source media access control (MAC) address of network-related information about a finding.
            :param network_source_port: The source port of network-related information about a finding.
            :param note_text: The text of a note.
            :param note_updated_at: The timestamp of when the note was updated.
            :param note_updated_by: The principal that created a note.
            :param process_launched_at: A timestamp that identifies when the process was launched. For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .
            :param process_name: The name of the process.
            :param process_parent_pid: The parent process ID. This field accepts positive integers between ``O`` and ``2147483647`` .
            :param process_path: The path to the process executable.
            :param process_pid: The process ID.
            :param process_terminated_at: A timestamp that identifies when the process was terminated. For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .
            :param product_arn: The ARN generated by Security Hub that uniquely identifies a third-party company (security findings provider) after this provider's product (solution that generates findings) is registered with Security Hub.
            :param product_fields: A data type where security findings providers can include additional solution-specific details that aren't part of the defined ``AwsSecurityFinding`` format.
            :param product_name: The name of the solution (product) that generates findings.
            :param recommendation_text: The recommendation of what to do about the issue described in a finding.
            :param record_state: The updated record state for the finding.
            :param region: The Region from which the finding was generated.
            :param related_findings_id: The solution-generated identifier for a related finding.
            :param related_findings_product_arn: The ARN of the solution that generated a related finding.
            :param resource_application_arn: The ARN of the application that is related to a finding.
            :param resource_application_name: The name of the application that is related to a finding.
            :param resource_aws_ec2_instance_iam_instance_profile_arn: The IAM profile ARN of the instance.
            :param resource_aws_ec2_instance_image_id: The Amazon Machine Image (AMI) ID of the instance.
            :param resource_aws_ec2_instance_ip_v4_addresses: The IPv4 addresses associated with the instance.
            :param resource_aws_ec2_instance_ip_v6_addresses: The IPv6 addresses associated with the instance.
            :param resource_aws_ec2_instance_key_name: The key name associated with the instance.
            :param resource_aws_ec2_instance_launched_at: The date and time the instance was launched.
            :param resource_aws_ec2_instance_subnet_id: The identifier of the subnet that the instance was launched in.
            :param resource_aws_ec2_instance_type: The instance type of the instance.
            :param resource_aws_ec2_instance_vpc_id: The identifier of the VPC that the instance was launched in.
            :param resource_aws_iam_access_key_created_at: The creation date/time of the IAM access key related to a finding.
            :param resource_aws_iam_access_key_principal_name: The name of the principal that is associated with an IAM access key.
            :param resource_aws_iam_access_key_status: The status of the IAM access key related to a finding.
            :param resource_aws_iam_access_key_user_name: This field is deprecated. The username associated with the IAM access key related to a finding.
            :param resource_aws_iam_user_user_name: The name of an IAM user.
            :param resource_aws_s3_bucket_owner_id: The canonical user ID of the owner of the S3 bucket.
            :param resource_aws_s3_bucket_owner_name: The display name of the owner of the S3 bucket.
            :param resource_container_image_id: The identifier of the image related to a finding.
            :param resource_container_image_name: The name of the image related to a finding.
            :param resource_container_launched_at: A timestamp that identifies when the container was started. For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .
            :param resource_container_name: The name of the container related to a finding.
            :param resource_details_other: The details of a resource that doesn't have a specific subfield for the resource type defined.
            :param resource_id: The canonical identifier for the given resource type.
            :param resource_partition: The canonical AWS partition name that the Region is assigned to.
            :param resource_region: The canonical AWS external Region name where this resource is located.
            :param resource_tags: A list of AWS tags associated with a resource at the time the finding was processed.
            :param resource_type: Specifies the type of the resource that details are provided for.
            :param sample: Indicates whether or not sample findings are included in the filter results.
            :param severity_label: The label of a finding's severity.
            :param severity_normalized: Deprecated. The normalized severity of a finding. Instead of providing ``Normalized`` , provide ``Label`` . The value of ``Normalized`` can be an integer between ``0`` and ``100`` . If you provide ``Label`` and don't provide ``Normalized`` , then ``Normalized`` is set automatically as follows. - ``INFORMATIONAL`` - 0 - ``LOW`` - 1 - ``MEDIUM`` - 40 - ``HIGH`` - 70 - ``CRITICAL`` - 90
            :param severity_product: Deprecated. This attribute isn't included in findings. Instead of providing ``Product`` , provide ``Original`` . The native severity as defined by the AWS service or integrated partner product that generated the finding.
            :param source_url: A URL that links to a page about the current finding in the security findings provider's solution.
            :param threat_intel_indicator_category: The category of a threat intelligence indicator.
            :param threat_intel_indicator_last_observed_at: A timestamp that identifies the last observation of a threat intelligence indicator. For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .
            :param threat_intel_indicator_source: The source of the threat intelligence.
            :param threat_intel_indicator_source_url: The URL for more details from the source of the threat intelligence.
            :param threat_intel_indicator_type: The type of a threat intelligence indicator.
            :param threat_intel_indicator_value: The value of a threat intelligence indicator.
            :param title: A finding's title.
            :param type: A finding type in the format of ``namespace/category/classifier`` that classifies a finding.
            :param updated_at: A timestamp that indicates when the security findings provider last updated the finding record. For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .
            :param user_defined_fields: A list of name/value string pairs associated with the finding. These are custom, user-defined fields added to a finding.
            :param verification_state: The veracity of a finding.
            :param vulnerabilities_exploit_available: Indicates whether a software vulnerability in your environment has a known exploit. You can filter findings by this field only if you use Security Hub and Amazon Inspector.
            :param vulnerabilities_fix_available: Indicates whether a vulnerability is fixed in a newer version of the affected software packages. You can filter findings by this field only if you use Security Hub and Amazon Inspector.
            :param workflow_state: The workflow state of a finding. Note that this field is deprecated. To search for a finding based on its workflow status, use ``WorkflowStatus`` .
            :param workflow_status: The status of the investigation into a finding. Allowed values are the following. - ``NEW`` - The initial state of a finding, before it is reviewed. Security Hub also resets the workflow status from ``NOTIFIED`` or ``RESOLVED`` to ``NEW`` in the following cases: - ``RecordState`` changes from ``ARCHIVED`` to ``ACTIVE`` . - ``Compliance.Status`` changes from ``PASSED`` to either ``WARNING`` , ``FAILED`` , or ``NOT_AVAILABLE`` . - ``NOTIFIED`` - Indicates that the resource owner has been notified about the security issue. Used when the initial reviewer is not the resource owner, and needs intervention from the resource owner. If one of the following occurs, the workflow status is changed automatically from ``NOTIFIED`` to ``NEW`` : - ``RecordState`` changes from ``ARCHIVED`` to ``ACTIVE`` . - ``Compliance.Status`` changes from ``PASSED`` to ``FAILED`` , ``WARNING`` , or ``NOT_AVAILABLE`` . - ``SUPPRESSED`` - Indicates that you reviewed the finding and don't believe that any action is needed. The workflow status of a ``SUPPRESSED`` finding does not change if ``RecordState`` changes from ``ARCHIVED`` to ``ACTIVE`` . - ``RESOLVED`` - The finding was reviewed and remediated and is now considered resolved. The finding remains ``RESOLVED`` unless one of the following occurs: - ``RecordState`` changes from ``ARCHIVED`` to ``ACTIVE`` . - ``Compliance.Status`` changes from ``PASSED`` to ``FAILED`` , ``WARNING`` , or ``NOT_AVAILABLE`` . In those cases, the workflow status is automatically reset to ``NEW`` . For findings from controls, if ``Compliance.Status`` is ``PASSED`` , then Security Hub automatically sets the workflow status to ``RESOLVED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                aws_security_finding_filters_property = securityhub_mixins.CfnInsightPropsMixin.AwsSecurityFindingFiltersProperty(
                    aws_account_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    aws_account_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    company_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    compliance_associated_standards_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    compliance_security_control_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    compliance_security_control_parameters_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    compliance_security_control_parameters_value=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    compliance_status=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    confidence=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    created_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    criticality=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    description=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    finding_provider_fields_confidence=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    finding_provider_fields_criticality=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    finding_provider_fields_related_findings_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    finding_provider_fields_related_findings_product_arn=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    finding_provider_fields_severity_label=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    finding_provider_fields_severity_original=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    finding_provider_fields_types=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    first_observed_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    generator_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    keyword=[securityhub_mixins.CfnInsightPropsMixin.KeywordFilterProperty(
                        value="value"
                    )],
                    last_observed_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    malware_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    malware_path=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    malware_state=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    malware_type=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    network_destination_domain=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    network_destination_ip_v4=[securityhub_mixins.CfnInsightPropsMixin.IpFilterProperty(
                        cidr="cidr"
                    )],
                    network_destination_ip_v6=[securityhub_mixins.CfnInsightPropsMixin.IpFilterProperty(
                        cidr="cidr"
                    )],
                    network_destination_port=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    network_direction=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    network_protocol=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    network_source_domain=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    network_source_ip_v4=[securityhub_mixins.CfnInsightPropsMixin.IpFilterProperty(
                        cidr="cidr"
                    )],
                    network_source_ip_v6=[securityhub_mixins.CfnInsightPropsMixin.IpFilterProperty(
                        cidr="cidr"
                    )],
                    network_source_mac=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    network_source_port=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    note_text=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    note_updated_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    note_updated_by=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    process_launched_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    process_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    process_parent_pid=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    process_path=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    process_pid=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    process_terminated_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    product_arn=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    product_fields=[securityhub_mixins.CfnInsightPropsMixin.MapFilterProperty(
                        comparison="comparison",
                        key="key",
                        value="value"
                    )],
                    product_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    recommendation_text=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    record_state=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    region=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    related_findings_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    related_findings_product_arn=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_application_arn=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_application_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_ec2_instance_iam_instance_profile_arn=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_ec2_instance_image_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_ec2_instance_ip_v4_addresses=[securityhub_mixins.CfnInsightPropsMixin.IpFilterProperty(
                        cidr="cidr"
                    )],
                    resource_aws_ec2_instance_ip_v6_addresses=[securityhub_mixins.CfnInsightPropsMixin.IpFilterProperty(
                        cidr="cidr"
                    )],
                    resource_aws_ec2_instance_key_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_ec2_instance_launched_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    resource_aws_ec2_instance_subnet_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_ec2_instance_type=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_ec2_instance_vpc_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_iam_access_key_created_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    resource_aws_iam_access_key_principal_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_iam_access_key_status=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_iam_access_key_user_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_iam_user_user_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_s3_bucket_owner_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_aws_s3_bucket_owner_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_container_image_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_container_image_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_container_launched_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    resource_container_name=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_details_other=[securityhub_mixins.CfnInsightPropsMixin.MapFilterProperty(
                        comparison="comparison",
                        key="key",
                        value="value"
                    )],
                    resource_id=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_partition=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_region=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_tags=[securityhub_mixins.CfnInsightPropsMixin.MapFilterProperty(
                        comparison="comparison",
                        key="key",
                        value="value"
                    )],
                    resource_type=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    sample=[securityhub_mixins.CfnInsightPropsMixin.BooleanFilterProperty(
                        value=False
                    )],
                    severity_label=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    severity_normalized=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    severity_product=[securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                        eq=123,
                        gte=123,
                        lte=123
                    )],
                    source_url=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    threat_intel_indicator_category=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    threat_intel_indicator_last_observed_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    threat_intel_indicator_source=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    threat_intel_indicator_source_url=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    threat_intel_indicator_type=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    threat_intel_indicator_value=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    title=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    type=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    updated_at=[securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                        date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                            unit="unit",
                            value=123
                        ),
                        end="end",
                        start="start"
                    )],
                    user_defined_fields=[securityhub_mixins.CfnInsightPropsMixin.MapFilterProperty(
                        comparison="comparison",
                        key="key",
                        value="value"
                    )],
                    verification_state=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    vulnerabilities_exploit_available=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    vulnerabilities_fix_available=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    workflow_state=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    workflow_status=[securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d25c1bb3cc97dbdfbe4857bdd1468371289e691d9b8bc79d0e0b9335b8123bdf)
                check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
                check_type(argname="argument aws_account_name", value=aws_account_name, expected_type=type_hints["aws_account_name"])
                check_type(argname="argument company_name", value=company_name, expected_type=type_hints["company_name"])
                check_type(argname="argument compliance_associated_standards_id", value=compliance_associated_standards_id, expected_type=type_hints["compliance_associated_standards_id"])
                check_type(argname="argument compliance_security_control_id", value=compliance_security_control_id, expected_type=type_hints["compliance_security_control_id"])
                check_type(argname="argument compliance_security_control_parameters_name", value=compliance_security_control_parameters_name, expected_type=type_hints["compliance_security_control_parameters_name"])
                check_type(argname="argument compliance_security_control_parameters_value", value=compliance_security_control_parameters_value, expected_type=type_hints["compliance_security_control_parameters_value"])
                check_type(argname="argument compliance_status", value=compliance_status, expected_type=type_hints["compliance_status"])
                check_type(argname="argument confidence", value=confidence, expected_type=type_hints["confidence"])
                check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
                check_type(argname="argument criticality", value=criticality, expected_type=type_hints["criticality"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument finding_provider_fields_confidence", value=finding_provider_fields_confidence, expected_type=type_hints["finding_provider_fields_confidence"])
                check_type(argname="argument finding_provider_fields_criticality", value=finding_provider_fields_criticality, expected_type=type_hints["finding_provider_fields_criticality"])
                check_type(argname="argument finding_provider_fields_related_findings_id", value=finding_provider_fields_related_findings_id, expected_type=type_hints["finding_provider_fields_related_findings_id"])
                check_type(argname="argument finding_provider_fields_related_findings_product_arn", value=finding_provider_fields_related_findings_product_arn, expected_type=type_hints["finding_provider_fields_related_findings_product_arn"])
                check_type(argname="argument finding_provider_fields_severity_label", value=finding_provider_fields_severity_label, expected_type=type_hints["finding_provider_fields_severity_label"])
                check_type(argname="argument finding_provider_fields_severity_original", value=finding_provider_fields_severity_original, expected_type=type_hints["finding_provider_fields_severity_original"])
                check_type(argname="argument finding_provider_fields_types", value=finding_provider_fields_types, expected_type=type_hints["finding_provider_fields_types"])
                check_type(argname="argument first_observed_at", value=first_observed_at, expected_type=type_hints["first_observed_at"])
                check_type(argname="argument generator_id", value=generator_id, expected_type=type_hints["generator_id"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument keyword", value=keyword, expected_type=type_hints["keyword"])
                check_type(argname="argument last_observed_at", value=last_observed_at, expected_type=type_hints["last_observed_at"])
                check_type(argname="argument malware_name", value=malware_name, expected_type=type_hints["malware_name"])
                check_type(argname="argument malware_path", value=malware_path, expected_type=type_hints["malware_path"])
                check_type(argname="argument malware_state", value=malware_state, expected_type=type_hints["malware_state"])
                check_type(argname="argument malware_type", value=malware_type, expected_type=type_hints["malware_type"])
                check_type(argname="argument network_destination_domain", value=network_destination_domain, expected_type=type_hints["network_destination_domain"])
                check_type(argname="argument network_destination_ip_v4", value=network_destination_ip_v4, expected_type=type_hints["network_destination_ip_v4"])
                check_type(argname="argument network_destination_ip_v6", value=network_destination_ip_v6, expected_type=type_hints["network_destination_ip_v6"])
                check_type(argname="argument network_destination_port", value=network_destination_port, expected_type=type_hints["network_destination_port"])
                check_type(argname="argument network_direction", value=network_direction, expected_type=type_hints["network_direction"])
                check_type(argname="argument network_protocol", value=network_protocol, expected_type=type_hints["network_protocol"])
                check_type(argname="argument network_source_domain", value=network_source_domain, expected_type=type_hints["network_source_domain"])
                check_type(argname="argument network_source_ip_v4", value=network_source_ip_v4, expected_type=type_hints["network_source_ip_v4"])
                check_type(argname="argument network_source_ip_v6", value=network_source_ip_v6, expected_type=type_hints["network_source_ip_v6"])
                check_type(argname="argument network_source_mac", value=network_source_mac, expected_type=type_hints["network_source_mac"])
                check_type(argname="argument network_source_port", value=network_source_port, expected_type=type_hints["network_source_port"])
                check_type(argname="argument note_text", value=note_text, expected_type=type_hints["note_text"])
                check_type(argname="argument note_updated_at", value=note_updated_at, expected_type=type_hints["note_updated_at"])
                check_type(argname="argument note_updated_by", value=note_updated_by, expected_type=type_hints["note_updated_by"])
                check_type(argname="argument process_launched_at", value=process_launched_at, expected_type=type_hints["process_launched_at"])
                check_type(argname="argument process_name", value=process_name, expected_type=type_hints["process_name"])
                check_type(argname="argument process_parent_pid", value=process_parent_pid, expected_type=type_hints["process_parent_pid"])
                check_type(argname="argument process_path", value=process_path, expected_type=type_hints["process_path"])
                check_type(argname="argument process_pid", value=process_pid, expected_type=type_hints["process_pid"])
                check_type(argname="argument process_terminated_at", value=process_terminated_at, expected_type=type_hints["process_terminated_at"])
                check_type(argname="argument product_arn", value=product_arn, expected_type=type_hints["product_arn"])
                check_type(argname="argument product_fields", value=product_fields, expected_type=type_hints["product_fields"])
                check_type(argname="argument product_name", value=product_name, expected_type=type_hints["product_name"])
                check_type(argname="argument recommendation_text", value=recommendation_text, expected_type=type_hints["recommendation_text"])
                check_type(argname="argument record_state", value=record_state, expected_type=type_hints["record_state"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument related_findings_id", value=related_findings_id, expected_type=type_hints["related_findings_id"])
                check_type(argname="argument related_findings_product_arn", value=related_findings_product_arn, expected_type=type_hints["related_findings_product_arn"])
                check_type(argname="argument resource_application_arn", value=resource_application_arn, expected_type=type_hints["resource_application_arn"])
                check_type(argname="argument resource_application_name", value=resource_application_name, expected_type=type_hints["resource_application_name"])
                check_type(argname="argument resource_aws_ec2_instance_iam_instance_profile_arn", value=resource_aws_ec2_instance_iam_instance_profile_arn, expected_type=type_hints["resource_aws_ec2_instance_iam_instance_profile_arn"])
                check_type(argname="argument resource_aws_ec2_instance_image_id", value=resource_aws_ec2_instance_image_id, expected_type=type_hints["resource_aws_ec2_instance_image_id"])
                check_type(argname="argument resource_aws_ec2_instance_ip_v4_addresses", value=resource_aws_ec2_instance_ip_v4_addresses, expected_type=type_hints["resource_aws_ec2_instance_ip_v4_addresses"])
                check_type(argname="argument resource_aws_ec2_instance_ip_v6_addresses", value=resource_aws_ec2_instance_ip_v6_addresses, expected_type=type_hints["resource_aws_ec2_instance_ip_v6_addresses"])
                check_type(argname="argument resource_aws_ec2_instance_key_name", value=resource_aws_ec2_instance_key_name, expected_type=type_hints["resource_aws_ec2_instance_key_name"])
                check_type(argname="argument resource_aws_ec2_instance_launched_at", value=resource_aws_ec2_instance_launched_at, expected_type=type_hints["resource_aws_ec2_instance_launched_at"])
                check_type(argname="argument resource_aws_ec2_instance_subnet_id", value=resource_aws_ec2_instance_subnet_id, expected_type=type_hints["resource_aws_ec2_instance_subnet_id"])
                check_type(argname="argument resource_aws_ec2_instance_type", value=resource_aws_ec2_instance_type, expected_type=type_hints["resource_aws_ec2_instance_type"])
                check_type(argname="argument resource_aws_ec2_instance_vpc_id", value=resource_aws_ec2_instance_vpc_id, expected_type=type_hints["resource_aws_ec2_instance_vpc_id"])
                check_type(argname="argument resource_aws_iam_access_key_created_at", value=resource_aws_iam_access_key_created_at, expected_type=type_hints["resource_aws_iam_access_key_created_at"])
                check_type(argname="argument resource_aws_iam_access_key_principal_name", value=resource_aws_iam_access_key_principal_name, expected_type=type_hints["resource_aws_iam_access_key_principal_name"])
                check_type(argname="argument resource_aws_iam_access_key_status", value=resource_aws_iam_access_key_status, expected_type=type_hints["resource_aws_iam_access_key_status"])
                check_type(argname="argument resource_aws_iam_access_key_user_name", value=resource_aws_iam_access_key_user_name, expected_type=type_hints["resource_aws_iam_access_key_user_name"])
                check_type(argname="argument resource_aws_iam_user_user_name", value=resource_aws_iam_user_user_name, expected_type=type_hints["resource_aws_iam_user_user_name"])
                check_type(argname="argument resource_aws_s3_bucket_owner_id", value=resource_aws_s3_bucket_owner_id, expected_type=type_hints["resource_aws_s3_bucket_owner_id"])
                check_type(argname="argument resource_aws_s3_bucket_owner_name", value=resource_aws_s3_bucket_owner_name, expected_type=type_hints["resource_aws_s3_bucket_owner_name"])
                check_type(argname="argument resource_container_image_id", value=resource_container_image_id, expected_type=type_hints["resource_container_image_id"])
                check_type(argname="argument resource_container_image_name", value=resource_container_image_name, expected_type=type_hints["resource_container_image_name"])
                check_type(argname="argument resource_container_launched_at", value=resource_container_launched_at, expected_type=type_hints["resource_container_launched_at"])
                check_type(argname="argument resource_container_name", value=resource_container_name, expected_type=type_hints["resource_container_name"])
                check_type(argname="argument resource_details_other", value=resource_details_other, expected_type=type_hints["resource_details_other"])
                check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
                check_type(argname="argument resource_partition", value=resource_partition, expected_type=type_hints["resource_partition"])
                check_type(argname="argument resource_region", value=resource_region, expected_type=type_hints["resource_region"])
                check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
                check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
                check_type(argname="argument sample", value=sample, expected_type=type_hints["sample"])
                check_type(argname="argument severity_label", value=severity_label, expected_type=type_hints["severity_label"])
                check_type(argname="argument severity_normalized", value=severity_normalized, expected_type=type_hints["severity_normalized"])
                check_type(argname="argument severity_product", value=severity_product, expected_type=type_hints["severity_product"])
                check_type(argname="argument source_url", value=source_url, expected_type=type_hints["source_url"])
                check_type(argname="argument threat_intel_indicator_category", value=threat_intel_indicator_category, expected_type=type_hints["threat_intel_indicator_category"])
                check_type(argname="argument threat_intel_indicator_last_observed_at", value=threat_intel_indicator_last_observed_at, expected_type=type_hints["threat_intel_indicator_last_observed_at"])
                check_type(argname="argument threat_intel_indicator_source", value=threat_intel_indicator_source, expected_type=type_hints["threat_intel_indicator_source"])
                check_type(argname="argument threat_intel_indicator_source_url", value=threat_intel_indicator_source_url, expected_type=type_hints["threat_intel_indicator_source_url"])
                check_type(argname="argument threat_intel_indicator_type", value=threat_intel_indicator_type, expected_type=type_hints["threat_intel_indicator_type"])
                check_type(argname="argument threat_intel_indicator_value", value=threat_intel_indicator_value, expected_type=type_hints["threat_intel_indicator_value"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
                check_type(argname="argument user_defined_fields", value=user_defined_fields, expected_type=type_hints["user_defined_fields"])
                check_type(argname="argument verification_state", value=verification_state, expected_type=type_hints["verification_state"])
                check_type(argname="argument vulnerabilities_exploit_available", value=vulnerabilities_exploit_available, expected_type=type_hints["vulnerabilities_exploit_available"])
                check_type(argname="argument vulnerabilities_fix_available", value=vulnerabilities_fix_available, expected_type=type_hints["vulnerabilities_fix_available"])
                check_type(argname="argument workflow_state", value=workflow_state, expected_type=type_hints["workflow_state"])
                check_type(argname="argument workflow_status", value=workflow_status, expected_type=type_hints["workflow_status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_account_id is not None:
                self._values["aws_account_id"] = aws_account_id
            if aws_account_name is not None:
                self._values["aws_account_name"] = aws_account_name
            if company_name is not None:
                self._values["company_name"] = company_name
            if compliance_associated_standards_id is not None:
                self._values["compliance_associated_standards_id"] = compliance_associated_standards_id
            if compliance_security_control_id is not None:
                self._values["compliance_security_control_id"] = compliance_security_control_id
            if compliance_security_control_parameters_name is not None:
                self._values["compliance_security_control_parameters_name"] = compliance_security_control_parameters_name
            if compliance_security_control_parameters_value is not None:
                self._values["compliance_security_control_parameters_value"] = compliance_security_control_parameters_value
            if compliance_status is not None:
                self._values["compliance_status"] = compliance_status
            if confidence is not None:
                self._values["confidence"] = confidence
            if created_at is not None:
                self._values["created_at"] = created_at
            if criticality is not None:
                self._values["criticality"] = criticality
            if description is not None:
                self._values["description"] = description
            if finding_provider_fields_confidence is not None:
                self._values["finding_provider_fields_confidence"] = finding_provider_fields_confidence
            if finding_provider_fields_criticality is not None:
                self._values["finding_provider_fields_criticality"] = finding_provider_fields_criticality
            if finding_provider_fields_related_findings_id is not None:
                self._values["finding_provider_fields_related_findings_id"] = finding_provider_fields_related_findings_id
            if finding_provider_fields_related_findings_product_arn is not None:
                self._values["finding_provider_fields_related_findings_product_arn"] = finding_provider_fields_related_findings_product_arn
            if finding_provider_fields_severity_label is not None:
                self._values["finding_provider_fields_severity_label"] = finding_provider_fields_severity_label
            if finding_provider_fields_severity_original is not None:
                self._values["finding_provider_fields_severity_original"] = finding_provider_fields_severity_original
            if finding_provider_fields_types is not None:
                self._values["finding_provider_fields_types"] = finding_provider_fields_types
            if first_observed_at is not None:
                self._values["first_observed_at"] = first_observed_at
            if generator_id is not None:
                self._values["generator_id"] = generator_id
            if id is not None:
                self._values["id"] = id
            if keyword is not None:
                self._values["keyword"] = keyword
            if last_observed_at is not None:
                self._values["last_observed_at"] = last_observed_at
            if malware_name is not None:
                self._values["malware_name"] = malware_name
            if malware_path is not None:
                self._values["malware_path"] = malware_path
            if malware_state is not None:
                self._values["malware_state"] = malware_state
            if malware_type is not None:
                self._values["malware_type"] = malware_type
            if network_destination_domain is not None:
                self._values["network_destination_domain"] = network_destination_domain
            if network_destination_ip_v4 is not None:
                self._values["network_destination_ip_v4"] = network_destination_ip_v4
            if network_destination_ip_v6 is not None:
                self._values["network_destination_ip_v6"] = network_destination_ip_v6
            if network_destination_port is not None:
                self._values["network_destination_port"] = network_destination_port
            if network_direction is not None:
                self._values["network_direction"] = network_direction
            if network_protocol is not None:
                self._values["network_protocol"] = network_protocol
            if network_source_domain is not None:
                self._values["network_source_domain"] = network_source_domain
            if network_source_ip_v4 is not None:
                self._values["network_source_ip_v4"] = network_source_ip_v4
            if network_source_ip_v6 is not None:
                self._values["network_source_ip_v6"] = network_source_ip_v6
            if network_source_mac is not None:
                self._values["network_source_mac"] = network_source_mac
            if network_source_port is not None:
                self._values["network_source_port"] = network_source_port
            if note_text is not None:
                self._values["note_text"] = note_text
            if note_updated_at is not None:
                self._values["note_updated_at"] = note_updated_at
            if note_updated_by is not None:
                self._values["note_updated_by"] = note_updated_by
            if process_launched_at is not None:
                self._values["process_launched_at"] = process_launched_at
            if process_name is not None:
                self._values["process_name"] = process_name
            if process_parent_pid is not None:
                self._values["process_parent_pid"] = process_parent_pid
            if process_path is not None:
                self._values["process_path"] = process_path
            if process_pid is not None:
                self._values["process_pid"] = process_pid
            if process_terminated_at is not None:
                self._values["process_terminated_at"] = process_terminated_at
            if product_arn is not None:
                self._values["product_arn"] = product_arn
            if product_fields is not None:
                self._values["product_fields"] = product_fields
            if product_name is not None:
                self._values["product_name"] = product_name
            if recommendation_text is not None:
                self._values["recommendation_text"] = recommendation_text
            if record_state is not None:
                self._values["record_state"] = record_state
            if region is not None:
                self._values["region"] = region
            if related_findings_id is not None:
                self._values["related_findings_id"] = related_findings_id
            if related_findings_product_arn is not None:
                self._values["related_findings_product_arn"] = related_findings_product_arn
            if resource_application_arn is not None:
                self._values["resource_application_arn"] = resource_application_arn
            if resource_application_name is not None:
                self._values["resource_application_name"] = resource_application_name
            if resource_aws_ec2_instance_iam_instance_profile_arn is not None:
                self._values["resource_aws_ec2_instance_iam_instance_profile_arn"] = resource_aws_ec2_instance_iam_instance_profile_arn
            if resource_aws_ec2_instance_image_id is not None:
                self._values["resource_aws_ec2_instance_image_id"] = resource_aws_ec2_instance_image_id
            if resource_aws_ec2_instance_ip_v4_addresses is not None:
                self._values["resource_aws_ec2_instance_ip_v4_addresses"] = resource_aws_ec2_instance_ip_v4_addresses
            if resource_aws_ec2_instance_ip_v6_addresses is not None:
                self._values["resource_aws_ec2_instance_ip_v6_addresses"] = resource_aws_ec2_instance_ip_v6_addresses
            if resource_aws_ec2_instance_key_name is not None:
                self._values["resource_aws_ec2_instance_key_name"] = resource_aws_ec2_instance_key_name
            if resource_aws_ec2_instance_launched_at is not None:
                self._values["resource_aws_ec2_instance_launched_at"] = resource_aws_ec2_instance_launched_at
            if resource_aws_ec2_instance_subnet_id is not None:
                self._values["resource_aws_ec2_instance_subnet_id"] = resource_aws_ec2_instance_subnet_id
            if resource_aws_ec2_instance_type is not None:
                self._values["resource_aws_ec2_instance_type"] = resource_aws_ec2_instance_type
            if resource_aws_ec2_instance_vpc_id is not None:
                self._values["resource_aws_ec2_instance_vpc_id"] = resource_aws_ec2_instance_vpc_id
            if resource_aws_iam_access_key_created_at is not None:
                self._values["resource_aws_iam_access_key_created_at"] = resource_aws_iam_access_key_created_at
            if resource_aws_iam_access_key_principal_name is not None:
                self._values["resource_aws_iam_access_key_principal_name"] = resource_aws_iam_access_key_principal_name
            if resource_aws_iam_access_key_status is not None:
                self._values["resource_aws_iam_access_key_status"] = resource_aws_iam_access_key_status
            if resource_aws_iam_access_key_user_name is not None:
                self._values["resource_aws_iam_access_key_user_name"] = resource_aws_iam_access_key_user_name
            if resource_aws_iam_user_user_name is not None:
                self._values["resource_aws_iam_user_user_name"] = resource_aws_iam_user_user_name
            if resource_aws_s3_bucket_owner_id is not None:
                self._values["resource_aws_s3_bucket_owner_id"] = resource_aws_s3_bucket_owner_id
            if resource_aws_s3_bucket_owner_name is not None:
                self._values["resource_aws_s3_bucket_owner_name"] = resource_aws_s3_bucket_owner_name
            if resource_container_image_id is not None:
                self._values["resource_container_image_id"] = resource_container_image_id
            if resource_container_image_name is not None:
                self._values["resource_container_image_name"] = resource_container_image_name
            if resource_container_launched_at is not None:
                self._values["resource_container_launched_at"] = resource_container_launched_at
            if resource_container_name is not None:
                self._values["resource_container_name"] = resource_container_name
            if resource_details_other is not None:
                self._values["resource_details_other"] = resource_details_other
            if resource_id is not None:
                self._values["resource_id"] = resource_id
            if resource_partition is not None:
                self._values["resource_partition"] = resource_partition
            if resource_region is not None:
                self._values["resource_region"] = resource_region
            if resource_tags is not None:
                self._values["resource_tags"] = resource_tags
            if resource_type is not None:
                self._values["resource_type"] = resource_type
            if sample is not None:
                self._values["sample"] = sample
            if severity_label is not None:
                self._values["severity_label"] = severity_label
            if severity_normalized is not None:
                self._values["severity_normalized"] = severity_normalized
            if severity_product is not None:
                self._values["severity_product"] = severity_product
            if source_url is not None:
                self._values["source_url"] = source_url
            if threat_intel_indicator_category is not None:
                self._values["threat_intel_indicator_category"] = threat_intel_indicator_category
            if threat_intel_indicator_last_observed_at is not None:
                self._values["threat_intel_indicator_last_observed_at"] = threat_intel_indicator_last_observed_at
            if threat_intel_indicator_source is not None:
                self._values["threat_intel_indicator_source"] = threat_intel_indicator_source
            if threat_intel_indicator_source_url is not None:
                self._values["threat_intel_indicator_source_url"] = threat_intel_indicator_source_url
            if threat_intel_indicator_type is not None:
                self._values["threat_intel_indicator_type"] = threat_intel_indicator_type
            if threat_intel_indicator_value is not None:
                self._values["threat_intel_indicator_value"] = threat_intel_indicator_value
            if title is not None:
                self._values["title"] = title
            if type is not None:
                self._values["type"] = type
            if updated_at is not None:
                self._values["updated_at"] = updated_at
            if user_defined_fields is not None:
                self._values["user_defined_fields"] = user_defined_fields
            if verification_state is not None:
                self._values["verification_state"] = verification_state
            if vulnerabilities_exploit_available is not None:
                self._values["vulnerabilities_exploit_available"] = vulnerabilities_exploit_available
            if vulnerabilities_fix_available is not None:
                self._values["vulnerabilities_fix_available"] = vulnerabilities_fix_available
            if workflow_state is not None:
                self._values["workflow_state"] = workflow_state
            if workflow_status is not None:
                self._values["workflow_status"] = workflow_status

        @builtins.property
        def aws_account_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The AWS account ID in which a finding is generated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-awsaccountid
            '''
            result = self._values.get("aws_account_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def aws_account_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The name of the AWS account in which a finding is generated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-awsaccountname
            '''
            result = self._values.get("aws_account_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def company_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The name of the findings provider (company) that owns the solution (product) that generates findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-companyname
            '''
            result = self._values.get("company_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def compliance_associated_standards_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The unique identifier of a standard in which a control is enabled.

            This field consists of the resource portion of the Amazon Resource Name (ARN) returned for a standard in the `DescribeStandards <https://docs.aws.amazon.com/securityhub/1.0/APIReference/API_DescribeStandards.html>`_ API response.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-complianceassociatedstandardsid
            '''
            result = self._values.get("compliance_associated_standards_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def compliance_security_control_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The unique identifier of a control across standards.

            Values for this field typically consist of an AWS service and a number, such as APIGateway.5.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-compliancesecuritycontrolid
            '''
            result = self._values.get("compliance_security_control_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def compliance_security_control_parameters_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The name of a security control parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-compliancesecuritycontrolparametersname
            '''
            result = self._values.get("compliance_security_control_parameters_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def compliance_security_control_parameters_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The current value of a security control parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-compliancesecuritycontrolparametersvalue
            '''
            result = self._values.get("compliance_security_control_parameters_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def compliance_status(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''Exclusive to findings that are generated as the result of a check run against a specific rule in a supported standard, such as CIS AWS Foundations.

            Contains security standard-related finding details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-compliancestatus
            '''
            result = self._values.get("compliance_status")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def confidence(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.NumberFilterProperty"]]]]:
            '''A finding's confidence.

            Confidence is defined as the likelihood that a finding accurately identifies the behavior or issue that it was intended to identify.

            Confidence is scored on a 0-100 basis using a ratio scale, where 0 means zero percent confidence and 100 means 100 percent confidence.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-confidence
            '''
            result = self._values.get("confidence")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.NumberFilterProperty"]]]], result)

        @builtins.property
        def created_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]]:
            '''A timestamp that indicates when the security findings provider created the potential security issue that a finding reflects.

            For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-createdat
            '''
            result = self._values.get("created_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def criticality(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.NumberFilterProperty"]]]]:
            '''The level of importance assigned to the resources associated with the finding.

            A score of 0 means that the underlying resources have no criticality, and a score of 100 is reserved for the most critical resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-criticality
            '''
            result = self._values.get("criticality")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.NumberFilterProperty"]]]], result)

        @builtins.property
        def description(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''A finding's description.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def finding_provider_fields_confidence(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.NumberFilterProperty"]]]]:
            '''The finding provider value for the finding confidence.

            Confidence is defined as the likelihood that a finding accurately identifies the behavior or issue that it was intended to identify.

            Confidence is scored on a 0-100 basis using a ratio scale, where 0 means zero percent confidence and 100 means 100 percent confidence.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-findingproviderfieldsconfidence
            '''
            result = self._values.get("finding_provider_fields_confidence")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.NumberFilterProperty"]]]], result)

        @builtins.property
        def finding_provider_fields_criticality(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.NumberFilterProperty"]]]]:
            '''The finding provider value for the level of importance assigned to the resources associated with the findings.

            A score of 0 means that the underlying resources have no criticality, and a score of 100 is reserved for the most critical resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-findingproviderfieldscriticality
            '''
            result = self._values.get("finding_provider_fields_criticality")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.NumberFilterProperty"]]]], result)

        @builtins.property
        def finding_provider_fields_related_findings_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The finding identifier of a related finding that is identified by the finding provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-findingproviderfieldsrelatedfindingsid
            '''
            result = self._values.get("finding_provider_fields_related_findings_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def finding_provider_fields_related_findings_product_arn(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The ARN of the solution that generated a related finding that is identified by the finding provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-findingproviderfieldsrelatedfindingsproductarn
            '''
            result = self._values.get("finding_provider_fields_related_findings_product_arn")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def finding_provider_fields_severity_label(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The finding provider value for the severity label.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-findingproviderfieldsseveritylabel
            '''
            result = self._values.get("finding_provider_fields_severity_label")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def finding_provider_fields_severity_original(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The finding provider's original value for the severity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-findingproviderfieldsseverityoriginal
            '''
            result = self._values.get("finding_provider_fields_severity_original")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def finding_provider_fields_types(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''One or more finding types that the finding provider assigned to the finding.

            Uses the format of ``namespace/category/classifier`` that classify a finding.

            Valid namespace values are: Software and Configuration Checks | TTPs | Effects | Unusual Behaviors | Sensitive Data Identifications

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-findingproviderfieldstypes
            '''
            result = self._values.get("finding_provider_fields_types")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def first_observed_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]]:
            '''A timestamp that indicates when the security findings provider first observed the potential security issue that a finding captured.

            For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-firstobservedat
            '''
            result = self._values.get("first_observed_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def generator_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The identifier for the solution-specific component (a discrete unit of logic) that generated a finding.

            In various security findings providers' solutions, this generator can be called a rule, a check, a detector, a plugin, etc.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-generatorid
            '''
            result = self._values.get("generator_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The security findings provider-specific identifier for a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def keyword(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.KeywordFilterProperty"]]]]:
            '''This field is deprecated.

            A keyword for a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-keyword
            '''
            result = self._values.get("keyword")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.KeywordFilterProperty"]]]], result)

        @builtins.property
        def last_observed_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]]:
            '''A timestamp that indicates when the security findings provider most recently observed a change in the resource that is involved in the finding.

            For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-lastobservedat
            '''
            result = self._values.get("last_observed_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def malware_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The name of the malware that was observed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-malwarename
            '''
            result = self._values.get("malware_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def malware_path(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The filesystem path of the malware that was observed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-malwarepath
            '''
            result = self._values.get("malware_path")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def malware_state(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The state of the malware that was observed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-malwarestate
            '''
            result = self._values.get("malware_state")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def malware_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The type of the malware that was observed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-malwaretype
            '''
            result = self._values.get("malware_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def network_destination_domain(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The destination domain of network-related information about a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-networkdestinationdomain
            '''
            result = self._values.get("network_destination_domain")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def network_destination_ip_v4(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.IpFilterProperty"]]]]:
            '''The destination IPv4 address of network-related information about a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-networkdestinationipv4
            '''
            result = self._values.get("network_destination_ip_v4")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.IpFilterProperty"]]]], result)

        @builtins.property
        def network_destination_ip_v6(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.IpFilterProperty"]]]]:
            '''The destination IPv6 address of network-related information about a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-networkdestinationipv6
            '''
            result = self._values.get("network_destination_ip_v6")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.IpFilterProperty"]]]], result)

        @builtins.property
        def network_destination_port(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.NumberFilterProperty"]]]]:
            '''The destination port of network-related information about a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-networkdestinationport
            '''
            result = self._values.get("network_destination_port")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.NumberFilterProperty"]]]], result)

        @builtins.property
        def network_direction(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''Indicates the direction of network traffic associated with a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-networkdirection
            '''
            result = self._values.get("network_direction")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def network_protocol(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The protocol of network-related information about a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-networkprotocol
            '''
            result = self._values.get("network_protocol")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def network_source_domain(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The source domain of network-related information about a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-networksourcedomain
            '''
            result = self._values.get("network_source_domain")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def network_source_ip_v4(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.IpFilterProperty"]]]]:
            '''The source IPv4 address of network-related information about a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-networksourceipv4
            '''
            result = self._values.get("network_source_ip_v4")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.IpFilterProperty"]]]], result)

        @builtins.property
        def network_source_ip_v6(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.IpFilterProperty"]]]]:
            '''The source IPv6 address of network-related information about a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-networksourceipv6
            '''
            result = self._values.get("network_source_ip_v6")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.IpFilterProperty"]]]], result)

        @builtins.property
        def network_source_mac(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The source media access control (MAC) address of network-related information about a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-networksourcemac
            '''
            result = self._values.get("network_source_mac")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def network_source_port(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.NumberFilterProperty"]]]]:
            '''The source port of network-related information about a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-networksourceport
            '''
            result = self._values.get("network_source_port")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.NumberFilterProperty"]]]], result)

        @builtins.property
        def note_text(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The text of a note.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-notetext
            '''
            result = self._values.get("note_text")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def note_updated_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]]:
            '''The timestamp of when the note was updated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-noteupdatedat
            '''
            result = self._values.get("note_updated_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def note_updated_by(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The principal that created a note.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-noteupdatedby
            '''
            result = self._values.get("note_updated_by")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def process_launched_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]]:
            '''A timestamp that identifies when the process was launched.

            For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-processlaunchedat
            '''
            result = self._values.get("process_launched_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def process_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The name of the process.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-processname
            '''
            result = self._values.get("process_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def process_parent_pid(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.NumberFilterProperty"]]]]:
            '''The parent process ID.

            This field accepts positive integers between ``O`` and ``2147483647`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-processparentpid
            '''
            result = self._values.get("process_parent_pid")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.NumberFilterProperty"]]]], result)

        @builtins.property
        def process_path(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The path to the process executable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-processpath
            '''
            result = self._values.get("process_path")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def process_pid(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.NumberFilterProperty"]]]]:
            '''The process ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-processpid
            '''
            result = self._values.get("process_pid")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.NumberFilterProperty"]]]], result)

        @builtins.property
        def process_terminated_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]]:
            '''A timestamp that identifies when the process was terminated.

            For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-processterminatedat
            '''
            result = self._values.get("process_terminated_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def product_arn(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The ARN generated by Security Hub that uniquely identifies a third-party company (security findings provider) after this provider's product (solution that generates findings) is registered with Security Hub.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-productarn
            '''
            result = self._values.get("product_arn")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def product_fields(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.MapFilterProperty"]]]]:
            '''A data type where security findings providers can include additional solution-specific details that aren't part of the defined ``AwsSecurityFinding`` format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-productfields
            '''
            result = self._values.get("product_fields")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.MapFilterProperty"]]]], result)

        @builtins.property
        def product_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The name of the solution (product) that generates findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-productname
            '''
            result = self._values.get("product_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def recommendation_text(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The recommendation of what to do about the issue described in a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-recommendationtext
            '''
            result = self._values.get("recommendation_text")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def record_state(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The updated record state for the finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-recordstate
            '''
            result = self._values.get("record_state")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def region(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The Region from which the finding was generated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def related_findings_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The solution-generated identifier for a related finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-relatedfindingsid
            '''
            result = self._values.get("related_findings_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def related_findings_product_arn(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The ARN of the solution that generated a related finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-relatedfindingsproductarn
            '''
            result = self._values.get("related_findings_product_arn")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_application_arn(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The ARN of the application that is related to a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourceapplicationarn
            '''
            result = self._values.get("resource_application_arn")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_application_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The name of the application that is related to a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourceapplicationname
            '''
            result = self._values.get("resource_application_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_aws_ec2_instance_iam_instance_profile_arn(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The IAM profile ARN of the instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourceawsec2instanceiaminstanceprofilearn
            '''
            result = self._values.get("resource_aws_ec2_instance_iam_instance_profile_arn")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_aws_ec2_instance_image_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The Amazon Machine Image (AMI) ID of the instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourceawsec2instanceimageid
            '''
            result = self._values.get("resource_aws_ec2_instance_image_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_aws_ec2_instance_ip_v4_addresses(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.IpFilterProperty"]]]]:
            '''The IPv4 addresses associated with the instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourceawsec2instanceipv4addresses
            '''
            result = self._values.get("resource_aws_ec2_instance_ip_v4_addresses")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.IpFilterProperty"]]]], result)

        @builtins.property
        def resource_aws_ec2_instance_ip_v6_addresses(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.IpFilterProperty"]]]]:
            '''The IPv6 addresses associated with the instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourceawsec2instanceipv6addresses
            '''
            result = self._values.get("resource_aws_ec2_instance_ip_v6_addresses")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.IpFilterProperty"]]]], result)

        @builtins.property
        def resource_aws_ec2_instance_key_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The key name associated with the instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourceawsec2instancekeyname
            '''
            result = self._values.get("resource_aws_ec2_instance_key_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_aws_ec2_instance_launched_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]]:
            '''The date and time the instance was launched.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourceawsec2instancelaunchedat
            '''
            result = self._values.get("resource_aws_ec2_instance_launched_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def resource_aws_ec2_instance_subnet_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The identifier of the subnet that the instance was launched in.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourceawsec2instancesubnetid
            '''
            result = self._values.get("resource_aws_ec2_instance_subnet_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_aws_ec2_instance_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The instance type of the instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourceawsec2instancetype
            '''
            result = self._values.get("resource_aws_ec2_instance_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_aws_ec2_instance_vpc_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The identifier of the VPC that the instance was launched in.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourceawsec2instancevpcid
            '''
            result = self._values.get("resource_aws_ec2_instance_vpc_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_aws_iam_access_key_created_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]]:
            '''The creation date/time of the IAM access key related to a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourceawsiamaccesskeycreatedat
            '''
            result = self._values.get("resource_aws_iam_access_key_created_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def resource_aws_iam_access_key_principal_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The name of the principal that is associated with an IAM access key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourceawsiamaccesskeyprincipalname
            '''
            result = self._values.get("resource_aws_iam_access_key_principal_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_aws_iam_access_key_status(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The status of the IAM access key related to a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourceawsiamaccesskeystatus
            '''
            result = self._values.get("resource_aws_iam_access_key_status")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_aws_iam_access_key_user_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''This field is deprecated.

            The username associated with the IAM access key related to a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourceawsiamaccesskeyusername
            '''
            result = self._values.get("resource_aws_iam_access_key_user_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_aws_iam_user_user_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The name of an IAM user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourceawsiamuserusername
            '''
            result = self._values.get("resource_aws_iam_user_user_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_aws_s3_bucket_owner_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The canonical user ID of the owner of the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourceawss3bucketownerid
            '''
            result = self._values.get("resource_aws_s3_bucket_owner_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_aws_s3_bucket_owner_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The display name of the owner of the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourceawss3bucketownername
            '''
            result = self._values.get("resource_aws_s3_bucket_owner_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_container_image_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The identifier of the image related to a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourcecontainerimageid
            '''
            result = self._values.get("resource_container_image_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_container_image_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The name of the image related to a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourcecontainerimagename
            '''
            result = self._values.get("resource_container_image_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_container_launched_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]]:
            '''A timestamp that identifies when the container was started.

            For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourcecontainerlaunchedat
            '''
            result = self._values.get("resource_container_launched_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def resource_container_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The name of the container related to a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourcecontainername
            '''
            result = self._values.get("resource_container_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_details_other(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.MapFilterProperty"]]]]:
            '''The details of a resource that doesn't have a specific subfield for the resource type defined.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourcedetailsother
            '''
            result = self._values.get("resource_details_other")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.MapFilterProperty"]]]], result)

        @builtins.property
        def resource_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The canonical identifier for the given resource type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourceid
            '''
            result = self._values.get("resource_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_partition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The canonical AWS partition name that the Region is assigned to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourcepartition
            '''
            result = self._values.get("resource_partition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_region(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The canonical AWS external Region name where this resource is located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourceregion
            '''
            result = self._values.get("resource_region")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_tags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.MapFilterProperty"]]]]:
            '''A list of AWS tags associated with a resource at the time the finding was processed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourcetags
            '''
            result = self._values.get("resource_tags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.MapFilterProperty"]]]], result)

        @builtins.property
        def resource_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''Specifies the type of the resource that details are provided for.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-resourcetype
            '''
            result = self._values.get("resource_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def sample(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.BooleanFilterProperty"]]]]:
            '''Indicates whether or not sample findings are included in the filter results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-sample
            '''
            result = self._values.get("sample")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.BooleanFilterProperty"]]]], result)

        @builtins.property
        def severity_label(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The label of a finding's severity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-severitylabel
            '''
            result = self._values.get("severity_label")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def severity_normalized(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.NumberFilterProperty"]]]]:
            '''Deprecated. The normalized severity of a finding. Instead of providing ``Normalized`` , provide ``Label`` .

            The value of ``Normalized`` can be an integer between ``0`` and ``100`` .

            If you provide ``Label`` and don't provide ``Normalized`` , then ``Normalized`` is set automatically as follows.

            - ``INFORMATIONAL`` - 0
            - ``LOW`` - 1
            - ``MEDIUM`` - 40
            - ``HIGH`` - 70
            - ``CRITICAL`` - 90

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-severitynormalized
            '''
            result = self._values.get("severity_normalized")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.NumberFilterProperty"]]]], result)

        @builtins.property
        def severity_product(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.NumberFilterProperty"]]]]:
            '''Deprecated. This attribute isn't included in findings. Instead of providing ``Product`` , provide ``Original`` .

            The native severity as defined by the AWS service or integrated partner product that generated the finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-severityproduct
            '''
            result = self._values.get("severity_product")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.NumberFilterProperty"]]]], result)

        @builtins.property
        def source_url(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''A URL that links to a page about the current finding in the security findings provider's solution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-sourceurl
            '''
            result = self._values.get("source_url")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def threat_intel_indicator_category(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The category of a threat intelligence indicator.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-threatintelindicatorcategory
            '''
            result = self._values.get("threat_intel_indicator_category")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def threat_intel_indicator_last_observed_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]]:
            '''A timestamp that identifies the last observation of a threat intelligence indicator.

            For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-threatintelindicatorlastobservedat
            '''
            result = self._values.get("threat_intel_indicator_last_observed_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def threat_intel_indicator_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The source of the threat intelligence.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-threatintelindicatorsource
            '''
            result = self._values.get("threat_intel_indicator_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def threat_intel_indicator_source_url(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The URL for more details from the source of the threat intelligence.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-threatintelindicatorsourceurl
            '''
            result = self._values.get("threat_intel_indicator_source_url")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def threat_intel_indicator_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The type of a threat intelligence indicator.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-threatintelindicatortype
            '''
            result = self._values.get("threat_intel_indicator_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def threat_intel_indicator_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The value of a threat intelligence indicator.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-threatintelindicatorvalue
            '''
            result = self._values.get("threat_intel_indicator_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def title(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''A finding's title.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''A finding type in the format of ``namespace/category/classifier`` that classifies a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def updated_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]]:
            '''A timestamp that indicates when the security findings provider last updated the finding record.

            For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-updatedat
            '''
            result = self._values.get("updated_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def user_defined_fields(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.MapFilterProperty"]]]]:
            '''A list of name/value string pairs associated with the finding.

            These are custom, user-defined fields added to a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-userdefinedfields
            '''
            result = self._values.get("user_defined_fields")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.MapFilterProperty"]]]], result)

        @builtins.property
        def verification_state(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The veracity of a finding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-verificationstate
            '''
            result = self._values.get("verification_state")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def vulnerabilities_exploit_available(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''Indicates whether a software vulnerability in your environment has a known exploit.

            You can filter findings by this field only if you use Security Hub and Amazon Inspector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-vulnerabilitiesexploitavailable
            '''
            result = self._values.get("vulnerabilities_exploit_available")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def vulnerabilities_fix_available(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''Indicates whether a vulnerability is fixed in a newer version of the affected software packages.

            You can filter findings by this field only if you use Security Hub and Amazon Inspector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-vulnerabilitiesfixavailable
            '''
            result = self._values.get("vulnerabilities_fix_available")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def workflow_state(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The workflow state of a finding.

            Note that this field is deprecated. To search for a finding based on its workflow status, use ``WorkflowStatus`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-workflowstate
            '''
            result = self._values.get("workflow_state")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def workflow_status(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]]:
            '''The status of the investigation into a finding. Allowed values are the following.

            - ``NEW`` - The initial state of a finding, before it is reviewed.

            Security Hub also resets the workflow status from ``NOTIFIED`` or ``RESOLVED`` to ``NEW`` in the following cases:

            - ``RecordState`` changes from ``ARCHIVED`` to ``ACTIVE`` .
            - ``Compliance.Status`` changes from ``PASSED`` to either ``WARNING`` , ``FAILED`` , or ``NOT_AVAILABLE`` .
            - ``NOTIFIED`` - Indicates that the resource owner has been notified about the security issue. Used when the initial reviewer is not the resource owner, and needs intervention from the resource owner.

            If one of the following occurs, the workflow status is changed automatically from ``NOTIFIED`` to ``NEW`` :

            - ``RecordState`` changes from ``ARCHIVED`` to ``ACTIVE`` .
            - ``Compliance.Status`` changes from ``PASSED`` to ``FAILED`` , ``WARNING`` , or ``NOT_AVAILABLE`` .
            - ``SUPPRESSED`` - Indicates that you reviewed the finding and don't believe that any action is needed.

            The workflow status of a ``SUPPRESSED`` finding does not change if ``RecordState`` changes from ``ARCHIVED`` to ``ACTIVE`` .

            - ``RESOLVED`` - The finding was reviewed and remediated and is now considered resolved.

            The finding remains ``RESOLVED`` unless one of the following occurs:

            - ``RecordState`` changes from ``ARCHIVED`` to ``ACTIVE`` .
            - ``Compliance.Status`` changes from ``PASSED`` to ``FAILED`` , ``WARNING`` , or ``NOT_AVAILABLE`` .

            In those cases, the workflow status is automatically reset to ``NEW`` .

            For findings from controls, if ``Compliance.Status`` is ``PASSED`` , then Security Hub automatically sets the workflow status to ``RESOLVED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-awssecurityfindingfilters.html#cfn-securityhub-insight-awssecurityfindingfilters-workflowstatus
            '''
            result = self._values.get("workflow_status")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.StringFilterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsSecurityFindingFiltersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnInsightPropsMixin.BooleanFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class BooleanFilterProperty:
        def __init__(
            self,
            *,
            value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Boolean filter for querying findings.

            :param value: The value of the boolean.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-booleanfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                boolean_filter_property = securityhub_mixins.CfnInsightPropsMixin.BooleanFilterProperty(
                    value=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a5c49ea2d5a63755edc5dd794add576e44bd643bf92b66f964157daae72e7123)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The value of the boolean.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-booleanfilter.html#cfn-securityhub-insight-booleanfilter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BooleanFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnInsightPropsMixin.DateFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"date_range": "dateRange", "end": "end", "start": "start"},
    )
    class DateFilterProperty:
        def __init__(
            self,
            *,
            date_range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInsightPropsMixin.DateRangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            end: typing.Optional[builtins.str] = None,
            start: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A date filter for querying findings.

            :param date_range: A date range for the date filter.
            :param end: A timestamp that provides the end date for the date filter. For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .
            :param start: A timestamp that provides the start date for the date filter. For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-datefilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                date_filter_property = securityhub_mixins.CfnInsightPropsMixin.DateFilterProperty(
                    date_range=securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                        unit="unit",
                        value=123
                    ),
                    end="end",
                    start="start"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__19bb77c68a1f852ad493f61588887f20e2db14fe813cf0ea9ff8f086ffb5e6bc)
                check_type(argname="argument date_range", value=date_range, expected_type=type_hints["date_range"])
                check_type(argname="argument end", value=end, expected_type=type_hints["end"])
                check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if date_range is not None:
                self._values["date_range"] = date_range
            if end is not None:
                self._values["end"] = end
            if start is not None:
                self._values["start"] = start

        @builtins.property
        def date_range(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateRangeProperty"]]:
            '''A date range for the date filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-datefilter.html#cfn-securityhub-insight-datefilter-daterange
            '''
            result = self._values.get("date_range")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInsightPropsMixin.DateRangeProperty"]], result)

        @builtins.property
        def end(self) -> typing.Optional[builtins.str]:
            '''A timestamp that provides the end date for the date filter.

            For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-datefilter.html#cfn-securityhub-insight-datefilter-end
            '''
            result = self._values.get("end")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start(self) -> typing.Optional[builtins.str]:
            '''A timestamp that provides the start date for the date filter.

            For more information about the validation and formatting of timestamp fields in Security Hub , see `Timestamps <https://docs.aws.amazon.com/securityhub/1.0/APIReference/Welcome.html#timestamps>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-datefilter.html#cfn-securityhub-insight-datefilter-start
            '''
            result = self._values.get("start")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DateFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnInsightPropsMixin.DateRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"unit": "unit", "value": "value"},
    )
    class DateRangeProperty:
        def __init__(
            self,
            *,
            unit: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A date range for the date filter.

            :param unit: A date range unit for the date filter.
            :param value: A date range value for the date filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-daterange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                date_range_property = securityhub_mixins.CfnInsightPropsMixin.DateRangeProperty(
                    unit="unit",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a2687c757cb4d175eb40a3c876ab0ba306df78e6a31cf66d39c805c1018130f2)
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if unit is not None:
                self._values["unit"] = unit
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''A date range unit for the date filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-daterange.html#cfn-securityhub-insight-daterange-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''A date range value for the date filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-daterange.html#cfn-securityhub-insight-daterange-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DateRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnInsightPropsMixin.IpFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"cidr": "cidr"},
    )
    class IpFilterProperty:
        def __init__(self, *, cidr: typing.Optional[builtins.str] = None) -> None:
            '''The IP filter for querying findings.

            :param cidr: A finding's CIDR value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-ipfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                ip_filter_property = securityhub_mixins.CfnInsightPropsMixin.IpFilterProperty(
                    cidr="cidr"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9750eb0a5742c8cd326a739ebf18b9ad2d0e995c4fd5991cfdd495b74104455d)
                check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cidr is not None:
                self._values["cidr"] = cidr

        @builtins.property
        def cidr(self) -> typing.Optional[builtins.str]:
            '''A finding's CIDR value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-ipfilter.html#cfn-securityhub-insight-ipfilter-cidr
            '''
            result = self._values.get("cidr")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IpFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnInsightPropsMixin.KeywordFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class KeywordFilterProperty:
        def __init__(self, *, value: typing.Optional[builtins.str] = None) -> None:
            '''A keyword filter for querying findings.

            :param value: A value for the keyword.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-keywordfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                keyword_filter_property = securityhub_mixins.CfnInsightPropsMixin.KeywordFilterProperty(
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__94d5ad9379640e4fcf89859bc3fb707bef3f1518f8ef0ad48a49405f9229d570)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''A value for the keyword.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-keywordfilter.html#cfn-securityhub-insight-keywordfilter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeywordFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnInsightPropsMixin.MapFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"comparison": "comparison", "key": "key", "value": "value"},
    )
    class MapFilterProperty:
        def __init__(
            self,
            *,
            comparison: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A map filter for filtering Security Hub findings.

            Each map filter provides the field to check for, the value to check for, and the comparison operator.

            :param comparison: The condition to apply to the key value when filtering Security Hub findings with a map filter. To search for values that have the filter value, use one of the following comparison operators: - To search for values that include the filter value, use ``CONTAINS`` . For example, for the ``ResourceTags`` field, the filter ``Department CONTAINS Security`` matches findings that include the value ``Security`` for the ``Department`` tag. In the same example, a finding with a value of ``Security team`` for the ``Department`` tag is a match. - To search for values that exactly match the filter value, use ``EQUALS`` . For example, for the ``ResourceTags`` field, the filter ``Department EQUALS Security`` matches findings that have the value ``Security`` for the ``Department`` tag. ``CONTAINS`` and ``EQUALS`` filters on the same field are joined by ``OR`` . A finding matches if it matches any one of those filters. For example, the filters ``Department CONTAINS Security OR Department CONTAINS Finance`` match a finding that includes either ``Security`` , ``Finance`` , or both values. To search for values that don't have the filter value, use one of the following comparison operators: - To search for values that exclude the filter value, use ``NOT_CONTAINS`` . For example, for the ``ResourceTags`` field, the filter ``Department NOT_CONTAINS Finance`` matches findings that exclude the value ``Finance`` for the ``Department`` tag. - To search for values other than the filter value, use ``NOT_EQUALS`` . For example, for the ``ResourceTags`` field, the filter ``Department NOT_EQUALS Finance`` matches findings that don’t have the value ``Finance`` for the ``Department`` tag. ``NOT_CONTAINS`` and ``NOT_EQUALS`` filters on the same field are joined by ``AND`` . A finding matches only if it matches all of those filters. For example, the filters ``Department NOT_CONTAINS Security AND Department NOT_CONTAINS Finance`` match a finding that excludes both the ``Security`` and ``Finance`` values. ``CONTAINS`` filters can only be used with other ``CONTAINS`` filters. ``NOT_CONTAINS`` filters can only be used with other ``NOT_CONTAINS`` filters. You can’t have both a ``CONTAINS`` filter and a ``NOT_CONTAINS`` filter on the same field. Similarly, you can’t have both an ``EQUALS`` filter and a ``NOT_EQUALS`` filter on the same field. Combining filters in this way returns an error. ``CONTAINS`` and ``NOT_CONTAINS`` operators can be used only with automation rules. For more information, see `Automation rules <https://docs.aws.amazon.com/securityhub/latest/userguide/automation-rules.html>`_ in the *Security Hub User Guide* .
            :param key: The key of the map filter. For example, for ``ResourceTags`` , ``Key`` identifies the name of the tag. For ``UserDefinedFields`` , ``Key`` is the name of the field.
            :param value: The value for the key in the map filter. Filter values are case sensitive. For example, one of the values for a tag called ``Department`` might be ``Security`` . If you provide ``security`` as the filter value, then there's no match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-mapfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                map_filter_property = securityhub_mixins.CfnInsightPropsMixin.MapFilterProperty(
                    comparison="comparison",
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__72e2eb46e1d2c10dd2f5a6d4880770bed89a565ebe4fc5f2352d69642086a96e)
                check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparison is not None:
                self._values["comparison"] = comparison
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def comparison(self) -> typing.Optional[builtins.str]:
            '''The condition to apply to the key value when filtering Security Hub findings with a map filter.

            To search for values that have the filter value, use one of the following comparison operators:

            - To search for values that include the filter value, use ``CONTAINS`` . For example, for the ``ResourceTags`` field, the filter ``Department CONTAINS Security`` matches findings that include the value ``Security`` for the ``Department`` tag. In the same example, a finding with a value of ``Security team`` for the ``Department`` tag is a match.
            - To search for values that exactly match the filter value, use ``EQUALS`` . For example, for the ``ResourceTags`` field, the filter ``Department EQUALS Security`` matches findings that have the value ``Security`` for the ``Department`` tag.

            ``CONTAINS`` and ``EQUALS`` filters on the same field are joined by ``OR`` . A finding matches if it matches any one of those filters. For example, the filters ``Department CONTAINS Security OR Department CONTAINS Finance`` match a finding that includes either ``Security`` , ``Finance`` , or both values.

            To search for values that don't have the filter value, use one of the following comparison operators:

            - To search for values that exclude the filter value, use ``NOT_CONTAINS`` . For example, for the ``ResourceTags`` field, the filter ``Department NOT_CONTAINS Finance`` matches findings that exclude the value ``Finance`` for the ``Department`` tag.
            - To search for values other than the filter value, use ``NOT_EQUALS`` . For example, for the ``ResourceTags`` field, the filter ``Department NOT_EQUALS Finance`` matches findings that don’t have the value ``Finance`` for the ``Department`` tag.

            ``NOT_CONTAINS`` and ``NOT_EQUALS`` filters on the same field are joined by ``AND`` . A finding matches only if it matches all of those filters. For example, the filters ``Department NOT_CONTAINS Security AND Department NOT_CONTAINS Finance`` match a finding that excludes both the ``Security`` and ``Finance`` values.

            ``CONTAINS`` filters can only be used with other ``CONTAINS`` filters. ``NOT_CONTAINS`` filters can only be used with other ``NOT_CONTAINS`` filters.

            You can’t have both a ``CONTAINS`` filter and a ``NOT_CONTAINS`` filter on the same field. Similarly, you can’t have both an ``EQUALS`` filter and a ``NOT_EQUALS`` filter on the same field. Combining filters in this way returns an error.

            ``CONTAINS`` and ``NOT_CONTAINS`` operators can be used only with automation rules. For more information, see `Automation rules <https://docs.aws.amazon.com/securityhub/latest/userguide/automation-rules.html>`_ in the *Security Hub User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-mapfilter.html#cfn-securityhub-insight-mapfilter-comparison
            '''
            result = self._values.get("comparison")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key of the map filter.

            For example, for ``ResourceTags`` , ``Key`` identifies the name of the tag. For ``UserDefinedFields`` , ``Key`` is the name of the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-mapfilter.html#cfn-securityhub-insight-mapfilter-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value for the key in the map filter.

            Filter values are case sensitive. For example, one of the values for a tag called ``Department`` might be ``Security`` . If you provide ``security`` as the filter value, then there's no match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-mapfilter.html#cfn-securityhub-insight-mapfilter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MapFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnInsightPropsMixin.NumberFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"eq": "eq", "gte": "gte", "lte": "lte"},
    )
    class NumberFilterProperty:
        def __init__(
            self,
            *,
            eq: typing.Optional[jsii.Number] = None,
            gte: typing.Optional[jsii.Number] = None,
            lte: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A number filter for querying findings.

            :param eq: The equal-to condition to be applied to a single field when querying for findings.
            :param gte: The greater-than-equal condition to be applied to a single field when querying for findings.
            :param lte: The less-than-equal condition to be applied to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-numberfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                number_filter_property = securityhub_mixins.CfnInsightPropsMixin.NumberFilterProperty(
                    eq=123,
                    gte=123,
                    lte=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ce0856142e23b6b526a54b356a6f64082e07b3c784cddd1e00355af23672521b)
                check_type(argname="argument eq", value=eq, expected_type=type_hints["eq"])
                check_type(argname="argument gte", value=gte, expected_type=type_hints["gte"])
                check_type(argname="argument lte", value=lte, expected_type=type_hints["lte"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if eq is not None:
                self._values["eq"] = eq
            if gte is not None:
                self._values["gte"] = gte
            if lte is not None:
                self._values["lte"] = lte

        @builtins.property
        def eq(self) -> typing.Optional[jsii.Number]:
            '''The equal-to condition to be applied to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-numberfilter.html#cfn-securityhub-insight-numberfilter-eq
            '''
            result = self._values.get("eq")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def gte(self) -> typing.Optional[jsii.Number]:
            '''The greater-than-equal condition to be applied to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-numberfilter.html#cfn-securityhub-insight-numberfilter-gte
            '''
            result = self._values.get("gte")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def lte(self) -> typing.Optional[jsii.Number]:
            '''The less-than-equal condition to be applied to a single field when querying for findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-numberfilter.html#cfn-securityhub-insight-numberfilter-lte
            '''
            result = self._values.get("lte")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NumberFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnInsightPropsMixin.StringFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"comparison": "comparison", "value": "value"},
    )
    class StringFilterProperty:
        def __init__(
            self,
            *,
            comparison: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A string filter for filtering Security Hub findings.

            :param comparison: The condition to apply to a string value when filtering Security Hub findings. To search for values that have the filter value, use one of the following comparison operators: - To search for values that include the filter value, use ``CONTAINS`` . For example, the filter ``Title CONTAINS CloudFront`` matches findings that have a ``Title`` that includes the string CloudFront. - To search for values that exactly match the filter value, use ``EQUALS`` . For example, the filter ``AwsAccountId EQUALS 123456789012`` only matches findings that have an account ID of ``123456789012`` . - To search for values that start with the filter value, use ``PREFIX`` . For example, the filter ``ResourceRegion PREFIX us`` matches findings that have a ``ResourceRegion`` that starts with ``us`` . A ``ResourceRegion`` that starts with a different value, such as ``af`` , ``ap`` , or ``ca`` , doesn't match. ``CONTAINS`` , ``EQUALS`` , and ``PREFIX`` filters on the same field are joined by ``OR`` . A finding matches if it matches any one of those filters. For example, the filters ``Title CONTAINS CloudFront OR Title CONTAINS CloudWatch`` match a finding that includes either ``CloudFront`` , ``CloudWatch`` , or both strings in the title. To search for values that don’t have the filter value, use one of the following comparison operators: - To search for values that exclude the filter value, use ``NOT_CONTAINS`` . For example, the filter ``Title NOT_CONTAINS CloudFront`` matches findings that have a ``Title`` that excludes the string CloudFront. - To search for values other than the filter value, use ``NOT_EQUALS`` . For example, the filter ``AwsAccountId NOT_EQUALS 123456789012`` only matches findings that have an account ID other than ``123456789012`` . - To search for values that don't start with the filter value, use ``PREFIX_NOT_EQUALS`` . For example, the filter ``ResourceRegion PREFIX_NOT_EQUALS us`` matches findings with a ``ResourceRegion`` that starts with a value other than ``us`` . ``NOT_CONTAINS`` , ``NOT_EQUALS`` , and ``PREFIX_NOT_EQUALS`` filters on the same field are joined by ``AND`` . A finding matches only if it matches all of those filters. For example, the filters ``Title NOT_CONTAINS CloudFront AND Title NOT_CONTAINS CloudWatch`` match a finding that excludes both ``CloudFront`` and ``CloudWatch`` in the title. You can’t have both a ``CONTAINS`` filter and a ``NOT_CONTAINS`` filter on the same field. Similarly, you can't provide both an ``EQUALS`` filter and a ``NOT_EQUALS`` or ``PREFIX_NOT_EQUALS`` filter on the same field. Combining filters in this way returns an error. ``CONTAINS`` filters can only be used with other ``CONTAINS`` filters. ``NOT_CONTAINS`` filters can only be used with other ``NOT_CONTAINS`` filters. You can combine ``PREFIX`` filters with ``NOT_EQUALS`` or ``PREFIX_NOT_EQUALS`` filters for the same field. Security Hub first processes the ``PREFIX`` filters, and then the ``NOT_EQUALS`` or ``PREFIX_NOT_EQUALS`` filters. For example, for the following filters, Security Hub first identifies findings that have resource types that start with either ``AwsIam`` or ``AwsEc2`` . It then excludes findings that have a resource type of ``AwsIamPolicy`` and findings that have a resource type of ``AwsEc2NetworkInterface`` . - ``ResourceType PREFIX AwsIam`` - ``ResourceType PREFIX AwsEc2`` - ``ResourceType NOT_EQUALS AwsIamPolicy`` - ``ResourceType NOT_EQUALS AwsEc2NetworkInterface`` ``CONTAINS`` and ``NOT_CONTAINS`` operators can be used only with automation rules V1. ``CONTAINS_WORD`` operator is only supported in ``GetFindingsV2`` , ``GetFindingStatisticsV2`` , ``GetResourcesV2`` , and ``GetResourceStatisticsV2`` APIs. For more information, see `Automation rules <https://docs.aws.amazon.com/securityhub/latest/userguide/automation-rules.html>`_ in the *Security Hub User Guide* .
            :param value: The string filter value. Filter values are case sensitive. For example, the product name for control-based findings is ``Security Hub`` . If you provide ``security hub`` as the filter value, there's no match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-stringfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                string_filter_property = securityhub_mixins.CfnInsightPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fe1fd8e4530fb7d39fc43c31d70d6ae6aca96fc7c7040ce03d9573f980df3060)
                check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparison is not None:
                self._values["comparison"] = comparison
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def comparison(self) -> typing.Optional[builtins.str]:
            '''The condition to apply to a string value when filtering Security Hub findings.

            To search for values that have the filter value, use one of the following comparison operators:

            - To search for values that include the filter value, use ``CONTAINS`` . For example, the filter ``Title CONTAINS CloudFront`` matches findings that have a ``Title`` that includes the string CloudFront.
            - To search for values that exactly match the filter value, use ``EQUALS`` . For example, the filter ``AwsAccountId EQUALS 123456789012`` only matches findings that have an account ID of ``123456789012`` .
            - To search for values that start with the filter value, use ``PREFIX`` . For example, the filter ``ResourceRegion PREFIX us`` matches findings that have a ``ResourceRegion`` that starts with ``us`` . A ``ResourceRegion`` that starts with a different value, such as ``af`` , ``ap`` , or ``ca`` , doesn't match.

            ``CONTAINS`` , ``EQUALS`` , and ``PREFIX`` filters on the same field are joined by ``OR`` . A finding matches if it matches any one of those filters. For example, the filters ``Title CONTAINS CloudFront OR Title CONTAINS CloudWatch`` match a finding that includes either ``CloudFront`` , ``CloudWatch`` , or both strings in the title.

            To search for values that don’t have the filter value, use one of the following comparison operators:

            - To search for values that exclude the filter value, use ``NOT_CONTAINS`` . For example, the filter ``Title NOT_CONTAINS CloudFront`` matches findings that have a ``Title`` that excludes the string CloudFront.
            - To search for values other than the filter value, use ``NOT_EQUALS`` . For example, the filter ``AwsAccountId NOT_EQUALS 123456789012`` only matches findings that have an account ID other than ``123456789012`` .
            - To search for values that don't start with the filter value, use ``PREFIX_NOT_EQUALS`` . For example, the filter ``ResourceRegion PREFIX_NOT_EQUALS us`` matches findings with a ``ResourceRegion`` that starts with a value other than ``us`` .

            ``NOT_CONTAINS`` , ``NOT_EQUALS`` , and ``PREFIX_NOT_EQUALS`` filters on the same field are joined by ``AND`` . A finding matches only if it matches all of those filters. For example, the filters ``Title NOT_CONTAINS CloudFront AND Title NOT_CONTAINS CloudWatch`` match a finding that excludes both ``CloudFront`` and ``CloudWatch`` in the title.

            You can’t have both a ``CONTAINS`` filter and a ``NOT_CONTAINS`` filter on the same field. Similarly, you can't provide both an ``EQUALS`` filter and a ``NOT_EQUALS`` or ``PREFIX_NOT_EQUALS`` filter on the same field. Combining filters in this way returns an error. ``CONTAINS`` filters can only be used with other ``CONTAINS`` filters. ``NOT_CONTAINS`` filters can only be used with other ``NOT_CONTAINS`` filters.

            You can combine ``PREFIX`` filters with ``NOT_EQUALS`` or ``PREFIX_NOT_EQUALS`` filters for the same field. Security Hub first processes the ``PREFIX`` filters, and then the ``NOT_EQUALS`` or ``PREFIX_NOT_EQUALS`` filters.

            For example, for the following filters, Security Hub first identifies findings that have resource types that start with either ``AwsIam`` or ``AwsEc2`` . It then excludes findings that have a resource type of ``AwsIamPolicy`` and findings that have a resource type of ``AwsEc2NetworkInterface`` .

            - ``ResourceType PREFIX AwsIam``
            - ``ResourceType PREFIX AwsEc2``
            - ``ResourceType NOT_EQUALS AwsIamPolicy``
            - ``ResourceType NOT_EQUALS AwsEc2NetworkInterface``

            ``CONTAINS`` and ``NOT_CONTAINS`` operators can be used only with automation rules V1. ``CONTAINS_WORD`` operator is only supported in ``GetFindingsV2`` , ``GetFindingStatisticsV2`` , ``GetResourcesV2`` , and ``GetResourceStatisticsV2`` APIs. For more information, see `Automation rules <https://docs.aws.amazon.com/securityhub/latest/userguide/automation-rules.html>`_ in the *Security Hub User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-stringfilter.html#cfn-securityhub-insight-stringfilter-comparison
            '''
            result = self._values.get("comparison")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The string filter value.

            Filter values are case sensitive. For example, the product name for control-based findings is ``Security Hub`` . If you provide ``security hub`` as the filter value, there's no match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-insight-stringfilter.html#cfn-securityhub-insight-stringfilter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StringFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnOrganizationConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_enable": "autoEnable",
        "auto_enable_standards": "autoEnableStandards",
        "configuration_type": "configurationType",
    },
)
class CfnOrganizationConfigurationMixinProps:
    def __init__(
        self,
        *,
        auto_enable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        auto_enable_standards: typing.Optional[builtins.str] = None,
        configuration_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnOrganizationConfigurationPropsMixin.

        :param auto_enable: Whether to automatically enable Security Hub in new member accounts when they join the organization. If set to ``true`` , then Security Hub is automatically enabled in new accounts. If set to ``false`` , then Security Hub isn't enabled in new accounts automatically. The default value is ``false`` . If the ``ConfigurationType`` of your organization is set to ``CENTRAL`` , then this field is set to ``false`` and can't be changed in the home Region and linked Regions. However, in that case, the delegated administrator can create a configuration policy in which Security Hub is enabled and associate the policy with new organization accounts.
        :param auto_enable_standards: Whether to automatically enable Security Hub `default standards <https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-enable-disable.html>`_ in new member accounts when they join the organization. The default value of this parameter is equal to ``DEFAULT`` . If equal to ``DEFAULT`` , then Security Hub default standards are automatically enabled for new member accounts. If equal to ``NONE`` , then default standards are not automatically enabled for new member accounts. If the ``ConfigurationType`` of your organization is set to ``CENTRAL`` , then this field is set to ``NONE`` and can't be changed in the home Region and linked Regions. However, in that case, the delegated administrator can create a configuration policy in which specific security standards are enabled and associate the policy with new organization accounts.
        :param configuration_type: Indicates whether the organization uses local or central configuration. If you use local configuration, the Security Hub delegated administrator can set ``AutoEnable`` to ``true`` and ``AutoEnableStandards`` to ``DEFAULT`` . This automatically enables Security Hub and default security standards in new organization accounts. These new account settings must be set separately in each AWS Region , and settings may be different in each Region. If you use central configuration, the delegated administrator can create configuration policies. Configuration policies can be used to configure Security Hub, security standards, and security controls in multiple accounts and Regions. If you want new organization accounts to use a specific configuration, you can create a configuration policy and associate it with the root or specific organizational units (OUs). New accounts will inherit the policy from the root or their assigned OU.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-organizationconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
            
            cfn_organization_configuration_mixin_props = securityhub_mixins.CfnOrganizationConfigurationMixinProps(
                auto_enable=False,
                auto_enable_standards="autoEnableStandards",
                configuration_type="configurationType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c974562a44abdb476bb056b25ad3bc789bb5bf282c468dc7c99046d94d4ae881)
            check_type(argname="argument auto_enable", value=auto_enable, expected_type=type_hints["auto_enable"])
            check_type(argname="argument auto_enable_standards", value=auto_enable_standards, expected_type=type_hints["auto_enable_standards"])
            check_type(argname="argument configuration_type", value=configuration_type, expected_type=type_hints["configuration_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_enable is not None:
            self._values["auto_enable"] = auto_enable
        if auto_enable_standards is not None:
            self._values["auto_enable_standards"] = auto_enable_standards
        if configuration_type is not None:
            self._values["configuration_type"] = configuration_type

    @builtins.property
    def auto_enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to automatically enable Security Hub in new member accounts when they join the organization.

        If set to ``true`` , then Security Hub is automatically enabled in new accounts. If set to ``false`` , then Security Hub isn't enabled in new accounts automatically. The default value is ``false`` .

        If the ``ConfigurationType`` of your organization is set to ``CENTRAL`` , then this field is set to ``false`` and can't be changed in the home Region and linked Regions. However, in that case, the delegated administrator can create a configuration policy in which Security Hub is enabled and associate the policy with new organization accounts.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-organizationconfiguration.html#cfn-securityhub-organizationconfiguration-autoenable
        '''
        result = self._values.get("auto_enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def auto_enable_standards(self) -> typing.Optional[builtins.str]:
        '''Whether to automatically enable Security Hub `default standards <https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-enable-disable.html>`_ in new member accounts when they join the organization.

        The default value of this parameter is equal to ``DEFAULT`` .

        If equal to ``DEFAULT`` , then Security Hub default standards are automatically enabled for new member accounts. If equal to ``NONE`` , then default standards are not automatically enabled for new member accounts.

        If the ``ConfigurationType`` of your organization is set to ``CENTRAL`` , then this field is set to ``NONE`` and can't be changed in the home Region and linked Regions. However, in that case, the delegated administrator can create a configuration policy in which specific security standards are enabled and associate the policy with new organization accounts.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-organizationconfiguration.html#cfn-securityhub-organizationconfiguration-autoenablestandards
        '''
        result = self._values.get("auto_enable_standards")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration_type(self) -> typing.Optional[builtins.str]:
        '''Indicates whether the organization uses local or central configuration.

        If you use local configuration, the Security Hub delegated administrator can set ``AutoEnable`` to ``true`` and ``AutoEnableStandards`` to ``DEFAULT`` . This automatically enables Security Hub and default security standards in new organization accounts. These new account settings must be set separately in each AWS Region , and settings may be different in each Region.

        If you use central configuration, the delegated administrator can create configuration policies. Configuration policies can be used to configure Security Hub, security standards, and security controls in multiple accounts and Regions. If you want new organization accounts to use a specific configuration, you can create a configuration policy and associate it with the root or specific organizational units (OUs). New accounts will inherit the policy from the root or their assigned OU.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-organizationconfiguration.html#cfn-securityhub-organizationconfiguration-configurationtype
        '''
        result = self._values.get("configuration_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOrganizationConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnOrganizationConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnOrganizationConfigurationPropsMixin",
):
    '''The ``AWS::SecurityHub::OrganizationConfiguration`` resource specifies the way that your AWS organization is configured in Security Hub .

    Specifically, you can use this resource to specify the configuration type for your organization and whether to automatically Security Hub and security standards in new member accounts. For more information, see `Managing administrator and member accounts <https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-accounts.html>`_ in the *Security Hub User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-organizationconfiguration.html
    :cloudformationResource: AWS::SecurityHub::OrganizationConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
        
        cfn_organization_configuration_props_mixin = securityhub_mixins.CfnOrganizationConfigurationPropsMixin(securityhub_mixins.CfnOrganizationConfigurationMixinProps(
            auto_enable=False,
            auto_enable_standards="autoEnableStandards",
            configuration_type="configurationType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnOrganizationConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecurityHub::OrganizationConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7433f807f85aa09a7d57c9a84564e3e6e35014049d67fed3b44526c42ccd1cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3493e8a7b5c252441c12503a99fe62c4c17fb2915893f363d5b701d6e421def9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d487bb52b5baf2aae15f7ba8ee353aee59f9bc4ed893a627e20988b301dc8b6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOrganizationConfigurationMixinProps:
        return typing.cast(CfnOrganizationConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnPolicyAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_policy_id": "configurationPolicyId",
        "target_id": "targetId",
        "target_type": "targetType",
    },
)
class CfnPolicyAssociationMixinProps:
    def __init__(
        self,
        *,
        configuration_policy_id: typing.Optional[builtins.str] = None,
        target_id: typing.Optional[builtins.str] = None,
        target_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPolicyAssociationPropsMixin.

        :param configuration_policy_id: The universally unique identifier (UUID) of the configuration policy. A self-managed configuration has no UUID. The identifier of a self-managed configuration is ``SELF_MANAGED_SECURITY_HUB`` .
        :param target_id: The identifier of the target account, organizational unit, or the root.
        :param target_type: Specifies whether the target is an AWS account , organizational unit, or the root.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-policyassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
            
            cfn_policy_association_mixin_props = securityhub_mixins.CfnPolicyAssociationMixinProps(
                configuration_policy_id="configurationPolicyId",
                target_id="targetId",
                target_type="targetType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60283011007072cff8d76971a1f0a9c4980467e47aed3653d3f2da1c9001223a)
            check_type(argname="argument configuration_policy_id", value=configuration_policy_id, expected_type=type_hints["configuration_policy_id"])
            check_type(argname="argument target_id", value=target_id, expected_type=type_hints["target_id"])
            check_type(argname="argument target_type", value=target_type, expected_type=type_hints["target_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration_policy_id is not None:
            self._values["configuration_policy_id"] = configuration_policy_id
        if target_id is not None:
            self._values["target_id"] = target_id
        if target_type is not None:
            self._values["target_type"] = target_type

    @builtins.property
    def configuration_policy_id(self) -> typing.Optional[builtins.str]:
        '''The universally unique identifier (UUID) of the configuration policy.

        A self-managed configuration has no UUID. The identifier of a self-managed configuration is ``SELF_MANAGED_SECURITY_HUB`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-policyassociation.html#cfn-securityhub-policyassociation-configurationpolicyid
        '''
        result = self._values.get("configuration_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the target account, organizational unit, or the root.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-policyassociation.html#cfn-securityhub-policyassociation-targetid
        '''
        result = self._values.get("target_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_type(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the target is an AWS account , organizational unit, or the root.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-policyassociation.html#cfn-securityhub-policyassociation-targettype
        '''
        result = self._values.get("target_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPolicyAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPolicyAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnPolicyAssociationPropsMixin",
):
    '''The ``AWS::SecurityHub::PolicyAssociation`` resource specifies associations for a configuration policy or a self-managed configuration.

    You can associate a Security Hub configuration policy or self-managed configuration with the organization root, organizational units (OUs), or AWS accounts . After a successful association, the configuration policy takes effect in the specified targets. For more information, see `Creating and associating Security Hub configuration policies <https://docs.aws.amazon.com/securityhub/latest/userguide/create-associate-policy.html>`_ in the *Security Hub User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-policyassociation.html
    :cloudformationResource: AWS::SecurityHub::PolicyAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
        
        cfn_policy_association_props_mixin = securityhub_mixins.CfnPolicyAssociationPropsMixin(securityhub_mixins.CfnPolicyAssociationMixinProps(
            configuration_policy_id="configurationPolicyId",
            target_id="targetId",
            target_type="targetType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPolicyAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecurityHub::PolicyAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f588f5dc98f10c00db814978221ef3198c78a8b0eaa4fa2c8231e006d60d588)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3f3604df74643a6a96d4000fcc5e19e236f242f9fc0fc82894333e5fb3910be)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6acc6da90a875bc051b4506e6d23bdf63fa1b0ff0d0b358efb7d084bf099b4e9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPolicyAssociationMixinProps:
        return typing.cast(CfnPolicyAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnProductSubscriptionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"product_arn": "productArn"},
)
class CfnProductSubscriptionMixinProps:
    def __init__(self, *, product_arn: typing.Optional[builtins.str] = None) -> None:
        '''Properties for CfnProductSubscriptionPropsMixin.

        :param product_arn: The ARN of the product to enable the integration for.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-productsubscription.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
            
            cfn_product_subscription_mixin_props = securityhub_mixins.CfnProductSubscriptionMixinProps(
                product_arn="productArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3b82f6495069be060f852c3442fdf853994fb2c1de629ceb77cad213b314868)
            check_type(argname="argument product_arn", value=product_arn, expected_type=type_hints["product_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if product_arn is not None:
            self._values["product_arn"] = product_arn

    @builtins.property
    def product_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the product to enable the integration for.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-productsubscription.html#cfn-securityhub-productsubscription-productarn
        '''
        result = self._values.get("product_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProductSubscriptionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnProductSubscriptionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnProductSubscriptionPropsMixin",
):
    '''The ``AWS::SecurityHub::ProductSubscription`` resource creates a subscription to a third-party product that generates findings that you want to receive in Security Hub .

    For a list of integrations to third-party products, see `Available third-party partner product integrations <https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-partner-providers.html>`_ in the *Security Hub User Guide* .

    To change a product subscription, remove the current product subscription resource, and then create a new one.

    Tags aren't supported for this resource.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-productsubscription.html
    :cloudformationResource: AWS::SecurityHub::ProductSubscription
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
        
        cfn_product_subscription_props_mixin = securityhub_mixins.CfnProductSubscriptionPropsMixin(securityhub_mixins.CfnProductSubscriptionMixinProps(
            product_arn="productArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnProductSubscriptionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecurityHub::ProductSubscription``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c55a7cfbcd242974de53a0f75ace7dd5422480ded5811aa5376459b4a5ef32e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbb63a1433a42001157d9add73b581bc39e564045109e90fa7affc96ed671297)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77c75b506e9218897e52b2744453d2f4210a17e6b243d2575b067853c1b8a0e1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnProductSubscriptionMixinProps:
        return typing.cast(CfnProductSubscriptionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnSecurityControlMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "last_update_reason": "lastUpdateReason",
        "parameters": "parameters",
        "security_control_arn": "securityControlArn",
        "security_control_id": "securityControlId",
    },
)
class CfnSecurityControlMixinProps:
    def __init__(
        self,
        *,
        last_update_reason: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSecurityControlPropsMixin.ParameterConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        security_control_arn: typing.Optional[builtins.str] = None,
        security_control_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSecurityControlPropsMixin.

        :param last_update_reason: The most recent reason for updating the customizable properties of a security control. This differs from the ``UpdateReason`` field of the ```BatchUpdateStandardsControlAssociations`` <https://docs.aws.amazon.com/securityhub/1.0/APIReference/API_BatchUpdateStandardsControlAssociations.html>`_ API, which tracks the reason for updating the enablement status of a control. This field accepts alphanumeric characters in addition to white spaces, dashes, and underscores.
        :param parameters: An object that identifies the name of a control parameter, its current value, and whether it has been customized.
        :param security_control_arn: The Amazon Resource Name (ARN) for a security control across standards, such as ``arn:aws:securityhub:eu-central-1:123456789012:security-control/S3.1`` . This parameter doesn't mention a specific standard.
        :param security_control_id: The unique identifier of a security control across standards. Values for this field typically consist of an AWS service name and a number, such as APIGateway.3.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-securitycontrol.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
            
            cfn_security_control_mixin_props = securityhub_mixins.CfnSecurityControlMixinProps(
                last_update_reason="lastUpdateReason",
                parameters={
                    "parameters_key": securityhub_mixins.CfnSecurityControlPropsMixin.ParameterConfigurationProperty(
                        value=securityhub_mixins.CfnSecurityControlPropsMixin.ParameterValueProperty(
                            boolean=False,
                            double=123,
                            enum="enum",
                            enum_list=["enumList"],
                            integer=123,
                            integer_list=[123],
                            string="string",
                            string_list=["stringList"]
                        ),
                        value_type="valueType"
                    )
                },
                security_control_arn="securityControlArn",
                security_control_id="securityControlId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8ca3ccdf93f6b612234256891c7b870c005a867821e239fd180e0eafafa25d9)
            check_type(argname="argument last_update_reason", value=last_update_reason, expected_type=type_hints["last_update_reason"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument security_control_arn", value=security_control_arn, expected_type=type_hints["security_control_arn"])
            check_type(argname="argument security_control_id", value=security_control_id, expected_type=type_hints["security_control_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if last_update_reason is not None:
            self._values["last_update_reason"] = last_update_reason
        if parameters is not None:
            self._values["parameters"] = parameters
        if security_control_arn is not None:
            self._values["security_control_arn"] = security_control_arn
        if security_control_id is not None:
            self._values["security_control_id"] = security_control_id

    @builtins.property
    def last_update_reason(self) -> typing.Optional[builtins.str]:
        '''The most recent reason for updating the customizable properties of a security control.

        This differs from the ``UpdateReason`` field of the ```BatchUpdateStandardsControlAssociations`` <https://docs.aws.amazon.com/securityhub/1.0/APIReference/API_BatchUpdateStandardsControlAssociations.html>`_ API, which tracks the reason for updating the enablement status of a control. This field accepts alphanumeric characters in addition to white spaces, dashes, and underscores.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-securitycontrol.html#cfn-securityhub-securitycontrol-lastupdatereason
        '''
        result = self._values.get("last_update_reason")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityControlPropsMixin.ParameterConfigurationProperty"]]]]:
        '''An object that identifies the name of a control parameter, its current value, and whether it has been customized.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-securitycontrol.html#cfn-securityhub-securitycontrol-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityControlPropsMixin.ParameterConfigurationProperty"]]]], result)

    @builtins.property
    def security_control_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) for a security control across standards, such as ``arn:aws:securityhub:eu-central-1:123456789012:security-control/S3.1`` . This parameter doesn't mention a specific standard.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-securitycontrol.html#cfn-securityhub-securitycontrol-securitycontrolarn
        '''
        result = self._values.get("security_control_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_control_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of a security control across standards.

        Values for this field typically consist of an AWS service name and a number, such as APIGateway.3.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-securitycontrol.html#cfn-securityhub-securitycontrol-securitycontrolid
        '''
        result = self._values.get("security_control_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecurityControlMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSecurityControlPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnSecurityControlPropsMixin",
):
    '''The ``AWS::SecurityHub::SecurityControl`` resource specifies custom parameter values for an Security Hub control.

    For a list of controls that support custom parameters, see `Security Hub controls reference <https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-controls-reference.html>`_ . You can also use this resource to specify the use of default parameter values for a control. For more information about custom parameters, see `Custom control parameters <https://docs.aws.amazon.com/securityhub/latest/userguide/custom-control-parameters.html>`_ in the *Security Hub User Guide* .

    Tags aren't supported for this resource.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-securitycontrol.html
    :cloudformationResource: AWS::SecurityHub::SecurityControl
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
        
        cfn_security_control_props_mixin = securityhub_mixins.CfnSecurityControlPropsMixin(securityhub_mixins.CfnSecurityControlMixinProps(
            last_update_reason="lastUpdateReason",
            parameters={
                "parameters_key": securityhub_mixins.CfnSecurityControlPropsMixin.ParameterConfigurationProperty(
                    value=securityhub_mixins.CfnSecurityControlPropsMixin.ParameterValueProperty(
                        boolean=False,
                        double=123,
                        enum="enum",
                        enum_list=["enumList"],
                        integer=123,
                        integer_list=[123],
                        string="string",
                        string_list=["stringList"]
                    ),
                    value_type="valueType"
                )
            },
            security_control_arn="securityControlArn",
            security_control_id="securityControlId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSecurityControlMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecurityHub::SecurityControl``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d416a40580e9db3d4805dc135f7be8f9d4f11cc1b65dd298cf421d9f41dc7bb7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a22b099bb9de5b35190c53052d5efe78bfdb3023747729242b9ac4baa26d1ac8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__697d167bb206c16854b6a365c1d655b81e8bb07c3dc803ff19650c9270199f54)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSecurityControlMixinProps:
        return typing.cast(CfnSecurityControlMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnSecurityControlPropsMixin.ParameterConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value", "value_type": "valueType"},
    )
    class ParameterConfigurationProperty:
        def __init__(
            self,
            *,
            value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSecurityControlPropsMixin.ParameterValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            value_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that provides the current value of a security control parameter and identifies whether it has been customized.

            :param value: The current value of a control parameter.
            :param value_type: Identifies whether a control parameter uses a custom user-defined value or subscribes to the default Security Hub behavior. When ``ValueType`` is set equal to ``DEFAULT`` , the default behavior can be a specific Security Hub default value, or the default behavior can be to ignore a specific parameter. When ``ValueType`` is set equal to ``DEFAULT`` , Security Hub ignores user-provided input for the ``Value`` field. When ``ValueType`` is set equal to ``CUSTOM`` , the ``Value`` field can't be empty.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-securitycontrol-parameterconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                parameter_configuration_property = securityhub_mixins.CfnSecurityControlPropsMixin.ParameterConfigurationProperty(
                    value=securityhub_mixins.CfnSecurityControlPropsMixin.ParameterValueProperty(
                        boolean=False,
                        double=123,
                        enum="enum",
                        enum_list=["enumList"],
                        integer=123,
                        integer_list=[123],
                        string="string",
                        string_list=["stringList"]
                    ),
                    value_type="valueType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__48d4219b5d6d1f2147c62256874d763cde06610c391797bd9a16a7a9c9a0fedb)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                check_type(argname="argument value_type", value=value_type, expected_type=type_hints["value_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if value is not None:
                self._values["value"] = value
            if value_type is not None:
                self._values["value_type"] = value_type

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityControlPropsMixin.ParameterValueProperty"]]:
            '''The current value of a control parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-securitycontrol-parameterconfiguration.html#cfn-securityhub-securitycontrol-parameterconfiguration-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityControlPropsMixin.ParameterValueProperty"]], result)

        @builtins.property
        def value_type(self) -> typing.Optional[builtins.str]:
            '''Identifies whether a control parameter uses a custom user-defined value or subscribes to the default Security Hub behavior.

            When ``ValueType`` is set equal to ``DEFAULT`` , the default behavior can be a specific Security Hub default value, or the default behavior can be to ignore a specific parameter. When ``ValueType`` is set equal to ``DEFAULT`` , Security Hub ignores user-provided input for the ``Value`` field.

            When ``ValueType`` is set equal to ``CUSTOM`` , the ``Value`` field can't be empty.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-securitycontrol-parameterconfiguration.html#cfn-securityhub-securitycontrol-parameterconfiguration-valuetype
            '''
            result = self._values.get("value_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnSecurityControlPropsMixin.ParameterValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "boolean": "boolean",
            "double": "double",
            "enum": "enum",
            "enum_list": "enumList",
            "integer": "integer",
            "integer_list": "integerList",
            "string": "string",
            "string_list": "stringList",
        },
    )
    class ParameterValueProperty:
        def __init__(
            self,
            *,
            boolean: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            double: typing.Optional[jsii.Number] = None,
            enum: typing.Optional[builtins.str] = None,
            enum_list: typing.Optional[typing.Sequence[builtins.str]] = None,
            integer: typing.Optional[jsii.Number] = None,
            integer_list: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
            string: typing.Optional[builtins.str] = None,
            string_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''An object that includes the data type of a security control parameter and its current value.

            :param boolean: A control parameter that is a boolean.
            :param double: A control parameter that is a double.
            :param enum: A control parameter that is an enum.
            :param enum_list: A control parameter that is a list of enums.
            :param integer: A control parameter that is an integer.
            :param integer_list: A control parameter that is a list of integers.
            :param string: A control parameter that is a string.
            :param string_list: A control parameter that is a list of strings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-securitycontrol-parametervalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                parameter_value_property = securityhub_mixins.CfnSecurityControlPropsMixin.ParameterValueProperty(
                    boolean=False,
                    double=123,
                    enum="enum",
                    enum_list=["enumList"],
                    integer=123,
                    integer_list=[123],
                    string="string",
                    string_list=["stringList"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b94b0555188c55f578a87f690b333612a252473aa88b395731d9093e029b75cf)
                check_type(argname="argument boolean", value=boolean, expected_type=type_hints["boolean"])
                check_type(argname="argument double", value=double, expected_type=type_hints["double"])
                check_type(argname="argument enum", value=enum, expected_type=type_hints["enum"])
                check_type(argname="argument enum_list", value=enum_list, expected_type=type_hints["enum_list"])
                check_type(argname="argument integer", value=integer, expected_type=type_hints["integer"])
                check_type(argname="argument integer_list", value=integer_list, expected_type=type_hints["integer_list"])
                check_type(argname="argument string", value=string, expected_type=type_hints["string"])
                check_type(argname="argument string_list", value=string_list, expected_type=type_hints["string_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if boolean is not None:
                self._values["boolean"] = boolean
            if double is not None:
                self._values["double"] = double
            if enum is not None:
                self._values["enum"] = enum
            if enum_list is not None:
                self._values["enum_list"] = enum_list
            if integer is not None:
                self._values["integer"] = integer
            if integer_list is not None:
                self._values["integer_list"] = integer_list
            if string is not None:
                self._values["string"] = string
            if string_list is not None:
                self._values["string_list"] = string_list

        @builtins.property
        def boolean(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A control parameter that is a boolean.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-securitycontrol-parametervalue.html#cfn-securityhub-securitycontrol-parametervalue-boolean
            '''
            result = self._values.get("boolean")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def double(self) -> typing.Optional[jsii.Number]:
            '''A control parameter that is a double.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-securitycontrol-parametervalue.html#cfn-securityhub-securitycontrol-parametervalue-double
            '''
            result = self._values.get("double")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def enum(self) -> typing.Optional[builtins.str]:
            '''A control parameter that is an enum.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-securitycontrol-parametervalue.html#cfn-securityhub-securitycontrol-parametervalue-enum
            '''
            result = self._values.get("enum")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enum_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A control parameter that is a list of enums.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-securitycontrol-parametervalue.html#cfn-securityhub-securitycontrol-parametervalue-enumlist
            '''
            result = self._values.get("enum_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def integer(self) -> typing.Optional[jsii.Number]:
            '''A control parameter that is an integer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-securitycontrol-parametervalue.html#cfn-securityhub-securitycontrol-parametervalue-integer
            '''
            result = self._values.get("integer")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def integer_list(
            self,
        ) -> typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]]:
            '''A control parameter that is a list of integers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-securitycontrol-parametervalue.html#cfn-securityhub-securitycontrol-parametervalue-integerlist
            '''
            result = self._values.get("integer_list")
            return typing.cast(typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def string(self) -> typing.Optional[builtins.str]:
            '''A control parameter that is a string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-securitycontrol-parametervalue.html#cfn-securityhub-securitycontrol-parametervalue-string
            '''
            result = self._values.get("string")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def string_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A control parameter that is a list of strings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-securitycontrol-parametervalue.html#cfn-securityhub-securitycontrol-parametervalue-stringlist
            '''
            result = self._values.get("string_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnStandardMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "disabled_standards_controls": "disabledStandardsControls",
        "standards_arn": "standardsArn",
    },
)
class CfnStandardMixinProps:
    def __init__(
        self,
        *,
        disabled_standards_controls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStandardPropsMixin.StandardsControlProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        standards_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnStandardPropsMixin.

        :param disabled_standards_controls: Specifies which controls are to be disabled in a standard. *Maximum* : ``100``
        :param standards_arn: The ARN of the standard that you want to enable. To view a list of available Security Hub standards and their ARNs, use the ```DescribeStandards`` <https://docs.aws.amazon.com/securityhub/1.0/APIReference/API_DescribeStandards.html>`_ API operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-standard.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
            
            cfn_standard_mixin_props = securityhub_mixins.CfnStandardMixinProps(
                disabled_standards_controls=[securityhub_mixins.CfnStandardPropsMixin.StandardsControlProperty(
                    reason="reason",
                    standards_control_arn="standardsControlArn"
                )],
                standards_arn="standardsArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24a0254c5a919836e1bffeaf0a4839fe228f5b054d90dbb54db84bfa8d8af9d8)
            check_type(argname="argument disabled_standards_controls", value=disabled_standards_controls, expected_type=type_hints["disabled_standards_controls"])
            check_type(argname="argument standards_arn", value=standards_arn, expected_type=type_hints["standards_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disabled_standards_controls is not None:
            self._values["disabled_standards_controls"] = disabled_standards_controls
        if standards_arn is not None:
            self._values["standards_arn"] = standards_arn

    @builtins.property
    def disabled_standards_controls(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStandardPropsMixin.StandardsControlProperty"]]]]:
        '''Specifies which controls are to be disabled in a standard.

        *Maximum* : ``100``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-standard.html#cfn-securityhub-standard-disabledstandardscontrols
        '''
        result = self._values.get("disabled_standards_controls")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStandardPropsMixin.StandardsControlProperty"]]]], result)

    @builtins.property
    def standards_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the standard that you want to enable.

        To view a list of available Security Hub standards and their ARNs, use the ```DescribeStandards`` <https://docs.aws.amazon.com/securityhub/1.0/APIReference/API_DescribeStandards.html>`_ API operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-standard.html#cfn-securityhub-standard-standardsarn
        '''
        result = self._values.get("standards_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStandardMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStandardPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnStandardPropsMixin",
):
    '''The ``AWS::SecurityHub::Standard`` resource specifies the enablement of a security standard.

    The standard is identified by the ``StandardsArn`` property. To view a list of Security Hub standards and their Amazon Resource Names (ARNs), use the ```DescribeStandards`` <https://docs.aws.amazon.com/securityhub/1.0/APIReference/API_DescribeStandards.html>`_ API operation.

    You must create a separate ``AWS::SecurityHub::Standard`` resource for each standard that you want to enable.

    For more information about Security Hub standards, see `Security Hub standards reference <https://docs.aws.amazon.com/securityhub/latest/userguide/standards-reference.html>`_ in the *Security Hub User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-standard.html
    :cloudformationResource: AWS::SecurityHub::Standard
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
        
        cfn_standard_props_mixin = securityhub_mixins.CfnStandardPropsMixin(securityhub_mixins.CfnStandardMixinProps(
            disabled_standards_controls=[securityhub_mixins.CfnStandardPropsMixin.StandardsControlProperty(
                reason="reason",
                standards_control_arn="standardsControlArn"
            )],
            standards_arn="standardsArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStandardMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecurityHub::Standard``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19f2e0fc9c261ad2f100ea510bf97117ef8e6b063726d3647579c1666c6cb86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d61b70ccf44e6f66a81f73f28a6bdb68f61a4842174d3b5a09688ba2d6f51261)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0ef7b576bfe312b11211cb7d2d856211c728c496f55d89524a6bf23f2468366)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStandardMixinProps:
        return typing.cast(CfnStandardMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_securityhub.mixins.CfnStandardPropsMixin.StandardsControlProperty",
        jsii_struct_bases=[],
        name_mapping={
            "reason": "reason",
            "standards_control_arn": "standardsControlArn",
        },
    )
    class StandardsControlProperty:
        def __init__(
            self,
            *,
            reason: typing.Optional[builtins.str] = None,
            standards_control_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides details about an individual security control.

            For a list of Security Hub controls, see `Security Hub controls reference <https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-controls-reference.html>`_ in the *Security Hub User Guide* .

            :param reason: A user-defined reason for changing a control's enablement status in a specified standard. If you are disabling a control, then this property is required.
            :param standards_control_arn: The Amazon Resource Name (ARN) of the control.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-standard-standardscontrol.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_securityhub import mixins as securityhub_mixins
                
                standards_control_property = securityhub_mixins.CfnStandardPropsMixin.StandardsControlProperty(
                    reason="reason",
                    standards_control_arn="standardsControlArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2e73006c8103b249db8cd6b1351e5454c6270bb3e69e0bf07eb0b7505104f749)
                check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
                check_type(argname="argument standards_control_arn", value=standards_control_arn, expected_type=type_hints["standards_control_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if reason is not None:
                self._values["reason"] = reason
            if standards_control_arn is not None:
                self._values["standards_control_arn"] = standards_control_arn

        @builtins.property
        def reason(self) -> typing.Optional[builtins.str]:
            '''A user-defined reason for changing a control's enablement status in a specified standard.

            If you are disabling a control, then this property is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-standard-standardscontrol.html#cfn-securityhub-standard-standardscontrol-reason
            '''
            result = self._values.get("reason")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def standards_control_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the control.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-securityhub-standard-standardscontrol.html#cfn-securityhub-standard-standardscontrol-standardscontrolarn
            '''
            result = self._values.get("standards_control_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StandardsControlProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAggregatorV2MixinProps",
    "CfnAggregatorV2PropsMixin",
    "CfnAutomationRuleMixinProps",
    "CfnAutomationRulePropsMixin",
    "CfnAutomationRuleV2MixinProps",
    "CfnAutomationRuleV2PropsMixin",
    "CfnConfigurationPolicyMixinProps",
    "CfnConfigurationPolicyPropsMixin",
    "CfnConnectorV2MixinProps",
    "CfnConnectorV2PropsMixin",
    "CfnDelegatedAdminMixinProps",
    "CfnDelegatedAdminPropsMixin",
    "CfnFindingAggregatorMixinProps",
    "CfnFindingAggregatorPropsMixin",
    "CfnHubMixinProps",
    "CfnHubPropsMixin",
    "CfnHubV2MixinProps",
    "CfnHubV2PropsMixin",
    "CfnInsightMixinProps",
    "CfnInsightPropsMixin",
    "CfnOrganizationConfigurationMixinProps",
    "CfnOrganizationConfigurationPropsMixin",
    "CfnPolicyAssociationMixinProps",
    "CfnPolicyAssociationPropsMixin",
    "CfnProductSubscriptionMixinProps",
    "CfnProductSubscriptionPropsMixin",
    "CfnSecurityControlMixinProps",
    "CfnSecurityControlPropsMixin",
    "CfnStandardMixinProps",
    "CfnStandardPropsMixin",
]

publication.publish()

def _typecheckingstub__94a0be53248e71505756e873712b092f8245a8ee330ec1d0f3d45f835de94e65(
    *,
    linked_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    region_linking_mode: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787e8b8e0c660635784e53469a8f18424e99616ae5d978f19b7a41f73a9e7da2(
    props: typing.Union[CfnAggregatorV2MixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b2fdd2580683bc5efbbdf48eee650b494ce24eb35ea15873beac6fd51ca8d6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5173e7e30309ba7ec3a2a6730cc669ee64c39c8d47c8ac56e248c21c7f86fc3a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a70cef8f5a998ff81255474b5ecd87ae9262528abe56d7e08471607a3f3087a(
    *,
    actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.AutomationRulesActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.AutomationRulesFindingFiltersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    is_terminal: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    rule_order: typing.Optional[jsii.Number] = None,
    rule_status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6748fd3a79a421df9da6fcbf09f3ca9ae5755d1006a8da6ec298b899962475(
    props: typing.Union[CfnAutomationRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93dd561ebd751e2dc39fcc38423895e06bb109c4f9bad51ec2e3d4827ed2b7ec(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394061078b77abb48e8a4a1d13eb12f1b81c87aab225a608f708f254ffe3ed2a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ce770db050ea565f4c3954a65295943e200ab82c04c708fe4b4c69e93f8765(
    *,
    finding_fields_update: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.AutomationRulesFindingFieldsUpdateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9caccaffd68cfa73b75727e86e1bfd297f74176363a2ee21b154e03dfd4a64(
    *,
    confidence: typing.Optional[jsii.Number] = None,
    criticality: typing.Optional[jsii.Number] = None,
    note: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.NoteUpdateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    related_findings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.RelatedFindingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    severity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.SeverityUpdateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_defined_fields: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    verification_state: typing.Optional[builtins.str] = None,
    workflow: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.WorkflowUpdateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8127f519a65ecfc36503e83965da3e3b1c879e797289424cddc8dbf795def5a2(
    *,
    aws_account_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    company_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    compliance_associated_standards_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    compliance_security_control_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    compliance_status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    confidence: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.NumberFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    created_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    criticality: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.NumberFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    first_observed_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    generator_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    last_observed_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    note_text: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    note_updated_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    note_updated_by: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    product_arn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    product_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    record_state: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    related_findings_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    related_findings_product_arn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_details_other: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.MapFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_partition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_region: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.MapFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    severity_label: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    source_url: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    title: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    updated_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    user_defined_fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.MapFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    verification_state: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    workflow_status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887ee0b850afa49cf671af6f233fa520e9eeff3942f097b5662298458928ca39(
    *,
    date_range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRulePropsMixin.DateRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    end: typing.Optional[builtins.str] = None,
    start: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c335575fda70574a4598a85fa398ae9ac244bdd2aa1325aefaa206d38565a6f(
    *,
    unit: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e5190129c990b1ca04431029e9500d9cdfc4f210df966a29bf52a3d3fa7afc4(
    *,
    comparison: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad083af91387ea6a85dd77ee35e7fa6f8506afb1560e352c6847ae1e6e2a0255(
    *,
    text: typing.Optional[builtins.str] = None,
    updated_by: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4153abc33c162931c5d6ae0e1d5ae3729ccc732bbc75d33a331fbdeda019e9(
    *,
    eq: typing.Optional[jsii.Number] = None,
    gte: typing.Optional[jsii.Number] = None,
    lte: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f15cfd2baa345c2c93664ca3e713784a5968626d0dca86de0e11ab7e6deb2a5(
    *,
    id: typing.Optional[builtins.str] = None,
    product_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d580b2b8ab190975a635761224118468a0eb39d45a62d66d4e1d0819a78eca6(
    *,
    label: typing.Optional[builtins.str] = None,
    normalized: typing.Optional[jsii.Number] = None,
    product: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5af0045035d0ec226bafd57a68aea5745b5a6c67d531f3f221a3d63d36a0de(
    *,
    comparison: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__987c6edb8b6d55217ef13ccf0cad34a20a0f4b7df6cebac361796031f5494456(
    *,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d12e74f0b1b682f2c83ae4d3f8d880b607ca7874f0baa478df278f8c8926de(
    *,
    actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRuleV2PropsMixin.AutomationRulesActionV2Property, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRuleV2PropsMixin.CriteriaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    rule_name: typing.Optional[builtins.str] = None,
    rule_order: typing.Optional[jsii.Number] = None,
    rule_status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9bb1402ffecec33af1d0d0c40b081f11637786ef53f78c3532dd2fd0cb3bc43(
    props: typing.Union[CfnAutomationRuleV2MixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__878fd859efe37ae68cf1ff9304252db7df901d4e4ed255dbfa68175255803a40(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b49aeb4ee3f1af4846212e9be8b88783cb2d04630f6b244e8c2897ecaba631(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5f9a6a4ec16cf9afb43324ebbd34e60ec01211a91ff01927c40cce4f0cc97b(
    *,
    external_integration_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRuleV2PropsMixin.ExternalIntegrationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    finding_fields_update: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRuleV2PropsMixin.AutomationRulesFindingFieldsUpdateV2Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2aed98906c741a9bd2fbe66dd1c32466fc8e648cc422e94de9724787a733e5(
    *,
    comment: typing.Optional[builtins.str] = None,
    severity_id: typing.Optional[jsii.Number] = None,
    status_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e72cadef72fcac5d45eecf8613e805dcebeb42086dc987d581a4bb67368b4493(
    *,
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36e833683d7b1f7c421c9ee85f415dd03466d176834b653f19b93275f35f43a7(
    *,
    boolean_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRuleV2PropsMixin.OcsfBooleanFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    date_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRuleV2PropsMixin.OcsfDateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    map_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRuleV2PropsMixin.OcsfMapFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    number_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRuleV2PropsMixin.OcsfNumberFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    operator: typing.Optional[builtins.str] = None,
    string_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRuleV2PropsMixin.OcsfStringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__729e7751a827d45283d5d908d2e5650dad538a290161d1ea6591a6deaa72c8bb(
    *,
    ocsf_finding_criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRuleV2PropsMixin.OcsfFindingFiltersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64cd3498225ef1f5db7396e7502e89a686745f296b4bbde01699c5a83ab34fa4(
    *,
    date_range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRuleV2PropsMixin.DateRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    end: typing.Optional[builtins.str] = None,
    start: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82e9e1f885af03664275a31b1e42d75c036733ea2ef9ce19143b89a8b6ec8b26(
    *,
    unit: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__132a13ec3c8311d3f3566f788d9037f9b65e87d870ab887fa10b541e4c98dda7(
    *,
    connector_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7145a119909f83b1489396d9999910a45e7d3197a046bafabd777f208dc3b8(
    *,
    comparison: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd1d5a8d0a884dc06297e8458dc5067836aa260871c82c300a95d3f6b4126355(
    *,
    eq: typing.Optional[jsii.Number] = None,
    gte: typing.Optional[jsii.Number] = None,
    lte: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a84fa5467bc5586d94f4dc420529fd5c80f7efbcc01d0cc6d5c5b7c008c0022(
    *,
    field_name: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRuleV2PropsMixin.BooleanFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__100d8a84541df070a70ab96b9d8f6ccbbc7317ce35bfe72aa5671b58fbe2fe5b(
    *,
    field_name: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRuleV2PropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e9abbd14e681a3715371939d3dc05934f3f9e5a9edb34c097b7e76a7aabde2f(
    *,
    composite_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRuleV2PropsMixin.CompositeFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    composite_operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4937851c68bd1c796025a3d3a917d11501c9785832334283ee57ea0d9b350ca1(
    *,
    field_name: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRuleV2PropsMixin.MapFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a786d7a7db9d2c2715f32c47900a6ccf157404ad71aed5ec7e2c2d6d6313d7(
    *,
    field_name: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRuleV2PropsMixin.NumberFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5861d0c9ca94acbe1fa13925e1d37574617eefac15192f106468b646e38b63e(
    *,
    field_name: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAutomationRuleV2PropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9937d4f883461d4a8a0676685218ae1013eda27bd7ad0a856c9aaf064f7ff7db(
    *,
    comparison: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82c67982d5b9eeb31b4268fd7a812fe836420897813487e5ddade98ae1e203d9(
    *,
    configuration_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationPolicyPropsMixin.PolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c7c81e721bb900af9bf7d428c2c2752adea9b5ea90871fbe2ce3a970e8d800(
    props: typing.Union[CfnConfigurationPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2db8731ab603f80b44b64a6b266f853bc19959f5c6f60a96cbbc2dec786f166(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a044a2446e8918746c91d966efd523716d0680cd3d64b6912e7919bca21de10(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bde4000cb262bb351f3f5d290d5cbe013273260740c7ece9e08061246ac3105(
    *,
    value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationPolicyPropsMixin.ParameterValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    value_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99a664ea7a26fbe10e27f1366544baf139354b31677f334764990f528fbf2a4(
    *,
    boolean: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    double: typing.Optional[jsii.Number] = None,
    enum: typing.Optional[builtins.str] = None,
    enum_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    integer: typing.Optional[jsii.Number] = None,
    integer_list: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
    string: typing.Optional[builtins.str] = None,
    string_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb8f5063963535e82785bc2685c614f68c3327834f3ace3d20e83efa4dae1969(
    *,
    security_hub: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationPolicyPropsMixin.SecurityHubPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9390657837a2f432cce4ea1dfe29cd420bc5c185e7c3d1508c55f331102e73f(
    *,
    parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationPolicyPropsMixin.ParameterConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    security_control_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ee235ad6ff1e9193ce9097890b6cb1e4fd139833d341d4ae6eb678de4656ff(
    *,
    disabled_security_control_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    enabled_security_control_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_control_custom_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationPolicyPropsMixin.SecurityControlCustomParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff3f55cf550c41cd67ddd71b073a51ba5a935699977851da551d194a17ef1091(
    *,
    enabled_standard_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_controls_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationPolicyPropsMixin.SecurityControlsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b22347b8af8ff6166538acb768c1292612f49946453d2e3ac3d5001855bc4d5(
    *,
    description: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorV2PropsMixin.ProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2571ff827250644f09e77d1c7aeca64d2fad1da1353f066e7dab2abca4cc5e(
    props: typing.Union[CfnConnectorV2MixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86d742876fbfd018a3dfde3f24ddfed44e6523a0ae48088a72f02a1835e67c3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e3b25e8891a2ecafacb9224aeb43519cfeea9aab0fdfe23cf7c15a2b2ec51a3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd173e2ec00f03ba6bcbf862bdafacb962eee58cc2d81bb7e7e3d12f50301733(
    *,
    auth_status: typing.Optional[builtins.str] = None,
    auth_url: typing.Optional[builtins.str] = None,
    cloud_id: typing.Optional[builtins.str] = None,
    domain: typing.Optional[builtins.str] = None,
    project_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f7081c25d2848f6ae2b23694987a30d7a650e6d67210b5c7343b0b04102a05(
    *,
    jira_cloud: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorV2PropsMixin.JiraCloudProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_now: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorV2PropsMixin.ServiceNowProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e6ca319f5c8e3a5e3f2eacfaa71751100d76204608b43d90716d0cdf7d1736(
    *,
    auth_status: typing.Optional[builtins.str] = None,
    instance_name: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8015c40264beb7267e661110c1c223c2d2d1152f3057d71d5be5c3d24371a905(
    *,
    admin_account_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b99c1513192a76b80d79193b8862c81b1a3308580e69bc764209fb1d40390c27(
    props: typing.Union[CfnDelegatedAdminMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0677209278f2d317b3afd32dd57ef2f2a6c199d6d7ab65af9ef6dc32264a1724(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7374a76c97a42d33c0dee974acaa90beeaf655428cfab93aedc2ecce25b5e5cb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f600bc6a7f51ab524f76ab1acec837910c25f7e719e77d0623cb9647ade2310(
    *,
    region_linking_mode: typing.Optional[builtins.str] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b15a52bd15cde4c4e9c19741a7be267f516ccb80c39709254ee52128508c2484(
    props: typing.Union[CfnFindingAggregatorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1bd477a4af5c7507cbca9919aa2ff70bfe6ef5e8a573d51cd362e500e6b7858(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42085121f61127d737c25cc384e925737944b0bf2e6dd1a1b6c29fdde1a5c68e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b16e6189f76d51cb37c62c4b36719cb50413f90512560854aada939a2c2eeab(
    *,
    auto_enable_controls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    control_finding_generator: typing.Optional[builtins.str] = None,
    enable_default_standards: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cffecc941a4a46096a36942db426921bf3a6167d394c0c36f633c608f8d598db(
    props: typing.Union[CfnHubMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d4c4cba6618837143bcfc8717e1a3d4cdbdf8fc648783f22a26eb2d1fdd48b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea50b08c74955869488b50ec99412131d74cfaed1e9d3271aafc319a91c1eee(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bce1aeaf7e3934efe86c8a459bd1869f1a69eaaf9f811963b5b5d39ef825c37(
    *,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd0d04ae0a27edbd9e9e8d7723c469ddf552fbd70b03f46d4245a8ed91fb4a1(
    props: typing.Union[CfnHubV2MixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5005f813c187dcec86503e6ba1d184eeb2a25c6436d24a98828336dc9cea74d3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a6e460c102a3458892fc1a3608cfb67c743d358f19ec2a8defb0637f7306e6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adc8ac0638e05ab2a5066ec5a09ecf1b0b18f778a3fd0aacaea32dad91d9e56b(
    *,
    filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.AwsSecurityFindingFiltersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    group_by_attribute: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b99110acc2e8bbb88d64bb9620e6c1a41e4e9647d346603e3fa4498e29d6a8cf(
    props: typing.Union[CfnInsightMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0164fd453745c82f3d08cf167797c4ced78a485127756da95765b0451b6c54a0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__490ecc20807184aba85a45af27d5580cc61fe2ca5d60d9331d2b69a926167bfa(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d25c1bb3cc97dbdfbe4857bdd1468371289e691d9b8bc79d0e0b9335b8123bdf(
    *,
    aws_account_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    aws_account_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    company_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    compliance_associated_standards_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    compliance_security_control_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    compliance_security_control_parameters_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    compliance_security_control_parameters_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    compliance_status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    confidence: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.NumberFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    created_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    criticality: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.NumberFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    finding_provider_fields_confidence: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.NumberFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    finding_provider_fields_criticality: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.NumberFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    finding_provider_fields_related_findings_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    finding_provider_fields_related_findings_product_arn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    finding_provider_fields_severity_label: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    finding_provider_fields_severity_original: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    finding_provider_fields_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    first_observed_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    generator_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    keyword: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.KeywordFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    last_observed_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    malware_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    malware_path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    malware_state: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    malware_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    network_destination_domain: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    network_destination_ip_v4: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.IpFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    network_destination_ip_v6: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.IpFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    network_destination_port: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.NumberFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    network_direction: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    network_protocol: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    network_source_domain: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    network_source_ip_v4: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.IpFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    network_source_ip_v6: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.IpFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    network_source_mac: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    network_source_port: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.NumberFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    note_text: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    note_updated_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    note_updated_by: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    process_launched_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    process_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    process_parent_pid: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.NumberFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    process_path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    process_pid: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.NumberFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    process_terminated_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    product_arn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    product_fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.MapFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    product_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    recommendation_text: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    record_state: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    region: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    related_findings_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    related_findings_product_arn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_application_arn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_application_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_aws_ec2_instance_iam_instance_profile_arn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_aws_ec2_instance_image_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_aws_ec2_instance_ip_v4_addresses: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.IpFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_aws_ec2_instance_ip_v6_addresses: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.IpFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_aws_ec2_instance_key_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_aws_ec2_instance_launched_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_aws_ec2_instance_subnet_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_aws_ec2_instance_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_aws_ec2_instance_vpc_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_aws_iam_access_key_created_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_aws_iam_access_key_principal_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_aws_iam_access_key_status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_aws_iam_access_key_user_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_aws_iam_user_user_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_aws_s3_bucket_owner_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_aws_s3_bucket_owner_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_container_image_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_container_image_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_container_launched_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_container_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_details_other: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.MapFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_partition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_region: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.MapFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    sample: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.BooleanFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    severity_label: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    severity_normalized: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.NumberFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    severity_product: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.NumberFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    source_url: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    threat_intel_indicator_category: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    threat_intel_indicator_last_observed_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    threat_intel_indicator_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    threat_intel_indicator_source_url: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    threat_intel_indicator_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    threat_intel_indicator_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    title: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    updated_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    user_defined_fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.MapFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    verification_state: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    vulnerabilities_exploit_available: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    vulnerabilities_fix_available: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    workflow_state: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    workflow_status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c49ea2d5a63755edc5dd794add576e44bd643bf92b66f964157daae72e7123(
    *,
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19bb77c68a1f852ad493f61588887f20e2db14fe813cf0ea9ff8f086ffb5e6bc(
    *,
    date_range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInsightPropsMixin.DateRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    end: typing.Optional[builtins.str] = None,
    start: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2687c757cb4d175eb40a3c876ab0ba306df78e6a31cf66d39c805c1018130f2(
    *,
    unit: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9750eb0a5742c8cd326a739ebf18b9ad2d0e995c4fd5991cfdd495b74104455d(
    *,
    cidr: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d5ad9379640e4fcf89859bc3fb707bef3f1518f8ef0ad48a49405f9229d570(
    *,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e2eb46e1d2c10dd2f5a6d4880770bed89a565ebe4fc5f2352d69642086a96e(
    *,
    comparison: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0856142e23b6b526a54b356a6f64082e07b3c784cddd1e00355af23672521b(
    *,
    eq: typing.Optional[jsii.Number] = None,
    gte: typing.Optional[jsii.Number] = None,
    lte: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1fd8e4530fb7d39fc43c31d70d6ae6aca96fc7c7040ce03d9573f980df3060(
    *,
    comparison: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c974562a44abdb476bb056b25ad3bc789bb5bf282c468dc7c99046d94d4ae881(
    *,
    auto_enable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    auto_enable_standards: typing.Optional[builtins.str] = None,
    configuration_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7433f807f85aa09a7d57c9a84564e3e6e35014049d67fed3b44526c42ccd1cc(
    props: typing.Union[CfnOrganizationConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3493e8a7b5c252441c12503a99fe62c4c17fb2915893f363d5b701d6e421def9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d487bb52b5baf2aae15f7ba8ee353aee59f9bc4ed893a627e20988b301dc8b6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60283011007072cff8d76971a1f0a9c4980467e47aed3653d3f2da1c9001223a(
    *,
    configuration_policy_id: typing.Optional[builtins.str] = None,
    target_id: typing.Optional[builtins.str] = None,
    target_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f588f5dc98f10c00db814978221ef3198c78a8b0eaa4fa2c8231e006d60d588(
    props: typing.Union[CfnPolicyAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f3604df74643a6a96d4000fcc5e19e236f242f9fc0fc82894333e5fb3910be(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6acc6da90a875bc051b4506e6d23bdf63fa1b0ff0d0b358efb7d084bf099b4e9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b82f6495069be060f852c3442fdf853994fb2c1de629ceb77cad213b314868(
    *,
    product_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55a7cfbcd242974de53a0f75ace7dd5422480ded5811aa5376459b4a5ef32e3(
    props: typing.Union[CfnProductSubscriptionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbb63a1433a42001157d9add73b581bc39e564045109e90fa7affc96ed671297(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c75b506e9218897e52b2744453d2f4210a17e6b243d2575b067853c1b8a0e1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8ca3ccdf93f6b612234256891c7b870c005a867821e239fd180e0eafafa25d9(
    *,
    last_update_reason: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSecurityControlPropsMixin.ParameterConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    security_control_arn: typing.Optional[builtins.str] = None,
    security_control_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d416a40580e9db3d4805dc135f7be8f9d4f11cc1b65dd298cf421d9f41dc7bb7(
    props: typing.Union[CfnSecurityControlMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a22b099bb9de5b35190c53052d5efe78bfdb3023747729242b9ac4baa26d1ac8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__697d167bb206c16854b6a365c1d655b81e8bb07c3dc803ff19650c9270199f54(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d4219b5d6d1f2147c62256874d763cde06610c391797bd9a16a7a9c9a0fedb(
    *,
    value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSecurityControlPropsMixin.ParameterValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    value_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b94b0555188c55f578a87f690b333612a252473aa88b395731d9093e029b75cf(
    *,
    boolean: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    double: typing.Optional[jsii.Number] = None,
    enum: typing.Optional[builtins.str] = None,
    enum_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    integer: typing.Optional[jsii.Number] = None,
    integer_list: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
    string: typing.Optional[builtins.str] = None,
    string_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a0254c5a919836e1bffeaf0a4839fe228f5b054d90dbb54db84bfa8d8af9d8(
    *,
    disabled_standards_controls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStandardPropsMixin.StandardsControlProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    standards_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19f2e0fc9c261ad2f100ea510bf97117ef8e6b063726d3647579c1666c6cb86(
    props: typing.Union[CfnStandardMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d61b70ccf44e6f66a81f73f28a6bdb68f61a4842174d3b5a09688ba2d6f51261(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ef7b576bfe312b11211cb7d2d856211c728c496f55d89524a6bf23f2468366(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e73006c8103b249db8cd6b1351e5454c6270bb3e69e0bf07eb0b7505104f749(
    *,
    reason: typing.Optional[builtins.str] = None,
    standards_control_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
