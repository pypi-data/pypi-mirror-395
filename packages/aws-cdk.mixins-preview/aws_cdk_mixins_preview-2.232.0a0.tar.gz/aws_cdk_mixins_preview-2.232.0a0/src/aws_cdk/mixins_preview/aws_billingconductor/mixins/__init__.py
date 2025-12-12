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
    jsii_type="@aws-cdk/mixins-preview.aws_billingconductor.mixins.CfnBillingGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_grouping": "accountGrouping",
        "computation_preference": "computationPreference",
        "description": "description",
        "name": "name",
        "primary_account_id": "primaryAccountId",
        "tags": "tags",
    },
)
class CfnBillingGroupMixinProps:
    def __init__(
        self,
        *,
        account_grouping: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBillingGroupPropsMixin.AccountGroupingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        computation_preference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBillingGroupPropsMixin.ComputationPreferenceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        primary_account_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnBillingGroupPropsMixin.

        :param account_grouping: The set of accounts that will be under the billing group. The set of accounts resemble the linked accounts in a consolidated billing family.
        :param computation_preference: The preferences and settings that will be used to compute the AWS charges for a billing group.
        :param description: The description of the billing group.
        :param name: The billing group's name.
        :param primary_account_id: The account ID that serves as the main account in a billing group.
        :param tags: A map that contains tag keys and tag values that are attached to a billing group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-billinggroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_billingconductor import mixins as billingconductor_mixins
            
            cfn_billing_group_mixin_props = billingconductor_mixins.CfnBillingGroupMixinProps(
                account_grouping=billingconductor_mixins.CfnBillingGroupPropsMixin.AccountGroupingProperty(
                    auto_associate=False,
                    linked_account_ids=["linkedAccountIds"],
                    responsibility_transfer_arn="responsibilityTransferArn"
                ),
                computation_preference=billingconductor_mixins.CfnBillingGroupPropsMixin.ComputationPreferenceProperty(
                    pricing_plan_arn="pricingPlanArn"
                ),
                description="description",
                name="name",
                primary_account_id="primaryAccountId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf9afa4562058651a8b3461d24b269b67405a888623439d6c00d12ddfa1a1acb)
            check_type(argname="argument account_grouping", value=account_grouping, expected_type=type_hints["account_grouping"])
            check_type(argname="argument computation_preference", value=computation_preference, expected_type=type_hints["computation_preference"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument primary_account_id", value=primary_account_id, expected_type=type_hints["primary_account_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_grouping is not None:
            self._values["account_grouping"] = account_grouping
        if computation_preference is not None:
            self._values["computation_preference"] = computation_preference
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if primary_account_id is not None:
            self._values["primary_account_id"] = primary_account_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def account_grouping(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBillingGroupPropsMixin.AccountGroupingProperty"]]:
        '''The set of accounts that will be under the billing group.

        The set of accounts resemble the linked accounts in a consolidated billing family.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-billinggroup.html#cfn-billingconductor-billinggroup-accountgrouping
        '''
        result = self._values.get("account_grouping")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBillingGroupPropsMixin.AccountGroupingProperty"]], result)

    @builtins.property
    def computation_preference(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBillingGroupPropsMixin.ComputationPreferenceProperty"]]:
        '''The preferences and settings that will be used to compute the AWS charges for a billing group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-billinggroup.html#cfn-billingconductor-billinggroup-computationpreference
        '''
        result = self._values.get("computation_preference")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBillingGroupPropsMixin.ComputationPreferenceProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the billing group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-billinggroup.html#cfn-billingconductor-billinggroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The billing group's name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-billinggroup.html#cfn-billingconductor-billinggroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_account_id(self) -> typing.Optional[builtins.str]:
        '''The account ID that serves as the main account in a billing group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-billinggroup.html#cfn-billingconductor-billinggroup-primaryaccountid
        '''
        result = self._values.get("primary_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A map that contains tag keys and tag values that are attached to a billing group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-billinggroup.html#cfn-billingconductor-billinggroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBillingGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBillingGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_billingconductor.mixins.CfnBillingGroupPropsMixin",
):
    '''Creates a billing group that resembles a consolidated billing family that AWS charges, based off of the predefined pricing plan computation.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-billinggroup.html
    :cloudformationResource: AWS::BillingConductor::BillingGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_billingconductor import mixins as billingconductor_mixins
        
        cfn_billing_group_props_mixin = billingconductor_mixins.CfnBillingGroupPropsMixin(billingconductor_mixins.CfnBillingGroupMixinProps(
            account_grouping=billingconductor_mixins.CfnBillingGroupPropsMixin.AccountGroupingProperty(
                auto_associate=False,
                linked_account_ids=["linkedAccountIds"],
                responsibility_transfer_arn="responsibilityTransferArn"
            ),
            computation_preference=billingconductor_mixins.CfnBillingGroupPropsMixin.ComputationPreferenceProperty(
                pricing_plan_arn="pricingPlanArn"
            ),
            description="description",
            name="name",
            primary_account_id="primaryAccountId",
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
        props: typing.Union[CfnBillingGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::BillingConductor::BillingGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__172e34211c12a876290238b1649690e15a3fa1bd8f5fe0f2ed23f6004ff649b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c242e09276838a3bc6a3436523c25e78037526916848c36494ccfd89286afcc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__468d559794f423d9d170369f00e0a71a4f4aa2e7e599777e7b44c23a144cdeee)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBillingGroupMixinProps:
        return typing.cast(CfnBillingGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_billingconductor.mixins.CfnBillingGroupPropsMixin.AccountGroupingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_associate": "autoAssociate",
            "linked_account_ids": "linkedAccountIds",
            "responsibility_transfer_arn": "responsibilityTransferArn",
        },
    )
    class AccountGroupingProperty:
        def __init__(
            self,
            *,
            auto_associate: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            linked_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            responsibility_transfer_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The set of accounts that will be under the billing group.

            The set of accounts resemble the linked accounts in a consolidated billing family.

            :param auto_associate: Specifies if this billing group will automatically associate newly added AWS accounts that join your consolidated billing family.
            :param linked_account_ids: The account IDs that make up the billing group. Account IDs must be a part of the consolidated billing family, and not associated with another billing group.
            :param responsibility_transfer_arn: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-billinggroup-accountgrouping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_billingconductor import mixins as billingconductor_mixins
                
                account_grouping_property = billingconductor_mixins.CfnBillingGroupPropsMixin.AccountGroupingProperty(
                    auto_associate=False,
                    linked_account_ids=["linkedAccountIds"],
                    responsibility_transfer_arn="responsibilityTransferArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__76a7063d68925710bfb015acd77422cc93f3648e128fe44bc01f2f0b602d7d4b)
                check_type(argname="argument auto_associate", value=auto_associate, expected_type=type_hints["auto_associate"])
                check_type(argname="argument linked_account_ids", value=linked_account_ids, expected_type=type_hints["linked_account_ids"])
                check_type(argname="argument responsibility_transfer_arn", value=responsibility_transfer_arn, expected_type=type_hints["responsibility_transfer_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_associate is not None:
                self._values["auto_associate"] = auto_associate
            if linked_account_ids is not None:
                self._values["linked_account_ids"] = linked_account_ids
            if responsibility_transfer_arn is not None:
                self._values["responsibility_transfer_arn"] = responsibility_transfer_arn

        @builtins.property
        def auto_associate(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies if this billing group will automatically associate newly added AWS accounts that join your consolidated billing family.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-billinggroup-accountgrouping.html#cfn-billingconductor-billinggroup-accountgrouping-autoassociate
            '''
            result = self._values.get("auto_associate")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def linked_account_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The account IDs that make up the billing group.

            Account IDs must be a part of the consolidated billing family, and not associated with another billing group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-billinggroup-accountgrouping.html#cfn-billingconductor-billinggroup-accountgrouping-linkedaccountids
            '''
            result = self._values.get("linked_account_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def responsibility_transfer_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-billinggroup-accountgrouping.html#cfn-billingconductor-billinggroup-accountgrouping-responsibilitytransferarn
            '''
            result = self._values.get("responsibility_transfer_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccountGroupingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_billingconductor.mixins.CfnBillingGroupPropsMixin.ComputationPreferenceProperty",
        jsii_struct_bases=[],
        name_mapping={"pricing_plan_arn": "pricingPlanArn"},
    )
    class ComputationPreferenceProperty:
        def __init__(
            self,
            *,
            pricing_plan_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The preferences and settings that will be used to compute the AWS charges for a billing group.

            :param pricing_plan_arn: The Amazon Resource Name (ARN) of the pricing plan used to compute the AWS charges for a billing group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-billinggroup-computationpreference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_billingconductor import mixins as billingconductor_mixins
                
                computation_preference_property = billingconductor_mixins.CfnBillingGroupPropsMixin.ComputationPreferenceProperty(
                    pricing_plan_arn="pricingPlanArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0e7ae25e7a9b745450ad5333416d7d5722b76f2ae6e28122cd48cab2179a88b3)
                check_type(argname="argument pricing_plan_arn", value=pricing_plan_arn, expected_type=type_hints["pricing_plan_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if pricing_plan_arn is not None:
                self._values["pricing_plan_arn"] = pricing_plan_arn

        @builtins.property
        def pricing_plan_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the pricing plan used to compute the AWS charges for a billing group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-billinggroup-computationpreference.html#cfn-billingconductor-billinggroup-computationpreference-pricingplanarn
            '''
            result = self._values.get("pricing_plan_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComputationPreferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_billingconductor.mixins.CfnCustomLineItemMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "billing_group_arn": "billingGroupArn",
        "billing_period_range": "billingPeriodRange",
        "computation_rule": "computationRule",
        "custom_line_item_charge_details": "customLineItemChargeDetails",
        "description": "description",
        "name": "name",
        "presentation_details": "presentationDetails",
        "tags": "tags",
    },
)
class CfnCustomLineItemMixinProps:
    def __init__(
        self,
        *,
        account_id: typing.Optional[builtins.str] = None,
        billing_group_arn: typing.Optional[builtins.str] = None,
        billing_period_range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCustomLineItemPropsMixin.BillingPeriodRangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        computation_rule: typing.Optional[builtins.str] = None,
        custom_line_item_charge_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCustomLineItemPropsMixin.CustomLineItemChargeDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        presentation_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCustomLineItemPropsMixin.PresentationDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCustomLineItemPropsMixin.

        :param account_id: The AWS account in which this custom line item will be applied to.
        :param billing_group_arn: The Amazon Resource Name (ARN) that references the billing group where the custom line item applies to.
        :param billing_period_range: A time range for which the custom line item is effective.
        :param computation_rule: The display settings of the Custom Line Item.
        :param custom_line_item_charge_details: The charge details of a custom line item. It should contain only one of ``Flat`` or ``Percentage`` .
        :param description: The custom line item's description. This is shown on the Bills page in association with the charge value.
        :param name: The custom line item's name.
        :param presentation_details: 
        :param tags: A map that contains tag keys and tag values that are attached to a custom line item.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-customlineitem.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_billingconductor import mixins as billingconductor_mixins
            
            cfn_custom_line_item_mixin_props = billingconductor_mixins.CfnCustomLineItemMixinProps(
                account_id="accountId",
                billing_group_arn="billingGroupArn",
                billing_period_range=billingconductor_mixins.CfnCustomLineItemPropsMixin.BillingPeriodRangeProperty(
                    exclusive_end_billing_period="exclusiveEndBillingPeriod",
                    inclusive_start_billing_period="inclusiveStartBillingPeriod"
                ),
                computation_rule="computationRule",
                custom_line_item_charge_details=billingconductor_mixins.CfnCustomLineItemPropsMixin.CustomLineItemChargeDetailsProperty(
                    flat=billingconductor_mixins.CfnCustomLineItemPropsMixin.CustomLineItemFlatChargeDetailsProperty(
                        charge_value=123
                    ),
                    line_item_filters=[billingconductor_mixins.CfnCustomLineItemPropsMixin.LineItemFilterProperty(
                        attribute="attribute",
                        match_option="matchOption",
                        values=["values"]
                    )],
                    percentage=billingconductor_mixins.CfnCustomLineItemPropsMixin.CustomLineItemPercentageChargeDetailsProperty(
                        child_associated_resources=["childAssociatedResources"],
                        percentage_value=123
                    ),
                    type="type"
                ),
                description="description",
                name="name",
                presentation_details=billingconductor_mixins.CfnCustomLineItemPropsMixin.PresentationDetailsProperty(
                    service="service"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__514f9768a4281acd8e84749cc7856a328f09280e7c2338a37e8f273cfb4ce7d4)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument billing_group_arn", value=billing_group_arn, expected_type=type_hints["billing_group_arn"])
            check_type(argname="argument billing_period_range", value=billing_period_range, expected_type=type_hints["billing_period_range"])
            check_type(argname="argument computation_rule", value=computation_rule, expected_type=type_hints["computation_rule"])
            check_type(argname="argument custom_line_item_charge_details", value=custom_line_item_charge_details, expected_type=type_hints["custom_line_item_charge_details"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument presentation_details", value=presentation_details, expected_type=type_hints["presentation_details"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_id is not None:
            self._values["account_id"] = account_id
        if billing_group_arn is not None:
            self._values["billing_group_arn"] = billing_group_arn
        if billing_period_range is not None:
            self._values["billing_period_range"] = billing_period_range
        if computation_rule is not None:
            self._values["computation_rule"] = computation_rule
        if custom_line_item_charge_details is not None:
            self._values["custom_line_item_charge_details"] = custom_line_item_charge_details
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if presentation_details is not None:
            self._values["presentation_details"] = presentation_details
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''The AWS account in which this custom line item will be applied to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-customlineitem.html#cfn-billingconductor-customlineitem-accountid
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def billing_group_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) that references the billing group where the custom line item applies to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-customlineitem.html#cfn-billingconductor-customlineitem-billinggrouparn
        '''
        result = self._values.get("billing_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def billing_period_range(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomLineItemPropsMixin.BillingPeriodRangeProperty"]]:
        '''A time range for which the custom line item is effective.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-customlineitem.html#cfn-billingconductor-customlineitem-billingperiodrange
        '''
        result = self._values.get("billing_period_range")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomLineItemPropsMixin.BillingPeriodRangeProperty"]], result)

    @builtins.property
    def computation_rule(self) -> typing.Optional[builtins.str]:
        '''The display settings of the Custom Line Item.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-customlineitem.html#cfn-billingconductor-customlineitem-computationrule
        '''
        result = self._values.get("computation_rule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_line_item_charge_details(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomLineItemPropsMixin.CustomLineItemChargeDetailsProperty"]]:
        '''The charge details of a custom line item.

        It should contain only one of ``Flat`` or ``Percentage`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-customlineitem.html#cfn-billingconductor-customlineitem-customlineitemchargedetails
        '''
        result = self._values.get("custom_line_item_charge_details")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomLineItemPropsMixin.CustomLineItemChargeDetailsProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The custom line item's description.

        This is shown on the Bills page in association with the charge value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-customlineitem.html#cfn-billingconductor-customlineitem-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The custom line item's name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-customlineitem.html#cfn-billingconductor-customlineitem-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def presentation_details(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomLineItemPropsMixin.PresentationDetailsProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-customlineitem.html#cfn-billingconductor-customlineitem-presentationdetails
        '''
        result = self._values.get("presentation_details")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomLineItemPropsMixin.PresentationDetailsProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A map that contains tag keys and tag values that are attached to a custom line item.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-customlineitem.html#cfn-billingconductor-customlineitem-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCustomLineItemMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCustomLineItemPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_billingconductor.mixins.CfnCustomLineItemPropsMixin",
):
    '''Creates a custom line item that can be used to create a one-time or recurring, fixed or percentage-based charge that you can apply to a single billing group.

    You can apply custom line items to the current or previous billing period. You can create either a fee or a discount custom line item.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-customlineitem.html
    :cloudformationResource: AWS::BillingConductor::CustomLineItem
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_billingconductor import mixins as billingconductor_mixins
        
        cfn_custom_line_item_props_mixin = billingconductor_mixins.CfnCustomLineItemPropsMixin(billingconductor_mixins.CfnCustomLineItemMixinProps(
            account_id="accountId",
            billing_group_arn="billingGroupArn",
            billing_period_range=billingconductor_mixins.CfnCustomLineItemPropsMixin.BillingPeriodRangeProperty(
                exclusive_end_billing_period="exclusiveEndBillingPeriod",
                inclusive_start_billing_period="inclusiveStartBillingPeriod"
            ),
            computation_rule="computationRule",
            custom_line_item_charge_details=billingconductor_mixins.CfnCustomLineItemPropsMixin.CustomLineItemChargeDetailsProperty(
                flat=billingconductor_mixins.CfnCustomLineItemPropsMixin.CustomLineItemFlatChargeDetailsProperty(
                    charge_value=123
                ),
                line_item_filters=[billingconductor_mixins.CfnCustomLineItemPropsMixin.LineItemFilterProperty(
                    attribute="attribute",
                    match_option="matchOption",
                    values=["values"]
                )],
                percentage=billingconductor_mixins.CfnCustomLineItemPropsMixin.CustomLineItemPercentageChargeDetailsProperty(
                    child_associated_resources=["childAssociatedResources"],
                    percentage_value=123
                ),
                type="type"
            ),
            description="description",
            name="name",
            presentation_details=billingconductor_mixins.CfnCustomLineItemPropsMixin.PresentationDetailsProperty(
                service="service"
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
        props: typing.Union[CfnCustomLineItemMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::BillingConductor::CustomLineItem``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75bf967905d491f05405895bd283ac980d75efabd731ed17cf1b7095154fc7f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c0be391451b2cccbb394b3877d77bc2848d42d1f6ddc07791e2e26d0d60090e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c706d7b494c20c2e6024f924b0e99b7c2c37aa77ae6d79925c025327c81517aa)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCustomLineItemMixinProps:
        return typing.cast(CfnCustomLineItemMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_billingconductor.mixins.CfnCustomLineItemPropsMixin.BillingPeriodRangeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exclusive_end_billing_period": "exclusiveEndBillingPeriod",
            "inclusive_start_billing_period": "inclusiveStartBillingPeriod",
        },
    )
    class BillingPeriodRangeProperty:
        def __init__(
            self,
            *,
            exclusive_end_billing_period: typing.Optional[builtins.str] = None,
            inclusive_start_billing_period: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The billing period range in which the custom line item request will be applied.

            :param exclusive_end_billing_period: The exclusive end billing period that defines a billing period range where a custom line is applied.
            :param inclusive_start_billing_period: The inclusive start billing period that defines a billing period range where a custom line is applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-customlineitem-billingperiodrange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_billingconductor import mixins as billingconductor_mixins
                
                billing_period_range_property = billingconductor_mixins.CfnCustomLineItemPropsMixin.BillingPeriodRangeProperty(
                    exclusive_end_billing_period="exclusiveEndBillingPeriod",
                    inclusive_start_billing_period="inclusiveStartBillingPeriod"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d8e81efa63119862b67b33131c09004028608edb34aa63d0c9a9ced80c0fdbd2)
                check_type(argname="argument exclusive_end_billing_period", value=exclusive_end_billing_period, expected_type=type_hints["exclusive_end_billing_period"])
                check_type(argname="argument inclusive_start_billing_period", value=inclusive_start_billing_period, expected_type=type_hints["inclusive_start_billing_period"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclusive_end_billing_period is not None:
                self._values["exclusive_end_billing_period"] = exclusive_end_billing_period
            if inclusive_start_billing_period is not None:
                self._values["inclusive_start_billing_period"] = inclusive_start_billing_period

        @builtins.property
        def exclusive_end_billing_period(self) -> typing.Optional[builtins.str]:
            '''The exclusive end billing period that defines a billing period range where a custom line is applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-customlineitem-billingperiodrange.html#cfn-billingconductor-customlineitem-billingperiodrange-exclusiveendbillingperiod
            '''
            result = self._values.get("exclusive_end_billing_period")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inclusive_start_billing_period(self) -> typing.Optional[builtins.str]:
            '''The inclusive start billing period that defines a billing period range where a custom line is applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-customlineitem-billingperiodrange.html#cfn-billingconductor-customlineitem-billingperiodrange-inclusivestartbillingperiod
            '''
            result = self._values.get("inclusive_start_billing_period")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BillingPeriodRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_billingconductor.mixins.CfnCustomLineItemPropsMixin.CustomLineItemChargeDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "flat": "flat",
            "line_item_filters": "lineItemFilters",
            "percentage": "percentage",
            "type": "type",
        },
    )
    class CustomLineItemChargeDetailsProperty:
        def __init__(
            self,
            *,
            flat: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCustomLineItemPropsMixin.CustomLineItemFlatChargeDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            line_item_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCustomLineItemPropsMixin.LineItemFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            percentage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCustomLineItemPropsMixin.CustomLineItemPercentageChargeDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The charge details of a custom line item.

            It should contain only one of ``Flat`` or ``Percentage`` .

            :param flat: A ``CustomLineItemFlatChargeDetails`` that describes the charge details of a flat custom line item.
            :param line_item_filters: A representation of the line item filter.
            :param percentage: A ``CustomLineItemPercentageChargeDetails`` that describes the charge details of a percentage custom line item.
            :param type: The type of the custom line item that indicates whether the charge is a fee or credit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-customlineitem-customlineitemchargedetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_billingconductor import mixins as billingconductor_mixins
                
                custom_line_item_charge_details_property = billingconductor_mixins.CfnCustomLineItemPropsMixin.CustomLineItemChargeDetailsProperty(
                    flat=billingconductor_mixins.CfnCustomLineItemPropsMixin.CustomLineItemFlatChargeDetailsProperty(
                        charge_value=123
                    ),
                    line_item_filters=[billingconductor_mixins.CfnCustomLineItemPropsMixin.LineItemFilterProperty(
                        attribute="attribute",
                        match_option="matchOption",
                        values=["values"]
                    )],
                    percentage=billingconductor_mixins.CfnCustomLineItemPropsMixin.CustomLineItemPercentageChargeDetailsProperty(
                        child_associated_resources=["childAssociatedResources"],
                        percentage_value=123
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__375669a0867e9656222ecfee679c504e17e58c5b18bbef5b5ca9170a219585ac)
                check_type(argname="argument flat", value=flat, expected_type=type_hints["flat"])
                check_type(argname="argument line_item_filters", value=line_item_filters, expected_type=type_hints["line_item_filters"])
                check_type(argname="argument percentage", value=percentage, expected_type=type_hints["percentage"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if flat is not None:
                self._values["flat"] = flat
            if line_item_filters is not None:
                self._values["line_item_filters"] = line_item_filters
            if percentage is not None:
                self._values["percentage"] = percentage
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def flat(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomLineItemPropsMixin.CustomLineItemFlatChargeDetailsProperty"]]:
            '''A ``CustomLineItemFlatChargeDetails`` that describes the charge details of a flat custom line item.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-customlineitem-customlineitemchargedetails.html#cfn-billingconductor-customlineitem-customlineitemchargedetails-flat
            '''
            result = self._values.get("flat")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomLineItemPropsMixin.CustomLineItemFlatChargeDetailsProperty"]], result)

        @builtins.property
        def line_item_filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomLineItemPropsMixin.LineItemFilterProperty"]]]]:
            '''A representation of the line item filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-customlineitem-customlineitemchargedetails.html#cfn-billingconductor-customlineitem-customlineitemchargedetails-lineitemfilters
            '''
            result = self._values.get("line_item_filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomLineItemPropsMixin.LineItemFilterProperty"]]]], result)

        @builtins.property
        def percentage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomLineItemPropsMixin.CustomLineItemPercentageChargeDetailsProperty"]]:
            '''A ``CustomLineItemPercentageChargeDetails`` that describes the charge details of a percentage custom line item.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-customlineitem-customlineitemchargedetails.html#cfn-billingconductor-customlineitem-customlineitemchargedetails-percentage
            '''
            result = self._values.get("percentage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomLineItemPropsMixin.CustomLineItemPercentageChargeDetailsProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the custom line item that indicates whether the charge is a fee or credit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-customlineitem-customlineitemchargedetails.html#cfn-billingconductor-customlineitem-customlineitemchargedetails-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomLineItemChargeDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_billingconductor.mixins.CfnCustomLineItemPropsMixin.CustomLineItemFlatChargeDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"charge_value": "chargeValue"},
    )
    class CustomLineItemFlatChargeDetailsProperty:
        def __init__(
            self,
            *,
            charge_value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The charge details of a custom line item.

            It should contain only one of ``Flat`` or ``Percentage`` .

            :param charge_value: The custom line item's fixed charge value in USD.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-customlineitem-customlineitemflatchargedetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_billingconductor import mixins as billingconductor_mixins
                
                custom_line_item_flat_charge_details_property = billingconductor_mixins.CfnCustomLineItemPropsMixin.CustomLineItemFlatChargeDetailsProperty(
                    charge_value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1cf9bae97ccb30d93a9a968442cb1d19d1c27e511aeef183bf89c758d5340abf)
                check_type(argname="argument charge_value", value=charge_value, expected_type=type_hints["charge_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if charge_value is not None:
                self._values["charge_value"] = charge_value

        @builtins.property
        def charge_value(self) -> typing.Optional[jsii.Number]:
            '''The custom line item's fixed charge value in USD.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-customlineitem-customlineitemflatchargedetails.html#cfn-billingconductor-customlineitem-customlineitemflatchargedetails-chargevalue
            '''
            result = self._values.get("charge_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomLineItemFlatChargeDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_billingconductor.mixins.CfnCustomLineItemPropsMixin.CustomLineItemPercentageChargeDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "child_associated_resources": "childAssociatedResources",
            "percentage_value": "percentageValue",
        },
    )
    class CustomLineItemPercentageChargeDetailsProperty:
        def __init__(
            self,
            *,
            child_associated_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
            percentage_value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A representation of the charge details associated with a percentage custom line item.

            :param child_associated_resources: A list of resource ARNs to associate to the percentage custom line item.
            :param percentage_value: The custom line item's percentage value. This will be multiplied against the combined value of its associated resources to determine its charge value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-customlineitem-customlineitempercentagechargedetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_billingconductor import mixins as billingconductor_mixins
                
                custom_line_item_percentage_charge_details_property = billingconductor_mixins.CfnCustomLineItemPropsMixin.CustomLineItemPercentageChargeDetailsProperty(
                    child_associated_resources=["childAssociatedResources"],
                    percentage_value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3e4795f2af71f533887bbeb45b8b69270ddf462fb11a49561bd1d6954ee15f7b)
                check_type(argname="argument child_associated_resources", value=child_associated_resources, expected_type=type_hints["child_associated_resources"])
                check_type(argname="argument percentage_value", value=percentage_value, expected_type=type_hints["percentage_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if child_associated_resources is not None:
                self._values["child_associated_resources"] = child_associated_resources
            if percentage_value is not None:
                self._values["percentage_value"] = percentage_value

        @builtins.property
        def child_associated_resources(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of resource ARNs to associate to the percentage custom line item.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-customlineitem-customlineitempercentagechargedetails.html#cfn-billingconductor-customlineitem-customlineitempercentagechargedetails-childassociatedresources
            '''
            result = self._values.get("child_associated_resources")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def percentage_value(self) -> typing.Optional[jsii.Number]:
            '''The custom line item's percentage value.

            This will be multiplied against the combined value of its associated resources to determine its charge value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-customlineitem-customlineitempercentagechargedetails.html#cfn-billingconductor-customlineitem-customlineitempercentagechargedetails-percentagevalue
            '''
            result = self._values.get("percentage_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomLineItemPercentageChargeDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_billingconductor.mixins.CfnCustomLineItemPropsMixin.LineItemFilterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute": "attribute",
            "match_option": "matchOption",
            "values": "values",
        },
    )
    class LineItemFilterProperty:
        def __init__(
            self,
            *,
            attribute: typing.Optional[builtins.str] = None,
            match_option: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A representation of the line item filter for your custom line item.

            You can use line item filters to include or exclude specific resource values from the billing group's total cost. For example, if you create a custom line item and you want to filter out a value, such as Savings Plans discounts, you can update ``LineItemFilter`` to exclude it.

            :param attribute: The attribute of the line item filter. This specifies what attribute that you can filter on.
            :param match_option: The match criteria of the line item filter. This parameter specifies whether not to include the resource value from the billing group total cost.
            :param values: The values of the line item filter. This specifies the values to filter on. Currently, you can only exclude Savings Plans discounts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-customlineitem-lineitemfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_billingconductor import mixins as billingconductor_mixins
                
                line_item_filter_property = billingconductor_mixins.CfnCustomLineItemPropsMixin.LineItemFilterProperty(
                    attribute="attribute",
                    match_option="matchOption",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__063c198b878810c8ec1dd1110adec7f24dbef55554905a11ce803c43bacea06c)
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
                check_type(argname="argument match_option", value=match_option, expected_type=type_hints["match_option"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute is not None:
                self._values["attribute"] = attribute
            if match_option is not None:
                self._values["match_option"] = match_option
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def attribute(self) -> typing.Optional[builtins.str]:
            '''The attribute of the line item filter.

            This specifies what attribute that you can filter on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-customlineitem-lineitemfilter.html#cfn-billingconductor-customlineitem-lineitemfilter-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def match_option(self) -> typing.Optional[builtins.str]:
            '''The match criteria of the line item filter.

            This parameter specifies whether not to include the resource value from the billing group total cost.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-customlineitem-lineitemfilter.html#cfn-billingconductor-customlineitem-lineitemfilter-matchoption
            '''
            result = self._values.get("match_option")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The values of the line item filter.

            This specifies the values to filter on. Currently, you can only exclude Savings Plans discounts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-customlineitem-lineitemfilter.html#cfn-billingconductor-customlineitem-lineitemfilter-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LineItemFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_billingconductor.mixins.CfnCustomLineItemPropsMixin.PresentationDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"service": "service"},
    )
    class PresentationDetailsProperty:
        def __init__(self, *, service: typing.Optional[builtins.str] = None) -> None:
            '''
            :param service: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-customlineitem-presentationdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_billingconductor import mixins as billingconductor_mixins
                
                presentation_details_property = billingconductor_mixins.CfnCustomLineItemPropsMixin.PresentationDetailsProperty(
                    service="service"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__256c08cfaa76d30253124a7f66a8e69c550035574589bfcb533477bde4a7819e)
                check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if service is not None:
                self._values["service"] = service

        @builtins.property
        def service(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-customlineitem-presentationdetails.html#cfn-billingconductor-customlineitem-presentationdetails-service
            '''
            result = self._values.get("service")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PresentationDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_billingconductor.mixins.CfnPricingPlanMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "pricing_rule_arns": "pricingRuleArns",
        "tags": "tags",
    },
)
class CfnPricingPlanMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        pricing_rule_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPricingPlanPropsMixin.

        :param description: The pricing plan description.
        :param name: The name of a pricing plan.
        :param pricing_rule_arns: The ``PricingRuleArns`` that are associated with the Pricing Plan.
        :param tags: A map that contains tag keys and tag values that are attached to a pricing plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-pricingplan.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_billingconductor import mixins as billingconductor_mixins
            
            cfn_pricing_plan_mixin_props = billingconductor_mixins.CfnPricingPlanMixinProps(
                description="description",
                name="name",
                pricing_rule_arns=["pricingRuleArns"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e615756f158195f0c39a64098a945299476c211159d0ee91580a1a46b73a5266)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument pricing_rule_arns", value=pricing_rule_arns, expected_type=type_hints["pricing_rule_arns"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if pricing_rule_arns is not None:
            self._values["pricing_rule_arns"] = pricing_rule_arns
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The pricing plan description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-pricingplan.html#cfn-billingconductor-pricingplan-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of a pricing plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-pricingplan.html#cfn-billingconductor-pricingplan-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pricing_rule_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ``PricingRuleArns`` that are associated with the Pricing Plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-pricingplan.html#cfn-billingconductor-pricingplan-pricingrulearns
        '''
        result = self._values.get("pricing_rule_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A map that contains tag keys and tag values that are attached to a pricing plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-pricingplan.html#cfn-billingconductor-pricingplan-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPricingPlanMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPricingPlanPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_billingconductor.mixins.CfnPricingPlanPropsMixin",
):
    '''Creates a pricing plan that is used for computing AWS charges for billing groups.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-pricingplan.html
    :cloudformationResource: AWS::BillingConductor::PricingPlan
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_billingconductor import mixins as billingconductor_mixins
        
        cfn_pricing_plan_props_mixin = billingconductor_mixins.CfnPricingPlanPropsMixin(billingconductor_mixins.CfnPricingPlanMixinProps(
            description="description",
            name="name",
            pricing_rule_arns=["pricingRuleArns"],
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
        props: typing.Union[CfnPricingPlanMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::BillingConductor::PricingPlan``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e2a4dd312838cfd6869bf1d61eb379f43164e6b001696660ae31f3f514c8138)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7af7bd6c41096770e8c69a6cd8902340026a679c5cce7f60ff450d6b65cd99e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66bb5336ce7e5c13c1972f9312d29e5817a24e295f1ba8f7c3c2d97a473af3a9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPricingPlanMixinProps:
        return typing.cast(CfnPricingPlanMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_billingconductor.mixins.CfnPricingRuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "billing_entity": "billingEntity",
        "description": "description",
        "modifier_percentage": "modifierPercentage",
        "name": "name",
        "operation": "operation",
        "scope": "scope",
        "service": "service",
        "tags": "tags",
        "tiering": "tiering",
        "type": "type",
        "usage_type": "usageType",
    },
)
class CfnPricingRuleMixinProps:
    def __init__(
        self,
        *,
        billing_entity: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        modifier_percentage: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        operation: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        tiering: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPricingRulePropsMixin.TieringProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
        usage_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPricingRulePropsMixin.

        :param billing_entity: The seller of services provided by AWS , their affiliates, or third-party providers selling services via AWS Marketplace .
        :param description: The pricing rule description.
        :param modifier_percentage: A percentage modifier applied on the public pricing rates.
        :param name: The name of a pricing rule.
        :param operation: Operation is the specific AWS action covered by this line item. This describes the specific usage of the line item. If the ``Scope`` attribute is set to ``SKU`` , this attribute indicates which operation the ``PricingRule`` is modifying. For example, a value of ``RunInstances:0202`` indicates the operation of running an Amazon EC2 instance.
        :param scope: The scope of pricing rule that indicates if it's globally applicable or service-specific.
        :param service: If the ``Scope`` attribute is ``SERVICE`` , this attribute indicates which service the ``PricingRule`` is applicable for.
        :param tags: A map that contains tag keys and tag values that are attached to a pricing rule.
        :param tiering: The set of tiering configurations for the pricing rule.
        :param type: The type of pricing rule.
        :param usage_type: Usage Type is the unit that each service uses to measure the usage of a specific type of resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-pricingrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_billingconductor import mixins as billingconductor_mixins
            
            cfn_pricing_rule_mixin_props = billingconductor_mixins.CfnPricingRuleMixinProps(
                billing_entity="billingEntity",
                description="description",
                modifier_percentage=123,
                name="name",
                operation="operation",
                scope="scope",
                service="service",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                tiering=billingconductor_mixins.CfnPricingRulePropsMixin.TieringProperty(
                    free_tier=billingconductor_mixins.CfnPricingRulePropsMixin.FreeTierProperty(
                        activated=False
                    )
                ),
                type="type",
                usage_type="usageType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d1303e9d706ad70e5af730398c84be5d2ac791b1dddd1423a6d588b8a1d0300)
            check_type(argname="argument billing_entity", value=billing_entity, expected_type=type_hints["billing_entity"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument modifier_percentage", value=modifier_percentage, expected_type=type_hints["modifier_percentage"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tiering", value=tiering, expected_type=type_hints["tiering"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument usage_type", value=usage_type, expected_type=type_hints["usage_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if billing_entity is not None:
            self._values["billing_entity"] = billing_entity
        if description is not None:
            self._values["description"] = description
        if modifier_percentage is not None:
            self._values["modifier_percentage"] = modifier_percentage
        if name is not None:
            self._values["name"] = name
        if operation is not None:
            self._values["operation"] = operation
        if scope is not None:
            self._values["scope"] = scope
        if service is not None:
            self._values["service"] = service
        if tags is not None:
            self._values["tags"] = tags
        if tiering is not None:
            self._values["tiering"] = tiering
        if type is not None:
            self._values["type"] = type
        if usage_type is not None:
            self._values["usage_type"] = usage_type

    @builtins.property
    def billing_entity(self) -> typing.Optional[builtins.str]:
        '''The seller of services provided by AWS , their affiliates, or third-party providers selling services via AWS Marketplace .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-pricingrule.html#cfn-billingconductor-pricingrule-billingentity
        '''
        result = self._values.get("billing_entity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The pricing rule description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-pricingrule.html#cfn-billingconductor-pricingrule-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def modifier_percentage(self) -> typing.Optional[jsii.Number]:
        '''A percentage modifier applied on the public pricing rates.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-pricingrule.html#cfn-billingconductor-pricingrule-modifierpercentage
        '''
        result = self._values.get("modifier_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of a pricing rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-pricingrule.html#cfn-billingconductor-pricingrule-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operation(self) -> typing.Optional[builtins.str]:
        '''Operation is the specific AWS action covered by this line item.

        This describes the specific usage of the line item.

        If the ``Scope`` attribute is set to ``SKU`` , this attribute indicates which operation the ``PricingRule`` is modifying. For example, a value of ``RunInstances:0202`` indicates the operation of running an Amazon EC2 instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-pricingrule.html#cfn-billingconductor-pricingrule-operation
        '''
        result = self._values.get("operation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''The scope of pricing rule that indicates if it's globally applicable or service-specific.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-pricingrule.html#cfn-billingconductor-pricingrule-scope
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''If the ``Scope`` attribute is ``SERVICE`` , this attribute indicates which service the ``PricingRule`` is applicable for.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-pricingrule.html#cfn-billingconductor-pricingrule-service
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A map that contains tag keys and tag values that are attached to a pricing rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-pricingrule.html#cfn-billingconductor-pricingrule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def tiering(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPricingRulePropsMixin.TieringProperty"]]:
        '''The set of tiering configurations for the pricing rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-pricingrule.html#cfn-billingconductor-pricingrule-tiering
        '''
        result = self._values.get("tiering")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPricingRulePropsMixin.TieringProperty"]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of pricing rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-pricingrule.html#cfn-billingconductor-pricingrule-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def usage_type(self) -> typing.Optional[builtins.str]:
        '''Usage Type is the unit that each service uses to measure the usage of a specific type of resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-pricingrule.html#cfn-billingconductor-pricingrule-usagetype
        '''
        result = self._values.get("usage_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPricingRuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPricingRulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_billingconductor.mixins.CfnPricingRulePropsMixin",
):
    '''Creates a pricing rule which can be associated with a pricing plan, or a set of pricing plans.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-billingconductor-pricingrule.html
    :cloudformationResource: AWS::BillingConductor::PricingRule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_billingconductor import mixins as billingconductor_mixins
        
        cfn_pricing_rule_props_mixin = billingconductor_mixins.CfnPricingRulePropsMixin(billingconductor_mixins.CfnPricingRuleMixinProps(
            billing_entity="billingEntity",
            description="description",
            modifier_percentage=123,
            name="name",
            operation="operation",
            scope="scope",
            service="service",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            tiering=billingconductor_mixins.CfnPricingRulePropsMixin.TieringProperty(
                free_tier=billingconductor_mixins.CfnPricingRulePropsMixin.FreeTierProperty(
                    activated=False
                )
            ),
            type="type",
            usage_type="usageType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPricingRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::BillingConductor::PricingRule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__647b7566fce403798c3fbdd522bcb8d5a12a7f4411e6fd37dcff4acf7295a9f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e47ffa532b13dc6485598ab769b6859b8a67f8dbe08a531520e1de811bda62d8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__972a61c8d5ff767a445b9d49c7f2bb3b67548b4d6325f78ce131c4297c4bdb3f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPricingRuleMixinProps:
        return typing.cast(CfnPricingRuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_billingconductor.mixins.CfnPricingRulePropsMixin.FreeTierProperty",
        jsii_struct_bases=[],
        name_mapping={"activated": "activated"},
    )
    class FreeTierProperty:
        def __init__(
            self,
            *,
            activated: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The possible AWS Free Tier configurations.

            :param activated: Activate or deactivate AWS Free Tier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-pricingrule-freetier.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_billingconductor import mixins as billingconductor_mixins
                
                free_tier_property = billingconductor_mixins.CfnPricingRulePropsMixin.FreeTierProperty(
                    activated=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__029feb07e1baa732abc523968584546011acf5e7163ae9dd16b59dce404d5ced)
                check_type(argname="argument activated", value=activated, expected_type=type_hints["activated"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if activated is not None:
                self._values["activated"] = activated

        @builtins.property
        def activated(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Activate or deactivate AWS Free Tier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-pricingrule-freetier.html#cfn-billingconductor-pricingrule-freetier-activated
            '''
            result = self._values.get("activated")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FreeTierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_billingconductor.mixins.CfnPricingRulePropsMixin.TieringProperty",
        jsii_struct_bases=[],
        name_mapping={"free_tier": "freeTier"},
    )
    class TieringProperty:
        def __init__(
            self,
            *,
            free_tier: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPricingRulePropsMixin.FreeTierProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The set of tiering configurations for the pricing rule.

            :param free_tier: The possible AWS Free Tier configurations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-pricingrule-tiering.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_billingconductor import mixins as billingconductor_mixins
                
                tiering_property = billingconductor_mixins.CfnPricingRulePropsMixin.TieringProperty(
                    free_tier=billingconductor_mixins.CfnPricingRulePropsMixin.FreeTierProperty(
                        activated=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__45d316edfe34615fec141e82a4705f4c6203d0a258f907036110ec35ffc7caed)
                check_type(argname="argument free_tier", value=free_tier, expected_type=type_hints["free_tier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if free_tier is not None:
                self._values["free_tier"] = free_tier

        @builtins.property
        def free_tier(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPricingRulePropsMixin.FreeTierProperty"]]:
            '''The possible AWS Free Tier configurations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-billingconductor-pricingrule-tiering.html#cfn-billingconductor-pricingrule-tiering-freetier
            '''
            result = self._values.get("free_tier")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPricingRulePropsMixin.FreeTierProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TieringProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnBillingGroupMixinProps",
    "CfnBillingGroupPropsMixin",
    "CfnCustomLineItemMixinProps",
    "CfnCustomLineItemPropsMixin",
    "CfnPricingPlanMixinProps",
    "CfnPricingPlanPropsMixin",
    "CfnPricingRuleMixinProps",
    "CfnPricingRulePropsMixin",
]

publication.publish()

def _typecheckingstub__cf9afa4562058651a8b3461d24b269b67405a888623439d6c00d12ddfa1a1acb(
    *,
    account_grouping: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBillingGroupPropsMixin.AccountGroupingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    computation_preference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBillingGroupPropsMixin.ComputationPreferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    primary_account_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__172e34211c12a876290238b1649690e15a3fa1bd8f5fe0f2ed23f6004ff649b5(
    props: typing.Union[CfnBillingGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c242e09276838a3bc6a3436523c25e78037526916848c36494ccfd89286afcc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468d559794f423d9d170369f00e0a71a4f4aa2e7e599777e7b44c23a144cdeee(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a7063d68925710bfb015acd77422cc93f3648e128fe44bc01f2f0b602d7d4b(
    *,
    auto_associate: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    linked_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    responsibility_transfer_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e7ae25e7a9b745450ad5333416d7d5722b76f2ae6e28122cd48cab2179a88b3(
    *,
    pricing_plan_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514f9768a4281acd8e84749cc7856a328f09280e7c2338a37e8f273cfb4ce7d4(
    *,
    account_id: typing.Optional[builtins.str] = None,
    billing_group_arn: typing.Optional[builtins.str] = None,
    billing_period_range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCustomLineItemPropsMixin.BillingPeriodRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    computation_rule: typing.Optional[builtins.str] = None,
    custom_line_item_charge_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCustomLineItemPropsMixin.CustomLineItemChargeDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    presentation_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCustomLineItemPropsMixin.PresentationDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75bf967905d491f05405895bd283ac980d75efabd731ed17cf1b7095154fc7f2(
    props: typing.Union[CfnCustomLineItemMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c0be391451b2cccbb394b3877d77bc2848d42d1f6ddc07791e2e26d0d60090e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c706d7b494c20c2e6024f924b0e99b7c2c37aa77ae6d79925c025327c81517aa(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8e81efa63119862b67b33131c09004028608edb34aa63d0c9a9ced80c0fdbd2(
    *,
    exclusive_end_billing_period: typing.Optional[builtins.str] = None,
    inclusive_start_billing_period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375669a0867e9656222ecfee679c504e17e58c5b18bbef5b5ca9170a219585ac(
    *,
    flat: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCustomLineItemPropsMixin.CustomLineItemFlatChargeDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    line_item_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCustomLineItemPropsMixin.LineItemFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    percentage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCustomLineItemPropsMixin.CustomLineItemPercentageChargeDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf9bae97ccb30d93a9a968442cb1d19d1c27e511aeef183bf89c758d5340abf(
    *,
    charge_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e4795f2af71f533887bbeb45b8b69270ddf462fb11a49561bd1d6954ee15f7b(
    *,
    child_associated_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    percentage_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063c198b878810c8ec1dd1110adec7f24dbef55554905a11ce803c43bacea06c(
    *,
    attribute: typing.Optional[builtins.str] = None,
    match_option: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__256c08cfaa76d30253124a7f66a8e69c550035574589bfcb533477bde4a7819e(
    *,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e615756f158195f0c39a64098a945299476c211159d0ee91580a1a46b73a5266(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    pricing_rule_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2a4dd312838cfd6869bf1d61eb379f43164e6b001696660ae31f3f514c8138(
    props: typing.Union[CfnPricingPlanMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7af7bd6c41096770e8c69a6cd8902340026a679c5cce7f60ff450d6b65cd99e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66bb5336ce7e5c13c1972f9312d29e5817a24e295f1ba8f7c3c2d97a473af3a9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d1303e9d706ad70e5af730398c84be5d2ac791b1dddd1423a6d588b8a1d0300(
    *,
    billing_entity: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    modifier_percentage: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    operation: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    service: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tiering: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPricingRulePropsMixin.TieringProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
    usage_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__647b7566fce403798c3fbdd522bcb8d5a12a7f4411e6fd37dcff4acf7295a9f6(
    props: typing.Union[CfnPricingRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47ffa532b13dc6485598ab769b6859b8a67f8dbe08a531520e1de811bda62d8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__972a61c8d5ff767a445b9d49c7f2bb3b67548b4d6325f78ce131c4297c4bdb3f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029feb07e1baa732abc523968584546011acf5e7163ae9dd16b59dce404d5ced(
    *,
    activated: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45d316edfe34615fec141e82a4705f4c6203d0a258f907036110ec35ffc7caed(
    *,
    free_tier: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPricingRulePropsMixin.FreeTierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
