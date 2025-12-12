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
    jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "budget": "budget",
        "notifications_with_subscribers": "notificationsWithSubscribers",
        "resource_tags": "resourceTags",
    },
)
class CfnBudgetMixinProps:
    def __init__(
        self,
        *,
        budget: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetPropsMixin.BudgetDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        notifications_with_subscribers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetPropsMixin.NotificationWithSubscribersProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        resource_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetPropsMixin.ResourceTagProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnBudgetPropsMixin.

        :param budget: The budget object that you want to create.
        :param notifications_with_subscribers: A notification that you want to associate with a budget. A budget can have up to five notifications, and each notification can have one SNS subscriber and up to 10 email subscribers. If you include notifications and subscribers in your ``CreateBudget`` call, AWS creates the notifications and subscribers for you.
        :param resource_tags: An optional list of tags to associate with the specified budget. Each tag consists of a key and a value, and each key must be unique for the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budget.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
            
            # cost_filters: Any
            # expression_property_: budgets_mixins.CfnBudgetPropsMixin.ExpressionProperty
            # planned_budget_limits: Any
            
            cfn_budget_mixin_props = budgets_mixins.CfnBudgetMixinProps(
                budget=budgets_mixins.CfnBudgetPropsMixin.BudgetDataProperty(
                    auto_adjust_data=budgets_mixins.CfnBudgetPropsMixin.AutoAdjustDataProperty(
                        auto_adjust_type="autoAdjustType",
                        historical_options=budgets_mixins.CfnBudgetPropsMixin.HistoricalOptionsProperty(
                            budget_adjustment_period=123
                        )
                    ),
                    billing_view_arn="billingViewArn",
                    budget_limit=budgets_mixins.CfnBudgetPropsMixin.SpendProperty(
                        amount=123,
                        unit="unit"
                    ),
                    budget_name="budgetName",
                    budget_type="budgetType",
                    cost_filters=cost_filters,
                    cost_types=budgets_mixins.CfnBudgetPropsMixin.CostTypesProperty(
                        include_credit=False,
                        include_discount=False,
                        include_other_subscription=False,
                        include_recurring=False,
                        include_refund=False,
                        include_subscription=False,
                        include_support=False,
                        include_tax=False,
                        include_upfront=False,
                        use_amortized=False,
                        use_blended=False
                    ),
                    filter_expression=budgets_mixins.CfnBudgetPropsMixin.ExpressionProperty(
                        and=[expression_property_],
                        cost_categories=budgets_mixins.CfnBudgetPropsMixin.CostCategoryValuesProperty(
                            key="key",
                            match_options=["matchOptions"],
                            values=["values"]
                        ),
                        dimensions=budgets_mixins.CfnBudgetPropsMixin.ExpressionDimensionValuesProperty(
                            key="key",
                            match_options=["matchOptions"],
                            values=["values"]
                        ),
                        not=expression_property_,
                        or=[expression_property_],
                        tags=budgets_mixins.CfnBudgetPropsMixin.TagValuesProperty(
                            key="key",
                            match_options=["matchOptions"],
                            values=["values"]
                        )
                    ),
                    metrics=["metrics"],
                    planned_budget_limits=planned_budget_limits,
                    time_period=budgets_mixins.CfnBudgetPropsMixin.TimePeriodProperty(
                        end="end",
                        start="start"
                    ),
                    time_unit="timeUnit"
                ),
                notifications_with_subscribers=[budgets_mixins.CfnBudgetPropsMixin.NotificationWithSubscribersProperty(
                    notification=budgets_mixins.CfnBudgetPropsMixin.NotificationProperty(
                        comparison_operator="comparisonOperator",
                        notification_type="notificationType",
                        threshold=123,
                        threshold_type="thresholdType"
                    ),
                    subscribers=[budgets_mixins.CfnBudgetPropsMixin.SubscriberProperty(
                        address="address",
                        subscription_type="subscriptionType"
                    )]
                )],
                resource_tags=[budgets_mixins.CfnBudgetPropsMixin.ResourceTagProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a670285d7a75dfd9e8a053ae8b8952f00601c21cf19624807962ec497be22ff)
            check_type(argname="argument budget", value=budget, expected_type=type_hints["budget"])
            check_type(argname="argument notifications_with_subscribers", value=notifications_with_subscribers, expected_type=type_hints["notifications_with_subscribers"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if budget is not None:
            self._values["budget"] = budget
        if notifications_with_subscribers is not None:
            self._values["notifications_with_subscribers"] = notifications_with_subscribers
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags

    @builtins.property
    def budget(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.BudgetDataProperty"]]:
        '''The budget object that you want to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budget.html#cfn-budgets-budget-budget
        '''
        result = self._values.get("budget")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.BudgetDataProperty"]], result)

    @builtins.property
    def notifications_with_subscribers(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.NotificationWithSubscribersProperty"]]]]:
        '''A notification that you want to associate with a budget.

        A budget can have up to five notifications, and each notification can have one SNS subscriber and up to 10 email subscribers. If you include notifications and subscribers in your ``CreateBudget`` call, AWS creates the notifications and subscribers for you.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budget.html#cfn-budgets-budget-notificationswithsubscribers
        '''
        result = self._values.get("notifications_with_subscribers")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.NotificationWithSubscribersProperty"]]]], result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.ResourceTagProperty"]]]]:
        '''An optional list of tags to associate with the specified budget.

        Each tag consists of a key and a value, and each key must be unique for the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budget.html#cfn-budgets-budget-resourcetags
        '''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.ResourceTagProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBudgetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBudgetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetPropsMixin",
):
    '''The ``AWS::Budgets::Budget`` resource allows customers to take pre-defined actions that will trigger once a budget threshold has been exceeded.

    creates, replaces, or deletes budgets for Billing and Cost Management. For more information, see `Managing Your Costs with Budgets <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/budgets-managing-costs.html>`_ in the *Billing and Cost Management User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budget.html
    :cloudformationResource: AWS::Budgets::Budget
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
        
        # cost_filters: Any
        # expression_property_: budgets_mixins.CfnBudgetPropsMixin.ExpressionProperty
        # planned_budget_limits: Any
        
        cfn_budget_props_mixin = budgets_mixins.CfnBudgetPropsMixin(budgets_mixins.CfnBudgetMixinProps(
            budget=budgets_mixins.CfnBudgetPropsMixin.BudgetDataProperty(
                auto_adjust_data=budgets_mixins.CfnBudgetPropsMixin.AutoAdjustDataProperty(
                    auto_adjust_type="autoAdjustType",
                    historical_options=budgets_mixins.CfnBudgetPropsMixin.HistoricalOptionsProperty(
                        budget_adjustment_period=123
                    )
                ),
                billing_view_arn="billingViewArn",
                budget_limit=budgets_mixins.CfnBudgetPropsMixin.SpendProperty(
                    amount=123,
                    unit="unit"
                ),
                budget_name="budgetName",
                budget_type="budgetType",
                cost_filters=cost_filters,
                cost_types=budgets_mixins.CfnBudgetPropsMixin.CostTypesProperty(
                    include_credit=False,
                    include_discount=False,
                    include_other_subscription=False,
                    include_recurring=False,
                    include_refund=False,
                    include_subscription=False,
                    include_support=False,
                    include_tax=False,
                    include_upfront=False,
                    use_amortized=False,
                    use_blended=False
                ),
                filter_expression=budgets_mixins.CfnBudgetPropsMixin.ExpressionProperty(
                    and=[expression_property_],
                    cost_categories=budgets_mixins.CfnBudgetPropsMixin.CostCategoryValuesProperty(
                        key="key",
                        match_options=["matchOptions"],
                        values=["values"]
                    ),
                    dimensions=budgets_mixins.CfnBudgetPropsMixin.ExpressionDimensionValuesProperty(
                        key="key",
                        match_options=["matchOptions"],
                        values=["values"]
                    ),
                    not=expression_property_,
                    or=[expression_property_],
                    tags=budgets_mixins.CfnBudgetPropsMixin.TagValuesProperty(
                        key="key",
                        match_options=["matchOptions"],
                        values=["values"]
                    )
                ),
                metrics=["metrics"],
                planned_budget_limits=planned_budget_limits,
                time_period=budgets_mixins.CfnBudgetPropsMixin.TimePeriodProperty(
                    end="end",
                    start="start"
                ),
                time_unit="timeUnit"
            ),
            notifications_with_subscribers=[budgets_mixins.CfnBudgetPropsMixin.NotificationWithSubscribersProperty(
                notification=budgets_mixins.CfnBudgetPropsMixin.NotificationProperty(
                    comparison_operator="comparisonOperator",
                    notification_type="notificationType",
                    threshold=123,
                    threshold_type="thresholdType"
                ),
                subscribers=[budgets_mixins.CfnBudgetPropsMixin.SubscriberProperty(
                    address="address",
                    subscription_type="subscriptionType"
                )]
            )],
            resource_tags=[budgets_mixins.CfnBudgetPropsMixin.ResourceTagProperty(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnBudgetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Budgets::Budget``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b8e854c14fdefff6bcffac29e2897448fcdeac96af7fba191ceb9b7966def12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b75cdcb2badf38f563ac1e13478c899547efe58eb1ca63f7c6478fab32cfcad)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__debccf0b401c580cd1db020994e343f2d6a62e42e9b964389157c789d7486ba3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBudgetMixinProps:
        return typing.cast(CfnBudgetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetPropsMixin.AutoAdjustDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_adjust_type": "autoAdjustType",
            "historical_options": "historicalOptions",
        },
    )
    class AutoAdjustDataProperty:
        def __init__(
            self,
            *,
            auto_adjust_type: typing.Optional[builtins.str] = None,
            historical_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetPropsMixin.HistoricalOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Determine the budget amount for an auto-adjusting budget.

            :param auto_adjust_type: The string that defines whether your budget auto-adjusts based on historical or forecasted data.
            :param historical_options: The parameters that define or describe the historical data that your auto-adjusting budget is based on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-autoadjustdata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                auto_adjust_data_property = budgets_mixins.CfnBudgetPropsMixin.AutoAdjustDataProperty(
                    auto_adjust_type="autoAdjustType",
                    historical_options=budgets_mixins.CfnBudgetPropsMixin.HistoricalOptionsProperty(
                        budget_adjustment_period=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__70962bf28ad60232de8e1843e1e037d70bedece14b01412f9e4a560a59303f9d)
                check_type(argname="argument auto_adjust_type", value=auto_adjust_type, expected_type=type_hints["auto_adjust_type"])
                check_type(argname="argument historical_options", value=historical_options, expected_type=type_hints["historical_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_adjust_type is not None:
                self._values["auto_adjust_type"] = auto_adjust_type
            if historical_options is not None:
                self._values["historical_options"] = historical_options

        @builtins.property
        def auto_adjust_type(self) -> typing.Optional[builtins.str]:
            '''The string that defines whether your budget auto-adjusts based on historical or forecasted data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-autoadjustdata.html#cfn-budgets-budget-autoadjustdata-autoadjusttype
            '''
            result = self._values.get("auto_adjust_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def historical_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.HistoricalOptionsProperty"]]:
            '''The parameters that define or describe the historical data that your auto-adjusting budget is based on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-autoadjustdata.html#cfn-budgets-budget-autoadjustdata-historicaloptions
            '''
            result = self._values.get("historical_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.HistoricalOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoAdjustDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetPropsMixin.BudgetDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_adjust_data": "autoAdjustData",
            "billing_view_arn": "billingViewArn",
            "budget_limit": "budgetLimit",
            "budget_name": "budgetName",
            "budget_type": "budgetType",
            "cost_filters": "costFilters",
            "cost_types": "costTypes",
            "filter_expression": "filterExpression",
            "metrics": "metrics",
            "planned_budget_limits": "plannedBudgetLimits",
            "time_period": "timePeriod",
            "time_unit": "timeUnit",
        },
    )
    class BudgetDataProperty:
        def __init__(
            self,
            *,
            auto_adjust_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetPropsMixin.AutoAdjustDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            billing_view_arn: typing.Optional[builtins.str] = None,
            budget_limit: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetPropsMixin.SpendProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            budget_name: typing.Optional[builtins.str] = None,
            budget_type: typing.Optional[builtins.str] = None,
            cost_filters: typing.Any = None,
            cost_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetPropsMixin.CostTypesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            filter_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetPropsMixin.ExpressionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            metrics: typing.Optional[typing.Sequence[builtins.str]] = None,
            planned_budget_limits: typing.Any = None,
            time_period: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetPropsMixin.TimePeriodProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            time_unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents the output of the ``CreateBudget`` operation.

            The content consists of the detailed metadata and data file information, and the current status of the ``budget`` object.

            This is the Amazon Resource Name (ARN) pattern for a budget:

            ``arn:aws:budgets::AccountId:budget/budgetName``

            :param auto_adjust_data: Determine the budget amount for an auto-adjusting budget.
            :param billing_view_arn: 
            :param budget_limit: The total amount of cost, usage, RI utilization, RI coverage, Savings Plans utilization, or Savings Plans coverage that you want to track with your budget. ``BudgetLimit`` is required for cost or usage budgets, but optional for RI or Savings Plans utilization or coverage budgets. RI and Savings Plans utilization or coverage budgets default to ``100`` . This is the only valid value for RI or Savings Plans utilization or coverage budgets. You can't use ``BudgetLimit`` with ``PlannedBudgetLimits`` for ``CreateBudget`` and ``UpdateBudget`` actions.
            :param budget_name: The name of a budget. The value must be unique within an account. ``BudgetName`` can't include ``:`` and ``\\`` characters. If you don't include value for ``BudgetName`` in the template, Billing and Cost Management assigns your budget a randomly generated name.
            :param budget_type: Specifies whether this budget tracks costs, usage, RI utilization, RI coverage, Savings Plans utilization, or Savings Plans coverage.
            :param cost_filters: The cost filters, such as ``Region`` , ``Service`` , ``LinkedAccount`` , ``Tag`` , or ``CostCategory`` , that are applied to a budget. AWS Budgets supports the following services as a ``Service`` filter for RI budgets: - Amazon EC2 - Amazon Redshift - Amazon Relational Database Service - Amazon ElastiCache - Amazon OpenSearch Service
            :param cost_types: The types of costs that are included in this ``COST`` budget. ``USAGE`` , ``RI_UTILIZATION`` , ``RI_COVERAGE`` , ``SAVINGS_PLANS_UTILIZATION`` , and ``SAVINGS_PLANS_COVERAGE`` budgets do not have ``CostTypes`` .
            :param filter_expression: 
            :param metrics: 
            :param planned_budget_limits: A map containing multiple ``BudgetLimit`` , including current or future limits. ``PlannedBudgetLimits`` is available for cost or usage budget and supports both monthly and quarterly ``TimeUnit`` . For monthly budgets, provide 12 months of ``PlannedBudgetLimits`` values. This must start from the current month and include the next 11 months. The ``key`` is the start of the month, ``UTC`` in epoch seconds. For quarterly budgets, provide four quarters of ``PlannedBudgetLimits`` value entries in standard calendar quarter increments. This must start from the current quarter and include the next three quarters. The ``key`` is the start of the quarter, ``UTC`` in epoch seconds. If the planned budget expires before 12 months for monthly or four quarters for quarterly, provide the ``PlannedBudgetLimits`` values only for the remaining periods. If the budget begins at a date in the future, provide ``PlannedBudgetLimits`` values from the start date of the budget. After all of the ``BudgetLimit`` values in ``PlannedBudgetLimits`` are used, the budget continues to use the last limit as the ``BudgetLimit`` . At that point, the planned budget provides the same experience as a fixed budget. ``DescribeBudget`` and ``DescribeBudgets`` response along with ``PlannedBudgetLimits`` also contain ``BudgetLimit`` representing the current month or quarter limit present in ``PlannedBudgetLimits`` . This only applies to budgets that are created with ``PlannedBudgetLimits`` . Budgets that are created without ``PlannedBudgetLimits`` only contain ``BudgetLimit`` . They don't contain ``PlannedBudgetLimits`` .
            :param time_period: The period of time that is covered by a budget. The period has a start date and an end date. The start date must come before the end date. There are no restrictions on the end date. The start date for a budget. If you created your budget and didn't specify a start date, the start date defaults to the start of the chosen time period (MONTHLY, QUARTERLY, or ANNUALLY). For example, if you create your budget on January 24, 2019, choose ``MONTHLY`` , and don't set a start date, the start date defaults to ``01/01/19 00:00 UTC`` . The defaults are the same for the Billing and Cost Management console and the API. You can change your start date with the ``UpdateBudget`` operation. After the end date, AWS deletes the budget and all associated notifications and subscribers.
            :param time_unit: The length of time until a budget resets the actual and forecasted spend. ``DAILY`` is available only for ``RI_UTILIZATION`` and ``RI_COVERAGE`` budgets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                # cost_filters: Any
                # expression_property_: budgets_mixins.CfnBudgetPropsMixin.ExpressionProperty
                # planned_budget_limits: Any
                
                budget_data_property = budgets_mixins.CfnBudgetPropsMixin.BudgetDataProperty(
                    auto_adjust_data=budgets_mixins.CfnBudgetPropsMixin.AutoAdjustDataProperty(
                        auto_adjust_type="autoAdjustType",
                        historical_options=budgets_mixins.CfnBudgetPropsMixin.HistoricalOptionsProperty(
                            budget_adjustment_period=123
                        )
                    ),
                    billing_view_arn="billingViewArn",
                    budget_limit=budgets_mixins.CfnBudgetPropsMixin.SpendProperty(
                        amount=123,
                        unit="unit"
                    ),
                    budget_name="budgetName",
                    budget_type="budgetType",
                    cost_filters=cost_filters,
                    cost_types=budgets_mixins.CfnBudgetPropsMixin.CostTypesProperty(
                        include_credit=False,
                        include_discount=False,
                        include_other_subscription=False,
                        include_recurring=False,
                        include_refund=False,
                        include_subscription=False,
                        include_support=False,
                        include_tax=False,
                        include_upfront=False,
                        use_amortized=False,
                        use_blended=False
                    ),
                    filter_expression=budgets_mixins.CfnBudgetPropsMixin.ExpressionProperty(
                        and=[expression_property_],
                        cost_categories=budgets_mixins.CfnBudgetPropsMixin.CostCategoryValuesProperty(
                            key="key",
                            match_options=["matchOptions"],
                            values=["values"]
                        ),
                        dimensions=budgets_mixins.CfnBudgetPropsMixin.ExpressionDimensionValuesProperty(
                            key="key",
                            match_options=["matchOptions"],
                            values=["values"]
                        ),
                        not=expression_property_,
                        or=[expression_property_],
                        tags=budgets_mixins.CfnBudgetPropsMixin.TagValuesProperty(
                            key="key",
                            match_options=["matchOptions"],
                            values=["values"]
                        )
                    ),
                    metrics=["metrics"],
                    planned_budget_limits=planned_budget_limits,
                    time_period=budgets_mixins.CfnBudgetPropsMixin.TimePeriodProperty(
                        end="end",
                        start="start"
                    ),
                    time_unit="timeUnit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5db31e71da825d1a062880048db3e9576512bfb75e5234891c324f2fd3399583)
                check_type(argname="argument auto_adjust_data", value=auto_adjust_data, expected_type=type_hints["auto_adjust_data"])
                check_type(argname="argument billing_view_arn", value=billing_view_arn, expected_type=type_hints["billing_view_arn"])
                check_type(argname="argument budget_limit", value=budget_limit, expected_type=type_hints["budget_limit"])
                check_type(argname="argument budget_name", value=budget_name, expected_type=type_hints["budget_name"])
                check_type(argname="argument budget_type", value=budget_type, expected_type=type_hints["budget_type"])
                check_type(argname="argument cost_filters", value=cost_filters, expected_type=type_hints["cost_filters"])
                check_type(argname="argument cost_types", value=cost_types, expected_type=type_hints["cost_types"])
                check_type(argname="argument filter_expression", value=filter_expression, expected_type=type_hints["filter_expression"])
                check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
                check_type(argname="argument planned_budget_limits", value=planned_budget_limits, expected_type=type_hints["planned_budget_limits"])
                check_type(argname="argument time_period", value=time_period, expected_type=type_hints["time_period"])
                check_type(argname="argument time_unit", value=time_unit, expected_type=type_hints["time_unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_adjust_data is not None:
                self._values["auto_adjust_data"] = auto_adjust_data
            if billing_view_arn is not None:
                self._values["billing_view_arn"] = billing_view_arn
            if budget_limit is not None:
                self._values["budget_limit"] = budget_limit
            if budget_name is not None:
                self._values["budget_name"] = budget_name
            if budget_type is not None:
                self._values["budget_type"] = budget_type
            if cost_filters is not None:
                self._values["cost_filters"] = cost_filters
            if cost_types is not None:
                self._values["cost_types"] = cost_types
            if filter_expression is not None:
                self._values["filter_expression"] = filter_expression
            if metrics is not None:
                self._values["metrics"] = metrics
            if planned_budget_limits is not None:
                self._values["planned_budget_limits"] = planned_budget_limits
            if time_period is not None:
                self._values["time_period"] = time_period
            if time_unit is not None:
                self._values["time_unit"] = time_unit

        @builtins.property
        def auto_adjust_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.AutoAdjustDataProperty"]]:
            '''Determine the budget amount for an auto-adjusting budget.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html#cfn-budgets-budget-budgetdata-autoadjustdata
            '''
            result = self._values.get("auto_adjust_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.AutoAdjustDataProperty"]], result)

        @builtins.property
        def billing_view_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html#cfn-budgets-budget-budgetdata-billingviewarn
            '''
            result = self._values.get("billing_view_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def budget_limit(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.SpendProperty"]]:
            '''The total amount of cost, usage, RI utilization, RI coverage, Savings Plans utilization, or Savings Plans coverage that you want to track with your budget.

            ``BudgetLimit`` is required for cost or usage budgets, but optional for RI or Savings Plans utilization or coverage budgets. RI and Savings Plans utilization or coverage budgets default to ``100`` . This is the only valid value for RI or Savings Plans utilization or coverage budgets. You can't use ``BudgetLimit`` with ``PlannedBudgetLimits`` for ``CreateBudget`` and ``UpdateBudget`` actions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html#cfn-budgets-budget-budgetdata-budgetlimit
            '''
            result = self._values.get("budget_limit")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.SpendProperty"]], result)

        @builtins.property
        def budget_name(self) -> typing.Optional[builtins.str]:
            '''The name of a budget.

            The value must be unique within an account. ``BudgetName`` can't include ``:`` and ``\\`` characters. If you don't include value for ``BudgetName`` in the template, Billing and Cost Management assigns your budget a randomly generated name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html#cfn-budgets-budget-budgetdata-budgetname
            '''
            result = self._values.get("budget_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def budget_type(self) -> typing.Optional[builtins.str]:
            '''Specifies whether this budget tracks costs, usage, RI utilization, RI coverage, Savings Plans utilization, or Savings Plans coverage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html#cfn-budgets-budget-budgetdata-budgettype
            '''
            result = self._values.get("budget_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cost_filters(self) -> typing.Any:
            '''The cost filters, such as ``Region`` , ``Service`` , ``LinkedAccount`` , ``Tag`` , or ``CostCategory`` , that are applied to a budget.

            AWS Budgets supports the following services as a ``Service`` filter for RI budgets:

            - Amazon EC2
            - Amazon Redshift
            - Amazon Relational Database Service
            - Amazon ElastiCache
            - Amazon OpenSearch Service

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html#cfn-budgets-budget-budgetdata-costfilters
            '''
            result = self._values.get("cost_filters")
            return typing.cast(typing.Any, result)

        @builtins.property
        def cost_types(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.CostTypesProperty"]]:
            '''The types of costs that are included in this ``COST`` budget.

            ``USAGE`` , ``RI_UTILIZATION`` , ``RI_COVERAGE`` , ``SAVINGS_PLANS_UTILIZATION`` , and ``SAVINGS_PLANS_COVERAGE`` budgets do not have ``CostTypes`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html#cfn-budgets-budget-budgetdata-costtypes
            '''
            result = self._values.get("cost_types")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.CostTypesProperty"]], result)

        @builtins.property
        def filter_expression(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.ExpressionProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html#cfn-budgets-budget-budgetdata-filterexpression
            '''
            result = self._values.get("filter_expression")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.ExpressionProperty"]], result)

        @builtins.property
        def metrics(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html#cfn-budgets-budget-budgetdata-metrics
            '''
            result = self._values.get("metrics")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def planned_budget_limits(self) -> typing.Any:
            '''A map containing multiple ``BudgetLimit`` , including current or future limits.

            ``PlannedBudgetLimits`` is available for cost or usage budget and supports both monthly and quarterly ``TimeUnit`` .

            For monthly budgets, provide 12 months of ``PlannedBudgetLimits`` values. This must start from the current month and include the next 11 months. The ``key`` is the start of the month, ``UTC`` in epoch seconds.

            For quarterly budgets, provide four quarters of ``PlannedBudgetLimits`` value entries in standard calendar quarter increments. This must start from the current quarter and include the next three quarters. The ``key`` is the start of the quarter, ``UTC`` in epoch seconds.

            If the planned budget expires before 12 months for monthly or four quarters for quarterly, provide the ``PlannedBudgetLimits`` values only for the remaining periods.

            If the budget begins at a date in the future, provide ``PlannedBudgetLimits`` values from the start date of the budget.

            After all of the ``BudgetLimit`` values in ``PlannedBudgetLimits`` are used, the budget continues to use the last limit as the ``BudgetLimit`` . At that point, the planned budget provides the same experience as a fixed budget.

            ``DescribeBudget`` and ``DescribeBudgets`` response along with ``PlannedBudgetLimits`` also contain ``BudgetLimit`` representing the current month or quarter limit present in ``PlannedBudgetLimits`` . This only applies to budgets that are created with ``PlannedBudgetLimits`` . Budgets that are created without ``PlannedBudgetLimits`` only contain ``BudgetLimit`` . They don't contain ``PlannedBudgetLimits`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html#cfn-budgets-budget-budgetdata-plannedbudgetlimits
            '''
            result = self._values.get("planned_budget_limits")
            return typing.cast(typing.Any, result)

        @builtins.property
        def time_period(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.TimePeriodProperty"]]:
            '''The period of time that is covered by a budget.

            The period has a start date and an end date. The start date must come before the end date. There are no restrictions on the end date.

            The start date for a budget. If you created your budget and didn't specify a start date, the start date defaults to the start of the chosen time period (MONTHLY, QUARTERLY, or ANNUALLY). For example, if you create your budget on January 24, 2019, choose ``MONTHLY`` , and don't set a start date, the start date defaults to ``01/01/19 00:00 UTC`` . The defaults are the same for the Billing and Cost Management console and the API.

            You can change your start date with the ``UpdateBudget`` operation.

            After the end date, AWS deletes the budget and all associated notifications and subscribers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html#cfn-budgets-budget-budgetdata-timeperiod
            '''
            result = self._values.get("time_period")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.TimePeriodProperty"]], result)

        @builtins.property
        def time_unit(self) -> typing.Optional[builtins.str]:
            '''The length of time until a budget resets the actual and forecasted spend.

            ``DAILY`` is available only for ``RI_UTILIZATION`` and ``RI_COVERAGE`` budgets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html#cfn-budgets-budget-budgetdata-timeunit
            '''
            result = self._values.get("time_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BudgetDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetPropsMixin.CostCategoryValuesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "key": "key",
            "match_options": "matchOptions",
            "values": "values",
        },
    )
    class CostCategoryValuesProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The cost category values used for filtering the costs.

            :param key: The unique name of the cost category.
            :param match_options: The match options that you can use to filter your results.
            :param values: The specific value of the cost category.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costcategoryvalues.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                cost_category_values_property = budgets_mixins.CfnBudgetPropsMixin.CostCategoryValuesProperty(
                    key="key",
                    match_options=["matchOptions"],
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ff0ea6b99b8415f284db820d74b2108b39861316f2254691a6814e3ed77c0a9b)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument match_options", value=match_options, expected_type=type_hints["match_options"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if match_options is not None:
                self._values["match_options"] = match_options
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The unique name of the cost category.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costcategoryvalues.html#cfn-budgets-budget-costcategoryvalues-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def match_options(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The match options that you can use to filter your results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costcategoryvalues.html#cfn-budgets-budget-costcategoryvalues-matchoptions
            '''
            result = self._values.get("match_options")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The specific value of the cost category.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costcategoryvalues.html#cfn-budgets-budget-costcategoryvalues-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CostCategoryValuesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetPropsMixin.CostTypesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "include_credit": "includeCredit",
            "include_discount": "includeDiscount",
            "include_other_subscription": "includeOtherSubscription",
            "include_recurring": "includeRecurring",
            "include_refund": "includeRefund",
            "include_subscription": "includeSubscription",
            "include_support": "includeSupport",
            "include_tax": "includeTax",
            "include_upfront": "includeUpfront",
            "use_amortized": "useAmortized",
            "use_blended": "useBlended",
        },
    )
    class CostTypesProperty:
        def __init__(
            self,
            *,
            include_credit: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_discount: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_other_subscription: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_recurring: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_refund: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_subscription: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_support: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_tax: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_upfront: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            use_amortized: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            use_blended: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The types of cost that are included in a ``COST`` budget, such as tax and subscriptions.

            ``USAGE`` , ``RI_UTILIZATION`` , ``RI_COVERAGE`` , ``SAVINGS_PLANS_UTILIZATION`` , and ``SAVINGS_PLANS_COVERAGE`` budgets don't have ``CostTypes`` .

            :param include_credit: Specifies whether a budget includes credits. The default value is ``true`` .
            :param include_discount: Specifies whether a budget includes discounts. The default value is ``true`` .
            :param include_other_subscription: Specifies whether a budget includes non-RI subscription costs. The default value is ``true`` .
            :param include_recurring: Specifies whether a budget includes recurring fees such as monthly RI fees. The default value is ``true`` .
            :param include_refund: Specifies whether a budget includes refunds. The default value is ``true`` .
            :param include_subscription: Specifies whether a budget includes subscriptions. The default value is ``true`` .
            :param include_support: Specifies whether a budget includes support subscription fees. The default value is ``true`` .
            :param include_tax: Specifies whether a budget includes taxes. The default value is ``true`` .
            :param include_upfront: Specifies whether a budget includes upfront RI costs. The default value is ``true`` .
            :param use_amortized: Specifies whether a budget uses the amortized rate. The default value is ``false`` .
            :param use_blended: Specifies whether a budget uses a blended rate. The default value is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                cost_types_property = budgets_mixins.CfnBudgetPropsMixin.CostTypesProperty(
                    include_credit=False,
                    include_discount=False,
                    include_other_subscription=False,
                    include_recurring=False,
                    include_refund=False,
                    include_subscription=False,
                    include_support=False,
                    include_tax=False,
                    include_upfront=False,
                    use_amortized=False,
                    use_blended=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e594110be42d7dfa671d0b9f9a0890dc6292612082f69042353c9accdab0c372)
                check_type(argname="argument include_credit", value=include_credit, expected_type=type_hints["include_credit"])
                check_type(argname="argument include_discount", value=include_discount, expected_type=type_hints["include_discount"])
                check_type(argname="argument include_other_subscription", value=include_other_subscription, expected_type=type_hints["include_other_subscription"])
                check_type(argname="argument include_recurring", value=include_recurring, expected_type=type_hints["include_recurring"])
                check_type(argname="argument include_refund", value=include_refund, expected_type=type_hints["include_refund"])
                check_type(argname="argument include_subscription", value=include_subscription, expected_type=type_hints["include_subscription"])
                check_type(argname="argument include_support", value=include_support, expected_type=type_hints["include_support"])
                check_type(argname="argument include_tax", value=include_tax, expected_type=type_hints["include_tax"])
                check_type(argname="argument include_upfront", value=include_upfront, expected_type=type_hints["include_upfront"])
                check_type(argname="argument use_amortized", value=use_amortized, expected_type=type_hints["use_amortized"])
                check_type(argname="argument use_blended", value=use_blended, expected_type=type_hints["use_blended"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if include_credit is not None:
                self._values["include_credit"] = include_credit
            if include_discount is not None:
                self._values["include_discount"] = include_discount
            if include_other_subscription is not None:
                self._values["include_other_subscription"] = include_other_subscription
            if include_recurring is not None:
                self._values["include_recurring"] = include_recurring
            if include_refund is not None:
                self._values["include_refund"] = include_refund
            if include_subscription is not None:
                self._values["include_subscription"] = include_subscription
            if include_support is not None:
                self._values["include_support"] = include_support
            if include_tax is not None:
                self._values["include_tax"] = include_tax
            if include_upfront is not None:
                self._values["include_upfront"] = include_upfront
            if use_amortized is not None:
                self._values["use_amortized"] = use_amortized
            if use_blended is not None:
                self._values["use_blended"] = use_blended

        @builtins.property
        def include_credit(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether a budget includes credits.

            The default value is ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-includecredit
            '''
            result = self._values.get("include_credit")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_discount(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether a budget includes discounts.

            The default value is ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-includediscount
            '''
            result = self._values.get("include_discount")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_other_subscription(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether a budget includes non-RI subscription costs.

            The default value is ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-includeothersubscription
            '''
            result = self._values.get("include_other_subscription")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_recurring(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether a budget includes recurring fees such as monthly RI fees.

            The default value is ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-includerecurring
            '''
            result = self._values.get("include_recurring")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_refund(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether a budget includes refunds.

            The default value is ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-includerefund
            '''
            result = self._values.get("include_refund")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_subscription(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether a budget includes subscriptions.

            The default value is ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-includesubscription
            '''
            result = self._values.get("include_subscription")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_support(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether a budget includes support subscription fees.

            The default value is ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-includesupport
            '''
            result = self._values.get("include_support")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_tax(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether a budget includes taxes.

            The default value is ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-includetax
            '''
            result = self._values.get("include_tax")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_upfront(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether a budget includes upfront RI costs.

            The default value is ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-includeupfront
            '''
            result = self._values.get("include_upfront")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def use_amortized(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether a budget uses the amortized rate.

            The default value is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-useamortized
            '''
            result = self._values.get("use_amortized")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def use_blended(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether a budget uses a blended rate.

            The default value is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-useblended
            '''
            result = self._values.get("use_blended")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CostTypesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetPropsMixin.ExpressionDimensionValuesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "key": "key",
            "match_options": "matchOptions",
            "values": "values",
        },
    )
    class ExpressionDimensionValuesProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Contains the specifications for the filters to use for your request.

            :param key: The name of the dimension that you want to filter on.
            :param match_options: The match options that you can use to filter your results. You can specify only one of these values in the array.
            :param values: The metadata values you can specify to filter upon, so that the results all match at least one of the specified values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-expressiondimensionvalues.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                expression_dimension_values_property = budgets_mixins.CfnBudgetPropsMixin.ExpressionDimensionValuesProperty(
                    key="key",
                    match_options=["matchOptions"],
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b4175ad612bf07e1f1ae684b0a52a8e1c3ab24cd1f9bdc9862497259e0a8acb6)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument match_options", value=match_options, expected_type=type_hints["match_options"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if match_options is not None:
                self._values["match_options"] = match_options
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The name of the dimension that you want to filter on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-expressiondimensionvalues.html#cfn-budgets-budget-expressiondimensionvalues-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def match_options(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The match options that you can use to filter your results.

            You can specify only one of these values in the array.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-expressiondimensionvalues.html#cfn-budgets-budget-expressiondimensionvalues-matchoptions
            '''
            result = self._values.get("match_options")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The metadata values you can specify to filter upon, so that the results all match at least one of the specified values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-expressiondimensionvalues.html#cfn-budgets-budget-expressiondimensionvalues-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExpressionDimensionValuesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetPropsMixin.ExpressionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "and_": "and",
            "cost_categories": "costCategories",
            "dimensions": "dimensions",
            "not_": "not",
            "or_": "or",
            "tags": "tags",
        },
    )
    class ExpressionProperty:
        def __init__(
            self,
            *,
            and_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetPropsMixin.ExpressionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            cost_categories: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetPropsMixin.CostCategoryValuesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetPropsMixin.ExpressionDimensionValuesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            not_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetPropsMixin.ExpressionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            or_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetPropsMixin.ExpressionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            tags: typing.Optional[typing.Union["CfnBudgetPropsMixin.TagValuesProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        ) -> None:
            '''Use Expression to filter in various Budgets APIs.

            :param and_: Return results that match both Dimension objects.
            :param cost_categories: The filter that's based on CostCategoryValues.
            :param dimensions: The specific Dimension to use for Expression.
            :param not_: Return results that don't match a Dimension object.
            :param or_: Return results that match either Dimension object.
            :param tags: The specific Tag to use for Expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-expression.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                # expression_property_: budgets_mixins.CfnBudgetPropsMixin.ExpressionProperty
                
                expression_property = budgets_mixins.CfnBudgetPropsMixin.ExpressionProperty(
                    and=[expression_property_],
                    cost_categories=budgets_mixins.CfnBudgetPropsMixin.CostCategoryValuesProperty(
                        key="key",
                        match_options=["matchOptions"],
                        values=["values"]
                    ),
                    dimensions=budgets_mixins.CfnBudgetPropsMixin.ExpressionDimensionValuesProperty(
                        key="key",
                        match_options=["matchOptions"],
                        values=["values"]
                    ),
                    not=expression_property_,
                    or=[expression_property_],
                    tags=budgets_mixins.CfnBudgetPropsMixin.TagValuesProperty(
                        key="key",
                        match_options=["matchOptions"],
                        values=["values"]
                    )
                )
            '''
            if isinstance(tags, dict):
                tags = CfnBudgetPropsMixin.TagValuesProperty(**tags)
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__967237f3dac9c5234d555e9f04267f5f1826c3722158c55ab9bea71e7826b772)
                check_type(argname="argument and_", value=and_, expected_type=type_hints["and_"])
                check_type(argname="argument cost_categories", value=cost_categories, expected_type=type_hints["cost_categories"])
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument not_", value=not_, expected_type=type_hints["not_"])
                check_type(argname="argument or_", value=or_, expected_type=type_hints["or_"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if and_ is not None:
                self._values["and_"] = and_
            if cost_categories is not None:
                self._values["cost_categories"] = cost_categories
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if not_ is not None:
                self._values["not_"] = not_
            if or_ is not None:
                self._values["or_"] = or_
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def and_(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.ExpressionProperty"]]]]:
            '''Return results that match both Dimension objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-expression.html#cfn-budgets-budget-expression-and
            '''
            result = self._values.get("and_")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.ExpressionProperty"]]]], result)

        @builtins.property
        def cost_categories(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.CostCategoryValuesProperty"]]:
            '''The filter that's based on CostCategoryValues.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-expression.html#cfn-budgets-budget-expression-costcategories
            '''
            result = self._values.get("cost_categories")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.CostCategoryValuesProperty"]], result)

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.ExpressionDimensionValuesProperty"]]:
            '''The specific Dimension to use for Expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-expression.html#cfn-budgets-budget-expression-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.ExpressionDimensionValuesProperty"]], result)

        @builtins.property
        def not_(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.ExpressionProperty"]]:
            '''Return results that don't match a Dimension object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-expression.html#cfn-budgets-budget-expression-not
            '''
            result = self._values.get("not_")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.ExpressionProperty"]], result)

        @builtins.property
        def or_(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.ExpressionProperty"]]]]:
            '''Return results that match either Dimension object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-expression.html#cfn-budgets-budget-expression-or
            '''
            result = self._values.get("or_")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.ExpressionProperty"]]]], result)

        @builtins.property
        def tags(self) -> typing.Optional["CfnBudgetPropsMixin.TagValuesProperty"]:
            '''The specific Tag to use for Expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-expression.html#cfn-budgets-budget-expression-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional["CfnBudgetPropsMixin.TagValuesProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExpressionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetPropsMixin.HistoricalOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"budget_adjustment_period": "budgetAdjustmentPeriod"},
    )
    class HistoricalOptionsProperty:
        def __init__(
            self,
            *,
            budget_adjustment_period: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The parameters that define or describe the historical data that your auto-adjusting budget is based on.

            :param budget_adjustment_period: The number of budget periods included in the moving-average calculation that determines your auto-adjusted budget amount. The maximum value depends on the ``TimeUnit`` granularity of the budget: - For the ``DAILY`` granularity, the maximum value is ``60`` . - For the ``MONTHLY`` granularity, the maximum value is ``12`` . - For the ``QUARTERLY`` granularity, the maximum value is ``4`` . - For the ``ANNUALLY`` granularity, the maximum value is ``1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-historicaloptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                historical_options_property = budgets_mixins.CfnBudgetPropsMixin.HistoricalOptionsProperty(
                    budget_adjustment_period=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__12aeb586b22de12ca280d83e36ec4c0311360186658f5c8481a142a725a8729c)
                check_type(argname="argument budget_adjustment_period", value=budget_adjustment_period, expected_type=type_hints["budget_adjustment_period"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if budget_adjustment_period is not None:
                self._values["budget_adjustment_period"] = budget_adjustment_period

        @builtins.property
        def budget_adjustment_period(self) -> typing.Optional[jsii.Number]:
            '''The number of budget periods included in the moving-average calculation that determines your auto-adjusted budget amount.

            The maximum value depends on the ``TimeUnit`` granularity of the budget:

            - For the ``DAILY`` granularity, the maximum value is ``60`` .
            - For the ``MONTHLY`` granularity, the maximum value is ``12`` .
            - For the ``QUARTERLY`` granularity, the maximum value is ``4`` .
            - For the ``ANNUALLY`` granularity, the maximum value is ``1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-historicaloptions.html#cfn-budgets-budget-historicaloptions-budgetadjustmentperiod
            '''
            result = self._values.get("budget_adjustment_period")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HistoricalOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetPropsMixin.NotificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "comparison_operator": "comparisonOperator",
            "notification_type": "notificationType",
            "threshold": "threshold",
            "threshold_type": "thresholdType",
        },
    )
    class NotificationProperty:
        def __init__(
            self,
            *,
            comparison_operator: typing.Optional[builtins.str] = None,
            notification_type: typing.Optional[builtins.str] = None,
            threshold: typing.Optional[jsii.Number] = None,
            threshold_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A notification that's associated with a budget. A budget can have up to ten notifications.

            Each notification must have at least one subscriber. A notification can have one SNS subscriber and up to 10 email subscribers, for a total of 11 subscribers.

            For example, if you have a budget for 200 dollars and you want to be notified when you go over 160 dollars, create a notification with the following parameters:

            - A notificationType of ``ACTUAL``
            - A ``thresholdType`` of ``PERCENTAGE``
            - A ``comparisonOperator`` of ``GREATER_THAN``
            - A notification ``threshold`` of ``80``

            :param comparison_operator: The comparison that's used for this notification.
            :param notification_type: Specifies whether the notification is for how much you have spent ( ``ACTUAL`` ) or for how much that you're forecasted to spend ( ``FORECASTED`` ).
            :param threshold: The threshold that's associated with a notification. Thresholds are always a percentage, and many customers find value being alerted between 50% - 200% of the budgeted amount. The maximum limit for your threshold is 1,000,000% above the budgeted amount.
            :param threshold_type: The type of threshold for a notification. For ``ABSOLUTE_VALUE`` thresholds, AWS notifies you when you go over or are forecasted to go over your total cost threshold. For ``PERCENTAGE`` thresholds, AWS notifies you when you go over or are forecasted to go over a certain percentage of your forecasted spend. For example, if you have a budget for 200 dollars and you have a ``PERCENTAGE`` threshold of 80%, AWS notifies you when you go over 160 dollars.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-notification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                notification_property = budgets_mixins.CfnBudgetPropsMixin.NotificationProperty(
                    comparison_operator="comparisonOperator",
                    notification_type="notificationType",
                    threshold=123,
                    threshold_type="thresholdType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__03bc5222edad586b8094ed89be2482508cc0ca665e924eda73377093920de642)
                check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
                check_type(argname="argument notification_type", value=notification_type, expected_type=type_hints["notification_type"])
                check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
                check_type(argname="argument threshold_type", value=threshold_type, expected_type=type_hints["threshold_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparison_operator is not None:
                self._values["comparison_operator"] = comparison_operator
            if notification_type is not None:
                self._values["notification_type"] = notification_type
            if threshold is not None:
                self._values["threshold"] = threshold
            if threshold_type is not None:
                self._values["threshold_type"] = threshold_type

        @builtins.property
        def comparison_operator(self) -> typing.Optional[builtins.str]:
            '''The comparison that's used for this notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-notification.html#cfn-budgets-budget-notification-comparisonoperator
            '''
            result = self._values.get("comparison_operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def notification_type(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the notification is for how much you have spent ( ``ACTUAL`` ) or for how much that you're forecasted to spend ( ``FORECASTED`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-notification.html#cfn-budgets-budget-notification-notificationtype
            '''
            result = self._values.get("notification_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def threshold(self) -> typing.Optional[jsii.Number]:
            '''The threshold that's associated with a notification.

            Thresholds are always a percentage, and many customers find value being alerted between 50% - 200% of the budgeted amount. The maximum limit for your threshold is 1,000,000% above the budgeted amount.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-notification.html#cfn-budgets-budget-notification-threshold
            '''
            result = self._values.get("threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def threshold_type(self) -> typing.Optional[builtins.str]:
            '''The type of threshold for a notification.

            For ``ABSOLUTE_VALUE`` thresholds, AWS notifies you when you go over or are forecasted to go over your total cost threshold. For ``PERCENTAGE`` thresholds, AWS notifies you when you go over or are forecasted to go over a certain percentage of your forecasted spend. For example, if you have a budget for 200 dollars and you have a ``PERCENTAGE`` threshold of 80%, AWS notifies you when you go over 160 dollars.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-notification.html#cfn-budgets-budget-notification-thresholdtype
            '''
            result = self._values.get("threshold_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetPropsMixin.NotificationWithSubscribersProperty",
        jsii_struct_bases=[],
        name_mapping={"notification": "notification", "subscribers": "subscribers"},
    )
    class NotificationWithSubscribersProperty:
        def __init__(
            self,
            *,
            notification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetPropsMixin.NotificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            subscribers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetPropsMixin.SubscriberProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A notification with subscribers.

            A notification can have one SNS subscriber and up to 10 email subscribers, for a total of 11 subscribers.

            :param notification: The notification that's associated with a budget.
            :param subscribers: A list of subscribers who are subscribed to this notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-notificationwithsubscribers.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                notification_with_subscribers_property = budgets_mixins.CfnBudgetPropsMixin.NotificationWithSubscribersProperty(
                    notification=budgets_mixins.CfnBudgetPropsMixin.NotificationProperty(
                        comparison_operator="comparisonOperator",
                        notification_type="notificationType",
                        threshold=123,
                        threshold_type="thresholdType"
                    ),
                    subscribers=[budgets_mixins.CfnBudgetPropsMixin.SubscriberProperty(
                        address="address",
                        subscription_type="subscriptionType"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__94e5db20c874699ae3c6d1ece1d8ff694baea7a6ea8681db95bab95166a431f0)
                check_type(argname="argument notification", value=notification, expected_type=type_hints["notification"])
                check_type(argname="argument subscribers", value=subscribers, expected_type=type_hints["subscribers"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if notification is not None:
                self._values["notification"] = notification
            if subscribers is not None:
                self._values["subscribers"] = subscribers

        @builtins.property
        def notification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.NotificationProperty"]]:
            '''The notification that's associated with a budget.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-notificationwithsubscribers.html#cfn-budgets-budget-notificationwithsubscribers-notification
            '''
            result = self._values.get("notification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.NotificationProperty"]], result)

        @builtins.property
        def subscribers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.SubscriberProperty"]]]]:
            '''A list of subscribers who are subscribed to this notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-notificationwithsubscribers.html#cfn-budgets-budget-notificationwithsubscribers-subscribers
            '''
            result = self._values.get("subscribers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetPropsMixin.SubscriberProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationWithSubscribersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetPropsMixin.ResourceTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ResourceTagProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The tag structure that contains a tag key and value.

            :param key: The key that's associated with the tag.
            :param value: The value that's associated with the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-resourcetag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                resource_tag_property = budgets_mixins.CfnBudgetPropsMixin.ResourceTagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6070f206525027f1172b4ea4d00409d4df47ba3e697840561eaa4b01fd3e8a41)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key that's associated with the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-resourcetag.html#cfn-budgets-budget-resourcetag-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value that's associated with the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-resourcetag.html#cfn-budgets-budget-resourcetag-value
            '''
            result = self._values.get("value")
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
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetPropsMixin.SpendProperty",
        jsii_struct_bases=[],
        name_mapping={"amount": "amount", "unit": "unit"},
    )
    class SpendProperty:
        def __init__(
            self,
            *,
            amount: typing.Optional[jsii.Number] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The amount of cost or usage that's measured for a budget.

            *Cost example:* A ``Spend`` for ``3 USD`` of costs has the following parameters:

            - An ``Amount`` of ``3``
            - A ``Unit`` of ``USD``

            *Usage example:* A ``Spend`` for ``3 GB`` of S3 usage has the following parameters:

            - An ``Amount`` of ``3``
            - A ``Unit`` of ``GB``

            :param amount: The cost or usage amount that's associated with a budget forecast, actual spend, or budget threshold.
            :param unit: The unit of measurement that's used for the budget forecast, actual spend, or budget threshold.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-spend.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                spend_property = budgets_mixins.CfnBudgetPropsMixin.SpendProperty(
                    amount=123,
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__880c58d2acd9c23e29a9d0838a18cffa64908f3f99c7e7a97f83ca53eb0295e9)
                check_type(argname="argument amount", value=amount, expected_type=type_hints["amount"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if amount is not None:
                self._values["amount"] = amount
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def amount(self) -> typing.Optional[jsii.Number]:
            '''The cost or usage amount that's associated with a budget forecast, actual spend, or budget threshold.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-spend.html#cfn-budgets-budget-spend-amount
            '''
            result = self._values.get("amount")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit of measurement that's used for the budget forecast, actual spend, or budget threshold.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-spend.html#cfn-budgets-budget-spend-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SpendProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetPropsMixin.SubscriberProperty",
        jsii_struct_bases=[],
        name_mapping={"address": "address", "subscription_type": "subscriptionType"},
    )
    class SubscriberProperty:
        def __init__(
            self,
            *,
            address: typing.Optional[builtins.str] = None,
            subscription_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``Subscriber`` property type specifies who to notify for a Billing and Cost Management budget notification.

            The subscriber consists of a subscription type, and either an Amazon SNS topic or an email address.

            For example, an email subscriber would have the following parameters:

            - A ``subscriptionType`` of ``EMAIL``
            - An ``address`` of ``example@example.com``

            :param address: The address that AWS sends budget notifications to, either an SNS topic or an email. When you create a subscriber, the value of ``Address`` can't contain line breaks.
            :param subscription_type: The type of notification that AWS sends to a subscriber.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-subscriber.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                subscriber_property = budgets_mixins.CfnBudgetPropsMixin.SubscriberProperty(
                    address="address",
                    subscription_type="subscriptionType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ce26fe79aa46476ded0165fe2b965c53c8345329959493c1430578cb6b8abd80)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
                check_type(argname="argument subscription_type", value=subscription_type, expected_type=type_hints["subscription_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address
            if subscription_type is not None:
                self._values["subscription_type"] = subscription_type

        @builtins.property
        def address(self) -> typing.Optional[builtins.str]:
            '''The address that AWS sends budget notifications to, either an SNS topic or an email.

            When you create a subscriber, the value of ``Address`` can't contain line breaks.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-subscriber.html#cfn-budgets-budget-subscriber-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subscription_type(self) -> typing.Optional[builtins.str]:
            '''The type of notification that AWS sends to a subscriber.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-subscriber.html#cfn-budgets-budget-subscriber-subscriptiontype
            '''
            result = self._values.get("subscription_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubscriberProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetPropsMixin.TagValuesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "key": "key",
            "match_options": "matchOptions",
            "values": "values",
        },
    )
    class TagValuesProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The values that are available for a tag.

            :param key: The key for the tag.
            :param match_options: The match options that you can use to filter your results.
            :param values: The specific value of the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-tagvalues.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                tag_values_property = budgets_mixins.CfnBudgetPropsMixin.TagValuesProperty(
                    key="key",
                    match_options=["matchOptions"],
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e2dfc451346cea3a1deb0a70963996549da4236697830e7ee1607561b787cf90)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument match_options", value=match_options, expected_type=type_hints["match_options"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if match_options is not None:
                self._values["match_options"] = match_options
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key for the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-tagvalues.html#cfn-budgets-budget-tagvalues-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def match_options(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The match options that you can use to filter your results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-tagvalues.html#cfn-budgets-budget-tagvalues-matchoptions
            '''
            result = self._values.get("match_options")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The specific value of the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-tagvalues.html#cfn-budgets-budget-tagvalues-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagValuesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetPropsMixin.TimePeriodProperty",
        jsii_struct_bases=[],
        name_mapping={"end": "end", "start": "start"},
    )
    class TimePeriodProperty:
        def __init__(
            self,
            *,
            end: typing.Optional[builtins.str] = None,
            start: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The period of time that is covered by a budget.

            The period has a start date and an end date. The start date must come before the end date. There are no restrictions on the end date.

            :param end: The end date for a budget. If you didn't specify an end date, AWS set your end date to ``06/15/87 00:00 UTC`` . The defaults are the same for the Billing and Cost Management console and the API. After the end date, AWS deletes the budget and all the associated notifications and subscribers. You can change your end date with the ``UpdateBudget`` operation.
            :param start: The start date for a budget. If you created your budget and didn't specify a start date, the start date defaults to the start of the chosen time period (MONTHLY, QUARTERLY, or ANNUALLY). For example, if you create your budget on January 24, 2019, choose ``MONTHLY`` , and don't set a start date, the start date defaults to ``01/01/19 00:00 UTC`` . The defaults are the same for the Billing and Cost Management console and the API. You can change your start date with the ``UpdateBudget`` operation. Valid values depend on the value of ``BudgetType`` : - If ``BudgetType`` is ``COST`` or ``USAGE`` : Valid values are ``MONTHLY`` , ``QUARTERLY`` , and ``ANNUALLY`` . - If ``BudgetType`` is ``RI_UTILIZATION`` or ``RI_COVERAGE`` : Valid values are ``DAILY`` , ``MONTHLY`` , ``QUARTERLY`` , and ``ANNUALLY`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-timeperiod.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                time_period_property = budgets_mixins.CfnBudgetPropsMixin.TimePeriodProperty(
                    end="end",
                    start="start"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e6c48c7b6b4276dcc966f9a8c7807c886573e5b087c203931e2af25f65577690)
                check_type(argname="argument end", value=end, expected_type=type_hints["end"])
                check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end is not None:
                self._values["end"] = end
            if start is not None:
                self._values["start"] = start

        @builtins.property
        def end(self) -> typing.Optional[builtins.str]:
            '''The end date for a budget.

            If you didn't specify an end date, AWS set your end date to ``06/15/87 00:00 UTC`` . The defaults are the same for the Billing and Cost Management console and the API.

            After the end date, AWS deletes the budget and all the associated notifications and subscribers. You can change your end date with the ``UpdateBudget`` operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-timeperiod.html#cfn-budgets-budget-timeperiod-end
            '''
            result = self._values.get("end")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start(self) -> typing.Optional[builtins.str]:
            '''The start date for a budget.

            If you created your budget and didn't specify a start date, the start date defaults to the start of the chosen time period (MONTHLY, QUARTERLY, or ANNUALLY). For example, if you create your budget on January 24, 2019, choose ``MONTHLY`` , and don't set a start date, the start date defaults to ``01/01/19 00:00 UTC`` . The defaults are the same for the Billing and Cost Management console and the API.

            You can change your start date with the ``UpdateBudget`` operation.

            Valid values depend on the value of ``BudgetType`` :

            - If ``BudgetType`` is ``COST`` or ``USAGE`` : Valid values are ``MONTHLY`` , ``QUARTERLY`` , and ``ANNUALLY`` .
            - If ``BudgetType`` is ``RI_UTILIZATION`` or ``RI_COVERAGE`` : Valid values are ``DAILY`` , ``MONTHLY`` , ``QUARTERLY`` , and ``ANNUALLY`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-timeperiod.html#cfn-budgets-budget-timeperiod-start
            '''
            result = self._values.get("start")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimePeriodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetsActionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "action_threshold": "actionThreshold",
        "action_type": "actionType",
        "approval_model": "approvalModel",
        "budget_name": "budgetName",
        "definition": "definition",
        "execution_role_arn": "executionRoleArn",
        "notification_type": "notificationType",
        "resource_tags": "resourceTags",
        "subscribers": "subscribers",
    },
)
class CfnBudgetsActionMixinProps:
    def __init__(
        self,
        *,
        action_threshold: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetsActionPropsMixin.ActionThresholdProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        action_type: typing.Optional[builtins.str] = None,
        approval_model: typing.Optional[builtins.str] = None,
        budget_name: typing.Optional[builtins.str] = None,
        definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetsActionPropsMixin.DefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        notification_type: typing.Optional[builtins.str] = None,
        resource_tags: typing.Optional[typing.Sequence[typing.Union["CfnBudgetsActionPropsMixin.ResourceTagProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        subscribers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetsActionPropsMixin.SubscriberProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnBudgetsActionPropsMixin.

        :param action_threshold: The trigger threshold of the action.
        :param action_type: The type of action. This defines the type of tasks that can be carried out by this action. This field also determines the format for definition.
        :param approval_model: This specifies if the action needs manual or automatic approval.
        :param budget_name: A string that represents the budget name. ":" and "" characters aren't allowed.
        :param definition: Specifies all of the type-specific parameters.
        :param execution_role_arn: The role passed for action execution and reversion. Roles and actions must be in the same account.
        :param notification_type: The type of a notification.
        :param resource_tags: An optional list of tags to associate with the specified budget action. Each tag consists of a key and a value, and each key must be unique for the resource.
        :param subscribers: A list of subscribers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budgetsaction.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
            
            cfn_budgets_action_mixin_props = budgets_mixins.CfnBudgetsActionMixinProps(
                action_threshold=budgets_mixins.CfnBudgetsActionPropsMixin.ActionThresholdProperty(
                    type="type",
                    value=123
                ),
                action_type="actionType",
                approval_model="approvalModel",
                budget_name="budgetName",
                definition=budgets_mixins.CfnBudgetsActionPropsMixin.DefinitionProperty(
                    iam_action_definition=budgets_mixins.CfnBudgetsActionPropsMixin.IamActionDefinitionProperty(
                        groups=["groups"],
                        policy_arn="policyArn",
                        roles=["roles"],
                        users=["users"]
                    ),
                    scp_action_definition=budgets_mixins.CfnBudgetsActionPropsMixin.ScpActionDefinitionProperty(
                        policy_id="policyId",
                        target_ids=["targetIds"]
                    ),
                    ssm_action_definition=budgets_mixins.CfnBudgetsActionPropsMixin.SsmActionDefinitionProperty(
                        instance_ids=["instanceIds"],
                        region="region",
                        subtype="subtype"
                    )
                ),
                execution_role_arn="executionRoleArn",
                notification_type="notificationType",
                resource_tags=[budgets_mixins.CfnBudgetsActionPropsMixin.ResourceTagProperty(
                    key="key",
                    value="value"
                )],
                subscribers=[budgets_mixins.CfnBudgetsActionPropsMixin.SubscriberProperty(
                    address="address",
                    type="type"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0200f40c9e9e6a7e264d6d846bfd64414a5275a2c8d0fffd49c40e1f13dd1e6)
            check_type(argname="argument action_threshold", value=action_threshold, expected_type=type_hints["action_threshold"])
            check_type(argname="argument action_type", value=action_type, expected_type=type_hints["action_type"])
            check_type(argname="argument approval_model", value=approval_model, expected_type=type_hints["approval_model"])
            check_type(argname="argument budget_name", value=budget_name, expected_type=type_hints["budget_name"])
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument notification_type", value=notification_type, expected_type=type_hints["notification_type"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
            check_type(argname="argument subscribers", value=subscribers, expected_type=type_hints["subscribers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action_threshold is not None:
            self._values["action_threshold"] = action_threshold
        if action_type is not None:
            self._values["action_type"] = action_type
        if approval_model is not None:
            self._values["approval_model"] = approval_model
        if budget_name is not None:
            self._values["budget_name"] = budget_name
        if definition is not None:
            self._values["definition"] = definition
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if notification_type is not None:
            self._values["notification_type"] = notification_type
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags
        if subscribers is not None:
            self._values["subscribers"] = subscribers

    @builtins.property
    def action_threshold(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetsActionPropsMixin.ActionThresholdProperty"]]:
        '''The trigger threshold of the action.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budgetsaction.html#cfn-budgets-budgetsaction-actionthreshold
        '''
        result = self._values.get("action_threshold")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetsActionPropsMixin.ActionThresholdProperty"]], result)

    @builtins.property
    def action_type(self) -> typing.Optional[builtins.str]:
        '''The type of action.

        This defines the type of tasks that can be carried out by this action. This field also determines the format for definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budgetsaction.html#cfn-budgets-budgetsaction-actiontype
        '''
        result = self._values.get("action_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def approval_model(self) -> typing.Optional[builtins.str]:
        '''This specifies if the action needs manual or automatic approval.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budgetsaction.html#cfn-budgets-budgetsaction-approvalmodel
        '''
        result = self._values.get("approval_model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def budget_name(self) -> typing.Optional[builtins.str]:
        '''A string that represents the budget name.

        ":" and "" characters aren't allowed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budgetsaction.html#cfn-budgets-budgetsaction-budgetname
        '''
        result = self._values.get("budget_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def definition(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetsActionPropsMixin.DefinitionProperty"]]:
        '''Specifies all of the type-specific parameters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budgetsaction.html#cfn-budgets-budgetsaction-definition
        '''
        result = self._values.get("definition")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetsActionPropsMixin.DefinitionProperty"]], result)

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The role passed for action execution and reversion.

        Roles and actions must be in the same account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budgetsaction.html#cfn-budgets-budgetsaction-executionrolearn
        '''
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_type(self) -> typing.Optional[builtins.str]:
        '''The type of a notification.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budgetsaction.html#cfn-budgets-budgetsaction-notificationtype
        '''
        result = self._values.get("notification_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.List["CfnBudgetsActionPropsMixin.ResourceTagProperty"]]:
        '''An optional list of tags to associate with the specified budget action.

        Each tag consists of a key and a value, and each key must be unique for the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budgetsaction.html#cfn-budgets-budgetsaction-resourcetags
        '''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.List["CfnBudgetsActionPropsMixin.ResourceTagProperty"]], result)

    @builtins.property
    def subscribers(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetsActionPropsMixin.SubscriberProperty"]]]]:
        '''A list of subscribers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budgetsaction.html#cfn-budgets-budgetsaction-subscribers
        '''
        result = self._values.get("subscribers")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetsActionPropsMixin.SubscriberProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBudgetsActionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBudgetsActionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetsActionPropsMixin",
):
    '''The ``AWS::Budgets::BudgetsAction`` resource enables you to take predefined actions that are initiated when a budget threshold has been exceeded.

    For more information, see `Managing Your Costs with Budgets <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/budgets-managing-costs.html>`_ in the *Billing and Cost Management User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budgetsaction.html
    :cloudformationResource: AWS::Budgets::BudgetsAction
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
        
        cfn_budgets_action_props_mixin = budgets_mixins.CfnBudgetsActionPropsMixin(budgets_mixins.CfnBudgetsActionMixinProps(
            action_threshold=budgets_mixins.CfnBudgetsActionPropsMixin.ActionThresholdProperty(
                type="type",
                value=123
            ),
            action_type="actionType",
            approval_model="approvalModel",
            budget_name="budgetName",
            definition=budgets_mixins.CfnBudgetsActionPropsMixin.DefinitionProperty(
                iam_action_definition=budgets_mixins.CfnBudgetsActionPropsMixin.IamActionDefinitionProperty(
                    groups=["groups"],
                    policy_arn="policyArn",
                    roles=["roles"],
                    users=["users"]
                ),
                scp_action_definition=budgets_mixins.CfnBudgetsActionPropsMixin.ScpActionDefinitionProperty(
                    policy_id="policyId",
                    target_ids=["targetIds"]
                ),
                ssm_action_definition=budgets_mixins.CfnBudgetsActionPropsMixin.SsmActionDefinitionProperty(
                    instance_ids=["instanceIds"],
                    region="region",
                    subtype="subtype"
                )
            ),
            execution_role_arn="executionRoleArn",
            notification_type="notificationType",
            resource_tags=[budgets_mixins.CfnBudgetsActionPropsMixin.ResourceTagProperty(
                key="key",
                value="value"
            )],
            subscribers=[budgets_mixins.CfnBudgetsActionPropsMixin.SubscriberProperty(
                address="address",
                type="type"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnBudgetsActionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Budgets::BudgetsAction``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acb78e8f7ace20ee4f9926de350cc86891d666bb58175489e276a8e5c057e33e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__568aae79b943e8e49b8e561ec3c3be9d4d45c06974c2877cfa8e3504d7a60a33)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c874671d0370f703ee847c5930eff02b3942af5e5025766e23bf2a47b38e21e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBudgetsActionMixinProps:
        return typing.cast(CfnBudgetsActionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetsActionPropsMixin.ActionThresholdProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class ActionThresholdProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The trigger threshold of the action.

            :param type: The type of threshold for a notification.
            :param value: The threshold of a notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-actionthreshold.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                action_threshold_property = budgets_mixins.CfnBudgetsActionPropsMixin.ActionThresholdProperty(
                    type="type",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__882df1925c14c0d6e27df33924c099b7ba3d66eb7b8064ec492631287fdfb11e)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of threshold for a notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-actionthreshold.html#cfn-budgets-budgetsaction-actionthreshold-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The threshold of a notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-actionthreshold.html#cfn-budgets-budgetsaction-actionthreshold-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionThresholdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetsActionPropsMixin.DefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "iam_action_definition": "iamActionDefinition",
            "scp_action_definition": "scpActionDefinition",
            "ssm_action_definition": "ssmActionDefinition",
        },
    )
    class DefinitionProperty:
        def __init__(
            self,
            *,
            iam_action_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetsActionPropsMixin.IamActionDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            scp_action_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetsActionPropsMixin.ScpActionDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ssm_action_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBudgetsActionPropsMixin.SsmActionDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The definition is where you specify all of the type-specific parameters.

            :param iam_action_definition: The AWS Identity and Access Management ( IAM ) action definition details.
            :param scp_action_definition: The service control policies (SCP) action definition details.
            :param ssm_action_definition: The Amazon EC2 Systems Manager ( SSM ) action definition details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-definition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                definition_property = budgets_mixins.CfnBudgetsActionPropsMixin.DefinitionProperty(
                    iam_action_definition=budgets_mixins.CfnBudgetsActionPropsMixin.IamActionDefinitionProperty(
                        groups=["groups"],
                        policy_arn="policyArn",
                        roles=["roles"],
                        users=["users"]
                    ),
                    scp_action_definition=budgets_mixins.CfnBudgetsActionPropsMixin.ScpActionDefinitionProperty(
                        policy_id="policyId",
                        target_ids=["targetIds"]
                    ),
                    ssm_action_definition=budgets_mixins.CfnBudgetsActionPropsMixin.SsmActionDefinitionProperty(
                        instance_ids=["instanceIds"],
                        region="region",
                        subtype="subtype"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9b9096898e69a7f0c115cd373f9070a8b47a0c79101147fa4618d68e8a610cca)
                check_type(argname="argument iam_action_definition", value=iam_action_definition, expected_type=type_hints["iam_action_definition"])
                check_type(argname="argument scp_action_definition", value=scp_action_definition, expected_type=type_hints["scp_action_definition"])
                check_type(argname="argument ssm_action_definition", value=ssm_action_definition, expected_type=type_hints["ssm_action_definition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iam_action_definition is not None:
                self._values["iam_action_definition"] = iam_action_definition
            if scp_action_definition is not None:
                self._values["scp_action_definition"] = scp_action_definition
            if ssm_action_definition is not None:
                self._values["ssm_action_definition"] = ssm_action_definition

        @builtins.property
        def iam_action_definition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetsActionPropsMixin.IamActionDefinitionProperty"]]:
            '''The AWS Identity and Access Management ( IAM ) action definition details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-definition.html#cfn-budgets-budgetsaction-definition-iamactiondefinition
            '''
            result = self._values.get("iam_action_definition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetsActionPropsMixin.IamActionDefinitionProperty"]], result)

        @builtins.property
        def scp_action_definition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetsActionPropsMixin.ScpActionDefinitionProperty"]]:
            '''The service control policies (SCP) action definition details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-definition.html#cfn-budgets-budgetsaction-definition-scpactiondefinition
            '''
            result = self._values.get("scp_action_definition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetsActionPropsMixin.ScpActionDefinitionProperty"]], result)

        @builtins.property
        def ssm_action_definition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetsActionPropsMixin.SsmActionDefinitionProperty"]]:
            '''The Amazon EC2 Systems Manager ( SSM ) action definition details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-definition.html#cfn-budgets-budgetsaction-definition-ssmactiondefinition
            '''
            result = self._values.get("ssm_action_definition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBudgetsActionPropsMixin.SsmActionDefinitionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetsActionPropsMixin.IamActionDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "groups": "groups",
            "policy_arn": "policyArn",
            "roles": "roles",
            "users": "users",
        },
    )
    class IamActionDefinitionProperty:
        def __init__(
            self,
            *,
            groups: typing.Optional[typing.Sequence[builtins.str]] = None,
            policy_arn: typing.Optional[builtins.str] = None,
            roles: typing.Optional[typing.Sequence[builtins.str]] = None,
            users: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The AWS Identity and Access Management ( IAM ) action definition details.

            :param groups: A list of groups to be attached. There must be at least one group.
            :param policy_arn: The Amazon Resource Name (ARN) of the policy to be attached.
            :param roles: A list of roles to be attached. There must be at least one role.
            :param users: A list of users to be attached. There must be at least one user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-iamactiondefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                iam_action_definition_property = budgets_mixins.CfnBudgetsActionPropsMixin.IamActionDefinitionProperty(
                    groups=["groups"],
                    policy_arn="policyArn",
                    roles=["roles"],
                    users=["users"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5cb2cb7fc1ce7dc37bcb7a6669f2fd4cf63356ab9d9f1d5c738fd7ab833aa465)
                check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
                check_type(argname="argument policy_arn", value=policy_arn, expected_type=type_hints["policy_arn"])
                check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
                check_type(argname="argument users", value=users, expected_type=type_hints["users"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if groups is not None:
                self._values["groups"] = groups
            if policy_arn is not None:
                self._values["policy_arn"] = policy_arn
            if roles is not None:
                self._values["roles"] = roles
            if users is not None:
                self._values["users"] = users

        @builtins.property
        def groups(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of groups to be attached.

            There must be at least one group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-iamactiondefinition.html#cfn-budgets-budgetsaction-iamactiondefinition-groups
            '''
            result = self._values.get("groups")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def policy_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the policy to be attached.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-iamactiondefinition.html#cfn-budgets-budgetsaction-iamactiondefinition-policyarn
            '''
            result = self._values.get("policy_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def roles(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of roles to be attached.

            There must be at least one role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-iamactiondefinition.html#cfn-budgets-budgetsaction-iamactiondefinition-roles
            '''
            result = self._values.get("roles")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def users(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of users to be attached.

            There must be at least one user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-iamactiondefinition.html#cfn-budgets-budgetsaction-iamactiondefinition-users
            '''
            result = self._values.get("users")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IamActionDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetsActionPropsMixin.ResourceTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ResourceTagProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The tag structure that contains a tag key and value.

            :param key: The key that's associated with the tag.
            :param value: The value that's associated with the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-resourcetag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                resource_tag_property = budgets_mixins.CfnBudgetsActionPropsMixin.ResourceTagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0e79f71611bdd186971ffcb670310ec256e59603cab3fe07a6cc3ef8b803bb8e)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key that's associated with the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-resourcetag.html#cfn-budgets-budgetsaction-resourcetag-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value that's associated with the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-resourcetag.html#cfn-budgets-budgetsaction-resourcetag-value
            '''
            result = self._values.get("value")
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
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetsActionPropsMixin.ScpActionDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"policy_id": "policyId", "target_ids": "targetIds"},
    )
    class ScpActionDefinitionProperty:
        def __init__(
            self,
            *,
            policy_id: typing.Optional[builtins.str] = None,
            target_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The service control policies (SCP) action definition details.

            :param policy_id: The policy ID attached.
            :param target_ids: A list of target IDs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-scpactiondefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                scp_action_definition_property = budgets_mixins.CfnBudgetsActionPropsMixin.ScpActionDefinitionProperty(
                    policy_id="policyId",
                    target_ids=["targetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a183107dcca25aa29a1a479ea927c1681d6038c3cd79fb25bb234308235abb43)
                check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
                check_type(argname="argument target_ids", value=target_ids, expected_type=type_hints["target_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if policy_id is not None:
                self._values["policy_id"] = policy_id
            if target_ids is not None:
                self._values["target_ids"] = target_ids

        @builtins.property
        def policy_id(self) -> typing.Optional[builtins.str]:
            '''The policy ID attached.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-scpactiondefinition.html#cfn-budgets-budgetsaction-scpactiondefinition-policyid
            '''
            result = self._values.get("policy_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of target IDs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-scpactiondefinition.html#cfn-budgets-budgetsaction-scpactiondefinition-targetids
            '''
            result = self._values.get("target_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScpActionDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetsActionPropsMixin.SsmActionDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instance_ids": "instanceIds",
            "region": "region",
            "subtype": "subtype",
        },
    )
    class SsmActionDefinitionProperty:
        def __init__(
            self,
            *,
            instance_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            region: typing.Optional[builtins.str] = None,
            subtype: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Amazon EC2 Systems Manager ( SSM ) action definition details.

            :param instance_ids: The EC2 and RDS instance IDs.
            :param region: The Region to run the ( SSM ) document.
            :param subtype: The action subType.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-ssmactiondefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                ssm_action_definition_property = budgets_mixins.CfnBudgetsActionPropsMixin.SsmActionDefinitionProperty(
                    instance_ids=["instanceIds"],
                    region="region",
                    subtype="subtype"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4cfe13b3ff924912fe34798f87ae05b3fdb3cb1ae47b476d307bb6eeae125dd0)
                check_type(argname="argument instance_ids", value=instance_ids, expected_type=type_hints["instance_ids"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument subtype", value=subtype, expected_type=type_hints["subtype"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_ids is not None:
                self._values["instance_ids"] = instance_ids
            if region is not None:
                self._values["region"] = region
            if subtype is not None:
                self._values["subtype"] = subtype

        @builtins.property
        def instance_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The EC2 and RDS instance IDs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-ssmactiondefinition.html#cfn-budgets-budgetsaction-ssmactiondefinition-instanceids
            '''
            result = self._values.get("instance_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The Region to run the ( SSM ) document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-ssmactiondefinition.html#cfn-budgets-budgetsaction-ssmactiondefinition-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subtype(self) -> typing.Optional[builtins.str]:
            '''The action subType.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-ssmactiondefinition.html#cfn-budgets-budgetsaction-ssmactiondefinition-subtype
            '''
            result = self._values.get("subtype")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SsmActionDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_budgets.mixins.CfnBudgetsActionPropsMixin.SubscriberProperty",
        jsii_struct_bases=[],
        name_mapping={"address": "address", "type": "type"},
    )
    class SubscriberProperty:
        def __init__(
            self,
            *,
            address: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The subscriber to a budget notification.

            The subscriber consists of a subscription type and either an Amazon SNS topic or an email address.

            For example, an email subscriber has the following parameters:

            - A ``subscriptionType`` of ``EMAIL``
            - An ``address`` of ``example@example.com``

            :param address: The address that AWS sends budget notifications to, either an SNS topic or an email. When you create a subscriber, the value of ``Address`` can't contain line breaks.
            :param type: The type of notification that AWS sends to a subscriber.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-subscriber.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_budgets import mixins as budgets_mixins
                
                subscriber_property = budgets_mixins.CfnBudgetsActionPropsMixin.SubscriberProperty(
                    address="address",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9594776ec8c440be0a2debf97b46b6d78302914ba04c8ecfc766e7809628f09f)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def address(self) -> typing.Optional[builtins.str]:
            '''The address that AWS sends budget notifications to, either an SNS topic or an email.

            When you create a subscriber, the value of ``Address`` can't contain line breaks.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-subscriber.html#cfn-budgets-budgetsaction-subscriber-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of notification that AWS sends to a subscriber.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budgetsaction-subscriber.html#cfn-budgets-budgetsaction-subscriber-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubscriberProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnBudgetMixinProps",
    "CfnBudgetPropsMixin",
    "CfnBudgetsActionMixinProps",
    "CfnBudgetsActionPropsMixin",
]

publication.publish()

def _typecheckingstub__7a670285d7a75dfd9e8a053ae8b8952f00601c21cf19624807962ec497be22ff(
    *,
    budget: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetPropsMixin.BudgetDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    notifications_with_subscribers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetPropsMixin.NotificationWithSubscribersProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetPropsMixin.ResourceTagProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b8e854c14fdefff6bcffac29e2897448fcdeac96af7fba191ceb9b7966def12(
    props: typing.Union[CfnBudgetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b75cdcb2badf38f563ac1e13478c899547efe58eb1ca63f7c6478fab32cfcad(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__debccf0b401c580cd1db020994e343f2d6a62e42e9b964389157c789d7486ba3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70962bf28ad60232de8e1843e1e037d70bedece14b01412f9e4a560a59303f9d(
    *,
    auto_adjust_type: typing.Optional[builtins.str] = None,
    historical_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetPropsMixin.HistoricalOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db31e71da825d1a062880048db3e9576512bfb75e5234891c324f2fd3399583(
    *,
    auto_adjust_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetPropsMixin.AutoAdjustDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    billing_view_arn: typing.Optional[builtins.str] = None,
    budget_limit: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetPropsMixin.SpendProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    budget_name: typing.Optional[builtins.str] = None,
    budget_type: typing.Optional[builtins.str] = None,
    cost_filters: typing.Any = None,
    cost_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetPropsMixin.CostTypesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    filter_expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetPropsMixin.ExpressionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metrics: typing.Optional[typing.Sequence[builtins.str]] = None,
    planned_budget_limits: typing.Any = None,
    time_period: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetPropsMixin.TimePeriodProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    time_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff0ea6b99b8415f284db820d74b2108b39861316f2254691a6814e3ed77c0a9b(
    *,
    key: typing.Optional[builtins.str] = None,
    match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e594110be42d7dfa671d0b9f9a0890dc6292612082f69042353c9accdab0c372(
    *,
    include_credit: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_discount: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_other_subscription: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_recurring: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_refund: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_subscription: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_support: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_tax: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_upfront: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    use_amortized: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    use_blended: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4175ad612bf07e1f1ae684b0a52a8e1c3ab24cd1f9bdc9862497259e0a8acb6(
    *,
    key: typing.Optional[builtins.str] = None,
    match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967237f3dac9c5234d555e9f04267f5f1826c3722158c55ab9bea71e7826b772(
    *,
    and_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetPropsMixin.ExpressionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    cost_categories: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetPropsMixin.CostCategoryValuesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetPropsMixin.ExpressionDimensionValuesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    not_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetPropsMixin.ExpressionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    or_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetPropsMixin.ExpressionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Union[CfnBudgetPropsMixin.TagValuesProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12aeb586b22de12ca280d83e36ec4c0311360186658f5c8481a142a725a8729c(
    *,
    budget_adjustment_period: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03bc5222edad586b8094ed89be2482508cc0ca665e924eda73377093920de642(
    *,
    comparison_operator: typing.Optional[builtins.str] = None,
    notification_type: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
    threshold_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e5db20c874699ae3c6d1ece1d8ff694baea7a6ea8681db95bab95166a431f0(
    *,
    notification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetPropsMixin.NotificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    subscribers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetPropsMixin.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6070f206525027f1172b4ea4d00409d4df47ba3e697840561eaa4b01fd3e8a41(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880c58d2acd9c23e29a9d0838a18cffa64908f3f99c7e7a97f83ca53eb0295e9(
    *,
    amount: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce26fe79aa46476ded0165fe2b965c53c8345329959493c1430578cb6b8abd80(
    *,
    address: typing.Optional[builtins.str] = None,
    subscription_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2dfc451346cea3a1deb0a70963996549da4236697830e7ee1607561b787cf90(
    *,
    key: typing.Optional[builtins.str] = None,
    match_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c48c7b6b4276dcc966f9a8c7807c886573e5b087c203931e2af25f65577690(
    *,
    end: typing.Optional[builtins.str] = None,
    start: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0200f40c9e9e6a7e264d6d846bfd64414a5275a2c8d0fffd49c40e1f13dd1e6(
    *,
    action_threshold: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetsActionPropsMixin.ActionThresholdProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    action_type: typing.Optional[builtins.str] = None,
    approval_model: typing.Optional[builtins.str] = None,
    budget_name: typing.Optional[builtins.str] = None,
    definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetsActionPropsMixin.DefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    notification_type: typing.Optional[builtins.str] = None,
    resource_tags: typing.Optional[typing.Sequence[typing.Union[CfnBudgetsActionPropsMixin.ResourceTagProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    subscribers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetsActionPropsMixin.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb78e8f7ace20ee4f9926de350cc86891d666bb58175489e276a8e5c057e33e(
    props: typing.Union[CfnBudgetsActionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__568aae79b943e8e49b8e561ec3c3be9d4d45c06974c2877cfa8e3504d7a60a33(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c874671d0370f703ee847c5930eff02b3942af5e5025766e23bf2a47b38e21e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882df1925c14c0d6e27df33924c099b7ba3d66eb7b8064ec492631287fdfb11e(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b9096898e69a7f0c115cd373f9070a8b47a0c79101147fa4618d68e8a610cca(
    *,
    iam_action_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetsActionPropsMixin.IamActionDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scp_action_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetsActionPropsMixin.ScpActionDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ssm_action_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBudgetsActionPropsMixin.SsmActionDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cb2cb7fc1ce7dc37bcb7a6669f2fd4cf63356ab9d9f1d5c738fd7ab833aa465(
    *,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    policy_arn: typing.Optional[builtins.str] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    users: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e79f71611bdd186971ffcb670310ec256e59603cab3fe07a6cc3ef8b803bb8e(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a183107dcca25aa29a1a479ea927c1681d6038c3cd79fb25bb234308235abb43(
    *,
    policy_id: typing.Optional[builtins.str] = None,
    target_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cfe13b3ff924912fe34798f87ae05b3fdb3cb1ae47b476d307bb6eeae125dd0(
    *,
    instance_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    subtype: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9594776ec8c440be0a2debf97b46b6d78302914ba04c8ecfc766e7809628f09f(
    *,
    address: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
