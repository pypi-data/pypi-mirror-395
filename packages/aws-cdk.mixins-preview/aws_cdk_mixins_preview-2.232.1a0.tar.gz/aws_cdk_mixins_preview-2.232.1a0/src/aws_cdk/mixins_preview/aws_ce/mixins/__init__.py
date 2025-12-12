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
    jsii_type="@aws-cdk/mixins-preview.aws_ce.mixins.CfnAnomalyMonitorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "monitor_dimension": "monitorDimension",
        "monitor_name": "monitorName",
        "monitor_specification": "monitorSpecification",
        "monitor_type": "monitorType",
        "resource_tags": "resourceTags",
    },
)
class CfnAnomalyMonitorMixinProps:
    def __init__(
        self,
        *,
        monitor_dimension: typing.Optional[builtins.str] = None,
        monitor_name: typing.Optional[builtins.str] = None,
        monitor_specification: typing.Optional[builtins.str] = None,
        monitor_type: typing.Optional[builtins.str] = None,
        resource_tags: typing.Optional[typing.Sequence[typing.Union["CfnAnomalyMonitorPropsMixin.ResourceTagProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAnomalyMonitorPropsMixin.

        :param monitor_dimension: For customer managed monitors, do not specify this field. For AWS managed monitors, this field controls which cost dimension is automatically analyzed by the monitor. For ``TAG`` and ``COST_CATEGORY`` dimensions, you must also specify MonitorSpecification to configure the specific tag or cost category key to analyze.
        :param monitor_name: The name of the monitor.
        :param monitor_specification: The array of ``MonitorSpecification`` in JSON array format. For instance, you can use ``MonitorSpecification`` to specify a tag, Cost Category, or linked account for your custom anomaly monitor. For further information, see the `Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#aws-resource-ce-anomalymonitor--examples>`_ section of this page.
        :param monitor_type: The type of the monitor. Set this to ``DIMENSIONAL`` for an AWS managed monitor. AWS managed monitors automatically track up to the top 5,000 values by cost within a dimension of your choosing. Each dimension value is evaluated independently. If you start incurring cost in a new value of your chosen dimension, it will automatically be analyzed by an AWS managed monitor. Set this to ``CUSTOM`` for a customer managed monitor. Customer managed monitors let you select specific dimension values that get monitored in aggregate. For more information about monitor types, see `Monitor types <https://docs.aws.amazon.com/cost-management/latest/userguide/getting-started-ad.html#monitor-type-def>`_ in the *Billing and Cost Management User Guide* .
        :param resource_tags: Tags to assign to monitor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ce import mixins as ce_mixins
            
            cfn_anomaly_monitor_mixin_props = ce_mixins.CfnAnomalyMonitorMixinProps(
                monitor_dimension="monitorDimension",
                monitor_name="monitorName",
                monitor_specification="monitorSpecification",
                monitor_type="monitorType",
                resource_tags=[ce_mixins.CfnAnomalyMonitorPropsMixin.ResourceTagProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51027ba76cbf534629f7b9985053f52bb3b7a7efc6aef02481160d55d4da129a)
            check_type(argname="argument monitor_dimension", value=monitor_dimension, expected_type=type_hints["monitor_dimension"])
            check_type(argname="argument monitor_name", value=monitor_name, expected_type=type_hints["monitor_name"])
            check_type(argname="argument monitor_specification", value=monitor_specification, expected_type=type_hints["monitor_specification"])
            check_type(argname="argument monitor_type", value=monitor_type, expected_type=type_hints["monitor_type"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if monitor_dimension is not None:
            self._values["monitor_dimension"] = monitor_dimension
        if monitor_name is not None:
            self._values["monitor_name"] = monitor_name
        if monitor_specification is not None:
            self._values["monitor_specification"] = monitor_specification
        if monitor_type is not None:
            self._values["monitor_type"] = monitor_type
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags

    @builtins.property
    def monitor_dimension(self) -> typing.Optional[builtins.str]:
        '''For customer managed monitors, do not specify this field.

        For AWS managed monitors, this field controls which cost dimension is automatically analyzed by the monitor. For ``TAG`` and ``COST_CATEGORY`` dimensions, you must also specify MonitorSpecification to configure the specific tag or cost category key to analyze.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#cfn-ce-anomalymonitor-monitordimension
        '''
        result = self._values.get("monitor_dimension")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitor_name(self) -> typing.Optional[builtins.str]:
        '''The name of the monitor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#cfn-ce-anomalymonitor-monitorname
        '''
        result = self._values.get("monitor_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitor_specification(self) -> typing.Optional[builtins.str]:
        '''The array of ``MonitorSpecification`` in JSON array format.

        For instance, you can use ``MonitorSpecification`` to specify a tag, Cost Category, or linked account for your custom anomaly monitor. For further information, see the `Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#aws-resource-ce-anomalymonitor--examples>`_ section of this page.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#cfn-ce-anomalymonitor-monitorspecification
        '''
        result = self._values.get("monitor_specification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitor_type(self) -> typing.Optional[builtins.str]:
        '''The type of the monitor.

        Set this to ``DIMENSIONAL`` for an AWS managed monitor. AWS managed monitors automatically track up to the top 5,000 values by cost within a dimension of your choosing. Each dimension value is evaluated independently. If you start incurring cost in a new value of your chosen dimension, it will automatically be analyzed by an AWS managed monitor.

        Set this to ``CUSTOM`` for a customer managed monitor. Customer managed monitors let you select specific dimension values that get monitored in aggregate.

        For more information about monitor types, see `Monitor types <https://docs.aws.amazon.com/cost-management/latest/userguide/getting-started-ad.html#monitor-type-def>`_ in the *Billing and Cost Management User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#cfn-ce-anomalymonitor-monitortype
        '''
        result = self._values.get("monitor_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.List["CfnAnomalyMonitorPropsMixin.ResourceTagProperty"]]:
        '''Tags to assign to monitor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html#cfn-ce-anomalymonitor-resourcetags
        '''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.List["CfnAnomalyMonitorPropsMixin.ResourceTagProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAnomalyMonitorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAnomalyMonitorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ce.mixins.CfnAnomalyMonitorPropsMixin",
):
    '''The ``AWS::CE::AnomalyMonitor`` resource is a Cost Explorer resource type that continuously inspects your account's cost data for anomalies, based on ``MonitorType`` and ``MonitorSpecification`` .

    The content consists of detailed metadata and the current status of the monitor object.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html
    :cloudformationResource: AWS::CE::AnomalyMonitor
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ce import mixins as ce_mixins
        
        cfn_anomaly_monitor_props_mixin = ce_mixins.CfnAnomalyMonitorPropsMixin(ce_mixins.CfnAnomalyMonitorMixinProps(
            monitor_dimension="monitorDimension",
            monitor_name="monitorName",
            monitor_specification="monitorSpecification",
            monitor_type="monitorType",
            resource_tags=[ce_mixins.CfnAnomalyMonitorPropsMixin.ResourceTagProperty(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAnomalyMonitorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CE::AnomalyMonitor``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec92c11e69ec64ac94613d2aeefec798751d4974be7b5c6d53d79072509d5892)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2ae766c1b864333dabecd2e3263735abd7bc15b6fe1cd6ded1f63810913a99d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f29abfae6e91d8c01c79a074da211433d8476677cec28985c9faa05713a67a29)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAnomalyMonitorMixinProps:
        return typing.cast(CfnAnomalyMonitorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ce.mixins.CfnAnomalyMonitorPropsMixin.ResourceTagProperty",
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

            .. epigraph::

               Tagging is supported only for the following Cost Explorer resource types: ```AnomalyMonitor`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_AnomalyMonitor.html>`_ , ```AnomalySubscription`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_AnomalySubscription.html>`_ , ```CostCategory`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_CostCategory.html>`_ .

            :param key: The key that's associated with the tag.
            :param value: The value that's associated with the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-anomalymonitor-resourcetag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ce import mixins as ce_mixins
                
                resource_tag_property = ce_mixins.CfnAnomalyMonitorPropsMixin.ResourceTagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__937eb51a44d829a99deac267673e68a6d79f855957206eea8c7e7cb8f1e43554)
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

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-anomalymonitor-resourcetag.html#cfn-ce-anomalymonitor-resourcetag-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value that's associated with the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-anomalymonitor-resourcetag.html#cfn-ce-anomalymonitor-resourcetag-value
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
    jsii_type="@aws-cdk/mixins-preview.aws_ce.mixins.CfnAnomalySubscriptionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "frequency": "frequency",
        "monitor_arn_list": "monitorArnList",
        "resource_tags": "resourceTags",
        "subscribers": "subscribers",
        "subscription_name": "subscriptionName",
        "threshold": "threshold",
        "threshold_expression": "thresholdExpression",
    },
)
class CfnAnomalySubscriptionMixinProps:
    def __init__(
        self,
        *,
        frequency: typing.Optional[builtins.str] = None,
        monitor_arn_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_tags: typing.Optional[typing.Sequence[typing.Union["CfnAnomalySubscriptionPropsMixin.ResourceTagProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        subscribers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAnomalySubscriptionPropsMixin.SubscriberProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        subscription_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        threshold_expression: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAnomalySubscriptionPropsMixin.

        :param frequency: The frequency that anomaly notifications are sent. Notifications are sent either over email (for DAILY and WEEKLY frequencies) or SNS (for IMMEDIATE frequency). For more information, see `Creating an Amazon SNS topic for anomaly notifications <https://docs.aws.amazon.com/cost-management/latest/userguide/ad-SNS.html>`_ .
        :param monitor_arn_list: A list of cost anomaly monitors.
        :param resource_tags: Tags to assign to subscription.
        :param subscribers: A list of subscribers to notify.
        :param subscription_name: The name for the subscription.
        :param threshold: (deprecated). An absolute dollar value that must be exceeded by the anomaly's total impact (see `Impact <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_Impact.html>`_ for more details) for an anomaly notification to be generated. This field has been deprecated. To specify a threshold, use ThresholdExpression. Continued use of Threshold will be treated as shorthand syntax for a ThresholdExpression. One of Threshold or ThresholdExpression is required for ``AWS::CE::AnomalySubscription`` . You cannot specify both.
        :param threshold_expression: An `Expression <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_Expression.html>`_ object in JSON string format used to specify the anomalies that you want to generate alerts for. This supports dimensions and nested expressions. The supported dimensions are ``ANOMALY_TOTAL_IMPACT_ABSOLUTE`` and ``ANOMALY_TOTAL_IMPACT_PERCENTAGE`` , corresponding to an anomaly’s TotalImpact and TotalImpactPercentage, respectively (see `Impact <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_Impact.html>`_ for more details). The supported nested expression types are ``AND`` and ``OR`` . The match option ``GREATER_THAN_OR_EQUAL`` is required. Values must be numbers between 0 and 10,000,000,000 in string format. One of Threshold or ThresholdExpression is required for ``AWS::CE::AnomalySubscription`` . You cannot specify both. For further information, see the `Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#aws-resource-ce-anomalysubscription--examples>`_ section of this page.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ce import mixins as ce_mixins
            
            cfn_anomaly_subscription_mixin_props = ce_mixins.CfnAnomalySubscriptionMixinProps(
                frequency="frequency",
                monitor_arn_list=["monitorArnList"],
                resource_tags=[ce_mixins.CfnAnomalySubscriptionPropsMixin.ResourceTagProperty(
                    key="key",
                    value="value"
                )],
                subscribers=[ce_mixins.CfnAnomalySubscriptionPropsMixin.SubscriberProperty(
                    address="address",
                    status="status",
                    type="type"
                )],
                subscription_name="subscriptionName",
                threshold=123,
                threshold_expression="thresholdExpression"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc4e5fd0a68db97fc6f9cb31c9d95e57aa3380d5741f2e110a8a122c48fc3d3c)
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument monitor_arn_list", value=monitor_arn_list, expected_type=type_hints["monitor_arn_list"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
            check_type(argname="argument subscribers", value=subscribers, expected_type=type_hints["subscribers"])
            check_type(argname="argument subscription_name", value=subscription_name, expected_type=type_hints["subscription_name"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument threshold_expression", value=threshold_expression, expected_type=type_hints["threshold_expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if frequency is not None:
            self._values["frequency"] = frequency
        if monitor_arn_list is not None:
            self._values["monitor_arn_list"] = monitor_arn_list
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags
        if subscribers is not None:
            self._values["subscribers"] = subscribers
        if subscription_name is not None:
            self._values["subscription_name"] = subscription_name
        if threshold is not None:
            self._values["threshold"] = threshold
        if threshold_expression is not None:
            self._values["threshold_expression"] = threshold_expression

    @builtins.property
    def frequency(self) -> typing.Optional[builtins.str]:
        '''The frequency that anomaly notifications are sent.

        Notifications are sent either over email (for DAILY and WEEKLY frequencies) or SNS (for IMMEDIATE frequency). For more information, see `Creating an Amazon SNS topic for anomaly notifications <https://docs.aws.amazon.com/cost-management/latest/userguide/ad-SNS.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#cfn-ce-anomalysubscription-frequency
        '''
        result = self._values.get("frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitor_arn_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of cost anomaly monitors.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#cfn-ce-anomalysubscription-monitorarnlist
        '''
        result = self._values.get("monitor_arn_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.List["CfnAnomalySubscriptionPropsMixin.ResourceTagProperty"]]:
        '''Tags to assign to subscription.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#cfn-ce-anomalysubscription-resourcetags
        '''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.List["CfnAnomalySubscriptionPropsMixin.ResourceTagProperty"]], result)

    @builtins.property
    def subscribers(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalySubscriptionPropsMixin.SubscriberProperty"]]]]:
        '''A list of subscribers to notify.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#cfn-ce-anomalysubscription-subscribers
        '''
        result = self._values.get("subscribers")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAnomalySubscriptionPropsMixin.SubscriberProperty"]]]], result)

    @builtins.property
    def subscription_name(self) -> typing.Optional[builtins.str]:
        '''The name for the subscription.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#cfn-ce-anomalysubscription-subscriptionname
        '''
        result = self._values.get("subscription_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''(deprecated).

        An absolute dollar value that must be exceeded by the anomaly's total impact (see `Impact <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_Impact.html>`_ for more details) for an anomaly notification to be generated.

        This field has been deprecated. To specify a threshold, use ThresholdExpression. Continued use of Threshold will be treated as shorthand syntax for a ThresholdExpression.

        One of Threshold or ThresholdExpression is required for ``AWS::CE::AnomalySubscription`` . You cannot specify both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#cfn-ce-anomalysubscription-threshold
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def threshold_expression(self) -> typing.Optional[builtins.str]:
        '''An `Expression <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_Expression.html>`_ object in JSON string format used to specify the anomalies that you want to generate alerts for. This supports dimensions and nested expressions. The supported dimensions are ``ANOMALY_TOTAL_IMPACT_ABSOLUTE`` and ``ANOMALY_TOTAL_IMPACT_PERCENTAGE`` , corresponding to an anomaly’s TotalImpact and TotalImpactPercentage, respectively (see `Impact <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_Impact.html>`_ for more details). The supported nested expression types are ``AND`` and ``OR`` . The match option ``GREATER_THAN_OR_EQUAL`` is required. Values must be numbers between 0 and 10,000,000,000 in string format.

        One of Threshold or ThresholdExpression is required for ``AWS::CE::AnomalySubscription`` . You cannot specify both.

        For further information, see the `Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#aws-resource-ce-anomalysubscription--examples>`_ section of this page.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html#cfn-ce-anomalysubscription-thresholdexpression
        '''
        result = self._values.get("threshold_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAnomalySubscriptionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAnomalySubscriptionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ce.mixins.CfnAnomalySubscriptionPropsMixin",
):
    '''The ``AWS::CE::AnomalySubscription`` resource (also referred to as an alert subscription) is a Cost Explorer resource type that sends notifications about specific anomalies that meet an alerting criteria defined by you.

    You can specify the frequency of the alerts and the subscribers to notify.

    Anomaly subscriptions can be associated with one or more ```AWS::CE::AnomalyMonitor`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalymonitor.html>`_ resources, and they only send notifications about anomalies detected by those associated monitors. You can also configure a threshold to further control which anomalies are included in the notifications.

    Anomalies that don’t exceed the chosen threshold and therefore don’t trigger notifications from an anomaly subscription will still be available on the console and from the ```GetAnomalies`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetAnomalies.html>`_ API.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-anomalysubscription.html
    :cloudformationResource: AWS::CE::AnomalySubscription
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ce import mixins as ce_mixins
        
        cfn_anomaly_subscription_props_mixin = ce_mixins.CfnAnomalySubscriptionPropsMixin(ce_mixins.CfnAnomalySubscriptionMixinProps(
            frequency="frequency",
            monitor_arn_list=["monitorArnList"],
            resource_tags=[ce_mixins.CfnAnomalySubscriptionPropsMixin.ResourceTagProperty(
                key="key",
                value="value"
            )],
            subscribers=[ce_mixins.CfnAnomalySubscriptionPropsMixin.SubscriberProperty(
                address="address",
                status="status",
                type="type"
            )],
            subscription_name="subscriptionName",
            threshold=123,
            threshold_expression="thresholdExpression"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAnomalySubscriptionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CE::AnomalySubscription``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c55973d567ff9eb465e87e65d2a48dff3debce6cbf57353532106c78c4f4743b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd06ddc20fa8dd6c30962aa269c268f679928f5429da61ba0ee8b61a03ebc3a2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cb2503a307e7dcd207ac487bf9c021ad7b03269f69d655afd5b3d49578b2f14)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAnomalySubscriptionMixinProps:
        return typing.cast(CfnAnomalySubscriptionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ce.mixins.CfnAnomalySubscriptionPropsMixin.ResourceTagProperty",
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

            .. epigraph::

               Tagging is supported only for the following Cost Explorer resource types: ```AnomalyMonitor`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_AnomalyMonitor.html>`_ , ```AnomalySubscription`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_AnomalySubscription.html>`_ , ```CostCategory`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_CostCategory.html>`_ .

            :param key: The key that's associated with the tag.
            :param value: The value that's associated with the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-anomalysubscription-resourcetag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ce import mixins as ce_mixins
                
                resource_tag_property = ce_mixins.CfnAnomalySubscriptionPropsMixin.ResourceTagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3c4df8a7d987fde31bbd29b0a859c90540fce87fe9ae57103c82e50171951cfb)
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

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-anomalysubscription-resourcetag.html#cfn-ce-anomalysubscription-resourcetag-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value that's associated with the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-anomalysubscription-resourcetag.html#cfn-ce-anomalysubscription-resourcetag-value
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
        jsii_type="@aws-cdk/mixins-preview.aws_ce.mixins.CfnAnomalySubscriptionPropsMixin.SubscriberProperty",
        jsii_struct_bases=[],
        name_mapping={"address": "address", "status": "status", "type": "type"},
    )
    class SubscriberProperty:
        def __init__(
            self,
            *,
            address: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The recipient of ``AnomalySubscription`` notifications.

            :param address: The email address or SNS Topic Amazon Resource Name (ARN), depending on the ``Type`` .
            :param status: Indicates if the subscriber accepts the notifications.
            :param type: The notification delivery channel.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-anomalysubscription-subscriber.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ce import mixins as ce_mixins
                
                subscriber_property = ce_mixins.CfnAnomalySubscriptionPropsMixin.SubscriberProperty(
                    address="address",
                    status="status",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9fa4876077a0bf5dd9be875bc786576590150b63e97a6369af1bffcc67a0ca6e)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address
            if status is not None:
                self._values["status"] = status
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def address(self) -> typing.Optional[builtins.str]:
            '''The email address or SNS Topic Amazon Resource Name (ARN), depending on the ``Type`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-anomalysubscription-subscriber.html#cfn-ce-anomalysubscription-subscriber-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Indicates if the subscriber accepts the notifications.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-anomalysubscription-subscriber.html#cfn-ce-anomalysubscription-subscriber-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The notification delivery channel.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-anomalysubscription-subscriber.html#cfn-ce-anomalysubscription-subscriber-type
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


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ce.mixins.CfnCostCategoryMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_value": "defaultValue",
        "name": "name",
        "rules": "rules",
        "rule_version": "ruleVersion",
        "split_charge_rules": "splitChargeRules",
        "tags": "tags",
    },
)
class CfnCostCategoryMixinProps:
    def __init__(
        self,
        *,
        default_value: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        rules: typing.Optional[builtins.str] = None,
        rule_version: typing.Optional[builtins.str] = None,
        split_charge_rules: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnCostCategoryPropsMixin.ResourceTagProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCostCategoryPropsMixin.

        :param default_value: The default value for the cost category.
        :param name: The unique name of the Cost Category.
        :param rules: The array of CostCategoryRule in JSON array format. .. epigraph:: Rules are processed in order. If there are multiple rules that match the line item, then the first rule to match is used to determine that Cost Category value.
        :param rule_version: The rule schema version in this particular Cost Category.
        :param split_charge_rules: The split charge rules that are used to allocate your charges between your Cost Category values.
        :param tags: Tags to assign to the cost category.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ce import mixins as ce_mixins
            
            cfn_cost_category_mixin_props = ce_mixins.CfnCostCategoryMixinProps(
                default_value="defaultValue",
                name="name",
                rules="rules",
                rule_version="ruleVersion",
                split_charge_rules="splitChargeRules",
                tags=[ce_mixins.CfnCostCategoryPropsMixin.ResourceTagProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25a36b51c1cdb71fd4d21171b07a5b79634eed2f3f092d15f1adca858ffbf88e)
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument rule_version", value=rule_version, expected_type=type_hints["rule_version"])
            check_type(argname="argument split_charge_rules", value=split_charge_rules, expected_type=type_hints["split_charge_rules"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_value is not None:
            self._values["default_value"] = default_value
        if name is not None:
            self._values["name"] = name
        if rules is not None:
            self._values["rules"] = rules
        if rule_version is not None:
            self._values["rule_version"] = rule_version
        if split_charge_rules is not None:
            self._values["split_charge_rules"] = split_charge_rules
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def default_value(self) -> typing.Optional[builtins.str]:
        '''The default value for the cost category.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-defaultvalue
        '''
        result = self._values.get("default_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The unique name of the Cost Category.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules(self) -> typing.Optional[builtins.str]:
        '''The array of CostCategoryRule in JSON array format.

        .. epigraph::

           Rules are processed in order. If there are multiple rules that match the line item, then the first rule to match is used to determine that Cost Category value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-rules
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_version(self) -> typing.Optional[builtins.str]:
        '''The rule schema version in this particular Cost Category.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-ruleversion
        '''
        result = self._values.get("rule_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def split_charge_rules(self) -> typing.Optional[builtins.str]:
        '''The split charge rules that are used to allocate your charges between your Cost Category values.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-splitchargerules
        '''
        result = self._values.get("split_charge_rules")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnCostCategoryPropsMixin.ResourceTagProperty"]]:
        '''Tags to assign to the cost category.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnCostCategoryPropsMixin.ResourceTagProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCostCategoryMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCostCategoryPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ce.mixins.CfnCostCategoryPropsMixin",
):
    '''The ``AWS::CE::CostCategory`` resource creates groupings of cost that you can use across products in the Billing and Cost Management console, such as Cost Explorer and AWS Budgets.

    For more information, see `Managing Your Costs with Cost Categories <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-cost-categories.html>`_ in the *Billing and Cost Management User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html
    :cloudformationResource: AWS::CE::CostCategory
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ce import mixins as ce_mixins
        
        cfn_cost_category_props_mixin = ce_mixins.CfnCostCategoryPropsMixin(ce_mixins.CfnCostCategoryMixinProps(
            default_value="defaultValue",
            name="name",
            rules="rules",
            rule_version="ruleVersion",
            split_charge_rules="splitChargeRules",
            tags=[ce_mixins.CfnCostCategoryPropsMixin.ResourceTagProperty(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCostCategoryMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CE::CostCategory``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__993875ba66ca82ed721c788fd5aaa8a81d177a7f8081c59ee1217b08b24d734b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ae00113f92631c186271dc267f17e51747a5e8d53b1a806a3ca932469e7ad0f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cac0a319d3c872ac9b3372c45d0a31281859c92f64b49a4196a9aa0cd8518e8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCostCategoryMixinProps:
        return typing.cast(CfnCostCategoryMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ce.mixins.CfnCostCategoryPropsMixin.ResourceTagProperty",
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

            .. epigraph::

               Tagging is supported only for the following Cost Explorer resource types: ```AnomalyMonitor`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_AnomalyMonitor.html>`_ , ```AnomalySubscription`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_AnomalySubscription.html>`_ , ```CostCategory`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_CostCategory.html>`_ .

            :param key: The key that's associated with the tag.
            :param value: The value that's associated with the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-costcategory-resourcetag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ce import mixins as ce_mixins
                
                resource_tag_property = ce_mixins.CfnCostCategoryPropsMixin.ResourceTagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eea833b80215fd30e32a5cbca4892d589a2774e9c7f68b75bba0a55da887c373)
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

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-costcategory-resourcetag.html#cfn-ce-costcategory-resourcetag-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value that's associated with the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ce-costcategory-resourcetag.html#cfn-ce-costcategory-resourcetag-value
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


__all__ = [
    "CfnAnomalyMonitorMixinProps",
    "CfnAnomalyMonitorPropsMixin",
    "CfnAnomalySubscriptionMixinProps",
    "CfnAnomalySubscriptionPropsMixin",
    "CfnCostCategoryMixinProps",
    "CfnCostCategoryPropsMixin",
]

publication.publish()

def _typecheckingstub__51027ba76cbf534629f7b9985053f52bb3b7a7efc6aef02481160d55d4da129a(
    *,
    monitor_dimension: typing.Optional[builtins.str] = None,
    monitor_name: typing.Optional[builtins.str] = None,
    monitor_specification: typing.Optional[builtins.str] = None,
    monitor_type: typing.Optional[builtins.str] = None,
    resource_tags: typing.Optional[typing.Sequence[typing.Union[CfnAnomalyMonitorPropsMixin.ResourceTagProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec92c11e69ec64ac94613d2aeefec798751d4974be7b5c6d53d79072509d5892(
    props: typing.Union[CfnAnomalyMonitorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ae766c1b864333dabecd2e3263735abd7bc15b6fe1cd6ded1f63810913a99d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f29abfae6e91d8c01c79a074da211433d8476677cec28985c9faa05713a67a29(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937eb51a44d829a99deac267673e68a6d79f855957206eea8c7e7cb8f1e43554(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc4e5fd0a68db97fc6f9cb31c9d95e57aa3380d5741f2e110a8a122c48fc3d3c(
    *,
    frequency: typing.Optional[builtins.str] = None,
    monitor_arn_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_tags: typing.Optional[typing.Sequence[typing.Union[CfnAnomalySubscriptionPropsMixin.ResourceTagProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    subscribers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAnomalySubscriptionPropsMixin.SubscriberProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    subscription_name: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
    threshold_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55973d567ff9eb465e87e65d2a48dff3debce6cbf57353532106c78c4f4743b(
    props: typing.Union[CfnAnomalySubscriptionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd06ddc20fa8dd6c30962aa269c268f679928f5429da61ba0ee8b61a03ebc3a2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb2503a307e7dcd207ac487bf9c021ad7b03269f69d655afd5b3d49578b2f14(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4df8a7d987fde31bbd29b0a859c90540fce87fe9ae57103c82e50171951cfb(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa4876077a0bf5dd9be875bc786576590150b63e97a6369af1bffcc67a0ca6e(
    *,
    address: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a36b51c1cdb71fd4d21171b07a5b79634eed2f3f092d15f1adca858ffbf88e(
    *,
    default_value: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    rules: typing.Optional[builtins.str] = None,
    rule_version: typing.Optional[builtins.str] = None,
    split_charge_rules: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnCostCategoryPropsMixin.ResourceTagProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__993875ba66ca82ed721c788fd5aaa8a81d177a7f8081c59ee1217b08b24d734b(
    props: typing.Union[CfnCostCategoryMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae00113f92631c186271dc267f17e51747a5e8d53b1a806a3ca932469e7ad0f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cac0a319d3c872ac9b3372c45d0a31281859c92f64b49a4196a9aa0cd8518e8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea833b80215fd30e32a5cbca4892d589a2774e9c7f68b75bba0a55da887c373(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
